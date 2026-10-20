# MaxEnt girdileri

`girdi/` klasörü MaxEnt'e doğrudan yüklenmeye hazırdır (2026-10-20, K-020 seçimine göre; **danışman onayı bekleniyor**).

| MaxEnt alanı | Dosya |
|---|---|
| **Samples** | `girdi/adelie_maxent.csv` — 67 nokta (`species,longitude,latitude`; `gbif/temizle.py`, K-018) |
| **Environmental layers** (klasör) | `girdi/katmanlar/` — `kaya`, `bio18`, `sst_yillik`, `buz_yillik` (`.asc`, hepsi "Continuous") |

Kontroller (2026-10-20): 4 katmanın başlığı aynı · 67 noktanın tamamı alan içinde · hiçbiri NoData hücresine düşmüyor · aynı hücrede tekrar yok.

Katmanlar `era5/output/`'tan kopyalandı; kaynak ve yöntem için `era5/output/README.md`. Değişken seçimi değişirse bu klasör yeniden oluşturulmalı.
