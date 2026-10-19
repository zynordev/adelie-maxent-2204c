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
