"""Synthetic mechanics tests; these fixtures are not workload measurements."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from run_period_layout import adapt_capacity, condition_order, make_layout_probe
from run_period_layout import synthetic_decode_probe, EXPECTED_OFFSETS


class LayoutStudyTests(unittest.TestCase):
    def test_only_constant_changes_and_line_endings_survive(self):
        source = '# comment\r\nSHARE_ARRAY_SIZE = 1990\r\ndef schedule():\r\n    return 1990\r\n'
        expected = source.replace('SHARE_ARRAY_SIZE = 1990', 'SHARE_ARRAY_SIZE = 3964')
        self.assertEqual(adapt_capacity(source), expected)

    def test_patch_fails_closed_on_changed_or_duplicate_anchor(self):
        for source in ('SHARE_ARRAY_SIZE = 3964\n', 'SHARE_ARRAY_SIZE = 1990\n' * 2,
                       '# SHARE_ARRAY_SIZE = 1990\n'):
            with self.assertRaises(ValueError):
                adapt_capacity(source)

    def test_probe_uses_source_declaration_and_rejects_unexpected_runtime(self):
        runtime = '#define SHARE_MEMORY_THREAD_NUM 100\n#define SHARE_MEMORY_ARRAY_SIZE 3964\n'
        runtime += 'typedef struct Sched_Info {uint64_t time;} sched_info;\n'
        probe = make_layout_probe(runtime)
        self.assertIn('typedef struct Sched_Info {uint64_t time;} sched_info;', probe)
        self.assertIn('offsetof(sched_info,kpLoc)', probe)
        with self.assertRaises(ValueError):
            make_layout_probe(runtime.replace('3964', '1990'))

    def test_sentinel_exposes_wrong_fields_without_claiming_workload_result(self):
        result = synthetic_decode_probe({'sizeof': 24008, 'offsets': EXPECTED_OFFSETS})
        old = result['conditions']['capacity1990']
        new = result['conditions']['capacity3964']
        self.assertEqual((old['decoded_location'], old['decoded_order']), (101, 202))
        self.assertEqual((new['decoded_location'], new['decoded_order']), (202, 303))
        self.assertIn('Synthetic', result['scope'])
        with self.assertRaises(ValueError):
            synthetic_decode_probe({'sizeof': 24004, 'offsets': EXPECTED_OFFSETS})

    def test_registered_order_is_balanced(self):
        orders = [condition_order(repeat) for repeat in range(1, 11)]
        self.assertEqual(sum(pair[0] == 'capacity1990' for pair in orders), 5)
        self.assertTrue(all(set(pair) == {'capacity1990', 'capacity3964'} for pair in orders))


if __name__ == '__main__':
    unittest.main()
