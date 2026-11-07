#!/usr/bin/env python3
"""Export the existing English Markdown report to readable PDF and Word.

No experiments are run and no measurements are changed by this exporter.
See requirements-report.txt for the tested document-rendering dependencies.
"""
import argparse
from html import escape
from pathlib import Path
import re
import tempfile


def plain(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return text.replace('**', '').replace('`', '').replace('*', '')


def blocks(text):
    lines = text.splitlines(); i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1; continue
        match = re.match(r'^(#{1,3})\s+(.+)$', line)
        if match:
            yield ('heading', len(match[1]), match[2]); i += 1; continue
        if line.startswith('!['):
            match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line)
            if not match: raise ValueError('Invalid report image')
            yield ('image', match[1], match[2]); i += 1; continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', x) for x in cells): rows.append(cells)
                i += 1
            if not rows or len({len(r) for r in rows}) != 1: raise ValueError('Invalid report table')
            yield ('table', rows); continue
        paragraph = [line]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#|\||!\[|- )', lines[i].strip()):
            paragraph.append(lines[i].strip()); i += 1
        yield ('paragraph', ' '.join(paragraph).removeprefix('- '))


def export(root, output):
    import cairosvg
    from docx import Document
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether

    source = root / 'report/PILOT_REPORT.md'
    text = source.read_text(encoding='utf-8')
    statement = (root / 'report/AI_STATEMENT.md').read_text(encoding='utf-8')
    parsed = list(blocks(text.replace('## References', statement + '\n## References')))
    output.mkdir(parents=True, exist_ok=True)
    stem = 'CS340_PERIOD_Stage_Report_20261107'
    docx_path, pdf_path = output / (stem + '.docx'), output / (stem + '.pdf')
    doc = Document(); sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.2677), Inches(11.6929)
    sec.top_margin = sec.bottom_margin = Inches(0.65)
    sec.left_margin = sec.right_margin = Inches(0.65)
    sec.header_distance = sec.footer_distance = Inches(0.3)
    normal = doc.styles['Normal']; normal.font.name = 'Arial'; normal.font.size = Pt(10.5)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.12
    for name, size in [('Title', 22), ('Heading 1', 14), ('Heading 2', 12)]:
        style = doc.styles[name]; style.font.name = 'Arial'; style.font.size = Pt(size)
        style.font.color.rgb = __import__('docx').shared.RGBColor.from_string('17364D')
    doc.core_properties.title = 'PERIOD: scoped replication and depth-bound study'
    doc.core_properties.subject = 'CS340 stage report; archived measurements from 7 November 2026'
    doc.core_properties.author = 'CS340 project repository'
    header = sec.header.paragraphs[0]; header.text = 'CS340 | Operating Systems | Stage report'
    header.runs[0].font.size = Pt(8)
    footer = sec.footer.paragraphs[0]; footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    footer.add_run('Stage report - 7 November 2026 | Page ').font.size = Pt(8)
    fld = OxmlElement('w:fldSimple'); fld.set(qn('w:instr'), 'PAGE'); footer._p.append(fld)
    body = ParagraphStyle('Body', fontName='Helvetica', fontSize=10.2, leading=14,
                          spaceAfter=6, splitLongWords=True, alignment=TA_LEFT)
    title = ParagraphStyle('Title', parent=body, fontName='Helvetica-Bold', fontSize=21,
                           leading=25, spaceAfter=12, textColor=colors.HexColor('#17364D'))
    heading = ParagraphStyle('Heading', parent=body, fontName='Helvetica-Bold', fontSize=13,
                             leading=16, spaceBefore=11, spaceAfter=6, keepWithNext=True,
                             textColor=colors.HexColor('#17364D'))
    small = ParagraphStyle('Cell', parent=body, fontSize=8.1, leading=10.2, spaceAfter=0)
    story = []
    width = A4[0] - 84

    def inline(value):
        value = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', value)
        value = escape(value)
        value = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', value)
        value = re.sub(r'`([^`]+)`', r'<font name="Courier" size="8.6">\1</font>', value)
        value = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', value)
        return value

    with tempfile.TemporaryDirectory() as tmp:
        for n, block in enumerate(parsed):
            kind = block[0]
            if kind == 'heading':
                level, text = block[1:]
                doc.add_heading(plain(text), 0 if level == 1 else level - 1)
                story.append(Paragraph(inline(text), title if level == 1 else heading))
            elif kind == 'paragraph':
                text = block[1]
                p = doc.add_paragraph(plain(text))
                if text.startswith('**Table '): p.paragraph_format.keep_with_next = True
                if text.startswith('**Figure '):
                    for run in p.runs: run.italic = True; run.font.size = Pt(9)
                style = body
                if text.startswith('**Table '):
                    style = ParagraphStyle('TableCaption', parent=body, keepWithNext=True)
                story.append(Paragraph(inline(text), style))
            elif kind == 'table':
                rows = block[1]
                table = doc.add_table(rows=1, cols=len(rows[0])); table.style = 'Table Grid'
                table.autofit = True
                for j, text in enumerate(rows[0]): table.rows[0].cells[j].text = plain(text)
                repeat = OxmlElement('w:tblHeader'); table.rows[0]._tr.get_or_add_trPr().append(repeat)
                for row in rows[1:]:
                    cells = table.add_row().cells
                    for j, text in enumerate(row): cells[j].text = plain(text)
                for row in table.rows:
                    trpr = row._tr.get_or_add_trPr(); no_split = OxmlElement('w:cantSplit'); trpr.append(no_split)
                    for cell in row.cells:
                        for p in cell.paragraphs:
                            p.paragraph_format.space_after = Pt(3)
                            for run in p.runs: run.font.size = Pt(8.2)
                for cell in table.rows[0].cells:
                    for run in cell.paragraphs[0].runs: run.bold = True
                doc.add_paragraph().paragraph_format.space_after = Pt(0)
                count = len(rows[0])
                weights = ([.19, .25, .07, .20, .12, .17] if rows[0][0] == 'Case'
                           else [.25, .32, .23, .20] if count == 4
                           else [.065, .17, .17, .19, .195, .21] if count == 6
                           else [1/count] * count)
                weights = [x/sum(weights) for x in weights]
                cells = [[Paragraph(inline(x), small) for x in row] for row in rows]
                pdf_table = Table(cells, colWidths=[width*x for x in weights], repeatRows=1, hAlign='LEFT')
                pdf_table.setStyle(TableStyle([
                    ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E8EEF2')),
                    ('GRID',(0,0),(-1,-1),.35,colors.HexColor('#AAB7C1')),
                    ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),
                    ('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),
                    ('BOTTOMPADDING',(0,0),(-1,-1),5)]))
                story.extend([pdf_table, Spacer(1,8)])
            elif kind == 'image':
                caption, relative = block[1:]; path = (source.parent / relative).resolve()
                if root not in path.parents or not path.is_file(): raise ValueError('Missing/outside figure: ' + relative)
                target = Path(tmp) / ('figure-%d.png' % n)
                cairosvg.svg2png(url=str(path), write_to=str(target), output_width=1600)
                pic = doc.add_picture(str(target), width=Inches(6.55))
                pic._inline.docPr.set('descr', caption)
                image = Image(str(target)); ratio = image.imageHeight / image.imageWidth
                story.append(Image(str(target), width=width, height=width*ratio))
        doc.save(docx_path)

        def page(canvas, document):
            canvas.saveState(); canvas.setFont('Helvetica', 8)
            canvas.setFillColor(colors.HexColor('#526573'))
            canvas.drawString(42, A4[1]-25, 'CS340 | Operating Systems | Stage report')
            canvas.drawRightString(A4[0]-42, 24, '7 November 2026 | Page %d' % document.page)
            canvas.restoreState()

        SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=42, leftMargin=42,
                          topMargin=43, bottomMargin=40,
                          title='PERIOD: scoped replication and depth-bound study',
                          author='CS340 project repository').build(story, onFirstPage=page, onLaterPages=page)
    print(docx_path.relative_to(root) if docx_path.is_relative_to(root) else docx_path)
    print(pdf_path.relative_to(root) if pdf_path.is_relative_to(root) else pdf_path)
    return docx_path, pdf_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args(); root = Path(__file__).resolve().parents[1]
    export(root, args.output.resolve() if args.output else root / 'report/export')
