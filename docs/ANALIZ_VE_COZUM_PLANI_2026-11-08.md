# Adélie MaxEnt 2204-C — Teknik analiz ve çözüm planı

Tarih: 2026-11-08 (Europe/Istanbul). İncelenen commit: `152ba64`.
Kapsam: 2050 haritasının sorunları ve proje genelinin veri, yöntem, doğrulama, yazılım, kayıt ve raporlama denetimi.
Durum: **Analiz ve planlama tamamlandı; aşağıdaki düzeltmeler henüz uygulanmadı.**
Kullanıcı talebi: sorunları incele, çözüm planlarını kaydet; uygulama sonraki çalışma olacak.

## 1. Sonuç ve uygulanacak sıra

Projenin veri hazırlama ve ilk MaxEnt çalıştırması kullanılabilir bir başlangıç oluşturuyor. Ancak mevcut 2050 çıktısı, doğrulanmış bir CMIP6 SSP2-4.5 projeksiyonu olarak sunulamaz. Gelecek girdileri sabit değişimler uygulanarak hazırlanmış; harita düzeni bozuk; değişim yüzdelerine yüklenen biyolojik anlam hesaplanan ölçüyü aşıyor. Önceki kayıtlardaki “tamamlandı / baskıya hazır” ifadeleri bu denetimin bulgularıyla birlikte okunmalı.

Önerilen sıra:

1. Eski çıktıları ve bu denetimin başlangıç durumunu koru; geçici sonuçların niteliğini kayıtlarda düzelt.
2. Öğrenci/danışmanla modelin hedefini, çalışma alanını ve gelecek veri yaklaşımını netleştir.
3. Günümüz modelini ve mekânsal doğrulamasını sağlamlaştır.
4. Kaynakları izlenebilir gerçek gelecek iklim katmanlarını hazırla.
5. Belirsizlik ve uygunluk değişimi hesaplarını yeniden üret.
6. Sonuçlara bağlı, okunabilir haritaları üret ve görsel olarak kontrol et.
7. Yöntem, sınırlılıklar ve bulgular sabitlenince öğrenci raporunu tamamlasın.

Harita düzeninin teknik onarımı 3–4 ile paralel yapılabilir; nihai harita etiketleri ve sayıları 5 tamamlanmadan kesinleştirilmemeli.

Öncelikler: **P0** bilimsel sonucu veya sunumun doğruluğunu engeller; **P1** teslimden önce giderilmeli; **P2** kalite ve sürdürülebilirlik geliştirmesi.

## 2. İnceleme yöntemi ve sınırları

- `CLAUDE.md`, `docs/`, ERA5 ve GBIF yöntem kayıtları, MaxEnt güncel/gelecek girdileri ve çıktıları, MaxEnt logları, QGIS üretim betikleri okundu.
- `harita_2050_A4.png`, `harita_degisim_A4.png` ve üçlü karşılaştırma PNG'si görsel olarak incelendi. PDF sayfalarının ayrıca görsel denetimi yapılmadı; PNG bulguları PDF için tamamlanmış kontrol sayılmaz.
- ASCII rasterlar salt okunur olarak karşılaştırıldı; hücre sayıları, fark sınıfları, eğitim çevre aralığının dışına çıkan hücreler ve AUC kat değerleri yeniden hesaplandı.
- QGIS `.qgz` içindeki XML salt okunur açılarak katman kaynakları ve düzen öğeleri incelendi.
- `cd era5 && python test_biovars.py`: **19 değişken testi geçti**.
- Tam indirme/üretim zinciri yeniden çalıştırılmadı. Bu cihazda ham ERA5/GBIF/kaya klasörleri ve eski `era5/.venv` bulunmuyor; `pandas`, `rasterio`, `matplotlib` mevcut Python'da yok. Bu, başka cihazlardaki kopyaların yok olduğu anlamına gelmez.
- `python -I era5/test_biovars.py` ilk denemede yerel modül yolu nedeniyle çalışmadı; normal proje çalışma dizinindeki yukarıdaki komut başarılı oldu. Sayısal test arızası saptanmadı.
- Ortak kurallar uyarınca Gemini worker aracı denendi; `typer` eksik olduğu için başlatılamadı. Kullanılabilir alt ajanla bağımsız salt okunur kontrol tamamlandı; ek bulguları ana incelemede yeniden kontrol edildi. Nihai bulgular dosya ve hesaplara dayanır.
- Veri kaynakları ve yöntem önerileri için birincil belgeler incelendi (Bölüm 8). Yeni veri indirilmedi, MaxEnt yeniden eğitilmedi, QGIS projesi veya rasterlar değiştirilmedi.

## 3. Plan A — 2050 haritası ve gelecek analizinin sorunları

### A01 — Gelecek veri kaynağı yanlış adlandırılmış [P0, doğrulandı]

Kanıt: `maxent/hazirla_2050_katmanlari.py:3–10,44–66`.

Betik CMIP6 dosyası indirmiyor/okumuyor. Günümüz katmanlarında SST'ye +0,8 °C, deniz buzuna ×0,80, BIO18'e ×1,15 uyguluyor; kayayı sabit tutuyor. İncelenen betik, bu üç değerin belirli bir model, ensemble üyesi, dönem ve bölgeden nasıl çıkarıldığını göstermiyor. Genel IPCC/Cimino atfı bu sayısal türetmenin kanıtı değil.

**Çözüm:** mevcut denemeyi silmeden “varsayımsal çevresel değişim / duyarlılık denemesi” olarak ayır. Nihai gelecek katmanları için veri seti, sürüm, GCM, ensemble üyesi, SSP, referans ve gelecek dönemleri, değişken, birim, takvim, indirme sorgusu ve sağlama toplamı kaydı oluştur. “2050” için örneğin **2041–2060** dönem ortalaması öner; kesin dönem öğrenci/danışmanla kararlaştırılsın.

**Kabul:** her gelecek rasterının kaynak veri dosyası ve dönüşümü izlenebiliyor; kaynak/model bilgisi olmadan CMIP6/SSP etiketi üretilemiyor. Eski duyarlılık denemesi yeni projeksiyonla karışmıyor.

### A02 — Büyük piksellerin nedeni gerçek bilgi çözünürlüğü [P1, doğrulandı]

Kanıt: gelecek SST girdisi ve MaxEnt ortalama çıktısının ASCII başlıkları: `ncols=37`, `nrows=19`, `cellsize=0.25`; toplam 703 hücre. Bu enlemde yaklaşık 10 × 28 km ölçeği söz konusu. `_3031.tif` dosyasının 1 km hücre aralığı veya PNG'nin 300 DPI olması, kaynak bilgi çözünürlüğünü artırmaz.

**Çözüm iki ayrı düzeyde ele alınmalı:**

- Sunum: uygun ölçek, kıyı çizgisi, temiz yerleşim, okunaklı lejant ve eşlenik renk ölçekleri. İstenirse sürekli uygunluk rasterının yalnızca görüntüleme kopyasında bilinear gösterim kullanılabilir; “görsel enterpolasyon, kaynak 0,25°” notu zorunlu olmalı. Sınıflanmış kayıp/kazanç maskesine yumuşatma uygulanmamalı; hiçbir istatistik yumuşatılmış görüntüden hesaplanmamalı.
- Gerçek ayrıntı: Antarktika kapsamı, dönem uyumu ve değişken tanımları doğrulanmış daha ayrıntılı günümüz/gelecek veri ürünlerini araştır. Ortak analiz ölçeğini ekolojik amaçla seç. İnce çözünürlüklü tek bir katman eklemek diğer kaba katmanların bilgi sınırını kaldırmaz. Veri stratejisi değişirse GBIF seyreltmesi, korelasyon ve model baştan değerlendirilir.

**Kabul:** dosya hücre aralığı ile kaynak veri ölçeği ayrı yazılıyor; “1 km çözünürlüklü iklim modeli” iddiası kullanılmıyor. Kaynak ölçek korunursa koloni ölçeğinde ayrıntı vaat edilmiyor.

### A03 — Baskı düzeni ve katman yönetimi bozuk [P1, doğrulandı]

Kanıt: incelenen iki A4 PNG'de lejant haritanın geniş bir bölümünü kapatıyor; koordinatlar çakışıyor/kenarlarda kesiliyor. QGIS XML'de lejant yaklaşık 118 × 90 mm ve harita çerçevesinin içinde. Gelecek uygunluk haritasının lejantında değişim katmanı da var.

Kod nedenleri: `harita/uret_2050_ve_degisim_haritalari.py:109,115–118,128–146,154` tüm vektörleri denetimsiz listeye ekliyor, lejantı proje ağacından güncelliyor, değişim çıktısında bütün `QgsLayoutItemLabel` öğelerinin metnini değiştiriyor ve ana projeyi kaydediyor. Bu davranış gelecekteki çalıştırmaların başlangıç durumunu da değiştiriyor. Rasterın vektörlerin önüne konması kıyı/nokta görünürlüğü için ayrıca kontrol edilmeli.

Ek doğrulanmış hata: `harita/profesyonel_harita_uret.py:149` istasyon etiketi için `name` alanını kullanıyor; mevcut GeoPackage `istasyonlar` tablosunun metin alanı **`ad`**. Etiket alanı ve gerçek şema eşleştirilmeli.

**Çözüm:** ana projeyi şablon olarak koru; çıktı başına ayrı düzen/kopya oluştur. Başlık, kaynak, bilgi kutusu ve lejanta sabit öğe kimliği ver; yalnızca hedef öğeyi değiştir. Haritaya bağlı açık katman listesi ve elle sınırlandırılmış lejant kullan. Kıyı/noktalar raster üzerinde çizilsin. Enlem/boylam etiketlerini sadeleştir; çalışma alanı ve çerçeveyi eşleştir. Export dönüş kodunu kontrol et; başarısız exportta başarı mesajı verme. İkinci çalıştırma katman/ızgara çoğaltmamalı.

**Kabul:** günümüz, gelecek ve fark haritasında yalnızca ilgili lejant var; taşan/çakışan yazı yok; kıyı ve kayıtlar okunuyor; kaynak proje değişmiyor. PNG ve PDF %100 görünümde ve A4 baskı ölçeğinde ayrı ayrı inceleniyor.

### A04 — “Habitat kaybı” yüzdesi hesaplanan ölçü değil [P0, doğrulandı]

Kanıt: `maxent/fark_analizi.py:24–45,55–57` sadece `gelecek − günümüz` farkını ±0,05 eşiğiyle sınıflandırıyor. Günümüzde uygun habitatı belirleyen eşik, uygun → uygunsuz geçişi, başlangıç habitat alanı paydası ve hücre alanı hesabı yok.

Yeniden hesaplanan değerler:

| Ölçü | Hücre | Tüm 703 hücre içindeki oran |
|---|---:|---:|
| Uygunluk farkı < −0,05 | 384 | %54,6 |
| −0,05 ≤ fark ≤ +0,05 | 186 | %26,5 |
| Uygunluk farkı > +0,05 | 133 | %18,9 |
| Fark < −0,25 | 146 | %20,8 |
| Fark > +0,25 | 50 | %7,1 |

Dolayısıyla 384 hücrenin tamamına “şiddetli kayıp” demek de yanlış. Enlem/boylam hücreleri eşit alanlı değil: yalnızca yöntemi göstermek için tüm dikdörtgende küresel alan ağırlığıyla hesaplanan azalma/kararlı/artış payları yaklaşık **%56,0 / %25,3 / %18,7**. Bunlar düzeltilmiş nihai habitat alanı sonuçları değildir; ekolojik maske ve kaynak senaryo hâlâ doğrulanmamıştır.

**Çözüm:** sürekli uygunluk değişimini ayrı raporla. Gerçek alan kaybı istenirse eğitim verisiyle gerekçelendirilen sabit uygunluk eşiğini günümüz/geleceğe aynı uygula; uygun→uygunsuz, uygunsuz→uygun, kalıcı uygun ve kalıcı uygunsuz sınıflarını hesapla. Jeodezik veya uygun eşit alan yöntemi kullan; EPSG:3031 metrik olsa da eşit alanlı değildir. Toplam model alanı, günümüz uygun alanı ve net/brüt değişim paydalarını ayrı ver. Eşik duyarlılığını değerlendir; eşiği beklenen kaybı büyütmek için seçme.

**Kabul:** sonuç tablosunda ölçü, birim, payda, maske, eşik ve kaynak koşu açık; hücre payı km² alan kaybı gibi sunulmuyor.

### A05 — Ekstrapolasyon ve clamping sonuçları sunulmamış [P0, doğrulandı]

Kanıt: gelecek girdilerinin günümüz 703 hücrelik değişken min–maks aralıklarıyla karşılaştırılması:

| Değişken | Günümüz min–maks | Gelecek min–maks | Aralık dışında hücre |
|---|---|---|---:|
| SST, °C | −2,421918 … −0,556068 | −1,621918 … +0,243932 | 373 |
| Yıllık deniz buzu, % | 24,561850 … 65,024101 | 19,649480 … 52,019281 | 104 |
| BIO18, mm | 82,207203 … 631,720249 | 94,538283 … 726,478286 | 10 |
| Kaya, % | 0 … 15,280759 | aynı | 0 |

Sayılar değişkenler arasında toplanamaz; aynı hücre birden fazla aralık dışında olabilir. Mevcut `_novel.asc` çıktılarında **386/703 (%54,9)** hücre negatif; ilk üç katın clamping çıktısında 386 hücrede pozitif etki var. Bu aralık denetimi çok değişkenli bütün yeni kombinasyonları kapsamaz. Her katın eğitim aralığı ayrıca değerlendirilmelidir.

**Çözüm:** MESS/novelty, sınırlayıcı değişken ve clamping etkisini çıktı paketine dahil et. Maskeli/maskesiz özetleri ayır; ekstrapolasyon alanlarını tarama ile işaretle. Gelecek koşu için clamping tercihini açık kaydet ve duyarlılığını incele.

**Kabul:** bir “kesin sığınak” iddiası ekstrapolasyonlu tek ortalama haritadan çıkarılmıyor; belirsizlik katmanları harita ve raporla birlikte teslim ediliyor.

Ek bulgu: aynı katların günümüz ve gelecek rasterları eşlenerek fark alındığında **260/703 (%37,0)** hücrede katlar arasında hem pozitif hem negatif değişim var. Ortalama farkın tek bir sınıfa boyanması bu yön belirsizliğini gizliyor. Eşlenik farkların dağılımı ve değişim işareti uzlaşması hesaplanmalı. Bu kat varyasyonu, iklim modeli/senaryo belirsizliğinin yerine geçmez.

### A06 — Lejant biyolojik kanıttan fazla anlam yüklüyor [P0, doğrulandı]

Kanıt: harita betiklerinde yüksek puan “aktif koloni / yuvalama”, artış “refugia”, düşük puan “açık deniz” olarak adlandırılmış. GBIF girdisi doğrulanmış koloni kayıtlarından ibaret değil. Yüksek model puanı fiilî koloni veya belirli beslenme davranışı gözlemi değil; yalnızca puan artışı kalıcı ve erişilebilir sığınak kanıtı değil.

**Çözüm:** “düşük–yüksek modellenen uygunluk” ve “uygunlukta azalma/artış” gibi doğrudan ölçülen etiketler kullan. Olası sığınak yorumu ancak yeterli mutlak uygunluk, habitat/erişilebilirlik, çoklu model uyumu ve zaman tutarlılığı değerlendirmeleriyle, sınırlılıklarıyla yapılabilir.

**Kabul:** harita puanı ile gözlenen koloni/nüfus değişimi birbirinden ayrılıyor; nedensellik ve nüfus kaybı iddiası üretilmiyor.

### Plan A iş paketleri

| ID | Yapılacak | Bağımlılık | Beklenen çıktı / bitiş ölçütü |
|---|---|---|---|
| A-P1 | Eski koşuyu manifestle koru, iddiaları etiketle | Yok | Eski dosyalar kaybolmadan deneme/nihai ayrımı |
| A-P2 | Dönem, ölçek ve veri seçimini kararlaştır | Genel plan B-P1 | Kaynak/model/dönem seçim notu |
| A-P3 | Gerçek gelecek girdilerini üret | A-P2, B-P2 | Manifestli, ortak ızgaralı, birimleri doğrulanmış rasterlar |
| A-P4 | Şablon ve harita düzenini onar | A-P1; A-P3 ile paralel olabilir | Üç temiz düzen, deterministik katman/öğe yönetimi |
| A-P5 | Doğrulanmış modeli gelecek koşullarına uygula | B-P4, A-P3 | Aynı modelin eşlenik günümüz/gelecek çıktıları |
| A-P6 | Değişim, alan ve belirsizliği hesapla | A-P5 | Eşik/maske/payda açıklamalı tablolar, novelty ve belirsizlik |
| A-P7 | Haritaları ve kaynak notlarını sonlandır | A-P4, A-P6 | PNG/PDF görsel kontrolü ve kaynak raster bütünlük kontrolü |

## 4. Plan B — Proje genelindeki eksikler ve çözüm yaklaşımı

### Korunacak güçlü taraflar

- GBIF indirme DOI'si, sorgu dosyası ve adımlı temizlik kayıtları mevcut.
- Girdi 67 nokta içeriyor; GBIF'teki hazırlanmış MaxEnt CSV kopyasıyla birebir aynı. Dört çevresel girdi `era5/output/` kaynaklarıyla byte düzeyinde aynı.
- BIO hesapları için 19 değişkenlik sentetik test bu incelemede geçti. Günlük/saatlik eşdeğerliği için önceki kayıt mevcut; bu denetimde ham veriyle yeniden doğrulanmadı.
- 10 katlı MaxEnt sonuçları, response curves, jackknife, ortalama ve standart sapma rasterları saklanmış.
- `deneme3` ve `deneme_2050` içindeki günümüz ortalama rasterları sayısal olarak birebir aynı. Gelecek projeksiyonunun günümüz temelini değiştirdiğine ilişkin bulgu yok.
- Kaynaklar, birimler, doldurma varsayımı ve çözünürlük sınırlılıkları ERA5 README'sinde büyük ölçüde yazılmış.

### B01 — Modelin ekolojik hedefi net değil [P0, doğrulandı]

Koloni/üreme habitatı, denizde beslenme alanı ve genel bulunuş aynı hedef değil. CSV hem kara hem deniz hücresi kayıtları içeriyor; kaba kara-deniz maskesi küçük adaları yanlış sınıflandırabildiğinden deniz hücresindeki bütün kayıtlar elenemez. Kaya olmayan hücre de tek başına deniz davranışının kanıtı değil.

**Plan:** temsilci kayıtları kimlikleriyle geri eşleştir; tarih, mevsim, kaynak veri seti, koordinat belirsizliği, kayıt türü ve varsa koloni/üreme bilgisini gözden geçir. Temizlik betiği seçilen temsilcileri ayrı, bütün metadata'sıyla saklasın. “Genel çevresel uygunluk” veya “üreme kolonisi uygunluğu” hedefini öğrenci/danışman seçsin; veri filtreleri ve arka plan bu karara göre gerekçelendirilsin. Tuzluluk gibi ek değişkenler veri erişimi olduğu için otomatik eklenmesin.

**Kabul:** soru, hedef popülasyon/mevsim, kullanılan gözlemler ve harita yorumları birbiriyle uyumlu.

### B02 — Örnekleme yanlılığı ve kalite duyarlılığı eksik [P1, doğrulandı/risk]

Temiz 704 kaydın **423'ünde (%60,1)** koordinat belirsizliği boş. Bu oran seyreltme öncesi temiz kayıtlara ait; 67 temsilci için aynı oran varsayılamaz. Yedi veri seti arasında örnekleme yoğunluğu farklı; iki kaynak 579 kaydı taşıyor. Seyreltme hücre tekrarını azaltır ama gemi rotası, istasyon çevresi ve mevsim yanlılığını tek başına çözmez. 10 km konum eşiği bir filtre; kayıtların hepsinin doğru hücrede olduğunu garanti etmez.

**Plan:** 67 temsilcinin kalite ve kaynak tablosunu üret; belirsizliği bilinen/bilinmeyen, kayıt türü ve mevsim alt kümeleriyle duyarlılık karşılaştırması tasarla. GBIF `basisOfRecord` ve materyal atfı kayıtlarını kaynaklarına göre incele; otomatik doğru/yanlış kabul etme. Kaynak yanlılığı için gerekçeli target-group background veya bias yaklaşımının uygulanabilirliğini değerlendir; bağımsız veri yoksa belirsizliği açık raporla.

### B03 — Arka plan alanı ekolojik olarak gerekçelendirilmemiş [P1, doğrulandı]

MaxEnt logunda 703 geçerli background hücresi var; denizel değerler 364 kara hücresine doldurulmuş. Teknik olarak veri eksik olmaması ekolojik anlamlılık sağlamaz. İç kesimlerdeki doldurulmuş deniz koşulları sonuçları ve değerlendirmeyi etkileyebilir; etkinin büyüklüğü henüz test edilmedi.

**Plan:** erişilebilir alanı (M), koloni veya genel bulunuş hedefine göre tanımla. Model kalibrasyon alanı ve yalnızca gösterim amacıyla kullanılan maske ayrılmalı. Kıyı bandı/kaya oranı gibi seçenekleri gerekçelendirip maske duyarlılığını incele. ERA5 kara maskesiyle küçük ada kayıtlarını otomatik silme. Doldurma mesafesi ve kaynak deniz hücresi kaydı üret; fiziksel anlamı olmayan alanı analiz paydasına bilinçsizce katma.

### B04 — AUC tek başına yeterli değerlendirme değil [P1, doğrulandı]

Kat AUC'leri: `0.5183, 0.9164, 0.8341, 0.7729, 0.8471, 0.6750, 0.7780, 0.7013, 0.8876, 0.7459`.

Ortalama **0,76766**; katlar arası popülasyon SD **0,11091**, örneklem SD **0,11691**. `maxentResults.csv` içindeki ortalama `AUC Standard Deviation=0.0798` farklı bir rapor alanıdır; katlar arası SD ile eşit varsayılmamalı. Mevcut 0,768 ± 0,111 ifadesi katlar arası popülasyon SD olarak tanımlanabilir; güven aralığı değildir. Bir kat 0,5183 düzeyinde; kat başına yalnızca 6–7 test kaydı var.

Loglar varsayılan katlı çalıştırmayı gösteriyor; mekânsal blok değerlendirme kaydı bulunmadı. Mekânsal bağımlılık performansı iyimser gösterebilir; mevcut AUC'nin ne kadar etkilendiği test edilmeden söylenemez.

Kaydedilmiş `*_samplePredictions.csv` eğitim/test atamalarıyla ayrıca doğrulandı: 67 test kaydının **61'inde**, sekiz komşuluğa göre hemen bitişik bir hücrede eğitim kaydı var. En yakın eğitim kaydına büyük çember uzaklığının medyanı yaklaşık **12,64 km** (6371 km yarıçaplı küre). Bu, bir hücrede tek nokta bırakmanın tek başına mekânsal bağımsızlık sağlamadığını gösterir; performans yanlılığının büyüklüğünü hesaplamaz.

**Plan:** mevcut koşuyu referans olarak koru; yeterli doluluğa sahip mekânsal blok/grup doğrulaması tasarla. Blok sayısı/boyutunu 67 kaydın dağılımına göre seç; otomatik 10 blok dayatma. Eğitim/test ayrımı ve rastgele tohumları kaydet. AUC yanında önceden belirlenen omission ölçüleri ve uygun bir presence-only değerlendirme ölçütü (ör. yeterli bağımsız veriyle Boyce) düşün. Gerçek yokluk verisi olmadan TSS/özgüllüğü doğrulanmış absence gibi sunma. Hedef >0,70 danışman ölçütüdür; sağlanması dış doğrulamayı ikame etmez.

### B05 — Model karmaşıklığı ve değişken duyarlılığı gösterilmemiş [P1, kayıt bulunmadı]

Logda varsayılan regularization/feature ayarlarıyla çalıştırma görülüyor; sistematik aday model seçimi kaydı bulunmadı. Seçili değişkenler arası korelasyon için önceki gerekçe var; yıllık denizel ortalamalar üreme mevsimi mekanizmasını doğrudan temsil etmeyebilir. Yüksek korelasyon değişkenlerin her bağlamda aynı biyolojik bilgiyi taşıdığını kanıtlamaz.

**Plan:** sınırlı ve önceden belirlenmiş feature/regularization adayları oluştur; aynı mekânsal doğrulama altında karşılaştır. Az sayıdaki noktaya uygun karmaşıklığı seç; yalnızca en yüksek eğitim AUC'sini optimize etme. Yıllık/yaz denizel değişkenleri ile kaya/BIO18 etkilerini bilimsel soruya bağlı, sınırlı duyarlılık denemeleri olarak değerlendir. Permütasyon önemi ve percent contribution birbirinden ayrı adlandırılsın; %55,6 permütasyon önemi, açıklanan varyans veya nedensel katkı yüzdesi değil.

### B06 — Kaynak ve yöntem doğrulaması kısmi [P1, doğrulandı]

Rothera'da sayısal aralık kontrolü fiziksel tutarlılık kontrolüdür; bağımsız istasyon doğrulaması sayılmaz. Toplam yağıştan BIO18 üretimi sıvı yağışı veya kar erimesini doğrudan ölçmez. Kaya haritası tek dönemli ve statik; gelecekte sabit tutulması bir varsayım. ERA5 dönemi 2000–2025, kayıtlar 2000–2026; eşleştirme yaklaşımı açıklanmalı.

**Plan:** her değişkenin fiziksel anlamını ve temsil ettiği dönemi raporla. Uygun bağımsız istasyon/uydu kaynağı varsa ölçek uyumunu gözeterek karşılaştır; yoksa doğrulama düzeyini açıkça sınırla. Yağış/kar/nest etkisi arasında kanıtsız eşitlik kurma. Kaya statikliği ve kıyı/maskelerin zaman uyumsuzluğunu sınırlılıklara ekle.

### B07 — Çalışma ortamı ve yeniden üretilebilirlik eksik [P1, doğrulandı]

ERA5 için sürüm listesi mevcut, fakat bu cihazda kullanılan eski sanal ortam ve ham girdiler yok. Gelecek ve harita betiklerinde `/home/halil/...` yolları sabit; QGIS/GDAL/Java bağımlılıkları tek manifestte belgelenmemiş. Harita betiği ana projeyi yazıyor. Değişim okuyucusu başlık/ızgara eşitliği ve `NaN/Inf` kontrollerini yapmıyor; mevcut dosyalarda başlık uyumsuzluğu saptanmadı.

**Plan:** parametre dosyası ve göreli proje yolları; Python + sistem GIS/Java sürüm manifesti; ham veri konum/sorgu/checksum kayıtları; temiz ortamda küçük uçtan uca örnek; ayrı koşu kimliği ve girdi/çıktı hashleri. ASCII boyut/CRS/NoData/sonlu değer ve gelecek-günümüz başlık eşitliği kontrolleri ekle. MaxEnt cache kaynak dosyaya göre doğrulansın. Yeni bağımlılıklar asgari tutulsun; ortam kurulumu uygulama aşamasında yapılacak.

### B08 — Durum belgeleri ve teslim paketi geriden geliyor [P1, doğrulandı]

`CLAUDE.md` gelecek senaryosunu kapsam dışı/açık soru olarak tutarken aşama tablosu CMIP6 işini tamamlandı sayıyor. `docs/ASAMALAR.md` rapor taslağı hazır diyor; bu depoda `rapor/` klasörü yok. Bu yalnızca yerel depoda taslak bulunamadığı anlamına gelir; öğrencinin başka yerde taslağı olup olmadığı bilinmiyor. GBIF belirsizliği boş kayıt sayısı eski günlükte 420, güncel temizlik çıktısında 423.

**Plan:** önceki kayıtları silmeden tarihli düzeltme notu ekle; doğrulanmış durum ile geçmiş iddiayı ayır. Danışman onaylarını ve toplantı kararlarını K-009/K-018/K-020 ile eşleştir. Öğrencinin mevcut raporunu varsa bulup sürümle; yoksa rapor iskeleti ve kanıt tablosu hazırla. Güncel TÜBİTAK 2204-C çağrısındaki format, etik/AI kullanım beyanı ve teslim koşulları uygulama/rapor aşamasında resmi kaynaktan ayrıca doğrulansın; bu denetim çağrı uygunluk denetimi değildir.

### Plan B iş paketleri ve karar noktaları

| ID | İş / sorumlu | Bağımlılık | Tamamlanma ölçütü |
|---|---|---|---|
| B-P1 | Araştırma sorusu, hedef habitat, dönem, alan / öğrenci + danışman | Yok | Bir sayfalık kapsam ve karar kaydı |
| B-P2 | Veri/kayıt kalite envanteri, kaynak ve ortam / teknik çalışma; bilimsel filtreler öğrenci + danışman | B-P1 | 67 temsilci metadata tablosu; manifest; çalışır ortam |
| B-P3 | M alanı, maske, yanlılık ve doğrulama tasarımı / öğrenci + danışman; teknik uygulama | B-P1–2 | Tekrarlanabilir kat/maske dosyaları ve gerekçesi |
| B-P4 | Günümüz model adayları ve değerlendirme / teknik çalışma | B-P3 | Aynı değerlendirmede aday sonuçları, seçimin gerekçesi, belirsizlik |
| B-P5 | Literatür/yorum ve kayıtların tutarlılığı / öğrenci + teknik destek | B-P1–4; A-P6 sonuçlarını bekler | Her ana iddianın veri/koşu/kaynak karşılığı |
| B-P6 | Rapor ve teslim paketi / öğrenci; istenirse teknik biçim desteği | B-P5, A-P7 | Yöntem, bulgu, sınırlılık ve haritaların birbirini doğruladığı paket |

Karar noktaları uygulama öncesinde tek oturumda ele alınabilir:

- Model genel bulunuşu mu yoksa üreme kolonisi habitatını mı hedefliyor?
- Nihai ürün mevcut 0,25° ölçeğinde bölgesel model mi, yeni veri gerektiren ayrıntılı kıyı modeli mi?
- 2050 hedef dönemi ve temel SSP ne olacak; ikinci SSP ve çoklu GCM için kapsam ne kadar genişleyecek?
- Kayıt filtreleri, ERA5 yaklaşımı ve değişkenler için danışman onayının mevcut durumu ne?

Henüz alınmamış bilimsel kararlar bu belgeyle alınmış sayılmaz. Öğrenci/danışmanın önceki kararları korunur; öneriler uygulama sırasında gerekçeleriyle netleştirilir.

## 5. Gerçek gelecek veri zinciri için önerilen teknik tasarım

Bu bölüm bir uygulama önerisidir; indirme yapılmış veya model seçilmiş değildir.

1. CDS/ESGF üzerinden aynı model/üye/SSP için SST (`tos`), deniz buzu (`siconc`), yağış (`pr`) ve BIO18'in sıcak çeyreğini belirlemek için sıcaklık (`tas` ya da tutarlı Tmax/Tmin) bulunabilirliğini doğrula. Değişkenlerin farklı atmosfer/okyanus ızgaraları ve takvimleri olabilir; isim listesi erişim garantisi değildir.
2. Referans ile gelecek dönemlerini eşleştir. 2000–2025 tabanı korunursa CMIP6 tarihsel serinin 2014'te bittiğini ve 2015–2025 için aynı model/üye/SSP devamının gerektiğini açık kaydet. Alternatif ortak referans dönemine geçilecekse günümüz katmanları ve gerekçe birlikte ele alınsın.
3. Doğrudan ham gelecek GCM'yi ERA5'le karıştırmak yerine, aynı GCM'nin referans/gelecek farklarından kaynaklı bir delta/bias yaklaşımı tasarla. SST için toplamsal; yağışta sıfıra yakın değerleri gözeten oran veya uygun alternatif; deniz buzunda 0–100 sınırlarını gözeten yöntem değerlendir. Yöntem seçimi ve sınır etkileri test edilsin. Basit delta yaklaşımı da dinamik küçültme veya yeni 1 km iklim bilgisi değildir.
4. Yağışın kg m⁻² s⁻¹ birimini takvim/ay uzunluğuyla mm/ay'a, sıcaklığı °C'ye, deniz buzunu dosya metadata'sına göre %'ye dönüştür. Her değişkende aynı yıllık/yaz tanımı ve ağırlıklandırma kullanılsın. BIO18 gerekiyorsa geleceğin aylık sıcaklık/yağışından yeniden hesaplanır; doğrudan %15 çarpılmaz.
5. Okyanus kıyı maskelerini ve remapping yöntemlerini ayrı doğrula; bir ızgaranın kara boşluklarını bilinear interpolasyonla denize yayma. Kaya statik tutulursa varsayımı yaz. Doldurma ve geçerli analiz maskelerini kaydet.
6. Kaynağı/kalitesi doğrulanmış küçük bir GCM kümesini, veri erişimi elverirse birden fazla SSP'yi değerlendir. En az bir izlenebilir GCM tek-model sınırlılığıyla kullanılabilir; ensemble yokken ensemble iddiası olmaz. Birden fazla GCM varsa her modelde projeksiyon al, sonra uygunluk/alan sonuçlarını özetle; yalnızca ortalama iklimde tek projeksiyonla aynı kabul etme.
7. GCM belirsizliği ile MaxEnt katlar arası belirsizliği ayrı ver. Clamping/novelty maskesi ve değişim işareti uzlaşmasını hesapla; yalnızca ortalama renkli haritayı teslim etme.

## 6. Uygulama kontrol listesi

- [ ] Önceki çıktılar manifestle korundu, geçici senaryo etiketi düzeltildi.
- [ ] Hedef habitat / ölçek / dönem / danışman kararları kaydedildi.
- [ ] Girdi metadata, kalite ve kaynak tabloları tamamlandı.
- [ ] Kalibrasyon alanı ve mekânsal doğrulama tasarımı gerekçelendirildi.
- [ ] Günümüz aday modeli seçimi ve bağımsızlık sınırlılıkları raporlandı.
- [ ] Gerçek gelecek veri zinciri ve dönüşümler doğrulandı.
- [ ] Aynı modelle eşlenik günümüz–gelecek sonuçları alındı.
- [ ] Uygunluk farkı, eşikli alan değişimi ve belirsizlik ayrı hesaplandı.
- [ ] Lejant/başlık/veri tutarlı PNG ve PDF ayrı ayrı görsel kontrol edildi.
- [ ] Raporun yöntem, iddia, tablo, harita ve kaynakları eşleştirildi.
- [ ] Tekrarlanabilir paket ve güncel kayıtlar hazırlandı.

## 7. Denetim anındaki Git ve teslim durumu

Başlangıç: `main`, yerel `origin/main` izleme referansının bir commit önünde; son commit `152ba64`. Denetim başında çalışma ağacı temizdi. Bu çalışma yalnızca analiz belgeleri ve kayıt güncellemeleri oluşturur; yeni commit/push talebi yoktur. Uzak deponun canlı durumu bu incelemede fetch edilmedi.

Resmî proje kopyası: `docs/ANALIZ_VE_COZUM_PLANI_2026-11-08.md`.
Kullanıcıya sunulan kopya: Codex çalışma klasörünün `outputs/` dizinindeki aynı adlı belge.
Merkezi bilgi bankasında tarihli denetim özeti mevcut; geçmiş 2050 sonuçlarının geçerliliği bu belgeyle sınırlandırılmıştır.

## 8. Kaynaklar ve neyi destekledikleri

Erişim: 2026-11-08. Dosya incelemelerinin kanıtı yukarıdaki repo yollarıdır. Aşağıdaki kaynaklar mevcut projeye ait ölçümlerin değil, yöntem önerilerinin dayanağıdır.

1. [MaxEnt resmi yazılım sayfası](https://biodiversityinformatics.amnh.org/open_source/maxent/): model çıktısının yorumu ve cloglog için veri/örnekleme varsayımları.
2. [Phillips — MaxEnt Tutorial](https://biodiversityinformatics.amnh.org/open_source/maxent/Maxent_tutorial_2021.pdf): varsayılan rastgele katlama ve değerlendirme akışı.
3. [Copernicus CMIP6 kataloğu](https://cds.climate.copernicus.eu/datasets/projections-cmip6?tab=overview): model bazında çözünürlük, historical 1850–2014 ve SSP 2015–2100 kapsamı; sıcaklık/yağış/okyanus/buz değişkenleri ve birimleri. Belirli modelde bütün değişkenlerin erişilebilir olduğu ayrıca doğrulanacak.
4. [Copernicus — Climate projections](https://climate.copernicus.eu/climate-projections): sayısal iklim modelleri ve model/senaryo/doğal değişkenlik kaynaklı belirsizlik.
5. [Roberts vd. 2017](https://doi.org/10.1111/ecog.02881): yapılı veride çapraz doğrulama ve blok tasarımının probleme göre seçilmesi.
6. [Muscarella vd. 2014 — ENMeval](https://doi.org/10.1111/2041-210X.12261): MaxEnt karmaşıklık seçimi ve mekânsal değerlendirme. Araç kullanımı zorunlu değil; klasik Java MaxEnt iş akışı korunabilir.
7. [QGIS — raster properties / resampling](https://docs.qgis.org/3.44/en/docs/user_manual/working_with_raster/raster_properties.html#resampling): görüntüleme enterpolasyonunun pikselli görünümü yumuşatması. Bu, yeni bağımsız iklim gözlemi üretmez.
8. [Cimino vd. 2016, özgün makale PDF](https://www.nature.com/articles/srep28785.pdf), DOI 10.1038/srep28785: üreme kolonileri, yaz koşulları ve gelecek habitatı bağlamı. Bu yayının bulunması mevcut projedeki +0,8/−%20/+%15 sayılarının yerel CMIP6 türetmesini doğrulamaz.
