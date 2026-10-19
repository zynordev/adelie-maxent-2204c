# Karar Kaydı

Şablon ve kurallar: [`README.md`](README.md). Özet tablo: [`../CLAUDE.md`](../CLAUDE.md) Bölüm 2 ve 6.

> K-001 – K-011, önceki Claude sohbetinde (2026-10-16 – 2026-10-18) ve danışman toplantısında alınan kararların geriye dönük kaydıdır. Danışman toplantısı not alınmadı; öğrencinin aktarımına dayanır.

---

### K-001 — Ana görev ve iş akışı
- **Tarih:** 2026-10 (danışman toplantısı)
- **Karar veren:** Danışman
- **Durum:** Geçerli
- **Karar:** GBIF koordinatları → MaxEnt → habitat uygunluk haritası + AUC → danışmana bildir. Hedef: niş modeli oluşturmak.

### K-002 — Başarı ölçütü
- **Tarih:** 2026-10 (danışman toplantısı)
- **Karar veren:** Danışman
- **Durum:** Geçerli
- **Karar:** AUC > 0.70 başarılı sayılır; değilse model yeniden denenir.
- **Not:** Eski taslaktaki 0.80 eşiğinin yerini aldı.

### K-003 — Bio-ORACLE ve ekip rol dağılımı ertelendi
- **Tarih:** 2026-10 (danışman toplantısı)
- **Karar veren:** Danışman
- **Durum:** Geçerli (ertelendi)
- **Karar:** Bio-ORACLE ve ekip rol dağılımı şimdilik gündem dışı.

### K-004 — Çalışma alanı
- **Tarih:** 2026-10-16 – 2026-10-18
- **Karar veren:** Öğrenci
- **Durum:** Geçerli
- **Karar:** Marguerite Körfezi (Batı Antarktika Yarımadası).

### K-005 — Kayıt dönemi
- **Tarih:** 2026-10-16 – 2026-10-18
- **Karar veren:** Öğrenci
- **Durum:** Geçerli
- **Karar:** GBIF kayıtları 2000–2026.

### K-006 — Model aracı
- **Tarih:** 2026-10-16 – 2026-10-18
- **Karar veren:** Öğrenci
- **Durum:** Geçerli
- **Karar:** Klasik MaxEnt (Java GUI). Python yalnızca veri hazırlığı (ERA5 katmanları) için.
- **Gerekçe:** Danışmanın referans projesiyle aynı akış.
- **Alternatifler:** Python `elapid` (eski taslak) — bırakıldı.

### K-007 — Yazılım ortamı (Linux)
- **Tarih:** 2026-10-16 – 2026-10-18
- **Karar veren:** Öğrenci
- **Durum:** Geçerli
- **Karar:** ArcGIS / SDM Toolbox yerine QGIS + GDAL. MaxEnt `java -jar maxent.jar` ile çalıştırılır.
- **Gerekçe:** Öğrenci Linux kullanıyor; ArcGIS Linux'ta yok.

### K-008 — WorldClim kullanılmıyor
- **Tarih:** 2026-10-16 – 2026-10-18
- **Karar veren:** Öğrenci
- **Durum:** Geçerli
- **Karar:** WorldClim bioclim kullanılmayacak.
- **Gerekçe:** Öğrenci WorldClim 2.1'i indirip doğruladı: Antarktika'da veri yok. Danışmanın ilk önerisi (K-001 toplantısı) bu nedenle uygulanamıyor.
- **Kaynak:** https://worldclim.org/data/v1.4/formats.html ; Vega vd. 2017, doi:10.1038/sdata.2017.78

### K-009 — İklim kaynağı: ERA5'ten kendi bioclim katmanlarımız
- **Tarih:** 2026-10-16 – 2026-10-18
- **Karar veren:** Öğrenci
- **Durum:** Onay bekliyor (danışman)
- **Karar:** ERA5'ten 2000–2025 için Bio1–Bio19 hesaplanacak; ayrıca deniz yüzeyi sıcaklığı ve deniz buzu katmanları üretilecek. Teknik ayrıntı: `CLAUDE.md` Bölüm 9.
- **Gerekçe:** 2020'lere uzanan, Antarktika'yı kapsayan hazır bioclim yok. Adélie literatürü denizel değişkenleri öne çıkarıyor (Cimino vd. 2016).
- **Alternatifler:** K-010 (MERRAclim).
- **Kaynak:** Hersbach vd. 2020, doi:10.1002/qj.3803 ; Cimino vd. 2016, doi:10.1038/srep28785

### K-010 — Yedek iklim kaynağı: MERRAclim
- **Tarih:** 2026-10-16 – 2026-10-18
- **Karar veren:** Öğrenci
- **Durum:** Yedek
- **Karar:** ERA5 yaklaşımı onaylanmazsa MERRAclim 2000'ler (2001–2010), 10', Vmin (`10m_min_00s.zip`).
- **Not:** BIO12–BIO19 yağış değil özgül nemdir.
- **Kaynak:** Vega vd. 2017, doi:10.1038/sdata.2017.78 ; Dryad doi:10.5061/dryad.s2v81

### K-011 — ERA5 katman üretimini Claude yapacak
- **Tarih:** 2026-10-16 – 2026-10-18
- **Karar veren:** Öğrenci
- **Durum:** Geçerli
- **Karar:** `CLAUDE.md` Bölüm 9'daki teknik görevi öğrenci "başla" dediğinde Claude uygular. Diğer işlerde Claude yalnızca yol gösterir.

### K-012 — Proje kayıt sistemi
- **Tarih:** 2026-10-19
- **Karar veren:** Öğrenci
- **Durum:** Geçerli
- **Karar:** Her iş ve aşama için proje klasöründe (`docs/`) Markdown kaydı tutulur; Obsidian'dan bağımsız.
- **Gerekçe:** Profesyonel ve izlenebilir ilerleme; raporun Yöntem bölümüne temel.

### K-013 — Günlük sıcaklık saatlik ERA5'ten hesaplanıyor
- **Tarih:** 2026-10-19
- **Karar veren:** Claude (öğrencinin isteğiyle yürütülen ERA5 görevi kapsamında; sonuç değişmediği için yöntemsel değil teknik karar)
- **Durum:** Geçerli
- **Karar:** Günlük Tmax/Tmin, `derived-era5-single-levels-daily-statistics` yerine `reanalysis-era5-single-levels` (saatlik 2 m sıcaklık) indirilip yerelde hesaplanır: UTC günü içindeki 24 saatlik değerin maks/min'i.
- **Gerekçe:** Günlük istatistik veri setinin CDS kuyruğu çok yavaştı (istekler 35 dk'da hiç başlamadı; aynı anda yalnızca birkaç istek kabul ediliyor). Saatlik istek 13 sn'de başladı, yılı ~13 dk'da indi. 2000 ve 2001 yılları için iki yol karşılaştırıldı: 731 gün × 703 hücrenin **tamamında fark 0.0 K** (`era5/saatlik_gunluk_karsilastir.py`).
- **Alternatifler:** Günlük istatistik veri setini beklemek (52 istek, tahmini saatler–günler).
- **Kaynak:** CDS DOI 10.24381/cds.adbb2d47 (saatlik), 10.24381/cds.4991cf48 (günlük istatistik)

### K-014 — Günlük maks/min için UTC günü
- **Tarih:** 2026-10-19
- **Karar veren:** Claude (CDS varsayılanı korunarak)
- **Durum:** Geçerli
- **Karar:** Gün sınırı UTC 00:00. Yerel saat (≈UTC−4/−5) kullanılmadı.
- **Gerekçe:** CDS günlük istatistik ürününün varsayılanı; aylık ortalamalara etkisi ihmal edilebilir düzeyde. README'de sınırlılık olarak belirtilecek.

### K-015 — Denizel katmanlarda kara hücresi doldurma: küresel en yakın komşu
- **Tarih:** 2026-10-19
- **Karar veren:** Claude (`CLAUDE.md` 9.5 uygulanırken)
- **Durum:** Geçerli
- **Karar:** SST ve deniz buzunda NaN olan 364 kara hücresine, küre üzerindeki gerçek uzaklığa göre en yakın deniz hücresinin değeri atanır. Ham (doldurulmamış) sürüm `era5/output/ham/` altında.
- **Gerekçe:** 68°G'de 1° boylam ≈ 0.37° enlem uzunluğundadır; ızgara indeksine göre "en yakın" seçmek doğuya/batıya yanlı olurdu.

### K-016 — Deniz yüzeyi tuzluluğu (öneri)
- **Tarih:** 2026-10-19
- **Karar veren:** Öğrenci (netleştirme bekleniyor) → Danışman
- **Durum:** Onay bekliyor
- **Karar:** Öğrenci "deniz tuzu" değişkeninin eklenmesini önerdi. Kastedilenin deniz buzu mu (zaten planda) yoksa tuzluluk mu olduğu soruldu.
- **Not:** ERA5'te tuzluluk yok. CDS'te ORAS5 (`reanalysis-oras5`, `sea_surface_salinity`, aylık, CC-BY, DOI 10.24381/cds.67e8eeb7) var; ancak alan kırpma yok (küresel dosyalar) ve ORCA025 ızgarasında → ERA5 ızgarasına yeniden örnekleme gerekir (Bölüm 9.10 kuralına bilinçli istisna olur).

### K-017 — GBIF indirmesi API ile, öğrencinin isteğiyle Claude tarafından
- **Tarih:** 2026-10-19
- **Karar veren:** Öğrenci
- **Durum:** Geçerli
- **Karar:** GBIF kayıtları resmi indirme API'siyle (`gbif/indir_gbif.py`, öğrencinin hesabı) indirilir. Ürün sitedeki "Download → Simple" ile aynıdır (SIMPLE_CSV + DOI). Filtre `gbif/sorgu.json`'da saklanır. Temizlik ve seçim kararları öğrencide kalır.
- **Filtre:** taxonKey 2481663 (GBIF Backbone) · yıl 2000–2026 · koordinatlı · coğrafi sorun yok · occurrenceStatus = PRESENT · iklim katmanlarının sınırı (73.125°B–63.875°B, 70.625°G–65.875°G). 2026-10-19 itibarıyla arama API'sinde 1001 kayıt.
- **Gerekçe:** GBIF sitesinde aynı filtreler 0 sonuç verdi. Ekran görüntüsünde filtre "Scientific name: 2481663" olarak görünüyordu; sitenin varsayılan taksonomi listesi Backbone değil, bu numarayı tanımıyor. API'de `checklistKey` = Backbone açıkça verildi.
- **Gizlilik:** GBIF şifresi yalnızca `~/.gbif_sifre` dosyasında (izin 600, öğrenci oluşturdu); hiçbir proje dosyasına/commit'e yazılmaz.

### K-018 — GBIF temizlik kuralları ve seyreltme
- **Tarih:** 2026-10-19
- **Karar veren:** Claude (öğrencinin isteğiyle; öğrenci + danışman gözden geçirecek)
- **Durum:** Onay bekliyor (öğrenci + danışman)
- **Karar:** `gbif/temizle.py` sırasıyla: (1) ERA5 alanı dışını at · (2) `coordinateUncertaintyInMeters` > 10 km at · (3) konum adı yalnızca bölge olanları at ("Western Antarctic Peninsula" — 42 INSDC kaydı tek noktada; "Marguerite Bay Antartica" — 2 kayıt, körfez merkezi) · (4) belirsizliği yok + iki koordinat 0.5°'nin tam katı olanları at (yer tutucu; şu an 0) · (5) aynı koordinat + aynı tarih tekrarlarını teke indir · (6) ERA5 hücresi başına 1 nokta (en küçük belirsizlikli kayıt). Sonuç: 1001 → 704 temiz kayıt → **67 MaxEnt noktası** (19 kara, 48 deniz hücresi).
- **Gerekçe:** ERA5 hücresinin dar kenarı ≈ 10.4 km; daha büyük belirsizlikli kayıt hücreye güvenle atanamaz. Seyreltme MaxEnt'in "remove duplicate presence records" davranışıyla aynıdır, sayıyı şeffaf kılar. Belirsizliği bilinmeyen 420 kayıt tutuldu (çoğu kaynak bu alanı doldurmuyor).
- **Denenip geri alınan:** Ondalık basamak sayısına göre eleme. Metinde sondaki sıfırlar kaybolduğu için hassas kayıtlar (ör. iNaturalist, Stonington Adası, 160 m belirsizlik) haksız elendi.
- **Açık nokta:** Kara (koloni) ve deniz (beslenme/gemi gözlemi) kayıtları birlikte tutuldu → danışmanla konuşulacak.

### K-019 — Uzak depo: private GitHub
- **Tarih:** 2026-10-19
- **Karar veren:** Öğrenci
- **Durum:** Geçerli
- **Karar:** Proje `zynordev/adelie-maxent-2204c` (**private**) deposunda. Commit yazarı: Halil Erdem Yanık `<159820410+zynordev@users.noreply.github.com>` (GitHub noreply adresi; commit'ler hesaba bağlanır, gerçek e-posta geçmişe yazılmaz). Mevcut 6 yerel commit push öncesi bu kimlikle yeniden yazıldı.
- **Depoda olmayanlar:** `.venv/`, ham veriler (`era5/veri_ham/`, `gbif/ham/` — scriptlerle yeniden indirilebilir), CDS anahtarı ve GBIF şifresi (proje dışında; her push öncesi tüm geçmiş taranır).
