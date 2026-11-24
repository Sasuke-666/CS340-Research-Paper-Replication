#!/usr/bin/env python3
"""Generate or verify the evidence manifest for this member's audit chain."""

import argparse
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / 'docs/validation/evidence/1240001156-evidence-chain-20261124'
DEFAULT_MANIFEST = EVIDENCE_DIR / 'manifest.json'
DEFAULT_PATHS = (
    'scripts/audit_1240001156_acceptance_metrics.py',
    'scripts/audit_1240001156_validation_evidence.py',
    'tests/test_1240001156_parser_contract.py',
    'tests/test_1240001156_acceptance_metrics.py',
    'tests/test_1240001156_validation_evidence.py',
    'docs/validation/1240001156-evidence-chain-20261124.md',
    'docs/validation/evidence/1240001156-evidence-chain-20261124/parser-contract-tests.log',
    'docs/validation/evidence/1240001156-evidence-chain-20261124/acceptance-metrics-audit.log',
    'docs/validation/evidence/1240001156-evidence-chain-20261124/acceptance-metrics-tests.log',
    'docs/validation/evidence/1240001156-evidence-chain-20261124/validation-evidence-tests.log',
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe_relative(path):
    candidate = Path(path)
    return (
        bool(path)
        and not candidate.is_absolute()
        and not PurePosixPath(path).is_absolute()
        and not PureWindowsPath(path).is_absolute()
        and '..' not in candidate.parts
        and path == candidate.as_posix()
    )


def entry_for(root, relative):
    require(safe_relative(relative), 'unsafe evidence path: ' + str(relative))
    path = root / relative
    require(not path.is_symlink(), 'symlink is not accepted: ' + relative)
    require(path.is_file(), 'evidence file is missing: ' + relative)
    data = path.read_bytes()
    return {
        'path': relative,
        'bytes': len(data),
        'sha256': hashlib.sha256(data).hexdigest(),
    }


def build_manifest(root=ROOT, paths=DEFAULT_PATHS):
    root = Path(root)
    return {
        'schema_version': 1,
        'scope': 'Independent parser, acceptance-metrics and evidence-provenance audit',
        'files': [entry_for(root, path) for path in paths],
    }


def verify_manifest_data(manifest, root=ROOT, expected_paths=DEFAULT_PATHS):
    root = Path(root)
    require(manifest.get('schema_version') == 1, 'manifest schema version mismatch')
    files = manifest.get('files')
    require(isinstance(files, list), 'manifest files must be a list')
    paths = []
    for item in files:
        require(isinstance(item, dict), 'manifest entry must be an object')
        relative = item.get('path')
        require(isinstance(relative, str) and safe_relative(relative),
                'unsafe manifest path: ' + str(relative))
        paths.append(relative)
        actual = entry_for(root, relative)
        require(item.get('bytes') == actual['bytes'],
                'byte-count mismatch: ' + relative)
        require(item.get('sha256') == actual['sha256'],
                'SHA-256 mismatch: ' + relative)
    require(len(paths) == len(set(paths)), 'duplicate manifest path')
    require(set(paths) == set(expected_paths), 'manifest path set is stale or incomplete')
    return {'files': len(paths), 'bytes': sum(item['bytes'] for item in files)}


def load_manifest(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_manifest(path=DEFAULT_MANIFEST, root=ROOT, paths=DEFAULT_PATHS):
    path = Path(path)
    manifest = build_manifest(root, paths)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return manifest


def verify_manifest(path=DEFAULT_MANIFEST, root=ROOT, expected_paths=DEFAULT_PATHS):
    return verify_manifest_data(load_manifest(path), root, expected_paths)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=DEFAULT_MANIFEST)
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--write', action='store_true')
    action.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.write:
        write_manifest(args.manifest)
        print('WROTE: ' + str(args.manifest.relative_to(ROOT)))
    result = verify_manifest(args.manifest)
    print('PASS: verified %(files)d evidence files, %(bytes)d bytes' % result)


if __name__ == '__main__':
    try:
        main()
    except (KeyError, OSError, UnicodeError, ValueError) as error:
        sys.exit('FAIL: ' + str(error))
