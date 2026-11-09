#!/usr/bin/env python3
"""Build board/sample-state.json for the 3D board while ../state.json does not exist.

Every point is marked sample:true. Inputs:
  - SPEC.md section 4 example point (copied verbatim, plus round/sample fields)
  - ../../format-lab/2026-10-22/lab.json (targets, proof, verdicts)
  - ../../format-lab/2026-10-22/checks.json (the exact query per target)

How the axes were filled (hand derivation, NOT the harness method):
  demand     = 0.7 * log-scale of this month's top views (10K -> 0, 1M -> 100)
               + 0.3 * share of 12 uploads over 100K. Numbers read 22 Oct 2026.
  saturation = hand reading of the round's own "why" notes on the exact crossing.
               null where the crossing search drifted and nothing was read.
  fit        = hand estimate of faceless / 2D-animatable fit by the board builder.
               Not measured. Replace with the Crossing Auditor's numbers.
  freshness  = 1 - source age in days / 60 (age at 22 Oct 2026).
  verdict    = the round-2 proposer's own verdict. Not reconciled.
Run: python3 make_sample.py   (writes sample-state.json next to this file)
"""
import json, math, re, pathlib, datetime

HERE = pathlib.Path(__file__).resolve().parent
ROUND = '2026-10-22'
LAB = HERE.parent.parent / 'format-lab' / ROUND
READ_ON = datetime.date(2026, 10, 22)

SPEC_POINT = {
    "id": "you-wouldnt-last-f1",
    "format": "How Long You'd Last in Every [X]",
    "niche": "Formula 1 eras",
    "ourTitle": "How Long You'd Last in Every Era of Formula 1",
    "demand": 72, "saturation": 18, "fit": 81,
    "freshness": 0.9, "verdict": "open", "confidence": 0.8,
    "source": {"id": "qrfhhZ-Wvmk", "title": "How Long You'd Last in Every Prehistoric Ocean", "views": 2945558, "checkedAt": "2026-10-22"},
    "proof": {"id": "7ROJfkaewpc", "title": "Evolution of Formula 1 Cars (1950\u20132026)", "views": 316084},
    "query": "formula 1 history",
    "evidence": ["https://youtu.be/qrfhhZ-Wvmk", "https://youtu.be/7ROJfkaewpc"],
    "notes": "9 on-topic, 4 over 100K; no F1 video uses the ladder.",
}

# hand readings: (saturation or None, fit, confidence)
HAND = {
    'you-wouldnt-last|Group B rally': (8, 70, 0.3),
    'you-wouldnt-last|Le Mans': (None, 72, 0.3),
    'overdue-collapse|EV startups': (40, 60, 0.7),
    'overdue-collapse|Car dealerships': (15, 75, 0.7),
    'overdue-collapse|Hypercar market': (20, 65, 0.7),
    'shouldnt-exist|Engines': (55, 78, 0.8),
    'shouldnt-exist|Racetracks': (12, 70, 0.7),
    'shouldnt-exist|Concept cars': (70, 55, 0.5),
    'worse-than-thought|Dieselgate': (25, 70, 0.7),
    'worse-than-thought|Car insurance': (22, 68, 0.7),
    'worse-than-thought|Used cars': (35, 72, 0.7),
}
FORMULA = {
    'you-wouldnt-last': "How Long You'd Last in Every [X]",
    'overdue-collapse': 'The (Overdue) Collapse of [X]',
    'shouldnt-exist': "The [X] That Shouldn't Exist",
    'worse-than-thought': '[X] Is Worse Than You Think',
}


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def demand(n):
    top = n.get('topViews') or 0
    if top <= 0:
        return None
    logpart = max(0.0, min(1.0, math.log10(top / 1e4) / 2))
    count = min(1.0, (n.get('over100K') or 0) / 12)
    return round(100 * (0.7 * logpart + 0.3 * count))


def age_days(src):
    if src.get('date'):
        return (READ_ON - datetime.date.fromisoformat(src['date'])).days
    m = re.match(r'(\d+)\s*(w|mo|d)', src.get('age') or '')
    if not m:
        return None
    return int(m.group(1)) * {'d': 1, 'w': 7, 'mo': 30}[m.group(2)]


def main():
    lab = json.loads((LAB / 'lab.json').read_text())
    checks = json.loads((LAB / 'checks.json').read_text())
    pts = [dict(SPEC_POINT, round=ROUND, sample=True,
                axisNotes='SPEC.md section 4 example values, copied verbatim.')]
    for f in lab['formats']:
        s = f['source']
        days = age_days(s)
        fresh = None if days is None else round(max(0.1, min(1.0, 1 - days / 60)), 2)
        for t in f['targets']:
            key = f"{f['key']}|{t['niche']}"
            if key == 'you-wouldnt-last|Formula 1':
                continue  # covered by the SPEC example
            sat, fit, conf = HAND[key]
            pr = t.get('proof') or {}
            pts.append({
                'id': f"{f['key']}-{slug(t['niche'])}",
                'round': ROUND, 'sample': True,
                'format': FORMULA.get(f['key'], f['name']),
                'niche': t['niche'],
                'ourTitle': t['title'],
                'demand': demand(t.get('numbers') or {}),
                'saturation': sat, 'fit': fit,
                'freshness': fresh,
                'verdict': (t.get('verdict') or 'untested').lower(),
                'confidence': conf,
                'source': {'id': s['id'], 'title': s['title'], 'views': s.get('views'), 'checkedAt': '2026-10-22'},
                'proof': {'id': pr.get('id'), 'title': pr.get('title'), 'views': pr.get('views')} if pr else None,
                'query': (checks.get(key) or {}).get('topic'),
                'numbers': t.get('numbers'),
                'evidence': [u for u in [f"https://youtu.be/{s['id']}", pr.get('id') and f"https://youtu.be/{pr['id']}"] if u],
                'notes': t.get('why', ''),
                'axisNotes': 'Hand-derived sample: demand from the dated query numbers; saturation from the round notes; fit is a builder estimate, not measured.'
                             + (' Saturation not read: the crossing search drifted.' if sat is None else ''),
            })
    for m in lab.get('merges', []):
        pts.append({
            'id': m['key'], 'round': ROUND, 'sample': True,
            'format': 'Merge', 'niche': m['niche'], 'ourTitle': m['title'],
            'demand': None, 'saturation': None, 'fit': None, 'freshness': 0.6,
            'verdict': m['verdict'].lower(), 'confidence': 0.2,
            'source': {'id': m['packaging']['id'], 'title': m['packaging']['title'], 'views': m['packaging'].get('views'), 'checkedAt': '2026-10-22'},
            'proof': {'id': m['look']['id'], 'title': m['look']['title'], 'views': m['look'].get('views')},
            'query': None,
            'evidence': [f"https://youtu.be/{m['packaging']['id']}", f"https://youtu.be/{m['look']['id']}"],
            'notes': f"What is proven: {m.get('proven', '')} What is not: {m.get('unproven', '')}",
            'axisNotes': 'Merge: no crossing query was run, so no axis is measured.',
        })
    out = {
        'version': 1, 'sample': True, 'round': ROUND,
        'generatedAt': datetime.datetime.now().isoformat(timespec='seconds'),
        'note': 'SAMPLE for the 3D board. Built by board/make_sample.py from SPEC.md section 4 and format-lab/2026-10-22/lab.json. '
                "Fit and saturation are hand readings; verdicts are the round-2 proposer's, not reconciled. Do not keep from this file.",
        'points': pts,
    }
    (HERE / 'sample-state.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(f'wrote {len(pts)} points')


if __name__ == '__main__':
    main()
