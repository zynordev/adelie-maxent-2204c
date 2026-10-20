# deneme3 — 2026-10-20 · RAPORDA KULLANILACAK ÇALIŞTIRMA

- Ayarlar: 10 katlı çapraz doğrulama, response curves, pictures, **jackknife** (MaxEnt 3.4.4, Java 21, laptop).
- Katman klasörü olarak yine `girdi/katmanlar/maxent.cache` seçilmiş (aynı 4 katmanın MaxEnt önbelleği; veri aynı).
- Sonuçlar deneme2 ile birebir aynı (varsayılan rastgele tohum → aynı katlar → tekrarlanabilir).

| | Değer |
|---|---|
| Ortalama Test AUC | **0.768 ± 0.111** (MaxEnt raporu) |
| Ortalama Training AUC | 0.838 |
| Eğitim / test noktası (kat başına) | 60.3 / 6.7 |

| Değişken | Katkı % | Permütasyon % | Tek başına eğitim kazancı | Çıkarılınca eğitim kazancı | Tek başına test AUC | Çıkarılınca test AUC |
|---|---|---|---|---|---|---|
| buz_yillik | 43.1 | 55.6 | 0.210 | 0.441 | 0.657 | 0.753 |
| kaya | 30.0 | 9.1 | 0.139 | 0.530 | 0.612 | 0.772 |
| bio18 | 13.9 | 17.1 | 0.287 | 0.533 | 0.732 | 0.752 |
| sst_yillik | 12.9 | 18.3 | 0.058 | 0.483 | 0.612 | 0.752 |
| *Tümü* | | | *0.592* | | *0.768* | |

Ortalama uygunluk haritası: `Pygoscelis_adeliae_avg.asc` (QGIS'e girecek dosya).
