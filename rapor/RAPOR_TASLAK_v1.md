# Marguerite Körfezi'nde Adélie Pengueninin (*Pygoscelis adeliae*) Çevresel Uygunluğunun MaxEnt ile Modellenmesi ve CMIP6 SSP2-4.5 Altında 2041–2060 İçin Keşifsel Değerlendirme

**TÜBİTAK 2204-C Lise Öğrencileri Kutup Araştırma Projeleri — Rapor Taslağı v1 (öğrenci incelemesine açık)**
**Kısa proje adı:** Marguerite Körfezi Adélie MaxEnt
**Araştırmacı:** Halil Erdem Yanık · **Danışman:** Metin Silsüpür

## Özet

Bu çalışma, Batı Antarktika Yarımadası'ndaki Marguerite Körfezi'nde Adélie pengueninin (*Pygoscelis adeliae*) genel bulunuşunun çevresel uygunluğunu klasik MaxEnt 3.4.4 ile modellemeyi ve modeli keşifsel bir CMIP6 senaryosuna aktarmayı amaçlamıştır. GBIF'ten alınan 1001 kayıt temizlenmiş ve ERA5 hücresi başına bir kayıt bırakılarak 67 bulunuş noktası elde edilmiştir. Modelde ERA5 (2000–2025) tabanlı yıllık deniz buzu, yıllık deniz yüzeyi sıcaklığı ve en sıcak çeyrek yağışı (BIO18) ile SCAR kaya örtüsü kullanılmıştır. Rastgele 10 katlı doğrulamada test AUC'si 0,768 ± 0,111 bulunmuş; en yüksek permütasyon önemi deniz buzuna (%55,6) ait olmuştur. Dört enlem bandıyla yapılan mekânsal doğrulamada ortalama AUC 0,477–0,580 aralığında kalmış, eşleştirilmiş rastgele doğrulamada 0,715–0,765 bulunmuştur; bu nedenle model coğrafi aktarım açısından zayıf kabul edilmiştir. IPSL-CM6A-LR SSP2-4.5 (2041–2060) aylık delta yöntemiyle kayıtlı modele aktarıldığında 703 model hücresinin %42,2'sinde uygunluk puanı azalmış, %23,2'si kararlı kalmış, %34,6'sında artmıştır; bu oranlar habitat alanı kaybı değildir. Çalışma, Wang vd. (2026) ile aynı yönde MaxEnt, deniz yüzeyi sıcaklığı ve deniz buzu temelli bir yaklaşım izlemektedir. Gelecek sonuçları tek iklim modeline dayanan keşifsel bulgulardır.

**Anahtar kelimeler:** Adélie pengueni, MaxEnt, Marguerite Körfezi, deniz buzu, CMIP6

## 1. Amaç

1. Marguerite Körfezi'nde Adélie pengueni bulunuş kayıtlarının, deniz buzu, deniz yüzeyi sıcaklığı, en sıcak çeyrek yağışı ve kaya örtüsüyle ilişkisini MaxEnt ile ortaya koymak.
2. Modelin başarımını yalnızca rastgele değil, mekânsal olarak ayrılmış doğrulamayla da değerlendirmek (Roberts vd., 2017).
3. Kayıtlı modeli, IPSL-CM6A-LR SSP2-4.5 (2041–2060) iklim girdileriyle keşifsel olarak çalıştırıp uygunluk puanındaki değişimi ve belirsizliğini göstermek.

Bu çalışmada modellenen şey **genel bulunuş için çevresel uygunluktur**; üreme kolonisi, nüfus büyüklüğü veya beslenme davranışı doğrudan modellenmemiştir.

## 2. Giriş

*Pygoscelis* cinsi penguenler Antarktika ekosisteminde enerji akışının sürdürülmesinde önemli rol oynar ve ekosistem sağlığı için gösterge türlerdir (Wang vd., 2026). Wang vd. (2026), OBIS bulunuş kayıtlarını ve 2010–2020 ile 2090–2100 (SSP5-8.5) deniz çevresi verilerini MaxEnt ile kullanarak Adélie, Antarktika (chinstrap) ve Papua (gentoo) penguenleri için potansiyel uygun habitatı simüle etmiştir. Aynı çalışmada deniz yüzeyi sıcaklığı ve deniz buzu örtüsünün dağılımı etkileyen temel çevresel değişkenler olduğu, Adélie pengueni için uygun habitatın 60°G–75°G arasında Antarktika kıyılarında ve komşu sularda dağınık biçimde bulunduğu ve gelecek senaryosunda üç türün de uygun habitat alanının daraldığı bildirilmiştir (Wang vd., 2026).

Adélie pengueni için MaxEnt ve GAM ile yavru büyütme dönemi habitat uygunluğunu modelleyen Cimino vd. (2016), deniz yüzeyi sıcaklığı, deniz buzu yoğunluğu ve buzsuz kayayı değişken olarak kullanmış, tüm modellerde AUC değerini 0,85'in üzerinde bulmuştur (Cimino vd., 2016). Yavru büyütme döneminde yavru yüzeyinin yalnızca %10'unun kar veya eriyik suyla ıslanmasının uçma ağırlığını hayatta kalma şansını düşürecek kadar azalttığı bir model çalışmasıyla gösterilmiştir (Chapman vd., 2011); bu nedenle üreme mevsimi yağışını temsil eden BIO18 değişkeni modele alınmıştır.

MaxEnt, yalnızca varlık verisiyle çalışan bir tür dağılım modelleme yöntemidir (Phillips vd., 2006). Tür dağılım modellerinde rastgele kat ayırma, birbirine yakın kayıtların hem eğitimde hem testte bulunmasına yol açabildiği için mekânsal olarak ayrılmış doğrulama önerilmiştir (Roberts vd., 2017).

Bu çalışma, Wang vd. (2026)'nin Antarktika ölçeğindeki yaklaşımına benzer biçimde MaxEnt, deniz yüzeyi sıcaklığı ve deniz buzunu kullanmakta; farklı olarak çalışma alanını Marguerite Körfezi ile sınırlamakta, buzsuz kaya örtüsünü (Cimino vd., 2016) ve üreme mevsimi yağışını (Chapman vd., 2011) eklemekte ve mekânsal doğrulamayı raporlamaktadır.

## 3. Yöntem

### 3.1 Çalışma alanı ve ızgara
Alan, 73,125°B–63,875°B ve 70,625°G–65,875°G sınırlarındaki dikdörtgendir. Tüm katmanlar ERA5'in 0,25° ızgarasında (37 × 19) ve EPSG:4326'dadır; ortak geçerli alan 703 hücredir. Bu dikdörtgen karşılaştırılabilir bir başlangıç alanı olarak korunmuştur; ekolojik olarak erişilebilir alan (M) olarak gerekçelendirilmemiştir.

### 3.2 Bulunuş kayıtları
Kayıtlar GBIF'ten resmî indirme API'siyle alınmıştır (taxonKey 2481663; 2000–2026; koordinatlı; coğrafi sorunu olmayan; occurrenceStatus = PRESENT; DOI 10.15468/dl.jt3gt7). 1001 kayıt sırasıyla şu kurallarla temizlenmiştir: alan dışı kayıtların atılması; koordinat belirsizliği 10 km'den büyük kayıtların atılması; yalnızca bölge adı içeren konumların atılması; aynı koordinat ve tarih tekrarlarının teke indirilmesi; ERA5 hücresi başına en küçük belirsizlikli tek kaydın seçilmesi. Sonuç 704 temiz kayıt ve 67 hücre temsilcisidir. Kara ve deniz kayıtları birlikte tutulmuştur.

### 3.3 Çevresel katmanlar
- **BIO18** (en sıcak çeyreğin yağışı), **yıllık deniz yüzeyi sıcaklığı** ve **yıllık deniz buzu**: ERA5 (Hersbach vd., 2020) 2000–2025; BIO18 WorldClim/dismo tanımıyla, 12 sarmal üç aylık pencere üzerinden hesaplanmıştır. Deniz değişkenlerinin NaN olduğu 364 kara hücresine en yakın deniz hücresinin değeri atanmıştır.
- **Kaya:** SCAR Antarctic Digital Database v7.11 kaya çıkıntısı poligonlarından (Skachkova vd., 2025) hücre başına kaya yüzdesi; 703 hücrenin 343'ünde kaya vardır (en yüksek %15,3).
- **Değişken seçimi:** Değişkenler ekolojik gerekçeyle seçilmiştir (Cimino vd., 2016; Chapman vd., 2011). Seçilen dört katman arasındaki en yüksek |r| 0,65'tir (BIO18–deniz buzu); bu değer Dormann vd. (2013)'ün kullandığı 0,7 eşiğinin altındadır. BIO18 gibi sıcaklık ve yağışı birleştiren değişkenlerde çeyrek değişimi nedeniyle yapay kesintiler oluşabileceği (Booth, 2022) bilindiğinden gelecek BIO18 tekrar hesaplanmıştır (3.6).

### 3.4 MaxEnt modeli
MaxEnt 3.4.4 (Java 21), 67 bulunuş noktası ve 703 arka plan hücresiyle 10 katlı çapraz doğrulamada (kat başına ortalama 60,3 eğitim / 6,7 test noktası), jackknife ve tepki eğrileri açık, varsayılan özelliklerle çalıştırılmıştır (`maxent/cikti/deneme3`).

### 3.5 Doğrulama
- **Rastgele 10 kat:** MaxEnt raporundaki test AUC (presence–background).
- **Mekânsal 4 bant:** Kayıtlar enlem sırasıyla dört gruba bölünmüştür (test kayıtları 17, 17, 16, 17). Kesimler, model skorlarına bakılmadan grup büyüklüklerini eşitlemek için seçilmiştir. Her kayıt bir kez testte yer alır; eğitim ve test noktaları aynı hücreyi paylaşmaz. Arka plan her katta aynı 703 hücredir; bu nedenle test, bilinen alan içinde bulunuş kayıtlarının coğrafi aktarımıdır.
- **Eşleştirilmiş rastgele 4 kat:** Aynı kat boyutları (17, 17, 16, 17) ve aynı ayarlarla, tek sabit tohumla (20261108) rastgele atama.
- **Omission:** Yalnızca eğitim puanlarının %10'luk kuantiliyle belirlenen eşik altı test kayıtlarının oranı.
- Aday ayarlar: L/RM1, LQ/RM1, LQ/RM2 ve otomatik özellikli AUTO/RM1. Aday seçimi aynı katlar üzerinde yapılırsa ayar yanlılığı oluşacağı için nihai aday seçilmemiştir.

### 3.6 Gelecek girdileri (keşifsel)
IPSL-CM6A-LR, r1i1p1f1, SSP2-4.5; referans 2000–2025 (historical 2000–2014 + SSP2-4.5 2015–2025), gelecek 2041–2060. `tas` için aylık fark, `pr` için aylık oran ERA5 aylık değerlerine uygulanmış; BIO18 gelecek aylık değerlerden yeniden hesaplanmış (29/703 hücrede en sıcak çeyrek değişmiştir). Yıllık deniz yüzeyi sıcaklığı için aylık anomalilerin ortalaması, deniz buzu için yüzde puan farkı eklenmiş (0–100'e kırpılmış); kaya sabit tutulmuştur. GCM hücreleri ERA5 hücrelerine en yakın tam verili hücre eşlemesiyle aktarılmış; atmosfer için 20, deniz için 62 farklı kaynak hücre kullanılmıştır. Bu işlem yeni iklim ayrıntısı eklemez. Kayıtlı on kat modelinin `.lambdas` dosyaları yeniden eğitilmeden yeni girdilere uygulanmış (cloglog, clamping açık); kontrol çalıştırmasında kayıtlı iki çıktıyla fark 0,0'dır.

### 3.7 Değişimin ölçülmesi
Uygunluk farkı = gelecek puan − günümüz puanı. Sınıflar: azalma (< −0,05), kararlı (−0,05…+0,05), artış (> +0,05); eşik mutlak puandır. Hücre payı ve model dikdörtgeninin WGS84 elipsoidi üzerindeki alan payı ayrı hesaplanmıştır. Aralık uyarısı, bir değişkenin kayıtlı `.lambdas` dosyasındaki min–maks aralığı dışında olmasıdır (MESS değildir).

## 4. Bulgular

### 4.1 Veri
67 temsilci kaydın 62'si aralık–şubat (DJF), 2'si mart–mayıs, 3'ü eylül–kasım dönemindedir; haziran–ağustos kaydı yoktur. 61 kayıt insan gözlemi, 5 kayıt materyal atfı, 1 kayıt makine gözlemidir. 36 kaydın (%53,7) koordinat belirsizliği boştur. 19 kayıt ERA5 kara hücresinde, 48 kayıt deniz hücresindedir.

### 4.2 Model başarımı ve değişken önemi
Rastgele 10 katlı doğrulamada ortalama test AUC 0,768 (kat SD 0,111; en düşük 0,518, en yüksek 0,916); eğitim AUC 0,838'dir. AUC > 0,70 hedefi bu tasarımda sağlanmıştır.

| Değişken | Katkı (%) | Permütasyon önemi (%) |
|---|---:|---:|
| Yıllık deniz buzu | 43,1 ± 5,5 | 55,6 ± 5,3 |
| Kaya | 30,0 ± 3,5 | 9,1 ± 4,2 |
| BIO18 | 13,9 ± 5,6 | 17,1 ± 5,2 |
| Yıllık deniz yüzeyi sıcaklığı | 12,9 ± 2,6 | 18,3 ± 4,5 |

*Tablo 1. On katın ortalaması ± popülasyon standart sapması (`maxentResults.csv`). Birbiriyle ilişkili değişkenlerde katkı yüzdeleri modele bağlıdır; iki ölçüt farklı sırayı verdiği için tek bir sıralama iddia edilmemiştir.*

### 4.3 Mekânsal doğrulama

| Aday | Mekânsal 4 bant AUC | Rastgele 4 kat AUC | Mekânsal omission | Rastgele omission |
|---|---:|---:|---:|---:|
| L/RM1 | 0,580 | 0,715 | 19/67 (%28,4) | 6/67 (%9,0) |
| LQ/RM1 | 0,530 | 0,746 | 24/67 (%35,8) | 9/67 (%13,4) |
| LQ/RM2 | 0,557 | 0,720 | 23/67 (%34,3) | 8/67 (%11,9) |
| AUTO/RM1 | 0,477 | 0,765 | 38/67 (%56,7) | 13/67 (%19,4) |

*Tablo 2. Aynı kat boyutları ve ayarlarla eşleştirilmiş karşılaştırma (`docs/MEKANSAL_DOGRULAMA_2026-11-08.md`). Tek tohum, dört kat ve ortak arka plan nedeniyle fark için güven aralığı verilmemiştir.*

Hiçbir adayın mekânsal ortalama AUC değeri 0,70'e ulaşmamıştır. Mekânsal tasarımda test kayıtlarının en yakın eğitim kaydına uzaklığının medyanı 45,4 km (aralık 10,2–241,3 km), rastgele tasarımda 12,6 km'dir (0,8–58,9 km). Güney banttaki (kat 3) omission değerleri %94–100'dür. Bu nedenle model, coğrafi aktarım açısından zayıf kabul edilmiş ve nihai model seçilmemiştir.

### 4.4 Günümüz uygunluk haritası
Günümüz haritasında (Şekil 1) en yüksek uygunluk puanları, GBIF kayıtlarının yoğunlaştığı kuzeybatı ve orta-batı kıyı–ada kuşağında görülür; doğu ve güneydoğuda puanlar düşüktür. Yüksek puan, gözlenmiş koloni veya nüfus büyüklüğü anlamına gelmez.

![Şekil 1. Günümüz çevresel uygunluğu (ERA5 2000–2025, genel bulunuş modeli; gösterim bilineer enterpolasyonludur, analiz 0,25° hücrelerdendir).](/home/halil/adelie-maxent-2204c/harita/cmip6_ipsl_2050_v1/gunumuz_A4.png)

### 4.5 IPSL-CM6A-LR SSP2-4.5 (2041–2060) keşifsel aktarımı
Gelecek girdilerinde BIO18 77,6–756,6 mm, yıllık deniz yüzeyi sıcaklığı −1,89…+0,21 °C ve yıllık deniz buzu %9,3–53,0 aralığındadır. ±0,05 mutlak puan eşiğinde 703 hücrenin 297'sinde (%42,2) azalma, 163'ünde (%23,2) kararlılık, 243'ünde (%34,6) artış bulunmuştur; model dikdörtgeninin WGS84 alan payları sırasıyla %44,0, %22,2 ve %33,8'dir. Sonuç eşiğe duyarlıdır:

| Eşik (mutlak puan) | Azalma | Kararlı | Artış |
|---|---:|---:|---:|
| ±0,025 | %45,2 | %14,5 | %40,3 |
| ±0,05 | %42,2 | %23,2 | %34,6 |
| ±0,10 | %31,3 | %41,3 | %27,5 |
| ±0,25 | %14,5 | %75,5 | %10,0 |

*Tablo 3. Hücre payları (703 hücre; `ozet.json`). Gerekçelendirilmiş bir uygunluk eşiği olmadığı için habitat alanı (km²) kaybı hesaplanmamıştır.*

Değişim haritasında (Şekil 2) güçlü azalma (< −0,25) ağırlıkla kuzeybatıda ve Rothera–Horseshoe çevresinde, yani kayıtların yoğun olduğu kesimde; artış ise kuzeydoğuda ve güneydoğuda görülür. 357/703 hücrede en az bir değişken kayıtlı aralığın dışındadır; en büyük clamping etkisi yaklaşık 0,63 puandır. 246/703 hücrede aynı kat çiftleri değişimin yönü konusunda ayrışmaktadır. Bu kat dağılımı bağımsız iklim modelleri topluluğu değildir.

![Şekil 2. 2041–2060 için uygunluk değişimi (IPSL-CM6A-LR SSP2-4.5 tek model; habitat alanı kaybı değildir).](/home/halil/adelie-maxent-2204c/harita/cmip6_ipsl_2050_v1/degisim_A4.png)

## 5. Sonuç ve Tartışma

Rastgele 10 katlı doğrulamada AUC hedefi (> 0,70) sağlanmıştır (0,768), ancak aynı veriyle dört enlem bandına ayrılmış doğrulamada ortalama AUC 0,477–0,580'e düşmüştür. Rastgele doğrulamanın yakın kayıtları eğitim ve testte birlikte bulundurabildiği bilindiğinden (Roberts vd., 2017) ve bu çalışmada rastgele testte en yakın eğitim kaydı medyan 12,6 km, mekânsal testte 45,4 km olduğundan, başarı yalnızca AUC > 0,70 eşiğine bağlanmamıştır. Bu fark tek başına bir biyolojik nedene bağlanamaz; tasarım, kat sayısı ve arka plan seçimi de etkili olabilir.

Değişken önemi açısından yıllık deniz buzu permütasyon ölçütünde en yüksek değere (%55,6) sahiptir. Wang vd. (2026) deniz yüzeyi sıcaklığı ve deniz buzunu temel değişkenler olarak bildirmiş, Cimino vd. (2016) deniz yüzeyi sıcaklığı, deniz buzu yoğunluğu ve buzsuz kayanın önemini doğrulamıştır. Bu çalışmada deniz buzu, kaya ve BIO18'in de modele katkı vermesi bu sonuçlarla çelişmemektedir; ancak katkı yüzdeleri değişken ilişkilerine bağlı olduğundan nedensel yorum yapılmamıştır.

Gelecek aktarımında uygunluk puanı hem azalmış hem artmıştır ve oranlar eşiğe göre değişmektedir (Tablo 3). Wang vd. (2026) SSP5-8.5 ve 2090–2100 için Antarktika ölçeğinde genel bir daralma bildirmiştir; bu çalışmanın senaryosu (SSP2-4.5, 2041–2060), alanı ve ölçütü (hücre başına uygunluk puanı farkı) farklı olduğu için sonuçlar doğrudan karşılaştırılamaz. Bu çalışmada elde edilen hiçbir sayı habitat alanı kaybı, koloni kaybı veya iklim sığınağı kanıtı olarak sunulmamıştır.

**Sınırlılıklar.** (i) Tek iklim modeli, tek üye ve tek senaryo kullanılmış, iklim modeli ve senaryo belirsizliği sayısallaştırılmamıştır. (ii) GCM bilgisi en yakın kaynak hücre eşlemesiyle aktarılmış, yeni ince ölçekli iklim bilgisi üretilmemiştir. (iii) Kaya katmanı gelecekte sabit varsayılmıştır. (iv) 67 kayıt kara ve deniz hücrelerini birlikte içerir, koloni doğrulaması yoktur; 36 kaydın koordinat belirsizliği bilinmemektedir. (v) Ekolojik erişilebilir alan (M), bağımsız gözlem çabası verisi ve bağımsız doğrulama verisi yoktur. (vi) Aynı katlarda aday karşılaştırması ayar yanlılığı taşır. (vii) Aralık uyarısı tek değişkenlidir (MESS hesaplanmamıştır). (viii) Wang vd. (2026) yalnızca özet düzeyinde incelenmiştir; tam metin yöntemi bu taslağa yansıtılmamıştır.

## 6. Öneriler

1. Doğrulanmış koloni veya üreme kayıtlarıyla model hedefini netleştirmek ve ekolojik erişilebilir alanı (M) gerekçelendirmek.
2. Bağımsız gözlem çabası verisi veya bağımsız doğrulama verisi bulunduğunda target-group arka plan ve dış testle modeli yeniden değerlendirmek.
3. Birden fazla iklim modeli ve senaryoyla (ör. SSP2-4.5 ve SSP5-8.5) gelecek belirsizliğini sayısallaştırmak; böylece Wang vd. (2026) ile senaryo bazında karşılaştırma yapmak.
4. Wang vd. (2026) tam metnindeki yöntem adımlarını okuyup bu çalışmanın yöntemiyle adım adım eşleştirmek.
5. Gerekçelendirilmiş bir uygunluk eşiği ve ekolojik maske tanımlandıktan sonra alan bazlı değişim hesaplamak.

## 7. Gerçekleşen çalışma kaydı (iş–zaman çizelgesi yerine)

| Tarih (2026) | Yapılan |
|---|---|
| 19–20 Ekim | GBIF indirme ve temizlik (1001 → 704 → 67), ERA5 katmanları, ilk MaxEnt denemesi (AUC 0,781), değişken seçimi, kaya katmanı |
| 20 Ekim | 10 katlı çalıştırma `deneme3` (AUC 0,768) |
| 26–31 Ekim | İlk haritalar ve sabit oranlı duyarlılık denemesi (CMIP6 değildir; rapora girmemiştir) |
| 8 Kasım | Mekânsal doğrulama, kalite envanteri, gerçek IPSL-CM6A-LR SSP2-4.5 girdileri, kayıtlı modelin aktarımı, harita paketi |
| 10 Kasım | Danışman yönlendirmesiyle (Wang vd., 2026) yazım başlangıcı |

## Kaynakça

Booth, T. H. (2022). Checking bioclimatic variables that combine temperature and precipitation data before their use in species distribution models. *Austral Ecology*. https://doi.org/10.1111/aec.13234

Chapman, E., Hofmann, E., Patterson, D., Ribic, C., & Fraser, W. (2011). Marine and terrestrial factors affecting Adélie penguin chick growth and recruitment off the western Antarctic Peninsula. *Marine Ecology Progress Series, 436*, 273–289. https://doi.org/10.3354/meps09242

Cimino, M. A., Lynch, H. J., Saba, V. S., & Oliver, M. J. (2016). Projected asymmetric response of Adélie penguins to Antarctic climate change. *Scientific Reports, 6*, 28785. https://doi.org/10.1038/srep28785

Dormann, C. F., Elith, J., Bacher, S., et al. (2013). Collinearity: a review of methods to deal with it and a simulation study evaluating their performance. *Ecography, 36*, 27–46. https://doi.org/10.1111/j.1600-0587.2012.07348.x

GBIF.org. *GBIF Occurrence Download*. https://doi.org/10.15468/dl.jt3gt7

Hersbach, H., et al. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society*. https://doi.org/10.1002/qj.3803

Phillips, S. J., Anderson, R. P., & Schapire, R. E. (2006). Maximum entropy modeling of species geographic distributions. *Ecological Modelling, 190*, 231–259.

Roberts, D. R., et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography, 40*, 913–929. https://doi.org/10.1111/ecog.02881

Skachkova, A., et al. (2025). *High resolution vector polygons of Antarctic rock outcrop* (SCAR Antarctic Digital Database v7.11). https://doi.org/10.5285/815525ca-cefe-4fbf-9224-3ee784e7de4e

Wang, J.-R., Hu, A.-L., & Yang, J. (2026). [Impact of climate change on the potentially suitable habitat distribution of *Pygoscelis* penguins in Antarctica]. *Ying Yong Sheng Tai Xue Bao, 37*(3), 926–932. https://doi.org/10.13287/j.1001-9332.202603.037

## Ekler

**Ek-1.** Dört haritalık A4 paket: `harita/cmip6_ipsl_2050_v1/` (günümüz, 2041–2060, değişim, belirsizlik).
**Ek-2.** Yöntem ve sayı kaynakları: `docs/KAPSAM_VE_YONTEM_2026-11-08.md`, `docs/MEKANSAL_DOGRULAMA_2026-11-08.md`, `docs/CMIP6_DELTA_VE_PROJEKSIYON_2026-11-08.md`, `maxent/cikti/deneme3/NOT.md`.
**Ek-3. Teknik destek beyanı (öğrenci/danışman beyan biçimini teyit edecek):** Bu rapor taslağı ve analiz betikleri yapay zekâ desteğiyle hazırlanmıştır; kararlar, yorumlar ve rapor öğrenci tarafından gözden geçirilmektedir. Çalıştırılan komutlar ve sürümler proje manifestlerinde saklanmıştır.
