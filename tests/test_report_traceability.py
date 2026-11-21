"""Mutation regressions for report/evidence drift; these do not run workloads."""
import copy
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import audit_report


class ReportTraceabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / 'report/EXPANDED_REPORT.md').read_text(encoding='utf-8')
        cls.evidence = audit_report.load_evidence(ROOT)

    def changed(self, old, new):
        self.assertEqual(self.text.count(old), 1, 'Mutation target must be unique')
        return self.text.replace(old, new, 1)

    def assert_rejected(self, text, message):
        result = audit_report.audit_text(text, self.evidence)
        self.assertFalse(result['integrity_ok'])
        self.assertTrue(any(message in error for error in result['errors']), result['errors'])
        return result

    def test_archived_report_matches_all_bound_tables(self):
        result = audit_report.audit_text(self.text, self.evidence)
        self.assertTrue(result['integrity_ok'], result['errors'])
        self.assertEqual(result['quantitative_tables'], [str(n) for n in range(2, 13)])
        self.assertEqual(result['checked_cells'], 321)
        self.assertEqual(result['quantitative_or_missingness_cells'], 236)
        self.assertEqual(result['caption_count'], 18)
        self.assertEqual(result['revision_date'], (ROOT / 'report/REVISION_DATE').read_text().strip())

    def test_revision_header_cannot_drift_from_the_release_date(self):
        text = self.changed(self.evidence['revision_marker'], 'Stage report revised 1 January 2000.')
        self.assert_rejected(text, 'Report header does not match report/REVISION_DATE')

    def test_means_sample_sd_and_paper_gaps_cannot_drift(self):
        mutations = (
            ('| account | First failing schedule | 2 | 10.100 ± 0.316 | +8.100 | +405.00% |',
             '| account | First failing schedule | 2 | 10.200 ± 0.316 | +8.100 | +405.00% |', 'Table 2, row 7, Ours'),
            ('| account | Buggy schedules | 26 | 24.400 ± 2.914 | -1.600 | -6.15% |',
             '| account | Buggy schedules | 26 | 24.400 ± 2.999 | -1.600 | -6.15% |', 'Table 2, row 9, Ours'),
            ('| account | First failing schedule | 2 | 10.100 ± 0.316 | +8.100 | +405.00% |',
             '| account | First failing schedule | 2 | 10.100 ± 0.316 | +8.100 | +40.50% |', 'Table 2, row 7, Relative delta'),
            ('| account / 10 | -0.300 ± 1.160 | +0.000 ± 0.000 | +1.400 ± 4.402 | +1.070 ± 4.323 |',
             '| account / 10 | -0.300 ± 1.160 | +0.000 ± 0.000 | +1.400 ± 4.402 | +1.070 ± 4.000 |', 'Table 12, row 1, Elapsed-second delta'),
        )
        for old, new, message in mutations:
            with self.subTest(error=message):
                self.assert_rejected(self.changed(old, new), message)

    def test_sample_sizes_remain_explicit_and_correct(self):
        mutations = (
            ('paper Table 2; n=10 per case.', 'paper Table 2; n=20 per case.', 'Table 2: missing or changed sample'),
            ('| account / A | 10 |', '| account / A | 9 |', 'Table 11, row 1, n'),
            ('| account / 10 |', '| account / 20 |', 'Table 12, row 1, Case / pairs'),
        )
        for old, new, message in mutations:
            with self.subTest(error=message):
                self.assert_rejected(self.changed(old, new), message)

    def test_paired_direction_and_paper_gap_direction_are_preserved(self):
        mutations = (
            ('Paired time difference (Serial - PERIOD)', 'Paired time difference (PERIOD - Serial)', 'Table 5: header'),
            ('Within-pair change, B minus A,', 'Within-pair change, A minus B,', 'Table 12: missing or changed sample'),
            ('Signed delta is our mean minus the paper value', 'Signed delta is the paper value minus our mean', 'signed paper-gap orientation'),
        )
        for old, new, message in mutations:
            with self.subTest(error=message):
                self.assert_rejected(self.changed(old, new), message)

    def test_unknown_and_not_observed_are_not_converted_to_zero(self):
        mutations = (
            ('| Original account, run 43570556202 | 20 | Unknown | Unknown | Unknown | Unknown |',
             '| Original account, run 43570556202 | 20 | 0 | 0 | 0 | 0 |', 'Table 10, row 1, Recorded'),
            ('| 1 | 3.000 ± 0.000 | 0.000 ± 0.000 | 0/3 | Not observed | 0.371 ± 0.092 |',
             '| 1 | 3.000 ± 0.000 | 0.000 ± 0.000 | 0/3 | 0.000 ± 0.000 | 0.371 ± 0.092 |', 'Table 7, row 1, First failing schedule'),
        )
        for old, new, message in mutations:
            with self.subTest(error=message):
                self.assert_rejected(self.changed(old, new), message)

    def test_batch_scope_and_replay_outcomes_cannot_be_relabelled(self):
        mutations = (
            ('| Recovery account, run 43575584325 |', '| Recovery account, run 43570556202 |', 'Table 10, row 3, Scope'),
            ('n=3 from follow-up 42384122902.', 'n=3 from follow-up 42381922637.', 'Table 3: missing or changed sample'),
            ('| Original follow-up | 4/5 expected assertions | Not run |',
             '| Original follow-up | 5/5 expected assertions | Not run |', 'Table 6, row 1, Multiplier 1.5'),
        )
        for old, new, message in mutations:
            with self.subTest(error=message):
                self.assert_rejected(self.changed(old, new), message)

    def test_native_offsets_and_controlled_metrics_remain_bound(self):
        for number, row, column in (('9', 1, 1), ('11', 2, 4)):
            binding = self.evidence['tables'][number]
            original = '| ' + ' | '.join(binding['rows'][row]) + ' |'
            changed = list(binding['rows'][row])
            changed[column] = '999.000'
            with self.subTest(table=number):
                self.assert_rejected(self.changed(original, '| ' + ' | '.join(changed) + ' |'), 'Table ' + number + ', row')

    def test_each_caption_is_required_exactly_once(self):
        caption = re.search(r'^\*\*Table 7\..*$', self.text, re.M)[0]
        with self.subTest(kind='missing'):
            self.assert_rejected(self.changed(caption, ''), 'Table 7: expected one registered caption, found 0')
        with self.subTest(kind='duplicate'):
            self.assert_rejected(self.text + '\n\n' + caption + '\n', 'Table 7: expected one registered caption, found 2')

    def test_captions_do_not_count_as_narrative_references(self):
        fixture = ('**Table 7. Depth observations.**\n'
                   '| Reference | Table 7 |\n'
                   '![Figure 1](figure.svg)\n'
                   '**Figure 1. Failure counts.**\n'
                   '## Table 7 and Figure 1\n')
        self.assertEqual(audit_report.narrative_references(fixture),
                         {'Table': set(), 'Figure': set()})
        self.assertEqual(audit_report.narrative_references(
            fixture + '\nTables 2–12 contain the evidence. Figure 1 displays the counts.\n'),
            {'Table': {str(n) for n in range(2, 13)}, 'Figure': {'1'}})

        # Remove every prose callout, including ranges and repeated references.
        # Preserve captions, tables, images and headings so they cannot satisfy
        # the requirement by themselves. This remains valid as prose expands.
        lines = []
        for line in self.text.splitlines():
            protected = line.lstrip().startswith(('**Table ', '**Figure ', '|', '![', '#'))
            if protected or not re.search(r'\b(?:Tables?|Figures?)\b', line):
                lines.append(line)
        text = '\n'.join(lines)
        for kind in ('Figure 1', 'Table 7'):
            with self.subTest(reference=kind):
                self.assertIn('**' + kind + '.', text)
                self.assert_rejected(text, kind + ': missing narrative reference')

    def test_missing_or_duplicated_evidence_rows_fail(self):
        row = '| account / A | 10 | 10.500 ± 0.850 | 65.000 ± 0.000 | 22.900 ± 3.281 | 23.569 ± 3.547 |'
        with self.subTest(kind='missing'):
            self.assert_rejected(self.changed(row + '\n', ''), 'Table 11: expected 4 evidence rows, found 3')
        with self.subTest(kind='duplicate'):
            self.assert_rejected(self.changed(row, row + '\n' + row), 'Table 11: expected 4 evidence rows, found 5')

    def test_figure_must_have_a_readable_local_target(self):
        text = self.changed('../results/2026-11-07/figures/expanded_paper_gaps.svg',
                            '../results/2026-11-07/figures/missing_report_figure.svg')
        self.assert_rejected(text, 'Figure 1: missing or external image target')

    def test_unverified_or_wrong_batch_evidence_fails_closed(self):
        original_read = audit_report.read_json
        for field, value in (('integrity_ok', False), ('batch', 'comparison-other-batch')):
            def changed_source(root, relative):
                result = original_read(root, relative)
                if relative == audit_report.SUMMARIES['primary']:
                    result = copy.deepcopy(result)
                    result[field] = value
                return result
            with self.subTest(field=field), patch.object(audit_report, 'read_json', side_effect=changed_source):
                with self.assertRaisesRegex(ValueError, 'Unverified or wrong-scope summary'):
                    audit_report.load_evidence(ROOT)


if __name__ == '__main__':
    unittest.main()
