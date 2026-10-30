# Aşamalar

**Durumlar:** ⬜ Başlamadı · 🟡 Devam ediyor · ⏸️ Bekliyor · ✅ Tamamlandı

| # | Aşama | Sorumlu | Durum | Not |
|---|---|---|---|---|
| 0 | Proje kurulumu ve kayıt sistemi | Öğrenci + Claude | ✅ | 2026-10-19 |
| 1 | Danışmana ERA5 yaklaşımını onaylatmak | Öğrenci | ⏸️ | K-009 onay bekliyor |
| 2 | CDS hesabı, lisans onayları, API anahtarı | Öğrenci | ✅ | 2026-10-19; anahtar `~/.cdsapirc` (izin 600) |
| 3 | ERA5 iklim katmanlarının üretimi (19 Bio + 5 denizel) | Claude (öğrencinin isteğiyle) | ✅ | 2026-10-20 01:53; 24 katman `era5/output/`, tüm doğrulamalar geçti (README orada) |
| 4 | GBIF kayıtlarının indirilmesi ve temizlenmesi (2000–2026) | Öğrenci | 🟡 | 2026-10-19 indirildi (1001 kayıt, DOI 10.15468/dl.jt3gt7, K-017); öğrencinin isteğiyle temizlendi → 67 nokta `gbif/temiz/adelie_maxent.csv` (K-018, gözden geçirme bekliyor) |
| 5 | Korelasyon matrisine göre değişken seçimi | Öğrenci + Danışman | 🟡 | Öğrenci seçimi K-020: kaya, bio18, sst_yillik, buz_yillik (sıcaklık yok) → danışman onayı. Girdiler `maxent/girdi/` |
| 6 | MaxEnt çalıştırma (AUC, jackknife, katkı tabloları) | Öğrenci | ✅ | 2026-10-20 deneme3 (10 katlı ÇD + jackknife): Test AUC **0.768 ± 0.111** (hedef > 0.70 ✔) — `maxent/cikti/deneme3/NOT.md` |
| 7 | Haritanın QGIS'te görselleştirilmesi, danışmana iletim | Öğrenci | ✅ | 2026-10-31: 300 DPI nihai harita (`harita_final_A4.pdf/.png`), EPSG:4326 koordinat ızgarası, 5 sınıflı lejant ve parametre bilgi kutusu tamamlandı |
| 8 | Rapor (Özet → Amaç → Giriş → Yöntem → Bulgular → Sonuç ve Tartışma → Öneriler → Kaynaklar) | Öğrenci | ⬜ | Sınırlılıklar şeffaf yazılacak |

## Açık sorular

Güncel liste `CLAUDE.md` Bölüm 8'dedir.
