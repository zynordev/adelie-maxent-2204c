#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TÜBİTAK 2204-C Resmî Proje Raporu Word (.docx) ve PDF Üreticisi
Klasik TÜBİTAK Proje Yazma Şablonu Standartları:
- Kenar Boşlukları: 2.5 cm (Her yönden: Üst, Alt, Sol, Sağ)
- Yazı Tipi: Times New Roman (12 pt gövde, 1.15 satır aralığı, 6 pt sonra boşluk, İki yana yaslı)
- Başlıklar: 12-13 pt Kalın Siyah (Otomatik / RGB 0,0,0), keepWithNext
- Tablolar: Klasik APA formatı, başlık tablonun ÜSTÜNDE, no vertical borders
- Şekiller: Ortalanmış, altyazı şeklin ALTINDA, keepWithNext
- Sayfa Numaralandırma: Alt bilgi sağda/ortada, Times New Roman 10 pt
- Çıktılar: TUBITAK_2204C_PROJE_RAPORU.docx ve TUBITAK_2204C_PROJE_RAPORU.pdf
"""

import os
import sys
import re
import subprocess
import docx
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

import importlib.util

def add_formatted_runs(paragraph, text, base_size=12, base_bold=False, base_italic=False):
    t = text.replace('<b>', '**').replace('</b>', '**')
    t = t.replace('<i>', '*').replace('</i>', '*')
    t = t.replace('<em>', '*').replace('</em>', '*')
    t = t.replace('<strong>', '**').replace('</strong>', '**')
    
    tokens = re.split(r'(\*\*\*.*?\*\*\*|\*\*.*?\*\*|\*.*?\*)', t)
    for tok in tokens:
        if not tok:
            continue
        run = paragraph.add_run()
        run.font.name = 'Times New Roman'
        run.font.size = Pt(base_size)
        run.font.color.rgb = RGBColor(0, 0, 0)
        
        # Ensure Times New Roman in XML
        rPr = run._r.get_or_add_rPr()
        rFonts = parse_xml(r'<w:rFonts %s w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>' % nsdecls('w'))
        rPr.append(rFonts)

        if tok.startswith('***') and tok.endswith('***') and len(tok) >= 6:
            run.text = tok[3:-3]
            run.bold = True
            run.italic = True
        elif tok.startswith('**') and tok.endswith('**') and len(tok) >= 4:
            run.text = tok[2:-2]
            run.bold = True
            run.italic = base_italic
        elif tok.startswith('*') and tok.endswith('*') and len(tok) >= 2:
            run.text = tok[1:-1]
            run.bold = base_bold
            run.italic = True
        else:
            run.text = tok
            run.bold = base_bold
            run.italic = base_italic

def setup_page_and_styles(doc):
    section = doc.sections[0]
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    
    # Alt bilgi sayfa numarası
    footer = section.footer
    p_footer = footer.paragraphs[0]
    p_footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_footer.paragraph_format.space_before = Pt(0)
    p_footer.paragraph_format.space_after = Pt(0)
    run_footer = p_footer.add_run()
    run_footer.font.name = 'Times New Roman'
    run_footer.font.size = Pt(10)
    run_footer.font.color.rgb = RGBColor(0, 0, 0)
    
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run_footer._r.append(fldChar1)
    run_footer._r.append(instrText)
    run_footer._r.append(fldChar2)
    run_footer._r.append(fldChar3)
    
    # Normal stil ayarı
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.line_spacing = 1.15
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    rPr = style.element.get_or_add_rPr()
    rFonts = parse_xml(r'<w:rFonts %s w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>' % nsdecls('w'))
    rPr.append(rFonts)

def create_table_apa(doc, data, col_widths=None, header_bg="F2F2F2"):
    num_rows = len(data)
    num_cols = len(data[0])
    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # APA Tablo Kenarlıkları: Üst ve alt 1 pt siyah çizgi, iç yatay hafif gri çizgi, dikey çizgi yok
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        r'<w:tblBorders %s>'
        r'  <w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        r'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        r'  <w:left w:val="none"/>'
        r'  <w:right w:val="none"/>'
        r'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="D0D0D0"/>'
        r'  <w:insideV w:val="none"/>'
        r'</w:tblBorders>' % nsdecls('w')
    )
    tblPr.append(tblBorders)
    
    for r_idx, row in enumerate(table.rows):
        is_header = (r_idx == 0)
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
        if is_header:
            trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))
            
        for c_idx, cell in enumerate(row.cells):
            tcPr = cell._tc.get_or_add_tcPr()
            # Padding
            tcMar = parse_xml(
                f'<w:tcMar {nsdecls("w")}>'
                f'  <w:top w:w="80" w:type="dxa"/>'
                f'  <w:bottom w:w="80" w:type="dxa"/>'
                f'  <w:left w:w="120" w:type="dxa"/>'
                f'  <w:right w:w="120" w:type="dxa"/>'
                f'</w:tcMar>'
            )
            tcPr.append(tcMar)
            
            if is_header and header_bg:
                shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{header_bg}"/>')
                tcPr.append(shd)
                
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.first_line_indent = Cm(0)
            
            raw_val = data[r_idx][c_idx]
            cell_text = raw_val.text if hasattr(raw_val, 'text') else str(raw_val)
            
            # Hizalama
            if is_header:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                add_formatted_runs(p, cell_text, base_size=9.5, base_bold=True)
            else:
                # Sayı veya kısa kod ise ortala, metin ise sola yasla
                if len(cell_text) <= 8 and (re.match(r'^-?[0-9.,% ±]+$', cell_text) or cell_text in ['X', '%', 'mm', '°C', '1', '2', '3', '4', '5', '6']):
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                is_bold_row = (r_idx == num_rows - 1 and cell_text == "Toplam")
                add_formatted_runs(p, cell_text, base_size=9.0, base_bold=is_bold_row)
                
            if col_widths and c_idx < len(col_widths):
                cell.width = Cm(col_widths[c_idx])
                
    return table

def build_tubitak_report():
    base_dir = "/home/halil/adelie-maxent-2204c"
    out_docx = os.path.join(base_dir, "rapor/TUBITAK_2204C_PROJE_RAPORU.docx")
    out_pdf = os.path.join(base_dir, "rapor/TUBITAK_2204C_PROJE_RAPORU.pdf")
    
    print("Capturing verified report data from make_perfect_report.py...")
    spec = importlib.util.spec_from_file_location('mpr', os.path.join(base_dir, 'rapor/make_perfect_report.py'))
    mpr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mpr)
    
    captured_story = []
    class MockDoc:
        def __init__(self, *args, **kwargs): pass
        def build(self, story, canvasmaker=None): captured_story.extend(story)
        
    mpr.SimpleDocTemplate = MockDoc
    orig_sub_run = subprocess.run
    mpr.subprocess.run = lambda *args, **kwargs: type('Res', (), {'returncode': 0, 'stderr': '', 'stdout': ''})()
    mpr.build_perfect_18_page_report()
    mpr.subprocess.run = orig_sub_run
    subprocess.run = orig_sub_run
    
    print(f"Captured {len(captured_story)} flowable elements.")
    
    doc = docx.Document()
    setup_page_and_styles(doc)
    
    # 1. TÜBİTAK Başlık Bloğu (Sayfa 1 En Üst)
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.first_line_indent = Cm(0)
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(4)
    p_meta.paragraph_format.line_spacing = 1.15
    add_formatted_runs(p_meta, "**Proje Ana Alanı:** Kutup Araştırmaları (Biyoloji ve Ekoloji)", base_size=11)
    
    p_meta2 = doc.add_paragraph()
    p_meta2.paragraph_format.first_line_indent = Cm(0)
    p_meta2.paragraph_format.space_before = Pt(0)
    p_meta2.paragraph_format.space_after = Pt(4)
    p_meta2.paragraph_format.line_spacing = 1.15
    add_formatted_runs(p_meta2, "**Proje Tematik Alanı:** Kutup Biyoçeşitliliği ve Ekosistem Dinamikleri", base_size=11)
    
    p_title = doc.add_paragraph()
    p_title.paragraph_format.first_line_indent = Cm(0)
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(12)
    p_title.paragraph_format.line_spacing = 1.15
    add_formatted_runs(p_title, "**Proje Adı (Başlığı):** MaxEnt Algoritması ve CMIP6 İklim Senaryoları Kullanılarak Marguerite Körfezi'nde (Batı Antarktika) Adélie Pengueni (*Pygoscelis adeliae*) Potansiyel Habitat Uygunluğunun ve İklim Değişim Eğilimlerinin Modellenmesi", base_size=12)

    # Akış indeksini takip ederek elemanları Word'e aktar
    # İlk 3 eleman (DocTitle, DocMeta, Sub) ve HR/Spacer geçilir çünkü TÜBİTAK başlık bloğunu yukarıda ekledik
    skip_indices = set()
    
    # Tabloların başlıklarını (sonrasındaki caption) tablonun ÜSTÜNE almak için harita çıkar
    table_captions = {}
    for i, item in enumerate(captured_story):
        if type(item).__name__ == 'Table':
            if i + 1 < len(captured_story) and type(captured_story[i+1]).__name__ == 'Paragraph':
                next_p = captured_story[i+1]
                if next_p.style.name == 'Caption' and next_p.text.startswith('Tablo '):
                    table_captions[i] = next_p.text
                    skip_indices.add(i + 1)

    # İlgili sütun genişlikleri haritası (toplam 16.0 cm)
    col_widths_map = {
        0: [3.2, 1.8, 1.0, 2.2, 2.3, 5.5],   # Tablo 1 (6 cols)
        1: [3.0, 4.0, 9.0],                  # Tablo 2 (3 cols)
        2: [0.8, 4.2, 4.2, 2.0, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8], # Tablo 3 Gantt (10 cols)
        3: [4.5, 3.0, 3.0, 5.5],             # Tablo 4 (4 cols)
        4: [4.2, 2.4, 2.5, 2.4, 2.3, 2.2],   # Tablo 5 (6 cols)
        5: [3.2, 2.8, 2.5, 2.5, 3.0, 2.0],   # Tablo 6 (6 cols)
        6: [4.5, 2.2, 2.4, 2.8, 4.1]         # Tablo 7 (5 cols)
    }
    table_counter = 0

    idx = 0
    while idx < len(captured_story):
        if idx in skip_indices:
            idx += 1
            continue
            
        item = captured_story[idx]
        tname = type(item).__name__
        
        # İlk sayfa başlıkları zaten eklendi
        if idx in [0, 1, 2, 3, 4]:
            idx += 1
            continue

        if tname == 'Paragraph':
            style_name = item.style.name
            text = item.text.strip()
            
            if style_name == 'SecHead':
                # Ana Başlıklar (Özet, Amaç, Giriş, Yöntem, Bulgular, Sonuç ve Tartışma, Öneriler, Kaynaklar)
                p = doc.add_paragraph()
                p.paragraph_format.first_line_indent = Cm(0)
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.space_after = Pt(3.5)
                p.paragraph_format.keep_with_next = True
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                add_formatted_runs(p, text, base_size=13, base_bold=True)
                
            elif style_name == 'SubSecHead':
                # 2. Derece Başlıklar (1.1, 1.2, 2.1 vb.)
                p = doc.add_paragraph()
                p.paragraph_format.first_line_indent = Cm(0)
                p.paragraph_format.space_before = Pt(10)
                p.paragraph_format.space_after = Pt(3.5)
                p.paragraph_format.keep_with_next = True
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                add_formatted_runs(p, text, base_size=12, base_bold=True)
                
            elif style_name == 'SubSubSecHead':
                # 3. Derece Başlıklar (2.6.1, 2.6.2 vb.)
                p = doc.add_paragraph()
                p.paragraph_format.first_line_indent = Cm(0)
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.keep_with_next = True
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                add_formatted_runs(p, text, base_size=12, base_bold=True, base_italic=True)
                
            elif style_name == 'BodyBold':
                # Anahtar Kelimeler
                p = doc.add_paragraph()
                p.paragraph_format.first_line_indent = Cm(0)
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(10)
                p.paragraph_format.line_spacing = 1.15
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                add_formatted_runs(p, text, base_size=12)
                
            elif style_name == 'Bullet':
                # Madde İmleri
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(0.75)
                p.paragraph_format.first_line_indent = Cm(-0.5)
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(3.5)
                p.paragraph_format.line_spacing = 1.15
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                add_formatted_runs(p, text, base_size=12)
                
            elif style_name == 'RefStyle':
                # Kaynaklar (APA Asılı Girinti)
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(1.0)
                p.paragraph_format.first_line_indent = Cm(-1.0)
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(2.5)
                p.paragraph_format.line_spacing = 1.05
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                add_formatted_runs(p, text, base_size=9.5)
                
            elif style_name == 'Caption':
                # Genel Caption
                p = doc.add_paragraph()
                p.paragraph_format.first_line_indent = Cm(0)
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(8)
                p.paragraph_format.line_spacing = 1.15
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                add_formatted_runs(p, text, base_size=10, base_italic=True)
                
            else:
                # Normal Gövde Metni (1.0 cm girintili, iki yana yaslı)
                p = doc.add_paragraph()
                p.paragraph_format.first_line_indent = Cm(1.0)
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(2.5)
                p.paragraph_format.line_spacing = 1.05
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                add_formatted_runs(p, text, base_size=12)
                
        elif tname == 'Table':
            # Önce Tablo Başlığı (TÜBİTAK kuralı: Tablonun ÜSTÜNDE)
            if idx in table_captions:
                p_cap = doc.add_paragraph()
                p_cap.paragraph_format.first_line_indent = Cm(0)
                p_cap.paragraph_format.space_before = Pt(10)
                p_cap.paragraph_format.space_after = Pt(3.5)
                p_cap.paragraph_format.keep_with_next = True
                p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
                add_formatted_runs(p_cap, table_captions[idx], base_size=9.5, base_bold=False)
            
            # Tabloyu oluştur
            c_widths = col_widths_map.get(table_counter, None)
            table_counter += 1
            create_table_apa(doc, item._cellvalues, col_widths=c_widths)
            
            # Tablo sonrası boşluk
            # p_sp removed
            # p_sp.space_before = Pt(0)
            # p_sp.space_after = Pt(6)
            # p_sp.first_line_indent = Cm(0)
            
        elif tname == 'KeepTogether':
            # Şekil ve Altyazısı
            img_obj = None
            cap_obj = None
            for sub in item._content:
                if type(sub).__name__ == 'Image':
                    img_obj = sub
                elif type(sub).__name__ == 'Paragraph':
                    cap_obj = sub
                    
            if img_obj and hasattr(img_obj, 'filename') and os.path.exists(img_obj.filename):
                # Görsel paragrafı
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.first_line_indent = Cm(0)
                p_img.paragraph_format.space_before = Pt(8)
                p_img.paragraph_format.space_after = Pt(2)
                p_img.paragraph_format.keep_with_next = True
                
                run_img = p_img.add_run()
                # Haritalar ve grafikler için uygun genişlik
                w_cm = 11.5
                if 'roc' in img_obj.filename.lower():
                    w_cm = 10.5
                elif 'jacknife' in img_obj.filename.lower():
                    w_cm = 11.5
                elif 'belirsizlik' in img_obj.filename.lower():
                    w_cm = 11.0
                run_img.add_picture(img_obj.filename, width=Cm(w_cm))
                
                # Altyazı paragrafı (TÜBİTAK kuralı: Şeklin ALTINDA)
                if cap_obj:
                    p_cap = doc.add_paragraph()
                    p_cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    p_cap.paragraph_format.first_line_indent = Cm(0)
                    p_cap.paragraph_format.space_before = Pt(3)
                    p_cap.paragraph_format.space_after = Pt(10)
                    p_cap.paragraph_format.line_spacing = 1.15
                    add_formatted_runs(p_cap, cap_obj.text, base_size=10, base_italic=False)
                    
        elif tname == 'PageBreak':
            # Bölüm geçişlerinde temiz sayfa sonları
            # Özellikle Bulgular, Sonuç ve Tartışma, Kaynaklar öncesi veya büyük harita geçişlerinde
            # Word'ün doğal akışını bozmamak için sadece ana bloklar öncesinde bırakıyoruz
            pass

        idx += 1

    doc.save(out_docx)
    print(f"Word document generated: {out_docx}")
    
    # LibreOffice headless PDF dönüştürme
    print("Converting DOCX to PDF via LibreOffice...")
    cmd = f"soffice --headless --convert-to pdf {out_docx} --outdir {os.path.dirname(out_pdf)}"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"PDF generated: {out_pdf}")
        # pdftocairo ile sanitize et
        tmp_clean = "/tmp/clean_report.pdf"
        cmd_cairo = f"pdftocairo -pdf {out_pdf} {tmp_clean} && mv {tmp_clean} {out_pdf}"
        subprocess.run(cmd_cairo, shell=True, capture_output=True, text=True)
        print("PDF sanitized with pdftocairo.")
    else:
        print(f"LibreOffice conversion error: {res.stderr}")
        
    # PDF Sayfa Sayısı ve Kalite Kontrolü
    cmd_info = f"pdfinfo {out_pdf} | grep Pages"
    res_info = subprocess.run(cmd_info, shell=True, capture_output=True, text=True)
    print("PDF Info:", res_info.stdout.strip())

if __name__ == "__main__":
    build_tubitak_report()
