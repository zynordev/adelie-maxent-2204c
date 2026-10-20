# deneme2 — 2026-10-20 (öğrenci, laptop, MaxEnt 3.4.4, Java 21)

- Ayarlar: 10 katlı çapraz doğrulama (replicates=10, crossvalidate), response curves, pictures. **Jackknife işaretlenmemiş** (`maxent.log` → "Command line to repeat"'te `jackknife` yok).
- Katman klasörü olarak `girdi/katmanlar/maxent.cache` seçilmiş (MaxEnt'in aynı katmanlardan ürettiği önbellek; veri aynı).
- Noktalar: yeni `adelie_maxent.csv` (67) → her katta 60–61 eğitim, 6–7 test.
- **Sonuç: ortalama Test AUC 0.768 ± 0.111** (MaxEnt raporu; katlar arası 0.518–0.916, 10 katın 2'si < 0.70) · ortalama Training AUC 0.838.
- Ortalama katkı: buz_yillik 43.1 · kaya 30.0 · bio18 13.9 · sst_yillik 12.9 · permütasyon önemi: buz_yillik 55.6 · sst_yillik 18.3 · bio18 17.1 · kaya 9.1.
- Tepki eğrileri: sst_yillik ≈ −1.9 °C'de tepe yapıp iki yöne düşüyor; buz_yillik arttıkça uygunluk azalıyor.
