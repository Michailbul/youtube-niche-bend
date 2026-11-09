"""MCP stdio server for the niche-bend harness. Stdlib only.

    python3 <plugin>/skills/niche-bend-harness/harness/mcp_server.py   (cwd = project root; data in ./niche-bend/)

Speaks JSON-RPC 2.0 over stdio, one message per line (initialize, tools/list, tools/call).
Read-only by design: it never calls YouTube, a paid API or launchd, and never runs a mode.
niche_status / niche_points run nb.py and return its JSON. The four mode tools return the exact
nb.py command a human runs, plus the current mode status. niche_keep refuses unless NB_HUMAN=1."""
import json, os, shlex, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NB = os.path.join(HERE, 'nb.py')
NBQ = 'python3 ' + shlex.quote(NB)                 # commands are run from the project root
PROTOCOL = '2024-11-05'
SERVER = {'name': 'niche-bend-harness', 'version': '1.0.0'}

MODE_COMMANDS = {
    'discover': [NBQ + ' discover --dry-run',
                 NBQ + ' discover [--seeds F] [--top 12] [--recheck W ...]'],
    'validate': [NBQ + ' validate [--ids a,b] --verifier <id> [--channels-json F] [--frames-json F]',
                 NBQ + ' validate --reconcile decisions.json --reconciler <id>'],
    'adapt': [NBQ + ' adapt'],
    'deliver': [NBQ + ' deliver'],
}
MODE_NOTES = {
    'discover': 'Calls YouTube through yt_scout.py (sequential, stops at the first 429). Run --dry-run first. '
                'This server does not run it.',
    'validate': 'The verifier and the reconciler must be different agents from the proposer; nb.py refuses otherwise.',
    'adapt': 'Reads human keeps only (status "kept"). Agent proposals do not count.',
    'deliver': 'Writes runs/<run>/delivery/BRIEF-<id>.md for kept packages only.',
}

TOOLS = [
    {'name': 'niche_status', 'description': 'Harness status: run pointer, mode status, point counts, keeps gate, next action. Runs nb.py status.',
     'inputSchema': {'type': 'object', 'properties': {}}},
    {'name': 'niche_points', 'description': 'points[] for the 3D opportunity board (demand, saturation, fit, freshness, verdict). Runs nb.py points --json.',
     'inputSchema': {'type': 'object', 'properties': {
         'verdict': {'type': 'string', 'description': 'open, confirmed, contested, crowded, weak, untested'},
         'round': {'type': 'string', 'description': 'round date, e.g. 2026-10-22'}}}},
    {'name': 'niche_keep', 'description': 'Keeps gate. Refused unless the server was started with NB_HUMAN=1. Only a channel owner keeps.',
     'inputSchema': {'type': 'object', 'required': ['ids', 'note', 'by'], 'properties': {
         'ids': {'type': 'array', 'items': {'type': 'string'}}, 'note': {'type': 'string'}, 'by': {'type': 'string'}}}},
] + [{'name': 'niche_' + m, 'description': 'Returns the exact nb.py %s command and the current mode status. Does not run it.' % m,
      'inputSchema': {'type': 'object', 'properties': {}}} for m in MODE_COMMANDS]


class ToolError(Exception):
    pass


def run_nb(args):
    r = subprocess.run([sys.executable, NB] + args, capture_output=True, text=True, env=dict(os.environ),
                       stdin=subprocess.DEVNULL, timeout=120)
    if r.returncode != 0:
        raise ToolError((r.stderr or r.stdout).strip() or 'nb.py exit %d' % r.returncode)
    return json.loads(r.stdout)


def call_tool(name, args):
    if name == 'niche_status':
        return run_nb(['status'])
    if name == 'niche_points':
        cmd = ['points', '--json']
        if args.get('verdict'): cmd += ['--verdict', args['verdict']]
        if args.get('round'): cmd += ['--round', args['round']]
        return run_nb(cmd)
    if name == 'niche_keep':
        if os.environ.get('NB_HUMAN') != '1':
            raise ToolError('REFUSED: keeps are a channel owner\'s decision, made by a human click on the board or in a terminal. '
                            'Agent proposals are not keeps. This server writes nothing to keeps.json unless it was '
                            'started with NB_HUMAN=1. The owner runs: nb.py keep <ids> '
                            '--note "why" --by <name>')
        ids, note, by = args.get('ids') or [], args.get('note'), args.get('by')
        if not ids or not note or not by:
            raise ToolError('ids, note and by are required')
        # nb.py still decides kept vs proposed (terminal or board token); over stdio it records a proposal.
        return run_nb(['keep'] + list(ids) + ['--note', note, '--by', by])
    mode = name[len('niche_'):] if name.startswith('niche_') else None
    if mode in MODE_COMMANDS:
        st = run_nb(['status'])
        return {'mode': mode, 'status': st['modes'].get(mode), 'ran': False, 'commands': MODE_COMMANDS[mode],
                'note': MODE_NOTES[mode], 'gate': st['gate'], 'next': st['next']}
    raise ToolError('unknown tool: %s' % name)


def handle(msg):
    method, mid = msg.get('method'), msg.get('id')
    if mid is None:                       # notification (e.g. notifications/initialized)
        return None
    if method == 'initialize':
        result = {'protocolVersion': (msg.get('params') or {}).get('protocolVersion') or PROTOCOL,
                  'capabilities': {'tools': {}}, 'serverInfo': SERVER}
    elif method == 'ping':
        result = {}
    elif method == 'tools/list':
        result = {'tools': TOOLS}
    elif method == 'tools/call':
        params = msg.get('params') or {}
        try:
            out = call_tool(params.get('name'), params.get('arguments') or {})
            result = {'content': [{'type': 'text', 'text': json.dumps(out, ensure_ascii=False)}], 'isError': False}
        except (ToolError, subprocess.TimeoutExpired, ValueError) as e:
            result = {'content': [{'type': 'text', 'text': str(e)}], 'isError': True}
    else:
        return {'jsonrpc': '2.0', 'id': mid, 'error': {'code': -32601, 'message': 'method not found: %s' % method}}
    return {'jsonrpc': '2.0', 'id': mid, 'result': result}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            resp = {'jsonrpc': '2.0', 'id': None, 'error': {'code': -32700, 'message': 'parse error'}}
        else:
            resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + '\n')
            sys.stdout.flush()


if __name__ == '__main__':
    main()
