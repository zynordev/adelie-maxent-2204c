# GBIF temizlik raporu (otomatik — `temizle.py`)

- İndirme: GBIF.org (2026-10-19) GBIF Occurrence Download https://doi.org/10.15468/dl.jt3gt7
- Sorgu: `sorgu.json` · Ham dosya: `ham/0034792-260928105237408.zip`

| Adım | Kalan kayıt | Değişiklik |
|---|---|---|
| GBIF indirmesi (ham) | 1001 |  |
| 1. Çalışma alanı | 1001 | −0: ERA5 katmanlarının dışında |
| 2. Koordinat belirsizliği | 905 | −96: belirsizlik > 10 km |
| 3. Bölgesel konum | 861 | −44: konum adı yalnızca bölge (gözlem yeri değil) |
| 4. Yer tutucu koordinat | 861 | −0: belirsizlik yok ve koordinatlar 0.5°'nin tam katı |
| 5. Tekrar kayıt | 704 | −157: aynı koordinat + aynı tarih |
| 6. Seyreltme (MaxEnt dosyası) | 67 | ERA5 hücresi başına 1 nokta |

**MaxEnt dosyası:** `adelie_maxent.csv` — 67 nokta (19 kara, 48 deniz hücresinde; kara/deniz ayrımı ERA5 kara–deniz maskesine göre).

## Seyreltme öncesi temiz kayıtların dağılımı

| Veri seti (datasetKey) | Kayıt |
|---|---|
| `50c9509d-22c7-4a22-a47d-8c48425ef4a7` | 297 |
| `4fa7b334-ce0d-4e88-aaae-2e0c138d049e` | 282 |
| `8ff9e5d1-cc0e-4f3a-90c2-274039353f84` | 69 |
| `f7c30fac-cf80-471f-8343-4ec5d8594661` | 35 |
| `8a863029-f435-446a-821e-275f4f641165` | 12 |
| `6ff8b3b0-ef0f-4f79-a310-5a5615c6aa0b` | 8 |
| `6ddba1a7-e34d-41ae-a14b-017e3c565c87` | 1 |

| basisOfRecord | Kayıt |
|---|---|
| HUMAN_OBSERVATION | 634 |
| MATERIAL_CITATION | 69 |
| MACHINE_OBSERVATION | 1 |

Yıl aralığı: 2000–2026 · Belirsizliği bilinmeyen kayıt: 423 (tutuldu; GBIF'te çoğu kaynak bu alanı doldurmuyor).
