"""Synthetic patch fixtures; no workload measurement is fabricated."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from run_period_compatible import adapt_serial

class CompatibilityTests(unittest.TestCase):
    def fixture(self):
        s='def setup_share_memroy():\n    return old_abi\ndef create_DBDS_subprocess(check_STDOUT, check_STDERR):\n    pass\n'
        for n,k in [('kpNumArray','SHARE_THREAD_NUM'),('kpYieldArray','SHARE_ARRAY_SIZE'),('kpLocArray','SHARE_ARRAY_SIZE'),('kpOrderArray','SHARE_ARRAY_SIZE')]:
            s+=n+' = (c_uint*'+k+')(0)\n'
        s+='period_limit = bugDepth + N - 1\nfor x in SBPSched():\n    print(x)\n'
        return s
    def test_only_abi_and_array_types_change(self):
        old=self.fixture(); new=old.replace('old_abi','new_abi')
        out=adapt_serial(old,new)
        self.assertIn('return new_abi',out);self.assertEqual(out.count('(c_uint16*'),4)
        start='period_limit = bugDepth + N - 1'
        self.assertEqual(out[out.index(start):],old[old.index(start):])
    def test_unexpected_source_is_rejected(self):
        with self.assertRaises(ValueError): adapt_serial('unexpected',self.fixture())
    def test_missing_array_is_rejected(self):
        with self.assertRaises(ValueError): adapt_serial(self.fixture().replace('kpOrderArray =','other ='),self.fixture())

if __name__=='__main__':unittest.main()
