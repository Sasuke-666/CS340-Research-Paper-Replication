#!/usr/bin/env python3
"""Verify the frozen final documents against their source and byte manifest."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import zipfile

from report_config import report_identity


def require(condition, message):
    if not condition:
        raise ValueError(message)


def checked_release_tag(value):
    """Accept the original submission and positive, bounded patch revisions."""
    require(isinstance(value, str) and
            re.fullmatch(r'v1\.0(?:\.[1-9][0-9]{0,5})?', value) is not None,
            'Unsupported final release tag')
    return value


def publication_candidate(root, expected_commit):
    """Only a ready manifest changed by this exact commit can enter publication."""
    root = Path(root).resolve()
    head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'],
                                   text=True).strip()
    require(head == expected_commit, 'Checkout differs from the workflow commit')
    name = 'submission/FINAL_RELEASE.json'
    if not (root / name).is_file():
        return False
    history = subprocess.check_output(
        ['git', '-C', str(root), 'rev-list', '--parents', '-n', '1', 'HEAD'],
        text=True).split()
    command = (['diff', '--name-only', '--no-renames', history[1], 'HEAD', '--', name]
               if len(history) > 1 else ['ls-tree', '--name-only', 'HEAD', '--', name])
    changed = subprocess.check_output(['git', '-C', str(root), *command], text=True)
    if name not in changed.splitlines():
        return False
    data = json.loads((root / name).read_text(encoding='utf-8'))
    require(data.get('schema_version') == 1, 'Unsupported final manifest schema')
    checked_release_tag(data.get('tag'))
    require(data.get('status') in ('preparing', 'ready'), 'Invalid final manifest status')
    return data['status'] == 'ready'


def checked_path(root, name):
    require(isinstance(name, str), 'Manifest paths must be strings')
    relative = PurePosixPath(name)
    require(not relative.is_absolute() and relative.parts and
            '..' not in relative.parts and '.git' not in relative.parts and
            '\\' not in name and relative.as_posix() == name,
            'Invalid manifest path: ' + name)
    path = root.joinpath(*relative.parts)
    require(root in path.resolve().parents and path.is_file(),
            'Missing or outside file: ' + name)
    require(not any(p.is_symlink() for p in (path, *path.parents) if p != root),
            'Symbolic links are not accepted: ' + name)
    return path


def is_git_root(root):
    """An extracted bundle may be inside another repository without its own Git data."""
    try:
        result = subprocess.run(['git', '-C', str(root), 'rev-parse', '--show-toplevel'],
                                capture_output=True, text=True)
    except FileNotFoundError:
        return False
    return result.returncode == 0 and Path(result.stdout.strip()).resolve() == root


def check(root, manifest=None, check_commit=True):
    root = Path(root).resolve()
    manifest = manifest or root / 'submission/FINAL_RELEASE.json'
    data = json.loads(Path(manifest).read_text(encoding='utf-8'))
    require(data.get('schema_version') == 1 and data.get('status') == 'ready',
            'Final release is not ready')
    tag = checked_release_tag(data.get('tag'))
    revision, label, _ = report_identity(root)
    require(label == 'Final report' and data.get('report_revision') == revision.isoformat(),
            'Final report revision differs from the release')
    commit = data.get('source_commit', '')
    require(re.fullmatch(r'[0-9a-f]{40}', commit) is not None, 'Invalid source commit')
    git_commit_verified = check_commit and is_git_root(root)
    if git_commit_verified:
        subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor', commit, 'HEAD'],
                       check=True, capture_output=True)
    day = revision.strftime('%Y%m%d')
    expected = {
        'submission/CS340_PERIOD_Final_Report_' + day + suffix
        for suffix in ('.pdf', '.docx')
    } | {
        'submission/CS340_PERIOD_Final_Presentation_' + day + suffix
        for suffix in ('.pptx', '.pdf')
    } | {
        'submission/CS340_Final_Submission_Handbook_' + day + suffix
        for suffix in ('.docx', '.pdf')
    }
    artifacts = data.get('artifacts', [])
    require(len(artifacts) == len(expected) and {r.get('path') for r in artifacts} == expected,
            'The release must contain exactly the six named final documents')
    source_rows = data.get('sources', [])
    required_sources = {'report/EXPANDED_REPORT.md', 'report/AI_STATEMENT.md',
                        'report/REVISION_DATE', 'presentation/SLIDES.md',
                        'presentation/TALK_OUTLINE.md', 'docs/CONTRIBUTIONS.csv',
                        'docs/MEMBER_ACTIONS_ZH.md', 'docs/FINAL_SUBMISSION_CHECKLIST.md',
                        'submission/RELEASE_NOTES.md'}
    require(required_sources <= {r.get('path') for r in source_rows},
            'A required document source is missing from the manifest')
    seen = set()
    for row in source_rows + artifacts:
        name = row['path']
        require(name not in seen, 'Duplicate manifest path: ' + name)
        seen.add(name)
        path = checked_path(root, name)
        content = path.read_bytes()
        require(0 < len(content) <= 50_000_000, 'Empty or oversized file: ' + name)
        require(len(content) == row['size_bytes'] and
                hashlib.sha256(content).hexdigest() == row['sha256'],
                'Content or size differs: ' + name)
        if git_commit_verified and row in source_rows:
            committed = subprocess.check_output(
                ['git', '-C', str(root), 'show', commit + ':' + name])
            require(committed == content, 'Source differs from source_commit: ' + name)
        if row in artifacts:
            if path.suffix == '.pdf':
                require(content.startswith(b'%PDF-'), 'Invalid PDF: ' + name)
            else:
                with zipfile.ZipFile(path) as package:
                    require(package.testzip() is None, 'Damaged Office package: ' + name)
                    main = 'word/document.xml' if path.suffix == '.docx' else 'ppt/presentation.xml'
                    require(main in package.namelist(), 'Invalid Office document: ' + name)
    return {'tag': tag, 'report_revision': data['report_revision'],
            'source_commit': commit, 'verified_documents': len(artifacts),
            'verified_sources': len(source_rows), 'git_commit_verified': git_commit_verified,
            'status': 'passed'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(check(args.root), indent=2))
