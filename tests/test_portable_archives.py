"""Audit real archived bytes under both Windows and POSIX path/text defaults."""
from pathlib import Path, PureWindowsPath
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import summarize_comparison as comparison
import summarize_layout as layout

ACCEPTANCE = ROOT / 'results/2026-11-22/acceptance-45015126850-attempt1'
ARCHIVES = (
    (comparison, ACCEPTANCE,
     ROOT / 'results/2026-11-22/summaries/acceptance-45015126850-attempt1',
     {'expected_repeats': 3}),
    (layout, ROOT / 'results/2026-11-14/layout-43570556202',
     ROOT / 'results/2026-11-14/summaries/layout-43570556202-lazy01',
     {'expected_cases': ('lazy01',)}),
)


class PortableArchiveTests(unittest.TestCase):
    def test_windows_relative_paths_match_published_linux_outputs(self):
        native_relative_to = Path.relative_to

        def windows_relative_to(path, *other):
            return PureWindowsPath(native_relative_to(path, *other).as_posix())

        for module, batch, output, options in ARCHIVES:
            with self.subTest(auditor=module.__name__):
                # Only the relative path representation changes; actual reads
                # still use the platform's normal filesystem implementation.
                with patch.object(Path, 'relative_to', windows_relative_to):
                    result = module.summarize_batch(batch, **options)
                self.assertTrue(result['integrity_ok'], result['integrity_errors'])
                self.assertTrue(result['trials'])
                self.assertTrue(all('/' in row['log'] and '\\' not in row['log']
                                    for row in result['trials']))
                module.check_outputs(result, output)

    def test_windows_text_defaults_preserve_published_summary_bytes(self):
        native_open = Path.open

        def windows_text_open(path, mode='r', buffering=-1, encoding=None,
                              errors=None, newline=None):
            if 'b' not in mode and any(flag in mode for flag in 'wax') and newline is None:
                newline = '\r\n'
            return native_open(path, mode, buffering, encoding, errors, newline)

        for module, batch, output, options in ARCHIVES:
            with self.subTest(auditor=module.__name__):
                result = module.summarize_batch(batch, **options)
                self.assertTrue(result['integrity_ok'], result['integrity_errors'])
                before = {path.name: path.read_bytes() for path in output.iterdir() if path.is_file()}
                # A Linux test host also exercises Windows' default LF-to-CRLF
                # text writes. Explicit newline settings and binary I/O remain intact.
                with patch.object(Path, 'open', windows_text_open):
                    module.check_outputs(result, output)
                self.assertEqual(before, {path.name: path.read_bytes()
                                          for path in output.iterdir() if path.is_file()})

    def test_raw_log_line_endings_are_still_manifest_protected(self):
        with tempfile.TemporaryDirectory() as temp:
            batch = Path(temp) / 'batch'
            shutil.copytree(ACCEPTANCE / 'twostage', batch / 'twostage')
            options = {'expected_cases': ('twostage',), 'expected_repeats': 3}
            original = comparison.summarize_batch(batch, **options)
            self.assertTrue(original['integrity_ok'], original['integrity_errors'])
            log = batch / 'twostage/period_r01.txt'
            raw = log.read_bytes()
            changed = raw.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
            self.assertNotEqual(raw, changed)
            log.write_bytes(changed)
            result = comparison.summarize_batch(batch, **options)
            self.assertFalse(result['integrity_ok'])
            self.assertTrue(any('manifest content mismatch' in problem
                                for problem in result['integrity_errors']))
            self.assertEqual(log.read_bytes(), changed)


if __name__ == '__main__':
    unittest.main()
