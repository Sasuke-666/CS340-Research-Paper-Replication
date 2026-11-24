"""Negative and positive checks for the member evidence manifest."""

import copy
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import audit_1240001156_validation_evidence as evidence  # noqa: E402


class ValidationEvidenceTests(unittest.TestCase):
    def test_archived_manifest_verifies(self):
        result = evidence.verify_manifest()
        self.assertEqual(result['files'], len(evidence.DEFAULT_PATHS))
        self.assertGreater(result['bytes'], 0)

    def test_missing_extra_and_duplicate_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            expected_paths = ('real.txt',)
            (root / 'real.txt').write_bytes(b'real\n')
            (root / 'extra.txt').write_bytes(b'extra\n')
            manifest = evidence.build_manifest(root, expected_paths)

            missing = copy.deepcopy(manifest)
            missing['files'].pop()
            with self.assertRaisesRegex(ValueError, 'stale or incomplete'):
                evidence.verify_manifest_data(missing, root, expected_paths)

            extra = copy.deepcopy(manifest)
            extra['files'].append(evidence.entry_for(root, 'extra.txt'))
            with self.assertRaisesRegex(ValueError, 'stale or incomplete'):
                evidence.verify_manifest_data(extra, root, expected_paths)

            duplicate = copy.deepcopy(manifest)
            duplicate['files'].append(copy.deepcopy(duplicate['files'][0]))
            with self.assertRaisesRegex(ValueError, 'duplicate manifest path'):
                evidence.verify_manifest_data(duplicate, root, expected_paths)

    def test_unsafe_paths_are_rejected(self):
        for path in ('../README.md', '/etc/passwd', 'docs/../../README.md'):
            with self.subTest(path=path):
                with self.assertRaisesRegex(ValueError, 'unsafe'):
                    evidence.build_manifest(ROOT, (path,))

    def test_byte_and_hash_mismatch_are_rejected(self):
        manifest = evidence.load_manifest(evidence.DEFAULT_MANIFEST)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = 'evidence.txt'
            (root / relative).write_bytes(b'original\n')
            expected_paths = (relative,)
            good = evidence.build_manifest(root, expected_paths)
            evidence.verify_manifest_data(good, root, expected_paths)

            changed_bytes = copy.deepcopy(good)
            changed_bytes['files'][0]['bytes'] += 1
            with self.assertRaisesRegex(ValueError, 'byte-count mismatch'):
                evidence.verify_manifest_data(changed_bytes, root, expected_paths)

            changed_hash = copy.deepcopy(good)
            changed_hash['files'][0]['sha256'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
                evidence.verify_manifest_data(changed_hash, root, expected_paths)

        self.assertEqual(manifest['schema_version'], 1)


if __name__ == '__main__':
    unittest.main()
