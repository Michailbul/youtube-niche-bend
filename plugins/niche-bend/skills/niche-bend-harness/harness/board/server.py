#!/usr/bin/env python3
import os
"""3D opportunity board server (stdlib only). Local development preview.

  python3 server.py [--port 8810] [--host 127.0.0.1] [--by NAME]     (run from the project root)

GET  /                    board (index.html, board.js, style.css)
GET  /state.json          <project>/niche-bend/harness/state.json; falls back to sample-state.json while it does not exist
                          (header X-Board-Source: state | sample). 503 if state.json exists but is unreadable.
GET  /keeps.json          <project>/niche-bend/harness/keeps.json, read-only (kept / proposed badges)
GET  /round-img/<path>    images from <project>/niche-bend/format-lab/<path>, read in place, never copied
POST /keep                {"ids": [...], "note": "..."} -> nb.py keep <ids> --note ... --by <owner>
                          The board button is the human gate. Owner = --by flag, NB_OWNER or $USER. Sample points cannot be kept.
"""
import argparse, json, re, subprocess, sys, pathlib
from urllib.parse import unquote, urlsplit
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

BOARD = pathlib.Path(__file__).resolve().parent                       # static files, inside the plugin
HARNESS_CODE = BOARD.parent
NB = HARNESS_CODE / 'nb.py'
# Data lives in the project: ./niche-bend/ (or NB_WORK), the same folder nb.py uses.
WORK = pathlib.Path(os.environ.get('NB_WORK') or (pathlib.Path.cwd() / 'niche-bend')).resolve()
HOME = pathlib.Path(os.environ.get('NB_HOME') or (WORK / 'harness')).resolve()
LAB = pathlib.Path(os.environ.get('NB_FORMAT_LAB') or (WORK / 'format-lab')).resolve()
STATE = HOME / 'state.json'
SAMPLE = BOARD / 'sample-state.json'
KEEPS = HOME / 'keeps.json'
OWNER = re.sub(r'[^A-Za-z0-9._-]', '', os.environ.get('NB_OWNER') or os.environ.get('USER') or 'owner')[:40] or 'owner'
import secrets as _secrets
BOARD_TOKEN = _secrets.token_hex(16)
HOME.mkdir(parents=True, exist_ok=True)
_tok = HOME / '.board-token'
_tok.write_text(BOARD_TOKEN); os.chmod(_tok, 0o600)
ID_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._:-]{0,119}$')
IMG = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.gif': 'image/gif'}
STATIC = {'/', '/index.html', '/board.js', '/style.css', '/sample-state.json'}


def point_ids(data):
    pts = data.get('points') or (data.get('board') or {}).get('points') or []
    return {str(p.get('id')) for p in pts if isinstance(p, dict)}


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(BOARD), **k)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, *a):
        pass

    def send_json(self, code, obj, extra=None):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/state.json':
            return self.state()
        if path == '/keeps.json':
            if not KEEPS.exists():
                return self.send_json(200, {'entries': []})
            try:
                return self.send_json(200, json.loads(KEEPS.read_text()))
            except Exception as e:
                return self.send_json(503, {'error': f'keeps.json unreadable: {e}'})
        if path.startswith('/round-img/'):
            return self.round_img(unquote(path[len('/round-img/'):]))
        if path in STATIC:
            return super().do_GET()
        self.send_error(404)

    def state(self):
        if STATE.exists():
            try:
                body = STATE.read_bytes()
                json.loads(body)
            except Exception as e:  # the runner may be mid-write
                return self.send_json(503, {'error': f'state.json unreadable: {e}'}, {'X-Board-Source': 'error'})
            src = 'state'
        else:
            body, src = SAMPLE.read_bytes(), 'sample'
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Board-Source', src)
        self.end_headers()
        self.wfile.write(body)

    def round_img(self, rel):
        try:
            f = (LAB / rel).resolve()
            f.relative_to(LAB)
        except Exception:
            return self.send_error(403)
        if f.suffix.lower() not in IMG or not f.is_file():
            return self.send_error(404)
        data = f.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', IMG[f.suffix.lower()])
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if urlsplit(self.path).path != '/keep':
            return self.send_error(404)
        origin = self.headers.get('Origin')
        if origin and urlsplit(origin).netloc != self.headers.get('Host'):
            return self.send_json(403, {'error': 'cross-origin keep refused'})
        if 'application/json' not in (self.headers.get('Content-Type') or ''):
            return self.send_json(415, {'error': 'send application/json'})
        try:
            n = int(self.headers.get('Content-Length', 0))
            req = json.loads(self.rfile.read(min(n, 65536)) or b'{}')
            ids = [str(i) for i in req.get('ids') or []]
            note = str(req.get('note') or '').strip() or 'kept from the 3D board'
        except Exception:
            return self.send_json(400, {'error': 'bad JSON'})
        if not ids or len(ids) > 50 or not all(ID_RE.match(i) for i in ids) or len(note) > 2000:
            return self.send_json(400, {'error': 'ids must be 1-50 short IDs; note under 2000 characters'})
        if not STATE.exists():
            return self.send_json(409, {'error': 'the board is showing sample data; there is nothing real to keep'})
        try:
            known = point_ids(json.loads(STATE.read_text()))
        except Exception as e:
            return self.send_json(503, {'error': f'state.json unreadable: {e}'})
        unknown = [i for i in ids if i not in known]
        if unknown:
            return self.send_json(404, {'error': 'not in state.json', 'ids': unknown})
        if not NB.exists():
            return self.send_json(503, {'error': 'nb.py not found next to state.json; keep not written'})
        cmd = [sys.executable, str(NB), 'keep', *ids, '--note', note, '--by', OWNER]
        env = dict(os.environ, NB_BOARD_TOKEN=BOARD_TOKEN, NB_WORK=str(WORK), NB_HOME=str(HOME)); env.pop('NB_AGENT', None)
        try:
            p = subprocess.run(cmd, cwd=str(WORK.parent), capture_output=True, text=True, timeout=60, env=env)
        except subprocess.TimeoutExpired:
            return self.send_json(504, {'error': 'nb.py keep timed out'})
        self.send_json(200 if p.returncode == 0 else 500, {
            'ok': p.returncode == 0, 'code': p.returncode, 'ids': ids,
            'command': 'nb.py keep ' + ' '.join(ids) + ' --note ... --by ' + OWNER,
            'stdout': p.stdout[-4000:], 'stderr': p.stderr[-4000:]})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, default=8810)
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--by', help='name written on keeps from this board (default NB_OWNER or $USER)')
    a = ap.parse_args()
    global OWNER
    if a.by:
        OWNER = re.sub(r'[^A-Za-z0-9._-]', '', a.by)[:40] or OWNER
    src = 'state.json' if STATE.exists() else 'sample-state.json'
    print(f'opportunity board: http://{a.host}:{a.port}  (data: {src} in {HOME}; keeps signed {OWNER})', flush=True)
    ThreadingHTTPServer((a.host, a.port), H).serve_forever()


if __name__ == '__main__':
    main()
