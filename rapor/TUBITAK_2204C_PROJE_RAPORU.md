# TÜBİTAK 2204-C KUTUP ARAŞTIRMALARI PROJE RAPORU

Proje Ana Alanı: Kutup Araştırmaları (Biyoloji ve Ekoloji) | Proje Tematik Alanı: Kutup Biyoçeşitliliği ve Ekosistem Dinamikleri

MaxEnt Algoritması ve CMIP6 İklim Senaryoları Kullanılarak Marguerite Körfezi'nde (Batı Antarktika) Adélie Pengueni (*Pygoscelis adeliae*) Potansiyel Habitat Uygunluğunun ve İklim Değişim Eğilimlerinin Modellenmesi

# TÜBİTAK 2204-C KUTUP ARAŞTIRMALARI PROJE RAPORU

**Proje Ana Alanı:** Kutup Araştırmaları (Biyoloji ve Ekoloji)
**Proje Tematik Alanı:** Kutup Biyoçeşitliliği ve Ekosistem Dinamikleri
**Proje Adı:** MaxEnt Algoritması ve CMIP6 İklim Senaryoları Kullanılarak Marguerite Körfezi'nde (Batı Antarktika) Adélie Pengueni (*Pygoscelis adeliae*) Potansiyel Habitat Uygunluğunun ve İklim Değişim Eğilimlerinin Modellenmesi

---


# Özet

Batı Antarktika Yarımadası, 20. yüzyılın ikinci yarısında küresel ortalamanın yaklaşık üç katına ulaşan bölgesel ısınma hızıyla (Vaughan vd., 2003) yeryüzünün iklim değişimine en duyarlı ekosistemlerinden biridir. Bu çalışmada, deniz buzu zorunlu (sea-ice obligate) tepe avcı ve kutup biyo-indikatörü olan Adélie pengueninin (*Pygoscelis adeliae*), Batı Antarktika Yarımadası'ndaki (WAP) Marguerite Körfezi sahasında (65.88°–70.63°G, 63.88°–73.13°B) günümüz habitat uygunluğu modellenmiş; CMIP6 iklim projeksiyonu altında 2050 yılı olası çevresel değişim eğilimleri keşifsel düzeyde incelenmiştir. GBIF ve SCAR biyo-çeşitlilik veri tabanlarından derlenen 2000–2025 dönemine ait üreme kolonisi ve beslenme gözlemleri, 0.25° grid ölçeğinde mekânsal inceltme uygulanarak örnekleme yığılmasından arındırılmış ve 67 adet bağımsız varlık hücresi elde edilmiştir. Çevresel katman olarak ECMWF ERA5 yeniden analizlerinden yıllık ortalama deniz buzu konsantrasyonu (*buz_yillik*), deniz yüzeyi sıcaklığı (*sst_yillik*), en sıcak çeyrek toplam yağışı (*bio18*) ve REMA sayısal yükseklik modelinden çıplak kaya yüzdesi (*kaya*) üretilmiştir.

Maksimum Entropi (MaxEnt 3.4.4) algoritmasıyla yürütülen 10 katlı çapraz doğrulamada **0.768 ± 0.111** test AUC ve 0.838 eğitim AUC değeri elde edilmiştir. Permütasyon öneminde modelin birincil belirleyicisi **%55.6** ile yıllık deniz buzu konsantrasyonu olmuş; bunu deniz yüzeyi sıcaklığı (**%18.3**), yaz mevsimi yağışı (**%17.1**) ve çıplak kaya alanı (**%9.1**) izlemiştir. Çevresel tepki eğrileri, türün en yüksek uygunluğa %20–%25 marjinal buz konsantrasyonunda, -1.9°C su sıcaklığında ve 184 mm yaz yağışında ulaştığını göstermiştir. Buz konsantrasyonu arttıkça uygunluk kademeli düşerek %60'ta 0.154 ile en düşük seviyesine inmekte; aşırı kapalı kütlesel buz örtüsünde dalış ve besin erişiminin kısıtlanmasını yansıtmaktadır.

Roberts vd. (2017) yaklaşımıyla uygulanan 4 enlem bandı mekânsal blok çapraz doğrulaması (Spatial Block CV), test AUC değerlerinin **0.477–0.580** bandına gerilediğini göstererek kutup enlemlerinde mekânsal otokorelasyonun ve coğrafi aktarılabilirlik kısıtlarının raporlanmasının zorunluluğunu ortaya koymuştur. CMIP6 IPSL-CM6A-LR SSP2-4.5 (2041–2060) delta projeksiyonunda, 703 grid hücresinin **297 adedinde (%42.2)** uygunluk azalması, **163 adedinde (%23.2)** kararlılık, **243 adedinde (%34.6)** ise deniz buzu incelmesine bağlı kuramsal uygunluk artışı belirlenmiştir. Ancak hücrelerin %50.8'inde (357 hücre) iklim değişkenlerinin günümüz aralıklarını aşması (clamping), tek model kısıtlılığı ve George VI Boğazı'nın kalıcı şelf buzuyla kaplı olması, artış alanlarının doğrudan kesin bir 'ekolojik sığınak' sayılamayacağını; Ulusal Antarktika Bilim Seferleri (TAE) kapsamında sahada test edilmesi gereken birer **bölgesel hipotez** olduğunu göstermektedir.

**Anahtar Kelimeler:** Adélie Pengueni (*Pygoscelis adeliae*), MaxEnt Ekolojik Niş Modeli, Marguerite Körfezi, CMIP6 SSP2-4.5, Mekânsal Blok Çapraz Doğrulama, İklim Değişimi, Ekstrapolasyon Belirsizliği.


# Amaç

Bu projenin temel amacı; küresel iklim değişikliğine bağlı olarak oşinografik ve atmosferik süreçlerin hızla dönüştüğü Batı Antarktika Yarımadası'ndaki (WAP) Marguerite Körfezi'nde, deniz buzu dinamiklerine duyarlı tepe indikatör tür olan Adélie pengueninin (*Pygoscelis adeliae*) günümüz (2000–2025) potansiyel habitat uygunluğunu Maksimum Entropi (MaxEnt 3.4.4) algoritmasıyla mezo-ölçekte modellemek; CMIP6 IPSL-CM6A-LR SSP2-4.5 (2041–2060) projeksiyonu altında türün çevresel uygunluk gradyanındaki olası değişim eğilimlerini keşifsel düzeyde incelemek; model aktarılabilirliğini mekânsal blok çapraz doğrulama yöntemiyle sınamak ve elde edilen kuramsal değişimlerin sahadaki ekolojik fizibilitesini değerlendirmektir.

Bu genel amaç doğrultusunda şu hedefler belirlenmiştir:

- • 1. GBIF ve SCAR biyo-çeşitlilik veri tabanlarından Marguerite Körfezi'ne ait 2000–2025 dönemini kapsayan Adélie pengueni üreme kolonisi ve denizel gözlem koordinatlarını derlemek; 0.25° grid ölçeğinde mekânsal inceltme uygulayarak 67 adet bağımsız varlık hücresi belirlemek.
- • 2. ECMWF ERA5 yeniden analizlerinden ve REMA sayısal yükseklik modelinden penguenlerin üreme ve beslenme ekolojisini kontrol eden 4 temel çevresel katmanı (*buz_yillik*, *kaya*, *bio18*, *sst_yillik*) üretmek; değişkenler arası çoklu eşdoğrusallığı (VIF ve Pearson korelasyonu) denetlemek.
- • 3. MaxEnt 3.4.4 algoritmasıyla günümüz habitat uygunluk modelini kurmak; standart rastgele 10 katlı çapraz doğrulama (10-fold CV) ve Roberts vd. (2017) yöntemine dayalı 4 enlem bandı mekânsal blok çapraz doğrulama (Spatial Block CV) uygulayarak model başarımını ve coğrafi aktarılabilirlik sınırlarını karşılaştırmak.
- • 4. CMIP6 IPSL-CM6A-LR SSP2-4.5 (2041–2060) iklim projeksiyonunu delta aşağı ölçekleme yöntemiyle ERA5 referansına entegre ederek 2050 yılı potansiyel habitat değişim haritalarını üretmek; novel climate ve clamping alanlarını haritalandırarak ekstrapolasyon belirsizliklerini ortaya koymak.
- • 5. Model sonuçlarını ve mekânsal kısıtları, Türkiye'nin düzenlediği Ulusal Antarktika Bilim Seferleri (TAE) kapsamında yürütülecek izleme ve koruma stratejileri için sahada doğrulanabilir bir araştırma çerçevesine dönüştürmek.

# Giriş

Antarktika kıtası ve onu çevreleyen Güney Okyanusu, küresel termohalin sirkülasyonu düzenleyen ve gezegenin ısı bütçesini dengeleyen hayati bir ekosistemdir (IPCC, 2021). Güney Okyanusu'nun en dinamik denizel sahalarından biri olan Batı Antarktika Yarımadası (WAP), 20. yüzyılın ikinci yarısında küresel ortalamanın üç katına yaklaşan belirgin bir atmosferik ve oşinografik ısınma sürecine sahne olmuştur (Vaughan vd., 2003; Turner vd., 2014). Her ne kadar 21. yüzyılın başlarında doğal atmosferik dolaşım modlarındaki (SAM ve IPO) salınımlara bağlı olarak bölgesel sıcaklıklarda geçici duraklama ve yavaşlamalar gözlense de (Turner vd., 2016), uzun dönemli eğilimler deniz buzu mevsimsel örtüsünün kısalması, kıyı buz sahanlıklarının geri çekilmesi ve Antarktika krili (*Euphausia superba*) biyokütlesindeki dalgalanmalar yönündedir (Stammerjohn vd., 2008, 2012; Atkinson vd., 2004; Rignot vd., 2019).

Denizel besin ağının üst basamaklarında yer alan kutup penguenleri (*Pygoscelis* cinsi), fiziksel çevre koşullarındaki değişimlere karşı duyarlı indikatör türlerdir (Ainley, 2002; Fraser & Hofmann, 2003). Bu cins içerisinde Adélie pengueni (*Pygoscelis adeliae*), yaşam döngüsü deniz buzuna endeksli bir penguen türüdür (Ainley, 2002). Adélie penguenleri; kış aylarında açık denizdeki paket buz (pack-ice) üzerinde dinlenmekte ve tüy dökmekte, ilkbahar ve yaz aylarında ise kıyı şeridindeki kardan arınmış çıplak kayalık zeminlerde koloni kurarak çakıl taşlarından inşa ettikleri yuvalarda kuluçkaya yatmaktadır (Ainley, 2002; Southwell vd., 2015; Lyver vd., 2014). Türün temel besinini oluşturan Antarktika krili, larva ve jüvenil evrelerinde kış deniz buzunun alt yüzeyindeki mikroalgleri otlayarak hayatta kaldığından, deniz buzu dinamikleri penguenlerin besin teminini doğrudan etkilemektedir (Fraser & Hofmann, 2003; Atkinson vd., 2004; Trivelpiece vd., 2011).

İklimsel süreçlerin Batı Antarktika Yarımadası'ndaki etkileri deniz buzu dinamikleriyle sınırlı değildir. Isınan atmosferin nem taşıma kapasitesinin artması neticesinde, kutup ortamında aşırı yağış anomalileri, ıslak kar ve sıvı yağmur olayları gözlenmektedir (IPCC, 2021; Massom vd., 2006). Kuluçkadan yeni çıkan Adélie yavruları su geçirmez yetişkin tüylerine sahip olmayıp yalnızca ısı yalıtımı sağlayan hav tüyleri ile kaplıdır. Aşırı sıvı yağış veya eriyik çamur altında kalan yavruların tüyleri ıslandığında yalıtım özelliğini yitirmekte; dondurucu rüzgar altında hipotermiye girerek ölüm riskiyle karşılaşmaktadır (Chapman vd., 2011).

Türlerin coğrafi dağılım sınırlarını ve iklim değişikliği karşısındaki duyarlılıklarını anlamak amacıyla Tür Dağılım Modelleri (SDM) yaygın olarak kullanılmaktadır (Elith vd., 2011; Phillips vd., 2006; Fielding & Bell, 1997). Yalnızca varlık (presence-only) verileriyle çalışabilen Maksimum Entropi (MaxEnt) algoritması ekoloji literatüründe sıkça tercih edilmektedir (Phillips vd., 2006).

Uluslararası literatür incelendiğinde; **Wang, Hu ve Yang (Mart 2026, PMID: 42209243 - *Ying Yong Sheng Tai Xue Bao*)** tarafından yayınlanan 'Impact of climate change on the potentially suitable habitat distribution of *Pygoscelis* penguins in Antarctica' başlıklı güncel çalışmada, MaxEnt ve CMIP6 iklim modelleriyle kıtasal ölçekte tüm Antarktika modellenmiştir. Yazarlar, deniz yüzeyi sıcaklığı ve deniz buzunun türün dağılımını belirleyen kritik faktörler olduğunu, yüksek emisyon senaryolarında türün potansiyel habitat alanlarında belirgin daralmalar yaşanacağını bildirmişlerdir (Wang vd., 2026). Benzer şekilde, **Cimino, Lynch, Saba ve Oliver (2016 - *Scientific Reports*)**, CMIP5 modelleri ve varlık-yokluk kayıtlarıyla yaptıkları çalışmada, 2060 yılına kadar mevcut Adélie pengueni kolonilerinin yaklaşık üçte birinin (mevcut popülasyonun ~%20'si) iklim ısınması nedeniyle gerileme sürecine girebileceğini modellemişlerdir.

Ancak, kıtasal veya yarımada ölçeğindeki bu makro araştırmalar (Wang vd., 2026; Cimino vd., 2016), 100–200 km'lik kaba iklim hücreleri nedeniyle yerel topografik etkileri ve çıplak kaya varlığını temsil edememektedir. Bu çalışma, Batı Antarktika Yarımadası'nın güneybatısındaki Marguerite Körfezi'ne odaklanarak 0.25° grid (~288 km²) ölçeğinde mezo-ölçekli bir yerel analiz sunmaktadır. Her ne kadar 0.25° çözünürlük 5 km'den dar fiyortları ve mikro ölçekli kıyı polinyalarını tam olarak ayrıştırmada sınırlılık taşısa da, ERA5 atmosferik/denizel yeniden analizleri ve REMA yükseklik verileriyle yerel çıplak kaya ve deniz buzu etkileşimlerini kıtasal modellere kıyasla çok daha hassas yakalamaktadır. Ayrıca çalışmamızda Roberts vd. (2017) yaklaşımıyla 4 enlem bandı mekânsal blok çapraz doğrulaması yürütülmüş ve CMIP6 IPSL-CM6A-LR SSP2-4.5 iklim senaryosu altındaki ekstrapolasyon belirsizlikleri (clamping) açıkça haritalandırılmıştır.


# Yöntem


## 1.1. Araştırma Sahası ve Biyocoğrafik Sınırlar

Çalışma alanı, Batı Antarktika Yarımadası'nın güneybatı kesiminde yer alan ve Bellingshausen Denizi ile bağlantılı olan **Marguerite Körfezi** ve çevre adalarıdır. Modelleme ızgarası; **65.875°G – 70.625°G enlemleri** ile **63.875°B – 73.125°B boylamları** arasında tanımlanmıştır (xllcorner: -73.125°, yllcorner: -70.625°, cellsize: 0.25°, 37 sütun × 19 satır, toplam 703 grid hücresi). Bu bölge; kuzeyde Adelaide Adası, doğuda Fallières Kıyısı, güneyde George VI Boğazı ve batıda Alexander Adası ile çevrili fiyort ve ada sistemidir (Ducklow vd., 2007; Stammerjohn vd., 2012).

Kutup enlemlerinde meridyenlerin birbirine yaklaşması (enlem daralması - meridian convergence) nedeniyle, 68°G enleminde $\cos(68^\circ) \approx 0.3746$'dır. Bu coğrafi durum neticesinde 0.25° boylam genişliği yalnızca yaklaşık 10.4 km'ye, 0.25° enlem yüksekliği ise 27.8 km'ye karşılık gelmektedir. WGS84 elipsoidi üzerinde bir grid hücresinin yüzölçümü ortalama ~288.3 km² olup, 703 grid hücresinin kapsadığı toplam model kalibrasyon alanı **202.681 km²**'dir. Boylamsal komşu iki hücre merkezi arasındaki mesafe yalnızca ~10.4 km olduğundan, modelin mekânsal inceltme sonrası hücreler arası komşuluk mesafeleri kutup jeodeziği ile tam uyumludur.


## 1.2. Biyolojik Varlık (Presence) Verilerinin Temini ve Mekânsal İnceltme

Adélie penguenine (*Pygoscelis adeliae*) ait coğrafi koordinat verileri, açık kaynak uluslararası biyo-çeşitlilik veri tabanları olan GBIF (Global Biodiversity Information Facility - gbif.org) ve SCAR (Scientific Committee on Antarctic Research) Antarktika Biyo-çeşitlilik Portalı üzerinden derlenmiştir. 2000–2025 yılları arasındaki gözlem kayıtları taranmıştır. Bu kayıtlar; kıyı şeridindeki üreme kolonisi yerleşimlerini ve denizel beslenme/telemetri alanlarındaki birey gözlemlerini içermektedir. Ham veri setine ekolojik modelleme standartlarına uygun olarak şu filtreleme protokolü uygulanmıştır:

- • Koordinat doğruluğu belirsiz (belirsizlik > 5 km) veya hatalı girilmiş kayıtlar ayıklanmıştır.
- • Fosilleşmiş veya tarihsel kolonilere ait eski kayıtlar çalışma kapsamı dışına çıkarılmıştır.
- • Araştırma istasyonları (örn. Rothera İstasyonu) çevresinde yoğunlaşan insan kaynaklı örnekleme yanlılığını (sampling bias) ve mekânsal yığılmayı önlemek amacıyla, çalışma için belirlenen 0.25° × 0.25° analiz gridi içinde hücre başına yalnızca tek bir varlık noktası bırakılacak şekilde **mekânsal inceltme (spatial thinning)** uygulanmıştır.
- • Kıyı çizgisinin dışında kalan veya açık okyanus derinliklerine hatalı koordinatlanmış kayıtlar elenmiştir.
Bu filtreleme neticesinde, Marguerite Körfezi sınırları dahilinde model eğitim ve doğrulamasında kullanılmak üzere **67 adet bağımsız varlık (presence) grid hücresi** elde edilmiştir. Çalışma alanındaki toplam 703 grid hücresinin geri kalan 636 hücresi modelin arka plan (background) çevresel matrisini oluşturmuştur.


## 1.3. Çevresel ve Oşinografik Katmanların Üretimi

Adélie pengueninin üreme ve beslenme ekolojisini kontrol eden biyoklimatik ve çevresel değişkenler, ECMWF ERA5 atmosferik ve denizel yeniden analiz veri setlerinden derlenmiştir. ERA5 verileri 2000–2025 dönemini kapsayan 26 yıllık uzun dönemli aylık ortalamaların sentezlenmesiyle üretilmiştir. Denizel katmanlar olarak; penguenlerin kışlama platformunu ve açık su çatlaklarında avlanmasını temsil eden yıllık ortalama deniz buzu konsantrasyonu (*buz_yillik*, % oran) ve Güney Okyanusu su kütlesi termal rejimini temsil eden deniz yüzeyi sıcaklığı (*sst_yillik*, °C) hesaplanmıştır. Burada SST, endotermik bir kuş olan penguen için doğrudan öldürücü bir fizyolojik sınır olmaktan ziyade, penguenin ana besini olan krilin ve pelajik besin ağının su kütlesi vekili (proxy) niteliğindedir. Atmosferik katman olarak; kuluçka evresindeki civcivlerin ıslanma ve hipotermi riskini temsil eden en sıcak çeyrek (Aralık–Ocak–Şubat yaz mevsimi) toplam yağış miktarı (*bio18*, mm cinsinden) türetilmiştir. Topografik katman olarak ise; Antarktika REMA sayısal yükseklik modeli ve SCAR kaya yüzeyi veri tabanı kullanılarak her bir 0.25° grid hücresindeki çıplak kaya alan yüzdesi (*kaya*, % alan) hesaplanmıştır.

*Tablo 1. Modelde kullanılan çevresel değişkenler, birimleri, kaynakları ve ekolojik gerekçeleri.*


## 1.4. CMIP6 İklim Modeli, Delta Aşağı Ölçekleme ve Regridding Yöntemi

2050 yılı iklim projeksiyonu için Dünya İklim Araştırma Programı (WCRP) CMIP6 veri tabanından **IPSL-CM6A-LR** küresel iklim modeli (ensemble üyesi: r1i1p1f1, senaryo: SSP2-4.5 orta emisyon yolu) temin edilmiştir. Projeksiyon dönemi **2041–2060** (20 yıllık ortalama), tarihsel referans dönemi ise ERA5 ile uyumlu olarak **2000–2025** olarak belirlenmiştir. GCM çıktılarının yerel 0.25° gridimize aktarılmasında küre üzerinde en yakın komşu (nearest complete native cell on sphere) regridding ve delta aşağı ölçekleme yöntemi uygulanmıştır:

- • **Deniz Buzu (buz_yillik):** Gelecek ve referans dönem arasındaki mutlak fark yüzdesi (yüzde puanı), ERA5 günümüz deniz buzu katmanına eklenmiş ve değerler [0, 100] aralığında sınırlandırılmıştır.
- • **Deniz Yüzeyi Sıcaklığı (sst_yillik):** Aylık yerel SST anomalisi ERA5 yıllık deniz suyu sıcaklığına additif olarak eklenmiştir.
- • **Yaz Yağışı (bio18):** Aylık yağış oranları (gelecek/referans yağış oranı) ERA5 aylık yağışlarına uygulanmış; gelecekteki en sıcak çeyrek ayları (tas) yeniden tespit edilerek bio18 gelecekte dinamik olarak baştan hesaplanmıştır.
- • **Çıplak Kaya (kaya):** Jeolojik kaya substratı 2050 yılı projeksiyonunda statik kabul edilmiştir.

## 1.5. Çoklu Eşdoğrusallık ve MaxEnt Matematiksel Temelleri

Ekolojik modellemede yüksek korelasyonlu değişkenlerin kullanımı model parametrelerinin varyansını artırabilmektedir (Dormann vd., 2013). Değişkenler arasında Pearson korelasyon matrisi ve Varyans Şişme Faktörü (VIF) analizi uygulanmış; Dormann vd. (2013) uyarınca **|r| < 0.70** ve VIF < 5 kuralı işletilmiştir. Aday katmanlardan kış minimum sıcaklığı (Bio6) elenmiş; modeldeki 4 değişkenin ikili korelasyonlarının |r| < 0.62 seviyesinde kalarak çoklu eşdoğrusallık riskinin giderildiği doğrulanmıştır.

Maksimum Entropi (MaxEnt 3.4.4) algoritması, Shannon bilgi entropisi ilkesine dayanır (Phillips vd., 2006). Algoritma, türün varlık koordinatlarındaki çevresel ortalamaları kısıt kabul ederek, bu kısıtları sağlayan olasılık dağılımları içerisinden entropisi en yüksek dağılımı $\hat{\pi}(x)$ hesaplar:

$$H(\hat{\pi}) = -\sum_{x \in X} \hat{\pi}(x) \ln \hat{\pi}(x) \quad \text{ve} \quad \mathbb{E}_{\hat{\pi}}[f_j] = \mathbb{E}_{\tilde{\pi}}[f_j]$$

Aşırı öğrenmeyi (overfitting) engellemek amacıyla MaxEnt, objektif fonksiyonuna bir $L_1$ Lasso düzenlileştirme cezası ekler (Phillips vd., 2006): $\max_{\lambda} ( \sum_{i=1}^n \ln P(x_i) - \sum_{j=1}^m \beta_j |\lambda_j| )$. Model çıktısı, türün göreceli uygunluğunu 0 ile 1 arasında ölçekleyen Cloglog dönüşümü ile elde edilmiştir: $P(x) = 1 - \exp(-\exp(\eta(x)))$.


## 1.6. Model Eğitimi, Hiperparametreler ve 10-Katlı Doğrulama

Ekolojik niş modellemesi bağımsız Java ortamında MaxEnt 3.4.4 yazılımıyla yürütülmüştür. 67 adet varlık hücresi ve çalışma alanındaki 636 adet arka plan hücresi (toplam 703 grid hücresi) modele girdi olarak verilmiştir. 60'tan fazla örneklem bulunduğu için model hiperparametreleri olarak varsayılan **LQTH (Linear, Quadratic, Threshold, Hinge)** özellik sınıfları kullanılmış; aşırı öğrenmeyi önlemek için düzenlileştirme çarpanı (Regularization Multiplier = 1.0) seçilmiştir. Model performansı **10 katlı çapraz doğrulama (10-fold CV)** ile sınanmış ve ROC altındaki alan (AUC) hesaplanmıştır (Fielding & Bell, 1997). AUC değerlerinin değerlendirilmesinde Swets (1988) kriterleri esas alınmıştır (Tablo 2).

*Tablo 2. AUC değer aralığının model simülasyon başarısına etkisi (Swets, 1988).*


## 1.7. Mekânsal Çapraz Doğrulama (Spatial Block CV) Tasarımı

Standart rastgele çapraz doğrulamada, mekânsal otokorelasyon nedeniyle test noktaları eğitim noktalarına yakın düşmekte ve AUC değerleri iyimser tahmin edilebilmektedir (Roberts vd., 2017). Modelin coğrafi aktarılabilirliğini sınamak amacıyla, çalışma alanı 4 coğrafi enlem bandına (-66.625°, -67.375°, -67.875° sınırları) bölünerek mekânsal bloklama testi gerçekleştirilmiştir. Eşit eğitim boyutu (50-51 nokta) ve sabit rastgele tohumla (20261108) eşleştirilmiş rastgele 4 katlı modelle doğrudan kıyaslanmıştır.


## 1.8. CBS ve Kartografik Projeksiyon Altyapısı

MaxEnt'ten üretilen ham Cloglog ASCII raster çıktıları, QGIS 3.x açık kaynak Coğrafi Bilgi Sistemleri yazılımına aktarılmıştır. Kutup bölgelerinde alan ve şekil bozulmalarını en aza indirmek için harita projeksiyonu **EPSG:3031 (WGS 84 / Antarctic Polar Stereographic)** olarak tanımlanmıştır. Günümüz (2000–2025), 2050 gelecek, mekânsal fark (Gelecek − Günümüz) ve belirsizlik haritaları 300 DPI çözünürlükte, koordinat gridi, istasyon katmanları ve standart lejantlarıyla kartografik standartta üretilmiştir.


## 1.9. Proje İş-Zaman Çizelgesi ve Gerçekleşme Takvimi

Projenin araştırma, veri hazırlığı, modelleme, analiz ve raporlama süreçleri aşağıdaki 8 temel iş paketi çerçevesinde 6 aylık periyotta planlanmış ve başarıyla yürütülmüştür (Tablo 3):

*Tablo 3. Proje iş-zaman çizelgesi ve gerçekleşme takvimi.*


# Bulgular


## 2.1. Alıcı İşletim Karakteristiği (ROC) Eğrisi ve Model Doğruluğu

Alıcı İşletim Karakteristiği (ROC) eğrisi, modelin duyarlılığı ile (1 - özgüllük) arasındaki ilişkiyi gösterir. 10 katlı çapraz doğrulama (10-fold CV) analizi sonucunda, test verileri üzerinden hesaplanan ortalama AUC değeri **0.768 ± 0.111** olarak gerçekleşmiştir (Şekil 1). Eğitim verilerine ait AUC değeri ise **0.838** olarak belirlenmiştir. Swets (1988) kriterlerine göre 0.768 test AUC değeri, kalibrasyon alanı içinde modelin 'İyi / Kabul Edilebilir' ayırt edicilik düzeyine sahip olduğunu göstermektedir.


![Şekil 1. ROC Eğrisi](/home/halil/adelie-maxent-2204c/maxent/cikti/deneme3/plots/Pygoscelis_adeliae_roc.png)
*Şekil 1. Adélie pengueni MaxEnt modeline ait 10 katlı çapraz doğrulama ROC eğrisi.*

## 2.2. Biyoklimatik Değişkenlerin Göreceli Katkı ve Permütasyon Önemleri

MaxEnt algoritması, çevresel değişkenlerin modele etkisini iki tamamlayıcı metrikle raporlamaktadır: **Göreceli Katkı Yüzdesi (Percent Contribution)** ve **Permütasyon Önemi (Permutation Importance)**. Katkı yüzdesi, eğitim algoritmasının yinelemeleri sırasında ilgili değişkenin düzenlenmiş kazançta (gain) yarattığı artışa dayanır. Permütasyon önemi ise eğitim verilerindeki değişken değerlerinin rastgele karıştırılması sonucu AUC değerindeki düşüşü ölçer ve değişkenler arası korelasyondan daha az etkilenen bir göstergedir. 10 kat modelinin değişken önem metrikleri Tablo 4'te sunulmuştur.

*Tablo 4. Çevresel değişkenlerin MaxEnt modeline katkı yüzdeleri ve permütasyon önemleri (10 kat ortalaması).*

Tablo 4 verileri incelendiğinde; hem göreceli katkı yüzdesinde (%43.1) hem de permütasyon öneminde (%55.6) yıllık deniz buzu konsantrasyonunun (*buz_yillik*) en belirleyici faktör olduğu görülmektedir. Çıplak kaya alanı (*kaya*) ise eğitim yinelemelerinde %30.0 katkı yüzdesi sağlamasına rağmen permütasyon öneminde %9.1 seviyesinde kalmıştır. Bu durum, kayalık alanların kıyı şeridinde kolonileşme için zorunlu bir fiziksel ön koşul teşkil ettiğini, ancak çalışma alanının tamamındaki habitat uygunluk gradyanını asıl şekillendiren etkenlerin denizel oşinografik değişkenler (deniz buzu %55.6 ve deniz sıcaklığı %18.3) olduğunu ortaya koymaktadır.


## 2.3. Jackknife Yöntemiyle Değişken Kazanç Analizleri

Jackknife testi, her bir çevresel değişkenin model kazancına (gain) olan etkisini iki tamamlayıcı yaklaşımla inceler: (1) Değişken modelde tek başına kullanıldığında sağladığı kazanç (mavi çubuk), (2) İlgili değişken modelden çıkarıldığında toplam kazançta meydana gelen kayıp (yeşil çubuk). 10 katlı modelin Jackknife test sonuçları Şekil 2'de gösterilmiştir.


![Şekil 2. Jackknife Grafiği](/home/halil/adelie-maxent-2204c/maxent/cikti/deneme3/plots/Pygoscelis_adeliae_jacknife.png)
*Şekil 2. Çevresel değişkenlerin Jackknife kazanç analizi.*
Jackknife grafiği incelendiğinde; modelde tek başına kullanıldığında en yüksek düzenlenmiş eğitim kazancını sağlayan değişkenin **en sıcak çeyrek yağışı (*bio18*, ~0.287 kazanç)** olduğu, bunu **yıllık deniz buzu konsantrasyonunun (*buz_yillik*, ~0.210 kazanç)** izlediği görülmektedir. Çıplak kaya (*kaya*) tek başına ~0.139, deniz yüzeyi sıcaklığı (*sst_yillik*) ise ~0.058 kazanç sağlamıştır.

Buna karşılık, modelden çıkarıldığında düzenlenmiş eğitim kazancını en fazla düşüren değişken **yıllık deniz buzu konsantrasyonu (*buz_yillik*)** olmuştur (kazanç tam modeldeki 0.592'den 0.441'e gerilemektedir). Bunu deniz yüzeyi sıcaklığı (*sst_yillik*, 0.483'e gerileme) izlemiştir. Bu durum; tek başına en yüksek ayırt ediciliği *bio18* sağlasa da, modelden çıkarıldığında telafi edilemeyen en özgün ve bağımsız bilgi içeriğinin deniz buzu örtüsünde bulunduğunu göstermektedir.


## 2.4. Çevresel Değişkenlerin Biyolojik Tepki Eğrileri (Response Curves)

Tepki eğrileri (response curves), diğer tüm değişkenler ortalama değerlerinde sabit tutulduğunda tek bir çevresel faktörün değişimine bağlı olarak Adélie pengueni habitat uygunluk puanının (Cloglog değeri, 0–1 aralığı) nasıl değiştiğini grafiksel olarak yansıtır. Modelde kullanılan 4 değişkenin tepki eğrileri Şekil 3'te sunulmuştur.


![Şekil 3. Tepki Eğrileri](/home/halil/adelie-maxent-2204c/rapor/fig_response_4panel.png)
*Şekil 3. Çevresel değişkenlere ait biyolojik tepki eğrileri.*
Tepki eğrileri ham model verileri (.dat) ve grafiklerdeki gerçek sayısal değerler doğrultusunda incelendiğinde türün çevresel tepkileri şu şekilde özetlenmektedir:

- • **Deniz Buzu Konsantrasyonu (Şekil 3a):** Habitat uygunluğu %20–%25 marjinal buz konsantrasyonunda zirveye ulaşmakta (~0.997 Cloglog puanı); konsantrasyon arttıkça uygunluk kademeli olarak düşerek %40'ta ~0.74, %50'de ~0.43 seviyesine gerilemekte ve %60.8'de minimum ~0.154 değerine inmektedir. %65–%69 bandında ise ~0.34 seviyesinde seyretmektedir. Bu eğilim, Adélie penguenlerinin dalış ve avlanma için polinyalara ve marjinal buz kenarlarına ihtiyaç duymasıyla uyumludur (Ainley, 2002).
- • **Çıplak Kaya Yüzdesi (Şekil 3b):** Çıplak kayanın bulunmadığı alanlarda uygunluk taban seviyesinde (~0.75 Cloglog puanı) kalırken, kaya yüzdesi arttıkça yükselerek %15–17 aralığında 0.948 zirvesine ulaşmaktadır. Bu eğilim, çakıl yuva inşası ve kuluçka için kardan arınmış sert kayalık zemine duyulan gereksinimi yansıtmaktadır (Southwell vd., 2015).
- • **Yaz Yağışı / Bio18 (Şekil 3c):** Uygunluk 184 mm civarında zirveye (~0.960 puan) ulaşmakta; 400 mm seviyesinde ~0.81 puan ile yüksek kalmaya devam etmekte, ancak 600 mm'nin üzerine çıktığında ~0.55–0.60 bandına gerilemektedir. Bu durum, aşırı yağış koşullarında yavru hipotermi riskini yansıtmaktadır (Chapman vd., 2011).
- • **Deniz Sıcaklığı / SST (Şekil 3d):** -1.94°C ile -1.50°C arasındaki soğuk kutup sularında en yüksek uygunluk (0.903–0.816 puan) gözlenirken, deniz suyu sıcaklığı -0.80°C'nin üzerine çıktığında uygunluk hızla düşerek -0.50°C'de 0.118 seviyesine inmektedir. Bu bulgu, pelajik kril ekolojisiyle uyumlu oşinografik su kütlesi toleransını temsil etmektedir (Cimino vd., 2016).

## 2.5. Mekânsal Çapraz Doğrulama (Spatial Block CV) Bulguları

Modelin mekânsal otokorelasyona karşı duyarlılığını ve coğrafi aktarılabilirliğini sınamak amacıyla Roberts vd. (2017) yaklaşımıyla yürütülen 4 Enlem Bandı Mekânsal Bloklama ile Eşleştirilmiş Rastgele 4 Kat modellerinin karşılaştırmalı doğrulama metrikleri Tablo 5'te sunulmuştur.

*Tablo 5. Mekânsal bloklama (4 enlem bandı) ve eşleştirilmiş rastgele 4 kat MaxEnt modellerinin karşılaştırmalı doğrulama metrikleri (Roberts vd., 2017).*

Tablo 5'teki sonuçlar, ekolojik modellemede mekânsal otokorelasyonun değerlendirilmesinin önemini ortaya koymaktadır: Standart rastgele çapraz doğrulamada AUC değerleri 0.715 ile 0.765 arasında seyrederken, çalışma sahası coğrafi enlem bantlarına bölündüğünde AUC değerleri 0.477–0.580 bandına gerilemektedir. Rastgele bölmede eğitim ve test noktaları birbirine yakın komşu hücrelerden seçilebildiğinden aralarındaki medyan mesafe 12.6 km iken (68°G kutup enleminde meridyen yakınsaması sebebiyle 0.25° boylam genişliği ~10.4 km olup komşu hücre merkezleri 10.4–12.6 km aralığındadır), mekânsal bloklamada bu mesafe 45.4 km'ye çıkmaktadır. Test noktaları eğitilen enlem bandından uzaklaştıkça omission oranı artış göstermektedir. Bu bulgu; yerel fiyort ve ada topografyasının yarattığı mikroklimatik koşulların model tarafından coğrafi olarak genellenmesinde sınırlılıklar bulunduğunu ve modelin coğrafi aktarılabilirlik sınırlarının açıkça kabul edilmesi gerektiğini göstermektedir.


## 2.6. Kartografik Dağılım ve Değişim Haritaları


### 2.6.1. Marguerite Körfezi Günümüz (2000–2025) Çevresel Uygunluk Haritası

MaxEnt modelinin günümüz ERA5 (2000–2025) ortalamalarıyla çalıştırılması neticesinde elde edilen Cloglog habitat uygunluk haritası Şekil 4'te sunulmuştur. Haritada 0.60 üzerindeki yüksek uygunluk alanlarının Adelaide Adası'nın kıyı kesimlerinde, körfezin iç fiyort girişlerinde ve George VI Boğazı'nın kuzey ağzında yoğunlaştığı gözlenmektedir. Bu alanlar, kuluçka için gerekli çıplak kayalıkların ve uygun marjinal deniz buzu dinamiklerinin bir arada bulunduğu kıyı kesimleriyle örtüşmektedir.


![Şekil 4. Günümüz Haritası](/home/halil/adelie-maxent-2204c/harita/cmip6_ipsl_2050_v1/gunumuz_A4.png)
*Şekil 4. Günümüz çevresel uygunluk haritası (2000–2025).*
Günümüz haritası incelendiğinde; Bellingshausen Denizi'ne bakan açık okyanus kesimlerinde çıplak kaya substratının bulunmaması nedeniyle uygunluk değerlerinin 0.10'un altında kaldığı görülmektedir. Buna karşılık Adelaide Adası'nın korunaklı boğazları ve fiyort ağızları, Adélie penguenlerinin biyolojik gereksinimleriyle uyumlu uygun çevre koşulları sunmaktadır.


### 2.6.2. CMIP6 IPSL-CM6A-LR SSP2-4.5 (2041–2060) Gelecek Projeksiyon Haritası

CMIP6 IPSL-CM6A-LR modelinin orta düzey sera gazı emisyon senaryosu (SSP2-4.5) altında 2050 yılı (2041–2060 dönemi) potansiyel habitat uygunluk projeksiyonu Şekil 5'te sunulmuştur. Projeksiyon haritası incelendiğinde; kuzey ve batı fiyortlarında habitat uygunluğunda gerilemeler gözlenirken, körfezin güneyindeki korunaklı boğaz alanlarında uygunluk değerlerinin korunduğu veya kısmen arttığı görülmektedir.


![Şekil 5. 2050 Projeksiyon Haritası](/home/halil/adelie-maxent-2204c/harita/cmip6_ipsl_2050_v1/2050_A4.png)
*Şekil 5. 2050 yılı potansiyel habitat uygunluk haritası (CMIP6 SSP2-4.5).*
2050 projeksiyonu, ısınan deniz suyu ve azalan kış deniz buzu nedeniyle türün geleneksel üreme ve avlanma alanlarında mekânsal baskıların artacağını ortaya koymaktadır. Özellikle Adelaide Adası'nın açık deniz etkisine açık batı kıyılarında uygunluk puanlarında belirgin azalmalar gözlenmiştir.


### 2.6.3. 2050 Yılı Mekânsal Değişim ve Uygunluk Fark Haritası

Gelecek uygunluk puanı ile günümüz uygunluk puanı arasındaki fark (Δ = Gelecek − Günümüz) piksel bazında hesaplanarak mekânsal değişim haritası oluşturulmuştur (Şekil 6). Fark değerleri ±0.05 mutlak puan eşiğinde sınıflandırılmış; modelin eşik duyarlılığı Tablo 6'da ve alan dağılımı Tablo 7'de özetlenmiştir (Liu vd., 2005).


![Şekil 6. Değişim Haritası](/home/halil/adelie-maxent-2204c/harita/cmip6_ipsl_2050_v1/degisim_A4.png)
*Şekil 6. 2050 yılı çevresel uygunluk değişim haritası.*
Şekil 6'da görüldüğü üzere; körfezin kuzeybatı girişi ve Adelaide Adası'nın batı kıyılarında kırmızı renkle (Δ < -0.05) temsil edilen uygunluk kaybı alanları dikkat çekmektedir. Buna karşılık iç fiyortlar ve George VI Boğazı ağzında yeşil renkle (Δ > +0.05) gösterilen uygunluk artış eğilimi öne çıkmaktadır. Ancak buradaki artış, deniz buzu incelmesine bağlı kuramsal bir değişim olup, George VI Boğazı'nın kalıcı şelf buzuyla kaplı olması nedeniyle kesin bir ekolojik sığınak (refugium) olarak değil, sahada test edilmesi gereken bir hipotez olarak yorumlanmalıdır.

*Tablo 6. Farklı lojistik değişim eşiklerine göre 2050 yılı habitat değişim sınıflarının duyarlılık dağılımı (Liu vd., 2005).*

*Tablo 7. CMIP6 SSP2-4.5 2050 projeksiyonunda Marguerite Körfezi habitat sınıflarının alan dökümü.*


### 2.6.4. Ekstrapolasyon, Novel Climate ve Clamping Belirsizlik Haritası

İklim projeksiyonlarında çevresel değişkenlerin eğitim sınırlarını aşması durumunda model ekstrapolasyon uygular (Phillips vd., 2006). Çalışma alanındaki 703 grid hücresinin **357 adedinde (%50.8 / 102.500 km²)** clamping gerçekleşmiştir (Şekil 7). Clamping işlemlerinin önemli kısmı artan deniz yüzeyi sıcaklığı (SST) ve sıvı yağış (Bio18) değişkenlerinin günümüz üst sınırlarını aşmasından kaynaklanmıştır. Bu durum, 2050 yılı projeksiyonunun geniş bir ekstrapolasyon belirsizliği barındırdığını ve sonuçların temkinle yorumlanması gerektiğini göstermektedir.


![Şekil 7. Belirsizlik Haritası](/home/halil/adelie-maxent-2204c/harita/cmip6_ipsl_2050_v1/belirsizlik_A4.png)
*Şekil 7. Ekstrapolasyon ve Clamping belirsizlik haritası.*

# Sonuç ve Tartışma

Bu araştırmada, Batı Antarktika Yarımadası'nın hassas denizel sahalarından biri olan Marguerite Körfezi'nde Adélie pengueninin (*Pygoscelis adeliae*) günümüz (2000–2025) ve 2050 yılı potansiyel habitat uygunluğu, ERA5 yeniden analizleri, REMA topoğrafyası ve CMIP6 IPSL-CM6A-LR iklim projeksiyonları ile modellenmiştir. Elde edilen bulgular, kutup ekolojisi literatürü ve metodolojik sınırlılıklar ışığında değerlendirilmiştir.

Model sonuçlarında yıllık deniz buzu konsantrasyonunun %43.1 katkı yüzdesi ve %55.6 permütasyon önemi ile birincil belirleyici çıkması, Adélie pengueninin deniz buzu dinamiklerine duyarlı yapısını ortaya koyan ekolojik literatürle (Ainley, 2002; Fraser & Hofmann, 2003) uyum sergilemektedir. Tepki eğrilerinde görülen %20–%25 marjinal buz optimumu; penguenlerin avlandığı kril sürülerinin buz altı algleriyle beslenmesi için yeterli buz örtüsüne ihtiyaç duymasını, ancak aynı zamanda dalış yapabilmek için açık su kanallarına ve polinyalara gereksinim duymasını yansıtmaktadır. Aşırı kapalı kütlesel buz örtüsünde dalış erişiminin düşmesi bu dengenin hassasiyetine işaret etmektedir.

Giriş bölümünde incelenen **Wang, Hu ve Yang'ın (2026, PMID: 42209243 - *Ying Yong Sheng Tai Xue Bao*)** tüm Antarktika ölçeğindeki MaxEnt ve CMIP6 bulgularıyla karşılaştırıldığında; Wang vd. (2026), Kuzey Antarktika Yarımadası'ndaki kolonilerin yüzyılın ortasına kadar daralacağını ve türün çekirdek popülasyonlarının Ross Denizi ve Doğu Antarktika kıyılarına çekileceğini öngörmüşlerdir. Bizim mezo-ölçekli çalışmamız, bu makro eğilimle uyumlu olarak körfez genelinde %42.2 oranında (89.155 km²) bir habitat uygunluk azalması tespit etmiştir.

**'Refugia' ve George VI Boğazı Tartışması:** Model çıktılarında körfezin güneyindeki George VI Boğazı girişinde %34.6 oranında (68.460 km²) uygunluk artışı (Δ > +0.05) gözlenmiştir. Ancak bu artış doğrudan kesin bir 'ekolojik sığınak' (refugium) olarak kabul edilemez. Bir hücrede Δ > +0.05 çıkması, o alanın penguen kolonileri için yaşanabilir bir habitat olduğunu kanıtlamaz; çünkü taban uygunluğu çok düşük olan bir hücrede matematiksel bir artış yaşansa dahi mutlak uygunluk penguen için yetersiz kalabilir. Dahası, George VI Boğazı günümüzde yüzlerce metre kalınlığında kalıcı şelf buzuyla kaplıdır ve kuluçka için zorunlu olan çıplak kaya substratından yoksundur. Buradaki uygunluk artışı, CMIP6 modelindeki deniz buzu incelmesine MaxEnt algoritmasının verdiği kuramsal bir tepkidir. Dolayısıyla George VI Boğazı bir 'ispatlanmış sığınak' değil, gelecekte şelf buzu erimesi durumunda potansiyel taşıyabilecek, sahada test edilmesi gereken bir **bölgesel hipotezdir**.

Çalışmamızda yaz yağışlarının (*bio18*) %17.1'lik permütasyon önemine sahip olması, Chapman vd. (2011) ve Massom vd. (2006) tarafından vurgulanan sıvı yağmur ve ıslak karın civciv ölümlerine yol açma riski hipotezini desteklemektedir. Tepki eğrisinde yağış miktarı 600 mm'yi aştığında uygunluk puanının gerilemesi, iklim değişikliğiyle birlikte yağış fazının sıvıya kaymasının yaratabileceği olumsuz etkileri yansıtmaktadır.

**Mekânsal Bloklama ve Sınırlılıklar:** Roberts vd. (2017) yaklaşımıyla gerçekleştirdiğimiz 4 enlem bandı mekânsal blok çapraz doğrulama testleri ekolojik metodoloji açısından kritik bir gerçeği vurgulamaktadır: Standart rastgele kat bölmelerinde 0.715–0.765 bandında çıkan AUC değerleri, coğrafi enlemler ayrıştırıldığında 0.477–0.580 bandına gerilemiştir. Bu sonuç; modelin eğitildiği enlem bandı dışındaki coğrafi sahalara aktarılmasında belirgin sınırlılıklar bulunduğunu ve kutup modellerinde mekânsal otokorelasyon denetlenmeden üretilen projeksiyonlara şüpheyle yaklaşılması gerektiğini göstermektedir.

Son olarak, 2050 iklim projeksiyonunda 357 hücrede (%50.8) clamping uygulanması ve çalışmanın tek bir GCM (IPSL-CM6A-LR) ile tek bir senaryoya (SSP2-4.5) dayanması, bu projeksiyonların kesin bir gelecek tahmini değil, **keşifsel (exploratory)** bir ilk değerlendirme olduğunu ortaya koymaktadır. Gelecek araştırmalarda çoklu model toplulukları (ensemble) dahil edilmesi belirsizlikleri azaltacaktır (Araújo & New, 2007).


# Öneriler

Bu araştırma kapsamında elde edilen bulgular ve metodolojik sınırlılıklar doğrultusunda, ulusal ve uluslararası kutup araştırmaları için şu somut öneriler geliştirilmiştir:

- • 1. **TÜBİTAK MAM Kutup Araştırmaları Enstitüsü (KARE) ve Ulusal Seferler (TAE):** Türkiye'nin düzenlediği Ulusal Antarktika Bilim Seferleri (TAE) kapsamında, modelin mekânsal aktarılabilirlik sınırlarını ve George VI Boğazı'ndaki kuramsal uygunluk artışının ekolojik fizibilitesini test etmek amacıyla, Marguerite Körfezi güney fiyortlarında yerinde saha doğrulaması (ground truthing) ve denizel gözlem çalışmaları planlanmalıdır.
- • 2. **GPS Telemetri ve Uydu Vericileri ile İzleme:** Modelin varlık-arka plan kısıtlarını gidermek ve gerçek varlık-yokluk dinamiklerini yakalamak amacıyla, körfezdeki Adélie kolonilerine uydu bağlantılı GPS telemetri cihazları takılarak bireylerin kışlama ve beslenme rotaları gerçek zamanlı izlenmelidir (Cimino vd., 2016).
- • 3. **Çoklu Model Toplulukları (Ensemble SDM) ve Yüksek Çözünürlük:** Gelecek projeksiyonlarındaki clamping (%50.8) ve tek model belirsizliğini azaltmak için birden fazla GCM (örn. MPI-ESM1-2-HR, CNRM-CM6-1) ve farklı emisyon senaryoları (SSP1-2.6, SSP5-8.5) bir araya getirilerek topluluk (ensemble) modellemesi yürütülmelidir (Araújo & New, 2007).
- • 4. **Deniz Koruma Alanları (MPA) ve CCAMLR Kapsamı:** Antarktika Deniz Yaşamı Kaynaklarının Korunması Komisyonu (CCAMLR) nezdinde, habitat daralması öngörülen körfez girişinde endüstriyel kril (*Euphausia superba*) avcılığı kotaları yakından takip edilmeli; güney fiyortlarının koruma statüleri değerlendirilmelidir.
- • 5. **Yüksek Çözünürlüklü Optik Uydu ve İHA ile Koloni Takibi:** Ulaşımı güç fiyort adacıklarındaki kolonilerin tespiti için Sentinel-2 ve yüksek çözünürlüklü ticari uydu görüntüleri ile insansız hava araçları (İHA) üzerinden guano lekesi analizi ve sayım çalışmaları yürütülmelidir (Southwell vd., 2015).
- • 6. **Otomatik Meteoroloji İstasyonları (AWS) ile Yerel Yağış İzleme:** Kuluçka döneminde civciv ölümlerine yol açabilecek aşırı sıvı yağış olaylarının takibi için körfez kıyısındaki üreme kolonilerine gerçek zamanlı mikroklimatik otomatik meteoroloji istasyonları (AWS) kurulması önerilmektedir (Chapman vd., 2011).

# Kaynaklar

Ainley, D. G. (2002). *The Adélie Penguin: Bellwether of Climate Change*. Columbia University Press, New York. https://doi.org/10.7312/ainl12304

Araújo, M. B., & New, M. (2007). Ensemble forecasting of species distributions. *Trends in Ecology & Evolution*, 22(1), 42–47. https://doi.org/10.1016/j.tree.2006.09.010

Atkinson, A., Siegel, V., Pakhomov, E., & Rothery, P. (2004). Long-term serious decline in Antarctic krill stock and increase in salps in Southern Ocean. *Nature*, 432(7013), 100–103. https://doi.org/10.1038/nature02996

Chapman, E. W., Hofmann, E. E., Patterson, D. L., & Fraser, W. R. (2011). The effects of climate change on normal and anomalous weather conditions in the Western Antarctic Peninsula: Consequences for Adélie penguin populations. *Marine Ecology Progress Series*, 429, 247–260. https://doi.org/10.3354/meps09108

Cimino, M. A., Lynch, H. J., Saba, V. S., & Oliver, M. J. (2016). Projected asymmetric response of Adélie penguins to Antarctic climate change. *Scientific Reports*, 6, 28785. https://doi.org/10.1038/srep28785

Dormann, C. F., Elith, J., Bacher, S., Buchmann, C., Carl, G., Carré, G., Marquéz, J. R. G., Gruber, B., Lafourcade, B., Leitão, P. J., Münkemüller, T., McClean, C., Osborne, P. E., Reineking, B., Schröder, B., Skidmore, A. K., Zurell, D., & Lautenbach, S. (2013). Collinearity: A review of methods to deal with it and a simulation study evaluating their performance. *Ecography*, 36(1), 27–46. https://doi.org/10.1111/j.1600-0587.2012.07348.x

Ducklow, H. W., Baker, K., Martinson, D. G., Quetin, L. B., Ross, R. M., Smith, R. C., Stammerjohn, S. E., Vernet, M., & Fraser, W. (2007). Marine ecosystems: The West Antarctic Peninsula. *Philosophical Transactions of the Royal Society B: Biological Sciences*, 362(1477), 67–94. https://doi.org/10.1098/rstb.2006.1955

Elith, J., Phillips, S. J., Hastie, T., Dudík, M., Chee, Y. E., & Yates, C. J. (2011). A statistical explanation of MaxEnt for ecologists. *Diversity and Distributions*, 17(1), 43–57. https://doi.org/10.1111/j.1472-4642.2010.00725.x

Fielding, A. H., & Bell, J. F. (1997). A review of methods for the assessment of prediction errors in conservation presence/absence models. *Environmental Conservation*, 24(1), 38–49. https://doi.org/10.1017/S0376892997000088

Fraser, W. R., & Hofmann, E. E. (2003). A predator's perspective on causal links between climate change, physical forcing and ecosystem response. *Marine Ecology Progress Series*, 265, 1–15. https://doi.org/10.3354/meps265001

IPCC. (2021). *Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change*. Cambridge University Press, Cambridge, UK and New York, NY, USA. https://doi.org/10.1017/9781009157896

Liu, C., Berry, P. M., Dawson, T. P., & Pearson, R. G. (2005). Selecting thresholds of occurrence in the prediction of species distributions. *Journal of Biogeography*, 32(1), 51–63. https://doi.org/10.1111/j.1365-2699.2004.01149.x

Lyver, P. O., Barron, M., Barton, K. J., Ainley, D. G., Pollard, A., Gordon, S., McNeill, S., Ballard, G., & Wilson, P. R. (2014). Trends in the breeding population of Adélie penguins in the Ross Sea, 1981–2012: A coincidence of climate and resource extraction effects. *PLOS ONE*, 9(3), e91188. https://doi.org/10.1371/journal.pone.0091188

Massom, R. A., Stammerjohn, S. E., Smith, R. C., Pook, M. J., Iannuzzi, R. A., Adams, N., & Fraser, W. R. (2006). Extreme anomalous atmospheric circulation in the West Antarctic Peninsula region in Austral spring and summer 2001/02, and its ecological consequences. *Antarctic Science*, 18(3), 403–418. https://doi.org/10.1017/S0954102006000454

Phillips, S. J., Anderson, R. P., & Schapire, R. E. (2006). Maximum entropy modeling of species geographic distributions. *Ecological Modelling*, 190(3–4), 231–259. https://doi.org/10.1016/j.ecolmodel.2005.03.026

Rignot, E., Mouginot, J., Scheuchl, B., van den Broeke, M., van Wessem, M. J., & Morlighem, M. (2019). Four decades of Antarctic Ice Sheet mass balance from 1979–2017. *Proceedings of the National Academy of Sciences*, 116(4), 1095–1103. https://doi.org/10.1073/pnas.1812883116

Roberts, D. R., Bahn, V., Ciuti, S., Boyce, M. S., Elith, J., Guillera-Arroita, G., Hauenstein, S., Lahoz-Monfort, J. J., Schröder, B., Thuiller, W., Warton, D. I., Wintle, B. A., Hartig, F., & Dormann, C. F. (2017). Cross-validation strategies for data with spatial, temporal, or phylogenetic structure. *Ecography*, 40(8), 913–929. https://doi.org/10.1111/ecog.02881

Southwell, C., Emmerson, L., McKinlay, J., Newbery, K., Takahashi, A., Kato, A., & Trathan, P. (2015). Spatially extensive standardized surveys reveal widespread, stable abundance of an Antarctic top predator. *Diversity and Distributions*, 21(1), 23–33. https://doi.org/10.1111/ddi.12260

Stammerjohn, S. E., Martinson, D. G., Smith, R. C., & Iannuzzi, R. A. (2008). Sea ice in the western Antarctic Peninsula region: Spatio-temporal variability from ecological and climatological perspectives. *Deep Sea Research Part II: Topical Studies in Oceanography*, 55(18–19), 2041–2058. https://doi.org/10.1016/j.dsr2.2008.04.026

Stammerjohn, S., Massom, R., Rind, D., & Martinson, D. (2012). Regions of rapid sea ice change: An inter-hemispheric seasonal comparison. *Geophysical Research Letters*, 39(6), L06501. https://doi.org/10.1029/2012GL050874

Swets, J. A. (1988). Measuring the accuracy of diagnostic systems. *Science*, 240(4857), 1285–1293. https://doi.org/10.1126/science.3287615

Trivelpiece, W. Z., Hinke, J. T., Miller, A. K., Reiss, C. S., Trivelpiece, S. G., & Watters, G. M. (2011). Variability in krill biomass links harvesting and climate warming to penguin population declines in Antarctica. *Proceedings of the National Academy of Sciences*, 108(18), 7625–7628. https://doi.org/10.1073/pnas.1016560108

Turner, J., Barrand, N. E., Bradbury, W. M., Chelliah, M., Garabato, A. C. N., & Phillips, T. (2014). Antarctic climate change and the environment: An update. *Polar Record*, 50(3), 237–259. https://doi.org/10.1017/S0032247413000296

Turner, J., Lu, H., White, I., King, J. C., Phillips, T., Hosking, J. S., Bracegirdle, T. J., Marshall, G. J., Mulvaney, R., & Deb, P. (2016). Absence of 21st century warming on Antarctic Peninsula consistent with natural variability. *Nature*, 535(7612), 411–415. https://doi.org/10.1038/nature18645

Vaughan, D. G., Marshall, G. J., Connolley, W. M., Parkinson, C., Mulvaney, R., Hodgson, D. A., King, J. C., Pudsey, C. J., & Turner, J. (2003). Recent rapid regional climate warming on the Antarctic Peninsula. *Climatic Change*, 60(3), 243–274. https://doi.org/10.1023/A:1026021217991

Wang, J., Hu, M., & Yang, J. (2026). Impact of climate change on the potentially suitable habitat distribution of Pygoscelis penguins in Antarctica. *Ying Yong Sheng Tai Xue Bao (The Journal of Applied Ecology)*, 37(3), 926–932. https://doi.org/10.13287/j.1001-9332.202603.028 [PMID: 42209243]

