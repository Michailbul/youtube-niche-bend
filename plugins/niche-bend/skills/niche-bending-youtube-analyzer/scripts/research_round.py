#!/usr/bin/env python3
"""Collect real candidates with the existing scout; validate Gallery proposals.

No automatic conclusions or Gallery writes. The scheduled agent inspects the
evidence and saves through the authenticated Gallery MCP, then reads it back.
"""
import argparse
import importlib.util
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = Path.cwd()                      # the project; rounds go to ./niche-bend/research/rounds/


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def collect(args):
    spec = importlib.util.spec_from_file_location('yt_scout', HERE / 'yt_scout.py')
    scout = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scout)
    original_get, original_data = scout.get, scout.initial_data

    def checked_get(url):
        html = original_get(url)
        if html.startswith('ERR '):
            raise RuntimeError(html[:180])
        return html

    def checked_data(html):
        data = original_data(html)
        if data is None:
            raise RuntimeError('YouTube returned no readable initial data; collection is unverified')
        return data

    scout.get, scout.initial_data = checked_get, checked_data
    now = datetime.now(ZoneInfo('Europe/Prague'))
    out = args.out or ROOT / 'niche-bend' / 'research' / 'rounds' / now.strftime('%Y-%m-%d') / now.strftime('%H%M%S')
    seeds = json.loads((HERE / 'watch_seeds.json').read_text())
    queries = [q for niche, qs in seeds['niches'].items() if niche != 'cars' for q in qs] + seeds['shapes']
    offset = (now.date().toordinal() * args.queries) % len(queries)
    selected = [queries[(offset + n) % len(queries)] for n in range(args.queries)]
    searches, errors, by_id = [], [], {}
    for query in selected:
        try:
            videos = scout.search_videos(query, period='month', sort='views', limit=20)
            searches.append({'query': query, 'videos': videos, 'status': 'checked'})
            for video in videos:
                if video.get('id') and (video.get('views') or 0) >= 100000 and scout.secs(video.get('length')) >= 180:
                    by_id[video['id']] = video
        except Exception as ex:
            errors.append({'query': query, 'error': str(ex)[:180]})
    videos = sorted(by_id.values(), key=lambda v: -(v.get('views') or 0))
    handles = list(dict.fromkeys(v['handle'] for v in videos if v.get('handle')))
    channels = []
    for handle in handles[:args.channels]:
        try:
            channels.append(scout.channel(handle))
        except Exception as ex:
            errors.append({'channel': handle, 'error': str(ex)[:180]})
    report = {'checkedAt': now.isoformat(), 'status': 'partial' if errors else 'collected',
              'scope': 'raw candidates; visual, opening, demand and crossing checks pending',
              'searches': searches, 'candidates': videos, 'channels': channels, 'errors': errors}
    write_json(out / 'collection.json', report)
    print(json.dumps({'path': str(out / 'collection.json'), 'status': report['status'],
                      'queriesChecked': len(searches), 'candidates': len(videos),
                      'channelsChecked': len(channels), 'errors': errors}, ensure_ascii=False))
    return 1 if not searches else 0


def validate(path, now=None):
    now = now or datetime.now(timezone.utc)
    data = json.loads(path.read_text())
    errors = []
    items = data.get('items', [])
    if not 1 <= len(items) <= 12:
        errors.append('Gallery batch must contain 1–12 references')
    allowed_styles = {'2D animation', 'Whiteboard animation', 'AI pictures', 'AI 2D', 'Stock footage',
                      'Game recording', '3D animation', 'Archive and paintings', 'AI presenter', 'Mixed'}
    for index, item in enumerate(items):
        prefix = f'items[{index}]'
        required = ['url', 'title', 'agentDescription', 'language', 'checkedAt',
                    'publishedAt', 'channelLastUploadAt', 'titlePattern', 'thumbnailPattern',
                    'format', 'hook', 'whyItWorks']
        for key in required:
            if not item.get(key): errors.append(f'{prefix}.{key}: required')
        # Origin labels are optional legacy data; new research uses frame evidence.
        if item.get('productionStyle') is not None and item['productionStyle'] not in allowed_styles:
            errors.append(f'{prefix}: unsupported legacy productionStyle')
        if len(item.get('agentDescription', '').split()) > 45:
            errors.append(f'{prefix}: agentDescription exceeds 45 words')
        if not {'youtube-niche-bend', 'youtube-style-map'}.intersection(item.get('collections', [])):
            errors.append(f'{prefix}: reuse an existing research theme')
        published = None
        try:
            checked = datetime.fromisoformat(item['checkedAt'].replace('Z', '+00:00'))
            published = datetime.fromisoformat(item['publishedAt'].replace('Z', '+00:00'))
            if checked.tzinfo is None: raise ValueError('checkedAt needs a timezone')
            if published.tzinfo is None: published = published.replace(tzinfo=timezone.utc)
            if not timedelta(0) <= now - checked <= timedelta(days=1):
                errors.append(f'{prefix}: stats must have been checked within 24 hours')
            if published > now: errors.append(f'{prefix}: future upload date')
        except (ValueError, KeyError, TypeError) as ex:
            errors.append(f'{prefix}: invalid dates: {ex}')
        if 'bendIdea' not in item: continue  # companion source, not a proposed bend
        raw = item['bendIdea']
        if not isinstance(raw, str) or len(raw) > 4000:
            errors.append(f'{prefix}: bendIdea must be JSON text under the 4000-character backend limit')
            continue
        try:
            research = json.loads(raw)
            if research.get('v') != 1 or research.get('sourceVerdict') not in ['Proven', 'Format only']:
                raise ValueError('invalid research version or source verdict')
            if not research.get('validation') or research.get('checkedAt') != item.get('checkedAt'):
                raise ValueError('source validation and matching checkedAt required')
            if published is None: raise ValueError('source publication date unavailable')
            if now - published > timedelta(days=30): raise ValueError('packaging source older than 30 days')
            bends = research.get('bends', [])
            if not 1 <= len(bends) <= 3: raise ValueError('one to three bends required')
            for bend in bends:
                for key in ['niche','title','verdict','why','tension','urgency','thumbnail','style','format','adaptation']:
                    if not isinstance(bend.get(key), str) or not bend[key].strip(): raise ValueError(f'missing bend {key}')
                if bend['verdict'] not in ['Confirmed','Open','Contested','Crowded','Weak','Untested']:
                    raise ValueError('invalid target verdict')
                if len(bend.get('first30', [])) != 3 or not all(isinstance(s,str) and s.strip() for s in bend['first30']):
                    raise ValueError('all three first-30-second beats required')
                for key in ['demand','saturation','audienceFit','previousAttempts']:
                    reading = bend.get(key, {})
                    if not reading.get('summary') or not isinstance(reading.get('evidence'),list) or len(reading['evidence']) > 3:
                        raise ValueError(f'{key} needs summary and up to three evidence videos')
                    for video in reading['evidence']:
                        if not re.fullmatch(r'[\w-]{11}', video.get('id','')) or not video.get('title') or not isinstance(video.get('views'),int) or video['views'] < 0:
                            raise ValueError('evidence needs real video ID, title and nonnegative views')
                if bend['verdict'] != 'Untested' and not bend['demand']['evidence']:
                    raise ValueError('a recommendation needs on-topic demand evidence')
                fit = bend['audienceFit']
                if fit.get('verdict') not in ['Supported','Partial','Unknown','Mismatch']:
                    raise ValueError('audienceFit needs a valid verdict')
                if fit['verdict'] == 'Supported' and not fit['evidence']:
                    raise ValueError('Supported visual fit needs observed video evidence')
                if bend['verdict'] in ['Confirmed','Open'] and fit['verdict'] != 'Supported':
                    raise ValueError('Confirmed/Open needs Supported audience and visual fit')
                urgency_evidence = bend.get('urgencyEvidence')
                if urgency_evidence is not None and (not urgency_evidence.get('summary') or not urgency_evidence.get('url','').startswith('https://')):
                    raise ValueError('urgencyEvidence needs a summary and HTTPS source')
                external = bend.get('externalDemand', {})
                if not external.get('source') or not external.get('summary') or not external.get('url','').startswith('https://'):
                    raise ValueError('separate external demand reading required')
                if not isinstance(bend.get('toCheck'),list): raise ValueError('toCheck required')
            if 'passes-filters' in item.get('tagNames',[]) and research['sourceVerdict'] != 'Proven':
                raise ValueError('Format only sources cannot carry passes-filters')
        except (ValueError, KeyError, TypeError, UnboundLocalError) as ex:
            errors.append(f'{prefix}: {ex}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    collect_parser = sub.add_parser('collect')
    collect_parser.add_argument('--out', type=Path)
    collect_parser.add_argument('--queries', type=int, default=6, choices=range(1, 21))
    collect_parser.add_argument('--channels', type=int, default=6, choices=range(0, 13))
    check_parser = sub.add_parser('validate')
    check_parser.add_argument('payload', type=Path)
    args = parser.parse_args()
    if args.command == 'collect': return collect(args)
    errors = validate(args.payload)
    print(json.dumps({'ok': not errors, 'errors': errors}))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
