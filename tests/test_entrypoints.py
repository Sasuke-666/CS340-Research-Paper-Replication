"""Exercise maintained entrypoints with dry runs and isolated synthetic bytes.

Network and container boundaries are stopped before any real experiment starts.
These fixtures never enter the archived scientific results.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]


def run_step(workflow, name):
    """Read one named run block from the repository's maintained YAML style."""
    text = (ROOT / '.github/workflows' / workflow).read_text(encoding='utf-8')
    anchor = '      - name: ' + name + '\n'
    if text.count(anchor) != 1:
        raise AssertionError('Missing or duplicated workflow step: ' + name)
    block = text.split(anchor, 1)[1].split('\n      - ', 1)[0]
    match = re.search(r'(?m)^        run: (.*)$', block)
    if match is None:
        raise AssertionError('Workflow step has no run command: ' + name)
    if match[1] != '|':
        return match[1] + '\n'
    return textwrap.dedent(block[match.end():].lstrip('\n'))


class MakeEntrypointTests(unittest.TestCase):
    def commands(self, targets, override=None):
        env = dict(os.environ)
        for key in ('CASE', 'MAKEFLAGS', 'MFLAGS'):
            env.pop(key, None)
        command = ['make', '--no-print-directory', '-n'] + list(targets)
        command.append('EVIDENCE_DIR=results/entrypoint-dry-run')
        if override is not None:
            command.append('CASE=' + override)
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True,
                                text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = [shlex.split(line) for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual(len(rows), len(targets))
        return {Path(row[1]).name: row[2] for row in rows}

    def test_target_defaults_do_not_leak_between_targets(self):
        for targets in (('comparison', 'layout'), ('layout', 'comparison')):
            with self.subTest(order=targets):
                self.assertEqual(self.commands(targets), {
                    'period_container_compatible.sh': 'reorder_3',
                    'period_container_layout.sh': 'account',
                })

    def test_command_line_case_overrides_both_defaults(self):
        for targets in (('comparison', 'layout'), ('layout', 'comparison')):
            with self.subTest(order=targets):
                self.assertEqual(self.commands(targets, 'lazy01'), {
                    'period_container_compatible.sh': 'lazy01',
                    'period_container_layout.sh': 'lazy01',
                })


class WorkflowEntrypointTests(unittest.TestCase):
    def test_pilot_workflow_reaches_clone_and_keeps_output_protection(self):
        script = run_step('period-pilot.yml', 'Run bounded pilot')
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            bin_dir = temp / 'bin'
            bin_dir.mkdir()
            # Stop at the first external operation. An existing output must fail
            # earlier, while a fresh workflow attempt must reach this boundary.
            stubs = {
                'git': '#!/bin/sh\nprintf reached > "$RUNNER_TEMP/clone-reached"\nexit 73\n',
                'docker': '#!/bin/sh\nexit 99\n',
                'uname': '#!/bin/sh\nprintf "x86_64\\n"\n',
            }
            for name, content in stubs.items():
                path = bin_dir / name
                path.write_text(content)
                path.chmod(0o755)
            env = dict(os.environ, RUNNER_TEMP=str(temp),
                       PATH=str(bin_dir) + os.pathsep + os.environ['PATH'])
            env.pop('PERIOD_DRIVER', None)
            env.pop('PERIOD_IMAGE', None)
            first = subprocess.run(['bash', '-euo', 'pipefail', '-c', script],
                                   cwd=ROOT, env=env, capture_output=True, text=True, timeout=10)
            self.assertEqual(first.returncode, 73, first.stdout + first.stderr)
            self.assertTrue((temp / 'clone-reached').is_file())
            out = temp / 'period-evidence'
            self.assertTrue(out.is_dir())

            sentinel = out / 'retained.txt'
            sentinel.write_bytes(b'previous attempt must remain unchanged\n')
            (temp / 'clone-reached').unlink()
            second = subprocess.run(['bash', '-euo', 'pipefail', '-c', script],
                                    cwd=ROOT, env=env, capture_output=True, text=True, timeout=10)
            self.assertEqual(second.returncode, 2, second.stdout + second.stderr)
            self.assertFalse((temp / 'clone-reached').exists())
            self.assertEqual(sentinel.read_bytes(), b'previous attempt must remain unchanged\n')
            self.assertEqual(sorted(p.name for p in out.iterdir()), ['retained.txt'])

    def test_current_archive_downloads_only_the_current_run(self):
        text = (ROOT / '.github/workflows/period-abi16.yml').read_text(encoding='utf-8')
        steps = re.split(r'(?m)^      - ', text)
        downloads = [step for step in steps if 'uses: actions/download-artifact@' in step]
        self.assertTrue(downloads)
        for step in downloads:
            requested_run = re.search(r'(?m)^          run-id:\s*(.+)$', step)
            self.assertTrue(requested_run is None or requested_run[1] == '${{ github.run_id }}',
                            'Archiving a new run must not request another run')
            pattern = re.search(r'(?m)^          pattern:\s*(.+)$', step)
            self.assertIsNotNone(pattern)
            self.assertIn('${{ github.run_id }}', pattern[1])

    def test_current_archive_preserves_bytes_without_a_historical_download(self):
        shell = run_step('period-abi16.yml', 'Archive exact bytes')
        match = re.search(r"(?ms)^python(?:3)? - <<'PY'\n(.*?)^PY$", shell)
        self.assertIsNotNone(match)
        program = match[1]
        for history_present in (False, True):
            with self.subTest(history_present=history_present), tempfile.TemporaryDirectory() as directory:
                temp = Path(directory)
                workspace = temp / 'workspace'
                workspace.mkdir()
                run = '90000000001'
                protocol = 'a' * 40
                payload = b'synthetic archive fixture\r\nexact bytes\n'
                artifact = temp / 'downloaded/current' / ('period-deep-account-' + run)
                artifact.mkdir(parents=True)
                (artifact / 'raw.txt').write_bytes(payload)
                (artifact / 'records.json').write_text('[{"phase": "fixture"}]\n')
                historical = workspace / 'results/2026-11-07/comparison-42380166815'
                if history_present:
                    historical.mkdir(parents=True)
                    (historical / 'retained.txt').write_bytes(b'original failure bytes\n')
                env = dict(os.environ, RUNNER_TEMP=str(temp), BATCH_RUN=run, PROTOCOL_SHA=protocol)
                command = [sys.executable, '-c', program]
                result = subprocess.run(command, cwd=workspace, env=env, capture_output=True,
                                        text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                destination = workspace / 'results/2026-11-07' / ('comparison-' + run)
                self.assertEqual((destination / 'account/raw.txt').read_bytes(), payload)
                manifest_bytes = (destination / 'archive_manifest.json').read_bytes()
                manifest = json.loads(manifest_bytes)
                self.assertEqual(manifest['run_id'], run)
                self.assertEqual(manifest['protocol_commit'], protocol)
                self.assertEqual(manifest['command_records'], {'account': 1})
                entry = next(item for item in manifest['files'] if item['path'] == 'account/raw.txt')
                self.assertEqual(entry['bytes'], len(payload))
                self.assertEqual(entry['sha256'], hashlib.sha256(payload).hexdigest())
                if history_present:
                    self.assertEqual((historical / 'retained.txt').read_bytes(), b'original failure bytes\n')
                    self.assertEqual(sorted(p.name for p in historical.iterdir()), ['retained.txt'])
                else:
                    self.assertFalse(historical.exists())

                # Reusing the same run ID must retain the first archived bytes.
                (artifact / 'raw.txt').write_bytes(b'changed retry bytes\n')
                repeated = subprocess.run(command, cwd=workspace, env=env, capture_output=True,
                                          text=True, timeout=10)
                self.assertNotEqual(repeated.returncode, 0)
                self.assertIn('Refuse evidence overwrite', repeated.stderr)
                self.assertEqual((destination / 'account/raw.txt').read_bytes(), payload)
                self.assertEqual((destination / 'archive_manifest.json').read_bytes(), manifest_bytes)


if __name__ == '__main__':
    unittest.main()
