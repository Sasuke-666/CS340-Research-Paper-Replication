#!/usr/bin/env python3
"""Verify archived bytes, parsed measurements, and replay signatures."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from run_period_pilot import read_metrics


def verify(root):
    root = root.resolve()
    batch = root / 'results/2026-11-07'
    manifest = json.loads((batch / 'manifest.json').read_text())
    for record in manifest['files']:
        path = (root / record['path']).resolve()
        if root not in path.parents or not path.is_file():
            raise ValueError('Invalid or missing manifest file')
        data = path.read_bytes()
        if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
            raise ValueError('Manifest mismatch: ' + record['path'])
    checked = 0
    replay_hits = {}
    schedule_lists = {}
    for folder, filename in [('pilot', 'runs.json'), ('followup', 'followup.json')]:
        directory = batch / folder
        records = json.loads((directory / filename).read_text())
        for record in records:
            name = record['log']
            if Path(name).name != name:
                raise ValueError('Log path must be a filename')
            path = directory / name
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != record['log_sha256']:
                raise ValueError('Log checksum mismatch: ' + name)
            checked += 1
            phase = record['phase']
            text = re.sub(r'\x1b\[[0-9;]*m', '', raw.decode('utf-8', errors='replace'))
            if phase in ('run', 'extension'):
                metrics = read_metrics(path)
                for key, value in metrics.items():
                    if record.get(key) != value:
                        raise ValueError('Parsed metric mismatch: ' + name + ':' + key)
                total = re.search(r'Total Error Interleavings:\s*(\d+)', text)
                if total and int(total.group(1)) != metrics['reported_buggy_schedules']:
                    raise ValueError('Error total disagrees with event count: ' + name)
                schedule_lists.setdefault(folder + ':' + record['case'], []).append(
                    re.findall(r'(?m)^test\s+\d+:\s*(.+)$', text))
            elif phase == 'replay':
                expected = ('AddressSanitizer: attempting double-free' in text) if record['case'] == 'df' else ('Assertion' in text and 'failed' in text)
                if expected != record['expected_error_observed']:
                    raise ValueError('Replay signature mismatch: ' + name)
                replay_hits.setdefault(record['case'], []).append(expected)
    result = {'verified_manifest_files': len(manifest['files']), 'verified_command_logs': checked,
              'replay_expected_signatures': {k: {'hits': sum(v), 'trials': len(v)} for k, v in replay_hits.items()},
              'pilot_schedule_lists_identical': {k: all(x == v[0] for x in v) for k, v in schedule_lists.items() if k.startswith('pilot:')}}
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    verify(parser.parse_args().root)
