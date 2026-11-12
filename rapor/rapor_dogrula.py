"""Verify report tables against saved analysis evidence; never run a model.

Run with the Codex bundled Python, after render QA and PDF promotion.
"""
import csv
import hashlib
import json
from pathlib import Path
import re

from docx import Document
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'rapor/TUBITAK_2204C_PROJE_RAPORU'


def rows(path):
    with path.open(newline='') as stream:
        return list(csv.DictReader(stream))


def number(text):
    return float(text.replace(',', '.'))


def main():
    source = BASE.with_suffix('.md').read_text()
    doc = Document(BASE.with_suffix('.docx'))
    pdf = PdfReader(BASE.with_suffix('.pdf'))
    blocks = re.findall(r'(?:^\|.*\n)+', source, flags=re.M)
    tables = []
    for block in blocks:
        table = [[cell.strip() for cell in line.strip('|').split('|')]
                 for line in block.strip().splitlines()]
        tables.append([row for row in table
                       if not all(re.fullmatch(r'[-: ]+', cell) for cell in row)])
    assert len(tables) == len(doc.tables) == 5
    for expected, actual in zip(tables, doc.tables):
        assert expected == [[cell.text for cell in row.cells] for row in actual.rows]

    # Every non-table/non-image Markdown paragraph survives authoring unchanged.
    word_paragraphs = [p.text for p in doc.paragraphs]
    for line in source.splitlines():
        if not line or line.startswith(('|', '![')):
            continue
        line = re.sub(r'^#{1,2} ', '', line)
        line = line.replace('**Proje adı:** ', '')
        line = re.sub(r'\*\*(.*?)\*\*|\*([^*]+)\*|`([^`]+)`',
                      lambda m: next(g for g in m.groups() if g is not None), line)
        assert line in word_paragraphs, line

    checked = 0
    variables = ['bio18', 'buz_yillik', 'kaya', 'sst_yillik']
    domains = ['rectangle', 'coastal_support', 'marine_support']
    vif = rows(ROOT / 'maxent/cikti/revizyon_20261112/denetim_v2/vif.csv')
    for table_row, variable in zip(tables[1][1:], variables):
        for cell, domain in zip(table_row[1:], domains):
            value = next(r['vif'] for r in vif
                         if r['domain'] == domain and r['variable'] == variable)
            assert abs(number(cell) - float(value)) <= .0005001
            checked += 1

    summary = rows(ROOT / 'maxent/cikti/revizyon_20261112/comparison_v3/summary.csv')
    schemes = ['latitude', 'longitude', 'checker_40km_shift0',
               'checker_40km_shift0.5', 'checker_80km_shift0', 'checker_80km_shift0.5']
    candidates = ['L_RM1', 'LQ_RM1', 'LQ_RM2', 'LQH_RM1', 'LQH_RM2']
    for table_row, scheme in zip(tables[2][1:], schemes):
        for cell, candidate in zip(table_row[1:], candidates + ['distance_null']):
            value = next(r['auc_mean'] for r in summary if r['predictors'] == 'annual'
                         and r['scheme'] == scheme and r['candidate'] == candidate)
            assert abs(number(cell) - float(value)) <= .0005001
            checked += 1
    assert all(float(r['auc_minus_distance_null']) < 0 for r in summary
               if r['candidate'] in candidates)

    for column, model in enumerate(['IPSL', 'GFDL', 'MPI'], start=1):
        metrics = rows(ROOT / f'maxent/cikti/revizyon_20261112/projection_{model}/model_metrics.csv')
        for table_row, candidate in zip(tables[3][1:], candidates):
            value = next(r['delta_mean_presence_resubstitution'] for r in metrics
                         if r['predictors'] == 'annual' and r['candidate'] == candidate)
            assert abs(number(table_row[column]) - float(value)) <= .0005001
            checked += 1
        ice = json.loads((ROOT / f'maxent/girdi/revizyon_{model}_20261112_v2/ice_baseline_comparison.json').read_text())
        table_row = tables[4][column]
        for cell, key in zip(table_row[1:], ['mean_bias_percentage_points', 'rmse_percentage_points']):
            assert abs(number(cell) - ice[key]) <= .005001
            checked += 1

    pdf_text = re.sub(r'\s+', ' ', '\n'.join(page.extract_text() for page in pdf.pages))
    for token in ['Analiz durumu', 'Tamamlanması beklenen sonuçlar', 'Kaynaklar', '42209243']:
        assert token in pdf_text, token
    for token in ['%42.2', '%42,2', '89.155', '202603.028', '\\text{', '\\frac{']:
        assert token not in source and token not in pdf_text, token
    assert len(doc.inline_shapes) == 2
    assert len(pdf.pages) == 10
    build = json.loads(BASE.with_suffix('.build.json').read_text())
    hashes = {ext: hashlib.sha256(BASE.with_suffix('.' + ext).read_bytes()).hexdigest()
              for ext in ['md', 'docx', 'pdf']}
    assert hashes['md'] == build['markdown_sha256']
    assert hashes['docx'] == build['docx_sha256']
    result = {'date': '2026-11-12', 'status': 'passed', 'numeric_cells_checked': checked,
              'tables': 5, 'figures': 2, 'pdf_pages': 10,
              'visual_qa': 'all 10 pages reviewed from v2 render',
              'sha256': hashes, 'scientific_status': 'colony results pending; not final'}
    BASE.with_suffix('.verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
