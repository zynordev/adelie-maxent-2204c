"""Build the reviewable report from one Markdown source, without model runs.

Use the Codex bundled Python. Render the resulting DOCX with the packaged
render_docx.py and --emit_pdf; only promote that visually checked PDF.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT=Path(__file__).resolve().parents[1]


def font(style,size,bold=False):
    style.font.name='Times New Roman';style.font.size=Pt(size)
    style.font.bold=bold;style.font.color.rgb=RGBColor(0,0,0)
    rpr=style.element.get_or_add_rPr()
    for key in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme','csTheme']:
        rpr.rFonts.attrib.pop(qn('w:'+key),None)
    rpr.rFonts.set(qn('w:eastAsia'),'Times New Roman')
    for node in list(style.element.iter(qn('w:pBdr'))):node.getparent().remove(node)


def inline(paragraph,text):
    tokens=re.split(r'(\*\*.*?\*\*|\*[^*]+\*|`[^`]+`)',text)
    for token in tokens:
        if not token:continue
        run=paragraph.add_run(token[2:-2] if token.startswith('**') else
                              token[1:-1] if token.startswith(('*','`')) else token)
        if token.startswith('**'):run.bold=True
        elif token.startswith('*'):run.italic=True
        elif token.startswith('`'):run.font.name='Liberation Mono';run.font.size=Pt(9)


def table(doc,lines):
    values=[[v.strip() for v in line.strip().strip('|').split('|')] for line in lines]
    values=[r for r in values if not all(re.fullmatch(r'[-: ]+',v) for v in r)]
    count=len(values[0])
    if any(len(r)!=count for r in values):raise ValueError('Ragged Markdown table')
    widths={3:[5.1,5.3,5.6],4:[4.3,3.9,3.9,3.9],7:[4.3,1.95,1.95,1.95,1.95,1.95,1.95]}.get(count)
    if widths is None:widths=[16/count]*count
    t=doc.add_table(rows=0,cols=count);t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    for col,width in zip(t.columns,widths):col.width=Cm(width)
    for i,row in enumerate(values):
        cells=t.add_row().cells
        trpr=t.rows[-1]._tr.get_or_add_trPr()
        no_split=OxmlElement('w:cantSplit');trpr.append(no_split)
        if i==0:trpr.append(OxmlElement('w:tblHeader'))
        for j,(cell,text,width) in enumerate(zip(cells,row,widths)):
            cell.width=Cm(width);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            tcpr=cell._tc.get_or_add_tcPr()
            borders=OxmlElement('w:tcBorders')
            for side in ['top','left','bottom','right']:
                edge=OxmlElement('w:'+side)
                for key,val in [('val','single'),('sz','4'),('color','D9D9D9')]:edge.set(qn('w:'+key),val)
                borders.append(edge)
            tcpr.append(borders)
            margins=OxmlElement('w:tcMar')
            for side in ['top','bottom','left','right']:
                item=OxmlElement('w:'+side);item.set(qn('w:w'),'85');item.set(qn('w:type'),'dxa');margins.append(item)
            tcpr.append(margins)
            shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'E5E7EB' if i==0 else ('F7F7F7' if i%2==0 else 'FFFFFF'));tcpr.append(shade)
            p=cell.paragraphs[0];p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=1.05
            p.alignment=WD_ALIGN_PARAGRAPH.LEFT if j==0 or count==3 and i>0 and len(text)>30 else WD_ALIGN_PARAGRAPH.CENTER
            inline(p,text)
            for run in p.runs:
                run.font.size=Pt(9 if count==7 else 10)
                if i==0:run.bold=True
    doc.add_paragraph().paragraph_format.space_after=Pt(2)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=ROOT/'rapor/TUBITAK_2204C_PROJE_RAPORU.md')
    parser.add_argument('--output',type=Path,default=ROOT/'rapor/TUBITAK_2204C_PROJE_RAPORU.docx')
    args=parser.parse_args()
    text=args.source.read_text();lines=text.splitlines();doc=Document();section=doc.sections[0]
    # Preserve the existing report's A4 format, not a new Letter document.
    section.page_width=Cm(21);section.page_height=Cm(29.7)
    section.top_margin=section.bottom_margin=Cm(2.2)
    section.left_margin=section.right_margin=Cm(2.5)
    for name,size,bold in [('Normal',11,False),('Title',14,True),('Subtitle',10,False),
                           ('Heading 1',13,True),('Heading 2',11.5,True),('Caption',10,False)]:
        font(doc.styles[name],size,bold)
    for node in list(doc.element.iter(qn('w:pBdr'))):node.getparent().remove(node)
    base=doc.styles['Normal'].paragraph_format
    base.line_spacing=1.15;base.space_after=Pt(6);base.widow_control=True
    for name in ['Title','Heading 1','Heading 2']:
        f=doc.styles[name].paragraph_format;f.keep_with_next=True;f.space_before=Pt(10);f.space_after=Pt(6)
    footer=section.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
    field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
    images=[];i=0;references=False
    while i<len(lines):
        line=lines[i].strip()
        if not line or line=='---':i+=1;continue
        if line.startswith('|'):
            block=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                block.append(lines[i]);i+=1
            table(doc,block);continue
        match=re.fullmatch(r'!\[(.*?)\]\((.*?)\)',line)
        if match:
            path=Path(match[2]);path=path if path.is_absolute() else args.source.parent/path
            if not path.is_file():raise FileNotFoundError(path)
            p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next=True
            p.add_run().add_picture(str(path),width=Cm(16))
            doc.inline_shapes[-1]._inline.docPr.set('descr',match[1]);images.append(str(path))
        elif line.startswith('# '):
            title=line[2:]
            if i==0:p=doc.add_paragraph(title,'Subtitle')
            else:
                p=doc.add_paragraph(title,'Heading 1')
                if title=='Kaynaklar':references=True;p.paragraph_format.page_break_before=True
        elif line.startswith('## '):doc.add_paragraph(line[3:],'Heading 2')
        elif line.startswith('**Proje adı:**'):
            doc.add_paragraph(line.split('**Proje adı:**',1)[1].strip(),'Title')
        else:
            # All author paragraphs in this source occupy one Markdown line.
            p=doc.add_paragraph()
            if re.match(r'^(Tablo|Şekil) \d+\.',line):
                p.style='Caption';p.paragraph_format.keep_with_next=line.startswith('Tablo')
            elif references:
                p.paragraph_format.left_indent=Cm(.5);p.paragraph_format.first_line_indent=Cm(-.5)
                p.paragraph_format.line_spacing=1.05
            else:p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
            inline(p,line)
            if references:
                for run in p.runs:run.font.size=Pt(10)
        i+=1
    props=doc.core_properties
    props.title='Marguerite Körfezi odaklı Adélie pengueni modellemesi'
    props.subject='Tamamlanan yöntem denetimleri ve bekleyen koloni analizleri'
    props.author='';props.last_modified_by='';props.comments=''
    args.output.parent.mkdir(parents=True,exist_ok=True);doc.save(args.output)
    manifest={'markdown_sha256':hashlib.sha256(text.encode()).hexdigest(),
              'docx_sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),
              'source':str(args.source),'output':str(args.output),'figures':images,
              'model_run_performed':False,'report_status':'completed audits; colony results pending'}
    args.output.with_suffix('.build.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'docx':str(args.output),'figures':len(images),'status':manifest['report_status']}))


if __name__=='__main__':main()
