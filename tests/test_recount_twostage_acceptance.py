"""Offline regression tests for the twostage recount using synthetic log bytes."""
import hashlib
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from recount_twostage_acceptance import recount


# The first request succeeds. The first error is reported on request 2.
PREFIX = """runs_limit: 10000
Start Testing!
test 0001: [[0], [1]]
test 0002: [[1], [0]]
    [Error Found]: NO.1 assertion failed
"""
THIRD_REQUEST = "test 0003: [[0], [1], [0]]\n"
SECOND_ERROR = "    [Error Found]: NO.2 assertion failed\n"
FOOTER = """End Testing!
Total Error Interleavings: 2
Total Timeouts Interleavings: 0
Round 0 3
Runner exit_code=0 timed_out=False elapsed_seconds=0.5
"""


class TwostageRecountTests(unittest.TestCase):
    def recount_fixture(self, log, buggy_schedules):
        raw = log.encode('utf-8')
        record = {
            'log_sha256': hashlib.sha256(raw).hexdigest(),
            'schedules': 3,
            'first_error': 2,
            'buggy_schedules': buggy_schedules,
            'error_event_count': 2,
            'status': 'complete',
            'complete_markers': True,
            'exit_code': 0,
            'timed_out': False,
            'inner_timeouts': 0,
            'budget_reached': False,
            'timeout_seconds': 240,
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'synthetic.txt'
            path.write_bytes(raw)
            with redirect_stdout(io.StringIO()):
                return recount(path, record)

    def test_complete_log_counts_distinct_failing_requests(self):
        log = PREFIX + THIRD_REQUEST + SECOND_ERROR + FOOTER
        self.assertEqual(self.recount_fixture(log, buggy_schedules=2),
                         {'schedules': 3, 'first_error': 2, 'buggy_schedules': 2})

    def test_two_error_events_on_one_request_count_as_one_failing_schedule(self):
        log = PREFIX + SECOND_ERROR + THIRD_REQUEST + FOOTER
        self.assertEqual(self.recount_fixture(log, buggy_schedules=1),
                         {'schedules': 3, 'first_error': 2, 'buggy_schedules': 1})

    def test_missing_end_marker_is_rejected_even_with_valid_hash_and_footer(self):
        log = PREFIX + THIRD_REQUEST + SECOND_ERROR + FOOTER.removeprefix('End Testing!\n')
        with self.assertRaisesRegex(ValueError, 'End Testing!'):
            self.recount_fixture(log, buggy_schedules=2)
