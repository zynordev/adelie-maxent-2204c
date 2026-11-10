# Aşamalar

**Durumlar:** ⬜ Başlamadı · 🟡 Devam ediyor · ⏸️ Bekliyor · ✅ Tamamlandı

> **2026-11-08 güncellemesi:** [Analiz planı](ANALIZ_VE_COZUM_PLANI_2026-11-08.md) teknik olarak uygulandı; [güncel durum ve kalan işler](UYGULAMA_DURUMU_2026-11-08.md). Gerçek tek-GCM IPSL SSP245 girdileri/deneysel aktarımı hazır, haritalar onarıldı. Coğrafi doğrulama zayıf: nihai bilimsel sonuç henüz hazır değil. Eski 2026-10-31 “habitat kaybı/sığınak” yorumları geçerli sonuç olarak kullanılmayacak; geçmiş günlük kayıtları korunur.

| # | Aşama | Sorumlu | Durum | Not |
|---|---|---|---|---|
| 0 | Proje kurulumu ve kayıt sistemi | Öğrenci + Claude | ✅ | 2026-10-19 |
| 1 | Danışmana ERA5 yaklaşımını onaylatmak | Öğrenci | ⏸️ | K-009 onay bekliyor |
| 2 | CDS hesabı, lisans onayları, API anahtarı | Öğrenci | ✅ | 2026-10-19; anahtar `~/.cdsapirc` (izin 600) |
| 3 | ERA5 iklim katmanlarının üretimi (19 Bio + 5 denizel) | Claude (öğrencinin isteğiyle) | ✅ | 2026-10-20 01:53; 24 katman `era5/output/`, tüm doğrulamalar geçti (README orada) |
| 4 | GBIF kayıtlarının indirilmesi ve temizlenmesi (2000–2026) | Öğrenci | 🟡 | 2026-10-19 indirildi (1001 kayıt, DOI 10.15468/dl.jt3gt7, K-017); öğrencinin isteğiyle temizlendi → 67 nokta `gbif/temiz/adelie_maxent.csv` (K-018, gözden geçirme bekliyor) |
| 5 | Korelasyon matrisine göre değişken seçimi | Öğrenci + Danışman | 🟡 | Öğrenci seçimi K-020: kaya, bio18, sst_yillik, buz_yillik (sıcaklık yok) → danışman onayı. Girdiler `maxent/girdi/` |
| 6 | MaxEnt çalıştırma ve coğrafi değerlendirme | Öğrenci + teknik destek | 🟡 | Rastgele10 AUC 0,768; eşit ayarlı AUTO random4 0,765 / coğrafi4 0,477. Nihai model kabul edilmedi; veri/alan tasarımı güçlendirilecek |
| 7 | QGIS görselleştirme ve danışmana iletim | Öğrenci + teknik destek | 🟡 | Düzen/etiket/katman onarımı tamam; 300 DPI PNG/PDF kontrol edildi. Yeni `harita/cmip6_ipsl_2050_v1/`; bilimsel yorum ve danışmana iletim ayrı |
| 7.1 | Gerçek CMIP6 SSP245 2041-2060 ve değişim | Öğrenci + teknik destek | 🟡 | IPSL r1i1p1f1 aylık veri→delta ASC→kayıtlı model aktarımı tamam; tek-GCM deneysel. Nihai habitat kaybı/sığınak sonucu değil |
| 8 | Rapor (Özet → Amaç → Giriş → Yöntem → Bulgular → Sonuç ve Tartışma → Öneriler → Kaynaklar) | Öğrenci + Danışman | ✅ | 2026-11-10; Danışman referansına uygun 18 sayfalık resmî rapor hem MD (`rapor/TUBITAK_2204C_PROJE_RAPORU.md`) hem de Cairo PDF (`rapor/TUBITAK_2204C_PROJE_RAPORU.pdf`) olarak hazırlandı. |

## Açık sorular

Güncel liste `CLAUDE.md` Bölüm 8'dedir.
