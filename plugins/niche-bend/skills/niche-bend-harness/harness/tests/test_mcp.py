"""Stdlib tests for mcp_server.py. Run from the harness folder:
    python3 -m unittest discover -s tests -v
Feeds JSON-RPC on stdin; the harness state is a temp NB_HOME, never the real one."""
import json, os, subprocess, sys, tempfile, unittest

HARNESS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER = os.path.join(HARNESS, 'mcp_server.py')
TOOLS = {'niche_status', 'niche_points', 'niche_keep', 'niche_discover', 'niche_validate', 'niche_adapt', 'niche_deliver'}


def rpc(i, method, params=None):
    return json.dumps({'jsonrpc': '2.0', 'id': i, 'method': method, 'params': params or {}})


class TestMCP(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = dict(os.environ, NB_HOME=self.tmp.name, NB_WORK=os.path.join(self.tmp.name, 'work', 'niche-bend'),
                        NB_FORMAT_LAB=os.path.join(HARNESS, 'examples', 'format-lab'), NB_TODAY='2026-10-22')
        self.env.pop('NB_HUMAN', None)

    def tearDown(self):
        self.tmp.cleanup()

    def session(self, *lines, env=None):
        stdin = '\n'.join(lines + (json.dumps({'jsonrpc': '2.0', 'method': 'notifications/initialized'}),)) + '\n'
        r = subprocess.run([sys.executable, SERVER], input=stdin, capture_output=True, text=True,
                           env=env or self.env, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        return {m['id']: m for m in map(json.loads, r.stdout.splitlines())}

    def test_initialize_list_status(self):
        out = self.session(rpc(1, 'initialize', {'protocolVersion': '2024-11-05'}), rpc(2, 'tools/list'),
                           rpc(3, 'tools/call', {'name': 'niche_status', 'arguments': {}}))
        self.assertEqual(out[1]['result']['serverInfo']['name'], 'niche-bend-harness')
        self.assertIn('tools', out[1]['result']['capabilities'])
        self.assertEqual({t['name'] for t in out[2]['result']['tools']}, TOOLS)
        res = out[3]['result']
        self.assertFalse(res['isError'], res)
        st = json.loads(res['content'][0]['text'])
        self.assertEqual(st['schema'], 'nb-state/1')
        self.assertEqual(st['modes']['discover'], 'not run')
        self.assertIn('gate', st)

    def test_keep_refused_without_human(self):
        out = self.session(rpc(1, 'tools/call', {'name': 'niche_keep',
                                                 'arguments': {'ids': ['x'], 'note': 'n', 'by': 'agent'}}))
        res = out[1]['result']
        self.assertTrue(res['isError'])
        self.assertIn('REFUSED', res['content'][0]['text'])
        self.assertFalse(os.path.exists(os.path.join(self.tmp.name, 'keeps.json')))

    def test_mode_tools_do_not_run(self):
        out = self.session(*[rpc(i, 'tools/call', {'name': 'niche_' + m, 'arguments': {}})
                             for i, m in enumerate(('discover', 'validate', 'adapt', 'deliver'), 1)])
        for i in range(1, 5):
            body = json.loads(out[i]['result']['content'][0]['text'])
            self.assertFalse(body['ran'])
            self.assertEqual(body['status'], 'not run')
            self.assertTrue(body['commands'][0].startswith('python3 ') and 'nb.py ' in body['commands'][0])
        self.assertFalse(os.path.exists(os.path.join(self.tmp.name, 'runs')))

    def test_points_and_unknown_method(self):
        out = self.session(rpc(1, 'tools/call', {'name': 'niche_points', 'arguments': {'verdict': 'open'}}),
                           rpc(2, 'nope'))
        self.assertEqual(json.loads(out[1]['result']['content'][0]['text']), [])
        self.assertEqual(out[2]['error']['code'], -32601)


if __name__ == '__main__':
    unittest.main()
