"""从演示正文、讲者备注和可编辑版式导出 PPTX 与 PDF。"""
import argparse
from collections import Counter
from io import BytesIO
import json
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape
from zipfile import ZipFile

from office_pdf import convert_pdf
from report_config import revision_date

ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/Sasuke-666/CS340-Research-Paper-Replication'
DRAW = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
PRES = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
CHART = '{http://schemas.openxmlformats.org/drawingml/2006/chart}'
DOCREL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKGREL = '{http://schemas.openxmlformats.org/package/2006/relationships}'
SHEET = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
FIELD = re.compile(r'\{\{([a-zA-Z0-9_]+)\}\}')


def parse_slides(markdown):
    blocks = re.split(r'^## Slide (\d+): (.+)$', markdown, flags=re.M)[1:]
    slides = []
    for number, title, body in zip(blocks[::3], blocks[1::3], blocks[2::3]):
        if int(number) != len(slides) + 1:
            raise ValueError(f'Unexpected slide number {number}')
        screen, notes = body.split('### Chinese speaker notes')
        notes, sources = notes.split('### Sources')
        screen = screen.split('### English screen text')[1]
        fields = {'title': title}
        table = []
        counts = Counter()
        for line in screen.strip().splitlines():
            line = line.strip()
            if not line or line == 'Native editable chart data:':
                continue
            if line.startswith('|'):
                cells = [cell.strip() for cell in line.strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', cell) for cell in cells):
                    table.append(cells)
                continue
            kind = 'point' if line.startswith('- ') else 'caption'
            for paragraph in line.removeprefix('- ').split('<br>'):
                counts[kind] += 1
                fields[f'{kind}{counts[kind]}'] = paragraph.strip()
        links = re.findall(r'\[([^\]]+)\]\((https?://[^\s)]+)\)', sources)
        if not links or not notes.strip():
            raise ValueError(f'Missing speaker notes or sources on slide {number}')
        slides.append((fields, table, notes.strip().split('\n\n'), links))
    return slides


def check_chart(archive, table):
    """同时对照屏幕图表缓存和 PowerPoint 的编辑数据工作簿。"""
    chart = ET.fromstring(archive.read('ppt/slides/charts/chart1.xml'))
    if not table or any(len(row) != 3 for row in table):
        raise ValueError('Expected a program and two chart series')
    columns = list(zip(*table))
    series = chart.findall('.//' + CHART + 'ser')
    if len(series) != len(columns) - 1:
        raise ValueError('Chart series count differs from Markdown')
    for item, column in zip(series, columns[1:]):
        for field, expected in [('tx', column[:1]), ('cat', columns[0][1:]), ('val', column[1:])]:
            values = tuple(n.text for n in item.findall(CHART + field + '//' + CHART + 'v'))
            if values != expected:
                raise ValueError(f'Chart {field} differs from Markdown: {values}')
    with ZipFile(BytesIO(archive.read('ppt/embeddings/chart-data-snapshot-001.xlsx'))) as book:
        sheet = ET.fromstring(book.read('xl/worksheets/sheet1.xml'))
    rows = [[''.join(cell.itertext()) for cell in row.findall(SHEET + 'c')]
            for row in sheet.findall('.//' + SHEET + 'row')]
    expected = [['Category', table[0][1], 'Category', table[0][2]]]
    expected.extend([case, a, case, b] for case, a, b in table[1:])
    if rows != expected:
        raise ValueError('Embedded workbook differs from Markdown')


def render_screen(template, fields, table):
    values = fields.copy()
    for r, row in enumerate(table, start=1):
        for c, cell in enumerate(row, start=1):
            for p, part in enumerate(cell.split('<br>'), start=1):
                values[f'cell{r}_{c}_{p}'] = part.strip()
    xml = template.decode('utf-8')
    if Counter(FIELD.findall(xml)) != Counter(values.keys()):
        raise ValueError('Slide text/table dimensions differ from the editable layout')
    return FIELD.sub(lambda m: escape(values[m[1]]), xml).encode('utf-8')


def make_notes(template, relationships, paragraphs, links, revision):
    notes = ET.fromstring(template)
    rels = ET.fromstring(relationships)
    body = next(shape.find(PRES + 'txBody') for shape in notes.iter(PRES + 'sp')
                if shape.find('.//' + PRES + 'ph').get('type') == 'body')
    for node in body.findall(DRAW + 'p'):
        body.remove(node)

    def add(text, target=None):
        run = ET.SubElement(ET.SubElement(body, DRAW + 'p'), DRAW + 'r')
        if target:
            link_id = 'Source' + str(len(rels) + 1)
            ET.SubElement(ET.SubElement(run, DRAW + 'rPr'), DRAW + 'hlinkClick',
                          {'{' + DOCREL + '}id': link_id})
            ET.SubElement(rels, PKGREL + 'Relationship',
                          Id=link_id, Target=target, TargetMode='External', Type=DOCREL + '/hyperlink')
        ET.SubElement(run, DRAW + 't').text = text

    for paragraph in paragraphs:
        add(paragraph)
    add('来源 / Sources')
    for i, (label, url) in enumerate(links, start=1):
        url = re.sub(r'^' + re.escape(REPO) + r'/blob/v[\d.]+/', f'{REPO}/blob/{revision}/', url)
        add(f'[{i}] {label}')
        add(url, url)
    return ET.tostring(notes, encoding='utf-8'), ET.tostring(rels, encoding='utf-8')


def export_pptx(destination, revision):
    slides = parse_slides((ROOT / 'presentation/SLIDES.md').read_text(encoding='utf-8'))
    with ZipFile(ROOT / 'presentation/SLIDE_LAYOUT.pptx') as base:
        if len(slides) != sum(bool(re.fullmatch(r'ppt/slides/slide\d+\.xml', n))
                              for n in base.namelist()):
            raise ValueError('Slide count differs from the editable layout')
        changes = {}
        for number, (fields, table, paragraphs, links) in enumerate(slides, start=1):
            path = f'ppt/slides/slide{number}.xml'
            if number == 5:
                check_chart(base, table)
                table = []
            changes[path] = render_screen(base.read(path), fields, table)
            notes = f'ppt/notesSlides/notesSlide{number}.xml'
            rels = f'ppt/notesSlides/_rels/notesSlide{number}.xml.rels'
            changes[notes], changes[rels] = make_notes(base.read(notes), base.read(rels), paragraphs, links, revision)
        meta = 'docProps/core.xml'
        changes[meta] = base.read(meta).replace(b'{{source_commit}}', revision.encode('ascii'))
        with ZipFile(destination, 'w') as out:
            for entry in base.infolist():
                out.writestr(entry, changes.get(entry.filename, base.read(entry)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-commit', help='文档绑定的完整源提交')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'report/export')
    args = parser.parse_args()
    if args.source_commit:
        revision = args.source_commit
    else:
        manifest = ROOT / 'submission/FINAL_RELEASE.json'
        frozen = json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else {}
        revision = frozen.get('source_commit') if frozen.get('status') == 'ready' else None
        if not revision:
            revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    if not re.fullmatch('[0-9a-f]{40}', revision):
        raise ValueError('Expected a full Git source SHA')
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    stem = 'CS340_PERIOD_Final_Presentation_' + revision_date(ROOT).strftime('%Y%m%d')
    with TemporaryDirectory(dir=output) as temp:
        work = Path(temp)
        pptx = work / (stem + '.pptx')
        export_pptx(pptx, revision)
        pdf = pptx.with_suffix('.pdf')
        convert_pdf(pptx, pdf)
        for path in (pptx, pdf):
            path.replace(output / path.name)
            print(output / path.name)


if __name__ == '__main__':
    main()
