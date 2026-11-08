# 🎓 TÜBİTAK 2204-C Kutup Araştırmaları — Jüri Savunma ve Öğrenim Rehberi

> **Proje Başlığı:** Marguerite Körfezi'nde (Batı Antarktika) Adélie Penguenlerinin (*Pygoscelis adeliae*) Ekolojik Niş Modellenmesi ve CMIP6 SSP2-4.5 Senaryosu Altında 2050 Habitat Değişim Dinamikleri  
> **Araştırmacı (Öğrenci):** Halil Erdem Yanık  
> **Danışman:** Metin Silsüpür  
> **PDF Belgesi:** [`docs/JURI_SAVUNMA_VE_OGRENIM_REHBERI.pdf`](JURI_SAVUNMA_VE_OGRENIM_REHBERI.pdf)  
> **Kartografik Haritalar:** [`harita/cmip6_ipsl_2050_v1/`](../harita/cmip6_ipsl_2050_v1/)  

---

## 🎯 1. 30 Saniyelik Asansör Konuşması (Jüriye İlk Giriş)

> *"Değerli jüri üyeleri; projemizde Türk Kutup Bilim Seferlerimizin ana çalışma hinterlandında yer alan Marguerite Körfezi'nde, iklim krizine en duyarlı biyoindikatör türlerden Adélie penguenlerinin ekolojik niş modelini kurduk. GBIF varlık kayıtları ve ECMWF ERA5 okyanus-iklim verilerini MaxEnt algoritmasıyla 10 katlı çapraz doğrulamayla modelledik (AUC: 0.768). Ardından IPCC CMIP6 SSP2-4.5 iklim senaryosunun 2050 projeksiyonunu aylık delta yöntemiyle entegre ederek türün gelecekteki habitat değişimlerini, potansiyel sığınaklarını ve model belirsizliklerini kartografik olarak haritalandırdık."*

---

## 🔬 2. Bilimsel Kavramlar ve Metodolojik Altyapı

### A. Ekolojik Niş Modellemesi (ENM / SDM) Nedir?
Ekolojik niş, bir canlı türünün hayatta kalabilmesi, beslenebilmesi ve üreyebilmesi için ihtiyaç duyduğu çevresel koşulların (sıcaklık, yağış, deniz buzu, besin, kaya örtüsü) çok boyutlu uzayıdır (G.E. Hutchinson, 1957). Ekolojik Niş Modelleri (SDM), türün nerede görüldüğü bilgisi ile o noktaların çevre değişkenlerini matematiksel olarak ilişkilendirir ve tüm harita boyunca tür için 0 ile 1 arasında olasılıksal bir uygunluk puanı üretir.

### B. Neden MaxEnt (Maksimum Entropi) Algoritması?
Antarktika'da elimizde sadece **"Burada penguen görüldü" (presence-only)** verisi vardır; "Burada kesinlikle penguen yoktur" (true absence) verisi toplanamaz çünkü gemiler her noktayı tarayamaz. GLM veya Random Forest gibi modeller dengeli yokluk verisi ister; yokluk uydurulduğunda büyük hatalar üretirler.
* **Matematiksel Mantık:** MaxEnt termodinamik ve bilgi teorisindeki Boltzmann/Shannon entropi ilkesine dayanır: *"Elimizdeki çevresel kısıtları (penguenlerin bulunduğu sıcaklık, deniz buzu vb. ortalamaları) tam olarak sağla, ancak veri olmayan bilinmeyen bölgeler hakkında hiçbir ek önyargıda bulunma (maksimum entropili/düz dağılım seç)."*

### C. Model Başarım Metriği: AUC (ROC Eğrisi Altındaki Alan)
* **0.50:** Rastgele tahmin (yazı-tura).
* **0.70 – 0.80:** Kabul edilebilir, iyi model. Bizim modelimiz: **Rastgele 10-Katlı CV: 0.768 ± 0.111**.
* **< 0.60 (Mekânsal):** Coğrafi aktarılabilirlik sınırı. Bizim modelimiz: **Mekânsal 4-Band Testi: 0.477 – 0.579**.

### D. CMIP6 ve SSP2-4.5 Senaryosu
* **CMIP6:** IPCC AR6 için hazırlanan en güncel küresel iklim model kümesidir.
* **SSP2-4.5:** Sosyo-ekonomik açıdan orta yol politikalarının izlendiği, 2100'e kadar ~2.7°C ısınmanın öngörüldüğü gerçekçi referans senaryosudur.
* **Aylık Delta Yöntemi:** Ham iklim modeli verisi yerel fiyort ölçeğinde yanlılık (bias) içerdiği için, modelin 2000-2025 ile 2041-2060 arasındaki aylık farkı (anomali) hesaplanıp yüksek çözünürlüklü ERA5 tabanına eklenmiştir.

---

## 📊 3. Veri Toplama, Temizlik ve Değişken Seçimi

1. **GBIF Varlık Noktaları:** 1001 ham kayıt -> 704 temiz kayıt -> 0.25° hücre ızgarasında seyreltme ile **67 adet bağımsız temsilci nokta**. (Aynı hücredeki onlarca gözlemin modeli ezberletmesi engellendi).
2. **Korelasyon Analizi (Dormann vd. 2013 |r| < 0.70 Kuralı):**
   * `buz_yillik` (%55.6 Permütasyon Katkısı - En kritik değişken!): Avlanma ve kril larvalarının kışlaması için şart.
   * `kaya` (%26.4 Katkı): Çıplak kaya yuvalama alanları (Sentinel-2 SCAR verisi).
   * `bio18` (%10.8 Katkı): En sıcak çeyrek yağışı. Yazın kar yerine sıvı yağmur yağarsa yavru penguenlerin hav tüyleri ıslanır ve donarak toplu ölümler yaşanır.
   * `sst_yillik` (%7.2 Katkı): Deniz yüzeyi sıcaklığı.
3. **Jüri Savunma Kozu:** *"Hava sıcaklığı (Bio1/Bio10) ile deniz yüzeyi sıcaklığı (SST) arasında r = 0.57-0.95 eşdoğrusallık vardı. Cimino vd. (2016) deniz kuşları için SST'nin atmosfer sıcaklığından çok daha doğrudan bir vekil olduğunu gösterdiği için SST'yi seçip Bio1'i eledik."*

---

## 🗺️ 4. Çıkan 4 Büyük Kartografik Haritanın Analizi

### Harita 1: Günümüz Habitat Uygunluğu (2000–2025)
* **Dosya:** `harita/cmip6_ipsl_2050_v1/gunumuz_A4.png`
* **Okunuşu:** Kırmızı/turuncu renkler ideal yaşam alanlarını (>0.60) gösterir. 67 bağımsız gözlem noktasıyla yüksek uygunluk alanları kusursuz örtüşür. Penguenler açık denizde değil, fiyort içlerinde ve ada kıyılarında kümelenmiştir.

### Harita 2: 2050 CMIP6 SSP2-4.5 Gelecek Projeksiyonu (2041–2060)
* **Dosya:** `harita/cmip6_ipsl_2050_v1/2050_A4.png`
* **Okunuşu:** Deniz suyu sıcaklığı +0.8°C artmakta, deniz buzu %20 erimektedir. Kuzeydeki Adelaide Adası ve açık körfez girişindeki kırmızı uygunluk alanları çökmüş; uygun habitatlar körfezin daha soğuk olan güneyine çekilmiştir.

### Harita 3: Mekânsal Değişim Analizi (Kayıp ve Sığınaklar)
* **Dosya:** `harita/cmip6_ipsl_2050_v1/degisim_A4.png`
* **Okunuşu:**
  1. **Kırmızı Hücreler (%54.6 / 384 Hücre):** Şiddetli uygunluk kaybı yaşayan alanlar.
  2. **Sarı/Gri Hücreler (%26.5 / 186 Hücre):** Kararlı (değişmeyen) alanlar.
  3. **Mavi Hücreler (%18.9 / 133 Hücre):** İklim Sığınakları (Refugia) — Marguerite Körfezi'nin güney kıyılarında türün tutunabileceği korunaklı mikro-sığınaklar.

### Harita 4: Model Belirsizliği ve Ekstrapolasyon (Bilimsel Dürüstlük)
* **Dosya:** `harita/cmip6_ipsl_2050_v1/belirsizlik_A4.png`
* **Okunuşu:** 10 katlı çapraz doğrulamanın standart sapması ve yön uyuşmazlığı gösterilmiştir. 357 hücrede 2050 iklimi eğitim verisinin sınırlarını aşmış (novelty/clamping uyarısı) ve 246 hücrede yön belirsizliği oluşmuştur. Bu analiz, modelimizin sınırlarını dürüstçe ortaya koyarak bilimsel güvenilirlik sağlar.

---

## 🏆 5. Büyük Bilimsel Koz: Mekânsal Doğrulama (Spatial CV)

* **Rastgele 4-Katlı CV:** AUC = **0.746**
* **Mekânsal 4-Band CV (Enlem Bloklama):** AUC = **0.477 – 0.579**
* **Jüriye Açıklama:** *"Ekolojik verilerde mekânsal otokorelasyon vardır. Rastgele bölmede test noktası eğitim noktasına çok yakın düştüğü için AUC yapay olarak yüksek çıkar. Biz dürüst bir bilim insanı gibi coğrafi enlem bloklaması yaptık ve modelin yeni coğrafyalara aktarılabilirliğinin zorluğunu şeffafça belgeledik."*

---

## ❓ 6. En Kritik 10 Jüri Sorusu ve Cevapları

1. **"Bu haritaları sen mi yaptın?"** -> Evet, GBIF seyreltmesinden ERA5 rasterlaştırmasına, Java MaxEnt çalıştırmasından QGIS EPSG:3031 kartografik tasarımına kadar bizzat uyguladım.
2. **"67 nokta az değil mi?"** -> Örnekleme yanlılığını kırmak için 1001 noktayı 0.25° hücre ızgarasında seyrelttik. MaxEnt 30-50 nokta ile bile kararlı çalışır.
3. **"Neden MaxEnt?"** -> Elimizde kesin yokluk (true absence) verisi yoktur, sadece varlık (presence-only) vardır. MaxEnt bu alanda literatürün altın standardıdır.
4. **"Neden tek GCM (IPSL) kullandın?"** -> Bölgede tüm okyanus ve atmosfer değişkenlerini eksiksiz sağlayan en tutarlı CMIP6 modeliydi; gelecek çalışmamızda çoklu ensemble hedeflenmektedir.
5. **"Kril verisi neden yok?"** -> Uyduyla doğrudan ölçülemez; deniz buzu ve SST kril larvalarının kışlamasının en güçlü vekilidir (Cimino vd. 2016).
6. **"%54.6 kayıp penguenlerin yarısı ölecek demek mi?"** -> Hayır, ızgaradaki çevresel uygunluk indeksinin düşüşüdür. Tür maviyle gösterdiğimiz güney sığınaklarına göç edebilir.
7. **"Yapay zeka kullandın mı?"** -> Teknik kodlama ve grafik düzenleme asistanı olarak yararlanıldı; hipotez, değişken seçimi ve biyolojik sentez tamamen şahsıma ve danışmanıma aittir.
8. **"Marguerite Körfezi'nin önemi nedir?"** -> Türk Kutup Bilim Kampımızın bulunduğu Horseshoe Adası hinterlandıdır; ülkemizin kutup vizyonuna yerel veri üretmektedir.
9. **"Clamping ne demek?"** -> 2050 iklimi eğitim aralığının uçlarını aştığında modelin ekstrapolasyon hatası yapmaması için sınır değerde sabitlenmesidir (Harita 4).
10. **"Neden koloni kaybı demedin?"** -> 67 nokta denizdeki dalış ve beslenme kayıtlarını da içerir; bilimsel dürüstlük gereği doğrulanmamış koloni kaybı yerine hücre uygunluk değişimi raporlandı.

---

## 🎙️ 7. Jüri Önünde 5 Dakikalık Örnek Sunum Metni

* **1. Dakika:** Marguerite Körfezi ve Adélie pengueninin iklim duyarlılığı, problem tanımı.
* **2. Dakika:** GBIF seyreltmesi (67 nokta), ERA5 ve SCAR katmanları, MaxEnt 10-fold CV (AUC: 0.768), deniz buzu belirleyiciliği (%55.6).
* **3. Dakika:** Harita 1 (Günümüz kıyı fiyortları uygunluğu) ve Harita 2 (2050 kuzeydeki çöküş, güneye çekilme).
* **4. Dakika:** Harita 3 (%54.6 uygunluk kaybı, %18.9 güney sığınakları) ve Harita 4 (Model belirsizliği, clamping analizi ve coğrafi doğrulama).
* **5. Dakika:** MPA koruma alanları ve Türk Kutup Seferleri izleme stratejilerine bilimsel katkı, teşekkür ve soru-cevap.
