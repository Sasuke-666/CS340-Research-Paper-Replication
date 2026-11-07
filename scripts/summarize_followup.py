#!/usr/bin/env python3
"""Summarize every declared extension condition and targeted replay."""
import csv
import json
from pathlib import Path
import statistics
from verify_period_evidence import verify

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / 'results/2026-11-07'


def main():
    verify(ROOT)
    records = json.loads((BATCH / 'followup/followup.json').read_text())
    rows = []
    for depth in (1, 2, 3):
        attempts = [r for r in records if r.get('phase') == 'extension' and r['depth'] == depth]
        valid = [r for r in attempts if r['exit_code'] == 0 and not r['timed_out'] and r['end_marker']]
        for metric in ('observed_schedule_count', 'reported_buggy_schedules', 'first_error_schedule', 'elapsed_seconds'):
            values = [r[metric] for r in valid if r[metric] is not None]
            rows.append({'depth': depth, 'metric': metric, 'attempted': len(attempts),
                         'complete': len(valid), 'measured_n': len(values),
                         'mean': statistics.mean(values) if values else None,
                         'sample_sd': statistics.stdev(values) if len(values) > 1 else None})
    with (BATCH / 'extension_summary.csv').open('w', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    replays = {}
    for case in ('reorder_3_bad', 'reorder_4_bad', 'df'):
        runs = [r for r in records if r.get('phase') == 'replay' and r['case'] == case]
        replays[case] = {'trials': len(runs),
                        'expected_signature_observed': sum(r['expected_error_observed'] for r in runs),
                        'outer_timeouts': sum(r['timed_out'] for r in runs)}
    (BATCH / 'replay_summary.json').write_text(json.dumps(replays, indent=2) + '\n')
    print(json.dumps({'extension': rows, 'replays': replays}, indent=2))


if __name__ == '__main__':
    main()
