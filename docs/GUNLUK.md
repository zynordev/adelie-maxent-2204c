# Çalışma Günlüğü

Şablon: [`README.md`](README.md). En yeni kayıt en üstte.

---

## 2026-10-20 — QGIS için harita katmanları (Aşama 7 🟡)

**Yapılanlar**
- Laptop'ta QGIS kurulumu: CachyOS paket listesi eskiydi (16 Ekim) ve ilk ayna (mirror.bali0531.hu) paket yerine HTML yönlendirme döndürüyordu ("bozuk paket / imza hatası" sanıldı, gerçek bozulma yoktu). Çözüm: `cachyos-rate-mirrors` → `pacman -Syu` → `pacman -S qgis` (öğrenci yaptı).
- `harita/hazirla.py` → `harita/qgis_katmanlari.gpkg` (kiyi: SCAR ADD kıyı çizgisi v7.11, Gerrish vd. 2025, doi:10.5285/7d6793c2-2513-4752-8f37-11db5b791fb5, alana kırpıldı; noktalar: 67; istasyonlar: Rothera, San Martín, Horseshoe Adası) + `harita/uygunluk_ortalama.tif` (deneme3 ortalaması, EPSG:4326 tanımlı). Vektörler EPSG:3031.

- QGIS'te 4326 → 3031 anlık dönüşüm uygunluk hücrelerini bulanık gösterdi → `harita/uygunluk_ortalama_3031.tif`: 1 km ızgara, en yakın komşu (değerler değişmedi: 702 benzersiz değerin tamamı kaynaktakiyle aynı).

- Öğrencinin ilk baskı düzeni taslağı (`harita2_A4.pdf`, 2026-10-26) incelendi. Kırpılmış kıyı poligonlarının kesim kenarları açık denizde çizgi olarak görünüyordu → `kiyi_cizgi` katmanı eklendi (sınır önce çıkarılıp sonra kırpılıyor).

**Sıradaki adım**
- Öğrenci: QGIS'te harita (projeksiyon EPSG:3031, renk skalası, lejant, ölçek, kuzey oku, kaynaklar).

---

## 2026-10-20 — İlk MaxEnt denemesi (Aşama 6 🟡)

**Yapılanlar**
- Öğrenci MaxEnt 3.4.4'ü laptop'ta çalıştırdı. Laptop'taki Java 27'de MaxEnt açılırken çöktü (`checkVersion` sürüm adının ilk 3 karakterini okuyor, "27" 2 karakter) → Java 21 kuruldu, MaxEnt doğrudan onunla çalıştırıldı (varsayılan Java 27 kaldı).
- **deneme1:** Test AUC **0.781**, Training AUC 0.819 (hedef > 0.70 ✔). Çıktılar Pi'deki repoya kopyalandı: `maxent/cikti/deneme1/`.
- **Hata bulundu ve düzeltildi:** MaxEnt 67 yerine 66 nokta kullandı. 66.875°G hücre sınırındaki bir nokta için `gbif/temizle.py` satırı kuzeyden, MaxEnt güneyden sayıyor → farklı hücre. Script MaxEnt kuralına uyduruldu; yeni dosyada 67 nokta, sınırda nokta yok, MaxEnt'te tekrar yok.

- **deneme2** (10 katlı çapraz doğrulama, 67 nokta): ortalama Test AUC **0.768 ± 0.111** (MaxEnt; katlar 0.518–0.916). Permütasyon önemi en yüksek buz_yillik (55.6). Jackknife bu çalıştırmada işaretlenmemişti. Çıktılar `maxent/cikti/deneme2/`.

- **deneme3** (ÇD + jackknife): sonuçlar deneme2 ile birebir aynı (tekrarlanabilir). Jackknife: tek başına en çok bilgi bio18 (eğitim kazancı 0.287, test AUC 0.732); çıkarılınca en çok kayıp buz_yillik (0.592 → 0.441); kaya çıkarılınca test AUC hafifçe artıyor (0.768 → 0.772). Tablo: `maxent/cikti/deneme3/NOT.md`. **Raporda kullanılacak çalıştırma bu.**

**Sıradaki adım**
- Aşama 7: `deneme3/Pygoscelis_adeliae_avg.asc` → QGIS haritası.

---

## 2026-10-20 — Değişken önerisi ve buzsuz kaya katmanı

**Yapılanlar**
- Öğrenci değişkenleri önerdi: kaya, bio18, sst_yillik, buz_yillik; üreme sıcaklığında karar veremedi (K-020, danışman onayı bekliyor). Seçilenler arası en yüksek |r| = 0.65.
- Buzsuz kaya katmanı üretildi (K-021): SCAR ADD v7.11 (288 MB GeoPackage, boyutu katalogla aynı) → `era5/output/kaya.asc/.tif/.png`. 343/703 hücrede kaya, en yüksek %15.3.
- 25 katmanla korelasyon ve doğrulama yeniden çalıştı: tüm kontroller geçti.
- Öğrenci üreme mevsimi sıcaklığını **eklememeye** karar verdi (K-020). MaxEnt girdi klasörü hazırlandı: `maxent/girdi/` (4 katman + 67 nokta; başlıklar aynı, NoData'ya düşen nokta yok).
- **Bulgu:** ERA5'in "deniz" saydığı 48 penguen hücresinin 33'ünde kaya var → bunlar küçük adalardaki koloniler; 16 hücrede kaya yok → büyük olasılıkla deniz gözlemleri.

---

## 2026-10-20 — Değişken seçimi için literatür taraması

**Yapılanlar**
- `docs/literatur/degisken_literaturu.md` hazırlandı: 9 kaynak, hepsinin künyesi doi.org/Crossref'ten doğrulandı. Ana referans: Cimino vd. 2016 (Adélie, MaxEnt + GAM, değişkenler yaz SST + yaz SIC + buzsuz kaya, AUC > 0.85).
- Gemini worker sistemi (hk_agents, 15 worker) paralel çalıştırıldı; önerdiği 9 DOI'nin 4'ü yanlış/uydurma çıktı → çıktısı kullanılmadı, ham dosya silindi.
- Kendi verimizden: en sıcak çeyrek her hücrede yaz (Ara–Şub / Oca–Mar), en soğuk her hücrede kış → bio10/bio18 üreme mevsimi, bio11/bio19 kış. En yağışlı/kurak çeyrek yerden yere farklı → **bio8/bio9 haritalarında yapay kesintiler** (Booth 2022 ile uyumlu).
- |r| > 0.7 (Dormann vd. 2013 eşiği) → 64 çift; |r| > 0.8 → 49 çift.

**Sıradaki adım**
- Öğrenci + danışman: Bölüm 8'deki 5 soruyu konuşup değişkenleri seçmek.

---

## 2026-10-20 — ERA5 katmanları tamamlandı (Aşama 3 ✅)

**Yapılanlar**
- Saatlik 2 m sıcaklık indirmesi 01:51'de bitti (26/26 yıl). `hepsini_calistir.sh` 01:52–01:53'te zinciri otomatik çalıştırdı: biovars testi ✔ → saatlik/günlük eşdeğerlik (2000, 2001: fark 0.0 K) ✔ → denizel → bioclim → korelasyon → doğrulama: **tüm kontroller geçti**.
- `era5/output/README.md` yazıldı (veri setleri + DOI, dönem, alan, birimler, formüller, doldurma, doğrulama, sınırlılıklar, atıflar). Veri seti atıfları DOI kayıt sisteminden (DataCite) doğrulandı; ezberden yazılan yazar/yıl yanlıştı, düzeltildi.
- Push öncesi elle yapılan gizli bilgi taramasında komut hatası fark edildi (tarama çalışmadan push yapılmıştı). Tüm geçmiş doğru komutla yeniden tarandı: temiz. Kalıcı çözüm: `.git/hooks/pre-push` kancası, her push'ta gönderilen commit'lerde CDS anahtarı/GBIF şifresi arar ve bulursa push'u engeller; sahte anahtarla geçici depoda test edildi (temiz → geçti, sızıntı → engellendi). Not: kanca `.git/` içinde olduğu için repoya gitmez, yalnızca bu bilgisayarda geçerlidir.

**Sonuçlar**
- 24 katman (`.asc` + `.tif` + `.png`), ızgara 37 × 19, 0.25°, NoData yok.
- Rothera hücresi (67.50°G, 68.25°B; deniz): Bio1 −6.78 °C · Bio5 −0.23 °C · Bio6 −14.76 °C · Bio12 1341 mm · sst_yaz −1.45 °C · buz_kis %58.6.
- Korelasyon: 49 çift |r| > 0.8 (sıcaklık grubu bio1/5/6/10/11 ve yağış grubu bio12–19 kendi içinde çok yüksek; sst_yillik–sst_yaz 0.98; buz_yillik–buz_yaz 0.98).

**Sıradaki adım**
- Öğrenci + danışman: korelasyon matrisine bakarak değişken seçimi (Aşama 5). Açık sorular: K-009 (ERA5 onayı), K-016 (tuzluluk), K-018 (GBIF kuralları + kara/deniz kayıtları).

---

## 2026-10-19 — ERA5 katman üretimi başladı (Aşama 2 ✅, Aşama 3 🟡)

**Yapılanlar**
- CDS API anahtarı `~/.cdsapirc` dosyasına yazıldı (izin 600; anahtar hiçbir proje dosyasında/commit'te yok — kontrol edildi).
- CDS veri seti adları, değişkenler ve DOI'ler katalog API'sinden doğrulandı.
- `era5/` altında sanal ortam ve scriptler: `indir.py`, `biovars.py`, `test_biovars.py`, `bioclim_hesapla.py`, `denizel_hesapla.py`, `korelasyon.py`, `dogrula.py`, `saatlik_gunluk_karsilastir.py`.
- `biovars()` elle hesaplanmış sentetik örnekle test edildi: 19 değişkenin tamamı geçti.
- Aylık yağış, SST ve deniz buzu (2000–2025) indi. 5 denizel katman üretildi; 364 kara hücresi küresel en yakın komşu ile dolduruldu (K-015).
- Saatlik 2 m sıcaklık indiriliyor (yıl başına ~12 dk; CDS aynı anda tek iş işliyor).

**Sorunlar / notlar**
- CDS günlük istatistik veri seti kuyruğu çok yavaş + eşzamanlı istek sınırı ("Number queued requests for this dataset is temporarily limited"). Saatlik veriye geçildi; 2000 ve 2001'de sonuç birebir aynı (fark 0.0 K) → K-013.
- rasterio 1.5.2 (ARM) içindeki GDAL 3.12.2 açılışta zararsız "apszKnownConfigOptions" satırları basıyor; `CPL_LOG` ile susturuldu.
- Öğrenci "deniz tuzu" eklemek istedi; deniz buzu mu tuzluluk mu netleşmedi → K-016.
- Öğrenci önizleme PNG'lerinin kalitesizliğini belirtti. Yenilendi: 220 dpi, gerçek en/boy oranı, °G/°B eksenler, Rothera işareti, kaynak dipnotu; kıyı çizgisi hücre merkezlerinden geçen kontur yerine hücre kenarlarını izleyen basamaklı sınır. Pikseller bilerek yumuşatılmadı (0.25° verinin gerçek çözünürlüğü; enterpolasyon olmayan ayrıntı gösterirdi). Rapor haritaları Aşama 7'de QGIS'te yapılacak.
- Hesaplama zinciri 7 yıllık veriyle (2000–2006) deneme olarak uçtan uca çalıştırıldı: tüm doğrulama kontrolleri geçti.
- GBIF: sitede filtreler 0 sonuç verdi (site varsayılan taksonomi listesi taxonKey 2481663'ü tanımıyor). Öğrencinin isteğiyle resmi indirme API'siyle indirildi (K-017): **1001 kayıt, 8 veri seti, DOI 10.15468/dl.jt3gt7** → `gbif/ham/0034792-260928105237408.zip`. Sorgu `gbif/sorgu.json`, bilgiler `gbif/indirme_bilgisi.json`.
- GBIF temizliği (öğrencinin isteğiyle, K-018): `gbif/temizle.py` → 1001 → 704 temiz kayıt → **67 MaxEnt noktası** (`gbif/temiz/adelie_maxent.csv`). Atılan her kayıt nedeniyle `gbif/temiz/atilan_kayitlar.csv`'de; adım tablosu `gbif/temiz/temizlik_raporu.md`; kontrol haritası `gbif/temiz/noktalar.png`. Ondalık sayısına göre eleme denendi, hassas kayıtları haksız elediği için geri alındı.
- **ERA5 yavaşlığının bir nedeni bulundu:** Laptop'ta önceki sohbetten kalan `~/marguerite_bioklim/indir.py` 2026-10-18 21:34'ten beri aynı CDS anahtarıyla günlük istatistik veri setinden indirme yapıyordu (23 saatte 3 dosya) ve CDS'teki kullanıcı sırasını Pi ile paylaşıyordu. Öğrencinin onayıyla durduruldu (21:05), kuyruktaki isteği silindi. Laptop'taki klasöre dokunulmadı. Kuyrukta "sahipsiz" sanılan günlük istatistik istekleri (1fc69cab, d92bf99c) bu scriptindi.
- Öğrencinin isteğiyle private GitHub deposu açıldı: `zynordev/adelie-maxent-2204c` (K-019). Commit'ler öğrencinin adıyla (GitHub noreply e-postası), tüm geçmiş push öncesi gizli bilgi için tarandı.

**Sıradaki adım**
- İndirme bitince: `bioclim_hesapla.py` → `korelasyon.py` → `dogrula.py`, çıktı README'si.
- Öğrenci: "deniz tuzu" sorusunu yanıtlamak; danışmana ERA5 yaklaşımını sormak; K-018 temizlik kurallarını gözden geçirmek; kara+deniz kayıtlarını danışmana sormak.

---

## 2026-10-19 — Proje klasörü ve kayıt sistemi kuruldu

**Yapılanlar**
- Önceki sohbetin bağlam dosyası (`CLAUDE.md`) proje klasörüne kaydedildi.
- `CLAUDE.md`'ye kayıt tutma kuralı eklendi (Bölüm 0, madde 7).
- Kayıt sistemi kuruldu: günlük, karar kaydı, aşama takibi, toplantı notları klasörü.
- Önceki sohbet ve danışman toplantısının kararları geriye dönük olarak K-001 – K-011 şeklinde numaralandırıldı.

**Üretilen / değişen dosyalar**
- `CLAUDE.md`, `README.md`
- `docs/README.md`, `docs/GUNLUK.md`, `docs/KARARLAR.md`, `docs/ASAMALAR.md`, `docs/toplantilar/`

**Sorunlar / notlar**
- Danışman toplantısının tarihi kesin bilinmiyor (Ekim 2026); öğrenci hatırlarsa K-001 – K-003 güncellenebilir.

**Sıradaki adım**
- Öğrenci: danışmana ERA5 yaklaşımını sormak (Aşama 1), CDS hesabını hazırlamak (Aşama 2).

---

## 2026-10-16 – 2026-10-18 — Önceki Claude sohbeti (geriye dönük özet)

**Yapılanlar**
- Danışman toplantısı kararları netleştirildi (AUC > 0.70, klasik MaxEnt, Bio-ORACLE ertelendi).
- WorldClim'in Antarktika'yı kapsamadığı doğrulandı (öğrenci indirip kontrol etti).
- Alternatifler araştırıldı: MERRAclim (2001–2010), Copernicus ERA5 biyoklimatik göstergeler (1979–2018, 0.5°), CHELSA-BIOCLIM+.
- ERA5 ham verisinden 2000–2025 Bio1–Bio19 + denizel katmanlar üretme planı hazırlandı.
- Adélie MaxEnt literatürü ve özgünlük konusu incelendi (Cimino vd. 2016).

**Sıradaki adım**
- Danışman onayı, CDS hazırlığı, ERA5 katman üretimi.
