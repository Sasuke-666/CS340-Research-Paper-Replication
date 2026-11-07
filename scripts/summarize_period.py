#!/usr/bin/env python3
"""Summarize verified pilot logs. Missing/censored runs never become zeros."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import statistics

REFERENCE = {
    'smoke_double_free': {'first_error_schedule': 3, 'observed_schedule_count': 6, 'reported_buggy_schedules': 4},
    'CS.reorder_3_bad': {'first_error_schedule': 6, 'observed_schedule_count': 27, 'reported_buggy_schedules': 6},
    'CS.reorder_4_bad': {'first_error_schedule': 9, 'observed_schedule_count': 100, 'reported_buggy_schedules': 12},
}


def summarize(records, directory):
    rows = []
    for case, expected in REFERENCE.items():
        all_runs = [r for r in records if r.get('phase') == 'run' and r.get('case') == case]
        accepted = []
        for record in all_runs:
            name = record.get('log', '')
            if not name or Path(name).name != name:
                raise ValueError('A run log must be a simple relative filename')
            path = directory / name
            if not path.is_file():
                raise ValueError('Missing raw log: ' + name)
            if hashlib.sha256(path.read_bytes()).hexdigest() != record.get('log_sha256'):
                raise ValueError('Raw log checksum mismatch: ' + name)
            if (record.get('status') == 'complete' and record.get('exit_code') == 0
                    and not record.get('timed_out') and record.get('end_marker')
                    and record.get('observed_schedule_count', 0) > 0):
                accepted.append(record)
        for metric, reference in list(expected.items()) + [('elapsed_seconds', None)]:
            values = [r[metric] for r in accepted if isinstance(r.get(metric), (int, float))]
            mean = statistics.mean(values) if values else None
            sd = statistics.stdev(values) if len(values) >= 2 else None
            delta = mean - reference if mean is not None and reference is not None else None
            rows.append({'case': case, 'metric': metric, 'paper_reference': reference,
                         'attempted_runs': len(all_runs), 'complete_runs': len(accepted),
                         'measured_n': len(values), 'mean': mean, 'sample_sd': sd,
                         'absolute_difference': delta,
                         'relative_difference_percent': delta / reference * 100 if delta is not None and reference else None,
                         'comparison_status': 'pilot_observation_requires_witness_review' if len(values) >= 3 else 'insufficient_complete_runs'})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('evidence', type=Path)
    args = parser.parse_args()
    records = json.loads((args.evidence / 'runs.json').read_text())
    rows = summarize(records, args.evidence)
    with (args.evidence / 'summary.csv').open('w', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (args.evidence / 'summary.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
