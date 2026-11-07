"""Independent-recount tests use synthetic log text, not research observations."""
from pathlib import Path
import importlib.util
import unittest

P = Path(__file__).resolve().parents[1] / 'scripts/audit_period_results.py'
spec = importlib.util.spec_from_file_location('audit_period_results', P)
audit = importlib.util.module_from_spec(spec); spec.loader.exec_module(audit)


def fixture(error=True):
    return ('test 0001: a\ntest 0002: b\n' + ('[Error Found]: NO.1 AF\n' if error else '')
            + 'End Testing!\nTotal Error Interleavings: ' + ('1' if error else '0') + '\n')


class IndependentAuditTests(unittest.TestCase):
    def test_recounts_failure_position(self):
        self.assertEqual(audit.recount(fixture()), {'first_error_schedule': 2, 'observed_schedule_count': 2, 'reported_buggy_schedules': 1})

    def test_no_failure_remains_missing(self):
        self.assertIsNone(audit.recount(fixture(False))['first_error_schedule'])
        self.assertEqual(audit.stats([None, None, None])['missing_n'], 3)

    def test_duplicate_schedule_fails(self):
        with self.assertRaises(ValueError): audit.recount(fixture().replace('0002', '0001'))

    def test_missing_end_fails(self):
        with self.assertRaises(ValueError): audit.recount(fixture().replace('End Testing!', ''))

    def test_inconsistent_total_fails(self):
        with self.assertRaises(ValueError): audit.recount(fixture().replace('Interleavings: 1', 'Interleavings: 3'))

    def test_sample_standard_deviation(self):
        self.assertEqual(audit.stats([1, 2, 3])['sample_sd'], 1)
        self.assertIsNone(audit.stats([1])['sample_sd'])

    def test_nonfinite_and_boolean_fail(self):
        for x in (float('nan'), float('inf'), True):
            with self.assertRaises(ValueError): audit.stats([x])


if __name__ == '__main__': unittest.main()
