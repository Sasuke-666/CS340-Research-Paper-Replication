"""Differential and mutation checks for the two general raw-log parsers."""

import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from run_period_comparison import parse_log  # noqa: E402
from summarize_comparison import parse_raw_log  # noqa: E402


ARCHIVE_ROOTS = (
    ROOT / 'results/2026-11-07/comparison-42380929383',
    ROOT / 'results/2026-11-07/comparison-42381922637',
    ROOT / 'results/2026-11-07/comparison-42384122902',
    ROOT / 'results/member-reruns/1240001156-account-20261108T122201Z',
)
COMMON_FIELDS = (
    'schedules',
    'first_error',
    'buggy_schedules',
    'error_event_count',
    'complete_markers',
    'inner_timeouts',
)


def complete_logs():
    logs = []
    for root in ARCHIVE_ROOTS:
        for path in sorted(root.rglob('*.txt')):
            if not re.search(r'_r\d{2}\.txt$', path.name):
                continue
            text = path.read_text(encoding='utf-8')
            if parse_log(text)['complete_markers'] and parse_raw_log(text)['complete_markers']:
                logs.append(path)
    return logs


def valid_fixture():
    return (
        'Started UTC: 2026-11-22T00:00:00+00:00\n'
        'Command: ["python3", "runner", "-d", "3", "-f", "10000"]\n'
        'runs_limit: 10000\n'
        'Start Testing!\n'
        'test 0001: [[0], [1]]\n'
        'test 0002: [[1], [0]]\n'
        '    [Error Found]: NO.1 assertion failed\n'
        'End Testing!\n'
        'Total Error Interleavings: 1\n'
        'Total Timeouts Interleavings: 0\n'
        'Round\t0\t\t\t2\n'
        'Runner exit_code=0 timed_out=False elapsed_seconds=0.5\n'
    )


class ParserContractTests(unittest.TestCase):
    def test_all_archived_complete_logs_use_the_same_contract(self):
        logs = complete_logs()
        self.assertEqual(len(logs), 166)
        for path in logs:
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text(encoding='utf-8')
                live = parse_log(text)
                archived = parse_raw_log(text)
                self.assertTrue(live['complete_markers'])
                self.assertTrue(archived['complete_markers'])
                self.assertEqual(
                    {key: live[key] for key in COMMON_FIELDS},
                    {key: archived[key] for key in COMMON_FIELDS},
                )

    def test_mutation_matrix_fails_closed_in_both_parsers(self):
        base = valid_fixture()
        mutations = {
            'duplicate end marker': base + 'End Testing!\n',
            'event after completion': base + 'test 0003: [[0], [1], [0]]\n',
            'end marker after runner footer': (
                base.replace('End Testing!\n', '', 1) + 'End Testing!\n'
            ),
            'duplicate error total': base.replace(
                'Total Error Interleavings: 1\n',
                'Total Error Interleavings: 1\nTotal Error Interleavings: 1\n',
                1,
            ),
            'duplicate round footer': base.replace(
                'Round\t0\t\t\t2\n',
                'Round\t0\t\t\t2\nRound\t0\t\t\t2\n',
                1,
            ),
            'over-budget schedule': base.replace(
                'End Testing!\n',
                'test 10001: [[0], [1]]\nEnd Testing!\n',
                1,
            ),
            'unattributed error': (
                '[Error Found]: NO.1 assertion failed\n' + base
            ),
        }
        for name, text in mutations.items():
            with self.subTest(mutation=name):
                live = parse_log(text)
                archived = parse_raw_log(text)
                self.assertFalse(live['complete_markers'])
                self.assertFalse(archived['complete_markers'])
                self.assertTrue(archived['parse_problems'])


if __name__ == '__main__':
    unittest.main()
