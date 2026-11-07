"""Synthetic parser/patch fixtures; never treated as research measurements."""
from pathlib import Path
import sys
import unittest
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from run_period_comparison import parse_log,diagnostic_source,new_output_folders

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
    def test_failed_invocation_cannot_inherit_old_witnesses(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp);(directory/'out_target_old').mkdir()
            self.assertEqual(new_output_folders(directory,'target',{'out_target_old'}),[])
    def test_only_new_case_directories_supply_witnesses(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)
            for name in ['out_target_old','out_target_new','out_other_new']:(directory/name).mkdir()
            (directory/'out_target_file').write_text('not a directory')
            self.assertEqual([p.name for p in new_output_folders(directory,'target',{'out_target_old'})],['out_target_new'])

if __name__=='__main__':unittest.main()
