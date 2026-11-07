"""Synthetic runner/parser tests. Fixtures are not experimental observations."""
import hashlib
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pilot = load('run_period_pilot')
summary = load('summarize_period')


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.log = self.root / 'raw.txt'

    def tearDown(self):
        self.temp.cleanup()

    def test_colored_output(self):
        self.log.write_text('test 0001: x\ntest 0002: y\n\x1b[31m[Error Found]: NO.1 AF\x1b[0m\nEnd Testing!\n')
        result = pilot.read_metrics(self.log)
        self.assertEqual(result['first_error_schedule'], 2)
        self.assertEqual(result['observed_schedule_count'], 2)
        self.assertTrue(result['end_marker'])

    def test_missing_output_stays_missing(self):
        self.log.write_text('Permission denied\n')
        result = pilot.read_metrics(self.log)
        self.assertIsNone(result['first_error_schedule'])
        self.assertFalse(result['end_marker'])

    def test_timeout_is_separate_from_bug(self):
        self.log.write_text('test 0001: x\n[Timeout 5]: NO.1\n')
        result = pilot.read_metrics(self.log)
        self.assertEqual(result['timeout_reports'], 1)
        self.assertEqual(result['reported_buggy_schedules'], 0)

    def test_execute_records_exit_code_and_hash(self):
        result = pilot.execute([sys.executable, '-c', 'print("fixture");raise SystemExit(3)'], self.root, self.log, 3)
        self.assertEqual(result['exit_code'], 3)
        self.assertEqual(result['log_sha256'], hashlib.sha256(self.log.read_bytes()).hexdigest())

    def test_outer_timeout_is_recorded(self):
        result = pilot.execute([sys.executable, '-c', 'import time;time.sleep(10)'], self.root, self.log, 0.05)
        self.assertTrue(result['timed_out'])
        self.assertNotEqual(result['exit_code'], 0)

    def test_missing_executable_is_recorded(self):
        result = pilot.execute([str(self.root / 'absent')], self.root, self.log, 1)
        self.assertEqual(result['exit_code'], 127)

    def fixture(self, **overrides):
        self.log.write_text('synthetic data\n')
        record = {'case': 'CS.reorder_3_bad', 'phase': 'run', 'status': 'complete',
                  'exit_code': 0, 'timed_out': False, 'end_marker': True,
                  'observed_schedule_count': 27, 'first_error_schedule': 6,
                  'reported_buggy_schedules': 6, 'elapsed_seconds': 1.0,
                  'log': 'raw.txt', 'log_sha256': hashlib.sha256(self.log.read_bytes()).hexdigest()}
        record.update(overrides)
        return record

    def test_three_repeats_and_sample_standard_deviation(self):
        rows = summary.summarize([self.fixture(elapsed_seconds=i) for i in (1., 2., 3.)], self.root)
        row = next(r for r in rows if r['case'] == 'CS.reorder_3_bad' and r['metric'] == 'elapsed_seconds')
        self.assertEqual(row['mean'], 2.)
        self.assertEqual(row['sample_sd'], 1.)

    def test_missing_case_is_not_zero_measurement(self):
        rows = summary.summarize([], self.root)
        self.assertTrue(all(r['mean'] is None for r in rows))
        self.assertTrue(all(r['comparison_status'] == 'insufficient_complete_runs' for r in rows))

    def test_timeout_is_excluded_not_zero_filled(self):
        rows = summary.summarize([self.fixture(timed_out=True)], self.root)
        row = next(r for r in rows if r['case'] == 'CS.reorder_3_bad')
        self.assertEqual(row['attempted_runs'], 1)
        self.assertEqual(row['complete_runs'], 0)
        self.assertIsNone(row['mean'])

    def test_checksum_failure(self):
        with self.assertRaises(ValueError):
            summary.summarize([self.fixture(log_sha256='incorrect')], self.root)

    def test_path_traversal_rejected(self):
        with self.assertRaises(ValueError):
            summary.summarize([self.fixture(log='../raw.txt')], self.root)

    def test_one_run_has_no_sample_sd(self):
        rows = summary.summarize([self.fixture()], self.root)
        row = next(r for r in rows if r['case'] == 'CS.reorder_3_bad')
        self.assertEqual(row['mean'], 6)
        self.assertIsNone(row['sample_sd'])


if __name__ == '__main__':
    unittest.main()
