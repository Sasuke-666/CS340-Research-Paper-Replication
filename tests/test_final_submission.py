"""Prevent publishing stale, incomplete or redirected final deliverables."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_final_submission import check
from package_final_submission import package


def commit_fixture(root, data):
    """Create separate source-freeze and delivery commits in an isolated repository."""
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), '-c', 'user.name=Fixture Author',
                                        '-c', 'user.email=fixture@example.invalid', *args],
                                       stderr=subprocess.PIPE, text=True).strip()
    git('init', '--quiet')
    git('config', 'core.autocrlf', 'false')
    git('add', '--', *(row['path'] for row in data['sources']))
    git('commit', '--quiet', '-m', 'Freeze fixture sources')
    data['source_commit'] = git('rev-parse', 'HEAD')
    (root / 'submission/FINAL_RELEASE.json').write_text(json.dumps(data), encoding='utf-8')
    git('add', '.')
    git('commit', '--quiet', '-m', 'Freeze fixture delivery')
    return git


class FinalSubmissionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        sources = {
            'report/EXPANDED_REPORT.md': '# Fixture\n\nFinal report revised 24 November 2026.\n',
            'report/REVISION_DATE': '2026-11-24\n',
            'report/AI_STATEMENT.md': 'Disclosure fixture\n',
            'presentation/SLIDES.md': 'Slide source fixture\n',
            'presentation/TALK_OUTLINE.md': 'Talk fixture\n',
            'docs/CONTRIBUTIONS.csv': 'Contribution fixture\n',
            'docs/MEMBER_ACTIONS_ZH.md': 'Handbook fixture\n',
            'docs/FINAL_SUBMISSION_CHECKLIST.md': 'Checklist fixture\n',
            'submission/RELEASE_NOTES.md': 'Final release fixture\n',
        }
        for name, text in sources.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
        names = []
        for stem, extensions in (
            ('CS340_PERIOD_Final_Report_20261124', ('.pdf', '.docx')),
            ('CS340_PERIOD_Final_Presentation_20261124', ('.pptx', '.pdf')),
            ('CS340_Final_Submission_Handbook_20261124', ('.docx', '.pdf')),
        ):
            for extension in extensions:
                path = self.root / 'submission' / (stem + extension)
                path.parent.mkdir(exist_ok=True)
                if extension == '.pdf':
                    path.write_bytes(b'%PDF-1.4\nSynthetic validation fixture\n')
                else:
                    with zipfile.ZipFile(path, 'w') as package:
                        package.writestr('ppt/presentation.xml' if extension == '.pptx'
                                         else 'word/document.xml', '<fixture/>')
                names.append(path.relative_to(self.root).as_posix())
        def row(name):
            content = (self.root / name).read_bytes()
            return {'path': name, 'size_bytes': len(content),
                    'sha256': hashlib.sha256(content).hexdigest()}
        self.data = {'schema_version': 1, 'tag': 'v1.0', 'status': 'ready',
                     'report_revision': '2026-11-24', 'source_commit': 'a' * 40,
                     'sources': [row(name) for name in sources],
                     'artifacts': [row(name) for name in names]}

    def run_check(self, data=None):
        path = self.root / 'submission/FINAL_RELEASE.json'
        path.write_text(json.dumps(self.data if data is None else data), encoding='utf-8')
        return check(self.root, check_commit=False)

    def test_complete_frozen_fixture_passes(self):
        result = self.run_check()
        self.assertEqual(result['verified_documents'], 6)
        self.assertFalse(result['git_commit_verified'])

    def test_patch_tags_keep_the_checks_and_reject_invalid_release_names(self):
        for tag in ('v1.0', 'v1.0.1', 'v1.0.999999'):
            with self.subTest(tag=tag):
                data = dict(self.data, tag=tag)
                result = self.run_check(data)
                self.assertEqual(result['tag'], tag)
                self.assertEqual(result['verified_documents'], 6)
        for tag in ('v1.0.0', 'v1.0.01', 'v1.0.1000000', 'v1.1',
                    'v1.0.1/other', 'v1.0.1\n', 'v1.0.1 --draft', '', None, 1):
            with self.subTest(tag=tag), self.assertRaisesRegex(ValueError, 'release tag'):
                self.run_check(dict(self.data, tag=tag))

    def test_source_or_export_change_requires_new_manifest(self):
        for section in ('sources', 'artifacts'):
            path = self.root / self.data[section][0]['path']
            original = path.read_bytes()
            with self.subTest(section=section):
                path.write_bytes(original + b'changed')
                with self.assertRaisesRegex(ValueError, 'Content or size differs'):
                    self.run_check()
                path.write_bytes(original)

    def test_missing_documents_sources_and_wrong_date_fail(self):
        for mutate in (
            lambda d: d['artifacts'].pop(),
            lambda d: d['sources'].pop(),
            lambda d: d.update(report_revision='2026-11-25'),
            lambda d: d.update(tag='v2.0'),
            lambda d: d.update(status='preparing'),
        ):
            data = copy.deepcopy(self.data)
            mutate(data)
            with self.subTest(data=data), self.assertRaises(ValueError):
                self.run_check(data)

    def test_path_redirection_and_duplicate_sources_fail(self):
        for name in ('../outside.txt', '/outside.txt', 'docs\\outside.txt',
                     './report/EXPANDED_REPORT.md', 'report//EXPANDED_REPORT.md',
                     '.git/config',
                     self.data['sources'][0]['path']):
            data = copy.deepcopy(self.data)
            row = dict(data['sources'][0], path=name)
            data['sources'].append(row)
            with self.subTest(path=name), self.assertRaises(ValueError):
                self.run_check(data)

    def test_declared_source_commit_must_contain_the_frozen_source_bytes(self):
        git = commit_fixture(self.root, self.data)
        self.assertTrue(check(self.root)['git_commit_verified'])
        name = self.data['sources'][0]['path']
        path = self.root / name
        path.write_bytes(path.read_bytes() + b'Later source revision\n')
        self.data['sources'][0].update(size_bytes=path.stat().st_size,
                                      sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        (self.root / 'submission/FINAL_RELEASE.json').write_text(json.dumps(self.data))
        git('add', '.')
        git('commit', '--quiet', '-m', 'Change source without updating declared source commit')
        with self.assertRaisesRegex(ValueError, 'Source differs from source_commit'):
            check(self.root)

    def test_bundle_contains_the_complete_clean_checkout_and_survives_extraction(self):
        git = commit_fixture(self.root, self.data)
        tool = self.root / 'run.sh'
        tool.write_text('#!/bin/sh\nexit 0\n')
        git('add', '--chmod=+x', 'run.sh')
        tool.chmod(0o755)
        git('commit', '--quiet', '-m', 'Track executable fixture')
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'delivery.zip'
            first = package(self.root, output)
            self.assertEqual(first['sha256'], package(self.root, output)['sha256'])
            tracked = git('ls-files').splitlines()
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(archive.getinfo('Repository/run.sh').external_attr >> 16, 0o100755)
                names = archive.namelist()
                self.assertEqual(len(names), len(set(names)))
                self.assertTrue({'Repository/' + name for name in tracked} <= set(names))
                self.assertFalse(any('.git' in Path(name).parts for name in names))
                archive.extractall(Path(temp) / 'extracted')
            extracted = check(Path(temp) / 'extracted/Repository')
            self.assertEqual(extracted['verified_documents'], 6)
            self.assertFalse(extracted['git_commit_verified'])

    def test_packaging_rejects_dirty_or_untracked_inputs_and_protects_frozen_files(self):
        git = commit_fixture(self.root, self.data)
        artifact = self.root / self.data['artifacts'][0]['path']
        before = artifact.read_bytes()
        with self.assertRaisesRegex(ValueError, 'outside the repository'):
            package(self.root, artifact)
        self.assertEqual(artifact.read_bytes(), before)
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'delivery.zip'
            output.write_bytes(b'Existing bundle must survive failed checks')
            artifact.write_bytes(before + b'changed')
            with self.assertRaisesRegex(ValueError, 'clean tracked'):
                package(self.root, output)
            self.assertEqual(output.read_bytes(), b'Existing bundle must survive failed checks')
            artifact.write_bytes(before)
            git('rm', '--cached', '--', 'docs/FINAL_SUBMISSION_CHECKLIST.md')
            git('commit', '--quiet', '-m', 'Remove a required source from the tracked tree')
            with self.assertRaisesRegex(ValueError, 'must all be tracked'):
                package(self.root, output)


if __name__ == '__main__':
    unittest.main()
