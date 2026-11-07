# Gerçek CMIP6 girdileri ve deneysel MaxEnt aktarımı

Tarih: 2026-11-08. Bu belge **gerçek kaynağı olan tek-GCM denemesini** tanımlar. Modelin bilimsel olarak nihai kabul edildiği anlamına gelmez.

## Veri ve dönem

- GCM: IPSL-CM6A-LR, üye r1i1p1f1, SSP2-4.5.
- Referans: 2000-2025; aynı model/üyenin historical 2000-2014 ve SSP245 2015-2025 devamı.
- Gelecek: 2041-2060 dönem ortalaması; “2050” bu dönem için kısa addır.
- Atmosfer: Amon `tas`, `pr`, gr. Deniz: Omon `tos`, SImon `siconc`, gn.
- Özgün historical sürümü 20180803, SSP245 sürümü 20190119. Özgün ESGF/CEDA dosya kimlikleri, URL'leri ve bildirilen dosya checksum'ları bölgesel veri manifestinde bulunur.
- Yerel NetCDF ve NPZ alt kümeleri gerçekten indirildi; checksum'ları yerelde doğrulandı. Global dosyanın tamamı indirilmiş gibi checksum doğrulama iddiası yok.

Kaynak incelemesi: `docs/CMIP6_ERISIM_2026-11-08.md`.

## Üretilen dizinler

| Dizin | İçerik |
|---|---|
| `maxent/girdi/cmip6_2041_2060/` | Katalog/ESGF envanterleri, bölgesel aylık seriler ve 12 aylık normal |
| `maxent/girdi/cmip6_ipsl_ssp245_2041_2060_v1/` | Dört gerçek kaynaklı gelecek ASC, aylık delta tanıları, scenario/manifest |
| `maxent/cikti/cmip6_ipsl_ssp245_2041_2060_v1/` | Eski on kat modelin yeniden eğitilmeden projeksiyonu, fark ve belirsizlik |
| `harita/cmip6_ipsl_2050_v1/` | Aynı analizden üretilen harita projeleri, PNG/PDF ve yalnız gösterim TIFF'leri |

## Delta yöntemi

Bu, kaynaklı bir basit delta/bias düzeltmesi denemesidir; dinamik küçültme veya ince ölçekli yeni iklim bilgisi değildir.

1. Her kaynak hücre/ay için referansta 26, gelecekte 20 geçerli yıl şartı arandı. Dört NPZ'nin hash'leri indirme manifestiyle doğrulandı.
2. ERA5 hedef hücreleri, küre üzerinde en yakın **tam verili kaynak hücreye** eşlendi. Atmosfer değişiminde 20 farklı native hücre, deniz değişiminde 62 farklı native hücre kullanıldı. GCM kaynaklarının 703 bağımsız hedef hücrelik iklim bilgisi taşıdığı varsayılmadı.
3. Denizel anomaliler önce ERA5'in deniz hücrelerine eşlenir; kara hücresinde mevcut projenin en yakın ERA5 deniz hücresinden doldurma politikası korunur. NaN kara değerleri denize enterpole edilmez.
4. `tas` aylık gelecek−referans farkı ERA5 aylık `tavg` değerlerine eklendi. Tas anomalisinin Tmin/Tmax ortalamasına uygulanması bir delta varsayımıdır; gelecek günlük sıcaklık serisi üretilmedi.
5. `pr` için aylık toplamın gelecek/referans oranı ERA5 aylık toplam yağışına uygulandı. Referans <1 mm/ay olursa betik sessizce oran kırpmak yerine durur. Bu veride durma koşulu oluşmadı. Kaynak yağış mm/ay dönüşümü, ayın gerçek takvim gün sayısıyla indirme sırasında yapılmıştır.
6. Gelecekteki aylık sıcaklık ve yağışla 12 sarmalı üç-ay penceresi tekrar hesaplandı. **29/703 hücrede en sıcak çeyrek değişti.** BIO18 sabit %15 artış değil.
7. SST için 12 eşit ağırlıklı aylık GCM anomalisinin ortalaması, mevcut ERA5 yıllık SST'ye eklendi. Buz için aynı şekilde **yüzde puan** değişimi yıllık ERA5 buzuna eklendi ve 0-100'e sınırlandı. Mevcut yıllık değişken tanımı korunur; aylık ERA5 buzu üzerinde ay ay kırpma yapılmış gibi sunulmaz.
8. Kaya mevcut katmandan sabit tutuldu. Bu, gelecekte buzsuz kayalık alanların değişmeyeceğinin gözlemsel kanıtı değil.

Kaynak mesafeleri ve eşleme indisleri `scenario.json` ve `monthly_delta_diagnostics.npz` içinde. Atmosfer için en yakın native hücre uzaklığı 3,74-85,83 km; deniz için 1,76-44,71 km (kara için önce ERA5 deniz hücresine geçildikten sonra). Kara→ERA5 deniz uzaklığı ayrıca saklanır; bu aralıklara dahil değildir.

Gelecek dört ASC aynı orijinal EPSG:4326, 37×19, 0,25° ızgarada; 703 hücrede sonlu değer var. Gelecek BIO18 77,59-756,55 mm, yıllık SST −1,887…+0,208 °C, yıllık buz %9,28-53,02; kaya değişmedi. Bu aralıklar bağımsız bölgesel iklim doğrulaması sayılmaz.

## MaxEnt modeli ve kontrol

`maxent/cmip6_projeksiyon.py`, özgün 2026-10-31 koşusunun on `.lambdas` dosyasını `density.Project` ile uygular. Parametreler açık: cloglog, clamping açık, clamp grid açık, extrapolation açık. Kaynak kodu: [MaxEnt Project.java](https://github.com/mrmaxent/Maxent/blob/master/density/Project.java).

Yeni model eğitimi veya nihai model seçimi yok. Önce fold0 modeliyle günümüz girdileri ve eski varsayımsal gelecek tekrar projekte edildi; kayıtlı iki fold0 çıktısına karşı **maksimum mutlak fark 0,0**. Böylece kaydedilmiş modelin uygulanma yolu kontrol edildi. On günümüz katının ortalaması da mevcut ortalama rasterla tolerans içinde eşleşti. Komutlar, Java/jar ve lambda hash'leri çıktı manifestinde.

Bu projeksiyon **mekânsal aktarım performansı zayıf eski modelin** gerçek iklim girdilerine deneysel aktarımıdır. Gerçek CMIP6 girdisi kullanmak, modeli kendiliğinden güvenilir yapmaz. Eşit ayarlı AUTO/RM1 karşılaştırmasında rastgele4 AUC 0,76543, mekânsal4 AUC 0,47742; ayrıntı mekânsal doğrulama belgesinde.

## Betimsel sonuçlar ve sınırlar

±0,05 mutlak uygunluk puanı farkı eşiği, tüm 703 hücrelik dikdörtgen:

| Sınıf | Hücre | Hücre payı | Model dikdörtgeninin WGS84 alan payı |
|---|---:|---:|---:|
| Uygunlukta azalma | 297 | %42,25 | %43,99 |
| Kararlı | 163 | %23,19 | %22,23 |
| Uygunlukta artış | 243 | %34,57 | %33,78 |

Bu tablo **habitat alanı kaybı veya kazanımı değildir**. Ekolojik maske ve gerekçeli uygunluk eşiği yok; nüfus/koloni kaybı ya da sığınak sonucuna dönüştürülemez. Eski varsayımsal denemenin %54,6 sayısıyla aynı senaryo gibi karşılaştırılmaz.

- 357/703 hücre en az bir native prediktörde lambda dosyasındaki min-maks aralığının dışında. Bu bir tek-değişken aralık uyarısıdır; MESS hesaplandığı iddia edilmez.
- 246/703 hücrede eşlenik katlar hem pozitif hem negatif değişim üretiyor.
- En büyük clamping etkisi yaklaşık 0,630 puan. Bu etki yorumlarda saklanmamalı.
- Kat dağılımı bağımsız GCM ensemble'ı değil. Bu yalnız bir GCM/üye/SSP'dir; iklim modeli/senaryo belirsizliği sayısallaştırılmış değildir.
- Görselleştirme yumuşatması yalnız sürekli uygunluk için uygulanır; bütün hesaplar özgün 0,25° hücrelerden gelir.
- Mevcut genel bulunuş kayıtları, M alanı ve bağımsız doğrulama iyileştirilmeden nihai bilimsel habitat sonucu olarak kullanılmamalı.

## Yeniden üretim

İndirme ortamı ve paket sürümleri CMIP erişim belgesinde. Aşağıdaki çevrimdışı teknik üretim sistem NumPy/GDAL ve Java 21 kullanır. Üreticiler mevcut gerçek veri koşusunun üzerine yazmayı reddeder; yeni sürüm için yeni çıktı dizini ve ona uygun giriş bağlantıları kullanılmalı.

```bash
python maxent/cmip6_delta_katmanlari.py
python maxent/cmip6_projeksiyon.py
QT_QPA_PLATFORM=offscreen python harita/duzeltilmis_haritalar.py --smooth-display --analysis-dir maxent/cikti/cmip6_ipsl_ssp245_2041_2060_v1
python -m unittest discover -s maxent -p 'test_*.py' -v
```

Varsayımsal ve gerçek senaryo üretim/analiz yolları ayrıdır. Eski kaynak dosyalar `docs/arsiv_20261108/baslangic_manifest.json` ile korunur; doğrulamada hiçbir orijinal raster, CSV, QGIS projesi, PDF veya PNG değişmedi.
