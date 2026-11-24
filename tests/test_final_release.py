"""Exercise release decisions against real Git snapshots and a local API boundary."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest
from unittest.mock import patch

import test_final_submission as fixtures

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import publish_final_release as release
from package_final_submission import package


class ReleaseService:
    """Model remote state; unexpected mutations fail the test immediately."""
    def __init__(self):
        self.release = None
        self.tag = None
        self.calls = []
        self.creations = []
        self.fail_upload = False
        self.read_status = 200
        self.native_run = subprocess.run

    def run(self, command, *args, **kwargs):
        if command[0] != 'gh':
            return self.native_run(command, *args, **kwargs)
        self.calls.append(command)
        if command[1] == 'api':
            endpoint = command[-1].split(release.REPOSITORY + '/', 1)[1]
            status = self.read_status
            if endpoint.startswith('releases?'):
                body = [self.release] if self.release else []
            elif endpoint == 'git/ref/tags/v1.0':
                if self.tag is None:
                    status, body = 404, {'message': 'Not Found'}
                else:
                    body = {'ref': 'refs/tags/v1.0', 'object': {'type': 'commit', 'sha': self.tag}}
            else:
                raise AssertionError('Unexpected API read: ' + endpoint)
            return subprocess.CompletedProcess(command, 0 if status == 200 else 1,
                'HTTP/2.0 {} Fixture\nContent-Type: application/json\n\n{}'.format(status, json.dumps(body)), '')
        if command[1:4] != ['release', 'create', 'v1.0']:
            raise AssertionError('Unexpected remote mutation: ' + repr(command))
        self.creations.append(command)
        target = command[command.index('--target') + 1]
        notes_index = command.index('--notes-file') + 1
        paths = [Path(name) for name in command[notes_index + 1:]]
        assets = [{'name': path.name, 'size': path.stat().st_size, 'state': 'uploaded',
                   'digest': 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()} for path in paths]
        self.release = {'tag_name': 'v1.0', 'draft': self.fail_upload, 'prerelease': False,
                        'name': command[command.index('--title') + 1],
                        'body': Path(command[notes_index]).read_text(),
                        'published_at': None if self.fail_upload else '2026-11-24T12:00:00Z',
                        'assets': assets[:2] if self.fail_upload else assets}
        self.tag = None if self.fail_upload else target
        return subprocess.CompletedProcess(command, 1 if self.fail_upload else 0, '',
                                           'Fixture upload failure' if self.fail_upload else '')


class FinalReleaseTests(unittest.TestCase):
    def setUp(self):
        fixture = fixtures.FinalSubmissionTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.root, self.data = fixture.root, fixture.data
        self.git = fixtures.commit_fixture(self.root, self.data)
        self.target = self.git('rev-parse', 'HEAD')
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.temp = Path(temporary.name)
        self.bundle = self.temp / 'CS340_Final_Deliverables_20261124.zip'
        package(self.root, self.bundle)
        self.service = ReleaseService()

    def publish(self):
        with patch.object(subprocess, 'run', self.service.run):
            return release.publish(self.root, self.bundle, release.REPOSITORY, self.target)

    def test_create_exact_target_and_seven_assets_then_repeat_without_mutation(self):
        created = self.publish()
        self.assertEqual(created['status'], 'published')
        self.assertEqual(created['assets_with_verified_remote_digest'], 7)
        command = self.service.creations[0]
        self.assertEqual(command[command.index('--target') + 1], self.target)
        self.assertEqual(self.service.release['name'], 'CS340 PERIOD final submission v1.0')
        self.assertEqual(self.service.release['body'], (self.root / 'submission/RELEASE_NOTES.md').read_text())
        self.assertEqual({row['name'] for row in self.service.release['assets']},
                         {Path(row['path']).name for row in self.data['artifacts']} | {self.bundle.name})
        self.assertEqual(self.publish()['status'], 'already_published')
        self.assertEqual(len(self.service.creations), 1)
        # Older API responses can lack digests; report that limit explicitly.
        for asset in self.service.release['assets']:
            asset.pop('digest')
        self.assertEqual(self.publish()['assets_with_verified_remote_digest'], 0)
        self.assertEqual(len(self.service.creations), 1)

    def test_conflicting_incomplete_or_altered_remote_state_is_preserved(self):
        self.publish()
        complete = copy.deepcopy(self.service.release)
        for case in ('different_tag', 'draft', 'missing_asset', 'wrong_size', 'wrong_digest'):
            with self.subTest(case=case):
                self.service.release = copy.deepcopy(complete)
                self.service.tag = self.target
                if case == 'different_tag':
                    self.service.tag = 'b' * 40
                elif case == 'draft':
                    self.service.release.update(draft=True, published_at=None)
                elif case == 'missing_asset':
                    self.service.release['assets'].pop()
                elif case == 'wrong_size':
                    self.service.release['assets'][0]['size'] += 1
                else:
                    self.service.release['assets'][0]['digest'] = 'sha256:' + '0' * 64
                before = copy.deepcopy(self.service.release)
                with self.assertRaises(ValueError):
                    self.publish()
                self.assertEqual(self.service.release, before)
                self.assertEqual(len(self.service.creations), 1)

    def test_failed_upload_preserves_draft_and_rerun_does_not_complete_it(self):
        self.service.fail_upload = True
        with self.assertRaisesRegex(ValueError, 'Release creation failed'):
            self.publish()
        self.assertTrue(self.service.release['draft'])
        self.assertEqual(len(self.service.release['assets']), 2)
        before = copy.deepcopy(self.service.release)
        with self.assertRaisesRegex(ValueError, 'unpublished'):
            self.publish()
        self.assertEqual(self.service.release, before)
        self.assertEqual(len(self.service.creations), 1)

    def test_failed_reads_and_invalid_local_inputs_never_publish(self):
        for status in (401, 500):
            with self.subTest(http_status=status):
                self.service.read_status = status
                with self.assertRaisesRegex(ValueError, 'GitHub read failed'):
                    self.publish()
                self.assertFalse(self.service.creations)
        self.service.read_status = 200
        self.service.calls.clear()
        original = self.bundle.read_bytes()
        self.bundle.write_bytes(original + b'changed')
        with self.assertRaisesRegex(ValueError, 'bundle differs'):
            self.publish()
        self.bundle.write_bytes(original)
        self.target = 'c' * 40
        with self.assertRaisesRegex(ValueError, 'checkout differs'):
            self.publish()
        self.assertFalse(self.service.calls)

    def test_workflow_detects_only_the_current_commit_manifest_change(self):
        workflow = (ROOT / '.github/workflows/repository-checks.yml').read_text()
        step = workflow.split('      - name: Detect a final-manifest change in this commit\n', 1)[1]
        block = textwrap.dedent(step.split('        run: |\n', 1)[1].split('      - name:', 1)[0])

        def ready():
            output = self.temp / 'step-output'
            output.write_text('')
            environment = dict(os.environ, GITHUB_SHA=self.git('rev-parse', 'HEAD'),
                               GITHUB_OUTPUT=str(output))
            subprocess.run([sys.executable, '-c', block], cwd=self.root, env=environment,
                           check=True, capture_output=True, text=True)
            return output.read_text().strip()

        self.assertEqual(ready(), 'ready=true')
        (self.root / 'unrelated.txt').write_text('Later unrelated change\n')
        self.git('add', 'unrelated.txt')
        self.git('commit', '--quiet', '-m', 'An unrelated later change')
        self.assertEqual(ready(), 'ready=false')
        self.git('checkout', '--quiet', self.data['source_commit'])
        self.assertFalse((self.root / 'submission/FINAL_RELEASE.json').exists())
        self.assertEqual(ready(), 'ready=false')


if __name__ == '__main__':
    unittest.main()
