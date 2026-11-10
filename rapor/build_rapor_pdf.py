#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RAPOR_TASLAK_v1.md dosyasını A4 PDF'e çevirir (basit Markdown alt kümesi)."""
import os, re, subprocess, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

F = '/usr/share/fonts/TTF/'
for n, f in [('R', 'Roboto-Regular'), ('B', 'Roboto-Bold'), ('I', 'Roboto-Italic'), ('BI', 'Roboto-BoldItalic')]:
    pdfmetrics.registerFont(TTFont(n, F + f + '.ttf'))
pdfmetrics.registerFontFamily('R', normal='R', bold='B', italic='I', boldItalic='BI')

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'RAPOR_TASLAK_v1.md')
OUT = os.path.join(HERE, 'RAPOR_TASLAK_v1.pdf')

body = ParagraphStyle('b', fontName='R', fontSize=9.3, leading=13.2, spaceAfter=5, alignment=4)
h1 = ParagraphStyle('h1', fontName='B', fontSize=14, leading=18, spaceAfter=6, textColor=colors.HexColor('#0F172A'))
h2 = ParagraphStyle('h2', fontName='B', fontSize=11.5, leading=15, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor('#1E3A8A'), keepWithNext=1)
h3 = ParagraphStyle('h3', fontName='B', fontSize=9.8, leading=13, spaceBefore=5, spaceAfter=3, textColor=colors.HexColor('#1E293B'), keepWithNext=1)
cap = ParagraphStyle('c', fontName='I', fontSize=8.2, leading=11, spaceAfter=6, alignment=1, textColor=colors.HexColor('#334155'))
cell = ParagraphStyle('t', fontName='R', fontSize=8.2, leading=10.5)
cellb = ParagraphStyle('tb', parent=cell, fontName='B')
bul = ParagraphStyle('bl', parent=body, leftIndent=12, firstLineIndent=-9, alignment=0, spaceAfter=3)
ref = ParagraphStyle('r', parent=body, leftIndent=14, firstLineIndent=-14, alignment=0, fontSize=8.6, leading=11.6)


def inline(t):
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    t = re.sub(r'`(.+?)`', r'<font face="R" color="#7C2D12">\1</font>', t)
    return t


class NC(canvas.Canvas):
    def __init__(s, *a, **k):
        super().__init__(*a, **k); s._st = []
    def showPage(s):
        s._st.append(dict(s.__dict__)); s._startPage()
    def save(s):
        n = len(s._st)
        for st in s._st:
            s.__dict__.update(st)
            s.setFont('R', 7.8); s.setFillColor(colors.HexColor('#64748B'))
            s.drawString(45, 28, 'TÜBİTAK 2204-C · Marguerite Körfezi Adélie MaxEnt · Rapor taslağı v1')
            s.drawRightString(550, 28, f'{s._pageNumber} / {n}')
            super().showPage()
        super().save()


def table(rows):
    data = []
    for i, r in enumerate(rows):
        data.append([Paragraph(inline(c), cellb if i == 0 else cell) for c in r])
    n = len(rows[0])
    w = 505 / n
    if n == 3:
        cw = [235, 135, 135]
    elif n == 5:
        cw = [90, 110, 105, 100, 100]
    else:
        cw = [w] * n
    if rows[0][0].startswith('Tarih'):
        cw = [90, 415]
    t = Table(data, colWidths=cw, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E2E8F0')),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#94A3B8')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    return t


def build():
    lines = open(SRC, encoding='utf-8').read().split('\n')
    st = []
    i = 0
    while i < len(lines):
        l = lines[i].rstrip()
        if not l.strip():
            i += 1; continue
        if l.startswith('# '):
            st.append(Paragraph(inline(l[2:]), h1))
        elif l.startswith('## '):
            st.append(Paragraph(inline(l[3:]), h2))
        elif l.startswith('### '):
            st.append(Paragraph(inline(l[4:]), h3))
        elif l.startswith('!['):
            m = re.match(r'!\[(.*)\]\((.*)\)', l)
            img = Image(m.group(2), width=470, height=470 * 2480 / 3507)
            st.append(KeepTogether([img, Paragraph(inline(m.group(1)), cap)]))
        elif l.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                    rows.append(cells)
                i += 1
            st.append(table(rows)); st.append(Spacer(1, 3))
            continue
        elif re.match(r'^(\d+\.|-) ', l):
            mk = re.match(r'^(\d+\.|-) (.*)', l)
            st.append(Paragraph(('• ' if mk.group(1) == '-' else mk.group(1) + ' ') + inline(mk.group(2)), bul))
        elif l.startswith('*Tablo') or l.startswith('*Şekil'):
            st.append(Paragraph(inline(l), cap))
        elif re.match(r'^(Booth|Chapman|Cimino|Dormann|GBIF|Hersbach|Phillips|Roberts|Skachkova|Wang)', l):
            st.append(Paragraph(inline(l), ref))
        else:
            st.append(Paragraph(inline(l), body))
        i += 1
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=45, rightMargin=45, topMargin=42, bottomMargin=44,
                            title='Marguerite Körfezi Adélie MaxEnt — Rapor taslağı v1', author='Halil Erdem Yanık')
    doc.build(st, canvasmaker=NC)
    tmp = OUT + '.tmp'
    subprocess.run(['pdftocairo', '-pdf', OUT, tmp], check=True)  # CUPS uyumu (RULES.md)
    os.replace(tmp, OUT)
    print('OK', OUT)


build()
