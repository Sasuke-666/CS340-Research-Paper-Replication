#!/usr/bin/env python3
"""Check ordinary tracked/staged files against course storage rules.

This is a conservative local safeguard, not an exhaustive secret scanner.
"""
from __future__ import annotations
import argparse
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

MAX_BYTES = 50_000_000  # Conservative interpretation of the course's 50 MB limit.
BANNED_SUFFIXES = {'.o', '.obj', '.a', '.so', '.dylib', '.dll', '.exe', '.iso',
                   '.img', '.qcow', '.qcow2', '.vdi', '.vmdk', '.vhd', '.vhdx',
                   '.pem', '.key', '.p12', '.pfx', '.pyc', '.pyo'}
BANNED_DIRS = {'build', 'dist', 'CMakeFiles', '__pycache__', '.venv', 'venv',
               'large-traces'}
SECRET_PATTERNS = (
    re.compile(rb'-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----'),
    re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b'),
    re.compile(rb'\bAKIA[A-Z0-9]{16}\b'),
)


def validate_identity(student_id: str, full_name: str) -> None:
    """Validate a supplied identity's shape, not university enrollment."""
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{4,31}', student_id):
        raise ValueError('Supply your real student ID (5–32 letters/digits/_/-).')
    folded = student_id.lower()
    if (any(x in folded for x in ('student', 'your', 'todo', 'example', 'placeholder'))
            or len(set(folded)) == 1 or student_id == '1234567890'):
        raise ValueError('A placeholder is not a real student ID.')
    if student_id == '2250025281':
        raise ValueError('2250025281 is the TA ID in the course document, not the owner ID.')
    if (len(full_name.strip()) < 2 or full_name != full_name.strip()
            or any(c in full_name for c in '\r\n<>\x00')
            or full_name.lower() in {'full name', 'your name', 'todo', 'student', 'unknown'}):
        raise ValueError('Supply your actual full name.')


def path_errors(path: str, size: int, data: bytes) -> list[str]:
    p = PurePosixPath(path)
    errors = []
    if size > MAX_BYTES:
        errors.append('larger than 50,000,000 bytes')
    if (p.suffix.lower() in BANNED_SUFFIXES
            or re.search(r'\.so(?:\.\d+)+$', p.name, re.IGNORECASE)
            or any(x in BANNED_DIRS for x in p.parts)
            or any(x.startswith('cmake-build-') for x in p.parts[:-1])):
        errors.append('prohibited build output / image / credential or local-environment path')
    if (p.name in {'a.out', 'core', 'CMakeCache.txt', 'credentials.json', 'secrets.json'}
            or re.fullmatch(r'core\.\d+', p.name)):
        errors.append('prohibited generated or credential file')
    if (p.name == '.env' or p.name.startswith('.env.')) and p.name != '.env.example':
        errors.append('environment credential/configuration file')
    if any(pattern.search(data) for pattern in SECRET_PATTERNS):
        errors.append('possible credential detected; value intentionally not printed')
    return errors


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(['git', '-C', str(root), *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=check)


def check(root: Path, staged: bool = False) -> list[str]:
    errors = []
    probe = git(root, 'rev-parse', '--show-toplevel', check=False)
    in_this_repo = (probe.returncode == 0 and
                    Path(probe.stdout.decode().strip()).resolve() == root.resolve())
    if staged and not in_this_repo:
        return ['Staged checking requires the repository root.']
    if in_this_repo:
        # T includes regular-file <-> symlink changes; omitting it bypasses checks.
        args = ('diff', '--cached', '--name-only', '--diff-filter=ACMRT', '-z') if staged else ('ls-files', '-z')
        names = git(root, *args).stdout.decode('utf-8', 'surrogateescape').split('\0')
        names = [n for n in names if n]
    else:
        names = [p.relative_to(root).as_posix() for p in root.rglob('*')
                 if (p.is_file() or p.is_symlink()) and '.git' not in p.relative_to(root).parts]
    for name in names:
        path = root / name
        if staged:
            mode = git(root, 'ls-files', '-s', '--', name).stdout.decode().split(' ', 1)[0]
            if mode == '120000':
                errors.append(f'{name}: symlink requires explicit review; not accepted by this check')
                continue
            size = int(git(root, 'cat-file', '-s', ':' + name).stdout)
            data = git(root, 'show', ':' + name).stdout if size <= MAX_BYTES else b''
        else:
            if path.is_symlink():
                errors.append(f'{name}: symlink requires explicit review; not accepted by this check')
                continue
            if not path.is_file():
                errors.append(f'{name}: tracked path is missing from the working tree')
                continue
            size = path.stat().st_size
            data = path.read_bytes() if size <= MAX_BYTES else b''
        for problem in path_errors(name, size, data):
            errors.append(f'{name}: {problem}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staged', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        errors = check(root, args.staged)
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        print(f'CHECK ERROR: {exc}', file=sys.stderr)
        return 2
    if errors:
        for err in errors:
            print('FAIL:', err, file=sys.stderr)
        return 1
    print('PASS: checked repository file rules. No experiment result has been verified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
