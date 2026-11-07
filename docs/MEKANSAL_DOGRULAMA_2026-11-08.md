# Mekânsal doğrulama ve örnekleme kalitesi — 2026-11-08

Bu çalışma kullanıcının açık uygulama talebiyle, mevcut modele ek ve ayrı çıktılar
olarak yürütüldü. Geçici hedef **genel bulunuş**, alan mevcut tam dikdörtgendir.
Ekolojik erişilebilir alan (M), üreme kolonisi hedefi veya nihai model seçimi bu
çalışmayla kesinleştirilmedi. Senaryo, harita ve CMIP işleri kapsam dışındadır.

**Durum:** Eski çıktılar ve aşağıdaki ilk 10-kat/4-bant karşılaştırması geçicidir
(provisional). Tasarımları ayıran yeni eşleştirilmiş karşılaştırma belgenin son
bölümündedir; hiçbir aşamada nihai kazanan seçilmedi veya tam veri modeli kurulmadı.

## Dosyalar ve yeniden çalıştırma

Yeni kaynaklar: `maxent/mekansal_dogrulama.py`,
`maxent/test_mekansal_dogrulama.py`, `gbif/kalite_envanteri.py` ve bu belge.
Kaynak bağımlılığı yalnızca Python stdlib ve NumPy'dır; Java model aracı ayrıca gerekir.

Proje kökünden:

```bash
python3 -B -m unittest discover -s maxent -p test_mekansal_dogrulama.py -v
python3 -B gbif/kalite_envanteri.py
python3 -B maxent/mekansal_dogrulama.py --run-java
```

Varsayılan çıktı klasörleri zaten oluşturulmuştur; betikler üzerine yazmayı reddeder.
Tekrar için izinli ağaçlarda yeni bir alt klasör belirtin:

```bash
python3 -B gbif/kalite_envanteri.py --output gbif/temiz/kalite_20261108/tekrar_02
python3 -B maxent/mekansal_dogrulama.py --run-java --output maxent/cikti/mekansal_20261108/tekrar_02
```

İlk uygulama aşamasının kaynak sürümüyle tamamlanan referans koşu:
`maxent/cikti/mekansal_20261108/verified_run/`.
İlk koşu ana çıktı dizininde, ilk tekrar `repro_check/` içinde korunmuştur.
Her koşu 3 aday × 4 kat = 12 eğitim içerir; iki tekrar dahil toplam 36 Java
eğitimi yapıldı. Tekrarlar ek aday, yeni bağımsız veri veya nested CV değildir.

Java: `/usr/lib/jvm/java-21-openjdk/bin/java`, OpenJDK 21.0.12.1;
MaxEnt: mevcut `maxent/maxent.jar`, sürüm 3.4.4. NumPy: 2.5.4.
Tam Python/sistem/Java sürümleri `versions.json` içinde saklıdır.
Java 27 kullanılmadı; Java 21 ile ortam kurulumu gerekmeksizin çalıştı.

## Önceden sabitlenen tasarım

Girdiler mevcut 67 koordinat ve `bio18`, `buz_yillik`, `kaya`, `sst_yillik`
katmanlarıdır. Dört ASCII başlığı, boyutları ve sonlu değerler kontrol edildi;
ortak geçerli alan 703 hücredir. Özgün girdiler, önbellek ve `deneme3` çıktıları
değiştirilmedi. Java yalnızca yeni çıktı klasörüne kopyalanan katmanlarla çalıştı.

Her iki yön için benzersiz raster satır/sütunları üzerinde dört ardışık grup
oluşturuldu. Amaç, grup sayılarının 67/4'ten sapmalarının kareleri toplamını
en aza indirmektir. Dinamik programlama bütün kesim seçeneklerini kapsar;
aynı satır/sütun bölünmez. Yönler arası eşitlikte enlem, kesim eşitliğinde ilk
sıralı kesim tercih edilir. Kararda model skorları veya çevresel değerler kullanılmaz.

| Yön | Kat başına test kaydı | Dengesizlik kareleri toplamı |
|---|---|---:|
| Enlem (seçildi) | 17, 17, 16, 17 | 0,75 |
| Boylam | 16, 20, 14, 17 | 18,75 |

Katlar kuzeyden güneye 0–3'tür. Kesimler raster satır indisinde 2,5 / 5,5 / 7,5;
coğrafi sınırlar −66,625°, −67,375°, −67,875° enlemdir. Sınır noktaları
MaxEnt'in güneyden taban alma kuralıyla kuzey hücresine atanır. Her test kaydı
tam bir kez kullanılır; eğitim/test nokta ve hücre kesişimi sıfırdır.
Eğitim sayıları 50 / 50 / 51 / 50'dir. Buffer uygulanmadı; bantlar bağımsızlık garantisi değildir.

Arka plan her katta aynı tam alanın 703 hücresidir, hücre başına eşit ağırlıklıdır;
alan ağırlıklı değildir. Tutulan bandın çevresel arka planı da eğitim alanında
kalır: bu, **bilinen alan içinde varlık kayıtlarının coğrafi aktarımı** denemesidir,
tümüyle görülmemiş bir bölgenin çevresine aktarım testi değildir.
`addsamplestobackground=false`; eğitim örnekleri arka plana ayrıca eklenmez.
Java'ya yalnızca `train.csv` verilir; test dosyası haricen değerlendirilir.
Tüm hücreler kullanıldığından arka plan alt örneklemesi yoktur;
`randomseed=false`, `threads=1`, rastgele kat ataması yoktur.

Önceden sabit üç aday: L/RM1, LQ/RM1, LQ/RM2.
`autofeature=false`; product, threshold ve hinge kapalıdır.
L doğrusal, LQ doğrusal+karesel özelliklerdir. Diğer eğitim seçenekleri
mevcut jar varsayılanlarıdır; tam komutlar ve jar hash'i saklanmıştır.

## Mekânsal yakınlık ve mevcut tasarımla karşılaştırma

Eski 10 katın gerçek atamaları `deneme3/*_samplePredictions.csv` dosyalarından
geri okundu; her noktanın tam bir kez test olduğu doğrulandı. Yeni ve eski
atamalar, nokta başına mesafe ve komşuluk dosyaları saklandı.
Mesafe küresel haversine, yarıçap 6371 km; komşuluk rasterda sekiz yönlüdür.

| Ölçü | Eski 10 kat | Yeni 4 enlem bandı |
|---|---:|---:|
| Bitişik eğitim hücresi olan test kaydı | 61/67 | 24/67 |
| Eğitimle aynı hücrede test kaydı | 0 | 0 |
| En yakın eğitim uzaklığı medyanı, km | 12,6422 | 45,3912 |
| En yakın eğitim uzaklığı min–maks, km | 0,8216–45,2041 | 10,1732–241,2503 |

## Gerçek MaxEnt sonuçları

Değerlendirme cloglog çıktı rasterlarından aynı hücre okuma kuralıyla yapılır.
Presence-background AUC, her test puanının 703 arka plan puanıyla karşılaştırılmasıdır;
eşit puan yarım kazanım sayılır. Bu arka plan gözlenmiş yokluk değildir.
Eşik, yalnız eğitim puanlarının NumPy `quantile(0.10, method="linear")` değeridir;
puan eşikten **küçükse** omission sayılır. Bu açık tanım, MaxEnt'in CSV'de
raporladığı kendi sıra/eşik enterpolasyonuyla birebir aynı sayı olmak zorunda değildir.
Eşik seçimi test kayıtlarını kullanmaz. Raster yuvarlaması bütün adaylarda aynıdır.

| Aday | Kat 0 AUC | Kat 1 AUC | Kat 2 AUC | Kat 3 AUC | Ortalama AUC | Kat SD (popülasyon) | Omission, 67 kayıtta |
|---|---:|---:|---:|---:|---:|---:|---:|
| L/RM1 | 0,78567 | 0,76793 | 0,39669 | 0,36821 | 0,57962 | 0,19753 | 19/67 = %28,36 |
| LQ/RM1 | 0,62911 | 0,81010 | 0,33339 | 0,34679 | 0,52985 | 0,20031 | 24/67 = %35,82 |
| LQ/RM2 | 0,78341 | 0,74969 | 0,33028 | 0,36503 | 0,55710 | 0,21014 | 23/67 = %34,33 |

AUC ortalaması katlara eşit ağırlıklıdır; SD güven aralığı değildir.
Omission sütunu bütün test kayıtları üzerinden toplanır; eşit kat ağırlıklı
omission ortalamaları sırasıyla %28,22 / %35,66 / %34,38'dir.
Kat 3 omission değerleri %94,12 / %100 / %100; güney bandına aktarım bu
tasarım altında zayıftır. Bu durumun biyolojik nedeni bu denemeyle belirlenmez.

Eski rasterları aynı değerlendirme koduyla yeniden okumak AUC **0,76766**,
kat SD **0,11091**, toplam omission **14/67 = %20,90** verir. Eski Java
raporundaki yuvarlatılmış AUC ortalamasıyla uyumludur.
Eski ve yeni koşularda kat sayısı, eğitim büyüklüğü, özellikler ve arka plana
örnek ekleme ayarı farklıdır: farkın tamamı mekânsal bağımlılığa yüklenemez.
Bu karşılaştırma eşlenik tek-değişkenli bir deney değildir.

Bu üç adayda L/RM1'in ortalama skoru en yüksek olsa da bağımsız doğrulanmış
optimum ilan edilmedi ve bütün veride yeni nihai model eğitilmedi. Aynı katlar
üzerinde karşılaştırma ve olası seçim **tuning bias** taşır; dış test veya nested
CV yoktur. Az sayıdaki kat, ortak arka plan ve artık komşuluk belirsizlik yaratır.
>0,70 hedefinin sağlanması bağımsız doğrulama yerine geçmez; burada ortalama
olarak hiçbir aday o hedefe ulaşmadı. Boyce/TSS/gerçek absence iddiası üretilmedi.

## 67 temsilcinin kalite envanteri

`gbif/temiz/kalite_20261108/temsilciler_metadata.csv`, mevcut temiz dosyanın
**bütün 12 sütununu** ve türetilmiş satır/sütunu korur. Kaybolmuş ham GBIF
sütunları, koloni doğrulaması veya üreme bilgisi yeniden oluşturulmuş sayılmaz.
Seçim en küçük belirsizlik (boşlar sona), sonra sayısal en küçük `gbifID` kuralını
tekrarlar. 67 koordinat ve sıralama orijinal MaxEnt CSV ile aynı; yeniden üretilen
CSV'nin newline normalize edilmiş metni de aynıdır.

Temiz 704 kayıtta belirsizliği boş **423 (%60,09)**;
gerçek 67 temsilcide **36 (%53,73)**, bilinen **31**.
Temsilcilerde DJF **62**, MAM **2**, SON **3**, JJA **0**;
19 kayıt ERA5 kara hücresinde, 48 kayıt deniz hücresindedir. Bu maske küçük
adaların gerçek habitatını veya gözlem davranışını doğrulamaz.

| Temsilci datasetKey | Kayıt | Belirsizliği boş |
|---|---:|---:|
| 4fa7b334-ce0d-4e88-aaae-2e0c138d049e | 29 | 29 |
| 50c9509d-22c7-4a22-a47d-8c48425ef4a7 | 25 | 2 |
| 6ddba1a7-e34d-41ae-a14b-017e3c565c87 | 1 | 0 |
| 6ff8b3b0-ef0f-4f79-a310-5a5615c6aa0b | 1 | 1 |
| 8a863029-f435-446a-821e-275f4f641165 | 1 | 0 |
| 8ff9e5d1-cc0e-4f3a-90c2-274039353f84 | 5 | 4 |
| f7c30fac-cf80-471f-8343-4ec5d8594661 | 5 | 0 |

| Temsilci basisOfRecord | Kayıt | Belirsizliği boş |
|---|---:|---:|
| HUMAN_OBSERVATION | 61 | 32 |
| MACHINE_OBSERVATION | 1 | 0 |
| MATERIAL_CITATION | 5 | 4 |

`quality_groups.csv` hem 704 temiz kayıt hem 67 temsilci için dataset, kayıt türü,
mevsim ve dataset×tür kırılımını; `summary.json` yıl ve maske sayımlarını da içerir.
Kayıt türleri otomatik doğru/yanlış diye filtrelenmedi. Kalite bilinen/bilinmeyen
ve mevsim alt kümeleriyle yeni model eğitimleri bu sınırlı iş paketinde yapılmadı.
Bağımsız target-group gözlem çabası verisi bulunmadığından bias rasterı veya
target-group background uydurulmadı. Bunlar bilimsel gerekçelendirme gerektirir.

## Doğrulama, manifestler ve sınırlar

Yedi test geçti: bantların sürekliliği ve tie koruması, küçük örnekte tüm kesimleri
deneyerek denge optimumu, gerçek 67 noktada eğitim/test nokta-hücre ayrılığı ve
tek test kapsaması, AUC eşitlikleri/omission/NaN reddi, küresel mesafe ve komşuluk,
hücre sınırı/67 koordinat eşliği, belirsizlik ve sayısal kimlik seçimi.

Tekrarlarda 12 tahmin rasterı byte düzeyinde, `metrics.csv`, `assignments.csv`,
`distance_diagnostics.csv` ve `summary.json` aynı çıktı verdi. Java eğitim
puanlarıyla rasterdan okunan eğitim puanları ayrıca karşılaştırıldı; maksimum
mutlak fark 5,13 × 10⁻⁷ ile ASCII yuvarlama düzeyinde uyuştu. Her Java sonuç dosyasında eğitim sayısı ve 703 arka
plan kaydı kontrol edildi; Java örnek tahminlerinin tamamı `train` etiketlidir.

`verified_run/manifest.json` kullanılan eski girdilerin ve baseline dosyalarının
SHA-256 değerlerini, çıktı SHA-256 değerlerini ve değişmezlik kontrolünü içerir.
`commands.json` argüman dizileri, `commands.sh` çalıştırılan komutlar;
`versions.json` ortam; her katın `console.log`, `maxent.log`, `.lambdas`, `.asc`
ve sonuç CSV'leri saklanmıştır. Java cache'i yalnız çıktı içindedir.
Manifest kendisini hash'lemez; sonradan eklenen tekrar klasörleri eski manifestin
çıktı listesine dahil değildir.

İlk iki koşunun tarihsel manifesti, o sırada mevcut olan başka bir çalışmanın
`maxent/girdi/cmip6_2041_2060/` dosyalarını da geniş girdi taramasına almıştı.
Bu dosyaların diğer çalışma tarafından sonradan güncellenmesi ilk manifestlerde
güncel hash farklılığı yaratır; bu iş paketinin kullandığı dört katman/samples/eski
modelde değişiklik değildir. Son sürüm girdi koruma listesini yalnız bu işin
gerçek girdileriyle sınırlar. İlk aşamanın doğrulaması için `verified_run`
manifesti kullanılır; aşağıdaki uzantının kaynak sürümü farklıdır. Eski kaynak
hash'leri ait oldukları sürümün tarihsel kaydıdır, güncel betikle aynı olmaları
beklenmez. İlk aşamanın manifestleri değiştirilmedi.

Ortak günlükler/karar belgeleri ve Obsidian, kullanıcının yalnız belirtilen
dosyalara yazma talebi nedeniyle bu iş paketinde güncellenmedi. Mevcut eşzamanlı
değişikliklere dokunulmadı. Commit/push yapılmadı. Ortam engeli kalmadı.

## Uzantı: eşleştirilmiş random4 ve mekânsal dört kat

Kullanıcının sonuç incelemesi sonrası talebiyle değerlendirme tasarımı için
eşleştirilmiş kontrol eklendi. **Yalnız 20 yeni Java eğitimi** yapıldı:
random4 üzerinde L/RM1, LQ/RM1, LQ/RM2 ve AUTO/RM1 (16 eğitim);
aynı mekânsal bantlarda yalnız AUTO/RM1 (4 eğitim).
İlk üç adayın `verified_run/` mekânsal eğitimleri yeniden kullanılmaktadır;
ilgisiz tekrar yapılmadı. Kalite envanteri ve ortak belgeler değiştirilmedi.

Rastgele atama tek `numpy.random.Generator(numpy.random.PCG64(20261108))`
permütasyonudur. Permütasyon sırasıyla **17,17,16,17** parçaya ayrılır;
kat indisleri mekânsal tasarımdaki sayılarla aynı sırayı korur. Her aday aynı
random4 atamasını kullanır. Tek tohum bir kez kullanıldı, alternatif tohumlar
performansa bakılarak denenmedi. Test ve eğitim noktaları/hücreleri ayrı;
her kayıt bir kez testtir. Eğitim sayıları iki tasarımda da **50,50,51,50**.

AUTO/RM1, `autofeature=true betamultiplier=1` ile jar'ın varsayılan özellik
ailelerini ve örnek sayısına bağlı etkinleştirme kurallarını kullanır. Manuel
adayların kapalı feature bayrakları AUTO'ya aktarılmaz. Bu, önceki özgün
modelin otomatik özellik ailesiyle bağlantı kurar; özgün 10 kat koşusunun tüm
ayarlarının aynısı olduğu anlamına gelmez. Özellikle bu uzantıda her iki
tasarımda `addsamplestobackground=false`, aynı 703 hücrelik tam alan, aynı
cloglog/omission hesabı ve diğer eğitim ayarları korunur.

Tam komutlar (proje kökünden; klasörler artık vardır):

```bash
python3 -B maxent/mekansal_dogrulama.py --run-java --partition spatial --candidates AUTO_RM1 --output maxent/cikti/mekansal_20261108/matched_spatial_default
python3 -B maxent/mekansal_dogrulama.py --run-java --partition random4 --seed 20261108 --candidates L_RM1 LQ_RM1 LQ_RM2 AUTO_RM1 --output maxent/cikti/mekansal_20261108/matched_random4 --compare-spatial maxent/cikti/mekansal_20261108/verified_run maxent/cikti/mekansal_20261108/matched_spatial_default
```

| Aday | Mekânsal AUC ort. | Random4 AUC ort. | Random − mekânsal | Mekânsal omission | Random4 omission |
|---|---:|---:|---:|---:|---:|
| L/RM1 | 0,57962 | 0,71545 | +0,13583 | 19/67 (%28,36) | 6/67 (%8,96) |
| LQ/RM1 | 0,52985 | 0,74562 | +0,21577 | 24/67 (%35,82) | 9/67 (%13,43) |
| LQ/RM2 | 0,55710 | 0,72046 | +0,16336 | 23/67 (%34,33) | 8/67 (%11,94) |
| AUTO/RM1 | 0,47742 | 0,76543 | +0,28801 | 38/67 (%56,72) | 13/67 (%19,40) |

AUC ortalamaları katlara eşit ağırlıklı; omission tüm 67 test kaydında
birleştirilmiştir. Kat SD'leri, kat başına AUC/omission ve eğitim eşikleri
makine okunur karşılaştırma dosyalarında bulunur. AUTO/RM1'in mekânsal kat
AUC'leri 0,26713 / 0,67580 / 0,60491 / 0,36185'tir.

Random4'te bitişik eğitim hücresi bulunan test sayısı **58/67**, medyan en yakın
eğitim uzaklığı **12,6422 km**, aralık **0,8216–58,8817 km**.
Mekânsal tasarımda sırasıyla **24/67**, **45,3912 km**, **10,1732–241,2503 km**.
İki tasarımda aynı hücrede eğitim/test kesişimi sıfırdır.

Bu eşleştirmede sabit ayarlar altında değişen faktör kayıtların katlara atanma
tasarımıdır; eski 10-kat karşılaştırmasındaki eğitim büyüklüğü ve özellik ailesi
karışıklığı kaldırılmıştır. Coğrafi çevresel kapsamın farklılaşması bu tasarım
etkisinin parçasıdır. Fark, evrensel bir "AUC şişmesi" veya biyolojik nedene ait
nedensel etki tahmini değildir. Tek tohum, dört kat, artık mekânsal komşuluk ve
ortak tam alan arka planı sınırlılıkları sürer. Kat 0 gibi aynı numaralı iki kat
aynı kayıtları taşımaz; farklar üzerinden eşlenik test veya güven aralığı verilmedi.
Nested CV/bağımsız dış test yoktur; adayları bu sonuçlara göre seçmek tuning bias
taşır. Nihai kazanan seçilmedi ve tüm 67 kayıtla yeni model eğitilmedi.

Yeni çıktılar `maxent/cikti/mekansal_20261108/` altında:

- `matched_spatial_default/`: AUTO/RM1 mekânsal eğitimleri, atamalar, bölmeler,
  metrikler, mesafeler, komutlar, sürümler ve hash manifesti.
- `matched_random4/`: dört adayın random4 eğitimleri ve aynı kayıt türleri.
- `matched_random4/matched_fold_metrics.csv`: dört aday × iki tasarım × dört kat,
  toplam 32 metrik satırı.
- `matched_random4/matched_comparison.csv`: yukarıdaki özetin hassas değerleri
  ve katlar arası popülasyon SD'leri.
- `matched_random4/matched_sources.json`: yeniden kullanılan mekânsal dosyaların
  hash'leri, geçici çıktı ve nihai seçim yapılmadığı etiketleri.

Karşılaştırma kodu kaynakların model/katman/samples hash'lerini, kullanılan
mekânsal çıktı dosyalarının hash'lerini, örnek kimlik/sırasını ve kat büyüklüklerini
denetler. Her aday/kat için Java komutlarını girdi/çıktı yolları hariç eşleştirir;
mekânsal AUC/omission değerlerini eski rasterlardan yeniden hesaplayıp kayıtlı
metriklerle doğrular. Mevcut çıktıları değiştirmez.

Uzantıyla **9 test** geçti. Yeni testler sabit tohumla aynı atamayı, değişen tohumla
farklı atamayı, tam test kapsamasını/ayrılığı ve eşit eğitim büyüklüklerini;
AUTO'nun manuel feature kısıtlarını devralmamasını denetler. Yeni 20 Java eğitimi
ve iki yeni manifest ayrıca kontrol edildi. Eski çıktı manifestleri bu uzantı için
yeniden yazılmadı; yeni kaynak hash'i yeni koşu manifestlerinde kayıtlıdır.
