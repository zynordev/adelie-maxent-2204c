# Proje raporu çalışma iskeleti ve kanıt tablosu

Bu dosya öğrencinin yazacağı rapor için teknik iskelettir; tamamlanmış araştırma raporu veya danışman onaylı sonuç değildir. Eski taslağın bulunduğu varsayılmaz. Güncel TÜBİTAK çağrı formatı, sayfa/kelime sınırları ve AI kullanım beyanı teslimden önce resmi kaynaktan kontrol edilmelidir.

## Özet

Araştırma sorusu, veri ve gerçek test tasarımı netleşince yazılacak. “2050'de %54,6 habitat kaybı” mevcut kanıtlarla özet bulgusu olarak kullanılamaz.

## Amaç

Marguerite Körfezi'nde Adélie pengueni bulunuşlarının çevresel uygunlukla ilişkisini değerlendirmek. Koloni/üreme odağı kararlaştırılırsa kayıt türü ve amaç birlikte değiştirilmeli.

## Giriş

Yerel bağlam, türün karasal/denizel yaşam döngüsü, önceki Adélie modelleme çalışmaları ve araştırma boşluğu. “İlk Adélie MaxEnt çalışması” iddiası kullanılmamalı; Cimino vd. 2016 zaten var. Nedensel kril/nüfus kaybı hipotezi veriyle test edilmediyse sonuç gibi yazılmamalı.

## Yöntem

1. Çalışma alanı, kayıt dönemi ve kalibrasyon alanının gerekçesi.
2. GBIF DOI, sorgu ve temizlik kuralları; 1001 ham → 704 temiz → 67 hücre temsilcisi.
3. ERA5 verileri, birimler, 2000-2025 aylık normalleri ve kaya kaynağı.
4. Korelasyon, değişken seçimi, kaba ızgara ve kara hücresi doldurma varsayımı.
5. MaxEnt sürümü, özellikler, regularization, arka plan, eğitim/test ayırma ve kayıtlı komutlar.
6. Rastgele ve mekânsal değerlendirme farkı; presence-background AUC ve eğitimden türetilen omission eşiği.
7. Gerçek gelecek veri zinciri tamamlanırsa model/üye/SSP/dönem ve dönüştürmeler; varsayımsal deneme ayrı alt bölüm.
8. Sürekli uygunluk farkı, WGS84 alan hesabı, eşik duyarlılığı ve belirsizlik.
9. Harita projeksiyonu; gösterim enterpolasyonu ile gerçek çözünürlük ayrımı.

## Bulgular için kanıt tablosu

| İfade | Kanıt | Kullanım sınırı |
|---|---|---|
| 67 temsilci orijinal CSV ile aynı | `gbif/temiz/kalite_20261108/manifest.json` ve temsilci metadata tablosu | Ham indirmedeki bütün sütunların kurtarıldığı iddia edilmez |
| 67 temsilcinin 36'sında belirsizlik eksik | Aynı klasör `summary.json` | 704 kaydın 423 eksikliğiyle karıştırılmaz |
| Eski 10 kat ortalama AUC 0,76766 | `deneme3/maxentResults.csv`, mekânsal denetim belgesi | Kat SD'si güven aralığı değil; gelecek tahminini doğrulamaz |
| Mekânsal testler zayıf aktarım gösteriyor | `docs/MEKANSAL_DOGRULAMA_2026-11-08.md` ve kaydedilmiş metrikler | Kat tasarımı/ayar farkları belirtilmeli; yalnız düşüşten neden çıkarılmaz |
| Varsayımsal denemede 384/186/133 hücre | `maxent/cikti/duyarlilik_analizi_v1/ozet.json` | Uygunluk azalma/kararlı/artış sayıları; habitat alanı kaybı değil |
| 386 hücrede novelty uyarısı | Aynı analiz ve kaynak kat rasterları | Eğitim aralığı dışı tahmin; biyolojik yokluk değil |
| 260 hücrede değişim yönü katlar arasında değişiyor | Eşlenik kat farkları ve `isaret_belirsiz.asc` | İklim modelleri arası belirsizlik değil |
| Görsel kalite düzeltildi | `harita/duzeltilmis_v1/` PNG/PDF/QGIS projeleri | Yumuşatma gerçek iklim çözünürlüğünü artırmadı |

## Sonuç ve tartışma

Başarıyı yalnız AUC>0,70 eşiğine bağlama. Coğrafi aktarım, örnekleme kaynağı/çabası, kayıt türü, koordinat belirsizliği, kara/deniz karışımı, kaba çözünürlük, iklim dönemi ve ekstrapolasyonu tartış. Puan artışı “iklim sığınağı”, yüksek puan “aktif koloni” olarak doğrulanmış sayılmaz.

## Öneriler ve kaynaklar

Bağımsız/koloni doğrulanmış kayıtlar, ekolojik alan tanımı, uygun ölçek ve gerçek iklim projeksiyonu belirsizliği. Kaynakçayı `docs/literatur/`, veri DOI'leri ve yeni CMIP manifestlerinden oluştur. Danışmanla nihai yorum ve kapsamı kararlaştır.
