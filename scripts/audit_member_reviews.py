#!/usr/bin/env python3
"""Strict offline integration checks for PR #3 and PR #4; no workload execution."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ANSI = re.compile(r'\x1b\[[0-9;]*m')
SIGNATURE = re.compile(r'twostage_bad\.c:48:.*funcB.*Assertion .0. failed')
ACCOUNT_BATCHES = (
    'results/2026-11-07/comparison-42381922637/account',
    'results/member-reruns/1240001156-account-20261108T122201Z',
)
SEQUENCES = {
    'period': (65, 'c4ceaea3afb045a0d16e410386ed38cbc4aeff4a70a9e19cd809fb45bca07c0e'),
    'author_serialized_abi16': (136, '06b7fb843aad805c9b1233d77213406968d06334b6e5813d388ae91f9c2b1953'),
}
REPLAY_DIR = 'results/member-reruns/1240000576-twostage-43681034375'


def sequence_digest(raw, expected_count):
    """Strip ANSI, retain ordered full test lines, join with LF and no final LF."""
    text = ANSI.sub('', raw.decode('utf-8'))
    lines = [line.strip() for line in text.splitlines()
             if re.match(r'^test\s+\d+', line)]
    ids = [int(re.match(r'^test\s+(\d+)', line)[1]) for line in lines]
    if ids != list(range(1, expected_count + 1)):
        raise ValueError('Missing, repeated or reordered schedule IDs')
    return hashlib.sha256('\n'.join(lines).encode('utf-8')).hexdigest()


def audit_account(root):
    checked = 0
    for batch in ACCOUNT_BATCHES:
        folder = root / batch
        manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
        entries = {entry['path']: entry for entry in manifest['files']}
        for method, (count, expected) in SEQUENCES.items():
            for repetition in range(1, 11):
                name = f'{method}_r{repetition:02}.txt'
                raw = (folder / name).read_bytes()
                entry = entries[name]
                if len(raw) != entry['bytes'] or hashlib.sha256(raw).hexdigest() != entry['sha256']:
                    raise ValueError(f'Archive digest mismatch: {batch}/{name}')
                if sequence_digest(raw, count) != expected:
                    raise ValueError(f'Request-sequence mismatch: {batch}/{name}')
                checked += 1
    return checked


def matching_assertion(raw, exit_code):
    text = ANSI.sub('', raw.decode('utf-8'))
    _, marker, target = text.partition('Perform Reproduction!')
    return bool(exit_code == 0 and marker and 'Bug found!' in target and SIGNATURE.search(target))


def audit_replays(folder):
    required = {'container.txt', 'host.txt'} | {
        f'replay-{n}.{suffix}' for n in range(1, 6) for suffix in ('txt', 'exit')}
    entries = {}
    for line in (folder / 'SHA256SUMS').read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        if not match or match[2] not in required or match[2] in entries:
            raise ValueError('Invalid or duplicate replay checksum entry')
        entries[match[2]] = match[1]
    if set(entries) != required:
        raise ValueError('Incomplete replay checksum coverage')
    for name, expected in entries.items():
        path = folder / name
        if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Replay digest mismatch: {name}')
    hits = 0
    for n in range(1, 6):
        raw = (folder / f'replay-{n}.txt').read_bytes()
        rc = int((folder / f'replay-{n}.exit').read_text(encoding='utf-8'))
        if not matching_assertion(raw, rc):
            raise ValueError(f'Replay {n} does not contain the required post-reproduction assertion')
        hits += 1
    return len(entries), hits


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        logs = audit_account(root)
        files, hits = audit_replays(root / REPLAY_DIR)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    print(f'PASS: {logs} archived account logs match the two declared request sequences; '
          f'{files} replay files match their checksums; {hits}/5 post-reproduction assertions.')
    print('Offline evidence verification only; no new measurements or personal explanation certified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
