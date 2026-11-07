# CMIP6 erişimi ve gerçek bölgesel aylık girdiler

Tarih: 2026-11-08, Europe/Istanbul. Bu yan çalışma yalnızca CMIP6 erişimi,
kaynak izlenebilirliği ve bölgesel aylık alan üretimini kapsar. Genel bulunuş
yorumu, ERA5'in 2000–2025 tabanı ve mevcut 0,25° analiz ızgarası değiştirilmedi.

## Gerçek tamamlanma durumu

**IPSL-CM6A-LR / r1i1p1f1 için tos, siconc, pr, tas gerçek bölgesel aylık
verileri üretildi.** Historical 2000–2014 ile aynı üyenin SSP2-4.5
2015–2025 devamı birleştirildi; gelecek dönem SSP2-4.5 2041–2060.
Her değişken için 312 aylık baseline, 240 aylık gelecek ve iki dönemin
12 aylık klimatolojileri mevcut. Bu, yalnızca katalog bulunabilirliği değildir.

Henüz tamamlanmayanlar: bu alanların ERA5 ızgarasına taşınması, delta/bias
yöntemi, kıyı ve kara doldurma politikası, BIO18 ve diğer nihai ASC katmanları,
MaxEnt projeksiyonu ve bilimsel geçerlilik değerlendirmesi. Bunlar ana çalışma
tarafından ele alınır. Bu yan çalışma hiçbir nihai habitat sonucu üretmez;
çoklu GCM ensemble üretildiği iddia edilmez.

## Çıktı sözleşmesi

Proje köküne göre klasör:
`maxent/girdi/cmip6_2041_2060/IPSL-CM6A-LR_r1i1p1f1/`.

Her `{var}` için (`tos`, `siconc`, `pr`, `tas`) dört dosya:

- `{var}_baseline_2000_2025.nc`: `{var}(time=312,y,x)`,
  `days_in_month(time)`, gerçek aylık tarih koordinatları.
- `{var}_future_2041_2060.nc`: aynı yapı, `time=240`.
- `{var}_aylik_klimatoloji.nc`: `{var}(period=2,month=12,y,x)`.
- `{var}_aylik_klimatoloji.npz`: NumPy ile doğrudan okunabilen eşdeğer alanlar.

NetCDF'de `period=[0,1]`: 0=baseline 2000–2025, 1=SSP2-4.5 2041–2060;
`month=1..12`. `latitude(y,x)`, `longitude(y,x)` iki boyutludur;
boylam −180…180 aralığındadır. `y`, `x` kaynak dosyadaki gerçek hücre indisleridir.
`period_start_year`, `period_end_year`, `valid_year_count(period,month,y,x)` ve
`mean_days_in_month(period,month)` ayrıca bulunur.

NPZ anahtarları: `baseline`, `future` (12,y,x); `lat`, `lon` (y,x);
`month`, `units`, `baseline_valid_year_count`, `future_valid_year_count`,
`baseline_mean_days_in_month`, `future_mean_days_in_month`.
Yüklerken `np.load(path, allow_pickle=False)` yeterlidir.

| Alan | Klimatoloji boyutu | Birim | Kaynak ızgara |
|---|---|---|---|
| tos | 2×12×15×11 | °C (`degC`) | Omon, gn, yerel eğrisel okyanus |
| siconc | 2×12×15×11 | % | SImon, gn, yerel eğrisel okyanus |
| pr | 2×12×5×6 | mm/ay (`mm month-1`) | Amon, gr, LMDZ atmosfer |
| tas | 2×12×5×6 | °C (`degC`) | Amon, gr, LMDZ atmosfer |

Bölgesel istek sınırı K/B/G/D = `[-66,-73,-70.5,-64]`.
Bu sınırdaki kaynak hücrelerin çevresine bir kaynak hücresi pay eklenerek
dikdörtgen indis dilimi alındı. Bu nedenle bazı hücreler istek sınırının
dışındadır. Atmosfer koordinatları yaklaşık −70,986…−65,915° enlem,
−75…−62,5° boylam; okyanus −70,838…−65,703° ve −73,501…−63,5°.
Bu pay gelecekteki yeniden ızgaralama için bırakılmıştır; analiz alanını büyütmez.

Kara boşlukları **NaN** olarak korunur. Deniz alanlarında her ay 76 geçerli
kaynak hücresi vardır; diğer 89 hücrede veri yoktur. Atmosferde 30 hücrenin
tamamı geçerlidir. Geçerli her hücre/ay için baseline yıl sayısı 26, gelecek 20;
kısmi yıllara dayanarak tam klimatoloji üretildiği iddia edilmez.

## Canlı erişim ve adaylar

İlk kontrol Pangeo CSV + konsolide Zarr metadata + gerçek zaman koordinatı
okumasıyla yapıldı. 24 dataset için HTTP 200 metadata ve örnek veri nesnesinde
HEAD yanıtı alındı. HEAD, bütün veri parçalarının okunması veya bölgesel
değerlerin geçerli olduğunun kanıtı değildir. Zaman koordinatları ise gerçekten
indirilip Blosc açılarak kontrol edildi; yalnızca metadata başlangıç tarihi ve
shape değerlerinden kapsam tahmini yapılmadı.

| GCM / üye | Historical sürüm | SSP245 sürüm | Izgara tos/siconc; pr/tas | Takvim | Sonuç |
|---|---|---|---|---|---|
| IPSL-CM6A-LR / r1i1p1f1 | 20180803 | 20190119 | gn; gr | gregorian; SSP siconc proleptic_gregorian | 8/8 erişim doğrulandı; bölgesel üretildi |
| GFDL-ESM4 / r1i1p1f1 | 20190726 | 20180701 | gn; gr1 | noleap | 8/8 erişim doğrulandı; bölgesel üretilmedi |
| MPI-ESM1-2-LR / r1i1p1f1 | 20190710 | 20190710 | gn; gn | proleptic_gregorian | SSP tas zaman sırası sorunu; üretime alınmadı |

Her kaynağın bütün URL'leri, özgün birimleri, koordinat tanımları, grid şekli,
chunk boyutları, parent model/üye, sürüm, lisans ve tracking ID bilgileri
`maxent/girdi/cmip6_2041_2060/erisim_envanteri.json` içindedir.
`istek_envanteri.json` üç dönem parçası × dört değişken × üç model = 36 planlı
istek kaydı taşır. Bu dosyanın `planned_not_submitted` durumu ilk katalog
kontrolüne aittir; sonradan gerçekleşen OPeNDAP üretiminin kaydı
`bolgesel_uretim_envanteri.json` dosyasındadır.

IPSL takvim etiketleri özgün halleriyle kaydedildi. Gregorian ve proleptic
Gregorian bu verilerin 1850 sonrası tarihlerinde aynı günleri verir; label
farkı tek başına tarih uyumsuzluğu sayılmadı. GFDL noleap ile aynı takvim gibi
işlem yapılmadı. Farklı modellerin alanları birleştirilmedi.

MPI SSP tas zaman dizisinde 1032 benzersiz ayın tümü bulunuyor ancak sıra
2095–2100, 2075–2094, 2055–2074, 2035–2054, 2015–2034 bloklarından oluşuyor.
Bu yüzden `time_coverage_incomplete` etiketi eksik ay olduğu anlamına gelmez:
betiğin sıralılık kabul koşulu sağlanmıyor. Veri-zaman eşleşmesi incelenmeden
yalnızca koordinatları sıralamak doğru olmaz. Model burada otomatik onarılmadı.

Katalog snapshot'ı 80.751.521 bayt; SHA256:
`a19a343d57f3137d11ce89e07e4c66586ed02e3d396361bf209eb7a324328b89`.
Sunucunun Last-Modified tarihi 2022-06-28'dir. Canlı erişilmiş olması bunun
ESGF'nin en yeni bütün sürümlerini içerdiğini göstermez. Güncel Pangeo/LEAP
2.0 QC kataloğu da canlı incelendi; seçilen IPSL sürümleri aynı Zarr URL'lerini
gösteriyordu. Üretim sırasında ESGF `latest=true` dosya sorguları ayrıca yapıldı;
seçilen özgün CEDA sürümleri Pangeo envanteriyle birebir eşleştirildi.

## Zarr yerine gerçek bölgesel erişim

İncelenen 24 Zarr'ın veri parçaları tüm yerel küresel uzamsal ızgarayı kapsıyor.
Bir parçanın açılmış boyutu yaklaşık 36–275 MiB; bölgesel `.sel()` bu parçayı
sunucuda kırpmaz. Bu nedenle küresel iklim parçaları indirilmedi.

ESGF DKRZ arama servisi, sekiz IPSL özgün dosyasının çalışan CEDA OPeNDAP
erişimini verdi. PyDAP üzerinden zaman ve iki uzamsal indis dilimi sunucuya
iletildi. Küresel koordinat dizileri yaklaşık 1 MB düzeyinde okundu; iklim
alanları yalnızca bölgesel hyperslab olarak okundu. On altı çıktı toplamı
yaklaşık 1,9 MB'dir; yüzlerce MB'lık özgün dosyalar indirilmedi.

`bolgesel_uretim_envanteri.json`: sekiz özgün dosya URL'si, canlı ESGF sorgu
URL/yanıt hashleri, özgün dosya ID/checksum/tracking ID, sürüm, native dilimler,
takvim, kaynak birimler, dönüşmüş serilerin boyut/aralıkları, 16 yerel dosyanın
SHA256 değerleri ve ortam sürümleri. Özgün global dosya checksum'u **ESGF'nin
bildirdiği** checksum'dur; dosyanın tamamı indirilip doğrulanmış değildir.
Yerel alt küme checksum'ları yerelde gerçekten hesaplandı ve tekrar kontrol edildi.

## Dönüşümler ve doğrulama sınırları

- `tas`: K − 273,15; `tos`: özgün degC korundu.
- `siconc`: özgün yüzde korundu; 0…100 sınırı kontrol edildi.
- `pr`: kg m⁻² s⁻¹ × 86400 × **o gerçek ayın gün sayısı** → mm/ay.
  Önce her yılın ayı dönüştürüldü, ardından takvim ayı ortalaması alındı.
  Böylece şubatın artık günleri ve 26/20 yıllık dönem farkı korunur.
- Her takvim ayının yıllar arası aritmetik ortalaması alındı. Yıllık ortalama
  veya mevsim tanımı bu yan çalışmada seçilmedi.
- DAP2 `_FillValue/missing_value=1e20` işareti float32/float64 yuvarlama farkıyla
  gelebiliyor. Yalnızca bildirilen eksik değer işareti toleranslı eşleşmeyle
  NaN'a çevrildi; fiziksel değerlere doldurma veya kırpma uygulanmadı.

Doğrulama kaydı `bolgesel_dogrulama.json` içindedir: 16 yerel dosya hash'i;
8 seri için 312/240 aylık kapsama, aylık klimatolojinin seriden yeniden hesabı,
NetCDF/NPZ eşitliği, koordinat ve tam yıl sayısı kontrolü; her değişkende
2000, 2015 ve 2041 ocaklarından birer hücrenin bağımsız küçük CEDA `.ascii`
sorgusuyla karşılaştırılması. Kaynak ASCII hassasiyetiyle 12 karşılaştırma geçti.
İzlenebilirlik ve sayısal tutarlılık, bağımsız gözlemsel iklim doğrulaması değildir.

IPSL bölgesel/paylı SST serisinde baseline en yüksek tek ay/hücre 8,781 °C,
gelecekte 10,936 °C görüldü. Baseline uç değeri ayrıca özgün kaynaktan tek hücre
ASCII isteğiyle doğrulandı; veri sessizce değiştirilmedi. Antarktika kıyı
maskesi/model yanlılığı ve uç değerlerin fiziksel uygunluğu ayrıca incelenmelidir.
Bu ham değerler doğrudan ERA5 yerine geçirilmemeli; kaynak içi aylık delta
yaklaşımı bile model yanlılığı sınırlılığını ortadan kaldırmaz.

## Yeniden çalıştırma ve ortam

Kaynak betik `maxent/cmip6_erisim_kontrolu.py`.
Erişim kontrolü Python standart kütüphanesiyle çalışır; zaman koordinatının
Blosc açılımında zaten sistemde kurulu `libblosc.so.1` kullanılır.

```bash
cd /home/halil/adelie-maxent-2204c
python3 maxent/cmip6_erisim_kontrolu.py --output-dir /yeni/klasor
uv venv .venv-cmip --python /usr/bin/python3
uv pip install --python .venv-cmip/bin/python xarray pydap scipy cftime
.venv-cmip/bin/python maxent/cmip6_erisim_kontrolu.py --regional --output-dir /yeni/klasor --timeout 60
```

Mevcut ortam varsa tekrar oluşturmak gerekmez. İlk erişim kontrolünün çıkış
kodu 2 olabilir: üç adaydan MPI sıralılık koşulunu sağlayamıyor. Envanter yine
yazılır; IPSL sekiz kaynağı doğrulanmışsa `--regional` bağımsız çalışır.
Başarılı bölgesel üretim çıkış kodu 0'dır. Mevcut bölgesel seri dosyalarının
üzerine yazılmaz; tekrarda yeni çıktı klasörü seçilmelidir. Erişim envanterini
yerinde yenilemek için ayrı `--overwrite` seçeneği vardır.

İzole `.venv-cmip` kullanıldı; global Python/GDAL bağımlılıklarına dokunulmadı.
Python 3.14'te Zarr 2'nin eski numcodecs sürümü derlenemedi; bu yol bırakıldı.
Başarılı yol xarray 2026.9.0, PyDAP 3.5.11, NumPy 2.5.4, SciPy 1.18.1,
cftime 1.6.6.1 ve requests 2.34.2 kullandı. Ana paket sürümleri üretim
envanterinde bulunur; hesap veya lisans kabulü değişikliği yapılmadı.
Kimlik dosyalarında sadece varlık kontrolü yapıldı; içerik okunmadı.
OPeNDAP oturumunda `.netrc` ve ortamdan kimlik edinimi `trust_env=False`
ile kapatıldı. API anahtarı gerekmeyen public erişim kullanıldı.

## Birincil kaynaklar

- [Copernicus CMIP6](https://cds.climate.copernicus.eu/datasets/projections-cmip6?tab=overview):
  historical 2014 sonu ve SSP 2015 başlangıcı, aylık değişkenlerin fiziksel anlamı.
- [Pangeo erişim belgesi](https://pangeo-data.github.io/pangeo-cmip6-cloud/accessing_data.html)
  ve [Zarr organizasyonu](https://pangeo-data.github.io/pangeo-cmip6-cloud/overview.html).
- [Pangeo katalog tanımı](https://storage.googleapis.com/cmip6/pangeo-cmip6.json)
  ve [CSV](https://storage.googleapis.com/cmip6/pangeo-cmip6.csv).
- [Pangeo/LEAP 2.0 sağlayıcı deposu](https://github.com/leap-stc/cmip6-leap-feedstock),
  [QC katalog tanımı](https://storage.googleapis.com/cmip6/cmip6-pgf-ingestion-test/catalog/catalog.json).
- [ESGF DKRZ arama servisi](https://esgf-data.dkrz.de/esg-search/search/):
  tam parametreli sorgular üretim envanterinde saklıdır.
- [IPSL SSP tos özgün CEDA metadata/erişim sayfası](https://esgf.ceda.ac.uk/thredds/dodsC/esg_cmip6/CMIP6/ScenarioMIP/IPSL/IPSL-CM6A-LR/ssp245/r1i1p1f1/Omon/tos/gn/v20190119/tos_Omon_IPSL-CM6A-LR_ssp245_r1i1p1f1_gn_201501-210012.nc.html).

Bu dosya, görev kapsamındaki kayıt yeridir. Diğer ajanların harita, duyarlılık,
istatistik, günlük, karar veya Obsidian dosyaları bu yan çalışmayla değiştirilmedi.
Commit/push yapılmadı.
