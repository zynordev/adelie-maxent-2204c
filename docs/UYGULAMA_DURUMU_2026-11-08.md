# Uygulama sonucu ve kalan bilimsel işler

2026-11-08. Kullanıcının “Tamam başla” talebiyle analiz planının teknik iş paketleri uygulandı. **Bütün araştırmanın nihai doğrulandığı iddia edilmiyor.** Eski kaynaklar ve çıktılar korundu; yeni commit/push yapılmadı.

## Tamamlananlar

1. Başlangıç envanteri ve hash'leri: `docs/arsiv_20261108/baslangic_manifest.json`. Son kontrolde hiçbir özgün veri/model/harita dosyası değişmedi.
2. Varsayımsal sabit delta denemesi gerçek CMIP6 işinden ayrıldı; scenario metadata ve doğrulama korumaları eklendi. Eski betikler yanlış CMIP6 haritasını yeniden üretmek yerine doğru etiketli ortak harita üreticisini çağırıyor.
3. Gelecek/günümüz ızgara uyumu, boyut, NoData/NaN/Inf ve senaryo dönüşümü doğrulanıyor. Hücre payı, WGS84 model-alanı payı ve eşik duyarlılığı ayrı çıktı.
4. Eşlenik kat farkı, işaret uyuşmazlığı, novelty/aralık uyarısı ve clamping analizleri üretildi.
5. Dört temiz harita düzeni: günümüz, gelecek/deneme, değişim, belirsizlik. Lejant, istasyon alanı, katman sırası, kaynaklar ve yanlış biyolojik etiketler düzeltildi. Ayrı QGIS projeleri kullanılıyor. Sürekli harita isteğe bağlı bilinear gösterilir; sınıf/istatistik yumuşatılmaz.
6. Mevcut 67 temsilci aynı koordinatlarla tam mevcut metadata'sına bağlandı. 36/67 koordinat belirsizliği eksik; 62/67 DJF. Kayıtlar otomatik elenmedi.
7. Dört coğrafi bandın atamaları ve karşılaştırma tasarımı üretildi. Üç kısıtlı aday + otomatik özellikli aday için gerçek Java MaxEnt çalıştırıldı; aynı ayarlı random4 karşılaştırması yapıldı. Sonuçlar, komutlar, tohum, sürümler ve hash'ler kayıtlı.
8. Gerçek IPSL-CM6A-LR / r1i1p1f1 SSP245 bölgesel aylık veri indirildi: 2000-2025 referans, 2041-2060 gelecek; tas/pr/tos/siconc. Birim/takvim/dönem kontrolleri ve kaynak manifestleri mevcut.
9. Gerçek kaynaklı dört gelecek ASC üretildi. Aylık delta/yağış oranı kullanıldı; BIO18 geleceğin en sıcak çeyreğinden yeniden hesaplandı (29 hücrede çeyrek değişti).
10. Kayıtlı on MaxEnt kat modeli yeniden eğitilmeden gerçek girdilere aktarıldı. Kontrol projeksiyonları eski iki fold0 rasterına karşı sıfır fark verdi. Yeni 2050/değişim/belirsizlik haritaları üretildi.
11. **17 birim testi geçti**, ayrıca 19 biyoklimatik değişken testi geçti. Gerçek dört PDF A4/tek sayfa olarak doğrulandı, PNG'ler ve PDF'den render edilen sayfalar görsel olarak kontrol edildi.
12. Rapor iskeleti ve iddia→kanıt tablosu hazır; güncel resmî sitede erişilen 2026 rehberi ile 2027 çağrı belirsizliği ayrı kaydedildi. Bilgi bankası ve proje kayıtları güncellendi.

## En önemli sonuç: yeni harita, güçlü model demek değil

Eşit ayar/eğitim boyutu/arka plan altında:

| Aday | Coğrafi4 AUC | Rastgele4 AUC |
|---|---:|---:|
| L/RM1 | 0,57962 | 0,71545 |
| LQ/RM1 | 0,52985 | 0,74562 |
| LQ/RM2 | 0,55710 | 0,72046 |
| AUTO/RM1 | 0,47742 | 0,76543 |

Eski rastgele10 AUC 0,76766 korunuyor; bu geleceğe/coğrafyaya aktarım güvencesi değil. Bu dört-band tasarımında modeller uzak bölgelere zayıf aktarılıyor. Bir model “kazandı” veya bağımsız optimum bulundu denmedi. Tohum/katları sonuç güzel görünsün diye değiştirme yapılmadı; kaynaklar sabit ve tekrar edilebilir.

Gerçek CMIP6 denemesinde 357/703 hücrede prediktör aralık uyarısı, 246/703 hücrede katlar arası değişim yönü uyuşmazlığı var. Bu deneme tek-GCM ve zayıf aktarım performanslı eski modelin projeksiyonudur. “2050'de şu kadar habitat kaybolacak” sonucuna dönüştürülemez.

## Plan durum tablosu

| Paket | Durum | Kalan |
|---|---|---|
| A-P1 kaynakları koruma/etiket | Tamam | Eski kök haritalar arşiv, raporda kullanılmayacak |
| A-P2 veri/dönem seçimi | Teknik başlangıç seçimi kayıtlı | Nihai hedef/ölçek/M için öğrenci-danışman kararı |
| A-P3 gerçek gelecek girdileri | Tek GCM/üye/SSP için tamam | GFDL/diğer SSP ensemble üretimi yapılmadı |
| A-P4 yerleşim onarımı | Tamam | Kaynak çözünürlüğü değişmedi |
| A-P5 projeksiyon | Eski modele keşif amaçlı aktarım tamam | Güvenilir nihai günümüz modelinin seçimi eksik |
| A-P6 değişim/belirsizlik | Teknik hesaplar tamam | Habitat alanı için M ve uygunluk eşiği gerekçesi yok |
| A-P7 harita paketi | Tamam, deneysel etiketiyle | Nihai bilimsel rapora hazır sonuç sayılmaz |
| B-P1 araştırma hedefi | Geçici genel bulunuş korundu | Kullanıcı/danışman nihai hedefi netleştirecek |
| B-P2 kalite/envanter/ortam | Mevcut veri için teknik tamam | Ham dosyada olup temiz CSV'de olmayan alanlar ve bağımsız doğrulama eksik |
| B-P3 mekânsal tasarım | Karşılaştırmalı tasarım tamam | Ekolojik M ve bağımsız gözlem çabası verisi eksik |
| B-P4 model değerlendirme | Sorun gösterildi, nihai seçim yapılmadı | Model hedefi/veri/alan iyileştirmesi gerekiyor |
| B-P5 kayıt/yorum | Yeni sonuçlar tutarlı kaydedildi | Nihai bilimsel yorum öğrenci-danışmanla |
| B-P6 rapor | İskelet/kanıt tablosu hazır | Öğrencinin raporu, yeni çağrı formatı ve nihai sonuçlar |

## Sonraki bilimsel çalışma

Genel bulunuş hedefinde kalınırsa kayıt kaynağı ve koordinat kalitesi duyarlılıkları, mevsimsellik ve erişilebilir alan tasarımı ele alınmalı. Koloni habitatı hedeflenirse öncelik doğrulanmış koloni/üreme kayıtlarıdır; mevcut deniz kayıtlarını kaba ERA5 maskesiyle otomatik atmak çözüm değil. Bu ayrım araştırmanın anlamını değiştirdiği için kullanıcı/danışman seçimi gerekir.

Target-group background veya bağımsız doğrulama verisi varmış gibi üretilmedi. Habitat kaybı alanı, uygunluk eşiği keyfî seçilerek hesaplanmadı. İkinci GCM/SSP veya yüksek çözünürlüklü yeni iklim bilgisi tamamlanmış sayılmadı. Gerekli bilimsel kararlar alındıktan sonra bu kayıt üzerinden devam edilecek.

## Kullanım

- Yöntem: `docs/CMIP6_DELTA_VE_PROJEKSIYON_2026-11-08.md`.
- Değerlendirme: `docs/MEKANSAL_DOGRULAMA_2026-11-08.md`.
- Yeni haritalar: `harita/cmip6_ipsl_2050_v1/`.
- Sayısal analiz: `maxent/cikti/cmip6_ipsl_ssp245_2041_2060_v1/ozet.json`.
- Kalite: `gbif/temiz/kalite_20261108/`.
- Test: `python -m unittest discover -s maxent -p 'test_*.py' -v` ve `python era5/test_biovars.py`.

Orijinal araştırma planı tarihsel doküman olarak değiştirilmeden korunur. Bu durum dosyası uygulamanın güncel kaydıdır.
