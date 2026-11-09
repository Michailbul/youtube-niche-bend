#!/usr/bin/env python3
"""General interest in a subject, outside YouTube: English Wikipedia page views (free, no key).

Usage: python3 wiki_views.py "Formula 1=Formula_One" "Rally=World_Rally_Championship" "Ferrari=Ferrari" ...
Each argument is Label=Article_title (the title as in the Wikipedia URL). Prints views for the last 12 full months and the last month.
"""
import json, sys, urllib.request, datetime

today = datetime.date.today().replace(day=1)
end = today - datetime.timedelta(days=1)
start = (end.replace(day=1) - datetime.timedelta(days=335)).replace(day=1)
rows = []
for arg in sys.argv[1:]:
    label, art = arg.split('=', 1)
    u = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{urllib.request.quote(art, safe='')}/monthly/{start:%Y%m%d}/{end:%Y%m%d}"
    try:
        v = [x['views'] for x in json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'explainers-research/1.0'}), timeout=20))['items']]
        rows.append((label, sum(v), v[-1]))
    except Exception as e:
        rows.append((label, 0, 0))
for label, year, month in sorted(rows, key=lambda r: -r[1]):
    print(f"{label:22} year {year:>12,}   last month {month:>10,}")
