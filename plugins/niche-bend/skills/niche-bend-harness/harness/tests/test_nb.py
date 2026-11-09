"""Stdlib tests for nb.py. Run from the harness folder:  python3 -m unittest discover -s tests -v
Every test works in a temp data dir (NB_WORK/NB_HOME); the bundled example rounds are read, never written."""
import importlib, json, os, subprocess, sys, tempfile, unittest

HARNESS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES = os.path.join(HARNESS, 'examples', 'format-lab')
ROUND2 = os.path.join(EXAMPLES, '2026-10-22')
ROUND1 = os.path.join(EXAMPLES, '2026-10-04')
SCHEMA_KEYS = {'id', 'format', 'niche', 'ourTitle', 'demand', 'saturation', 'fit', 'freshness', 'verdict',
               'confidence', 'source', 'proof', 'query', 'evidence', 'notes', 'round'}
AUTHOR = 'format-lab round author (agent)'


def load(path):
    with open(path) as f:
        return json.load(f)


def dump(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ['NB_HOME'] = self.tmp.name
        os.environ['NB_WORK'] = os.path.join(self.tmp.name, 'work', 'niche-bend')
        os.environ['NB_FORMAT_LAB'] = EXAMPLES                 # earlier rounds for the dedupe
        os.environ['NB_TODAY'] = '2026-10-22'
        os.environ.pop('NB_AGENT', None)
        sys.path.insert(0, HARNESS)
        import nb
        self.nb = importlib.reload(nb)

    def tearDown(self):
        self.tmp.cleanup()
        for k in ('NB_HOME', 'NB_WORK', 'NB_FORMAT_LAB', 'NB_TODAY'):
            os.environ.pop(k, None)

    def state(self):
        return load(os.path.join(self.tmp.name, 'state.json'))


class TestIngest(Base):
    def test_round2_points(self):
        r = self.nb.ingest(ROUND2)
        self.assertEqual(r['points'], 13)          # 4 formats x 3 targets + 1 merge
        pts = {q['id']: q for q in self.state()['points']}
        f1 = pts['you-wouldnt-last-formula-1']
        self.assertTrue(SCHEMA_KEYS <= set(f1))
        self.assertEqual(f1['demand'], 67)         # log10(465256) on the 10K..3M scale
        self.assertEqual(f1['saturation'], 35)     # 4 channels over 50K, 0 repeat
        self.assertEqual(f1['source']['checkedAt'], '2026-10-22')
        self.assertEqual(f1['query'], 'formula 1 history')
        self.assertFalse(f1['reconciled'])
        merge = pts['f1-1994-worse']
        self.assertIsNone(merge['demand'])         # missing number stays null, with a reason
        self.assertIn('no same-wording', merge['axes']['demand'])
        led = load(os.path.join(self.tmp.name, 'runs', '2026-10-22-ingest', 'ledger.json'))
        self.assertEqual(led['entries'][-1]['status'], 'complete')
        self.assertTrue(led['entries'][-1]['missing'])

    def test_reingest_is_idempotent(self):
        self.nb.ingest(ROUND1); self.nb.ingest(ROUND2); self.nb.ingest(ROUND2)
        self.assertEqual(len(self.state()['points']), 46)


class TestKeepGate(Base):
    def setUp(self):
        super().setUp()
        self.nb.ingest(ROUND2)

    def test_agent_keep_is_only_a_proposal(self):
        r = self.nb.keep(['you-wouldnt-last-formula-1'], 'looks good', 'scout-1', human=False)
        self.assertEqual(r['status'], 'proposed')
        with self.assertRaises(self.nb.Refused):
            self.nb.adapt()                        # proposals never feed ADAPT

    def test_nb_agent_env_forces_proposed(self):
        os.environ['NB_AGENT'] = 'packager'
        try:
            self.assertFalse(self.nb.is_human_tty())
        finally:
            os.environ.pop('NB_AGENT')

    def test_note_and_known_id_required(self):
        with self.assertRaises(self.nb.Refused):
            self.nb.keep(['you-wouldnt-last-formula-1'], '', 'michael', human=True)
        with self.assertRaises(self.nb.Refused):
            self.nb.keep(['made-up-id'], 'x', 'michael', human=True)

    def test_agent_can_not_overwrite_human_keep_and_adapt_deliver_run(self):
        self.nb.keep(['you-wouldnt-last-formula-1'], 'go', 'michael', human=True)
        r = self.nb.keep(['you-wouldnt-last-formula-1'], 'downgrade', 'scout-1', human=False)
        self.assertEqual(r['skippedHumanKeeps'], ['you-wouldnt-last-formula-1'])
        a = self.nb.adapt()
        self.assertEqual(a['packages'], 1)
        pk = load(os.path.join(self.tmp.name, 'runs', a['run'], 'packages.json'))['packages'][0]
        for k in ('sourceTitle', 'ourTitle', 'thumbnail', 'tension', 'urgency', 'adaptation', 'previousAttempts'):
            self.assertIn(k, pk)
        d = self.nb.deliver()
        self.assertEqual(d['status'], 'draft')     # tension/urgency/first30 still empty
        self.assertTrue(os.path.exists(os.path.join(self.nb.ROOT, d['briefs'][0]['path'])) or
                        os.path.exists(os.path.join(self.tmp.name, 'runs', a['run'], 'delivery', 'BRIEF-you-wouldnt-last-formula-1.md')))


class TestSelfCertification(Base):
    def setUp(self):
        super().setUp()
        self.nb.ingest(ROUND2)
        self.ch = os.path.join(self.tmp.name, 'channels.json')
        dump([{'handle': '@OfficialBeyondTheBlue', 'subs': 247000, 'medianViews': 293628,
               'checks': {'median50K': True, 'notOneHit': True, 'stillPosting': True, 'freshRatio': True}}], self.ch)

    def test_verifier_can_not_be_proposer(self):
        with self.assertRaises(self.nb.Refused):
            self.nb.validate(['you-wouldnt-last'], AUTHOR, self.ch)

    def test_reconciler_can_not_be_proposer_or_verifier(self):
        v = self.nb.validate(['you-wouldnt-last'], 'verifier-1', self.ch, run='2026-10-22')
        self.assertEqual(v['status'], 'awaiting-reconciler')
        row = load(os.path.join(self.tmp.name, 'runs', '2026-10-22', 'verdicts.json'))['verdicts'][0]
        # 247K subs fails notTooBig (one failed check demotes); 2.9M is 10x the median, so the gene survives
        self.assertEqual(row['sourceVerdict'], 'Format only')
        self.assertIn('notTooBig', row['failed'])
        dec = os.path.join(self.tmp.name, 'dec.json')
        dump({'you-wouldnt-last': {'decision': 'Format only', 'unresolved': ['frames'], 'strongestReason': 'big channel'}}, dec)
        for who in (AUTHOR, 'verifier-1'):
            with self.assertRaises(self.nb.Refused):
                self.nb.reconcile(dec, who, run='2026-10-22')
        r = self.nb.reconcile(dec, 'critic-1', run='2026-10-22')
        self.assertEqual(r['status'], 'complete')

    def test_one_failed_check_demotes(self):
        row = {c: True for c in self.nb.CHECKS}
        self.assertEqual(self.nb.source_verdict(row)[0], 'Proven')
        row['faceless'] = None
        self.assertEqual(self.nb.source_verdict(row)[0], 'Untested')
        row['faceless'] = False
        self.assertEqual(self.nb.source_verdict(row, outlier=True)[0], 'Format only')
        self.assertEqual(self.nb.source_verdict(row)[0], 'Pass')


class TestDedupe(Base):
    def test_previous_rounds_and_nogo(self):
        kept, dropped = self.nb.dedupe(['how long youd last in every', 'every _ with a strange mechanism explained',
                                        'the secret life of lighthouses'])
        self.assertEqual(kept, ['the secret life of lighthouses'])
        reasons = ' '.join(d['reason'] for d in dropped)
        self.assertIn('2026-10-22', reasons)

    def test_round2_dropped_table_is_read(self):
        kept, dropped = self.nb.dedupe(['explained in N minutes'])
        self.assertFalse(kept)

    def test_recheck_overrides(self):
        kept, _ = self.nb.dedupe(['how long youd last in every'], recheck=['how long youd last in every'])
        self.assertEqual(kept, ['how long youd last in every'])


class TestPoints(Base):
    def test_points_json_cli(self):
        self.nb.ingest(ROUND1)
        out = subprocess.run([sys.executable, os.path.join(HARNESS, 'nb.py'), 'points', '--json'],
                             capture_output=True, text=True, env=dict(os.environ))
        self.assertEqual(out.returncode, 0, out.stderr)
        pts = json.loads(out.stdout)
        self.assertEqual(len(pts), 33)
        for q in pts:
            self.assertTrue(SCHEMA_KEYS <= set(q), q['id'])
            for axis in ('demand', 'saturation', 'fit'):
                self.assertTrue(q[axis] is None or 0 <= q[axis] <= 100)
            self.assertTrue(0 <= q['freshness'] <= 1)
        self.assertLess(pts[0]['freshness'], 1)    # read 4 Oct, as of 22 Oct

    def test_status_cli(self):
        out = subprocess.run([sys.executable, os.path.join(HARNESS, 'nb.py'), 'status'], capture_output=True, text=True,
                             env=dict(os.environ))
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn('keeps gate', json.loads(out.stdout)['next'])


if __name__ == '__main__':
    unittest.main()


class TestInit(Base):
    def test_init_creates_project_folder_and_loads_examples(self):
        work = os.environ['NB_WORK']
        os.environ.pop('NB_FORMAT_LAB')                         # init uses the project's own format-lab
        self.nb = importlib.reload(self.nb)
        r = self.nb.init(examples=True)
        self.assertEqual(r['ingestedExamples'], ['2026-10-04', '2026-10-22'])
        for f in ('no-go.md', os.path.join('format-lab', '2026-10-22', 'lab.json')):
            self.assertTrue(os.path.exists(os.path.join(work, f)), f)
        self.assertTrue(os.path.exists(os.path.join(self.tmp.name, 'keeps.json')))
        self.assertEqual(len(self.state()['points']), 46)
        self.assertEqual(self.nb.nogo_path(), os.path.join(work, 'no-go.md'))
        again = self.nb.init(examples=True)                     # re-run never overwrites
        self.assertNotIn('no-go.md', ' '.join(again['created']))
        self.assertEqual(len(self.state()['points']), 46)
