"""Synthetic parser/patch fixtures; never treated as research measurements."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from run_period_comparison import parse_log,diagnostic_source

class ComparisonTests(unittest.TestCase):
    def fixture(self):
        return 'test 0001: [[0]]\ntest 0002: [[1]]\n[Error Found]: NO.1 AF\nEnd Testing!\nTotal Error Interleavings: 1\nRound\t0\t2\n'
    def test_counts(self):
        r=parse_log(self.fixture());self.assertTrue(r['complete_markers']);self.assertEqual(r['first_error'],2)
    def test_missing_remains_missing(self):
        r=parse_log(self.fixture().replace('[Error Found]: NO.1 AF\n','').replace('Interleavings: 1','Interleavings: 0'))
        self.assertTrue(r['complete_markers']);self.assertIsNone(r['first_error'])
    def test_no_end_rejected(self): self.assertFalse(parse_log(self.fixture().replace('End Testing!',''))['complete_markers'])
    def test_duplicate_rejected(self): self.assertFalse(parse_log(self.fixture().replace('0002','0001'))['complete_markers'])
    def test_prefix_counted(self): self.assertTrue(parse_log(self.fixture().replace('0002:', '0002 for prefix [0]:'))['complete_markers'])
    def test_inconsistent_total_rejected(self): self.assertFalse(parse_log(self.fixture().replace('Interleavings: 1','Interleavings: 2'))['complete_markers'])
    def test_diagnostic_patch_exact(self):
        s='int(Period*1.5)\n        process.communicate()\n        sys.exit()'
        out=diagnostic_source(s);self.assertIn('target_returncode',out);self.assertIn('CS340_REPLAY_SCALE',out)
    def test_diagnostic_patch_fails_closed(self):
        with self.assertRaises(ValueError): diagnostic_source('unknown source')

if __name__=='__main__':unittest.main()
