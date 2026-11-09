#!/usr/bin/env python3
"""Build evidence.js for an ideas board: the linked thumbnails shown under each Demand and Saturation line.

Usage: python3 evidence.py <board_dir> <spec.json>

spec.json maps an idea id to two lists, "d" (demand) and "s" (saturation). Each entry is either
  {"id": "<videoId>", "t": "<title>", "n": "520K", "a": "23 Sep", "h": "@handle"}        a video named by hand
  {"file": "raw/d6.json", "period": "year", "top": 3}                                   the top N of a yt_scout.py demand result
  {"file": "raw/d6.json", "period": "month", "ids": ["abc", "def"]}                     named videos from a demand result
Thumbnails are saved to <board_dir>/img/ev/<id>.jpg and evidence.js is written next to index.html.
"""
import json, os, sys, urllib.request

def fmt(n): return f"{n/1e6:.2f}M" if n >= 1e6 else f"{n//1000}K" if n >= 1000 else str(n)

def rows(board, e):
    if 'file' not in e: return [e]
    d = [x for x in json.load(open(os.path.join(board, e['file'])))[e['period']] if x.get('id')]
    if 'ids' in e: d = [x for x in d if x['id'] in e['ids']]
    else: d = sorted(d, key=lambda x: -(x.get('views') or 0))[:e.get('top', 3)]
    return [{'id': x['id'], 't': x['title'], 'n': fmt(x.get('views') or 0), 'a': x.get('age'), 'h': x.get('handle') or ''} for x in d]

board, spec = sys.argv[1], json.load(open(sys.argv[2]))
os.makedirs(os.path.join(board, 'img/ev'), exist_ok=True)
out = {}
for idea, v in spec.items():
    out[idea] = {}
    for k in 'ds':
        out[idea][k] = [r for e in v.get(k, []) for r in rows(board, e)]
        for r in out[idea][k]:
            f = os.path.join(board, f"img/ev/{r['id']}.jpg")
            if not os.path.exists(f):
                try: urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{r['id']}/mqdefault.jpg", f)
                except Exception as ex: print('thumbnail failed', r['id'], ex)
open(os.path.join(board, 'evidence.js'), 'w').write('window.EVIDENCE=' + json.dumps(out, ensure_ascii=False, indent=1) + ';')
print({k: (len(v['d']), len(v['s'])) for k, v in out.items()})
