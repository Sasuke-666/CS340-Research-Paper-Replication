"""Recount only the six twostage comparison logs in the November 22 batch."""

import hashlib
import json
import re
import sys
from pathlib import Path
from statistics import mean, stdev


BATCH = 'acceptance-45015126850-attempt1'
DAY = Path(__file__).resolve().parents[1] / 'results' / '2026-11-22'
CASE = DAY / BATCH / 'twostage'
SUMMARY = DAY / 'summaries' / BATCH / 'SUMMARY.md'
METHODS = ('period', 'author_serialized_abi16')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def recount(path, record):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == record['log_sha256'], f'{path.name}: SHA-256 mismatch')
    log = re.sub(r'\x1b\[[0-9;]*m', '', raw.decode('utf-8')).splitlines()
    for marker in ('Start Testing!', 'End Testing!'):
        require(log.count(marker) == 1, f'{path.name}: expected exactly one {marker}')
    start, end = log.index('Start Testing!'), log.index('End Testing!')
    require(start < end, f'{path.name}: invalid testing marker order')
    ids, events = [], []
    for line in log[start + 1:end]:
        test = re.match(r'^test (\d+):', line)
        if test:
            ids.append(int(test[1]))
        if '[Error Found]' in line:
            require(ids and re.fullmatch(r'\s*\[Error Found\]: NO\.\d+ assertion failed\s*', line),
                    f'{path.name}: unexpected or unassigned error marker')
            events.append(ids[-1])

    require(ids == list(range(1, len(ids) + 1)) and events,
            f'{path.name}: missing, duplicated or unordered test IDs, or no assertion event')
    failures = sorted(set(events))
    footer = '\n'.join(log[end + 1:])
    for marker in (rf'^Round[ \t]+\d+[ \t]+{len(ids)}$',
                   rf'^Total Error Interleavings: {len(events)}$',
                   r'^Total Timeouts Interleavings: 0$',
                   r'^Runner exit_code=0 timed_out=False elapsed_seconds=\d+(?:\.\d+)?\s*\Z'):
        require(re.search(marker, footer, re.MULTILINE), f'{path.name}: invalid or missing footer {marker!r}')
    budget = [int(line.split(':')[1]) for line in log[:start] if line.startswith('runs_limit:')]
    require(budget == [10000] and len(ids) < budget[0], f'{path.name}: unexpected or exhausted schedule budget')

    metrics = dict(schedules=len(ids), first_error=failures[0], buggy_schedules=len(failures))
    checks = dict(metrics, error_event_count=len(events), status='complete', complete_markers=True,
                  exit_code=0, timed_out=False, inner_timeouts=0, budget_reached=False, timeout_seconds=240)
    for field, value in checks.items():
        require(record[field] == value, f'{path.name}: records.json {field}={record[field]!r}, expected {value!r}')
    print(f'{path.name}: {len(ids)} schedules; first={failures[0]}; failing={len(failures)} {failures}; complete')
    return metrics


def main():
    records = [r for r in json.loads((CASE / 'records.json').read_text(encoding='utf-8')) if r['phase'] == 'comparison']
    expected = {f'{method}_r{rep:02}.txt' for method in METHODS for rep in range(1, 4)}
    require(len(records) == 6 and {r['log'] for r in records} == expected, 'Unexpected comparison log set')
    by_log = {r['log']: r for r in records}
    summary = SUMMARY.read_text(encoding='utf-8').splitlines()
    for method in METHODS:
        trials = []
        for rep in range(1, 4):
            name = f'{method}_r{rep:02}.txt'
            record = by_log[name]
            require((record['case'], record['method'], record['repeat']) == ('twostage', method, rep),
                    f'{name}: incorrect metadata')
            trials.append(recount(CASE / name, record))
        rows = [line.strip('|').split('|') for line in summary if line.startswith(f'| twostage | {method} |')]
        require(len(rows) == 1, f'{method}: missing or duplicate method in SUMMARY.md')
        cells = [cell.strip() for cell in rows[0]]
        require(len(cells) == 7 and cells[2] == '3 / 3', f'{method}: invalid comparison denominator in SUMMARY.md')
        for column, field in enumerate(('first_error', 'schedules', 'buggy_schedules'), start=3):
            values = [trial[field] for trial in trials]
            calculated = f'{mean(values):.4f} ± {stdev(values):.4f} (n={len(values)})'
            require(calculated == cells[column], f'{method} {field}: {calculated} differs from {cells[column]}')
            print(f'  {field}: {calculated.replace("±", "+/-")}')
    print('PASS: six raw logs and six mean/sample-SD cells agree with the archived records and summary.')


if __name__ == '__main__':
    try:
        main()
    except (KeyError, OSError, ValueError) as error:
        sys.exit(f'FAIL: {error}')
