#!/usr/bin/env python3
"""YouTube niche scouting without an API key or yt-dlp (plain page + RSS reads).

  yt_scout.py search  "every _ explained" [--period month|week|year|any] [--sort views|date|relevance] [--max 20]
      Video search the way the incognito method does it: recent uploads, sorted by views.
  yt_scout.py channels "Professor Gusty"
      Find channels by name (resolves a name or a cut-off handle to the real @handle).
  yt_scout.py channel @handle [@handle ...] [--thumbs DIR]
      Stats for each channel: subs, video count, joined date, latest 15 uploads from RSS,
      median views, best recent video, views-per-sub ratio, uploads per week, validation checks.
  yt_scout.py frames <video id or url> [...] [--dir img] [--sheet sheet.jpg]
      Download the three in-video stills of each video (and optionally a sheet, one row per video) to see the format.
  yt_scout.py styles "car history" "history of ferrari" ... --out DIR [--period year|month] [--top 24]
      Audience and style fit: the strongest recent videos of a niche with three inside frames each, on sheets.
      Read the sheets, fill "style" in DIR/survey.json, then: yt_scout.py tally DIR/survey.json --table
  yt_scout.py formulas [--out file.json] [--table]
      The format watch: sweep this month's uploads over 100K across the niches and title shapes in
      watch_seeds.json and list title wording shared by three or more channels, with the niches it was seen in.
  yt_scout.py spread "the _ levels of _ explained" [--table]
      How new one formula is: this month against the rest of the year, channels, hits, and a reading
      (new and spreading / established / past its peak / thin).
  yt_scout.py compare "formula 1|f1" "rally car|wrc" "le mans" [--table]
      Size topics against each other before choosing where to bend to: this month's views, how many small
      channels got through, the realistic ceiling for a small channel, and Wikipedia interest with its trend.
      Wordings of one topic are joined with |; add =Article_Title to name the Wikipedia page.
  yt_scout.py demand "lamborghini history" [--channels 12]
      Demand and saturation for a topic as we would frame it: relevant videos from the last month
      and the last year, who made them, how big those channels are, and a reading.
  yt_scout.py sheet "every _ explained" out.jpg [--period month] [--sort views] [--max 24]
      Contact sheet of the thumbnails a search returns, so formats and thumbnail layouts can be read at a glance.
All commands print JSON. Add --table for a compact text table.
"""
import argparse, json, re, statistics, sys, time, os, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime

# HTTPS certificates: python.org builds on macOS ship without a CA bundle and then every read fails
# silently. Use certifi when installed, else the system bundle, unless SSL_CERT_FILE is already set.
if not os.environ.get('SSL_CERT_FILE'):
    try:
        import certifi
        os.environ['SSL_CERT_FILE'] = certifi.where()
    except ImportError:
        for _ca in ('/etc/ssl/cert.pem', '/etc/ssl/certs/ca-certificates.crt'):
            if os.path.exists(_ca):
                os.environ['SSL_CERT_FILE'] = _ca
                break

UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36',
      'Accept-Language': 'en-US,en;q=0.9', 'Cookie': 'CONSENT=YES+1; SOCS=CAI'}
NS = {'a': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015', 'm': 'http://search.yahoo.com/mrss/'}
# search filter codes (the "sp" URL parameter): type=video + upload period + sort order
SP = {('any', 'relevance'): 'EgIQAQ%3D%3D', ('any', 'views'): 'CAMSAhAB', ('any', 'date'): 'CAISAhAB',
      ('week', 'relevance'): 'EgQIAxAB', ('week', 'views'): 'CAMSBAgDEAE%3D', ('week', 'date'): 'CAISBAgDEAE%3D',
      ('month', 'relevance'): 'EgQIBBAB', ('month', 'views'): 'CAMSBAgEEAE%3D', ('month', 'date'): 'CAISBAgEEAE%3D',
      ('year', 'relevance'): 'EgQIBRAB', ('year', 'views'): 'CAMSBAgFEAE%3D', ('year', 'date'): 'CAISBAgFEAE%3D'}

def get(url):
    try:
        return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read().decode('utf8', 'ignore')
    except Exception as e:
        return 'ERR %s' % e

def initial_data(html):
    m = re.search(r'var ytInitialData = (\{.*?\});</script>', html)
    return json.loads(m.group(1)) if m else None

def walk(o, key, out):
    if isinstance(o, dict):
        if key in o: out.append(o[key])
        else:
            for v in o.values(): walk(v, key, out)
    elif isinstance(o, list):
        for v in o: walk(v, key, out)
    return out

def num(s):
    if not s: return None
    m = re.search(r'([\d.,]+)\s*([KMB]?)', s.replace('\xa0', ' '))
    if not m: return None
    return int(float(m.group(1).replace(',', '')) * {'': 1, 'K': 1e3, 'M': 1e6, 'B': 1e9}[m.group(2)])

def text(o):
    if not o: return None
    return o.get('simpleText') or ''.join(r.get('text', '') for r in o.get('runs', []))

def search_videos(q, period='month', sort='views', limit=20):
    d = initial_data(get('https://www.youtube.com/results?search_query=%s&sp=%s' % (urllib.parse.quote(q), SP[(period, sort)])))
    out = []
    for v in walk(d or {}, 'videoRenderer', []):
        owner = (v.get('ownerText') or {}).get('runs', [{}])[0]
        handle = (owner.get('navigationEndpoint', {}).get('browseEndpoint', {}).get('canonicalBaseUrl') or '').lstrip('/')
        out.append({'id': v.get('videoId'), 'title': text(v.get('title')), 'views': num(text(v.get('viewCountText'))),
                    'age': text(v.get('publishedTimeText')), 'length': text(v.get('lengthText')),
                    'channel': owner.get('text'), 'handle': handle,
                    'channelId': owner.get('navigationEndpoint', {}).get('browseEndpoint', {}).get('browseId')})
    return out[:limit]

def search_channels(q, limit=8):
    d = initial_data(get('https://www.youtube.com/results?search_query=%s&sp=EgIQAg%%253D%%253D' % urllib.parse.quote(q)))
    out = []
    for c in walk(d or {}, 'channelRenderer', []):
        # YouTube puts the @handle in subscriberCountText and the sub count in videoCountText
        out.append({'name': text(c.get('title')), 'handle': text(c.get('subscriberCountText')),
                    'subs': num(text(c.get('videoCountText'))), 'channelId': c.get('channelId')})
    return out[:limit]

def channel(h, thumbs=None):
    path = h if h.startswith(('@', 'channel/')) else '@' + h
    c = {'handle': path}
    for attempt in range(3):
        d = initial_data(get('https://www.youtube.com/%s/videos' % path))
        if d:
            md = d.get('metadata', {}).get('channelMetadataRenderer', {})
            s = json.dumps(d)
            nv = re.search(r'"([\d.,]+[KMB]?) videos?"', s[max(0, s.find('pageHeaderViewModel')):])
            c.update(name=(md.get('title') or '').strip(), channelId=md.get('externalId'), url=md.get('vanityChannelUrl'),
                     description=(md.get('description') or '')[:300], subs=header_subs(d),
                     videoCount=num(nv.group(1)) if nv else None)
            if c['channelId'] and c['subs'] is not None: break
        time.sleep(1.5)
    if not c.get('channelId'):
        c['error'] = 'channel not found'; return c
    about = get('https://www.youtube.com/%s/about' % path)
    j = re.search(r'Joined ([A-Z][a-z]{2} \d{1,2}, \d{4})', about)
    if j:
        c['joined'] = datetime.strptime(j.group(1), '%b %d, %Y').date().isoformat()
        c['ageMonths'] = round((date.today() - date.fromisoformat(c['joined'])).days / 30.4, 1)
    tv = re.search(r'"viewCountText":"([\d,]+) views"', about)
    if tv: c['totalViews'] = num(tv.group(1))
    vids = []
    try:
        for e in ET.fromstring(get('https://www.youtube.com/feeds/videos.xml?channel_id=' + c['channelId'])).findall('a:entry', NS):
            st = e.find('m:group/m:community/m:statistics', NS)
            vids.append({'id': e.find('yt:videoId', NS).text, 'title': e.find('a:title', NS).text,
                         'published': e.find('a:published', NS).text[:10], 'views': int(st.get('views')) if st is not None else 0,
                         'short': '/shorts/' in e.find('a:link', NS).get('href')})
    except Exception as ex:
        c['rssError'] = str(ex)[:100]
    longs = [v for v in vids if not v['short']] or vids
    c['latest'] = vids
    if longs:
        views = [v['views'] for v in longs]
        best = max(longs, key=lambda v: v['views'])
        days = max(1, (date.fromisoformat(longs[0]['published']) - date.fromisoformat(longs[-1]['published'])).days)
        c.update(medianViews=int(statistics.median(views)), bestRecent=best, sample=len(longs),
                 uploadsPerWeek=round(len(longs) / days * 7, 1) if len(longs) > 1 else None,
                 bestOverMedian=round(best['views'] / max(1, statistics.median(views)), 1),
                 daysSinceUpload=(date.today() - date.fromisoformat(longs[0]['published'])).days)
        if c.get('subs'): c['bestViewsPerSub'] = round(best['views'] / c['subs'], 1)
        if c.get('totalViews') and c.get('videoCount'): c['avgViewsAllTime'] = int(c['totalViews'] / c['videoCount'])
    c['checks'] = checks(c)
    if thumbs and longs:
        os.makedirs(thumbs, exist_ok=True)
        for v in sorted(longs, key=lambda v: -v['views'])[:3]:
            p = os.path.join(thumbs, v['id'] + '.jpg')
            if os.path.exists(p): continue
            for q in ('maxresdefault', 'hq720', 'mqdefault'):
                try:
                    b = urllib.request.urlopen('https://i.ytimg.com/vi/%s/%s.jpg' % (v['id'], q), timeout=20).read()
                    if len(b) > 5000: open(p, 'wb').write(b); break
                except Exception: pass
    return c

def checks(c):
    """Pass/fail on the numbers a script can see. Faceless, competitors and format still need eyes."""
    k = {}
    # The account's join date is not the niche's age: many channels run on old or renamed accounts.
    # The first-video date is only known when RSS holds every upload (15 or fewer videos).
    if c.get('videoCount') and c.get('latest') and c['videoCount'] <= len(c['latest']):
        first = min(v['published'] for v in c['latest'])
        c['firstVideo'] = first
        k['firstVideoUnder6Months'] = (date.today() - date.fromisoformat(first)).days <= 183
    if 'medianViews' in c:
        k['median50K'] = c['medianViews'] >= 50000
        k['stillPosting'] = c['daysSinceUpload'] <= 14
        c['over100K'] = sum(1 for v in c['latest'] if not v['short'] and v['views'] >= 100000)
        k['notOneHit'] = c['bestOverMedian'] <= 10 or c['over100K'] >= 3   # one video far above the rest = one lucky day
    if 'bestViewsPerSub' in c: k['freshRatio'] = c['bestViewsPerSub'] >= 5   # views far above subs = new and pushed by the algorithm
    return k

STOPW = set('a an the of in on to and or for with at by from is are was how why what every all your my'.split())

def secs(length):
    p = [int(x) for x in (length or '').split(':') if x.isdigit()]
    return sum(x * 60 ** i for i, x in enumerate(reversed(p))) if p else None

def quick_subs(v):
    """Subscriber count for a search hit, from the channel page."""
    path = v.get('handle') or ('channel/' + v['channelId'] if v.get('channelId') else None)
    if not path: return None
    d = initial_data(get('https://www.youtube.com/%s/videos' % path))     # the Videos tab: the home tab lists other channels first
    return header_subs(d) if d else None

def header_subs(d):
    """Subscriber count from the channel's own header. The first '… subscribers' on the page can belong to
    a featured channel, which made small channels look tiny and big ones look small."""
    s = json.dumps(d); i = s.find('pageHeaderViewModel')
    m = re.search(r'"([\d.,]+[KMB]?) subscribers?"', s[i:] if i >= 0 else s)
    return num(m.group(1)) if m else None

def demand(q, nchan=12):
    """Demand = people watch this topic. Saturation = how many channels already serve it, and how big they are."""
    out = {'query': q}
    seen = {}
    for period in ('month', 'year'):
        hits = {}
        keys = [w for w in re.findall(r'[a-z0-9]+', q.lower()) if w not in STOPW]
        for sort in ('relevance', 'views'):
            for v in search_videos(q, period, sort, 30):
                if not v['id'] or v['views'] is None: continue
                t = (v['title'] or '').lower()
                # stay on topic: sorting by views drifts to unrelated hits, so those must carry the topic's words
                need = keys[:2] if sort == 'views' else keys[:1]
                if not all(k in t for k in need): continue
                if (secs(v['length']) or 0) < 180 or 'treamed' in (v['age'] or ''): continue
                hits[v['id']] = v
        vids = sorted(hits.values(), key=lambda v: -v['views'])
        out[period] = vids
    # channel sizes for the channels behind the biggest recent videos
    order = []
    for v in out['month'] + out['year']:
        key = v.get('handle') or v.get('channelId')
        if key and key not in seen and len(order) < nchan: seen[key] = None; order.append(v)
    for v in order:
        seen[v.get('handle') or v.get('channelId')] = quick_subs(v); time.sleep(0.4)
    for period in ('month', 'year'):
        for v in out[period]:
            v['subs'] = seen.get(v.get('handle') or v.get('channelId'))
            if v['subs']: v['viewsPerSub'] = round(v['views'] / v['subs'], 1)
    def summary(vids):
        chans = {}
        for v in vids:
            if v['views'] >= 50000: chans.setdefault(v.get('handle') or v.get('channel'), []).append(v)
        small = [v for v in vids if v.get('subs') and v['subs'] < 100000 and v['views'] >= 50000]
        return {'videos': len(vids), 'over50K': sum(v['views'] >= 50000 for v in vids), 'over100K': sum(v['views'] >= 100000 for v in vids),
                'over1M': sum(v['views'] >= 1000000 for v in vids), 'channelsOver50K': len(chans),
                'channelsWith2PlusOver50K': sum(len(x) >= 2 for x in chans.values()),
                'smallChannelHits': len(small), 'topViews': vids[0]['views'] if vids else 0}
    sm, sy = summary(out['month']), summary(out['year'])
    out['summary'] = {'month': sm, 'year': sy}
    # a reading, not a verdict: the videos still have to be looked at for relevance and format
    if sy['over100K'] == 0: d = 'no demand shown: nothing on this wording passed 100K in a year'
    elif sm['over50K'] == 0: d = 'cold: it worked within the year, nothing over 50K this month'
    elif sm['smallChannelHits'] >= 2: d = 'open demand: small channels are getting views on it this month'
    elif sm['over100K'] >= 3: d = 'demand, held by established channels: check their size before entering'
    else: d = 'some demand this month: thin, look at the videos'
    if sm['channelsWith2PlusOver50K'] >= 3 or sm['channelsOver50K'] >= 8: t = 'crowded: several channels serve it repeatedly'
    elif sm['channelsOver50K'] >= 3: t = 'contested: a few channels are on it'
    else: t = 'open: under 3 channels over 50K this month'
    out['reading'] = {'demand': d, 'saturation': t}
    return out

def wiki_trend(article):
    """Interest outside YouTube: Wikipedia page views for an article. Daily average of the last 30 days against the
    daily average of the 11 months before. Above 1.3 means people are looking it up more than usual right now."""
    from datetime import timedelta
    end = date.today() - timedelta(days=2); start = end - timedelta(days=364)
    u = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/%s/daily/%s/%s' % (
        urllib.parse.quote(article.replace(' ', '_'), safe=''), start.strftime('%Y%m%d'), end.strftime('%Y%m%d'))
    try:
        items = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'niche-research/1.0 (personal research script)'}), timeout=25).read())['items']
    except Exception as e:
        return {'article': article, 'error': str(e)[:80]}
    v = [i['views'] for i in items]
    if len(v) < 60: return {'article': article, 'error': 'not enough data'}
    last, before = v[-30:], v[:-30]
    return {'article': article, 'perDay30': int(sum(last) / len(last)), 'perDayYear': int(sum(before) / len(before)),
            'trend': round((sum(last) / len(last)) / max(1, sum(before) / len(before)), 2)}

def wiki_article(topic):
    u = 'https://en.wikipedia.org/w/api.php?action=opensearch&limit=1&format=json&search=' + urllib.parse.quote(topic)
    try:
        r = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'niche-research/1.0 (personal research script)'}), timeout=20).read())
        return r[1][0] if r[1] else None
    except Exception: return None

def topic_size(spec, nchan=12):
    """How big is a topic right now, and how much of it reaches small channels.
    spec: 'formula 1|f1' (search wordings separated by |), optionally '=Wikipedia article' at the end."""
    spec, _, article = spec.partition('=')
    aliases = [a.strip() for a in spec.split('|') if a.strip()]
    month, year = {}, {}
    keys = {w for a in aliases for w in re.findall(r'[a-z0-9]+', a.lower()) if w not in STOPW and len(w) > 1}
    for a in aliases:
        for period, bucket in (('month', month), ('year', year)):
            for sort in ('relevance', 'views'):
                for v in search_videos(a, period, sort, 30):
                    if not v['id'] or v['views'] is None: continue
                    if (secs(v['length']) or 0) < 180 or 'treamed' in (v['age'] or ''): continue
                    text_ = ((v['title'] or '') + ' ' + (v.get('channel') or '') + ' ' + (v.get('handle') or '')).lower()
                    # YouTube's own relevance ranking is trusted; the views ranking drifts, so it must carry one of the topic's words
                    if sort == 'views' and not any(k in text_ for k in keys): continue
                    bucket.setdefault(v['id'], v)
                time.sleep(0.3)
    mv = sorted(month.values(), key=lambda v: -v['views']); yv = sorted(year.values(), key=lambda v: -v['views'])
    cache = {}
    for v in mv[:40]:
        k = v.get('handle') or v.get('channelId')
        if k and k not in cache and len(cache) < nchan: cache[k] = quick_subs(v); time.sleep(0.3)
    for v in mv: v['subs'] = cache.get(v.get('handle') or v.get('channelId'))
    top = mv[:20]; known = [v for v in top if v.get('subs')]
    small = sorted([v for v in mv if v.get('subs') and v['subs'] < 100000], key=lambda v: -v['views'])
    out = {'topic': aliases[0], 'aliases': aliases,
           'monthUploadsSeen': len(mv), 'monthOver100K': sum(v['views'] >= 100000 for v in mv), 'monthOver1M': sum(v['views'] >= 1000000 for v in mv),
           'monthTop20Views': sum(v['views'] for v in top), 'monthMedianTop10': int(statistics.median([v['views'] for v in mv[:10]])) if mv else 0,
           'smallChannelHits': sum(v['views'] >= 50000 for v in small),
           'smallChannelBest': ({'views': small[0]['views'], 'subs': small[0]['subs'], 'title': small[0]['title'], 'id': small[0]['id'], 'handle': small[0].get('handle')} if small else None),
           'smallChannelThird': small[2]['views'] if len(small) > 2 else None,
           'smallShareOfTop20': round(sum(v['views'] for v in known if v['subs'] < 100000) / max(1, sum(v['views'] for v in known)), 2) if known else None,
           'yearOver100K': sum(v['views'] >= 100000 for v in yv), 'yearOver1M': sum(v['views'] >= 1000000 for v in yv), 'yearTop': yv[0]['views'] if yv else 0,
           'top': [{k: v.get(k) for k in ('id', 'title', 'views', 'age', 'handle', 'subs')} for v in mv[:8]]}
    art = article.strip() or wiki_article(aliases[0])
    out['wikipedia'] = wiki_trend(art) if art else None
    return out

def spread(formula, need=None):
    """How new a title formula is and how far it has spread. formula: 'the _ levels of _ explained'.
    Compares the last month with the rest of the last year. need: words every matching title must contain
    (default: the formula's own fixed words, numbers left out)."""
    q = formula.replace('_', ' ')
    need = need or [w for w in re.findall(r"[a-z']+", q.lower()) if w not in STOPW and len(w) > 2]
    out = {}
    for per in ('month', 'year'):
        got = {}
        for sort in ('views', 'relevance'):
            for v in search_videos(q, per, sort, 30):
                t = (v['title'] or '').lower()
                if v['id'] and v['views'] and all(k in t for k in need) and (secs(v['length']) or 0) >= 180 and 'treamed' not in (v['age'] or ''):
                    got[v['id']] = v
            time.sleep(0.3)
        out[per] = sorted(got.values(), key=lambda v: -v['views'])
    m = out['month']; ids = {v['id'] for v in m}
    older = [v for v in out['year'] if v['id'] not in ids]
    chans = lambda vs: len({v.get('handle') or v.get('channel') for v in vs})
    mv, ov = sum(v['views'] for v in m), sum(v['views'] for v in older)
    share = round(mv / max(1, mv + ov), 2)
    m100, o100 = sum(v['views'] >= 100000 for v in m), sum(v['views'] >= 100000 for v in older)
    if m100 < 3: reading = 'thin: fewer than 3 videos over 100K this month'
    elif share >= 0.7: reading = 'new and spreading: most of what this formula ever got came in the last month'
    elif share >= 0.2: reading = 'established and still working: it was getting views before this month too'
    else: reading = 'past its peak: the views came earlier in the year, this month is mostly copies'
    slim = lambda vs: [{k: v.get(k) for k in ('id', 'title', 'views', 'age', 'handle', 'channel', 'length')} for v in vs]
    return {'formula': formula, 'mustContain': need,
            'month': {'videos': len(m), 'channels': chans(m), 'over100K': m100, 'views': mv},
            'restOfYear': {'videos': len(older), 'channels': chans(older), 'over100K': o100, 'views': ov},
            'monthShare': share, 'reading': reading, 'examples': slim(m[:15]), 'olderExamples': slim(older[:8])}

def _title_words(title):
    t = re.sub(r"[’']", '', (title or '').lower())
    t = re.sub(r'\d[\d,.:]*', 'N', t)          # every number becomes N so "in 9 minutes" matches "in 13 minutes"
    return re.findall(r"[a-zA-Z]+|N", t)

def formulas(seeds_path, min_views=100000, min_channels=3):
    """Find title wording shared by several channels this month: a format on the move. Sweeps the niches and
    shapes in the seeds file, keeps this month's videos over min_views, and returns shared word sequences with
    the niches they were found in. Run `spread` on the promising ones to see how new each is."""
    import collections
    seeds = json.load(open(seeds_path))
    plan = [(n, q) for n, qs in seeds['niches'].items() for q in qs] + [('?', q.replace('_', ' ')) for q in seeds['shapes']]
    vids = {}
    for niche, q in plan:
        for sort in ('views', 'relevance'):
            for v in search_videos(q, 'month', sort, 30):
                if not v['id'] or not v['views'] or v['views'] < min_views: continue
                if (secs(v['length']) or 0) < 180 or 'treamed' in (v['age'] or ''): continue
                letters = [c for c in v['title'] if c.isalpha()]
                if letters and sum(ord(c) > 0x24F for c in letters) / len(letters) > 0.3: continue
                v.setdefault('niches', [])
                if v['id'] in vids:
                    if niche != '?' and niche not in vids[v['id']]['niches']: vids[v['id']]['niches'].append(niche)
                else:
                    v['niches'] = [] if niche == '?' else [niche]; vids[v['id']] = v
            time.sleep(0.25)
        sys.stderr.write('%-12s %s\n' % (niche, q))
    stop = STOPW | set('it its this that these those you his her he she they them we our i be'.split())
    seen = collections.defaultdict(dict)
    for v in vids.values():
        w = _title_words(v['title']); ch = v.get('handle') or v.get('channel')
        grams = set()
        for n in range(3, 7):
            for i in range(len(w) - n + 1):
                g = w[i:i + n]
                if sum(x not in stop and x != 'N' for x in g) >= 2: grams.add(' '.join(g))
        for g in grams:
            if ch not in seen[g] or v['views'] > seen[g][ch]['views']: seen[g][ch] = v
    out = []
    for g, chans in seen.items():
        if len(chans) < min_channels: continue
        vs = sorted(chans.values(), key=lambda v: -v['views'])
        niches = sorted({n for v in vs for n in v['niches']})
        out.append({'wording': g, 'channels': len(chans), 'views': sum(v['views'] for v in vs), 'nichesSeen': niches, 'inCars': 'cars' in niches,
                    'examples': [{'id': v['id'], 'title': v['title'], 'views': v['views'], 'age': v['age'], 'handle': v.get('handle') or v.get('channel'), 'niches': v['niches']} for v in vs[:8]]})
    out.sort(key=lambda s: (-len(s['wording'].split()), -s['channels']))
    kept = []
    for s_ in out:      # keep the longest phrasing of each group
        if not any(s_['wording'] in k['wording'] and k['channels'] >= s_['channels'] - 1 for k in kept): kept.append(s_)
    kept.sort(key=lambda s_: (-s_['channels'], -s_['views']))
    return {'videosOver100K': len(vids), 'searches': len(plan), 'wordings': kept}

def sheet(q, path, period='month', sort='views', limit=24):
    from PIL import Image, ImageDraw
    import io
    vids = search_videos(q, period, sort, limit)
    W, H, cols = 320, 180, 4
    rows = (len(vids) + cols - 1) // cols
    im = Image.new('RGB', (W * cols, (H + 34) * max(1, rows)), 'black'); d = ImageDraw.Draw(im)
    for i, v in enumerate(vids):
        x, y = (i % cols) * W, (i // cols) * (H + 34)
        try:
            b = urllib.request.urlopen('https://i.ytimg.com/vi/%s/mqdefault.jpg' % v['id'], timeout=20).read()
            im.paste(Image.open(io.BytesIO(b)).convert('RGB').resize((W, H)), (x, y))
        except Exception: pass
        d.text((x + 4, y + H + 2), '%d  %s  %s  %s' % (i, v.get('handle') or v.get('channel') or '', v.get('views'), v.get('age') or ''), fill='white')
        d.text((x + 4, y + H + 17), (v.get('title') or '')[:52], fill=(180, 180, 180))
    im.save(path, quality=85)
    return {'sheet': path, 'videos': vids}

def frames(vid, outdir, width=640):
    """The three stills YouTube captures inside a video (about 25, 50 and 75 percent). Saved as <id>_1..3.jpg.
    These show the format. A thumbnail is packaging and often shows nothing of how the video looks."""
    from PIL import Image
    import io
    os.makedirs(outdir, exist_ok=True)
    got = []
    for n in (1, 2, 3):
        p = os.path.join(outdir, '%s_%d.jpg' % (vid, n))
        if not os.path.exists(p):
            for q in ('maxres%d' % n, 'hq720_%d' % n, 'hq%d' % n):
                try:
                    b = urllib.request.urlopen('https://i.ytimg.com/vi/%s/%s.jpg' % (vid, q), timeout=20).read()
                    if len(b) < 3000: continue
                    im = Image.open(io.BytesIO(b)).convert('RGB')
                    if q.startswith('hq') and not q.startswith('hq720'):      # 4:3 with black bars: crop to 16:9
                        w, h = im.size; ch = int(w * 9 / 16); im = im.crop((0, (h - ch) // 2, w, (h - ch) // 2 + ch))
                    im.resize((width, int(width * 9 / 16))).save(p, quality=82); break
                except Exception: pass
        if os.path.exists(p): got.append(p)
    return got

def frame_sheet(ids, path, outdir, labels=None):
    """One row per video: its three in-video frames side by side. Read this image to describe formats."""
    from PIL import Image, ImageDraw
    W, H = 400, 225
    im = Image.new('RGB', (W * 3, (H + 18) * len(ids)), 'black'); d = ImageDraw.Draw(im)
    for r, vid in enumerate(ids):
        for c, p in enumerate(frames(vid, outdir)):
            n = int(p[-5]) - 1
            im.paste(Image.open(p).resize((W, H)), (n * W, r * (H + 18) + 18))
        d.text((4, r * (H + 18) + 3), '%d  %s  %s' % (r, vid, (labels or {}).get(vid, '')), fill='white')
    im.save(path, quality=80)
    return path

def styles(queries, out, period='year', top=24, min_views=50000):
    """Which visual styles does a niche's audience already watch? Collects the niche's strongest recent videos,
    pulls three inside frames for each and lays them out on sheets. Read the sheets, write a style name into
    each entry's "style" field in survey.json, then run `tally`."""
    os.makedirs(out, exist_ok=True)
    got = {}
    for q in queries:
        keys = [w for w in re.findall(r'[a-z0-9]+', q.lower()) if w not in STOPW]
        for sort in ('relevance', 'views'):
            for v in search_videos(q, period, sort, 30):
                if not v['id'] or not v['views']: continue
                sec = secs(v['length'])
                if sec is None or sec < 180 or 'treamed' in (v['age'] or ''): continue
                t = (v['title'] or '').lower()
                if sort == 'views' and not all(k in t for k in keys[:2]): continue    # sorting by views drifts off topic
                v['query'] = q
                got.setdefault(v['id'], v)
            time.sleep(0.4)
    vids = sorted([v for v in got.values() if v['views'] >= min_views], key=lambda v: -v['views'])[:top]
    cache = {}
    for v in vids:
        k = v.get('handle') or v.get('channelId')
        if k not in cache: cache[k] = quick_subs(v); time.sleep(0.3)
        v['subs'] = cache[k]; v['viewsPerSub'] = round(v['views'] / v['subs'], 1) if v['subs'] else None
        v['style'] = ''           # fill in after reading the sheet
        frames(v['id'], os.path.join(out, 'img'))
        tp = os.path.join(out, 'img', v['id'] + '.jpg')
        if not os.path.exists(tp):
            try: open(tp, 'wb').write(urllib.request.urlopen('https://i.ytimg.com/vi/%s/hq720.jpg' % v['id'], timeout=20).read())
            except Exception: pass
    sheets = []
    for i in range(0, len(vids), 8):
        part = vids[i:i + 8]
        lab = {v['id']: '%s | %s views | %s subs | %s | %s' % (v.get('handle') or v.get('channel'), v['views'], v['subs'], v['age'], (v['title'] or '')[:60]) for v in part}
        sheets.append(frame_sheet([v['id'] for v in part], os.path.join(out, 'styles-%d.jpg' % (i // 8)), os.path.join(out, 'img'), lab))
    json.dump({'queries': queries, 'period': period, 'videos': vids}, open(os.path.join(out, 'survey.json'), 'w'), indent=1, ensure_ascii=False)
    return {'survey': os.path.join(out, 'survey.json'), 'videos': len(vids), 'candidates': len(got), 'sheets': sheets}

def tally(path):
    import statistics as st
    d = json.load(open(path)); groups = {}
    for v in d['videos']: groups.setdefault(v.get('style') or 'unlabelled', []).append(v)
    rows = []
    for name, vs in groups.items():
        small = [v for v in vs if v.get('subs') and v['subs'] < 100000]
        rows.append({'style': name, 'videos': len(vs), 'medianViews': int(st.median(v['views'] for v in vs)), 'topViews': max(v['views'] for v in vs),
                     'smallChannelVideos': len(small), 'channels': len({v.get('handle') or v.get('channel') for v in vs})})
    return sorted(rows, key=lambda r: -r['videos'])

def table(rows, cols):
    f = lambda v: '' if v is None else ('%.1fM' % (v / 1e6) if isinstance(v, int) and v >= 1e6 else '%.0fK' % (v / 1e3) if isinstance(v, int) and v >= 1e4 else str(v))
    for r in rows: print(' | '.join(f(r.get(c))[:60] for c in cols))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('search'); s.add_argument('query'); s.add_argument('--period', default='month', choices=['week', 'month', 'year', 'any'])
    s.add_argument('--sort', default='views', choices=['views', 'date', 'relevance']); s.add_argument('--max', type=int, default=20); s.add_argument('--table', action='store_true')
    s = sub.add_parser('channels'); s.add_argument('query'); s.add_argument('--table', action='store_true')
    s = sub.add_parser('channel'); s.add_argument('handles', nargs='+'); s.add_argument('--thumbs'); s.add_argument('--table', action='store_true')
    s = sub.add_parser('demand'); s.add_argument('query'); s.add_argument('--channels', type=int, default=12); s.add_argument('--table', action='store_true')
    s = sub.add_parser('sheet'); s.add_argument('query'); s.add_argument('out'); s.add_argument('--period', default='month', choices=['week', 'month', 'year', 'any'])
    s.add_argument('--sort', default='views', choices=['views', 'date', 'relevance']); s.add_argument('--max', type=int, default=24); s.add_argument('--table', action='store_true')
    s = sub.add_parser('spread'); s.add_argument('formula'); s.add_argument('--need', nargs='*'); s.add_argument('--table', action='store_true')
    s = sub.add_parser('formulas'); s.add_argument('--seeds', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'watch_seeds.json'))
    s.add_argument('--out'); s.add_argument('--min-views', type=int, default=100000); s.add_argument('--table', action='store_true')
    s = sub.add_parser('compare'); s.add_argument('topics', nargs='+'); s.add_argument('--channels', type=int, default=12); s.add_argument('--table', action='store_true')
    s = sub.add_parser('styles'); s.add_argument('queries', nargs='+'); s.add_argument('--out', required=True); s.add_argument('--period', default='year', choices=['month', 'year'])
    s.add_argument('--top', type=int, default=24); s.add_argument('--min-views', type=int, default=50000)
    s = sub.add_parser('tally'); s.add_argument('survey'); s.add_argument('--table', action='store_true')
    s = sub.add_parser('frames'); s.add_argument('ids', nargs='+'); s.add_argument('--dir', default='img'); s.add_argument('--sheet')
    a = ap.parse_args()
    if a.cmd == 'spread':
        r = spread(a.formula, a.need)
        if a.table:
            print(json.dumps({k: r[k] for k in ('formula', 'month', 'restOfYear', 'monthShare', 'reading')}, indent=1))
            table(r['examples'], ['views', 'age', 'handle', 'title'])
        else: print(json.dumps(r, indent=1, ensure_ascii=False))
        sys.exit()
    if a.cmd == 'formulas':
        r = formulas(a.seeds, a.min_views)
        if a.out: json.dump(r, open(a.out, 'w'), indent=1, ensure_ascii=False)
        if a.table:
            print(r['videosOver100K'], 'videos over the floor from', r['searches'], 'searches')
            for w in r['wordings'][:40]:
                print('%-34s | %2d channels | %s views | niches: %s | %s' % (w['wording'][:34], w['channels'], w['views'], ','.join(w['nichesSeen']) or '?', ' · '.join(e['title'][:44] for e in w['examples'][:2])))
        elif not a.out: print(json.dumps(r, indent=1, ensure_ascii=False))
        sys.exit()
    if a.cmd == 'compare':
        r = sorted([topic_size(t, a.channels) for t in a.topics], key=lambda x: -x['monthTop20Views'])
        if a.table:
            for x in r:
                w = x.get('wikipedia') or {}; sb = x.get('smallChannelBest') or {}
                x.update(wikiPerDay=w.get('perDay30'), wikiTrend=w.get('trend'), smallBest=sb.get('views'))
            print('topic | month: top-20 views | over 100K | over 1M | small-channel hits | best small-channel video | 3rd best | small share | year over 1M | wikipedia views/day | trend')
            table(r, ['topic', 'monthTop20Views', 'monthOver100K', 'monthOver1M', 'smallChannelHits', 'smallBest', 'smallChannelThird', 'smallShareOfTop20', 'yearOver1M', 'wikiPerDay', 'wikiTrend'])
        else: print(json.dumps(r, indent=1, ensure_ascii=False))
        sys.exit()
    if a.cmd == 'styles':
        print(json.dumps(styles(a.queries, a.out, a.period, a.top, a.min_views), indent=1)); sys.exit()
    if a.cmd == 'tally':
        r = tally(a.survey)
        table(r, ['style', 'videos', 'channels', 'smallChannelVideos', 'medianViews', 'topViews']) if a.table else print(json.dumps(r, indent=1))
        sys.exit()
    if a.cmd == 'frames':
        ids = [re.sub(r'.*(?:v=|youtu\.be/)', '', i)[:11] for i in a.ids]
        r = {i: frames(i, a.dir) for i in ids}
        if a.sheet: frame_sheet(ids, a.sheet, a.dir)
        print(json.dumps({'frames': r, 'sheet': a.sheet}, indent=1)); sys.exit()
    if a.cmd == 'demand':
        r = demand(a.query, a.channels)
        if a.table:
            print(json.dumps({'summary': r['summary'], 'reading': r['reading']}, indent=1))
            for p in ('month', 'year'):
                print('--', p); table(r[p][:12], ['views', 'subs', 'viewsPerSub', 'age', 'handle', 'title'])
        else: print(json.dumps(r, indent=1, ensure_ascii=False))
        sys.exit()
    if a.cmd == 'sheet':
        r = sheet(a.query, a.out, a.period, a.sort, a.max)
        table(r['videos'], ['views', 'age', 'handle', 'title']) if a.table else print(json.dumps(r, indent=1, ensure_ascii=False))
        sys.exit()
    if a.cmd == 'search':
        r = search_videos(a.query, a.period, a.sort, a.max)
        table(r, ['views', 'age', 'length', 'handle', 'title']) if a.table else print(json.dumps(r, indent=1, ensure_ascii=False))
    elif a.cmd == 'channels':
        r = search_channels(a.query)
        table(r, ['name', 'handle', 'subs', 'channelId']) if a.table else print(json.dumps(r, indent=1, ensure_ascii=False))
    else:
        r = []
        for h in a.handles:
            r.append(channel(h, a.thumbs)); time.sleep(0.5)
        if a.table:
            for c in r: c['chk'] = ' '.join(('+' if v else '-') + k for k, v in c.get('checks', {}).items())
            table(r, ['handle', 'name', 'subs', 'videoCount', 'firstVideo', 'medianViews', 'bestOverMedian', 'uploadsPerWeek', 'chk'])
        else: print(json.dumps(r, indent=1, ensure_ascii=False))
