#!/usr/bin/env python3
"""Independently recount acceptance metrics without importing the summarizer."""

import argparse
import csv
import hashlib
import json
import math
import re
import statistics
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BATCH = ROOT / 'results/2026-11-22/acceptance-45015126850-attempt1'
DEFAULT_SUMMARY = (
    ROOT / 'results/2026-11-22/summaries/acceptance-45015126850-attempt1'
)
CASES = ('account', 'lazy01', 'reorder_3', 'reorder_4', 'twostage')
METHODS = ('author_serialized_abi16', 'period')
ANSI = re.compile(r'\x1b\[[0-9;]*m')
TEST_LINE = re.compile(r'^\s*test\s+(\d+)(?:\s+for prefix\s+[^:]+)?:\s*(.+)$')
ERROR_LINE = re.compile(
    r'^\s*\[Error Found\]:\s*NO\.(\d+)\s+assertion failed\s*$'
)
ERROR_TOTAL = re.compile(r'^\s*Total Error Interleavings:\s*(\d+)\s*$')
TIMEOUT_TOTAL = re.compile(r'^\s*Total Timeouts Interleavings:\s*(\d+)\s*$')
ROUND_TOTAL = re.compile(r'^\s*Round\s+0\s+(\d+)\s*$')
RUNNER = re.compile(
    r'^\s*Runner exit_code=(-?\d+) timed_out=(True|False) '
    r'elapsed_seconds=([0-9.]+)\s*$'
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def optional_int(value):
    return None if value == '' else int(value)


def close(left, right):
    if left is None or right is None:
        return left is right
    # Raw runner footers retain six decimal places; records.json retains the
    # full process timing. One microsecond still exceeds their rounding error.
    return math.isclose(float(left), float(right), rel_tol=1e-12, abs_tol=1e-6)


def stats(values):
    values = list(values)
    return {
        'n': len(values),
        'mean': statistics.mean(values) if values else None,
        'sample_sd': statistics.stdev(values) if len(values) > 1 else None,
        'min': min(values) if values else None,
        'max': max(values) if values else None,
    }


def assert_stats(actual, expected, label):
    for field in ('n', 'mean', 'sample_sd', 'min', 'max'):
        require(actual is not None, label + ': missing statistics')
        require(field in actual and field in expected, label + ': missing ' + field)
        if field == 'n':
            require(actual[field] == expected[field], label + ': n mismatch')
        else:
            require(close(actual[field], expected[field]), label + ': ' + field + ' mismatch')


def parse_comparison_log(path, record, budget=10000):
    """Parse one archived comparison log using only standard-library logic."""
    raw = path.read_bytes()
    require(
        hashlib.sha256(raw).hexdigest() == record['log_sha256'],
        path.name + ': SHA-256 mismatch',
    )
    clean = ANSI.sub('', raw.decode('utf-8'))
    lines = clean.splitlines()
    starts = [index for index, line in enumerate(lines) if line.strip() == 'Start Testing!']
    ends = [index for index, line in enumerate(lines) if line.strip() == 'End Testing!']
    require(len(starts) == 1, path.name + ': expected exactly one start marker')
    require(len(ends) == 1, path.name + ': expected exactly one end marker')
    start, end = starts[0], ends[0]
    require(start < end, path.name + ': completion markers are out of order')
    for line in lines[:start] + lines[end + 1:]:
        require(
            not (TEST_LINE.match(line) or '[Error Found]' in line),
            path.name + ': test or error event outside testing block',
        )

    budget_lines = [
        int(line.split(':', 1)[1].strip())
        for line in lines[:start]
        if re.match(r'^\s*runs_limit:', line)
    ]
    require(budget_lines == [budget], path.name + ': unexpected schedule budget')

    ordinals, failed, error_numbers, current = [], [], [], None
    for line in lines[start + 1:end]:
        test = TEST_LINE.match(line)
        if test:
            current = int(test.group(1))
            ordinals.append(current)
        if '[Error Found]' in line:
            error = ERROR_LINE.match(line)
            require(current is not None, path.name + ': error before any test')
            require(error is not None, path.name + ': malformed error marker')
            failed.append(current)
            error_numbers.append(int(error.group(1)))

    require(ordinals, path.name + ': no schedules')
    require(
        ordinals == list(range(1, len(ordinals) + 1)),
        path.name + ': schedule ordinals are not exactly 1..N',
    )
    require(len(ordinals) < budget, path.name + ': schedule budget was reached')
    require(error_numbers == list(range(1, len(error_numbers) + 1)),
            path.name + ': error event numbers are not exactly 1..E')
    require(len(failed) == len(set(failed)),
            path.name + ': one schedule has repeated error events')

    footer = lines[end + 1:]
    error_totals = [
        (index, int(match.group(1)))
        for index, line in enumerate(footer)
        for match in [ERROR_TOTAL.match(line)]
        if match
    ]
    timeout_totals = [
        (index, int(match.group(1)))
        for index, line in enumerate(footer)
        for match in [TIMEOUT_TOTAL.match(line)]
        if match
    ]
    round_totals = [
        (index, int(match.group(1)))
        for index, line in enumerate(footer)
        for match in [ROUND_TOTAL.match(line)]
        if match
    ]
    runners = [
        (index, match)
        for index, line in enumerate(footer)
        for match in [RUNNER.match(line)]
        if match
    ]
    for label, entries in (
        ('error-total', error_totals),
        ('timeout-total', timeout_totals),
        ('round-total', round_totals),
        ('runner', runners),
    ):
        require(len(entries) == 1, path.name + ': missing or repeated ' + label)
    positions = (
        error_totals[0][0],
        timeout_totals[0][0],
        round_totals[0][0],
        runners[0][0],
    )
    require(positions == tuple(sorted(positions)), path.name + ': footer markers are out of order')
    require(error_totals[0][1] == len(failed),
            path.name + ': error total disagrees with raw events')
    require(timeout_totals[0][1] == 0, path.name + ': timeout total is nonzero')
    require(round_totals[0][1] == len(ordinals),
            path.name + ': round total disagrees with schedules')
    runner = runners[0][1]
    require(runner.group(1) == '0', path.name + ': runner exit code is nonzero')
    require(runner.group(2) == 'False', path.name + ': runner timed out')
    require(not re.search(r'\[Timeout\s', clean), path.name + ': inner timeout found')

    metrics = {
        'schedules': len(ordinals),
        'first_error': failed[0] if failed else None,
        'buggy_schedules': len(failed),
        'error_event_count': len(failed),
        'inner_timeouts': 0,
        'elapsed_seconds': float(runner.group(3)),
    }
    for field in ('schedules', 'first_error', 'buggy_schedules', 'error_event_count', 'inner_timeouts'):
        require(
            record.get(field) == metrics[field],
            path.name + ': records.json ' + field + ' mismatch',
        )
    require(close(record.get('elapsed_seconds'), metrics['elapsed_seconds']),
            path.name + ': records.json elapsed_seconds mismatch')
    require(record.get('status') == 'complete', path.name + ': record is not complete')
    require(record.get('exit_code') == 0, path.name + ': record exit code is nonzero')
    require(record.get('timed_out') is False, path.name + ': record timed out')
    require(record.get('budget_reached') is False, path.name + ': record reached budget')
    return metrics


def collect_trials(batch):
    trials = []
    for case in CASES:
        case_dir = batch / case
        records_path = case_dir / 'records.json'
        require(records_path.is_file(), case + ': missing records.json')
        records = json.loads(records_path.read_text(encoding='utf-8'))
        comparisons = [record for record in records if record.get('phase') == 'comparison']
        require(len(comparisons) == 6, case + ': expected six comparison records')
        expected_logs = {
            method + '_r%02d.txt' % repeat
            for method in METHODS
            for repeat in range(1, 4)
        }
        require({record.get('log') for record in comparisons} == expected_logs,
                case + ': unexpected comparison log set')
        for record in sorted(comparisons, key=lambda item: item['log']):
            metrics = parse_comparison_log(case_dir / record['log'], record)
            trials.append({
                'case': case,
                'method': record['method'],
                'repeat': record['repeat'],
                'log': case + '/' + record['log'],
                'log_sha256': record['log_sha256'],
                **metrics,
            })
    require(len(trials) == 30, 'expected 30 comparison trials')
    return trials


def aggregate(trials):
    aggregate_rows = {}
    metric_keys = ('first_error', 'schedules', 'buggy_schedules', 'elapsed_seconds')
    for case in CASES:
        for method in METHODS:
            selected = [
                trial for trial in trials
                if trial['case'] == case and trial['method'] == method
            ]
            require(len(selected) == 3, case + '/' + method + ': expected three trials')
            aggregate_rows[(case, method)] = {
                'trials': selected,
                'stats': {
                    key: stats(trial[key] for trial in selected if trial[key] is not None)
                    for key in metric_keys
                },
            }
    return aggregate_rows


def paired_rows(aggregate_rows):
    rows = {}
    for case in CASES:
        period = {
            trial['repeat']: trial
            for trial in aggregate_rows[(case, 'period')]['trials']
        }
        serialized = {
            trial['repeat']: trial
            for trial in aggregate_rows[(case, 'author_serialized_abi16')]['trials']
        }
        require(set(period) == set(serialized) == {1, 2, 3},
                case + ': incomplete repetition pairing')
        ordered = [(period[index], serialized[index]) for index in (1, 2, 3)]
        rows[case] = {
            'serial_minus_period_seconds': stats(
                serial['elapsed_seconds'] - period_trial['elapsed_seconds']
                for period_trial, serial in ordered
            ),
            'serial_over_period_time_ratio': stats(
                serial['elapsed_seconds'] / period_trial['elapsed_seconds']
                for period_trial, serial in ordered
            ),
            'schedule_reduction_pct': stats(
                (serial['schedules'] - period_trial['schedules'])
                / serial['schedules'] * 100
                for period_trial, serial in ordered
            ),
        }
    return rows


def reconcile_summary_json(summary, aggregate_rows, paired):
    require(summary.get('schema_version') == 1, 'summary schema version mismatch')
    require(summary.get('integrity_ok') is True, 'summary integrity is not OK')
    groups = summary.get('groups', [])
    by_key = {(group.get('case'), group.get('method')): group for group in groups}
    require(len(by_key) == len(groups) == 10, 'summary must contain ten method groups')
    for (case, method), expected in aggregate_rows.items():
        label = case + '/' + method
        group = by_key.get((case, method))
        require(group is not None, label + ': missing summary group')
        require(group.get('attempted_n') == 3, label + ': attempted_n mismatch')
        require(group.get('complete_n') == 3, label + ': complete_n mismatch')
        require(group.get('eligible_n') == 3, label + ': eligible_n mismatch')
        for metric in ('first_error', 'schedules', 'buggy_schedules', 'elapsed_seconds'):
            assert_stats(group.get(metric), expected['stats'][metric], label + '/' + metric)

    denominators = summary.get('denominators', {})
    require(denominators.get('comparison_attempts') == 30, 'comparison denominator mismatch')
    require(denominators.get('comparison_complete') == 30, 'complete denominator mismatch')
    require(denominators.get('comparison_eligible') == 30, 'eligible denominator mismatch')
    require(denominators.get('diagnostic_attempts') == 40, 'diagnostic denominator mismatch')

    summary_pairs = {
        row.get('case'): row for row in summary.get('paired_comparisons', [])
    }
    require(len(summary_pairs) == 5, 'summary must contain five paired rows')
    for case, expected in paired.items():
        row = summary_pairs.get(case)
        require(row is not None, case + ': missing paired summary')
        require(row.get('n_complete_pairs') == 3, case + ': paired n mismatch')
        for metric, values in expected.items():
            assert_stats(row.get(metric), values, case + '/' + metric)


def reconcile_csv(summary_dir, aggregate_rows):
    expected = {
        trial['log']: trial
        for group in aggregate_rows.values()
        for trial in group['trials']
    }
    path = summary_dir / 'all_trials.csv'
    with path.open(newline='', encoding='utf-8') as handle:
        rows = [row for row in csv.DictReader(handle) if row.get('phase') == 'comparison']
    require(len(rows) == 30, 'CSV must contain 30 comparison rows')
    require(len({row.get('log') for row in rows}) == 30, 'CSV comparison logs are not unique')
    for row in rows:
        trial = expected.get(row.get('log'))
        require(trial is not None, 'unexpected CSV log: ' + str(row.get('log')))
        require(row.get('case') == trial['case'], row['log'] + ': CSV case mismatch')
        require(row.get('method') == trial['method'], row['log'] + ': CSV method mismatch')
        require(row.get('log_sha256') == trial['log_sha256'], row['log'] + ': CSV hash mismatch')
        require(row.get('complete') == 'True', row['log'] + ': CSV complete mismatch')
        require(row.get('integrity_ok') == 'True', row['log'] + ': CSV integrity mismatch')
        require(row.get('eligible') == 'True', row['log'] + ': CSV eligible mismatch')
        for field in ('schedules', 'first_error', 'buggy_schedules',
                      'error_event_count', 'inner_timeouts'):
            require(optional_int(row[field]) == trial[field],
                    row['log'] + ': CSV ' + field + ' mismatch')
        require(close(float(row['elapsed_seconds']), trial['elapsed_seconds']),
                row['log'] + ': CSV elapsed_seconds mismatch')
        require(not row.get('parse_problems'), row['log'] + ': CSV parse problem')
        require(not row.get('issues'), row['log'] + ': CSV issue')


def formatted(values):
    if not values['n']:
        return 'NA (n=0)'
    sample_sd = 'NA' if values['sample_sd'] is None else '%.4f' % values['sample_sd']
    return '%.4f ± %s (n=%d)' % (values['mean'], sample_sd, values['n'])


def table_cells(line):
    if not line.startswith('|'):
        return []
    return [cell.strip() for cell in line.strip().strip('|').split('|')]


def reconcile_summary_markdown(summary_dir, aggregate_rows, paired):
    lines = (summary_dir / 'SUMMARY.md').read_text(encoding='utf-8').splitlines()
    method_rows = {}
    pair_rows = {}
    for line in lines:
        cells = table_cells(line)
        if len(cells) == 7 and cells[0] in CASES and cells[1] in METHODS:
            method_rows[(cells[0], cells[1])] = cells
        elif len(cells) == 5 and cells[0] in CASES:
            pair_rows[cells[0]] = cells
    require(len(method_rows) == 10, 'SUMMARY.md must contain ten method rows')
    require(len(pair_rows) == 5, 'SUMMARY.md must contain five paired rows')
    for key, expected in aggregate_rows.items():
        cells = method_rows.get(key)
        require(cells is not None, '/'.join(key) + ': missing Markdown row')
        require(cells[2] == '3 / 3', '/'.join(key) + ': Markdown denominator mismatch')
        for column, metric in enumerate(
            ('first_error', 'schedules', 'buggy_schedules', 'elapsed_seconds'),
            start=3,
        ):
            value = expected['stats'][metric]
            text = formatted(value)
            require(cells[column] == text,
                    '/'.join(key) + ': Markdown ' + metric + ' mismatch')
    for case, expected in paired.items():
        cells = pair_rows.get(case)
        require(cells is not None, case + ': missing Markdown paired row')
        require(cells[1] == '3', case + ': Markdown paired n mismatch')
        for column, metric in enumerate(
            ('schedule_reduction_pct', 'serial_minus_period_seconds',
             'serial_over_period_time_ratio'),
            start=2,
        ):
            value = expected[metric]
            text = formatted(value)
            require(cells[column] == text, case + ': Markdown paired ' + metric + ' mismatch')


def audit(batch=DEFAULT_BATCH, summary_dir=DEFAULT_SUMMARY):
    batch = Path(batch)
    summary_dir = Path(summary_dir)
    trials = collect_trials(batch)
    aggregate_rows = aggregate(trials)
    paired = paired_rows(aggregate_rows)
    summary = json.loads((summary_dir / 'summary.json').read_text(encoding='utf-8'))
    reconcile_summary_json(summary, aggregate_rows, paired)
    reconcile_csv(summary_dir, aggregate_rows)
    reconcile_summary_markdown(summary_dir, aggregate_rows, paired)
    return {
        'status': 'passed',
        'comparison_trials': len(trials),
        'method_groups': len(aggregate_rows),
        'paired_case_rows': len(paired),
        'csv_comparison_rows': 30,
        'summary_method_rows': 10,
        'summary_paired_rows': 5,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, default=DEFAULT_BATCH)
    parser.add_argument('--summary', type=Path, default=DEFAULT_SUMMARY)
    args = parser.parse_args()
    print(json.dumps(audit(args.batch, args.summary), indent=2))


if __name__ == '__main__':
    try:
        main()
    except (KeyError, OSError, UnicodeError, ValueError) as error:
        sys.exit('FAIL: ' + str(error))
