#!/usr/bin/env python3
"""Independent raw-log recount for the fixed 7 November study (standard library).

This deliberately does not import the experiment parser or summary helpers.
Synthetic tests are separate from the archived experimental observations.
"""
import argparse
import csv
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import re
import statistics

BATCH = Path('results/2026-11-07')
PAPER = {'CS.reorder_3_bad': (6, 27, 6), 'CS.reorder_4_bad': (9, 100, 12)}
METRICS = ('first_error_schedule', 'observed_schedule_count', 'reported_buggy_schedules')


def recount(text):
    text = re.sub(r'\x1b\[[0-9;]*m', '', text)
    blocks = re.split(r'(?m)^test\s+(\d+):', text)
    numbers = [int(blocks[i]) for i in range(1, len(blocks), 2)]
    if not numbers or numbers != list(range(1, len(numbers) + 1)):
        raise ValueError('Missing, duplicate or non-contiguous schedule numbers')
    failures = [int(blocks[i]) for i in range(1, len(blocks), 2)
                if '[Error Found]:' in blocks[i + 1]]
    events = text.count('[Error Found]:')
    totals = re.findall(r'(?m)^Total Error Interleavings:\s*(\d+)\s*$', text)
    if events != len(failures) or len(totals) != 1 or int(totals[0]) != len(failures):
        raise ValueError('Failure events, distinct failing schedules and final total disagree')
    if text.count('End Testing!') != 1:
        raise ValueError('Exploration did not reach exactly one end marker')
    return {'first_error_schedule': failures[0] if failures else None,
            'observed_schedule_count': len(numbers),
            'reported_buggy_schedules': len(failures)}


def stats(values):
    present = [v for v in values if v is not None]
    if any(isinstance(v, bool) or not math.isfinite(v) for v in present):
        raise ValueError('Invalid numeric observation')
    return {'measured_n': len(present), 'missing_n': len(values) - len(present),
            'mean': statistics.mean(present) if present else None,
            'sample_sd': statistics.stdev(present) if len(present) > 1 else None}


def audit(root):
    root = Path(root).resolve(); batch = root / BATCH
    manifest = json.loads((batch / 'manifest.json').read_text())
    paths = [r['path'] for r in manifest['files']]
    if len(paths) != 126 or len(set(paths)) != len(paths):
        raise ValueError('The fixed raw archive must contain 126 unique files')
    for item in manifest['files']:
        p = (root / item['path']).resolve()
        if root not in p.parents or not p.is_file():
            raise ValueError('Invalid archive path')
        raw = p.read_bytes()
        if len(raw) != item['bytes'] or hashlib.sha256(raw).hexdigest() != item['sha256']:
            raise ValueError('Raw archive mismatch: ' + item['path'])
    groups = defaultdict(list); replay = defaultdict(list); observed = Counter(); logs = set()
    command_count = 0
    for folder, index in [('pilot', 'runs.json'), ('followup', 'followup.json')]:
        records = json.loads((batch / folder / index).read_text())
        for r in records:
            name = r['log']; identity = (folder, name)
            if Path(name).name != name or identity in logs:
                raise ValueError('Invalid or duplicate command log')
            logs.add(identity); raw = (batch / folder / name).read_bytes(); command_count += 1
            if hashlib.sha256(raw).hexdigest() != r['log_sha256']:
                raise ValueError('Command log checksum mismatch: ' + name)
            if r['exit_code'] != 0 or r['timed_out']:
                raise ValueError('Non-complete command in the fixed archived study: ' + name)
            phase = r['phase']; observed[(folder, phase)] += 1
            if phase in ('run', 'extension'):
                fresh = recount(raw.decode('utf-8', errors='replace'))
                if any(r[k] != fresh[k] for k in METRICS):
                    raise ValueError('Independent recount mismatch: ' + name)
                groups[(folder, r['case'], r['depth'])].append(dict(fresh, repeat=r['repeat'], elapsed_seconds=r['elapsed_seconds']))
            elif phase == 'replay':
                text = raw.decode('utf-8', errors='replace')
                expected = ('AddressSanitizer: attempting double-free' in text if r['case'] == 'df'
                            else bool(re.search(r'Assertion[^\n]*failed', text)))
                if expected != r['expected_error_observed']:
                    raise ValueError('Replay signature mismatch: ' + name)
                replay[r['case']].append((r['repeat'], expected))
    required = {('pilot', 'build'): 3, ('pilot', 'run'): 9, ('followup', 'build'): 3,
                ('followup', 'deadline_probe'): 1, ('followup', 'extension'): 9, ('followup', 'replay'): 15}
    if observed != Counter(required):
        raise ValueError('A planned phase is missing, duplicated or unexpected')
    expected_groups = {('pilot', c, 3) for c in ('smoke_double_free', *PAPER)}
    expected_groups |= {('followup', 'reorder_3_bad', d) for d in (1, 2, 3)}
    if set(groups) != expected_groups or set(replay) != {'reorder_3_bad', 'reorder_4_bad', 'df'}:
        raise ValueError('Case/condition coverage differs from the fixed protocol')
    summaries = []
    for (folder, case, depth), records in sorted(groups.items()):
        if sorted(r['repeat'] for r in records) != [1, 2, 3]:
            raise ValueError('Expected exactly repetitions 1, 2 and 3')
        for metric in (*METRICS, 'elapsed_seconds'):
            row = dict(batch=folder, case=case, depth=depth, metric=metric,
                       **stats([r[metric] for r in records]))
            if folder == 'pilot' and case in PAPER and metric in METRICS:
                reference = PAPER[case][METRICS.index(metric)]
                row.update(paper_reference=reference, absolute_delta=row['mean'] - reference,
                           relative_delta_percent=(row['mean'] / reference - 1) * 100)
            summaries.append(row)
    replay_counts = {}
    for case, trials in sorted(replay.items()):
        if sorted(x[0] for x in trials) != [1, 2, 3, 4, 5]:
            raise ValueError('Expected exactly five distinct replay repetitions')
        replay_counts[case] = {'trials': 5, 'signature_hits': sum(x[1] for x in trials)}
    # Compare independently recomputed pilot means/SDs with the published JSON.
    with (batch / 'pilot/summary.csv').open(newline='') as handle:
        published = list(csv.DictReader(handle))
    for row in (x for x in summaries if x['batch'] == 'pilot'):
        matches = [x for x in published if x['case'] == row['case'] and x['metric'] == row['metric']]
        if len(matches) != 1:
            raise ValueError('Published summary row missing or duplicated')
        for key in ('mean', 'sample_sd', 'measured_n'):
            a, b = matches[0][key], row[key]
            a = float(a) if a != '' else None
            if (a is None or b is None) and a != b:
                raise ValueError('Published missingness differs')
            if a is not None and not math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12):
                raise ValueError('Published statistic differs: ' + row['case'] + ':' + key)
    with (batch / 'extension_summary.csv').open(newline='') as handle:
        published_extension = list(csv.DictReader(handle))
    for row in (x for x in summaries if x['batch'] == 'followup'):
        matches = [x for x in published_extension if int(x['depth']) == row['depth'] and x['metric'] == row['metric']]
        if len(matches) != 1:
            raise ValueError('Extension summary row missing or duplicated')
        for key in ('mean', 'sample_sd', 'measured_n'):
            a = float(matches[0][key]) if matches[0][key] != '' else None
            b = row[key]
            if (a is None or b is None) and a != b:
                raise ValueError('Extension missingness differs')
            if a is not None and not math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12):
                raise ValueError('Extension statistic differs')
    published_replays = json.loads((batch / 'replay_summary.json').read_text())
    for case, counts in replay_counts.items():
        if (published_replays[case]['trials'] != counts['trials'] or
                published_replays[case]['expected_signature_observed'] != counts['signature_hits']):
            raise ValueError('Replay summary differs')
    return {'scope': 'Independent re-count of the archived 2026-11-07 study; no new experiments',
            'raw_files': len(paths), 'command_logs': command_count, 'test_and_replay_invocations': 33,
            'phase_counts': {a + '/' + b: n for (a, b), n in sorted(observed.items())},
            'replays': replay_counts, 'summaries': summaries}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--output', type=Path)
    args = p.parse_args(); result = audit(args.root)
    text = json.dumps(result, indent=2, allow_nan=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(text)
    print(text)


if __name__ == '__main__':
    main()
