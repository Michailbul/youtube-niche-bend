from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json, os, pathlib
P = pathlib.Path(__file__).parent
os.chdir(P)

class H(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/save':
            self.send_error(404); return
        n = int(self.headers.get('Content-Length', 0))
        try:
            (P / 'keeps.json').write_text(json.dumps(json.loads(self.rfile.read(n)), indent=2, ensure_ascii=False))
        except Exception:
            self.send_error(400); return
        self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers(); self.wfile.write(b'{"saved":true}')

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store'); super().end_headers()

    def log_message(self, *a):
        pass

ThreadingHTTPServer(('127.0.0.1', 8793), H).serve_forever()
