# TÜBİTAK 2204 C Kutup Araştırmaları Proje Raporu

**Proje ana alanı:** Kutup Araştırmaları - Biyoloji ve Ekoloji

**Proje tematik alanı:** Kutup Biyoçeşitliliği ve Ekosistem Dinamikleri

**Proje adı:** Marguerite Körfezi odaklı Adélie pengueni koloni bulunuşunun modellenmesi ve iklim projeksiyonlarının güvenilirliğinin değerlendirilmesi

**Analiz durumu:** 12 Kasım 2026. Aşağıda tamamlanan genel bulunuş denetimleri ile henüz sonuçlanmamış koloni modellemesi ayrı sunulmaktadır. Geniş alan koloni modeli, buna ait 2050 haritaları ve nihai ekolojik sonuçlar beklenmektedir.

# Özet

Bu çalışma, Marguerite Körfezi çevresinde Adélie pengueninin (*Pygoscelis adeliae*) koloni bulunuşunu çevresel değişkenlerle ilişkilendirmeyi ve geleceğe aktarılacak modellerin güvenilirliğini sınamayı amaçlamaktadır. İlk genel bulunuş modelinin denetiminde, kıyı ve deniz gözlemlerinin doğrulanmış üreme kayıtlarından ayrılmadığı, kayıt döneminin iklim dönemiyle tam eşleşmediği ve model seçiminin coğrafi aktarılabilirlik kanıtıyla yeterince desteklenmediği belirlenmiştir. Bu nedenle önceki uygunluk değişimi yüzdeleri koloni veya habitat kaybı sonucu olarak kullanılmamıştır.

Tamamlanan yeniden analizde, 2000-2025 dönemine ait 61 genel bulunuş hücresi ve 579 hücrelik aday kıyı desteği üzerinde iki değişken seti, beş özellik-düzenlileştirme ayarı ve altı mekânsal bölme şeması karşılaştırılmıştır. Toplam 240 eğitimde çevresel adayların hiçbirinin şema bazındaki ortalama AUC değeri, en yakın eğitim kaydına uzaklık referansını aşmamıştır. Üç CMIP6 modeliyle yapılan duyarlılık analizinde aynı iklim modeli altında dahi MaxEnt ayarına göre ortalama uygunluk farkının yönü değişmiştir. Bu sonuç, doğrulanmış bir ekolojik daralma değil, mevcut çıkarımın veri ve model tasarımına duyarlılığıdır.

Yeni hedef yalnızca MAPPPD pozitif yuva sayımlarına dayalı koloni bulunuşudur. Yerel kayıtlar 19 yerleşimden 14 çevresel hücreye düştüğü için eğitim alanının genişletilmesi, sonuçların ise Marguerite odağında raporlanması benimsenmiştir. Geniş alanın çevresel girdileri ve koloni doğrulaması tamamlanmadığından bu sürümde yeni koloni uygunluğu, kayıp alanı veya sığınak haritası sunulmamaktadır.

**Anahtar kelimeler:** Adélie pengueni, koloni bulunuşu, MaxEnt, Marguerite Körfezi, mekânsal doğrulama, model belirsizliği.

# Amaç

Araştırmanın temel amacı, Adélie pengueninin doğrulanmış yuva sayımlarına dayalı koloni bulunuşunu modellemek ve bu modelin Marguerite Körfezi'ne aktarılabilirliğini değerlendirmektir. Koloni bulunuşu, bir çevresel hücrede 2000-2025 arasında en az bir pozitif yuva sayımının bulunması olarak tanımlanır. Bu hedef koloni büyüklüğü, her yıl kesintisiz işgal, civciv sağkalımı veya denizde beslenme dağılımı değildir.

Çalışma şu soruları sınar: Çevresel değişkenler, yalnız coğrafi yakınlığa dayalı bir referanstan daha fazla ayırt edici bilgi sağlıyor mu? Özellik sınıfı, düzenlileştirme ve arka plan tasarımı değiştirilince günümüz ve gelecek çıktıları ne kadar değişiyor? SSP2-4.5 altında 2041-2060 aktarımında görülen değişimler hangi hücrelerde yeni çevresel koşullara veya clamping işlemine bağımlı kalıyor?

Amaç belirli bir kayıp yüzdesini yeniden üretmek veya daha yüksek AUC elde etmek değildir. Aktarılabilirlik gösterilemezse bu durum ana sonuç olarak raporlanacak; geleceğe ilişkin çıktılar doğrulanmış habitat değişimi olarak sunulmayacaktır.

# Giriş

Adélie pengueninin üreme alanı ile beslenme ortamı farklı ölçüm süreçleri gerektirir. Koloniler karasal yuvalama alanlarında bulunurken bireyler çevredeki denizel koşullardan da yararlanır. Gallagher vd. (2025), Batı Antarktika Yarımadası'nda bu iki ortamı birlikte ele almış; MAPPPD koloni kayıtları, karasal özellikler ve denizel değişkenlerle lojistik regresyon modelleri kurmuştur. Bu yaklaşım, genel gözlem koordinatlarını doğrudan koloni varlığı saymamak için gerekçe oluşturmaktadır.

Deniz buzu ile ilişkiler mevsime, konuma ve incelenen yaşam evresine göre değerlendirilmelidir. Yıllık ortalama buzdan elde edilen tek bir tepki eğrisi, üreme dönemindeki denize erişimi veya kış koşullarını tek başına açıklamaz. Bir modelin yüksek puanı da kril bolluğunu, üreme başarısını veya bir alanın bütün biyolojik gereksinimleri karşıladığını göstermez. Bu araştırmada bu süreçler doğrudan ölçülmediği için bunlara ilişkin nedensel sonuç çıkarılmamaktadır.

Tür dağılım modellerinde varlık kayıtları, kullanılan arka planın çevresel dağılımına göre değerlendirilir (Phillips vd., 2006; Elith vd., 2011). Arka plan gerçek yokluk değildir. Aynı hücrede yinelenen kayıtları azaltmak, gözlem yapılmayan alanları temsil eder hâle getirmez. Ayrıca mekânsal yakınlık rastgele bölmelerde değerlendirmeyi iyimserleştirebilir; coğrafi referanslar ve yapılandırılmış çapraz doğrulama bu nedenle gereklidir (Hijmans, 2012; Roberts vd., 2017).

Cimino vd. (2016) Adélie penguenlerinin iklim değişimine bölgesel olarak farklı yanıt verebileceğini modellemiştir. Wang vd. (2026) ise OBIS kayıtlarıyla 2010-2020 ve SSP5-8.5 altında 2090-2100 dönemlerini incelemiştir. Bu çalışmalar, burada hedeflenen yerel SSP2-4.5 ve 2041-2060 analizi için bağlam sağlar; farklı kayıt hedefleri, dönemler ve ölçekler nedeniyle yerel sonuçların bağımsız doğrulaması sayılmaz.

Gallagher vd. (2025) 500 m karasal hücrelerle çalışırken burada çevresel analiz 0,25° ızgaraya dayanmaktadır. ERA5'in yaklaşık 31 km yerel yatay çözünürlüğü, daha sık bir çıktı ızgarası kullanılarak koloni ölçeğine indirgenmiş olmaz (Hersbach vd., 2020). Çalışmanın katkısı yüksek çözünürlüklü koloni habitatı iddiası değil; Marguerite odaklı aktarımda veri hedefi, arka plan, model yapısı ve ekstrapolasyonun birlikte denetlenmesidir.

# Yöntem

## Araştırma alanı ve ölçek

Raporlama odağı Marguerite Körfezi ve çevresidir. Özgün çevresel ızgara 37 sütun ve 19 satırdan oluşur; hücre merkezleri 66,00-70,50°G ve 64,00-73,00°B arasındadır. Dış hücre kenarları 65,875-70,625°G ve 63,875-73,125°B'dir. Adelaide Adası körfezin batı/kuzeybatı tarafında ele alınır; yalnızca “kuzeyde” diye tanımlanmaz.

WGS84 üzerinde paralel ve meridyenlerle sınırlı hücrelerin jeodezik alanları ayrı hesaplanmıştır. Tam dikdörtgen 202.681,64 km²'dir; bu değer deniz, kara ve şelf buzu hücrelerini birlikte kapsayan çevresel ızgara alanıdır. Koloni veya kullanılabilir habitat alanı değildir. Hücre alanları enleme göre değişir; yuvarlanmış ortalama alan bütün hücrelerle çarpılarak sonuç üretilmez. EPSG:3031 harita gösterimi ile jeodezik alan hesabı birbirinden ayrılır.

Yeni veri indirme zarfı 60-74°G ve 53-78°B arasındadır. Bu zarf doğu kıyısını da içerir; tek başına Batı Yarımada'ya özgü erişilebilir alan, yani ekolojik M, değildir. Nihai kalibrasyon desteği ve bölgesel kapsam duyarlılığı henüz kesinleştirilmemiştir. Daha geniş alandan eğitim almak yerel aktarımı kendiliğinden geçerli kılmaz.

## Biyolojik kayıtlar ve yeni koloni hedefi

İlk modelde kullanılan GBIF genel bulunuş kayıtlarının indirme DOI'si 10.15468/dl.jt3gt7'dir. Temizlenmiş 704 kaydın 163'ü 2026 yılına aittir. Dolayısıyla eski 67 hücrelik kümenin tamamını 2000-2025 dönemi olarak tanımlamak doğru değildir. Mevcut metadata, kıyıda görülen her bireyin veya karaya düşen her koordinatın üreme kolonisi olduğunu doğrulamamaktadır.

Tamamlanan yöntem denetimi için kayıtlar 2000-2025 ile sınırlandırılmış, hücre başına temsilci yeniden seçilmiş ve aday kıyı desteğinde 61 varlık hücresi kullanılmıştır. Bu küme genel bulunuş denetimine aittir; yeni koloni örneklemi değildir. Hücre başına tek kayıt bırakılması istatistiksel bağımsızlığı veya Rothera çevresindeki gözlem yanlılığının giderildiğini kanıtlamaz.

Yeni koloni verisi Oceanites MAPPPD v5.0'ın tarihli CSV görüntüsünden hazırlanır. Yalnızca yıl alanı 2000-2025 olan, sayım türü “nests” ve sayım değeri sıfırdan büyük kayıtlar kabul edilir. Tekrarlanan sayımlar koloni büyüklüğü modeli kurmak için kullanılmaz; çevresel hücre başına bir temsilci bırakılır. Yerleşim kimlikleri, sayım yılı ve kaynak satırları saklanır. MAPPPD sayım yılı ile iki takvim yılına yayılabilen üreme sezonu aynı kavram değildir (Oceanites, 2026).

Yerel envanter 45 uygun sayım, 19 yerleşim ve 14 farklı çevresel hücre vermiştir. Bu nedenle eğitim alanının genişletilmesi onaylanmıştır. Geniş alanın yalnız kaya/şelf ön kontrolünde 85 Adélie yerleşimi 51 hücreye düşmektedir. Deniz verisine uzaklık filtresi ve son kapsam kontrolü tamamlanmadığından 51 nihai eğitim sayısı olarak kullanılmaz. GBIF deniz gözlemleri bu koloni modeline eklenmeyecektir.

## Çevresel veriler ve tamamlanma durumu

Kaya yüzdesi SCAR Antarctic Digital Database v7.11 kaya poligonlarının eşit alanlı projeksiyonda hücrelerle kesişiminden hesaplanır. Kıyı ve şelf sınıfları aynı sürümün kıyı poligonlarından alınır (Skachkova vd., 2025; Gerrish vd., 2025). Bu çalışmada REMA yükseklik modeli kullanılarak kaya üretilmemiştir; yükseklik, eğim ve bakı değişkenleri de modele eklenmiş değildir.

Tablo 1. Değişkenlerin bu sürümdeki kullanımı

| Değişken | Kaynak ve birim | Kullanım |
|---|---|---|
| Kaya yüzdesi | SCAR ADD v7.11, hücre alanının yüzdesi | Kayalık kıyı desteği ve koloni aday seti; gelecek için sabit |
| Üreme dönemi deniz buzu | ERA5, Kasım-Mart aylık ortalamalarının ortalaması, % | Yerelde üretildi; geniş alan girdisi bekleniyor |
| Kış deniz buzu | ERA5, Haziran-Ağustos aylık ortalamalarının ortalaması, % | Yerelde üretildi; geniş alan girdisi bekleniyor |
| Üreme dönemi SST | ERA5, Kasım-Mart ortalaması, °C | Fiziksel kalite kontrolü çözülmedi; yalnız duyarlılık adayı |
| BIO18 | ERA5, en sıcak ardışık üç ayın toplam yağışı, mm | Eski genel bulunuş denetiminde; ana koloni setinde yok |

Aylık kaynaklarda SST Kelvin'den °C'ye, deniz buzu 0-1 ölçeğinden yüzdeye çevrilir. Normaller her takvim ayı için 2000-2025 ortalamasından oluşturulur; mevsimsel göstergelerde aylara eşit ağırlık verilir. BIO18 her hücrenin en sıcak ardışık üç ayına göre hesaplanır; zorunlu olarak Aralık-Şubat değildir. Toplam yağışın kar/yağmur fazını ve olay şiddetini ayırmaması nedeniyle bu değişkenden civciv hipotermisi çıkarımı yapılmaz.

Deniz değişkenleri karasal hücrelerde tanımsız olabildiğinden en yakın geçerli deniz hücresi küre üzerinde belirlenir ve uzaklığı kaydedilir. Koloni tasarımında 50 km'yi aşan deniz verisi aktarımı dışlama ölçütüdür; 50 km ekolojik olarak doğrulanmış bir beslenme yarıçapı değildir. Bu doldurma işlemi yeni kıyısal iklim bilgisi üretmez.

Günlük 00 UTC buz örnekleri için ayrı veri isteği beklemektedir. Buz ilerleme/çekilme günü ve buzsuz süre henüz üretilmiş bulgu olarak sunulmaz. Aylık veriden kesin gün çıkarılmayacak; günlük veri geldiğinde %15 buz ve beş ardışık gün kuralı gibi operasyonel tanımlar ve sansürlenen olaylar ayrıca açıklanacaktır. Batimetri, kıyıya uzaklık, klorofil/kril ve koloni ölçeğinde topoğrafya henüz bu modele dahil değildir.

## Arka plan ve gözlem yanlılığı

Tamamlanan genel bulunuş denetiminde 579 hücrelik aday kıyı desteği kullanılmıştır. Varlık hücreleri bu arka planda tutulmuştur. Bu, önceki 703 hücrelik dikdörtgenden varlıkları çıkarıp kalan 636 hücreyi kullanma yaklaşımından farklı bir deneydir; iki deneyin sayıları karıştırılmaz.

Yeni koloni modelinde iki arka plan tasarımı karşılaştırılacaktır. İlk tasarım kaya bulunan, şelf buzu oranı %50'nin altında ve geçerli deniz verisi uzaklığı en çok 50 km olan hücrelerdir. İkinci tasarım aynı destek içinde herhangi bir *Pygoscelis* türünün pozitif yuva sayımı bulunan hücrelerden oluşur; Adélie hücreleri de korunur. Bunlar gerçek yokluk değil, farklı kullanılabilirlik ve gözlenme varsayımlarıdır.

Kaya/şelf ön kontrolünde 957 aday kıyı hücresi ve 111 hedef-grup hücresi bulunmaktadır; bir Adélie yerleşimi bu ön filtreye takılmaktadır. Dışlamalar kaynak kimliğiyle kaydedilir. Hedef-grup tasarımı da bütün gözlem yanlılığını ortadan kaldırmış kabul edilmeyecek; aynı örneklem üzerindeki sonuç değişimi raporlanacaktır.

## MaxEnt ayarları ve model seçimi

Özgün MaxEnt 3.4.4 HTML kayıtlarında kullanılan özellikler “hinge linear quadratic”, yani LQH'dir. Eşik özelliği T doğrulanmamıştır. Bu nedenle eski rapordaki AUTO=LQTH etiketi düzeltilmiştir. Yeni denetimde otomatik seçime dayanmak yerine L/RM1, LQ/RM1, LQ/RM2, LQH/RM1 ve LQH/RM2 açıkça tanımlanmıştır.

L yalnızca doğrusal özellikler içerir; Cloglog dönüşümü nedeniyle çıktı puanı bir doğru olmak zorunda değildir. Bir değişkene ait tek tepede optimumu temsil kapasitesi sınırlı olsa da bu özellik L modelini otomatik olarak biyolojik açıdan geçersiz yapmaz. LQ veya LQH'nin daha esnek olması da öğrenilen eğrinin gerçek tolerans ilişkisi olduğunu kanıtlamaz (Elith vd., 2011).

Denetimde iki değişken seti kullanılmıştır: yıllık set BIO18, yıllık buz, kaya ve yıllık SST; SST'siz mevsimsel set BIO18, üreme dönemi buzu ve kayadır. İkinci set yeni koloni ana setiyle aynı değildir. Koloni için hazırlanan ana aday seti kaya, üreme dönemi buzu ve kış buzudur; SST içeren set ayrı duyarlılık adayıdır. Hiçbir koloni ayarı henüz nihai model seçilmemiştir.

Tam genel bulunuş eğitimleri için ham yoğunluğun aynı destek üzerinde normalize edildiği ve sıfır olmayan özellik katsayılarının parametre sayısı kabul edildiği AICc hesapları üretilmiştir. Örneklem parametre sayısına yetmezse AICc geçersiz bırakılır. Bu hesap ENMeval çalıştırılması değildir; yalnız RM1/RM2 adaylarıyla yapılan duyarlılık taraması küresel hiperparametre optimumunu göstermez. AICc, dış doğrulamanın yerine kullanılmaz.

## Mekânsal doğrulama ve değerlendirme

Tamamlanan 61 hücrelik genel bulunuş denetiminde dört katlı enlem bantları, boylam bantları ve 40/80 km'lik iki farklı başlangıç kaydırmalı checkerboard şemaları kullanılmıştır. İki değişken seti, beş aday ve altı şema toplam 240 eğitim verir. Test bölgesinin arka planı da eğitimden çıkarılır; değerlendirme yalnız o bölgenin varlık ve arka plan hücrelerinde yapılır.

İki coğrafi referans aynı bölmelerde değerlendirilmiştir: en yakın eğitim varlığına uzaklığın negatifi ve yalnız koordinatlarla eğitilen düzenlileştirilmiş lojistik referans. Uzaklık referansı çevresel modelin coğrafi yakınlığın ötesinde bilgi sağlama iddiasını sınar; rastgele tahminle özdeş değildir (Hijmans, 2012).

AUC, eğitim varlık puanlarının 10. yüzdeliğine göre test omission oranı, sabit on kutulu Boyce ve duyarlılığın en az 0,95 olduğu ROC bölümüne ait tanımı açık oran hesaplanmıştır. Son iki ölçüt küçük test örneklemleriyle kararsız olabilir; kullanılan sabit kutulu Boyce, sürekli kayan pencereli bir Boyce uygulaması diye sunulmaz.

Aynı şema içindeki dört katın eşlenik yeniden örneklemesiyle aralıklar hesaplanmıştır. Bunlar bağımsız veri tekrarlarından elde edilen genel güven aralıkları değildir; farklı şemalar da aynı kayıtları yeniden kullanır. Adaylar bu test sonuçlarına bakılarak seçilmediğinden testteki en yüksek puan “nihai kazanan” ilan edilmemiştir (Roberts vd., 2017).

## CMIP6 aktarımı ve belirsizlik tasarımı

CMIP6 kapsamındaki IPSL-CM6A-LR, GFDL-ESM4 ve MPI-ESM1-2-LR kaynaklarıyla SSP2-4.5 için 2041-2060 aylık girdileri hazırlanmıştır. Referans 2000-2025, historical 2000-2014 ile aynı model/üye SSP2-4.5 devamı 2015-2025 birleştirilerek oluşturulmuştur. Böylece 2014 sonrası aylar historical diye etiketlenmez. Bu referans saf tarihsel deney değildir (Eyring vd., 2016).

Denizel değişkenlerde her ayın gelecek-referans farkı ERA5 normaline eklenir; buz değeri ardından %0-100 ile sınırlandırılır. Kaynak kıyı maskelerini koruyan en yakın tam yerel GCM hücresi eşlemesi uygulanır. Farklı modellerin yerel ızgaraları tek bir “1°/100 km” çözünürlükle tanımlanmaz. Yeniden örnekleme veya delta yöntemi GCM'de bulunmayan fiyort ölçeği fiziğini üretmez.

Mevcut genel bulunuş modeli için üç GCM'de toplam 30 tam eğitim/aktarım ve 720 kat-dışı gelecek aktarımı tamamlanmıştır. Clamping açık/kapalı farkları, tek değişken grubu değiştirme deneyleri ve tek değişken aralığına dayalı MESS haritaları üretilmiştir. Bu MESS çok değişkenli korelasyon yapısındaki her yeni birleşimi saptamaz. Yalnız buzun değiştirilmesi nedensel bir etki ölçümü değildir; etkileşimler nedeniyle ayrı değişken etkileri toplam deltaya eşit olmak zorunda değildir.

Her GCM için tek üye kullanılmıştır. Üç GCM'nin bulunması üyeler arası iç değişkenliği, model bağımlılıklarını veya yirmi yıllık pencerelerin belirsizliğini çözmez. Bütün adayların aynı yönde sonuç vermesi de ortak veri yanlılıkları nedeniyle tek başına doğruluk kanıtı olmayacaktır. Geniş koloni modelinin üç GCM aktarımı henüz yapılmamıştır.

## Tekrarlanabilirlik

Kod, maske ve ayarlar proje deposunda tutulmaktadır. Genel denetimin betikleri ve 12 Kasım kaynak/paket SHA256 manifestleri mevcuttur; bu sürümdeki yerel değişikliklerin tamamı yayımlanmış bir sürüm veya DOI'li arşiv değildir. Kod testlerinin geçmesi ekolojik doğrulamanın yerine kullanılmaz.

Ek teknik kayıtta, sayısal tablolara karşılık gelen dosyalar, kaynak DOI/URL'leri ve değişiklik listesi verilmiştir. Nihai sürüm öncesi koloni girdileri, dışlamalar, model komutları, kaynak model/üye/ızgara/sürüm bilgileri ve üretim ortamı aynı sürüme sabitlenecektir.

# Bulgular

## Veri hedefi ve kaynak denetimi

MAPPPD yerel pozitif yuva sayımları yalnız 14 çevresel hücreyi desteklemektedir. Bu sayı, genel gözlemlerden türetilen 67 eski veya 61 yeniden seçilmiş hücreyle eşdeğer değildir. Daha fazla genel gözlem, doğrulanmış koloni örnekleminin yerine geçirilemez.

Resmî CDS kaynağının yeniden indirilmesi SST kimliğini paramId 34 ve birimini Kelvin olarak doğrulamıştır. Doldurulmamış yerel yıllık SST'nin minimumu yaklaşık -2,422 °C'dir; altı deniz hücresinde -2 °C altında yıllık değer vardır. Bu nedenle sorun yalnız grafik ekseniyle açıklanamamaktadır. Uç değerlerin fiziksel/işlemsel nedeni henüz çözülmediğinden SST ana koloni aday setine alınmamış; duyarlılık adayı olarak işaretlenmiştir. Kaynak türü doğrulanmış olması fiziksel kalite kontrolünün tamamlandığı anlamına gelmez.

## Gerçek VIF değerleri

Tablo 2. Eski yıllık değişken setinin farklı arka plan desteklerindeki VIF değerleri

| Değişken | Tam dikdörtgen 703 hücre | Aday kıyı 579 hücre | Deniz desteği 325 hücre |
|---|---|---|---|
| BIO18 | 1,986 | 2,036 | 1,760 |
| Yıllık buz | 2,521 | 2,801 | 5,637 |
| Kaya | 1,071 | 1,160 | 1,235 |
| Yıllık SST | 1,556 | 2,012 | 5,246 |

Buz ve SST'nin VIF değerleri deniz desteğinde 5'i aşmaktadır. Dolayısıyla “tüm değişkenler VIF<5 koşulunu sağlıyor” ifadesi destek alanından bağımsız kullanılamaz. Bu tablo eski yıllık setin denetimidir; yeni koloni setinin VIF'i değildir. Kat bazlı VIF tabloları da ayrıca üretilmiştir.

## Coğrafi referanslarla karşılaştırma

Tablo 3. Yıllık genel bulunuş setinde dört test katının ortalama AUC değerleri

| Bölme şeması | L/RM1 | LQ/RM1 | LQ/RM2 | LQH/RM1 | LQH/RM2 | Uzaklık |
|---|---|---|---|---|---|---|
| Enlem bantları | 0,488 | 0,479 | 0,492 | 0,602 | 0,600 | 0,751 |
| Boylam bantları | 0,650 | 0,656 | 0,653 | 0,712 | 0,702 | 0,772 |
| Checkerboard 40 km | 0,725 | 0,760 | 0,727 | 0,797 | 0,783 | 0,856 |
| Checkerboard 40 km kaydırılmış | 0,730 | 0,763 | 0,737 | 0,775 | 0,772 | 0,852 |
| Checkerboard 80 km | 0,729 | 0,769 | 0,735 | 0,758 | 0,768 | 0,828 |
| Checkerboard 80 km kaydırılmış | 0,670 | 0,729 | 0,692 | 0,744 | 0,741 | 0,839 |

AUC bölme şemasına belirgin biçimde bağlıdır. Örneğin enlem şemasında L/RM1 için katlar arası standart sapma 0,180, LQ/RM1 için 0,240'tır. Bu tabloda tek bir en yüksek ortalamayı seçmek modelin aktarılabilirliğini kanıtlamaz. Her iki değişken setinde de bütün çevresel adayların şema bazındaki ortalama AUC'si uzaklık referansının altında kalmıştır (Şekil 1).

![Şekil 1 Çevresel modellerin ve coğrafi referansların test AUC karşılaştırması](/home/halil/adelie-maxent-2204c/maxent/cikti/revizyon_20261112/figures/spatial_null_comparison.png)

Şekil 1. Tamamlanan 61 hücrelik genel bulunuş denetiminde çevresel adayların, koordinat referansının ve uzaklık referansının ortalama test AUC değerleri. Hücrelerdeki sayılar AUC'dir; AUC farkı değildir. Şemalar bağımsız veri tekrarları değildir. Bu şekil yeni koloni modelinin sonucu değildir.

Bu sonuç bütün olası koloni modellerinin başarısız olduğunu göstermez. Mevcut kayıt hedefi, aday değişkenler ve değerlendirme tasarımı altında çevresel değişkenlerle coğrafi referansın ötesinde aktarılabilirlik gösterilemediğini belirtir. Eski 67 hücreli enlem testindeki L/RM1=0,580 ve AUTO=0,477 değerleri farklı bir deneydir; yeni tablonun satırları veya koloni doğrulaması olarak kullanılamaz.

## Eski Jackknife ve tepki eğrilerinin düzeltilmiş yorumu

![Şekil 2 Eski genel bulunuş modelinin Jackknife grafiği](/home/halil/adelie-maxent-2204c/maxent/cikti/deneme3/plots/Pygoscelis_adeliae_jacknife.png)

Şekil 2. Eski genel bulunuş modeli için Jackknife eğitim kazancı. Grafiğin kendi lejantında mavi tek değişkenle eğitim, turkuaz değişken çıkarılarak eğitim, kırmızı bütün değişkenlerle eğitimdir. Turkuaz çubuk doğrudan “kazanç kaybı” değil, değişken çıkarıldığında kalan kazançtır. Bu eski grafik yeni koloni değişken önemini göstermez.

BIO18'in tek başına daha yüksek eğitim kazancı vermesi doğrudan yağış mekanizmasını veya nedensel üstünlüğünü kanıtlamaz; coğrafi vekillik olasılığı dışlanmamıştır. Kaya sıfırken model puanının sıfırlanmaması da belirli bir mekanizmayla açıklanmış değildir. Genel kayıt hedefi, ölçek ve özellik yapısı birlikte etkili olabilir.

Eski buz eğrisinin yaklaşık %20 alt sınırında yüksek olması, %20-25'in türün evrensel optimumu olduğunu göstermez. %20 altındaki yanıt gözlenmemiştir; üst uçtaki yeniden yükseliş ve belirsizlik de çan eğrisi iddiasını desteklemez. L modeline geçmek bu ekstrapolasyon sorununu kendiliğinden çözmez. Model puanlarından açık denizde yaşayamama, kesin dalış sınırı veya %80 buzda biyolojik imkânsızlık sonucu çıkarılmamaktadır.

## Üç GCM ve model yapısı duyarlılığı

Tablo 4. Yıllık genel bulunuş setinde 61 varlık hücresinin ortalama gelecek eksi günümüz puanı

| MaxEnt ayarı | IPSL-CM6A-LR | GFDL-ESM4 | MPI-ESM1-2-LR |
|---|---|---|---|
| L/RM1 | +0,115 | +0,053 | +0,033 |
| LQ/RM1 | -0,174 | -0,029 | +0,003 |
| LQ/RM2 | +0,007 | +0,021 | +0,019 |
| LQH/RM1 | -0,318 | -0,089 | -0,004 |
| LQH/RM2 | -0,137 | -0,021 | +0,006 |

Tablo 4 tam eğitimde kullanılan varlık hücrelerindeki, clamping açık, Cloglog puanı farklarını gösterir. Değerler yüzde değildir; eğitim örneklemi üzerinde hesaplandığı için bağımsız test başarısı da değildir. Yeni koloni modelinin veya koloni nüfusunun değişimini ifade etmez. Aynı IPSL girdisinde L/RM1 artış, LQH/RM1 azalış üretmektedir. Bu fark model bağımlılığıdır; habitatın hangi yönde değiştiğini belirlemez.

Tablo 5. Yerel deniz hücrelerinde GCM referans buzu ile ERA5 aylık buzu arasındaki ön karşılaştırma

| GCM | Ortalama sapma yüzde puanı | RMSE yüzde puanı |
|---|---|---|
| IPSL-CM6A-LR | +10,14 | 22,05 |
| GFDL-ESM4 | +27,89 | 35,39 |
| MPI-ESM1-2-LR | -12,51 | 21,25 |

Tablo 5, 339 yerel ERA5 deniz hücresinde eşlenmiş aylık klimatolojilerin eşit hücre ağırlıklı karşılaştırmasıdır. Bütün Bellingshausen Denizi'nin başarım testi veya bağımsız yerinde gözlem doğrulaması değildir. Modellerin buza ilişkin bölgesel farkları bulunduğunu gösterir; tek başına GCM eleme/ağırlıklandırma ölçütü yapılmamıştır. İnterannual değişkenlik ve farklı gözlemsel buz ürünleriyle karşılaştırma henüz tamamlanmamıştır.

## Eski haritaların denetimi ve bekleyen sonuçlar

Eski tek-GCM değişim haritasındaki 243 artış hücresinin 59'u eğitim değişkenlerinin aralığı dışındadır; artış hücrelerinin 22'sinde eğitilmiş katların fark yönleri uyuşmamaktadır. Kuzeyde 66,00-66,50°G arasındaki bağlantılı artış bileşenlerinde bulunan 24 hücrenin tamamı yeni çevresel aralıktadır. Bu nedenle kuzey artış bloğu belirsizlikten bağımsız bir kazanım alanı olarak yorumlanamaz.

Eski belirsizlik haritasındaki toplam 246 hücrelik yön uyuşmazlığı, eşlenik eğitilmiş model katlarının gelecek-günümüz farkına aittir. Bu, farklı iklim değişkenlerinin veya GCM'lerin birbirine zıt yön verdiği anlamına gelmez. MESS ile saptanan aralık dışılık ve fiilen uygulanan clamping büyüklüğü de aynı ölçü değildir.

Önceki değişim sınıfları belirli model/maske ve seçilmiş delta eşiğinin hücre sayımıdır. Bunlardan doğrulanmış habitat kaybı yüzdesi üretilmemektedir; eski haritalar yeni koloni haritası olarak sunulmaz. ±0,05 fark sınıfı biyolojik olarak doğrulanmış eşik değildir. İkili bulunuş eşiği seçimi, iki sürekli model puanının farkına aynı biyolojik anlamı kazandırmaz.

**Tamamlanması beklenen sonuçlar:** Geniş alan koloni örnekleminin son dışlama dökümü; iki arka planın koloni modelleri üzerindeki karşılaştırması; koloniye ait mekânsal metrikler ve belirsizlik aralıkları; günlük buz fenolojisi; üç GCM'de koloni günümüz/gelecek/delta ve MESS-clamping haritaları; Marguerite'deki doğrulanmış varlık hücrelerinde kat-dışı ortalama delta. Bu sonuçların hiçbiri tamamlanmış gibi yazılmamıştır.

# Sonuç ve Tartışma

Tamamlanan genel bulunuş denetimi, çevresel model puanlarının coğrafi referanslara ve model yapısına göre değerlendirilmeden habitat değişimi olarak yorumlanamayacağını göstermiştir. Mevcut tasarımda coğrafi referansı aşan aktarılabilirlik ortaya konmamış; gelecekteki ortalama puan farkının işareti dahi ayarlara bağlı kalmıştır. Bu nedenle tek bir haritadan kesin kayıp oranı veya korunacak sığınak belirlenmemektedir.

Doğrulanmış koloni bulunuşuna geçilmesi eski modelin yalnızca adını değiştirmek değildir. Farklı kayıt hedefi, arka plan, değişken seti ve yeniden doğrulama gerektirir. Yerelde 14 hücre bulunması eğitimin genişletilmesine gerekçe olmuştur; genişletme de örnekleme yanlılığını veya yerel aktarım sorununu otomatik çözmez. Yeni koloni sonuçları görülmeden bu tasarımın başarılı olduğu ileri sürülemez.

Esneklik ile aktarılabilirlik arasında genel bir ödünleşim bulunabilse de mevcut birkaç ortalama puan, LQH'nin “biyolojik olarak doğru”, L'nin “biyolojik olarak imkânsız” olduğunu kanıtlamaz. Zayıf bir testi yalnız “keşifsel” etiketiyle açıklamak yeterli değildir. Bu çalışmada etiket değişikliği yerine veri hedefi ayrılmış ve tamamlanan karşılaştırmalar açıkça raporlanmıştır.

Türün buzla ve denizel besin ağıyla ilişkisini araştıran literatür, bu modellerin ekolojik bağlamını sağlar. Ancak kril, yağış fazı, koloni topografyası ve demografik yanıt ölçülmediğinden aynı mekanizmaların burada gösterildiği iddia edilmemektedir. Modelin yüksek puanı Adelaide kıyıları veya iç fiyortların bütün gereksinimleri karşıladığının kanıtı değildir.

Bu aşamanın sonucu yöntemsel güvenilirlikle sınırlıdır. Geniş koloni modeli ve yerel aktarım testleri tamamlandıktan sonra ekolojik sonuç bölümü güncellenecektir. Benzerlik yalnız ortak yanlılıklardan, farklılık ise doğrulanmamış model seçiminden kaynaklanabileceği için, model uzlaşması veya ayrışması tek başına ekolojik kanıt sayılmayacaktır.

# Öneriler

Öncelik, belirli bir bölgeyi sığınak veya kayıp alanı ilan etmek değil, kayıt türü ile model hedefinin tutarlılığını ve Marguerite'ye aktarımı sınamaktır. Bunun için dışlanan koloni kayıtları, deniz hücresinden aktarım uzaklıkları ve farklı arka planların etkisi gözden geçirilmelidir.

Saha doğrulaması yapılabilirse yüksek ve düşük model puanları ile yüksek belirsizlik alanlarını birlikte kapsayan bir tasarım tercih edilmelidir. Bir bölgeye özgü doğrulanmamış harita nedeniyle George VI çevresine tek başına öncelik verilmez. Koloni sayımları ile denizdeki hareket/telemetri verileri ayrı araştırma hedefleri olarak tutulmalıdır.

Kril avcılığı kotası, deniz koruma alanı sınırı veya koloni kaybı kararı bu analizden türetilmemektedir. Böyle uygulamalar için bağımsız biyolojik ve yönetim verileri gerekir. Daha ince kıyısal/topografik veriler ileride kullanılabilir; fakat yalnız ızgarayı küçültmek çevresel çözünürlüğü artırmaz.

Nihai sonuçta farklı özellik ve RM ayarları, arka plan tasarımları ve GCM'lerin yayılımı gösterilmelidir. Birbirine yakın puanlar ortak yanlılıkları dışlamadıkça güven kanıtı olarak sunulmamalı; aktarılabilirlik başarısızsa 2050 çıktıları hipotez üretimi sınırında tutulmalıdır.

# Kaynaklar

Cimino, M. A., Lynch, H. J., Saba, V. S., & Oliver, M. J. (2016). Projected asymmetric response of Adélie penguins to Antarctic climate change. *Scientific Reports*, 6, 28785. https://doi.org/10.1038/srep28785

Copernicus Climate Change Service. (2019). *ERA5 monthly averaged data on single levels from 1940 to present*. Climate Data Store. https://doi.org/10.24381/cds.f17050d7

Copernicus Climate Change Service. (2018). *ERA5 hourly data on single levels from 1940 to present*. Climate Data Store. https://doi.org/10.24381/cds.adbb2d47

Elith, J., Phillips, S. J., Hastie, T., Dudík, M., Chee, Y. E., & Yates, C. J. (2011). A statistical explanation of MaxEnt for ecologists. *Diversity and Distributions*, 17, 43-57. https://doi.org/10.1111/j.1472-4642.2010.00725.x

Eyring, V., Bony, S., Meehl, G. A., Senior, C. A., Stevens, B., Stouffer, R. J., & Taylor, K. E. (2016). Overview of the Coupled Model Intercomparison Project Phase 6 experimental design and organization. *Geoscientific Model Development*, 9, 1937-1958. https://doi.org/10.5194/gmd-9-1937-2016

Gallagher, K. L., Herman, R., Walton, K., Dinniman, M. S., & Lynch, H. J. (2025). Pygoscelis penguins prefer different oceanographic and terrestrial habitats during the austral summer. *Ecosphere*, 16, e70091. https://doi.org/10.1002/ecs2.70091

GBIF.org User. (2026). *Occurrence Download*. The Global Biodiversity Information Facility. https://doi.org/10.15468/dl.jt3gt7

Gerrish, L., Ireland, L., Fretwell, P., Cooper, P., & Skachkova, A. (2025). *High resolution vector polygons of the Antarctic coastline*, sürüm 7.11. NERC EDS UK Polar Data Centre. https://doi.org/10.5285/7d6793c2-2513-4752-8f37-11db5b791fb5

Hersbach, H., vd. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society*, 146, 1999-2049. https://doi.org/10.1002/qj.3803

Hijmans, R. J. (2012). Cross-validation of species distribution models: removing spatial sorting bias and calibration with a null model. *Ecology*, 93, 679-688. https://doi.org/10.1890/11-0826.1

Oceanites, Inc. (2026). *MAPPPD census counts of Antarctic and sub-Antarctic breeding penguins*, sürüm 5.0. Erişim 12 Kasım 2026. https://penguinmap.com/mapppd/

Phillips, S. J., Anderson, R. P., & Schapire, R. E. (2006). Maximum entropy modeling of species geographic distributions. *Ecological Modelling*, 190, 231-259. https://doi.org/10.1016/j.ecolmodel.2005.03.026

Roberts, D. R., vd. (2017). Cross-validation strategies for data with spatial, temporal, or phylogenetic structure. *Ecography*, 40, 913-929. https://doi.org/10.1111/ecog.02881

Skachkova, A., Gerrish, L., Fretwell, P., & Cooper, P. (2025). *High resolution vector polygons of Antarctic rock outcrop*, sürüm 7.11. NERC EDS UK Polar Data Centre. https://doi.org/10.5285/815525ca-cefe-4fbf-9224-3ee784e7de4e

Wang, J.-R., Hu, A.-L., & Yang, J. (2026). Impact of climate change on the potentially suitable habitat distribution of Pygoscelis penguins in Antarctica. *Ying Yong Sheng Tai Xue Bao*, 37, 926-932. https://doi.org/10.13287/j.1001-9332.202603.037 PMID 42209243.

