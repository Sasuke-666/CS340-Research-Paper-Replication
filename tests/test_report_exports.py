"""Check exported evidence links; optional document packages are not CI prerequisites."""
import importlib.util
from pathlib import Path
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import export_stage_report as exporter


class ReportLinkTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / 'report').mkdir()
        (self.root / 'results').mkdir()
        self.source = self.root / 'report/EXPANDED_REPORT.md'
        self.source.write_text('Report', encoding='utf-8')
        (self.root / 'results/evidence rows.csv').write_text('value\n1\n', encoding='utf-8')
        self.ref = 'a' * 40

    def resolve(self, target):
        return exporter.resolve_report_link(target, self.root, self.source, self.ref)

    def test_labels_files_directories_and_fragments_keep_destinations(self):
        text = 'Read [rows](../results/evidence rows.csv) and https://example.org/a'
        self.assertEqual([(label, target) for _, _, label, target in exporter.link_parts(text)],
                         [('rows', '../results/evidence rows.csv'),
                          ('https://example.org/a', 'https://example.org/a')])
        prefix = exporter.REPOSITORY_URL
        self.assertEqual(self.resolve('../results/evidence%20rows.csv'),
                         prefix + '/blob/' + self.ref + '/results/evidence%20rows.csv')
        self.assertEqual(self.resolve('../results/'),
                         prefix + '/tree/' + self.ref + '/results')
        self.assertEqual(self.resolve('#evidence'),
                         prefix + '/blob/' + self.ref + '/report/EXPANDED_REPORT.md#evidence')

    def test_external_query_is_preserved_and_invalid_local_targets_fail(self):
        external = 'https://example.org/?a=1&b=2#evidence'
        self.assertEqual(self.resolve(external), external)
        for target in ('../../outside.csv', '../missing.csv', 'file:///tmp/evidence',
                       'javascript:alert(1)', '//example.org/evidence'):
            with self.subTest(target=target), self.assertRaises(ValueError):
                self.resolve(target)


@unittest.skipUnless(all(importlib.util.find_spec(name) is not None
                         for name in ('cairosvg', 'docx', 'reportlab')),
                     'Optional report dependencies are not installed')
class ReportPackageLinkTests(unittest.TestCase):
    def test_docx_relationships_and_pdf_annotations_preserve_evidence_links(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'report').mkdir()
            (root / 'results').mkdir()
            (root / 'results/evidence rows.csv').write_text('value\n1\n', encoding='utf-8')
            source = root / 'report/EXPANDED_REPORT.md'
            source.write_text(
                '# Evidence export fixture\n\n'
                'Stage report revised 22 November 2026.\n\n'
                '[Rows](../results/evidence rows.csv), [batch](../results/), '
                '[section](#evidence) and [external](https://example.org/?a=1&b=2#section).\n\n'
                '## References\n\nFixture references.\n', encoding='utf-8')
            (root / 'report/REVISION_DATE').write_text('2026-11-22\n', encoding='utf-8')
            (root / 'report/AI_STATEMENT.md').write_text('', encoding='utf-8')
            ref = 'a' * 40
            docx_path, pdf_path = exporter.export(root, root / 'export', repository_ref=ref)
            prefix = exporter.REPOSITORY_URL
            expected = {
                prefix + '/blob/' + ref + '/results/evidence%20rows.csv',
                prefix + '/tree/' + ref + '/results',
                prefix + '/blob/' + ref + '/report/EXPANDED_REPORT.md#evidence',
                'https://example.org/?a=1&b=2#section',
            }
            with ZipFile(docx_path) as package:
                relationships = ET.fromstring(package.read('word/_rels/document.xml.rels'))
                links = [node for node in relationships if node.attrib['Type'].endswith('/hyperlink')]
                self.assertEqual({node.attrib['Target'] for node in links}, expected)
                self.assertTrue(all(node.attrib.get('TargetMode') == 'External' for node in links))
                document = ET.fromstring(package.read('word/document.xml'))
                visible = ''.join(document.itertext())
                for label in ('Rows', 'batch', 'section', 'external'):
                    self.assertIn(label, visible)
                self.assertNotIn(str(root), visible)
            pdf = pdf_path.read_bytes()
            # ReportLab writes URI actions as uncompressed PDF dictionaries. These
            # fixture URLs contain no PDF literal-string escape characters.
            self.assertEqual({match.group(1).decode('ascii') for match in
                              re.finditer(rb'/URI\s*\(([^)]*)\)', pdf)}, expected)
            self.assertGreaterEqual(pdf.count(b'/Subtype /Link'), len(expected))
            self.assertNotIn(str(root).encode(), pdf)


if __name__ == '__main__':
    unittest.main()
