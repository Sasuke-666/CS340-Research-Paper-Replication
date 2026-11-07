"""Synthetic shell fixtures; these are not PERIOD experiment measurements."""
from pathlib import Path
import os
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PIN = 'cb8deb9a176e5bb292d70d46557dd61dc0e98069'


class OutputProtectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        bin_dir = self.root / 'bin'; bin_dir.mkdir()
        fixtures = {
            'git': '#!/bin/bash\nif [[ "$1" == clone ]]; then mkdir -p "${@: -1}"; printf fixture > "${@: -1}/LICENSE"; elif [[ "$*" == *rev-parse* ]]; then echo ' + PIN + '; fi\n',
            'docker': '#!/bin/bash\nif [[ "$1" == pull ]]; then echo fixture-pull; elif [[ "$*" == *--format* ]]; then echo fixture@sha256:123; else echo fixture; fi\n',
            'uname': '#!/bin/bash\nif [[ "$1" == -m ]]; then echo x86_64; else echo fixture-kernel; fi\n',
        }
        for name, text in fixtures.items():
            p = bin_dir / name; p.write_text(text); p.chmod(0o755)
        self.env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ['PATH'])
        self.env.pop('PERIOD_DRIVER', None); self.env.pop('PERIOD_IMAGE', None)

    def tearDown(self):
        self.tmp.cleanup()

    def run_wrapper(self, out, **env):
        return subprocess.run(['bash', str(ROOT / 'scripts/period_container_pilot.sh'), str(out)],
                              cwd=ROOT, env=dict(self.env, **env), capture_output=True, text=True, timeout=10)

    def test_existing_evidence_is_unchanged(self):
        out = self.root / 'existing'; out.mkdir()
        sentinel = out / 'image_pull.txt'; sentinel.write_text('original evidence\n')
        result = self.run_wrapper(out)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(sentinel.read_text(), 'original evidence\n')
        self.assertEqual(sorted(p.name for p in out.iterdir()), ['image_pull.txt'])

    def test_symlink_output_is_rejected_without_modification(self):
        target = self.root / 'archive'; target.mkdir()
        sentinel = target / 'image_pull.txt'; sentinel.write_text('retained\n')
        link = self.root / 'alias'; link.symlink_to(target, target_is_directory=True)
        result = self.run_wrapper(link)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(sentinel.read_text(), 'retained\n')

    def test_invalid_driver_does_not_create_output(self):
        out = self.root / 'invalid-driver'
        result = self.run_wrapper(out, PERIOD_DRIVER='../not-a-driver.py')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(out.exists())

    def test_fresh_output_is_accepted(self):
        out = self.root / 'parent/new'
        result = self.run_wrapper(out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((out / 'container_exit_code.txt').is_file())


if __name__ == '__main__':
    unittest.main()
