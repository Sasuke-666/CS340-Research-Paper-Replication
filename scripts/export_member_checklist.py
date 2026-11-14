#!/usr/bin/env python3
"""Export the separate Chinese member checklist to an editable Word document."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import posixpath
import re


def clean(value):
    value=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',value)
    return value.replace('**','').replace('`','').replace('<https://','https://').replace('>。','。')


def export(source, target):
    from docx import Document
    from docx.shared import Cm,Pt,RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    doc=Document();sec=doc.sections[0]
    sec.page_width,sec.page_height=Cm(21),Cm(29.7)
    sec.left_margin=sec.right_margin=Cm(1.8)
    sec.top_margin=sec.bottom_margin=Cm(1.7)
    sec.header_distance=sec.footer_distance=Cm(.65)
    for name,size in [('Normal',10.5),('Title',20),('Heading 1',14),('Heading 2',11.5)]:
        st=doc.styles[name];st.font.name='Noto Sans CJK SC';st.font.size=Pt(size)
        st.font.color.rgb=RGBColor(0,0,0)
        st.element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Noto Sans CJK SC')
        st.paragraph_format.space_after=Pt(5)
        st.paragraph_format.line_spacing=Pt(16 if name=='Normal' else size*1.35)
    for name in ['Title','Heading 1','Heading 2']:
        doc.styles[name].font.bold=True
        doc.styles[name].paragraph_format.keep_with_next=True
    normal=doc.styles['Normal'];normal.paragraph_format.widow_control=True
    header=sec.header.paragraphs[0];header.text='CS340 操作系统｜组员行动清单'
    header.runs[0].font.size=Pt(8)
    footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    footer.add_run('2026 年 11 月 14 日｜第 ').font.size=Pt(8)
    field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
    footer.add_run(' 页').font.size=Pt(8)
    doc.core_properties.title='CS340 PERIOD 组员本人行动清单'
    doc.core_properties.author='CS340 project repository'
    doc.core_properties.created=datetime.now(timezone.utc)
    doc.core_properties.modified=doc.core_properties.created

    def add_inline(paragraph, text, size=10.5, bold=False):
        """Use clickable source labels instead of filling cells with raw paths."""
        def text_run(value):
            run=paragraph.add_run(clean(value));run.font.size=Pt(size);run.bold=bold
        position=0
        for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)',text):
            text_run(text[position:match.start()])
            label,url=match.groups()
            if not re.match(r'^https?://',url):
                url='https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/main/'+posixpath.normpath('docs/'+url)
            rel=paragraph.part.relate_to(url,RT.HYPERLINK,is_external=True)
            link=OxmlElement('w:hyperlink');link.set(qn('r:id'),rel)
            run=OxmlElement('w:r');props=OxmlElement('w:rPr')
            fonts=OxmlElement('w:rFonts');fonts.set(qn('w:ascii'),'Noto Sans CJK SC');fonts.set(qn('w:eastAsia'),'Noto Sans CJK SC');props.append(fonts)
            font_size=OxmlElement('w:sz');font_size.set(qn('w:val'),str(int(size*2)));props.append(font_size)
            color=OxmlElement('w:color');color.set(qn('w:val'),'1F4E79');props.append(color)
            underline=OxmlElement('w:u');underline.set(qn('w:val'),'single');props.append(underline)
            if bold:props.append(OxmlElement('w:b'))
            run.append(props);value=OxmlElement('w:t');value.text=clean(label);run.append(value)
            link.append(run);paragraph._p.append(link);position=match.end()
        text_run(text[position:])
    lines=source.read_text(encoding='utf-8').splitlines();i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line.startswith('```'):
            i+=1
            while i<len(lines) and not lines[i].strip().startswith('```'):
                p=doc.add_paragraph();p.paragraph_format.space_after=Pt(0)
                p.paragraph_format.line_spacing=1.0
                p.paragraph_format.left_indent=Cm(.18)
                r=p.add_run(lines[i]);r.font.name='DejaVu Sans Mono';r.font.size=Pt(8)
                r._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Noto Sans CJK SC')
                sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'F3F3F3');p._p.get_or_add_pPr().append(sh)
                i+=1
            doc.add_paragraph().paragraph_format.space_after=Pt(2);i+=1;continue
        heading=re.match(r'^(#{1,3})\s+(.+)',line)
        if heading:
            p=doc.add_heading(clean(heading[2]),len(heading[1])-1)
            i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',x) for x in cells):rows.append(cells)
                i+=1
            n=len(rows[0]);table=doc.add_table(rows=0,cols=n);table.autofit=False
            ratios=[.12,.20,.37,.31] if n==4 else [.24,.48,.28] if n==3 else [.32,.68] if n==2 else [1/n]*n
            for j,col in enumerate(table.columns):col.width=Cm(17.4*ratios[j])
            pr=table._tbl.tblPr;borders=OxmlElement('w:tblBorders')
            for edge in ['top','left','bottom','right','insideH','insideV']:
                el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');borders.append(el)
            pr.append(borders)
            for ri,values in enumerate(rows):
                row=table.add_row();row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
                if ri==0:row._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
                for j,value in enumerate(values):
                    cell=row.cells[j];cell.width=Cm(17.4*ratios[j]);p=cell.paragraphs[0]
                    cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
                    p.paragraph_format.space_before=Pt(3);p.paragraph_format.space_after=Pt(3)
                    p.paragraph_format.keep_with_next=(ri==0)
                    add_inline(p,value,size=9,bold=(ri==0))
                    if ri==0:
                        sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'EEEEEE');cell._tc.get_or_add_tcPr().append(sh)
            doc.add_paragraph().paragraph_format.space_after=Pt(0);continue
        ordered=re.match(r'^(\d+)\.\s+(.+)$',line)
        if ordered:
            parts=[ordered[2]];i+=1
            while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||```|- |\d+\.\s)',lines[i].strip()):
                parts.append(lines[i].strip());i+=1
            p=doc.add_paragraph();add_inline(p,ordered[1]+'. '+' '.join(parts))
            p.paragraph_format.left_indent=Cm(.55)
            p.paragraph_format.first_line_indent=Cm(-.55)
            p.paragraph_format.keep_together=True
            continue
        if line.startswith('- [ ] '):
            p=doc.add_paragraph();add_inline(p,'☐ '+line[6:]);p.paragraph_format.left_indent=Cm(.4);p.paragraph_format.first_line_indent=Cm(-.4)
            i+=1;continue
        if line.startswith('- '):
            p=doc.add_paragraph();add_inline(p,'• '+line[2:]);p.paragraph_format.left_indent=Cm(.4);p.paragraph_format.first_line_indent=Cm(-.4)
            i+=1;continue
        paragraph=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||```|- |\d+\.\s)',lines[i].strip()):
            paragraph.append(lines[i].strip());i+=1
        add_inline(doc.add_paragraph(),' '.join(paragraph))
    for tree in (doc._element,doc.styles.element):
        for border in tree.xpath('.//w:pBdr'):border.getparent().remove(border)
    target.parent.mkdir(parents=True,exist_ok=True);doc.save(target);print(target)


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=root/'report/export/CS340_Member_Action_Checklist_20261114.docx')
    args=p.parse_args();export(root/'docs/MEMBER_ACTIONS_ZH.md',args.output)
