#!/usr/bin/env python3
"""Publish the verified final snapshot once, preserving any existing release."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from check_final_submission import check, checked_path, require
from package_final_submission import package

REPOSITORY = 'Sasuke-666/CS340-Research-Paper-Replication'
TITLE = 'CS340 PERIOD final submission'


def gh_json(repository, endpoint, missing=False):
    """Only an actual HTTP 404 can represent an absent Git reference."""
    result = subprocess.run(['gh', 'api', '--method', 'GET', '--include',
                             'repos/' + repository + '/' + endpoint],
                            capture_output=True, text=True)
    headers, separator, body = result.stdout.partition('\n\n')
    status = re.match(r'HTTP/\S+\s+(\d{3})\b', headers)
    require(separator and status, 'Unrecognized GitHub response; publication stopped')
    code = int(status[1])
    if missing and code == 404:
        return None
    require(result.returncode == 0 and code == 200,
            'GitHub read failed with HTTP {}; publication stopped'.format(code))
    return json.loads(body)


def remote_release(repository, tag):
    """The authenticated release list also exposes unfinished drafts."""
    page, matches = 1, []
    while True:
        rows = gh_json(repository, 'releases?per_page=100&page=' + str(page))
        require(isinstance(rows, list), 'Invalid release listing')
        matches.extend(row for row in rows if row.get('tag_name') == tag)
        if len(rows) < 100:
            break
        page += 1
    require(len(matches) <= 1, 'Multiple releases use the final tag; no release was changed')
    return matches[0] if matches else None


def remote_tag_commit(repository, tag):
    ref = gh_json(repository, 'git/ref/tags/' + tag, missing=True)
    if ref is None:
        return None
    require(ref.get('ref') == 'refs/tags/' + tag, 'Unexpected tag reference')
    obj, seen = ref['object'], set()
    while obj.get('type') == 'tag':
        sha = obj.get('sha')
        require(isinstance(sha, str) and re.fullmatch(r'[0-9a-f]{40}', sha)
                and sha not in seen and len(seen) < 16, 'Invalid annotated-tag chain')
        seen.add(sha)
        obj = gh_json(repository, 'git/tags/' + sha)['object']
    require(obj.get('type') == 'commit' and
            re.fullmatch(r'[0-9a-f]{40}', obj.get('sha', '')), 'The final tag is not a commit')
    return obj['sha']


def verify_release(release, tag_commit, target, assets, tag):
    require(release is not None and release.get('tag_name') == tag,
            'The final release is missing')
    require(release.get('draft') is False and release.get('prerelease') is False
            and release.get('published_at'),
            'Existing ' + tag + ' is unpublished or a prerelease; it was left unchanged')
    require(tag_commit == target, 'Existing ' + tag + ' points to a different or missing commit')
    remote = release.get('assets', [])
    require(len(remote) == len(assets) and {row.get('name') for row in remote} == set(assets),
            'Existing release assets are incomplete or unexpected; they were left unchanged')
    digest_verified = 0
    for row in remote:
        expected = assets[row['name']]
        require(row.get('state') == 'uploaded' and row.get('size') == expected['size_bytes'],
                'Release asset state or size differs: ' + row['name'])
        if row.get('digest') is not None:
            require(row['digest'] == 'sha256:' + expected['sha256'],
                    'Release asset digest differs: ' + row['name'])
            digest_verified += 1
    return digest_verified


def publish(root, bundle, repository, target):
    root, bundle = Path(root).resolve(), Path(bundle).resolve()
    require(repository == REPOSITORY, 'Unexpected release repository')
    require(isinstance(target, str) and re.fullmatch(r'[0-9a-f]{40}', target),
            'Use the exact 40-character workflow commit')
    head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    require(head == target, 'The checkout differs from the requested release commit')
    receipt = check(root)
    tag = receipt['tag']
    require(receipt['git_commit_verified'], 'Publication requires verified Git ancestry and sources')
    manifest = json.loads((root / 'submission/FINAL_RELEASE.json').read_text(encoding='utf-8'))
    expected_name = 'CS340_Final_Deliverables_' + receipt['report_revision'].replace('-', '') + '.zip'
    require(bundle.name == expected_name and bundle.is_file(), 'Missing or incorrectly named delivery bundle')
    # Independently rebuild before any remote mutation, catching stale or altered ZIPs.
    with tempfile.TemporaryDirectory(prefix='release-verify-') as temp:
        rebuilt = package(root, Path(temp) / expected_name)
        require(bundle.stat().st_size == rebuilt['size_bytes'] and
                hashlib.sha256(bundle.read_bytes()).hexdigest() == rebuilt['sha256'],
                'Delivery bundle differs from the clean, checked-out final snapshot')
    paths = [checked_path(root, row['path']) for row in manifest['artifacts']] + [bundle]
    assets = {path.name: {'size_bytes': path.stat().st_size,
                         'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for path in paths}
    require(len(assets) == 7, 'The final release requires exactly seven distinct assets')
    notes = checked_path(root, 'submission/RELEASE_NOTES.md')
    existing = remote_release(repository, tag)
    tag_commit = remote_tag_commit(repository, tag)
    require(tag_commit in (None, target),
            'Existing ' + tag + ' points to a different commit; it was left unchanged')
    state = 'already_published'
    if existing is None:
        command = ['gh', 'release', 'create', tag, '--repo', repository,
                   '--target', target, '--title', TITLE + ' ' + tag,
                   '--notes-file', str(notes)]
        command.extend(str(path) for path in paths)
        created = subprocess.run(command, capture_output=True, text=True)
        require(created.returncode == 0,
                'Release creation failed; any draft or uploaded assets were left unchanged. '
                + created.stderr.strip())
        existing = remote_release(repository, tag)
        tag_commit = remote_tag_commit(repository, tag)
        state = 'published'
    digest_verified = verify_release(existing, tag_commit, target, assets, tag)
    return {'status': state, 'tag': tag, 'commit': target, 'verified_assets': len(assets),
            'assets_with_verified_remote_digest': digest_verified,
            'url': 'https://github.com/' + repository + '/releases/tag/' + tag}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--repository', default=os.environ.get('GITHUB_REPOSITORY'))
    parser.add_argument('--target', default=os.environ.get('GITHUB_SHA'))
    args = parser.parse_args()
    print(json.dumps(publish(args.root, args.bundle, args.repository, args.target), indent=2))
