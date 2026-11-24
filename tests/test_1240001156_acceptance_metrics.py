"""Tests for the independent acceptance-metrics recount."""

import csv
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import audit_1240001156_acceptance_metrics as audit  # noqa: E402


BATCH = ROOT / 'results/2026-11-22/acceptance-45015126850-attempt1'
SUMMARY = ROOT / 'results/2026-11-22/summaries/acceptance-45015126850-attempt1'


class AcceptanceMetricsTests(unittest.TestCase):
    def test_empty_statistics_are_undefined_not_zero(self):
        self.assertEqual(
            audit.stats([]),
            {'n': 0, 'mean': None, 'sample_sd': None, 'min': None, 'max': None},
        )
        self.assertEqual(audit.formatted(audit.stats([])), 'NA (n=0)')
        self.assertIsNone(audit.optional_int(''))

    def test_archived_batch_reconciles_across_all_three_outputs(self):
        result = audit.audit(BATCH, SUMMARY)
        self.assertEqual(result['comparison_trials'], 30)
        self.assertEqual(result['method_groups'], 10)
        self.assertEqual(result['paired_case_rows'], 5)

    def test_events_outside_testing_block_are_rejected_with_matching_hash(self):
        case_dir = BATCH / 'account'
        records = json.loads((case_dir / 'records.json').read_text(encoding='utf-8'))
        record = next(item for item in records if item.get('log') == 'period_r01.txt')
        original = (case_dir / record['log']).read_bytes()
        events = (
            b'test 9999: [[0]]\n',
            b'[Error Found]: NO.999 assertion failed\n',
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / record['log']
            for event in events:
                for position in ('before start', 'after end'):
                    with self.subTest(event=event, position=position):
                        raw = event + original if position == 'before start' else original + event
                        path.write_bytes(raw)
                        # Keep byte integrity valid so this exercises the event boundary.
                        current = dict(record, log_sha256=hashlib.sha256(raw).hexdigest())
                        with self.assertRaisesRegex(ValueError, 'event outside testing block'):
                            audit.parse_comparison_log(path, current)

    def test_raw_hash_or_record_metric_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory) / 'batch'
            summary = Path(directory) / 'summary'
            shutil.copytree(BATCH, batch)
            shutil.copytree(SUMMARY, summary)

            raw = batch / 'account/period_r01.txt'
            raw.write_bytes(raw.read_bytes() + b'\n')
            with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
                audit.audit(batch, summary)

            shutil.copyfile(BATCH / 'account/period_r01.txt', raw)
            records_path = batch / 'account/records.json'
            records = json.loads(records_path.read_text(encoding='utf-8'))
            target = next(
                record for record in records
                if record.get('phase') == 'comparison'
                and record.get('log') == 'period_r01.txt'
            )
            target['schedules'] += 1
            records_path.write_text(json.dumps(records), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'records.json schedules mismatch'):
                audit.audit(batch, summary)

    def test_summary_json_csv_and_markdown_drift_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory) / 'batch'
            summary_dir = Path(directory) / 'summary'
            shutil.copytree(BATCH, batch)
            shutil.copytree(SUMMARY, summary_dir)

            summary_path = summary_dir / 'summary.json'
            summary = json.loads(summary_path.read_text(encoding='utf-8'))
            summary['groups'][0]['schedules']['mean'] += 1
            summary_path.write_text(json.dumps(summary), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'schedules: mean mismatch'):
                audit.audit(batch, summary_dir)

            shutil.copyfile(SUMMARY / 'summary.json', summary_path)
            csv_path = summary_dir / 'all_trials.csv'
            with csv_path.open(newline='', encoding='utf-8') as handle:
                rows = list(csv.reader(handle))
            header = rows[0]
            target = next(row for row in rows[1:] if row[1] == 'comparison')
            target[header.index('schedules')] = str(int(target[header.index('schedules')]) + 1)
            with csv_path.open('w', newline='', encoding='utf-8') as handle:
                csv.writer(handle).writerows(rows)
            with self.assertRaisesRegex(ValueError, 'CSV schedules mismatch'):
                audit.audit(batch, summary_dir)

            shutil.copyfile(SUMMARY / 'all_trials.csv', csv_path)
            markdown_path = summary_dir / 'SUMMARY.md'
            text = markdown_path.read_text(encoding='utf-8')
            text = text.replace(
                '| account | period | 3 / 3 | 10.0000 ± 0.0000 (n=3) |',
                '| account | period | 3 / 3 | 10.1000 ± 0.0000 (n=3) |',
                1,
            )
            markdown_path.write_text(text, encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Markdown first_error mismatch'):
                audit.audit(batch, summary_dir)


if __name__ == '__main__':
    unittest.main()
