"""Repository safeguards only; these tests do not run PERIOD experiments.

All credentials and identities below are synthetic test inputs. Credential
samples are assembled at runtime so the suite itself remains safe to commit.
"""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / 'scripts' / 'check_repository.py'
SPEC = importlib.util.spec_from_file_location('check_repository', SCRIPT)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def fake_token(prefix='ghp_', length=20):
    return prefix.encode() + b'A' * length


class PathRulesTests(unittest.TestCase):
    def test_size_boundary_uses_decimal_megabytes(self):
        for size in (0, 49_999_999, 50_000_000):
            with self.subTest(size=size):
                self.assertEqual(checker.path_errors('results/run.log', size, b''), [])
        self.assertIn('larger than 50,000,000 bytes',
                      checker.path_errors('results/run.log', 50_000_001, b''))

    def test_small_research_inputs_and_outputs_are_allowed(self):
        for name in ('src/main.c', 'results/run.log', 'results/data.csv',
                     'results/chart.png', 'report/report.pdf', '.env.example',
                     'docs/building.md', 'core.py', 'src/core.c', 'lib/software.txt'):
            with self.subTest(name=name):
                self.assertEqual(checker.path_errors(name, 4, b'safe'), [])

    def test_prohibited_suffixes_include_case_variants(self):
        for suffix in ('.o', '.obj', '.a', '.so', '.dylib', '.dll', '.exe',
                       '.iso', '.img', '.qcow', '.qcow2', '.vdi', '.vmdk',
                       '.vhd', '.vhdx', '.pem', '.key', '.p12', '.pfx', '.pyc', '.pyo'):
            for variant in (suffix, suffix.upper()):
                with self.subTest(suffix=variant):
                    self.assertTrue(checker.path_errors('nested/file' + variant, 0, b''))

    def test_prohibited_directories_at_any_depth(self):
        for directory in ('build', 'dist', 'CMakeFiles', '__pycache__',
                          '.venv', 'venv', 'large-traces'):
            with self.subTest(directory=directory):
                self.assertTrue(checker.path_errors('nested/' + directory + '/x.txt', 0, b''))

    def test_generated_filenames_and_environment_files(self):
        for name in ('a.out', 'core', 'credentials.json', 'secrets.json',
                     '.env', '.env.local', '.env.production', '.env.example.local'):
            with self.subTest(name=name):
                self.assertTrue(checker.path_errors('nested/' + name, 0, b''))

    def test_generated_paths_already_excluded_by_gitignore(self):
        for name in ('lib/libperiod.so.1', 'lib/libperiod.so.1.2',
                     'cmake-build-debug/CMakeLists.txt', 'nested/cmake-build-release/x',
                     'nested/CMakeCache.txt', 'nested/core.1234'):
            with self.subTest(name=name):
                self.assertTrue(checker.path_errors(name, 0, b''))

    def test_secret_patterns_detect_supported_token_families(self):
        for prefix in ('ghp_', 'gho_', 'ghu_', 'ghs_', 'ghr_', 'github_pat_'):
            with self.subTest(prefix=prefix):
                data = b'token="' + fake_token(prefix) + b'"'
                self.assertTrue(checker.path_errors('notes.txt', len(data), data))
        data = b'AKIA' + b'Z' * 16
        self.assertTrue(checker.path_errors('notes.txt', len(data), data))

    def test_private_key_headers(self):
        for kind in ('', 'RSA ', 'EC ', 'OPENSSH ', 'DSA ', 'ENCRYPTED '):
            with self.subTest(kind=kind):
                data = b'-----BEGIN ' + kind.encode() + b'PRIVATE KEY-----'
                self.assertTrue(checker.path_errors('notes.txt', len(data), data))

    def test_short_tokens_and_embedded_word_fragments_are_not_credentials(self):
        for data in (fake_token(length=19), b'prefix' + fake_token(),
                     b'AKIA' + b'Z' * 15, b'AKIA' + b'Z' * 17,
                     b'-----BEGIN PUBLIC KEY-----', b'ordinary research notes'):
            with self.subTest(data=data):
                self.assertEqual(checker.path_errors('notes.txt', len(data), data), [])

    def test_env_example_is_still_scanned_for_credentials(self):
        data = fake_token()
        self.assertTrue(checker.path_errors('.env.example', len(data), data))

    def test_binary_content_is_scanned_and_credential_values_are_redacted(self):
        token = fake_token()
        errors = checker.path_errors('data.bin', 25, b'\x00\xff' + token + b'\x00')
        self.assertTrue(errors)
        self.assertNotIn(token.decode(), '\n'.join(errors))

    def test_multiple_violations_are_reported(self):
        errors = checker.path_errors('build/program.exe', 50_000_001, fake_token())
        self.assertEqual(len(errors), 3)


class IdentityTests(unittest.TestCase):
    def test_valid_shapes_include_unicode_names_and_id_length_boundaries(self):
        for sid, name in (('A2345', 'Test Contributor'), ('A' + '2' * 31, '测试成员'),
                          ('A12_3-4', 'Jean-Luc Test')):
            with self.subTest(sid=sid):
                checker.validate_identity(sid, name)

    def test_malformed_student_ids_are_rejected(self):
        for sid in ('', 'A234', 'A' + '2' * 32, '_2345', '-2345', ' A2345',
                    'A2345 ', 'A23 45', 'A234\n5', '学号12345', 'A23/45'):
            with self.subTest(sid=sid), self.assertRaises(ValueError):
                checker.validate_identity(sid, 'Test Contributor')

    def test_placeholder_and_ta_ids_are_rejected(self):
        for sid in ('student1', 'YOUR1234', 'TODO1234', 'example123',
                    'placeholder1', '11111', 'aaaaa', '1234567890', '2250025281'):
            with self.subTest(sid=sid), self.assertRaises(ValueError):
                checker.validate_identity(sid, 'Test Contributor')

    def test_malformed_and_placeholder_names_are_rejected(self):
        for name in ('', 'A', ' Test Contributor', 'Test Contributor ', 'A\nB',
                     'A\rB', 'A<B', 'A>B', 'A\x00B', 'Full Name', 'YOUR NAME',
                     'todo', 'student', 'unknown'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                checker.validate_identity('A2345', name)


class TemporaryRepository(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='cs340-check-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        # Ignore caller-specific Git settings and index/working-tree overrides.
        env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_TERMINAL_PROMPT='0', PYTHONDONTWRITEBYTECODE='1')
        patcher = mock.patch.dict(os.environ, env, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def init_git(self):
        self.git('init', '-q')
        self.git('config', 'user.name', 'Test Contributor')
        self.git('config', 'user.email', 'tests@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')

    def write(self, name, data=b'safe\n'):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def install_script(self):
        path = self.root / 'scripts' / 'check_repository.py'
        path.parent.mkdir(exist_ok=True)
        shutil.copyfile(SCRIPT, path)
        return path

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(self.install_script()), *args],
                              cwd=self.root, capture_output=True, text=True)


class GitAndFilesystemTests(TemporaryRepository):
    def test_plain_directory_scan_excludes_git_metadata(self):
        self.write('results/run.log')
        self.write('.git/nested/credentials.json', fake_token())
        self.assertEqual(checker.check(self.root), [])
        self.write('build/object.o')
        self.assertTrue(checker.check(self.root))

    def test_staged_check_requires_repository_root(self):
        self.assertEqual(checker.check(self.root, staged=True),
                         ['Staged checking requires the repository root.'])
        self.init_git()
        subdir = self.root / 'nested'
        subdir.mkdir()
        self.assertEqual(checker.check(subdir, staged=True),
                         ['Staged checking requires the repository root.'])

    def test_tracked_scan_ignores_untracked_outputs(self):
        self.init_git()
        self.write('safe.txt')
        self.git('add', 'safe.txt')
        self.write('build/object.o')
        self.assertEqual(checker.check(self.root), [])
        self.git('add', 'build/object.o')
        self.assertTrue(checker.check(self.root))

    def test_missing_tracked_path_is_reported(self):
        self.init_git()
        path = self.write('safe.txt')
        self.git('add', 'safe.txt')
        path.unlink()
        self.assertIn('tracked path is missing', '\n'.join(checker.check(self.root)))

    def test_staged_content_is_checked_even_if_worktree_is_clean(self):
        self.init_git()
        path = self.write('notes.txt', fake_token())
        self.git('add', 'notes.txt')
        path.write_bytes(b'safe')
        self.assertTrue(checker.check(self.root, staged=True))
        self.assertEqual(checker.check(self.root), [])

    def test_unstaged_secret_does_not_change_the_index_check(self):
        self.init_git()
        path = self.write('notes.txt')
        self.git('add', 'notes.txt')
        path.write_bytes(fake_token())
        self.assertEqual(checker.check(self.root, staged=True), [])
        self.assertTrue(checker.check(self.root))

    def test_staged_deletion_does_not_read_deleted_blob(self):
        self.init_git()
        self.write('notes.txt')
        self.git('add', '.')
        self.git('commit', '-qm', 'Temporary test fixture')
        self.git('rm', 'notes.txt')
        self.assertEqual(checker.check(self.root, staged=True), [])

    def test_staged_rename_is_checked_under_new_path(self):
        self.init_git()
        self.write('notes.txt')
        self.git('add', '.')
        self.git('commit', '-qm', 'Temporary test fixture')
        self.git('mv', 'notes.txt', 'notes.exe')
        self.assertIn('notes.exe:', '\n'.join(checker.check(self.root, staged=True)))

    def test_staged_names_with_spaces_unicode_and_newlines(self):
        self.init_git()
        for name in ('two words.txt', '实验.txt', 'line\nbreak.txt'):
            self.write(name, fake_token())
        self.git('add', '.')
        errors = checker.check(self.root, staged=True)
        self.assertEqual(len(errors), 3)
        self.assertTrue(all('possible credential detected' in e for e in errors))

    def test_oversized_worktree_file_is_rejected_without_reading_it(self):
        path = self.write('large.log', b'')
        with path.open('wb') as handle:
            handle.truncate(50_000_001)
        with mock.patch.object(Path, 'read_bytes', side_effect=AssertionError('must not read')):
            self.assertIn('larger than 50,000,000 bytes', '\n'.join(checker.check(self.root)))

    def test_staged_size_is_measured_from_blob_without_loading_large_content(self):
        self.init_git()
        self.write('notes.txt', b'12345')
        self.git('add', '.')
        with mock.patch.object(checker, 'MAX_BYTES', 4), mock.patch.object(checker, 'git', wraps=checker.git) as git:
            self.assertTrue(checker.check(self.root, staged=True))
        self.assertFalse(any('show' in call.args[1:] for call in git.call_args_list))

    def test_worktree_symlinks_including_broken_targets_are_rejected(self):
        for name, target in (('link', 'target.txt'), ('broken', 'absent.txt')):
            with self.subTest(name=name):
                self.write('target.txt')
                path = self.root / name
                path.symlink_to(target)
                self.assertIn('symlink requires explicit review', '\n'.join(checker.check(self.root)))
                path.unlink()

    def test_staged_symlink_is_rejected_even_if_worktree_is_regular(self):
        self.init_git()
        path = self.root / 'link'
        path.symlink_to('absent.txt')
        self.git('add', 'link')
        path.unlink()
        path.write_bytes(b'safe')
        self.assertIn('symlink requires explicit review', '\n'.join(checker.check(self.root, staged=True)))

    def test_staged_regular_file_to_symlink_type_change_is_rejected(self):
        self.init_git()
        path = self.write('notes.txt')
        self.git('add', '.')
        self.git('commit', '-qm', 'Temporary test fixture')
        path.unlink()
        path.symlink_to('absent.txt')
        self.git('add', 'notes.txt')
        self.assertTrue(self.git('diff', '--cached', '--name-status').stdout.startswith(b'T\t'))
        self.assertIn('symlink requires explicit review', '\n'.join(checker.check(self.root, staged=True)))

    def test_staged_symlink_to_regular_file_type_change_is_scanned(self):
        self.init_git()
        path = self.root / 'notes.txt'
        path.symlink_to('absent.txt')
        self.git('add', '.')
        self.git('commit', '-qm', 'Temporary test fixture')
        path.unlink()
        path.write_bytes(fake_token())
        self.git('add', 'notes.txt')
        self.assertIn('possible credential detected', '\n'.join(checker.check(self.root, staged=True)))

    def test_cli_success_returns_zero(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('PASS:', result.stdout)
        self.assertEqual(result.stderr, '')

    def test_cli_rule_violation_returns_one_without_echoing_secret(self):
        token = fake_token()
        self.write('notes.txt', token)
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertIn('FAIL:', result.stderr)
        self.assertNotIn(token.decode(), result.stdout + result.stderr)
        self.assertNotIn('PASS:', result.stdout)

    def test_cli_staged_without_git_returns_one(self):
        result = self.run_cli('--staged')
        self.assertEqual(result.returncode, 1)
        self.assertIn('requires the repository root', result.stderr)

    def test_cli_unknown_option_returns_two(self):
        result = self.run_cli('--not-a-valid-option')
        self.assertEqual(result.returncode, 2)
        self.assertIn('unrecognized arguments', result.stderr)

    def test_cli_missing_git_returns_two(self):
        with mock.patch.dict(os.environ, {'PATH': ''}):
            result = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn('CHECK ERROR:', result.stderr)
        self.assertNotIn('PASS:', result.stdout)


class MainErrorTests(unittest.TestCase):
    def test_operational_errors_return_two_and_no_success(self):
        for failure in (OSError('unreadable file'), ValueError('bad Git size'),
                        subprocess.CalledProcessError(128, ['git', 'ls-files'])):
            with self.subTest(failure=type(failure).__name__):
                stdout, stderr = io.StringIO(), io.StringIO()
                with mock.patch.object(sys, 'argv', ['check_repository.py']), \
                     mock.patch.object(checker, 'check', side_effect=failure), \
                     contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    self.assertEqual(checker.main(), 2)
                self.assertIn('CHECK ERROR:', stderr.getvalue())
                self.assertEqual(stdout.getvalue(), '')


class CommitHookTests(TemporaryRepository):
    def setUp(self):
        super().setUp()
        self.init_git()
        self.install_script()
        self.git('config', 'cs340.studentId', 'A2345')
        self.git('config', 'cs340.fullName', 'Test Contributor')
        self.hook = self.root / '.githooks' / 'commit-msg'
        self.hook.parent.mkdir()
        shutil.copyfile(REPO / '.githooks' / 'commit-msg', self.hook)

    def run_hook(self, message):
        path = Path(self.temp.name) / 'message.txt'
        path.write_text(message, encoding='utf-8')
        return subprocess.run([sys.executable, str(self.hook), str(path)],
                              cwd=self.root, capture_output=True, text=True)

    def test_valid_subject_with_comment_preamble_is_accepted(self):
        result = self.run_hook('# comment\n\n[A2345] Test Contributor: add regression coverage\n\nDetails\n')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_mismatched_identity_prefixes_are_rejected(self):
        for subject in ('[B2345] Test Contributor: add regression coverage',
                        '[A2345] Another Person: add regression coverage',
                        'add regression coverage'):
            with self.subTest(subject=subject):
                self.assertEqual(self.run_hook(subject).returncode, 1)

    def test_description_length_boundary(self):
        prefix = '[A2345] Test Contributor: '
        self.assertEqual(self.run_hook(prefix + '1234567').returncode, 1)
        self.assertEqual(self.run_hook(prefix + '12345678').returncode, 0)

    def test_missing_identity_config_is_rejected(self):
        self.git('config', '--unset', 'cs340.studentId')
        self.assertEqual(self.run_hook('[A2345] Test Contributor: add regression coverage').returncode, 1)

    def test_git_author_name_must_match_configured_name(self):
        self.git('config', 'user.name', 'Another Person')
        result = self.run_hook('[A2345] Test Contributor: add regression coverage')
        self.assertEqual(result.returncode, 1)
        self.assertIn('user.name', result.stderr)

    def test_empty_message_is_rejected(self):
        self.assertEqual(self.run_hook('# comment only\n').returncode, 1)


if __name__ == '__main__':
    unittest.main()
