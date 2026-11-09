#!/usr/bin/env python3
"""nb.py - the niche-bend harness runner. Stdlib only.

One entry point around the niche-bending-youtube-analyzer skill (same plugin).
Data goes to ./niche-bend/ in the current project (override with NB_WORK).
It does not rewrite the scouting scripts; it calls them, records what it called, and keeps
the state on disk so a killed session can resume.

  nb.py init [--examples]                         create ./niche-bend/ (harness, format-lab, own no-go.md)
  nb.py status                                    run pointer, modes, gate, next action
  nb.py ingest <round-folder>                     convert a format-lab round into candidates/verdicts/points
  nb.py discover [--seeds F] [--dry-run]          formulas + spread sweep, dedupe, runs/<date>/candidates.json
  nb.py validate [--ids a,b] --verifier ID        scorecard rows -> runs/<run>/verdicts.json (awaiting reconciler)
  nb.py validate --reconcile F --reconciler ID    reconciler decisions; refused when ID proposed or verified
  nb.py keep <ids> --note TEXT --by WHO           the only writer of keeps.json (human at a TTY = kept, else proposed)
  nb.py adapt                                     kept ids only -> runs/<date>/packages.json skeleton
  nb.py deliver                                   packages -> runs/<run>/delivery/BRIEF-<id>.md
  nb.py points [--json] [--round R] [--verdict V] the points[] for the 3D board
  nb.py rails [--dry-run]                         discover -> validate (scorecards) -> stop at the keeps gate

Rules this file enforces (SPEC.md, references/cross-verification.md):
  * keeps.json is written only by 'keep'; an agent call is recorded as 'proposed', never 'kept'.
  * a reconciler can not be the proposer or the verifier of the candidate (no self-certification).
  * every run appends to runs/<run>/ledger.json: queries, limits, errors, dropped + reasons, artifacts.
  * a failed mode writes status 'blocked' and stops. No silent retries.
  * a missing number is null with a reason. Nothing is filled in to make a point look complete.
"""
import argparse, json, math, os, re, subprocess, sys
from datetime import date, datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN_SKILLS = os.path.abspath(os.path.join(HERE, '..', '..'))      # the plugin's skills/ folder
# Data lives in the user's project, never inside the plugin (plugin updates replace the plugin folder).
WORK = os.path.abspath(os.environ.get('NB_WORK') or os.path.join(os.getcwd(), 'niche-bend'))
HOME = os.environ.get('NB_HOME', os.path.join(WORK, 'harness'))         # state.json, keeps.json, runs/
ROOT = os.environ.get('NB_ROOT', os.path.dirname(WORK))                 # project root; paths in state are relative to it
SKILL = os.environ.get('NB_SKILL', os.path.join(PLUGIN_SKILLS, 'niche-bending-youtube-analyzer'))
SCOUT = os.path.join(SKILL, 'scripts', 'yt_scout.py')
FORMAT_LAB = os.environ.get('NB_FORMAT_LAB', os.path.join(WORK, 'format-lab'))
EXAMPLES = os.path.join(HERE, 'examples', 'format-lab')


def nogo_path():
    """The project's own no-go list (it grows after every keep round); the plugin's copy until init made one."""
    own = os.path.join(WORK, 'no-go.md')
    return own if os.path.exists(own) else os.path.join(SKILL, 'references', 'no-go.md')


SCHEMA = 'nb-state/1'
MODES = ['ingest', 'discover', 'validate', 'adapt', 'deliver', 'rails']


class Refused(Exception):
    """A rule of the harness says no. Printed as-is, exit code 2."""


# ---------------------------------------------------------------- small helpers

def today():
    return os.environ.get('NB_TODAY') or date.today().isoformat()


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def p(*parts):
    return os.path.join(HOME, *parts)


def rel(path):
    """Repo-relative path for anything stored in state (no absolute user paths in the data)."""
    try:
        return os.path.relpath(path, ROOT)
    except ValueError:
        return path


def read_json(path, default=None):
    if not path or not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write('\n')
    os.replace(tmp, path)


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', (s or '').lower()).strip('-')


def norm_words(s):
    """Wording for dedupe: lower case, apostrophes dropped, gaps ([x], _, ...) and numbers removed."""
    s = (s or '').lower().replace('\u2019', "'").replace("'", '')
    s = re.sub(r'\[[^\]]*\]|_|\u2026|\.\.\.', ' ', s)
    s = re.sub(r'\d+', ' ', s)
    stop = set('a an the of in on to and or for with at by from is are was every all your you n'.split())
    return [w for w in re.findall(r'[a-z]+', s) if w not in stop]


def same_wording(a, b, threshold=0.6):
    wa, wb = set(norm_words(a)), set(norm_words(b))
    if len(wa) < 2 or len(wb) < 2:
        return wa == wb and bool(wa)
    if wa <= wb or wb <= wa:
        return True
    return len(wa & wb) / len(wa | wb) >= threshold


def is_human_tty():
    """A keep is a human click: a channel owner at a terminal, or an owner's click on the 3D board.
    The board server holds a per-start secret (<NB_HOME>/.board-token, 0600) and passes it as
    NB_BOARD_TOKEN; agents never get it. NB_AGENT always marks an agent call."""
    if os.environ.get('NB_AGENT'):
        return False
    tok = os.environ.get('NB_BOARD_TOKEN')
    if tok:
        try:
            with open(p('.board-token')) as fh:
                return tok == fh.read().strip()
        except OSError:
            return False
    return sys.stdin.isatty() and sys.stdout.isatty()


# ---------------------------------------------------------------- state + ledger

def load_state():
    st = read_json(p('state.json'))
    if st is None:
        st = {'schema': SCHEMA, 'updatedAt': None, 'run': None,
              'modes': {m: {'status': 'not run', 'artifact': None, 'at': None, 'error': None} for m in MODES},
              'gate': {'kept': 0, 'proposed': 0, 'file': 'keeps.json'},
              'rounds': [], 'points': []}
    return st


def save_state(st):
    st['updatedAt'] = now_iso()
    keeps = load_keeps()
    st['gate'] = {'kept': sum(k['status'] == 'kept' for k in keeps['entries']),
                  'proposed': sum(k['status'] == 'proposed' for k in keeps['entries']), 'file': 'keeps.json'}
    write_json(p('state.json'), st)


def set_mode(st, mode, status, artifact=None, error=None, run=None):
    st['modes'][mode] = {'status': status, 'artifact': artifact, 'at': now_iso(), 'error': error}
    if run:
        st['run'] = {'id': run, 'path': rel(p('runs', run)), 'lastMode': mode}


def ledger_append(run, entry):
    path = p('runs', run, 'ledger.json')
    led = read_json(path, {'run': run, 'entries': []})
    entry.setdefault('at', now_iso())
    led['entries'].append(entry)
    write_json(path, led)
    return path


def run_dirs():
    return sorted(os.listdir(p('runs'))) if os.path.isdir(p('runs')) else []


def last_complete(name):
    """The newest runs/<run>/<name> with status complete. Resume reads from here."""
    for run in reversed(run_dirs()):
        d = read_json(p('runs', run, name))
        if d and d.get('status') == 'complete':
            return run, d
    return None, None


def load_keeps():
    return read_json(p('keeps.json'), {'note': 'Written only by nb.py keep. status kept = a human at a terminal; '
                                               'proposed = an agent or a non-interactive call. ADAPT reads kept only.',
                                       'entries': []})


# ---------------------------------------------------------------- axes (see skill/references/axes.md)

DEMAND_FLOOR, DEMAND_CEIL = 10_000, 3_000_000


def axis_demand(month):
    """X. log10 of the top on-topic view count this month, same query wording per target. 10K -> 0, 3M -> 100."""
    top = (month or {}).get('topViews')
    if top is None:
        return None, 'no month summary for this target'
    if top <= 0:
        return 0, 'nothing on this wording this month'
    v = (math.log10(top) - math.log10(DEMAND_FLOOR)) / (math.log10(DEMAND_CEIL) - math.log10(DEMAND_FLOOR))
    return round(max(0, min(1, v)) * 100), 'log10(month topViews %d), 10K=0, 3M=100' % top


def axis_saturation(month):
    """Y. Channels with a video over 50K on the topic this month, plus channels that did it twice or more."""
    if not month or month.get('channelsOver50K') is None:
        return None, 'no month summary for this target'
    c, r = month['channelsOver50K'], month.get('channelsWith2PlusOver50K') or 0
    v = 0.7 * min(c, 8) / 8 + 0.3 * min(r, 3) / 3
    return round(v * 100), '0.7*min(channelsOver50K %d,8)/8 + 0.3*min(repeat channels %d,3)/3' % (c, r)


MAKE_RULES = [('presenter', 0.2, 'presenter inside: packaging only'),
              ('footage', 0.5, 'footage inside: needs a restyle to be ours'),
              ('generated', 0.8, 'generated stills: makeable, monetisation risk'),
              ('archive', 0.6, 'archive photos: makeable as stills, real people and rights to check'),
              ('2d', 1.0, '2D drawn'), ('cartoon', 1.0, '2D drawn'), ('diagram', 1.0, '2D drawn'),
              ('cutout', 1.0, 'cutouts'), ('canvas', 1.0, 'cutouts on canvas'),
              ('illustrated', 1.0, 'illustrated stills'), ('stills', 0.9, 'stills')]


def axis_fit(visual_tag, month, proof):
    """Z. makeability (from the card's visual line, read from frames) x audience signal. Inferred, not observed."""
    tag = (visual_tag or '').lower()
    make = next(((v, why) for k, v, why in MAKE_RULES if k in tag), (None, None))
    if make[0] is None:
        return None, 'no visual line on the card to judge makeability'
    aud, why = 0.5, ['audience unknown = 0.5']
    if month and (month.get('smallChannelHits') or 0) >= 1:
        aud += 0.25; why.append('+0.25 small channel over 50K on the topic this month')
    if proof and proof.get('subs') and proof['subs'] < 100_000 and (proof.get('views') or 0) >= 100_000:
        aud += 0.25; why.append('+0.25 proof video over 100K from a channel under 100K subs')
    return round(make[0] * aud * 100), 'make %.1f (%s) x audience %.2f (%s)' % (make[0], make[1], aud, '; '.join(why))


def freshness(checked_at, as_of=None):
    """Point size. Half-life 30 days from the day the numbers were read."""
    if not checked_at:
        return None
    days = (date.fromisoformat(as_of or today()) - date.fromisoformat(checked_at[:10])).days
    return round(0.5 ** (max(0, days) / 30), 2)


VERDICTS = {  # round verdict -> (board verdict, class, confidence once reconciled)
    'confirmed': ('confirmed', 'support', 0.8), 'proven': ('confirmed', 'support', 0.8),
    'open': ('open', 'support', 0.65), 'contested': ('contested', 'uncertain', 0.45),
    'untested': ('untested', 'uncertain', 0.35), 'format only': ('format only', 'uncertain', 0.35),
    'crowded': ('crowded', 'against', 0.25), 'weak': ('weak', 'against', 0.2),
    'pass': ('pass', 'against', 0.1), 'reject': ('pass', 'against', 0.1)}
UNRECONCILED = 0.75   # every ingested round verdict was written by one agent (cross-verification.md)


def verdict_fields(raw, reconciled=False):
    v, cls, conf = VERDICTS.get((raw or '').strip().lower(), ('untested', 'uncertain', 0.3))
    return v, cls, round(conf if reconciled else conf * UNRECONCILED, 2)


# ---------------------------------------------------------------- no-go + previous rounds (dedupe)

def nogo_entries():
    out = []
    nogo = nogo_path()
    if not os.path.exists(nogo):
        return out
    with open(nogo) as fh:
        lines = fh.read().splitlines()
    for line in lines:
        if line.startswith('|') and not set(line.strip()) <= set('|-: '):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if cells and cells[0] and cells[0] not in ('Out', 'Channel', 'Out for cars', 'Dropped'):
                out.append({'wording': re.sub(r'[*]', '', cells[0]), 'reason': 'no-go.md: ' + ' | '.join(cells[1:])[:160]})
    return out


def previous_formats():
    """Every format a previous round already carried or dropped, and every point already in state."""
    seen = []
    if os.path.isdir(FORMAT_LAB):
        for rd in sorted(os.listdir(FORMAT_LAB)):
            lab = read_json(os.path.join(FORMAT_LAB, rd, 'lab.json'))
            if lab:
                for f in lab.get('formats', []):
                    for w in (f.get('formula'), f.get('name')):
                        if w: seen.append({'wording': w, 'reason': 'carried in format-lab round %s (%s)' % (rd, f['key'])})
            md = os.path.join(FORMAT_LAB, rd, 'ROUND.md')
            if os.path.exists(md):
                with open(md) as fh:
                    block = fh.read().split('## Dropped', 1)
                if len(block) == 2:
                    for m in re.finditer(r'^\|\s*"([^"]+)"', block[1], re.M):
                        seen.append({'wording': m.group(1), 'reason': 'dropped in format-lab round %s (ROUND.md)' % rd})
    for f in (load_state().get('points') or []):
        if not f.get('merge'):
            seen.append({'wording': f.get('format') or '', 'reason': 'already a point (%s, round %s)' % (f['id'], f.get('round'))})
    return seen


def dedupe(wordings, recheck=()):
    """Split candidate wordings into kept and dropped. 'recheck' names wordings to keep anyway (new evidence)."""
    blockers = nogo_entries() + previous_formats()
    kept, dropped = [], []
    for w in wordings:
        hit = next((b for b in blockers if same_wording(w, b['wording'])), None)
        if hit and w not in recheck:
            dropped.append({'wording': w, 'reason': hit['reason'], 'matched': hit['wording']})
        else:
            kept.append(w)
    return kept, dropped


# ---------------------------------------------------------------- ingest

def ingest(folder, st=None):
    folder = os.path.abspath(folder)
    rd = os.path.basename(folder.rstrip('/'))
    lab = read_json(os.path.join(folder, 'lab.json')) or read_json(os.path.join(folder, 'spec.json'))
    if not lab:
        raise Refused('no lab.json or spec.json in %s' % folder)
    checks = read_json(os.path.join(folder, 'checks.json'), {})
    checked_at = lab.get('date') or rd
    run = '%s-ingest' % rd
    st = st or load_state()
    img = os.path.join(folder, 'img')

    def thumb(vid):
        if not vid:
            return None
        f = os.path.join(img, vid + '.jpg')
        return rel(f) if os.path.exists(f) else 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % vid

    def frames(vid):
        return [rel(os.path.join(img, '%s_%d.jpg' % (vid, i))) for i in (1, 2, 3)
                if vid and os.path.exists(os.path.join(img, '%s_%d.jpg' % (vid, i)))]

    candidates, verdicts, points, missing = [], [], [], []
    taken = {q['id'] for q in st['points'] if q.get('round') != rd}
    author = 'format-lab round author (agent)'
    for f in lab.get('formats', []):
        src = f.get('source') or {}
        candidates.append({'id': f['key'], 'kind': 'format', 'format': f.get('formula') or f.get('name'),
                           'name': f.get('name'), 'niche': f.get('niche'), 'proposedBy': author,
                           'source': {'id': src.get('id'), 'title': src.get('title'), 'views': src.get('views'),
                                      'handle': src.get('handle'), 'subs': src.get('subs'), 'median': src.get('median'),
                                      'checkedAt': checked_at, 'thumb': thumb(src.get('id'))},
                           'sourceFrames': frames(src.get('id')), 'visualTag': f.get('visualTag'),
                           'thumbnail': f.get('thumbnail'), 'structure': f.get('structure'), 'flags': f.get('flags') or []})
        for t in f.get('targets', []):
            pid = '%s-%s' % (f['key'], slug(t['niche']))
            if pid in taken:
                pid += '-' + rd
            ck = checks.get('%s|%s' % (f['key'], t['niche'])) or {}
            month = t.get('numbers') or (ck.get('summary') or {}).get('month')
            proof = t.get('proof') or {}
            d, dwhy = axis_demand(month)
            s, swhy = axis_saturation(month)
            z, zwhy = axis_fit(f.get('visualTag'), month, proof)
            v, cls, conf = verdict_fields(t.get('verdict'))
            for axis, val, why in (('demand', d, dwhy), ('saturation', s, swhy), ('fit', z, zwhy)):
                if val is None: missing.append({'point': pid, 'axis': axis, 'reason': why})
            cross = t.get('cross') or ck.get('cross') or []
            points.append({
                'id': pid, 'format': f.get('formula') or f.get('name'), 'formatKey': f['key'], 'niche': t['niche'],
                'ourTitle': t.get('title'), 'demand': d, 'saturation': s, 'fit': z,
                'freshness': freshness(checked_at), 'verdict': v, 'verdictRaw': t.get('verdict'),
                'verdictClass': cls, 'confidence': conf, 'reconciled': False,
                'source': {'id': src.get('id'), 'title': src.get('title'), 'views': src.get('views'),
                           'checkedAt': checked_at, 'thumb': thumb(src.get('id'))},
                'proof': ({'id': proof.get('id'), 'title': proof.get('title'), 'views': proof.get('views'),
                           'subs': proof.get('subs'), 'age': proof.get('age'), 'thumb': thumb(proof.get('id'))}
                          if proof.get('id') else None),
                'query': t.get('topic') or ck.get('topic'),
                'evidence': [u for u in ['https://youtu.be/%s' % src.get('id') if src.get('id') else None,
                                         'https://youtu.be/%s' % proof.get('id') if proof.get('id') else None] if u]
                            + [rel(os.path.join(folder, 'checks.json'))],
                'crossSample': [{'id': c.get('id'), 'title': c.get('title'), 'views': c.get('views'), 'age': c.get('age')}
                                for c in cross[:4]],
                'notes': t.get('why'),
                'axes': {'demand': dwhy, 'saturation': swhy, 'fit': zwhy, 'period': 'month',
                         'readOn': checked_at, 'reading': ck.get('reading')},
                'round': rd})
            verdicts.append({'id': pid, 'candidate': f['key'], 'verdict': t.get('verdict'), 'why': t.get('why'),
                             'proposer': author, 'verifier': None, 'reconciler': None, 'reconciled': False,
                             'gate': 'independent gate not passed: single-agent round (cross-verification.md)'})
    for m in lab.get('merges', []):
        v, cls, conf = verdict_fields(m.get('verdict'))
        pk, lk = m.get('packaging') or {}, m.get('look') or {}
        reason = 'merge card: no same-wording topic search was run for it'
        for axis in ('demand', 'saturation', 'fit'):
            missing.append({'point': m['key'], 'axis': axis, 'reason': reason})
        points.append({'id': m['key'], 'format': 'merge: %s + %s' % (pk.get('title'), lk.get('title')), 'formatKey': m['key'],
                       'niche': m.get('niche'), 'ourTitle': m.get('title'), 'demand': None, 'saturation': None, 'fit': None,
                       'freshness': freshness(checked_at), 'verdict': v, 'verdictRaw': m.get('verdict'),
                       'verdictClass': cls, 'confidence': conf, 'reconciled': False,
                       'source': {'id': pk.get('id'), 'title': pk.get('title'), 'views': pk.get('views'),
                                  'checkedAt': checked_at, 'thumb': thumb(pk.get('id'))},
                       'proof': {'id': lk.get('id'), 'title': lk.get('title'), 'views': lk.get('views'), 'thumb': thumb(lk.get('id'))},
                       'query': None, 'evidence': ['https://youtu.be/%s' % x for x in (pk.get('id'), lk.get('id')) if x],
                       'crossSample': [], 'notes': ' '.join(x for x in (m.get('proven'), m.get('unproven')) if x),
                       'axes': {'demand': reason, 'saturation': reason, 'fit': reason, 'readOn': checked_at},
                       'round': rd, 'merge': True})
        verdicts.append({'id': m['key'], 'candidate': m['key'], 'verdict': m.get('verdict'), 'why': m.get('unproven'),
                         'proposer': author, 'verifier': None, 'reconciler': None, 'reconciled': False,
                         'gate': 'independent gate not passed'})

    write_json(p('runs', run, 'candidates.json'), {'status': 'complete', 'run': run, 'from': rel(folder),
                                                   'checkedAt': checked_at, 'candidates': candidates})
    write_json(p('runs', run, 'verdicts.json'), {'status': 'complete', 'run': run, 'from': rel(folder), 'verdicts': verdicts})
    st['points'] = [q for q in st['points'] if q.get('round') != rd] + points
    st['points'].sort(key=lambda q: (q['round'], q['id']))
    st['rounds'] = sorted(set(st.get('rounds', [])) | {rd})
    set_mode(st, 'ingest', 'complete', rel(p('runs', run)), run=run)
    ledger_append(run, {'mode': 'ingest', 'status': 'complete', 'input': rel(folder),
                        'queries': sorted({q['query'] for q in points if q.get('query')}),
                        'limits': 'no network; numbers as read on %s by the round' % checked_at,
                        'errors': [], 'dropped': [], 'missing': missing,
                        'artifacts': {'candidates.json': 'complete', 'verdicts.json': 'complete', 'state.points': len(points)}})
    save_state(st)
    return {'run': run, 'candidates': len(candidates), 'points': len(points), 'missingAxes': len(missing)}


# ---------------------------------------------------------------- discover

def run_scout(args, timeout=1800):
    """Call yt_scout.py. Returns (json or None, error or None). Never retried here."""
    try:
        r = subprocess.run([sys.executable, SCOUT] + args, capture_output=True, text=True, timeout=timeout)
    except Exception as e:
        return None, str(e)[:300]
    if r.returncode != 0:
        return None, (r.stderr or r.stdout)[-300:]
    try:
        return (json.loads(r.stdout) if r.stdout.strip() else None), None
    except ValueError:
        return None, 'unreadable output: ' + r.stdout[:200]


def discover(seeds=None, dry_run=False, top=12, recheck=(), agent=None, run=None):
    st = load_state()
    run = run or today()
    seeds = seeds or os.path.join(SKILL, 'scripts', 'watch_seeds.json')
    agent = agent or os.environ.get('NB_AGENT') or 'scout'
    sd = read_json(seeds)
    if not sd:
        raise Refused('seeds file missing: %s' % seeds)
    plan = [q for qs in sd['niches'].values() for q in qs] + [q.replace('_', ' ') for q in sd['shapes']]
    limits = {'period': 'month', 'minViews': 100000, 'minChannels': 3, 'sorts': ['views', 'relevance'],
              'perQuery': 30, 'spreadTop': top}
    if dry_run:
        blockers = nogo_entries() + previous_formats()
        shapes_kept, shapes_dropped = dedupe(sd['shapes'], recheck)
        led = ledger_append(run, {'mode': 'discover', 'status': 'dry-run', 'dryRun': True, 'agent': agent,
                                  'queries': plan, 'limits': limits, 'errors': [],
                                  'dropped': shapes_dropped, 'dedupeAgainst': len(blockers),
                                  'wouldRun': ['yt_scout.py formulas --seeds %s --out runs/%s/formulas.json' % (rel(seeds), run),
                                               'yt_scout.py spread "<wording>" for the top %d kept wordings' % top],
                                  'artifacts': {'candidates.json': 'not written (dry run)'}})
        return {'dryRun': True, 'queries': len(plan), 'dedupeAgainst': len(blockers),
                'seedShapesAlreadySeen': [d['wording'] for d in shapes_dropped], 'ledger': rel(led)}
    set_mode(st, 'discover', 'running', run=run); save_state(st)
    out = p('runs', run, 'formulas.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    errors, cands = [], []
    fx, err = run_scout(['formulas', '--seeds', seeds, '--out', out], timeout=3600)
    fx = fx or read_json(out)
    if err or not fx:
        errors.append({'step': 'formulas', 'error': err or 'no output'})
        write_json(p('runs', run, 'candidates.json'), {'status': 'blocked', 'run': run, 'errors': errors, 'candidates': []})
        set_mode(st, 'discover', 'blocked', rel(p('runs', run, 'candidates.json')), error=errors[-1]['error'], run=run)
        ledger_append(run, {'mode': 'discover', 'status': 'blocked', 'agent': agent, 'queries': plan, 'limits': limits,
                            'errors': errors, 'dropped': [], 'artifacts': {'formulas.json': 'missing', 'candidates.json': 'blocked'}})
        save_state(st)
        return {'status': 'blocked', 'errors': errors}
    wordings = [w['wording'] for w in fx.get('wordings', [])]
    kept, dropped = dedupe(wordings, recheck)
    by = {w['wording']: w for w in fx['wordings']}
    for w in kept[:top]:
        q = re.sub(r'\bN\b', '_', w)
        sp, e = run_scout(['spread', q])
        if e or not sp:
            errors.append({'step': 'spread', 'wording': w, 'error': e or 'no output'}); continue
        ex = (by[w].get('examples') or [{}])[0]
        cands.append({'id': slug(w), 'kind': 'format', 'format': w, 'proposedBy': agent,
                      'nichesSeen': by[w].get('nichesSeen'), 'inCars': by[w].get('inCars'),
                      'source': {'id': ex.get('id'), 'title': ex.get('title'), 'views': ex.get('views'),
                                 'handle': ex.get('handle'), 'checkedAt': run[:10],
                                 'thumb': 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % ex.get('id') if ex.get('id') else None},
                      'sourceFrames': [], 'spread': {k: sp.get(k) for k in ('month', 'restOfYear', 'monthShare', 'reading')},
                      'freshness': sp.get('monthShare'), 'query': q})
    status = 'complete' if not errors else 'partial'
    write_json(p('runs', run, 'candidates.json'), {'status': status, 'run': run, 'checkedAt': run[:10], 'agent': agent,
                                                   'candidates': cands, 'errors': errors})
    set_mode(st, 'discover', 'complete' if status == 'complete' else 'blocked', rel(p('runs', run, 'candidates.json')),
             error=None if not errors else '%d spread errors' % len(errors), run=run)
    ledger_append(run, {'mode': 'discover', 'status': status, 'agent': agent,
                        'queries': plan + ['spread: ' + c['query'] for c in cands], 'limits': limits, 'errors': errors,
                        'dropped': dropped + [{'wording': w, 'reason': 'below the top %d kept wordings' % top} for w in kept[top:]],
                        'artifacts': {'formulas.json': 'complete', 'candidates.json': status}})
    save_state(st)
    return {'status': status, 'candidates': len(cands), 'dropped': len(dropped), 'errors': len(errors)}


# ---------------------------------------------------------------- validate

CHECKS = ('median50K', 'notOneHit', 'fresh', 'stillPosting', 'viewsAboveSize', 'notTooBig', 'faceless', 'makeable', 'lowMonetisationRisk')


def scorecard(ch):
    """Numeric checks from yt_scout 'channel' output. Faceless/makeable/monetisation need the Frame Reader."""
    k = ch.get('checks') or {}
    subs = ch.get('subs')
    return {'handle': ch.get('handle'), 'subs': subs, 'median': ch.get('medianViews'),
            'median50K': k.get('median50K'), 'notOneHit': k.get('notOneHit'), 'fresh': k.get('firstVideoUnder6Months'),
            'stillPosting': k.get('stillPosting'), 'viewsAboveSize': k.get('freshRatio'),
            'notTooBig': (subs < 100_000) if subs is not None else None,
            'faceless': None, 'makeable': None, 'lowMonetisationRisk': None}


def source_verdict(row, outlier=False):
    """One failed check is enough to demote. Unknown checks keep it Untested, never Proven."""
    failed = [c for c in CHECKS if row.get(c) is False]
    unknown = [c for c in CHECKS if row.get(c) is None]
    if failed:
        return ('Format only' if outlier else 'Pass'), failed, unknown
    if unknown:
        return 'Untested', failed, unknown
    return 'Proven', failed, unknown


def validate(ids=None, verifier=None, channels_json=None, frames_json=None, run=None):
    """Verifier step: scorecard rows. Leaves every row awaiting the reconciler."""
    st = load_state()
    if not verifier:
        raise Refused('--verifier is required (who wrote these scorecard rows)')
    crun, cdoc = last_complete('candidates.json')
    if not cdoc:
        raise Refused('no complete candidates.json in runs/: run discover (or ingest) first')
    run = run or crun
    cands = [c for c in cdoc['candidates'] if not ids or c['id'] in ids]
    if ids and len(cands) != len(ids):
        raise Refused('unknown candidate ids: %s' % ', '.join(sorted(set(ids) - {c['id'] for c in cands})))
    for c in cands:
        if c.get('proposedBy') == verifier:
            raise Refused('self-certification: verifier %s proposed %s' % (verifier, c['id']))
    frames = read_json(frames_json, {}) if frames_json else {}
    errors, rows, chan = [], [], {}
    if channels_json:
        data = read_json(channels_json, [])
        for ch in (data if isinstance(data, list) else data.get('channels', [data])):
            chan[(ch.get('handle') or '').lower()] = ch
    else:
        handles = sorted({c['source'].get('handle') for c in cands if c['source'].get('handle')})
        if handles:
            data, e = run_scout(['channel'] + handles, timeout=1800)
            if e: errors.append({'step': 'channel', 'error': e})
            for ch in (data if isinstance(data, list) else ([data] if data else [])):
                chan[(ch.get('handle') or '').lower()] = ch
    for c in cands:
        ch = chan.get((c['source'].get('handle') or '').lower())
        fr = frames.get(c['id']) or {}
        if not ch:
            rows.append({'id': c['id'], 'proposer': c.get('proposedBy'), 'verifier': verifier, 'scorecard': None,
                         'sourceVerdict': 'Untested', 'failed': [], 'unknown': ['channel data'], 'frameReader': fr.get('by'),
                         'reconciler': None, 'decision': None, 'status': 'awaiting-reconciler'})
            continue
        row = scorecard(ch)
        for k in ('faceless', 'makeable', 'lowMonetisationRisk'):
            if k in fr: row[k] = fr[k]
        med = ch.get('medianViews') or 0
        outlier = bool(c['source'].get('views') and med and c['source']['views'] >= 5 * med)
        sv, failed, unknown = source_verdict(row, outlier)
        rows.append({'id': c['id'], 'proposer': c.get('proposedBy'), 'verifier': verifier, 'scorecard': row,
                     'frameReader': fr.get('by'), 'sourceVerdict': sv, 'failed': failed, 'unknown': unknown,
                     'outlierGene': outlier, 'reconciler': None, 'decision': None, 'status': 'awaiting-reconciler'})
    status = 'partial' if errors else 'awaiting-reconciler'
    write_json(p('runs', run, 'verdicts.json'), {'status': status, 'run': run, 'from': 'runs/%s/candidates.json' % crun,
                                                 'checkedAt': today(), 'verdicts': rows, 'errors': errors})
    set_mode(st, 'validate', 'blocked' if errors else 'awaiting-reconciler', rel(p('runs', run, 'verdicts.json')),
             error=errors[0]['error'] if errors else None, run=run)
    ledger_append(run, {'mode': 'validate', 'step': 'scorecard', 'status': status, 'agent': verifier,
                        'queries': ['yt_scout.py channel ' + ' '.join(sorted(chan))] if chan else [],
                        'limits': 'RSS latest 15 uploads per channel', 'errors': errors, 'dropped': [],
                        'artifacts': {'verdicts.json': status}})
    save_state(st)
    return {'status': status, 'rows': len(rows), 'run': run}


def reconcile(path, reconciler, run=None):
    """Critic/Reconciler step. decisions file: {id: {decision, unresolved[], strongestReason}}."""
    if not reconciler:
        raise Refused('--reconciler is required')
    st = load_state()
    vrun, vdoc = run, (read_json(p('runs', run, 'verdicts.json')) if run else None)
    if not vdoc:
        for r in reversed(run_dirs()):
            d = read_json(p('runs', r, 'verdicts.json'))
            if d and d.get('status') == 'awaiting-reconciler':
                vrun, vdoc = r, d; break
    if not vdoc:
        raise Refused('no verdicts.json awaiting a reconciler')
    decisions = read_json(path)
    if not decisions:
        raise Refused('decisions file missing or empty: %s' % path)
    rows = {r['id']: r for r in vdoc['verdicts']}
    for vid in decisions:
        r = rows.get(vid)
        if not r:
            raise Refused('unknown id in decisions: %s' % vid)
        if reconciler in (r.get('proposer'), r.get('verifier')):
            raise Refused('self-certification: reconciler %s is the %s of %s' % (
                reconciler, 'proposer' if reconciler == r.get('proposer') else 'verifier', vid))
    for vid, d in decisions.items():
        rows[vid].update(reconciler=reconciler, decision=d.get('decision'), unresolved=d.get('unresolved') or [],
                         strongestReason=d.get('strongestReason'), reconciledAt=now_iso(), status='reconciled')
    done = all(r.get('status') == 'reconciled' for r in vdoc['verdicts'])
    vdoc['status'] = 'complete' if done else 'awaiting-reconciler'
    write_json(p('runs', vrun, 'verdicts.json'), vdoc)
    for q in st['points']:
        if q['id'] in decisions:
            v, cls, conf = verdict_fields(decisions[q['id']].get('decision'), reconciled=True)
            q.update(verdict=v, verdictClass=cls, confidence=conf, reconciled=True, reconciler=reconciler)
    set_mode(st, 'validate', 'complete' if done else 'awaiting-reconciler', rel(p('runs', vrun, 'verdicts.json')), run=vrun)
    ledger_append(vrun, {'mode': 'validate', 'step': 'reconcile', 'status': vdoc['status'], 'agent': reconciler,
                         'queries': [], 'limits': None, 'errors': [], 'dropped': [],
                         'artifacts': {'verdicts.json': vdoc['status']}, 'decided': sorted(decisions)})
    save_state(st)
    return {'status': vdoc['status'], 'reconciled': len(decisions)}


# ---------------------------------------------------------------- keep gate

def keep(ids, note, by, human=None):
    if not note:
        raise Refused('--note is required: say why it is kept')
    if not by:
        raise Refused('--by is required: who is keeping it')
    human = is_human_tty() if human is None else human
    st = load_state()
    known = {q['id'] for q in st['points']}
    for r in run_dirs():
        for c in (read_json(p('runs', r, 'candidates.json'), {}) or {}).get('candidates', []):
            known.add(c['id'])
    unknown = [i for i in ids if i not in known]
    if unknown:
        raise Refused('unknown ids (not a point or candidate): %s' % ', '.join(unknown))
    keeps = load_keeps()
    status = 'kept' if human else 'proposed'
    written, skipped = [], []
    for i in ids:
        prev = next((k for k in keeps['entries'] if k['id'] == i), None)
        if prev and prev['status'] == 'kept' and status == 'proposed':
            skipped.append(i); continue   # an agent never overwrites a human keep
        entry = {'id': i, 'status': status, 'by': by, 'at': now_iso(), 'note': note,
                 'via': ('board click (human)' if os.environ.get('NB_BOARD_TOKEN') else 'terminal (human)') if human else 'non-interactive call (agent): a proposal, not a keep'}
        keeps['entries'] = [k for k in keeps['entries'] if k['id'] != i] + [entry]
        written.append(i)
    write_json(p('keeps.json'), keeps)
    save_state(load_state())
    return {'status': status, 'written': written, 'skippedHumanKeeps': skipped}


# ---------------------------------------------------------------- adapt + deliver

def adapt(run=None):
    st = load_state()
    kept = [k for k in load_keeps()['entries'] if k['status'] == 'kept']
    if not kept:
        raise Refused('no kept ids in keeps.json. ADAPT only consumes human keeps; proposals do not count.')
    run = run or today()
    pts = {q['id']: q for q in st['points']}
    cands = {}
    for r in run_dirs():
        for c in (read_json(p('runs', r, 'candidates.json'), {}) or {}).get('candidates', []):
            cands[c['id']] = c
    packages, skipped = [], []
    for k in kept:
        q = pts.get(k['id'])
        c = cands.get(q['formatKey'] if q else k['id'])
        if not q and not c:
            skipped.append({'id': k['id'], 'reason': 'kept id has no point or candidate'}); continue
        base = q or c
        packages.append({
            'id': k['id'], 'keptBy': k['by'], 'keptAt': k['at'],
            'sourceTitle': base['source'].get('title'), 'sourceId': base['source'].get('id'),
            'ourTitle': q.get('ourTitle') if q else None,
            'thumbnail': {'source': (c or {}).get('thumbnail'), 'ours': None},
            'structure': (c or {}).get('structure'),
            'tension': None, 'urgency': None, 'first30': None,
            'adaptation': {'type': 'merge' if q and q.get('merge') else 'bend', 'from': (c or {}).get('niche'),
                           'to': q.get('niche') if q else None, 'keeps': None, 'changes': None},
            'previousAttempts': [dict(a, note='search result on the crossing query; not checked as an exact copy')
                                 for a in (q or {}).get('crossSample', [])],
            'factsToCheck': [], 'evidence': (q or {}).get('evidence', []),
            'status': 'skeleton: the Packager fills ourTitle, thumbnail.ours, tension, urgency, first30, factsToCheck'})
    write_json(p('runs', run, 'packages.json'), {'status': 'skeleton', 'run': run, 'packages': packages, 'skipped': skipped})
    set_mode(st, 'adapt', 'skeleton', rel(p('runs', run, 'packages.json')), run=run)
    ledger_append(run, {'mode': 'adapt', 'status': 'skeleton', 'queries': [], 'limits': None, 'errors': [],
                        'dropped': skipped, 'artifacts': {'packages.json': 'skeleton'}})
    save_state(st)
    return {'status': 'skeleton', 'packages': len(packages), 'run': run}


def deliver(run=None):
    st = load_state()
    prun, doc = run, (read_json(p('runs', run, 'packages.json')) if run else None)
    if not doc:
        for r in reversed(run_dirs()):
            doc = read_json(p('runs', r, 'packages.json'))
            if doc: prun = r; break
    if not doc:
        raise Refused('no packages.json: run adapt after a human keep')
    kept = {k['id'] for k in load_keeps()['entries'] if k['status'] == 'kept'}
    out = []
    for pk in doc['packages']:
        if pk['id'] not in kept:
            continue
        need = [f for f in ('ourTitle', 'tension', 'urgency', 'first30') if not pk.get(f)]
        if not (pk.get('thumbnail') or {}).get('ours'): need.append('thumbnail.ours')
        th = pk.get('thumbnail') or {}
        lines = ['# BRIEF: %s' % pk['id'], '',
                 '**Status:** %s' % ('DRAFT, missing: ' + ', '.join(need) if need else 'ready for production review'),
                 'Kept by %s on %s.' % (pk['keptBy'], pk['keptAt'][:10]), '',
                 '| | Source | Ours |', '|---|---|---|',
                 '| Title | %s | %s |' % (pk.get('sourceTitle'), pk.get('ourTitle') or '-'),
                 '| Thumbnail | %s | %s |' % (th.get('source') or '-', th.get('ours') or '-'),
                 '', '**Structure:** %s' % (pk.get('structure') or '-'),
                 '**Tension:** %s' % (pk.get('tension') or '-'), '**Urgency:** %s' % (pk.get('urgency') or '-'),
                 '**First 30 seconds:** %s' % (pk.get('first30') or '-'), '',
                 'Title, thumbnail and first 30 seconds must make the same promise.', '',
                 '## Previous attempts on the crossing query', '']
        lines += ['- %s, %s views, %s, https://youtu.be/%s' % (a.get('title'), a.get('views'), a.get('age'), a.get('id'))
                  for a in pk.get('previousAttempts', [])] or ['- none recorded']
        lines += ['', '## Facts to check', ''] + (['- ' + f for f in pk.get('factsToCheck', [])] or ['- none listed yet'])
        lines += ['', '## Evidence', ''] + ['- ' + e for e in pk.get('evidence', [])]
        f = p('runs', prun, 'delivery', 'BRIEF-%s.md' % pk['id'])
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, 'w') as fh:
            fh.write('\n'.join(lines) + '\n')
        out.append({'id': pk['id'], 'path': rel(f), 'missing': need})
    status = 'complete' if out and not any(o['missing'] for o in out) else 'draft'
    set_mode(st, 'deliver', status, rel(p('runs', prun, 'delivery')), run=prun)
    ledger_append(prun, {'mode': 'deliver', 'status': status, 'queries': [], 'limits': None, 'errors': [], 'dropped': [],
                         'artifacts': {o['path']: 'draft' if o['missing'] else 'complete' for o in out}})
    save_state(st)
    return {'status': status, 'briefs': out}


# ---------------------------------------------------------------- points + status + rails

def points(round_=None, verdict=None, as_of=None):
    out = []
    for q in load_state()['points']:
        if round_ and q.get('round') != round_: continue
        if verdict and q.get('verdict') != verdict: continue
        q = dict(q); q['freshness'] = freshness(q['source'].get('checkedAt'), as_of)
        out.append(q)
    return out


def status():
    st = load_state()
    pts = st['points']
    placed = [q for q in pts if None not in (q.get('demand'), q.get('saturation'), q.get('fit'))]
    keeps = load_keeps()['entries']
    kept = [k['id'] for k in keeps if k['status'] == 'kept']
    if st['modes']['validate']['status'] == 'awaiting-reconciler':
        nxt = 'spawn the Critic/Reconciler (skill/agents/critic-reconciler.md), then nb.py validate --reconcile F --reconciler ID'
    elif kept and st['modes']['adapt']['status'] == 'not run':
        nxt = 'nb.py adapt (consumes the kept ids)'
    elif not kept:
        nxt = 'keeps gate: a channel owner keeps ids in a terminal: nb.py keep <ids> --note "..." --by <your name>'
    else:
        nxt = 'nb.py rails (discover -> validate) or nb.py ingest <new round folder>'
    return {'schema': st['schema'], 'updatedAt': st['updatedAt'], 'run': st['run'], 'rounds': st.get('rounds', []),
            'modes': {m: v['status'] for m, v in st['modes'].items()},
            'points': {'total': len(pts), 'placed3d': len(placed), 'missingAxis': len(pts) - len(placed),
                       'byVerdict': {v: sum(q['verdict'] == v for q in pts) for v in sorted({q['verdict'] for q in pts})}},
            'gate': {'kept': kept, 'proposed': [k['id'] for k in keeps if k['status'] == 'proposed']},
            'next': nxt}


def rails(dry_run=False, seeds=None):
    run = today()
    r = discover(seeds=seeds, dry_run=dry_run, agent='rails-scout', run=run)
    if dry_run:
        ledger_append(run, {'mode': 'rails', 'status': 'dry-run', 'steps': ['discover (dry run)'],
                            'stoppedAt': 'keeps gate (nothing validated in a dry run)', 'errors': [], 'dropped': [],
                            'queries': [], 'limits': None, 'artifacts': {}})
        return {'dryRun': True, 'discover': r}
    if r.get('status') != 'complete':
        st = load_state(); set_mode(st, 'rails', 'blocked', error='discover %s' % r.get('status'), run=run); save_state(st)
        ledger_append(run, {'mode': 'rails', 'status': 'blocked', 'steps': ['discover'], 'errors': [r],
                            'queries': [], 'limits': None, 'dropped': [], 'artifacts': {}})
        return {'status': 'blocked', 'discover': r}
    v = validate(verifier='nb.py scorecard (mechanical)', run=run)
    st = load_state()
    set_mode(st, 'rails', 'stopped at keeps gate', rel(p('runs', run)), run=run); save_state(st)
    ledger_append(run, {'mode': 'rails', 'status': 'stopped at keeps gate', 'steps': ['discover', 'validate (scorecards)'],
                        'next': ['Frame Reader on candidates', 'Crossing Auditor: format_lab.py check, then nb.py ingest',
                                 'Critic/Reconciler', 'human keep'],
                        'queries': [], 'limits': None, 'errors': [], 'dropped': [], 'artifacts': {}})
    return {'status': 'stopped at keeps gate', 'discover': r, 'validate': v}


# ---------------------------------------------------------------- init (project data folder)

def board_files(made):
    """Install the format-lab board (index.html, server.py, rounds.json, keeps.json) beside the rounds, the way
    format_lab.py build does, so example rounds can be opened before the first live build."""
    import shutil
    assets = os.path.join(SKILL, 'assets', 'format-lab')
    for f in ('index.html', 'server.py'):
        dst = os.path.join(FORMAT_LAB, f)
        if not os.path.exists(dst):
            shutil.copy(os.path.join(assets, f), dst); made.append(rel(dst))
    rounds = sorted((d for d in os.listdir(FORMAT_LAB) if os.path.exists(os.path.join(FORMAT_LAB, d, 'lab.json'))), reverse=True)
    with open(os.path.join(FORMAT_LAB, 'rounds.json'), 'w') as fh:
        json.dump(rounds, fh)
    kp = os.path.join(FORMAT_LAB, 'keeps.json')
    if not os.path.exists(kp):
        with open(kp, 'w') as fh:
            json.dump({'formats': [], 'bends': [], 'merges': []}, fh)


def init(examples=False):
    """Create the project data folder. Safe to re-run: never overwrites state, keeps or the no-go list."""
    import shutil
    made = []
    for d in (HOME, os.path.join(HOME, 'runs'), FORMAT_LAB):
        if not os.path.isdir(d):
            os.makedirs(d); made.append(rel(d))
    own = os.path.join(WORK, 'no-go.md')
    if not os.path.exists(own):
        shutil.copy(os.path.join(SKILL, 'references', 'no-go.md'), own); made.append(rel(own))
    gi = os.path.join(WORK, '.gitignore')
    if not os.path.exists(gi):
        with open(gi, 'w') as fh:
            fh.write('# commit keeps, no-go, specs and lab.json; skip images and per-run secrets\n'
                     '**/img/\n*.jpg\n*.tmp\n.board-token\n__pycache__/\n')
        made.append(rel(gi))
    if not os.path.exists(p('keeps.json')):
        write_json(p('keeps.json'), load_keeps()); made.append(rel(p('keeps.json')))
    ingested = []
    if examples and os.path.isdir(EXAMPLES):
        for rd in sorted(os.listdir(EXAMPLES)):
            dst = os.path.join(FORMAT_LAB, rd)
            if not os.path.isdir(dst):
                shutil.copytree(os.path.join(EXAMPLES, rd), dst); made.append(rel(dst))
            ingest(dst); ingested.append(rd)
        board_files(made)
    st = load_state(); save_state(st)
    return {'work': rel(WORK) if WORK.startswith(ROOT) else WORK, 'created': made, 'ingestedExamples': ingested,
            'next': 'python3 <harness>/nb.py status' + ('' if ingested else '  (or init --examples to load the Oct 2026 rounds)')}


# ---------------------------------------------------------------- CLI

def main(argv=None):
    ap = argparse.ArgumentParser(prog='nb.py', description='niche-bend harness runner')
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('init'); s.add_argument('--examples', action='store_true')
    sub.add_parser('status')
    s = sub.add_parser('ingest'); s.add_argument('folder')
    s = sub.add_parser('discover'); s.add_argument('--seeds'); s.add_argument('--dry-run', action='store_true')
    s.add_argument('--top', type=int, default=12); s.add_argument('--recheck', nargs='*', default=[])
    s.add_argument('--agent')
    s = sub.add_parser('validate'); s.add_argument('--ids'); s.add_argument('--verifier')
    s.add_argument('--channels-json'); s.add_argument('--frames-json'); s.add_argument('--reconcile')
    s.add_argument('--reconciler'); s.add_argument('--run')
    s = sub.add_parser('keep'); s.add_argument('ids', nargs='+'); s.add_argument('--note', required=True)
    s.add_argument('--by', required=True)
    s = sub.add_parser('adapt'); s.add_argument('--run')
    s = sub.add_parser('deliver'); s.add_argument('--run')
    s = sub.add_parser('points'); s.add_argument('--json', action='store_true'); s.add_argument('--round')
    s.add_argument('--verdict')
    s = sub.add_parser('rails'); s.add_argument('--dry-run', action='store_true'); s.add_argument('--seeds')
    a = ap.parse_args(argv)
    try:
        if a.cmd == 'init': r = init(a.examples)
        elif a.cmd == 'status': r = status()
        elif a.cmd == 'ingest': r = ingest(a.folder)
        elif a.cmd == 'discover': r = discover(a.seeds, a.dry_run, a.top, a.recheck, a.agent)
        elif a.cmd == 'validate':
            ids = a.ids.split(',') if a.ids else None
            r = reconcile(a.reconcile, a.reconciler, a.run) if a.reconcile else \
                validate(ids, a.verifier, a.channels_json, a.frames_json, a.run)
        elif a.cmd == 'keep': r = keep([i for x in a.ids for i in x.split(',') if i], a.note, a.by)
        elif a.cmd == 'adapt': r = adapt(a.run)
        elif a.cmd == 'deliver': r = deliver(a.run)
        elif a.cmd == 'points':
            pts = points(a.round, a.verdict)
            if a.json:
                print(json.dumps(pts, ensure_ascii=False, indent=1)); return 0
            for q in pts:
                print('%-40s %-11s D=%-4s S=%-4s F=%-4s %s' % (q['id'][:40], q['verdict'], q['demand'], q['saturation'],
                                                              q['fit'], (q.get('ourTitle') or '')[:60]))
            return 0
        elif a.cmd == 'rails': r = rails(a.dry_run, a.seeds)
    except Refused as e:
        print('REFUSED: %s' % e, file=sys.stderr)
        return 2
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except BrokenPipeError:          # nb.py points --json | head
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(0)
