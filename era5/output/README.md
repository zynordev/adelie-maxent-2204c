# ERA5 tabanlı iklim ve denizel katmanlar — Marguerite Körfezi, 2000–2025

MaxEnt'in **"Environmental layers"** girdisi olarak hazırlanmış 25 katman (19 biyoklimatik + 5 denizel + 1 buzsuz kaya).
Kod: `../` (bu klasörün bir üstü). Kararların gerekçeleri: `../../docs/KARARLAR.md`.

> **Bu katmanlar hakemli bir veri seti değildir.** Ham ERA5 reanalizinden, WorldClim / `dismo::biovars`
> tanımlarıyla bu proje için hesaplanmıştır (aynı mantıkla üretilmiş hakemli bir örnek: MERRAclim,
> Vega vd. 2017). Doğrulama adımları aşağıda ve `../dogrula.py` dosyasındadır.

## 1. Kaynak veri

| Kullanım | CDS veri seti | Değişken | DOI |
|---|---|---|---|
| Günlük maks/min sıcaklık (saatlikten) | `reanalysis-era5-single-levels` (saatlik) | `2m_temperature` | 10.24381/cds.adbb2d47 |
| Aylık yağış | `reanalysis-era5-single-levels-monthly-means` (`monthly_averaged_reanalysis`) | `total_precipitation` | 10.24381/cds.f17050d7 |
| Deniz yüzeyi sıcaklığı | aynı | `sea_surface_temperature` | 10.24381/cds.f17050d7 |
| Deniz buzu | aynı | `sea_ice_cover` | 10.24381/cds.f17050d7 |
| Yalnızca eşdeğerlik kontrolü | `derived-era5-single-levels-daily-statistics` | `2m_temperature` (daily_maximum) | 10.24381/cds.4991cf48 |

- **İndirme:** Copernicus Climate Data Store, resmi `cdsapi` istemcisiyle; **2026-10-19 / 2026-10-20** (`../veri_ham/indirme_kaydi.csv`).
- **Lisans:** CC-BY 4.0 (ERA5).
- **Neden saatlik?** Günlük maks/min, planlanan günlük istatistik ürünü yerine saatlik veriden yerelde hesaplandı (CDS kuyruğu çok yavaştı). 2000 ve 2001 yıllarında iki yol karşılaştırıldı: 731 gün × 703 hücrenin **tamamında fark 0.0 K** (`../saatlik_gunluk_karsilastir.py`, K-013).

## 2. Alan, dönem, ızgara

| | |
|---|---|
| Dönem | 2000-01 → 2025-12 (26 yıl; iklim normali bu dönemin ortalamasıdır) |
| Alan (hücre kenarları) | 73.125°B – 63.875°B, 70.625°G – 65.875°G |
| Çözünürlük | 0.25° × 0.25° (ERA5 yerel ızgarası; **yeniden örnekleme yapılmadı**) |
| Boyut | 37 sütun × 19 satır = 703 hücre |
| Koordinat sistemi | EPSG:4326 (WGS84 enlem/boylam) |
| NoData | −9999 (MaxEnt katmanlarında NoData hücresi **yok**) |

Tüm `.asc` dosyalarının başlığı birebir aynıdır:
```
ncols 37 | nrows 19 | xllcorner -73.125 | yllcorner -70.625 | cellsize 0.25 | NODATA_value -9999
```

## 3. Hesaplama

**Sıcaklık:** saatlik 2 m sıcaklık → UTC günü içindeki 24 değerin maks/min'i → her yıl-ay için ortalama Tmax/Tmin → K − 273.15 = °C.
**Yağış:** aylık ortalama üründe `tp` = günlük ortalama birikim (m/gün) → **mm/ay = tp × 1000 × ayın gün sayısı** (artık yıllar dahil).
**Normaller:** 2000–2025 üzerinden 12 takvim ayının ortalaması → `tmax[12]`, `tmin[12]`, `prec[12]`, `tavg = (tmax + tmin) / 2`.

**Bio1–Bio19** — `dismo::biovars` ile birebir (`../biovars.py`; elle hesaplanmış örnekle test: `../test_biovars.py`):

| Kod | Tanım | Birim |
|---|---|---|
| bio1 | Yıllık ortalama sıcaklık = mean(tavg) | °C |
| bio2 | Ortalama günlük sıcaklık aralığı = mean(tmax − tmin) | °C |
| bio3 | İzotermalite = bio2 / bio7 × 100 | % |
| bio4 | Sıcaklık mevsimselliği = sd(tavg) × 100 | °C × 100 |
| bio5 | En sıcak ayın maks. sıcaklığı = max(tmax) | °C |
| bio6 | En soğuk ayın min. sıcaklığı = min(tmin) | °C |
| bio7 | Yıllık sıcaklık aralığı = bio5 − bio6 | °C |
| bio8 | En yağışlı çeyreğin ort. sıcaklığı | °C |
| bio9 | En kurak çeyreğin ort. sıcaklığı | °C |
| bio10 | En sıcak çeyreğin ort. sıcaklığı | °C |
| bio11 | En soğuk çeyreğin ort. sıcaklığı | °C |
| bio12 | Yıllık yağış = sum(prec) | mm |
| bio13 | En yağışlı ayın yağışı | mm |
| bio14 | En kurak ayın yağışı | mm |
| bio15 | Yağış mevsimselliği = sd(prec) / (1 + mean(prec)) × 100 | % |
| bio16 | En yağışlı çeyreğin yağışı | mm |
| bio17 | En kurak çeyreğin yağışı | mm |
| bio18 | En sıcak çeyreğin yağışı | mm |
| bio19 | En soğuk çeyreğin yağışı | mm |

Çeyrek = ardışık 3 ay; yıl sonundan başa saranlar dahil 12 pencere. `sd` = örneklem standart sapması (n − 1). Sıcaklıklar ×10 ölçeklenmemiştir.

**Denizel katmanlar** (`../denizel_hesapla.py`):

| Dosya | Tanım | Birim |
|---|---|---|
| `sst_yillik` | 12 ayın ortalama deniz yüzeyi sıcaklığı (K − 273.15) | °C |
| `sst_yaz` | Aralık–Şubat ortalaması (yavru büyütme dönemi) | °C |
| `buz_yillik` | 12 ayın ortalama deniz buzu (`sea_ice_cover` × 100) | % |
| `buz_yaz` | Aralık–Şubat ortalaması | % |
| `buz_kis` | Haziran–Ağustos ortalaması | % |

## 4. Kara hücrelerinin doldurulması (yalnızca denizel katmanlar)

ERA5'te SST ve deniz buzu **karada tanımsızdır** (703 hücrenin 364'ü). Adélie kolonileri kıyıda/karada olduğu için
doldurulmazsa MaxEnt bu kayıtları atar. Bu nedenle:

- `ham/` → doldurulmamış hali (kara = NoData).
- Bu klasördeki sürüm → her kara hücresine, **küre üzerindeki gerçek uzaklığa göre en yakın deniz hücresinin** değeri atandı
  (68°G'de 1° boylam ≈ 0.37° enlem uzunluğunda olduğu için ızgara indeksine göre değil; K-015).
- Doldurulan hücre: her denizel katmanda **364**. Deniz hücrelerinin değerleri değişmedi (doğrulandı).
- **Varsayım:** Kıyıdaki/karadaki bir hücrenin "denizel koşulu", ona en yakın deniz hücresininkidir. İç kesimlerde
  (penguen kaydı olmayan yükseklerde) bu değerlerin fiziksel anlamı yoktur; yalnızca MaxEnt'in kayıt atmaması içindir.

Biyoklimatik katmanlarda doldurma **yoktur**: 2 m sıcaklık ve yağış kara ve deniz üzerinde tanımlıdır.

## 5. Doğrulama (`../dogrula.py` — tüm kontroller geçti, 2026-10-20)

| Kontrol | Sonuç |
|---|---|
| 24 `.asc` başlığı aynı | ✔ |
| MaxEnt katmanlarında NoData yok | ✔ |
| Rothera hücresi (merkez 67.50°G, 68.25°B; deniz hücresi): Bio1 = −6.78 °C | ✔ sıfırın birkaç derece altında |
| Rothera: Bio5 = −0.23 > Bio1 = −6.78 > Bio6 = −14.76 °C | ✔ |
| Rothera: Bio12 = 1341 mm | ✔ > 0 |
| Yaz SST (deniz hücreleri) −2.14 … 0.76 °C | ✔ yaklaşık −2 … birkaç °C |
| Kış buzu ≥ yaz buzu | ✔ 339/339 deniz hücresi |
| Biovars testi / saatlik–günlük eşdeğerlik | ✔ / ✔ (fark 0.0 K) |

Katman başına min/maks/ortalama/NoData/doldurulan hücre: `ozet_istatistik.csv`.

## 6. Korelasyon

24 katman, 703 hücre, Pearson: `korelasyon_matrisi.csv`, `korelasyon_matrisi.png`.
|r| > 0.8 olan **49 çift**: `yuksek_korelasyon.txt`. **Değişken seçimi bu çalışmada yapılmamıştır**; öğrenci ve danışman tarafından yapılacaktır.
Not: Doldurulmuş kara hücreleri denizel katmanlarda tekrarlanan değerler içerdiği için bu katmanların korelasyonlarını bir miktar etkiler.

## 6b. Buzsuz kaya katmanı (`kaya`) — ERA5 değil

- **Kaynak:** SCAR Antarctic Digital Database, *High resolution vector polygons of Antarctic rock outcrop*, v7.11 — Skachkova, A., Gerrish, L., Fretwell, P. & Cooper, P. (2025), NERC EDS UK Polar Data Centre, https://doi.org/10.5285/815525ca-cefe-4fbf-9224-3ee784e7de4e (CC BY 4.0). Bu bölge (20°B–80°B) 2024/25 Sentinel-2 mozaiğinden otomatik çıkarılmıştır. İndirme: 2026-10-20.
- **Hesap (`../../kaya/kaya_hesapla.py`):** her 0.25° hücrenin kaya poligonlarıyla kesişim alanı / hücre alanı × 100, eşit alanlı Lambert azimutal (Güney Kutbu) projeksiyonunda. Birim: **% hücre alanı**. Denizdeki ve tamamen buzla kaplı hücreler 0 (NoData değil).
- **Sonuç:** 343/703 hücrede kaya; en yüksek %15.3; toplam 1856 km². Diğer katmanlarla |r| ≤ 0.29.
- **Sınırlılık:** Kaya örtüsü statiktir (tek bir yaz); hücre ortalaması koloni ölçeğindeki zemin özelliklerini (eğim, bakı, kar birikimi) göstermez.

## 7. Sınırlılıklar

- **Çözünürlük:** 0.25° ≈ enlemde ~28 km, bu enlemde boylamda ~10 km. Koloni ölçeğindeki mikroklima temsil edilmez; kıyı hücreleri kara ve denizi karışık temsil eder.
- **Reanaliz istasyon gözlemi değildir.** Model + asimilasyon ürünüdür. Örneğin Rothera hücresinin Bio1 değeri (−6.8 °C) istasyon ölçümlerinden daha soğuk olabilir; hücre ortalaması ile nokta ölçümü aynı şey değildir.
- **Yağış** ERA5'te modelden gelir; Antarktika'da gözlemle sınırlı doğrulanmıştır. Dağlık yamaçlarda (orografik) yüksek değerler fiziksel olarak tutarlı ama belirsizdir.
- **Gün sınırı UTC'dir** (yerel saat ≈ UTC−4/−5); aylık ortalamalara etkisi ihmal edilebilir (K-014).
- **Kara–deniz maskesi** ERA5'in kendi maskesidir; küçük adalar deniz hücresi olarak görünebilir.
- **Katmanlar hakemli değildir**; yöntem bu dosyada ve kodda şeffaf biçimde belgelenmiştir.

## 8. Atıflar

- Hersbach, H., Bell, B., Berrisford, P. vd. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society*, 146, 1999–2049. doi:10.1002/qj.3803
- C3S (2018). *ERA5 hourly data on single levels from 1940 to present* [Dataset]. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). https://doi.org/10.24381/cds.adbb2d47
- Copernicus Climate Change Service (2019). *ERA5 monthly averaged data on single levels from 1940 to present* [Dataset]. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). https://doi.org/10.24381/cds.f17050d7

(Veri seti atıfları DOI kayıt sisteminden — DataCite, APA biçimi — 2026-10-20'de alındı.)
- Bioclim tanımları: https://www.worldclim.org/data/bioclim.html ; Hijmans, R. J. vd. `dismo` R paketi, `biovars()`.
- Vega, G. C., Pertierra, L. R. & Olalla-Tárraga, M. Á. (2017). MERRAclim. *Scientific Data* 4:170078. doi:10.1038/sdata.2017.78

## 9. Dosyalar

| Dosya | İçerik |
|---|---|
| `bio1.asc` … `bio19.asc` | Biyoklimatik katmanlar (MaxEnt girdisi) |
| `sst_yillik.asc`, `sst_yaz.asc`, `buz_yillik.asc`, `buz_yaz.asc`, `buz_kis.asc` | Denizel katmanlar, kara dolduruldu (MaxEnt girdisi) |
| `kaya.asc` | Buzsuz kaya örtüsü (% hücre alanı; SCAR ADD v7.11, Bölüm 6b) |
| `*.tif` | Aynı katmanların GeoTIFF kopyaları (QGIS için) |
| `*.png` | Önizlemeler (220 dpi; pikseller bilerek yumuşatılmadı) |
| `ham/` | Denizel katmanların doldurulmamış hali |
| `ozet_istatistik.csv` | Katman istatistikleri |
| `korelasyon_matrisi.csv/.png`, `yuksek_korelasyon.txt` | Korelasyon |

**Yeniden üretmek için:** `../hepsini_calistir.sh` (ya da sırasıyla `indir.py` → `denizel_hesapla.py` → `bioclim_hesapla.py` → `korelasyon.py` → `dogrula.py`).
