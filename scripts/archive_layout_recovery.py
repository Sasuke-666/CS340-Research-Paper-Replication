#!/usr/bin/env python3
"""Archive a conditionally activated replacement batch without changing raw bytes.

This helper runs on the hosted runner outside the measurement container. It
never receives or reads a publication token. ZIP preservation is independent
of whether the Git publication step succeeded.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import zipfile

ORIGINAL_RUN = '43570556202'
ORIGINAL_JOB = '132373799340'
ORIGINAL_PROTOCOL = 'bddb831319679c30586d9bbe689fb11b897f1a14'
RUNNER_FILES = ('period_container_layout.sh', 'run_period_layout.py',
                'run_period_comparison.py', 'run_period_pilot.py')


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_activation(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    if data.get('enabled') is not True:
        raise ValueError('Recovery is inactive; do not run measurements')
    expected = {'original_run_id': ORIGINAL_RUN, 'original_job_id': ORIGINAL_JOB,
                'original_protocol_commit': ORIGINAL_PROTOCOL,
                'original_artifact_name': 'period-layout-account-' + ORIGINAL_RUN,
                'original_job_final_status': 'completed', 'artifact_readable': False}
    for key, value in expected.items():
        if data.get(key) != value:
            raise ValueError('Recovery activation requirement is unmet: ' + key)
    if data.get('original_job_final_conclusion') not in ('failure', 'cancelled', 'timed_out', 'action_required', 'neutral'):
        raise ValueError('Original unsuccessful final outcome must be recorded')
    for key in ('original_job_completed_at', 'artifact_check_utc'):
        value = data.get(key)
        if not isinstance(value, str):
            raise ValueError('Observed timestamp is required: ' + key)
        datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
    completed = datetime.datetime.fromisoformat(data['original_job_completed_at'].replace('Z', '+00:00'))
    checked = datetime.datetime.fromisoformat(data['artifact_check_utc'].replace('Z', '+00:00'))
    if completed.tzinfo is None or checked.tzinfo is None or checked < completed:
        raise ValueError('Artifact check must follow completed original job, with timezone')
    if not data.get('preserved_original_metadata_path'):
        raise ValueError('Preserve original final metadata before activation')
    return data


def ordinary_files(root, max_bytes=None):
    if not root.is_dir() or root.is_symlink():
        raise ValueError('A real source directory is required')
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError('Evidence symlink rejected: ' + str(path.relative_to(root)))
        if path.is_file():
            if '.git' in path.relative_to(root).parts:
                raise ValueError('Repository metadata must not enter evidence')
            if max_bytes is not None and path.stat().st_size > max_bytes:
                raise ValueError('Evidence exceeds course per-file size limit: ' + path.name)
            yield path


def prepare(root, activation, work):
    data = validate_activation(activation)
    if work.exists():
        raise ValueError('Refuse to reuse recovery preparation directory')
    runner = work / 'pinned-runner' / 'scripts'
    registration = work / 'registration'
    runner.mkdir(parents=True)
    registration.mkdir()
    # Keep the reviewed collector bytes available even if publication rebases
    # onto a remote commit that changes repository scripts.
    shutil.copyfile(Path(__file__).resolve(), registration / 'archive_helper.py')
    shutil.copyfile(activation, registration / 'ACCOUNT_RECOVERY_ACTIVATION.json')
    protocol = root / 'experiments/2026-11-14/ACCOUNT_RECOVERY_PROTOCOL.md'
    shutil.copyfile(protocol, registration / 'ACCOUNT_RECOVERY_PROTOCOL.md')
    for key in ('preserved_original_metadata_path', 'preserved_original_log_path'):
        relative = data.get(key)
        if not relative:
            continue
        source = (root / relative).resolve()
        if root.resolve() not in source.parents or not source.is_file():
            raise ValueError('Original evidence reference must identify a retained repository file')
        shutil.copyfile(source, registration / ('original_' + key + source.suffix))
    hashes = {}
    for name in RUNNER_FILES:
        raw = subprocess.check_output(['git', '-C', str(root), 'show', ORIGINAL_PROTOCOL + ':scripts/' + name])
        destination = runner / name
        destination.write_bytes(raw)
        saved = registration / 'runner_sources' / name
        saved.parent.mkdir(exist_ok=True)
        saved.write_bytes(raw)
        hashes[name] = hashlib.sha256(raw).hexdigest()
    write_json(registration / 'recovery_metadata.json', {
        'original_run_id': ORIGINAL_RUN, 'original_job_id': ORIGINAL_JOB,
        'original_protocol_commit': ORIGINAL_PROTOCOL,
        'recovery_run_id': os.environ['GITHUB_RUN_ID'],
        'recovery_registration_commit': os.environ['GITHUB_SHA'],
        'reason': 'Evidence-transfer recovery only; full fixed account sample on a new host',
        'case': 'account', 'planned_repetitions_per_condition': 10,
        'outer_timeout_seconds': 120, 'depth': 3, 'schedule_budget': 10000,
        'measurement_source_sha256': hashes,
        'archive_helper_sha256': sha256(registration / 'archive_helper.py'),
        'outcomes_used_for_activation': False,
        'activation_record': data})


def archive(work, destination):
    if destination.exists() or destination.is_symlink():
        raise ValueError('Refuse to overwrite an evidence batch')
    destination.mkdir(parents=True)
    source = work / 'evidence'
    registration = work / 'registration'
    # Missing workload output is retained as a setup failure, not fabricated trials.
    if source.is_dir():
        for path in ordinary_files(source, 50_000_000):
            target = destination / 'account' / path.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
    else:
        write_json(destination / 'measurement_output_missing.json', {
            'state': 'No raw measurement directory was produced',
            'original_run_id': ORIGINAL_RUN, 'recovery_run_id': os.environ['GITHUB_RUN_ID']})
    for path in ordinary_files(registration, 50_000_000):
        target = destination / 'registration' / path.relative_to(registration)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    record_path = destination / 'account' / 'records.json'
    count = None
    record_error = None
    if record_path.exists():
        try:
            rows = json.loads(record_path.read_text(encoding='utf-8'))
            if not isinstance(rows, list):
                raise ValueError('Command records are not a JSON list')
            count = len(rows)
        except (UnicodeError, ValueError) as error:
            # An interrupted writer may leave invalid JSON. Preserve those exact
            # bytes through Git; a convenience count must not block the archive.
            record_error = {'type': type(error).__name__, 'message': str(error)}
    entries = [{'path': path.relative_to(destination).as_posix(), 'bytes': path.stat().st_size,
                'sha256': sha256(path)} for path in ordinary_files(destination, 50_000_000)]
    write_json(destination / 'archive_manifest.json', {
        'run_id': os.environ['GITHUB_RUN_ID'], 'protocol_commit': os.environ['GITHUB_SHA'],
        'original_run_id': ORIGINAL_RUN, 'original_protocol_commit': ORIGINAL_PROTOCOL,
        'note': 'Separate account recovery batch; original raw files copied without modification; inspect all actual outcomes',
        'command_records': {'account': count},
        'command_record_parse_errors': {'account': record_error}, 'files': entries})
    print(json.dumps({'archive': str(destination), 'files': len(entries), 'command_records': {'account': count}}))


def make_zip(work, output):
    if output.exists() or output.is_symlink():
        raise ValueError('Refuse to overwrite recovery ZIP')
    output.parent.mkdir(parents=True, exist_ok=True)
    entries = []
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zipped:
        for name in ('evidence', 'registration'):
            source = work / name
            if source.is_dir():
                for path in ordinary_files(source):
                    prefix = 'account' if name == 'evidence' else 'registration'
                    archive_name = (Path(prefix) / path.relative_to(source)).as_posix()
                    zipped.write(path, archive_name)
                    entries.append({'path': archive_name, 'bytes': path.stat().st_size,
                                    'sha256': sha256(path)})
        zipped.writestr('backup_manifest.json', json.dumps({
            'original_run_id': ORIGINAL_RUN, 'recovery_run_id': os.environ['GITHUB_RUN_ID'],
            'measurement_output_directory_exists': (work / 'evidence').is_dir(),
            'scope': 'Independent backup of original raw files plus recovery registration metadata',
            'files': entries}, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'zip': output.name, 'bytes': output.stat().st_size, 'sha256': sha256(output)}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'archive', 'zip'))
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--activation', type=Path)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--destination', type=Path)
    parser.add_argument('--zip-output', type=Path)
    args = parser.parse_args()
    if args.action == 'prepare':
        if not args.activation:
            parser.error('--activation is required')
        prepare(args.root.resolve(), args.activation, args.work)
    elif args.action == 'archive':
        if not args.destination:
            parser.error('--destination is required')
        archive(args.work, args.destination)
    else:
        if not args.zip_output:
            parser.error('--zip-output is required')
        make_zip(args.work, args.zip_output)


if __name__ == '__main__':
    main()
