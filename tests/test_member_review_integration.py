"""Synthetic regression fixtures for the maintainer's strict offline audit."""
import contextlib
import hashlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import audit_member_reviews as audit

HIT = b"Perform Reproduction!\nBug found!\ntwostage_bad.c:48: void *funcB(void *): Assertion `0' failed.\n"


class MemberReviewAuditTests(unittest.TestCase):
    def fixture(self, folder):
        (folder / 'host.txt').write_text('synthetic host\n')
        (folder / 'container.txt').write_text('synthetic build\n')
        for n in range(1, 6):
            (folder / f'replay-{n}.txt').write_bytes(HIT)
            (folder / f'replay-{n}.exit').write_text('0\n')
        self.rehash(folder)

    def rehash(self, folder):
        paths = sorted(p for p in folder.iterdir() if p.name != 'SHA256SUMS')
        (folder / 'SHA256SUMS').write_text(''.join(
            f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in paths))

    def test_valid_replays(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.fixture(root)
            self.assertEqual(audit.audit_replays(root), (12, 5))

    def test_missing_assertion_fails_even_with_consistent_hash(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.fixture(root)
            (root / 'replay-1.txt').write_bytes(b'Perform Reproduction!\nnormal\n')
            self.rehash(root)
            with self.assertRaises(ValueError): audit.audit_replays(root)

    def test_digest_corruption_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.fixture(root)
            (root / 'replay-1.txt').write_bytes(HIT + b'changed')
            with self.assertRaises(ValueError): audit.audit_replays(root)

    def test_missing_checksum_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.fixture(root)
            checksum = root / 'SHA256SUMS'
            checksum.write_text('\n'.join(checksum.read_text().splitlines()[1:]) + '\n')
            with self.assertRaises(ValueError): audit.audit_replays(root)

    def test_driver_success_alone_is_insufficient(self):
        self.assertFalse(audit.matching_assertion(b'Perform Reproduction!\nnormal', 0))

    def test_pre_reproduction_assertion_does_not_count(self):
        self.assertFalse(audit.matching_assertion(HIT.split(b'\n', 1)[1] + b'Perform Reproduction!\n', 0))

    def test_timeout_with_assertion_does_not_pass(self):
        self.assertFalse(audit.matching_assertion(HIT, 124))

    def test_sequence_normalization(self):
        raw = b'\x1b[31mtest 0001: [[0]]\x1b[0m\ntest 0002: [[1]]\n'
        expected = hashlib.sha256(b'test 0001: [[0]]\ntest 0002: [[1]]').hexdigest()
        self.assertEqual(audit.sequence_digest(raw, 2), expected)

    def test_sequence_missing_id_fails(self):
        with self.assertRaises(ValueError): audit.sequence_digest(b'test 0002: [[0]]\n', 1)

    def test_command_returns_failure_for_nonmatching_evidence(self):
        with patch.object(audit, 'audit_account', return_value=40), \
             patch.object(audit, 'audit_replays', side_effect=ValueError('0/5 synthetic')), \
             contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(audit.main([]), 1)


if __name__ == '__main__':
    unittest.main()
