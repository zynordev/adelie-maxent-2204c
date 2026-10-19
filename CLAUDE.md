# CLAUDE.md — Adélie Pengueni MaxEnt Niş Modeli (TÜBİTAK 2204-C)

> Bu dosya, önceki bir Claude sohbetinin (16–18 Ekim 2026) **tüm bağlamını** tek yerde toplar. Claude Code'da sıfırdan başlayan bir oturum, bu dosyayı okuyarak projeyi, alınan kararları ve yapılacak teknik işi eksiksiz anlamalıdır.
> **Dil:** Türkçe. **Kullanıcı:** Linux kullanan lise öğrencisi; ekipte algoritma/kod tarafından sorumlu ("1024").

---

## 0. Claude için çalışma kuralları (ÖNCE BUNU OKU)

1. **Varsayılan mod: yol göstericilik.** Öğrenci projeyi AI'a yaptırmak istemiyor. Rapor yazma, bilimsel yorum üretme, MaxEnt'i çalıştırma, GBIF verisini indirme gibi işleri **öğrenci açıkça istemedikçe yapma**. Açıkla, yönlendir, takıldığı yerde yardım et.
2. **İstisna — açıkça istenen teknik görev:** Öğrenci, ERA5'ten iklim katmanlarını üretme işinin (Bölüm 9) senin tarafından **yapılmasını** istedi. Öğrenci "başla" dediğinde Bölüm 9'u uygula.
3. **Öncelik sırası:** Öğrencinin son söyledikleri > danışmanla toplantı kararları (Bölüm 2) > referans proje (Bölüm 4) > eski taslak (Bölüm 3).
4. Bir bilgiyi ezbere değil **doğrulayarak** kullan (veri seti adları, API formatları, değişken adları zamanla değişir).
5. Değişken seçimi, model yorumu gibi kararları **öğrenci ve danışmanı** verir; sen seçenekleri ve gerekçeleri sun.
6. Yeni karar alındıkça bu dosyanın "Kararlar" ve "Açık sorular" bölümlerini güncelle.
7. **Kayıt tutma (zorunlu):** Her oturumda ve her aşamada `docs/` altındaki kayıtları güncelle. Ayrıntı ve şablonlar: `docs/README.md`.
   - Her oturum sonunda → `docs/GUNLUK.md`'ye tarihli kayıt (ne yapıldı, çıktılar, sorunlar, sıradaki adım).
   - Her yeni karar → `docs/KARARLAR.md`'ye numaralı kayıt (K-xxx); özeti bu dosyanın Bölüm 6'sına da işle.
   - Aşama durumu değişince → `docs/ASAMALAR.md`.
   - Danışman toplantısı → `docs/toplantilar/YYYY-AA-GG-konu.md`.
   - Bu kayıtlar proje klasöründe tutulur; Obsidian'dan bağımsızdır.

---

## 1. Projenin özü

GBIF'ten Adélie penguenlerinin (*Pygoscelis adeliae*) **2000–2026** arasına ait bulunuş koordinatlarını alıp, çevresel katmanlarla birlikte **klasik MaxEnt (Java arayüzü)** programına yükleyerek türün **ekolojik niş modelini** kurmak. Model bir **habitat uygunluk haritası** ve bir **AUC değeri** üretir. **AUC > 0.70 → başarılı**; değilse model yeniden denenir. Çalışma alanı: **Marguerite Körfezi** (Batı Antarktika Yarımadası).

---

## 2. Danışman toplantısının kararları (bağlayıcı)

Toplantı not alınmadı; öğrencinin aktarımıdır.

| Konu | Karar |
|---|---|
| Ana görev | GBIF koordinatları → MaxEnt → harita + AUC → danışmana bildir |
| Başarı ölçütü | AUC > 0.70 |
| Hedef | "Niş modeli oluşturmak" |
| Bio-ORACLE | Şimdilik boş ver, sonra bakılacak |
| Ekip rol dağılımı | Şimdilik boş ver |
| Eski taslak | Toplantıda pek dikkate alınmadı |
| Çevresel katman (ilk cevap) | WorldClim bioclim (Bio1–Bio19) — "makalelerde hep bu veriliyor" |

---

## 3. Eski taslak plan (yalnızca arka plan)

- Başlık: İklim Değişikliği Senaryoları Altında Adélie Penguenlerinin Antarktika Yarımadası'ndaki Ekolojik Niş Modellemesi ve Gelecek Habitat Projeksiyonları
- Bölge: Antarktika Yarımadası ve Marguerite Körfezi (Türk Kutup Bilim Üssü hinterlandı)
- Fikir: deniz buzu ve deniz yüzeyi sıcaklığı değişimi → kril azalması → Adélie habitatı daralıyor
- Planlanan: Bio-ORACLE/Copernicus değişkenleri; CMIP6 2050 (SSP2-4.5, SSP5-8.5); Python (`elapid`); K-Fold; AUC > 0.80; 7 haftalık takvim
- Hipotez: 2050'ye kadar yüksek uygunluktaki habitatta daralma / güneye kayma

⚠️ Bunların çoğu ertelendi ya da değişti. AUC eşiği artık **0.70**. Gelecek senaryoları şimdilik kapsam dışı.

---

## 4. Referans çalışma: danışmanın derece almış projesi

**"MaxEnt Algoritması Kullanılarak İstilacı Tür *Halyomorpha halys* ve Konukçusu *Corylus avellana*'nın Gelecekteki Potansiyel Dağılımının Tahmini"** (Biyoloji / Ekolojik Denge, Türkiye ölçeği). Danışman büyük olasılıkla benzer bir akış bekliyor.

**Yöntem:**
1. GBIF + iNaturalist koordinatları, güvenilirliğe göre elendi (176 ve 224 nokta) → `.csv` → MaxEnt "Samples".
2. Günümüz: WorldClim (19 bioclim + yükselti). Gelecek: CHELSA (MPI-ESM1-2-HR; SSP1-2.6, SSP5-8.5; 2040, 2070).
3. Değişkenler literatürden seçildi (tüm 19'u değil).
4. ArcGIS + SDM Toolbox 2.4 ile kırpma ve `.asc`'ye dönüştürme → MaxEnt "Environmental layers".
5. Klasik MaxEnt çalıştırıldı.
6. Raporlananlar: ROC/AUC (0.868–0.884), Percent Contribution, Permutation Importance, Jackknife (mavi: tek başına; turkuaz: çıkarılınca; kırmızı: tümü), `.asc` uygunluk haritası → renklendirilmiş harita.
7. AUC yorum tablosu: 0.5–0.6 başarısız; 0.6–0.7 zayıf; 0.7–0.8 orta; 0.8–0.9 yüksek; 0.9–1 çok başarılı.
8. Rapor yapısı: Özet → Amaç → Giriş → Yöntem → Bulgular → Sonuç ve Tartışma → Öneriler → Kaynaklar.

**Bu projeyle farklar:** Referans karasal türler için karasal iklim kullandı. Adélie **karada (buzsuz kayalık kıyıda) ürer, denizde beslenir.** Ayrıca referans proje WorldClim 1970–2000 verisini güncel kayıtlarla kullandı; iklim dönemi ile kayıt yılları arasındaki uyuşmazlık bu alanda yaygın ve kabul gören bir durumdur.

---

## 5. Kavramlar

- **SDM / ekolojik niş modeli:** Türün bulunduğu noktalardaki çevre koşullarından, türün tercih ettiği koşulları öğrenip haritaya yayan model.
- **MaxEnt:** Yalnızca varlık (presence-only) verisiyle çalışan SDM algoritması (Phillips vd. 2006). Girdiler: koordinat `.csv` + **aynı ızgaradaki** çevresel `.asc` katmanları. **Herhangi bir katmanda NoData'ya düşen noktaları atar.**
- **Background noktaları:** MaxEnt'in "tür yok" yerine kullandığı rastgele çevre örnekleri.
- **AUC:** ROC eğrisi altındaki alan; 0.5 rastgele, 1 mükemmel.
- **Percent Contribution / Permutation Importance / Jackknife:** Değişken önem ölçütleri.
- **Spatial thinning:** Birbirine çok yakın kayıtları seyreltme.
- **Reanaliz:** Uydu, istasyon, gemi ve şamandıra gözlemlerinin bir iklim modeliyle birleştirilmesiyle üretilen tutarlı ızgaralı veri (ERA5, MERRA).

---

## 6. Netleşen kararlar

| Konu | Karar |
|---|---|
| Çalışma alanı | Marguerite Körfezi |
| Model aracı | **Klasik MaxEnt (Java GUI)**. Python **yalnızca veri hazırlığı** için (ERA5 katmanları) |
| Kayıt dönemi | 2000–2026 |
| AUC eşiği | > 0.70 |
| İşletim sistemi | Linux → ArcGIS/SDM Toolbox yok; yerine **QGIS + GDAL**. MaxEnt Java ile Linux'ta çalışır (`java -jar maxent.jar`) |
| WorldClim | **Kullanılamaz.** Öğrenci indirip kontrol etti: Antarktika'da veri yok |
| İklim kaynağı (öğrencinin kararı, danışman onayı bekleniyor) | **ERA5'ten 2000–2025 için Bio1–Bio19'u kendimiz hesaplamak** + **deniz yüzeyi sıcaklığı ve deniz buzu** katmanları |
| Yedek seçenek | MERRAclim 2000'ler (hazır, hakemli, ama 2001–2010) |
| Kayıt sistemi (2026-10-19) | Her iş/aşama `docs/` altında Markdown olarak kaydedilir (K-012) |
| Günlük sıcaklık kaynağı (2026-10-19) | Saatlik ERA5'ten günlük maks/min (UTC günü); CDS günlük ürünüyle birebir aynı, fark 0.0 K (K-013, K-014) |
| Kara hücresi doldurma (2026-10-19) | Küre üzerinde en yakın deniz hücresi (K-015) |
| GBIF indirme (2026-10-19) | API, öğrencinin hesabı; 1001 kayıt, DOI 10.15468/dl.jt3gt7 (K-017) |
| GBIF temizlik (2026-10-19, onay bekliyor) | 1001 → 704 temiz → 67 MaxEnt noktası, ERA5 hücresi başına 1 (K-018) |

Numaralı, gerekçeli tam karar kaydı: `docs/KARARLAR.md`.

---

## 7. Sohbette ulaşılan bulgular (kaynaklı)

### 7.1 WorldClim neden olmaz
- WorldClim katmanları Antarktika hariç küresel kara alanlarını kapsar (worldclim.org v1.4 dokümantasyonu; Vega vd. 2017; Antarktika likenleri çalışması, Theor. Appl. Climatol. 2017). Öğrenci 2.1 sürümünü indirip doğruladı.

### 7.2 MERRAclim (yedek seçenek)
- Vega, Pertierra & Olalla-Tárraga (2017), *Scientific Data* 4:170078, doi:10.1038/sdata.2017.78. Veri: Dryad doi:10.5061/dryad.s2v81, CC BY.
- NASA MERRA reanalizinden, WorldClim yöntemiyle 19 bioclim; Antarktika dahil. Dönemler: 1980'ler, 1990'lar, **2000'ler (2001–2010)**. Çözünürlük: 10', 5', 2.5' (ham ızgara ~40'×30', ince sürümler spline enterpolasyonu).
- Sürümler Vmax/Vmean/Vmin; WorldClim'e en yakın **Vmin**. Önerilen dosya: `10m_min_00s.zip` (~53 MB).
- **BIO12–BIO19 yağış değil, özgül nemdir.** Birimler: BIO1–11 °C×10; BIO12–19 kg/kg×100000. Format GeoTIFF.
- Antarktika istasyonlarıyla (Palmer dahil) korelasyon > 0.8; MERRA daha soğuk ama yaz aylarında sapma küçük. Kıyı ve yüksek rakımda enterpolasyon sapması büyük.

### 7.3 2020'lere uzanan hazır bioclim var mı?
- **Yok.** Copernicus C3S'nin ERA5 tabanlı biyoklimatik göstergeleri 1979–2018, 0.5° (çok kaba). CHELSA-BIOCLIM+ zaman serisi 1980–2018; Antarktika kapsamı doğrulanmadı.
- ERA5'in ham verisi günümüze kadar aylık güncellenir → 2000–2025 Bio1–Bio19 hesaplanabilir. **Bu uydurma değildir:** MERRAclim de aynı mantıkla (ham reanaliz + WorldClim formülleri) üretildi. Fark: bizim katmanlarımız hakemli değil, bu yüzden doğrulama adımı raporda gösterilmeli ve yöntem şeffafça yazılmalı.

### 7.4 Adélie literatürü
- Adélie MaxEnt çalışmaları çoğunlukla **denizel/uydu değişkenleri** kullanır: deniz yüzeyi sıcaklığı, deniz buzu, klorofil, batimetri, çıplak kaya yuvalama alanları (Cimino vd. 2016, *Scientific Reports*, doi:10.1038/srep28785; Cimino vd. NASA CCE posterleri 2011, 2015).
- Bulgular: Batı Antarktika Yarımadası'nda kuzeyde uygun habitat azalıyor, uygun koşullar güneye kayıyor (Marguerite Körfezi bu bölgede).

### 7.5 Özgünlük
- "Adélie için ilk MaxEnt" iddiası **yanlış** olur (Cimino vd. 2016 var).
- Savunulabilir özgünlük: **Marguerite Körfezi yerel ölçeği + güncel 2000–2025 iklim + karasal ve denizel katmanların birlikte kullanımı + Türk Kutup Bilim Üssü bağlamı.**

---

## 8. Açık sorular / bekleyenler

- Danışman, ERA5 tabanlı kendi hesapladığımız katmanları (Bio + denizel) onaylayacak mı? (Öğrenci soracak.)
- Hangi değişkenler modele girecek? (Korelasyon matrisi çıktıktan sonra öğrenci + danışman seçecek.)
- ~~GBIF'te kaç kayıt var?~~ → 1001 ham, 67 MaxEnt noktası (19 kara, 48 deniz hücresi). **Kara (koloni) + deniz kayıtları birlikte mi kullanılacak?** (K-018; öğrenci + danışman)
- Gelecek senaryoları (2050) ileride geri dönecek mi?
- "Deniz tuzu" = deniz buzu mu, tuzluluk mu? Tuzluluksa ORAS5 + yeniden örnekleme kabul edilecek mi? (K-016; öğrenci + danışman)

---

## 9. TEKNİK GÖREV: ERA5'ten iklim katmanları üretimi

> Öğrenci "başla" dediğinde uygula. Görev **yalnızca iklim katmanlarını üretmektir.** MaxEnt'i çalıştırma, GBIF verisine dokunma, rapor yazma.

**Ortam:** Linux, Python 3, sanal ortam (`python3 -m venv .venv`).

### 9.1 Ön koşullar (kullanıcıyla)
1. Veri **Copernicus Climate Data Store (CDS)** üzerinden iner. Kullanıcının CDS hesabı ve API anahtarı olmalı. Yoksa şunu söyle ve bekle:
   - https://cds.climate.copernicus.eu adresinde hesap açsın,
   - Kullanılacak her veri setinin sayfasında **lisans koşullarını kabul etsin**,
   - API anahtarını `~/.cdsapirc` dosyasına kendisi yazsın ya da sana versin.
2. `~/.cdsapirc` formatını **CDS'in güncel dokümantasyonundan** doğrula. **API anahtarını asla ekrana yazdırma, loglama veya başka dosyaya kopyalama.**
3. İndirme için resmi **`cdsapi`** paketini kullan (CDS API asenkron: istek kuyruğa girer). `curl` yalnızca bağlantı testi için.

### 9.2 Veri setleri (CDS kataloğundan doğrula)

| İhtiyaç | CDS veri seti | Değişken |
|---|---|---|
| Günlük max/min sıcaklık | ~~`derived-era5-single-levels-daily-statistics`~~ → **`reanalysis-era5-single-levels` (saatlik), günlük maks/min yerelde** (K-013) | `2m_temperature` |
| Aylık yağış | `reanalysis-era5-single-levels-monthly-means` (monthly_averaged_reanalysis) | `total_precipitation` |
| Deniz yüzeyi sıcaklığı | `reanalysis-era5-single-levels-monthly-means` | `sea_surface_temperature` |
| Deniz buzu | `reanalysis-era5-single-levels-monthly-means` | `sea_ice_cover` |

- **Dönem:** 2000-01 → 2025-12.
- **Alan [K, B, G, D]:** `[-66.0, -73.0, -70.5, -64.0]` (değiştirilebilir sabit).
- **Izgara:** ERA5 yerel 0.25°×0.25°; yeniden örnekleme yapma.
- İstekleri **yıl yıl böl**; inmiş dosyaları atla (yeniden başlatılabilir); ilerlemeyi logla.
- Hava değişkenleri (sıcaklık, yağış) kara + deniz üzerinde tanımlı; kara-deniz maskesi uygulama.

### 9.3 Birimler (metadata'dan doğrula)
- Sıcaklıklar: K − 273.15 → °C.
- `total_precipitation` (aylık ortalama ürün): genellikle m/gün → mm/ay = ×1000 × ayın gün sayısı (artık yıl dahil).
- `sea_ice_cover`: 0–1 → ×100 → %.

### 9.4 Bio1–Bio19 hesaplama
1. Günlük max/min → her yıl-ay için aylık ortalama Tmax/Tmin.
2. 2000–2025 üzerinden takvim ayı ortalamaları → 12 aylık normal: `tmax[12]`, `tmin[12]`, `prec[12]`, `tavg=(tmax+tmin)/2`.
3. **`dismo::biovars` / WorldClim tanımlarıyla birebir:**

| Kod | Tanım |
|---|---|
| Bio1 | mean(tavg) |
| Bio2 | mean(tmax − tmin) |
| Bio3 | Bio2 / Bio7 × 100 |
| Bio4 | sd(tavg) × 100 |
| Bio5 | max(tmax) |
| Bio6 | min(tmin) |
| Bio7 | Bio5 − Bio6 |
| Bio8 | En yağışlı çeyreğin tavg ortalaması |
| Bio9 | En kurak çeyreğin tavg ortalaması |
| Bio10 | En sıcak çeyreğin tavg ortalaması |
| Bio11 | En soğuk çeyreğin tavg ortalaması |
| Bio12 | sum(prec) |
| Bio13 | max(prec) |
| Bio14 | min(prec) |
| Bio15 | sd(prec) / (1 + mean(prec)) × 100 |
| Bio16 | En yağışlı çeyreğin yağış toplamı |
| Bio17 | En kurak çeyreğin yağış toplamı |
| Bio18 | En sıcak çeyreğin yağış toplamı |
| Bio19 | En soğuk çeyreğin yağış toplamı |

- Çeyrek = ardışık 3 ay, yıl sonundan başa saran pencereler dahil **12 pencere**.
- `sd` = örneklem standart sapması (n−1), dismo ile aynı.
- Sıcaklıklar °C (×10 ölçekleme yok), yağış mm.
- Hesaplama fonksiyonunu elle hesaplanabilir sentetik bir 12 aylık örnekle **test et**.

### 9.5 Denizel katmanlar

| Dosya | Tanım |
|---|---|
| `sst_yillik.asc` | Yıllık ortalama deniz yüzeyi sıcaklığı (°C) |
| `sst_yaz.asc` | Aralık–Şubat ortalaması (°C), yavru büyütme dönemi |
| `buz_yillik.asc` | Yıllık ortalama deniz buzu (%) |
| `buz_yaz.asc` | Aralık–Şubat ortalama deniz buzu (%) |
| `buz_kis.asc` | Haziran–Ağustos ortalama deniz buzu (%) |

**KRİTİK — kara hücreleri:** Bu iki değişken kara hücrelerinde NaN'dır. Penguen kolonileri kıyıda/karada olduğundan, doldurulmazsa MaxEnt bu kayıtları atar.
1. Ham sürümü `output/ham/` altına kaydet.
2. MaxEnt sürümünde her kara hücresine **en yakın deniz hücresinin değerini** ata (nearest-neighbour).
3. Doldurulan hücre sayısını `ozet_istatistik.csv` ve README'ye yaz; bu varsayımı README'de açıkla.

Tüm katmanlar Bio katmanlarıyla **birebir aynı ızgarada** olmalı.

### 9.6 Korelasyon
24 katman (19 Bio + 5 denizel) için Pearson korelasyon matrisi: `korelasyon_matrisi.csv`, `korelasyon_matrisi.png`, |r| > 0.8 çiftleri `yuksek_korelasyon.txt`. **Değişken seçimini sen yapma.**

### 9.7 Çıktılar (`output/`)
1. 24 adet `.asc` (ESRI ASCII Grid, EPSG:4326, aynı ncols/nrows/köşe/cellsize, `NODATA_value -9999`, ondalık ayırıcı nokta).
2. Aynı katmanların `.tif` kopyaları.
3. Her katman için önizleme `.png` (renk skalası + birim).
4. `ozet_istatistik.csv` (min, max, ortalama, NoData sayısı, doldurulan hücre sayısı).
5. `README.md` (Türkçe): veri setleri ve CDS kimlikleri, dönem, alan, çözünürlük, indirme tarihi, birim dönüşümleri, formüller, doldurma yöntemi, sınırlılıklar (0.25° ≈ enlemde ~28 km; reanaliz istasyon gözlemi değildir; kıyı pikselleri karışıktır; katmanlar hakemli değildir), atıflar: Hersbach vd. (2020) *The ERA5 global reanalysis*, QJRMS, doi:10.1002/qj.3803 + CDS veri seti DOI'leri.
6. Yorumlu, yeniden çalıştırılabilir Python kodu (`indir.py`, `bioclim_hesapla.py`, `denizel_hesapla.py` vb.) + `requirements.txt`.

Dosya/klasör adlarında **Türkçe karakter ve boşluk yok.**

### 9.8 Doğrulama (zorunlu)
- 24 `.asc` başlığının birebir aynı olduğunu programla kontrol et.
- Rothera istasyonu (~67.57°S, 68.13°W) hücresi: Bio1 birkaç derece sıfırın altında olmalı; Bio5 > Bio1 > Bio6; Bio12 > 0.
- Yaz deniz yüzeyi sıcaklığı yaklaşık −2 °C ile birkaç °C arası; kış deniz buzu > yaz deniz buzu.
- Beklenmedik NoData/NaN alanı kalmadığını göster.

### 9.9 Bitirince öğrenciye ver
- Çıktı klasörü ve içerik listesi,
- Rothera hücresindeki Bio1, Bio5, Bio6, Bio12 ve sst_yaz, buz_kis değerleri,
- Karşılaşılan sorunlar ve alınan kararlar (kısa).

### 9.10 Yapma
- MaxEnt'i çalıştırma, GBIF verisini indirme/değiştirme.
- API anahtarını hiçbir yere yazma.
- Yeniden örnekleme, alanı genişletme veya formülleri "iyileştirme".

---

## 10. Sonraki adımlar (öğrencinin yapacakları — bilgi amaçlı)

1. Danışmana ERA5 yaklaşımını onaylatmak.
2. GBIF'ten Adélie kayıtlarını (2000–2026, Marguerite Körfezi) indirmek, temizlemek, `.csv` yapmak (sütunlar: tür, boylam, enlem).
3. Korelasyon matrisine bakarak danışmanla değişken seçmek.
4. MaxEnt'e `.csv` + seçilen `.asc` katmanlarını yüklemek; AUC, jackknife, katkı tablolarını almak.
5. Haritayı QGIS'te görselleştirmek; danışmana iletmek.
6. Raporda yöntemi ve sınırlılıkları (iklim dönemi, çözünürlük, doldurma varsayımı) şeffaf yazmak.

## 11. Kaynaklar

- Vega, G. C., Pertierra, L. R. & Olalla-Tárraga, M. Á. (2017). MERRAclim. *Scientific Data* 4:170078. https://www.nature.com/articles/sdata201778
- MERRAclim verisi (Dryad): https://datadryad.org/dataset/doi:10.5061/dryad.s2v81
- Cimino, M. A. vd. (2016). *Scientific Reports* 6:28785. https://www.nature.com/articles/srep28785
- WorldClim bioclim tanımları: https://www.worldclim.org/data/bioclim.html
- WorldClim v1.4 veri formatı (Antarktika hariç): https://worldclim.org/data/v1.4/formats.html
- Copernicus ERA5 biyoklimatik göstergeler (1979–2018): https://cds.climate.copernicus.eu/datasets/sis-biodiversity-era5-global
- CHELSA-BIOCLIM+: https://envidat.ch/dataset/bioclim_plus
- Hersbach, H. vd. (2020). The ERA5 global reanalysis. *QJRMS*. doi:10.1002/qj.3803
- Phillips, S. J. vd. (2006). Maximum entropy modeling of species geographic distributions. *Ecological Modelling*.
