"""Engineering acceptance boundaries using archived evidence and isolated copies.

The existing independent summarizer validates raw bytes first. Mutations below
exercise the additional acceptance requirements and never modify an archive.
"""
import copy
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import check_acceptance
import summarize_comparison


class AcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.batch = ROOT / 'results/2026-11-07/comparison-42384122902'
        cls.summary = summarize_comparison.summarize_batch(
            cls.batch, expected_repeats=3, expected_cases=['reorder_4'])

    def assess(self, batch=None, summary=None, timeout=240):
        return check_acceptance.assess(
            self.batch if batch is None else batch,
            self.summary if summary is None else summary, ['reorder_4'], 3, timeout)

    def test_complete_archived_three_pairs_pass(self):
        self.assertTrue(self.summary['integrity_ok'], self.summary['integrity_errors'])
        result = self.assess()
        self.assertTrue(result['accepted'], result['problems'])
        self.assertEqual(result['comparison_counts']['comparison_eligible'], 6)
        self.assertEqual(result['complete_pairs'], 3)
        self.assertEqual(result['diagnostic_eligible'], 0)

    def test_integrity_pass_with_censored_calls_is_not_acceptance(self):
        batch = ROOT / 'results/2026-11-07/comparison-42381922637'
        summary = summarize_comparison.summarize_batch(
            batch / 'reorder_4', expected_repeats=10, expected_cases=['reorder_4'])
        self.assertTrue(summary['integrity_ok'], summary['integrity_errors'])
        self.assertEqual(summary['denominators']['comparison_attempts'], 20)
        self.assertEqual(summary['denominators']['comparison_eligible'], 10)
        result = check_acceptance.assess(batch, summary, ['reorder_4'], 10, 120)
        self.assertFalse(result['accepted'])
        for reason in ('comparison_complete:', 'comparison_eligible:', 'incomplete eligible sample'):
            self.assertTrue(any(reason in item for item in result['problems']), result['problems'])

    def test_different_watchdog_is_a_protocol_failure(self):
        result = self.assess(timeout=120)
        self.assertFalse(result['accepted'])
        self.assertIn('reorder_4: environment settings differ from acceptance protocol', result['problems'])
        self.assertIn('reorder_4: per-invocation watchdog differs from protocol', result['problems'])

    def test_completed_inner_timeouts_and_budget_boundaries_are_rejected(self):
        for field, value in (('inner_timeouts', 1), ('schedules', 10000)):
            with self.subTest(field=field):
                summary = copy.deepcopy(self.summary)
                trial = next(row for row in summary['trials'] if row['phase'] == 'comparison')
                trial[field] = value
                self.assertTrue(summary['integrity_ok'])
                self.assertTrue(trial['complete'])
                self.assertTrue(trial['eligible'])
                result = self.assess(summary=summary)
                self.assertFalse(result['accepted'])
                self.assertTrue(any('inner timeout or schedule-budget truncation' in item
                                    for item in result['problems']), result['problems'])

    def test_missing_manifest_and_failed_container_reject_temporary_copies(self):
        for defect in ('manifest', 'container'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                batch = Path(directory) / 'batch'
                shutil.copytree(self.batch, batch)
                if defect == 'manifest':
                    (batch / 'archive_manifest.json').unlink()
                    reason = 'Missing outer archive manifest'
                else:
                    (batch / 'reorder_4/container_exit_code.txt').write_text('124\n')
                    reason = 'reorder_4: unexpected or absent container_exit_code.txt'
                result = self.assess(batch=batch)
                self.assertFalse(result['accepted'])
                self.assertIn(reason, result['problems'])


if __name__ == '__main__':
    unittest.main()
