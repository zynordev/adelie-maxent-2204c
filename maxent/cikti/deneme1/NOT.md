# deneme1 — 2026-10-20 (öğrenci, laptop, MaxEnt 3.4.4, Java 21)

- Ayarlar: response curves, pictures, jackknife; random test %25; diğerleri varsayılan (`maxent.log` → "Command line to repeat").
- Katmanlar: kaya, bio18, sst_yillik, buz_yillik (K-020). Arka plan: 703 hücrenin tamamı.
- **Sonuç: Training AUC 0.819 · Test AUC 0.781 (SD 0.054)** · 50 eğitim + 16 test noktası.
- **Not:** Bu çalıştırma eski `adelie_maxent.csv` ile yapıldı. 66.875°G hücre sınırındaki bir nokta MaxEnt'te kuzey
  hücreye düşüp tekrar sayıldığı için **66 nokta** kullanıldı; o noktanın arkasında kalan bir hücre (66.649°B, 66.879°G)
  modelde temsil edilmedi. `gbif/temizle.py` MaxEnt'in hücre kuralına uyduruldu → yeni dosyada 67 nokta, sınırda nokta yok.
  Sonraki denemeler yeni dosyayla yapılmalı.
