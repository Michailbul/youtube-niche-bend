#!/usr/bin/env python3
"""Format lab: turn working videos into format cards (A packaging, B niche, C format, D other niches) and check D.

  format_lab.py check <round>/spec.json     demand + crossing numbers for every target niche -> <round>/checks.json
  format_lab.py build <round>/spec.json     pull thumbnails, frames and channel numbers, write <round>/lab.json,
                                            refresh the board (index.html, server.py, rounds.json) one folder up

The spec is written by the agent: see references/format-lab.md for its shape. Both commands can be re-run; check resumes.
"""
import json, os, shutil, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import yt_scout as Y

def thumb(vid, d):
    p = os.path.join(d, vid + '.jpg')
    if not os.path.exists(p):
        for q in ('maxresdefault', 'hq720', 'mqdefault'):
            try:
                b = urllib.request.urlopen('https://i.ytimg.com/vi/%s/%s.jpg' % (vid, q), timeout=20).read()
                if len(b) > 5000: open(p, 'wb').write(b); break
            except Exception: pass
    return p

def check(spec_path):
    spec = json.load(open(spec_path)); rd = os.path.dirname(spec_path); out = os.path.join(rd, 'checks.json')
    done = json.load(open(out)) if os.path.exists(out) else {}
    for f in spec['formats']:
        for t in f['targets']:
            k = f['key'] + '|' + t['niche']
            if k in done: continue
            d = Y.demand(t['topic'], 8)
            cross = {}
            for v in Y.search_videos(t['cross'], 'year', 'relevance', 20):
                if v['id'] and v['views'] and (Y.secs(v['length']) or 0) >= 180: cross[v['id']] = v
            keep = ('id', 'title', 'views', 'age', 'handle', 'channel', 'subs', 'length')
            done[k] = {'topic': t['topic'], 'summary': d['summary'], 'reading': d['reading'],
                       'top': [{x: v.get(x) for x in keep} for v in d['month'][:6]],
                       'cross': [{x: v.get(x) for x in keep} for v in sorted(cross.values(), key=lambda v: -v['views'])[:6]]}
            json.dump(done, open(out, 'w'), indent=1, ensure_ascii=False)
            print(k, '|', d['reading']['demand'], flush=True)

def build(spec_path):
    spec = json.load(open(spec_path)); rd = os.path.dirname(os.path.abspath(spec_path)); img = os.path.join(rd, 'img')
    os.makedirs(img, exist_ok=True)
    cp = os.path.join(rd, 'checks.json'); checks = json.load(open(cp)) if os.path.exists(cp) else {}
    def media(v):
        if v and v.get('id'): thumb(v['id'], img); Y.frames(v['id'], img)
    for f in spec['formats']:
        s = f['source']; media(s)
        if s.get('handle', '').startswith('@') and 'median' not in s:
            c = Y.channel(s['handle'])
            s.update(name=c.get('name'), subs=c.get('subs'), videoCount=c.get('videoCount'), median=c.get('medianViews'), over100K=c.get('over100K'), sample=c.get('sample'))
            for v in c.get('latest', []):
                if v['id'] == s['id']: s.update(views=v['views'], date=v['published'])
            time.sleep(0.4)
        for t in f['targets']:
            c = checks.get(f['key'] + '|' + t['niche'])
            if c:
                t['numbers'] = c['summary']['month']; t['year'] = c['summary']['year']; t['cross'] = c['cross'][:4]
                pid = t.get('proofId')
                t['proof'] = next((v for v in c['top'] + c['cross'] if v['id'] == pid), None) if pid else None
                if t['proof']: thumb(t['proof']['id'], img)
    for e in (spec.get('question') or {}).get('evidence', []): media(e)
    for m in spec.get('merges', []):
        for k in ('packaging', 'look'): media(m.get(k))
    json.dump(spec, open(os.path.join(rd, 'lab.json'), 'w'), indent=1, ensure_ascii=False)
    root = os.path.dirname(rd)
    for f_ in ('index.html', 'server.py'): shutil.copy(os.path.join(HERE, '..', 'assets', 'format-lab', f_), os.path.join(root, f_))
    rp = os.path.join(root, 'rounds.json'); rounds = json.load(open(rp)) if os.path.exists(rp) else []
    name = os.path.basename(rd)
    if name not in rounds: rounds.append(name)
    json.dump(sorted(rounds, reverse=True), open(rp, 'w'))
    kp = os.path.join(root, 'keeps.json')
    if not os.path.exists(kp): json.dump({'formats': [], 'bends': [], 'merges': []}, open(kp, 'w'))
    print(json.dumps({'lab': os.path.join(rd, 'lab.json'), 'formats': len(spec['formats']), 'targets': sum(len(f['targets']) for f in spec['formats']), 'merges': len(spec.get('merges', []))}))

if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] not in ('check', 'build'): sys.exit(__doc__)
    (check if sys.argv[1] == 'check' else build)(sys.argv[2])
