# Bilimsel revizyon — 2026-11-12

Durum: uygulama sürüyor; nihai rapor veya doğrulanmış 2050 habitat kaybı sonucu değil.

## Tamamlanan kaynak ve eski model denetimi

- AUTO HTML kayıtlarında gerçek özellikler **LQH**, LQTH değil.
- SST yeniden indirilen resmi CDS kaynağında paramId 34, Kelvin. Yerel yıllık kaynak minimumu yaklaşık −2,422 °C; kaynakta fiziksel uç değer var. Neden çözülmeden SST ana koloni modeline alınmayacak; ayrıca duyarlılık kolunda incelenecek.
- Kuzeyde eski artış bloğundaki 24 hücrenin tamamı eğitim değişken aralığı dışında. Eski tüm 243 artış hücresinin 59'u bu durumda, 22'sinde eğitilmiş model katlarının delta yönü uyuşmuyor. 246 hücreye ait eski maske iklim değişkenleri değil **eğitilmiş katlar arası yön** uyuşmazlığıdır.
- VIF gerçek tabloları `denetim_v2/vif.csv` ve eğitim-katı tablolarında. Destek alanına göre değişir; denizel destekte buz/SST yaklaşık 5,64/5,25.
- Temiz GBIF'in 163 kaydı 2026'dan; 2000–2025 dönemli denetimde bunlar çıkarıldı, geçerli kıyı desteğinde 61 varlık hücresi kaldı.
- Özgün tam dikdörtgenin WGS84 jeodezik alanı 202681,637 km². Ortalama hücre alanını yuvarlayıp çarpmak doğru düzeltme değildir. Izgara alanı koloni alanı değildir.

## Gerçekten çalıştırılan karşılaştırmalar

- İki değişken seti × beş açık L/LQ/LQH ve RM ayarı × altı mekânsal şema × dört kat = 240 eğitim (`comparison_v3`). Kat ayrımında test bölgesi arka planı da eğitimden çıkarılır; varlık hücreleri arka planda korunur.
- Her şemada uzaklık null ve koordinat referansı; AUC, P10 omission, sabit on kutulu Boyce ve tanımı açık kısmi ROC. Dört katın yeniden örnekleme aralığı gerçek bağımsız tekrarlı veri güven aralığı değildir. Aday ayarlar test başarısına bakılmadan sabitlenmiştir; testte kazanan seçilmemiştir.
- Bu **eski genel bulunuş** tasarımında hiçbir çevresel aday hiçbir şemada uzaklık null ortalamasını geçmedi. Bu, yeni koloni tasarımı için önceden verilmiş bir sonuç değildir.
- IPSL-CM6A-LR, GFDL-ESM4, MPI-ESM1-2-LR, SSP245 2041–2060; referans historical 2000–2014 + SSP245 2015–2025 olarak eşlendi. Tek üye/model; çoklu üye belirsizliği çözülmüş değil. Dosya parçalarının hem zamanı hem verisi birlikte sıralanır; eksik/tekrar ay kontrol edilir.
- Üç GCM için 30 tam model aktarımı ve 720 kat-dışı gelecek aktarımı, clamping açık/kapalı, MESS, yalnız buz/SST/yağış değişimi denemeleri. Kat-dışı günümüz noktası kullanmak gözlenmemiş geleceği doğrulamak değildir.
- Örnek IPSL yıllık sette varlık hücrelerindeki tam-model ortalama delta L/RM1 ile +0,115, LQH/RM1 ile −0,318: yön bile yapı bağımlı. Bu fark ekolojik değişimin kanıtı değil, model bağımlılığıdır.

## Kullanıcının onayladığı yeni koloni tasarımı

MAPPPD v5.0 pozitif yuva sayımları 2000–2025 yerelde 19 yerleşim/14 ızgara hücresi verir. Kullanıcı daha geniş eğitim, Marguerite odaklı raporlama seçti. Daha geniş zarf NWSE = [-60, -78, -74, -53]; tüm zarf M değildir.

1. Aynı sürüm SCAR ADD v7.11 kaya/kıyı vektörleriyle hücre içi kaya ve şelf alanı yeniden hesaplanır. Geniş ERA5 aylık kaynağı ayrı indirilir.
2. Kayalık kıyı desteği ve bütün Pygoscelis pozitif yuva sayımı hücrelerinden hedef-grup desteği karşılaştırılır. Gerçek yokluk varsayılmaz. Kaynakta şelf/kaya/sayım çelişkileri dışlama tablosuna yazılır.
3. Ana aday seti kaya + Kasım–Mart buzu + Haziran–Ağustos buzu. SST ayrı QC-işaretli duyarlılık seti; BIO18 ile hipotermi mekanizması iddiası çıkarılır. Günlük buz ilerleme/çekilme tarihleri aylık veriden türetilmez.
4. Geniş eğitimde bölgesel/şemalar arası doğrulama, null modeller, özellik/RM ve arka plan duyarlılığı tekrar çalıştırılır. Marguerite haritaları aynı kaynak/ızgaradan üretilir.

## Açık işler ve rapora geçiş koşulu

- Geniş ERA5 ve günlük kaynak CDS işlerinin tamamlanması; günlük 00 UTC fenoloji tanımı ve sansürlenen olaylar açık kaydedilecek.
- Yeni koloni modelinin eğitilmesi, üç GCM aktarımı ve bölgesel belirsizlik şekilleri.
- GCM'nin bölgesel buz performansı; kril/batimetri yokluğu, SST uç değerlerinin kaynağı henüz çözülmedi. Üç GCM indirmek bunları otomatik çözmez.
- Kaynak DOI/ayar/komut/ortam manifesti ve bağımsız yeniden çalıştırma kontrolü.
- Ancak bundan sonra özgün raporun yöntem-bulgu-sonuç/şekil ve sayıları birlikte değiştirilecek. Jackknife mavi=tek değişken, turkuaz=çıkarılınca; en azından eski şeklin metni de buna uymalı. Eski %42,2 doğrulanmış habitat kaybı olarak geri konmayacak.

Kaynak erişimleri: [MAPPPD](https://penguinmap.com/mapppd/), [ERA5 aylık](https://doi.org/10.24381/cds.f17050d7), [SCAR kaya v7.11](https://doi.org/10.5285/815525ca-cefe-4fbf-9224-3ee784e7de4e), [coğrafi null gerekçesi](https://doi.org/10.1890/11-0826.1).

## Geniş alan uygulaması ve yeniden çalıştırma

SCAR geometrisi 57 × 101 hücrede gerçekten hesaplandı: `maxent/girdi/koloni_geometry_20261112/`. İklim yer tutucusu üretilmedi. Deniz verisi uzaklık filtresi öncesinde 957 kayalık kıyı hücresi, 85 Adélie yerleşimi/51 varlık hücresi ve 111 Pygoscelis hedef-grup hücresi var; bir Adélie yerleşimi kaya/şelf filtresine takılıyor. Bunlar son eğitim sayısı değil. Zarf doğu kıyısını da kapsar; geniş zarf deneyi **Batı Yarımada'ya özgü nihai ekolojik M olarak sunulmayacak**. Marguerite odaklı aktarım öncesi bölgesel kapsam/sınır duyarlılığı ayrıca değerlendirilmeli.

Geniş alan üç GCM'nin dört değişkeni, kaynak kimliği ve ay kapsamı doğrulanarak indirildi. `koloni_gelecek.py` yeni koloni değişkenlerini gerçekten bu kaynaklardan üretecek; eski yerel atmosfer ızgarasını geniş alana kopyalamaz. Üreme dönemi Kasım–Mart, kış Haziran–Ağustos aritmetik aylık ortalamaları. Kaya sabit; yeni buzsuz arazi veya besin miktarı tahmini yok.

`koloni_calistir.py` için bir saatlik, mevcut indirmeyi bekleyen çalışma başlatıldı. Yeni CDS işi göndermiyor; indirme tamamlandı makbuzu ve SHA256 olmadan modele geçmiyor. Sonra iki arka plan için CV, üç GCM'de açık/kapalı clamping, MESS, yalnız buz/SST değişimi ve kat-dışı delta aşamalarını çalıştırıyor. Her aşamanın komutu/durumu ayrı kayıtlı; kısmi dosyalar sessizce ezilmez. Bir saat sonunda kaynak hâlâ gelmediyse `waiting_for_existing_CDS_job` durumuyla çıkar; aşağıdaki komutla devam edilir. Bu süreç raporu kendiliğinden nihai ilan etmez.

Linux kök diskte yaklaşık 1,7 GB boş alan kaldığı için büyük **yeni** analiz çıktıları ortak belgeler diskine yönlendirildi (yaklaşık 50 GB boş alan); mevcut dosyalar silinmedi/taşınmadı. Kod, Python ortamı ve hesaplama Linux'ta kalıyor.

```bash
cd /home/halil/adelie-maxent-2204c
.venv-cmip/bin/python maxent/koloni_calistir.py \
  --results-root /home/halil/Documents/2204c_revizyon_20261112/analiz \
  --data-root /home/halil/adelie-maxent-2204c/maxent/girdi/koloni_20261112_run \
  --wait-minutes 60
```

Canlı işlem kaydı: `/home/halil/Documents/2204c_revizyon_20261112/analiz/pipeline.json`. ERA5 geniş aylık istek kimliği `fe4b03ad-fe98-4618-91e6-dbd4acc0d7d8`; yerel günlük istek kimliği `533bacce-bcbf-4725-909d-82694dad07b9`. Bunlar kaynak izleme kimlikleridir, kimlik doğrulama anahtarı değildir. Günlük kaynak bağımsız iş; henüz koloni modeline fenoloji girdisi diye eklenmedi.

### Doğrulama

2026-11-12: toplam **28 test geçti** (yeni revizyon 11, mevcut mekânsal 9, delta 3, alan/ızgara 5). İzole ortamda GDAL yok; mevcut delta testinin sistem GDAL paketini kullanması için site-packages en sona eklendi. Sisteme paket kurulmadı.

```bash
.venv-cmip/bin/python - <<'PY'
import sys, unittest
sys.path.append('/usr/lib/python3.14/site-packages')
suite = unittest.defaultTestLoader.discover('maxent', pattern='test_*.py')
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
PY
```

Yerel kaynakla SCAR-geometri yeniden kullanım testi 14 koloni hücresini aynen korudu. Yeni geniş koloni eğitim/projeksiyonu henüz çalışmadığı için 28 sayısal testin geçmesi yeni modelin ekolojik doğrulaması sayılmaz. Kaynak ve paket sürümleri `maxent/revizyon_manifest.py` ile ayrı, zaman damgalı SHA256 manifestine kaydedilir.

Genel CSV/örnek kimliği desteği gerçek Java çalıştırmalarıyla da sınandı: eski 61 GBIF hücresi yalnızca yazılım regresyon testi için yeni `sample_id` yolundan geçirilerek 120 eğitim tekrarlandı. Çevresel+coğrafi 168 değerlendirmede AUC, omission ve eğitim P10 eşiği eski çıktılarla **tam aynı** çıktı (maksimum mutlak fark 0). Bu kohort koloni verisi olarak yeniden etiketlenmedi; test çıktıları yalnız `work/generic_cli_regression_20261112/` altında. Yeni koloni çıktılarında ayrıca yalnız Marguerite varlık hücreleri için delta ortalaması/medyanı ve bölgesel P10 ızgara alanı ayrı yazılacak; geniş eğitim alanının ortalaması yerel sonuç diye sunulmayacak.

### Literatür karşılaştırması için doğrulanmış sınırlar

Ek Java aktarım regresyonu: yeni genel CSV yolundan beş tam model de yeniden eğitildi/aktarıldı (`work/generic_projection_regression_20261112/`). Eski karşılıklarıyla clamping açık/kapalı varlık delta ortalaması ve AIC farkı sıfır. Bu yazılım uyumluluk testidir; yeni koloni modelinin bilimsel doğrulaması değildir.

- Oceanites, Inc. (2026), MAPPPD v5.0; CC BY 4.0. Kaynak web sayfası 5487 sayım/729 yerleşim ve 2025/2026 sezonuna kadar kapsam bildiriyor. Biz sayım yılını 2000–2025 ile kısıtlıyoruz; sayım yılı ve sezon aynı kavram değildir. İndirilen CSV'nin hash'i korunuyor.
- [Gallagher vd. (2025)](https://doi.org/10.1002/ecs2.70091) MaxEnt değil lojistik regresyon, 500 m karasal grid ve ayrı denizel/karasal değişkenler kullanır. Bu nedenle AUC >0,85'i bu çalışmanın farklı arka plan, çözünürlük ve test tasarımıyla doğrudan başarı kıyası yapmak yanlış olur. Bizim 0,25° verimiz koloni ölçeği değildir; ERA5'in yaklaşık 31 km yerel çözünürlüğünden daha yüksek fiziksel bilgi içermez.
