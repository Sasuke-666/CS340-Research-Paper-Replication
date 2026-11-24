#!/usr/bin/env python3
"""Bundle the checked documents and tracked repository without Git metadata."""
import argparse
from datetime import date
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import zipfile

from check_final_submission import check, checked_path, is_git_root, require


def package(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    require(root not in output.parents and output != root,
            'Keep the delivery archive outside the repository and its inputs')
    require(is_git_root(root), 'Packaging requires a Git checkout')
    dirty = subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain',
                                     '--untracked-files=no'])
    require(not dirty, 'Packaging requires a clean tracked working tree and index')
    receipt = check(root)
    manifest = json.loads((root / 'submission/FINAL_RELEASE.json').read_text(encoding='utf-8'))
    commit = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    paths = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z']).decode().split('\0')
    tracked = {name for name in paths if name}
    required = {'submission/FINAL_RELEASE.json'} | {
        row['path'] for row in manifest['sources'] + manifest['artifacts']}
    require(required <= tracked, 'The manifest, sources and final documents must all be tracked')
    revision = date.fromisoformat(receipt['report_revision'])
    timestamp = (revision.year, revision.month, revision.day, 0, 0, 0)
    output.parent.mkdir(parents=True, exist_ok=True)

    def add(bundle, name, content):
        entry = zipfile.ZipInfo(name, timestamp)
        entry.compress_type = zipfile.ZIP_DEFLATED
        entry.external_attr = 0o100644 << 16
        bundle.writestr(entry, content)

    # Assemble off to the side; a failed build must not truncate an existing bundle.
    with tempfile.TemporaryDirectory(prefix='final-package-', dir=output.parent) as temp:
        temporary = Path(temp) / 'delivery.zip'
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
            for row in manifest['artifacts']:
                path = checked_path(root, row['path'])
                add(bundle, path.name, path.read_bytes())
            for name in sorted(tracked):
                path = checked_path(root, name)
                add(bundle, 'Repository/' + name, path.read_bytes())
            delivery = dict(receipt, repository_commit=commit,
                            repository_url='https://github.com/Sasuke-666/CS340-Research-Paper-Replication',
                            documents=manifest['artifacts'],
                            scope='Final documents and tracked source/evidence. Course-platform submission and oral presentation are separate actions.')
            add(bundle, 'DELIVERY.json', (json.dumps(delivery, ensure_ascii=False, indent=2) + '\n').encode())
            add(bundle, 'START_HERE.txt', (
                'CS340 PERIOD final submission, ' + revision.isoformat() + '\n\n'
                'Submit the English Final_Report PDF through the confirmed course portal.\n'
                'The editable Word report and PowerPoint remain available for revision.\n'
                'The Chinese handbook contains the submission and presentation actions.\n'
                'Repository/ contains the complete tracked source and archived evidence,\n'
                'including all failed/censored/unknown outcomes in their original scopes.\n'
                'Read Repository/README.md for offline audits and Linux/Docker execution.\n'
                'In an extracted bundle, document/source hashes are checked locally;\n'
                'Git ancestry requires the checkout at the repository commit below.\n'
                'Repository commit: ' + commit + '\n'
                'Release: https://github.com/Sasuke-666/CS340-Research-Paper-Replication/releases/tag/' + receipt['tag'] + '\n'
            ).encode())
        require(not subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain',
                                             '--untracked-files=no']),
                'Tracked files changed while building the delivery archive')
        os.replace(temporary, output)
    return {'path': str(output), 'size_bytes': output.stat().st_size,
            'sha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'commit': commit}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(package(Path(__file__).resolve().parents[1], args.output), indent=2))
