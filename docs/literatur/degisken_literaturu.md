# Değişken seçimi için literatür özeti

*Hazırlanma: 2026-10-20 · Amaç: Aşama 5'te (değişken seçimi) öğrenci ve danışmana gerekçe sunmak.*
*Bu belge değişken SEÇMEZ; seçim öğrenci + danışmanındır.*

**Doğrulama kuralı:** Aşağıdaki her kaynağın künyesi DOI kayıt sisteminden (doi.org / Crossref) 2026-10-20'de kontrol edildi.
Yalnızca özetini okuyabildiğimiz kaynaklar ayrıca belirtildi.

> **Not — elenen kaynaklar:** Tarama, RULES.md gereği Gemini worker sistemiyle (hk_agents, 15 worker) paralel yapıldı.
> Gemini'nin önerdiği 9 DOI'nin 4'ü yanlış ya da uydurma çıktı (biri bulunamadı, biri ilgisiz bir dergi sayısına,
> biri Meksika Körfezi petrol sızıntısı makalesine gidiyordu); kaynak göstermeden verdiği sayısal eşikler
> (ör. "deniz buzu optimumu %15–30") de doğrulanamadı. Bu belgede Gemini çıktısından **doğrulanmamış hiçbir bilgi kullanılmadı**.

---

## 1. En yakın çalışma: Cimino vd. (2016) — Adélie için MaxEnt

Cimino, M. A., Lynch, H. J., Saba, V. S. & Oliver, M. J. (2016). Projected asymmetric response of Adélie penguins
to Antarctic climate change. *Scientific Reports* 6:28785. https://doi.org/10.1038/srep28785 *(tam metin okundu)*

- **Yöntem:** MaxEnt ve GAM; yavru büyütme dönemi habitat uygunluğu ("chick-rearing habitat suitability").
- **Değişkenler (yalnızca 3):** deniz yüzeyi sıcaklığı (SST), deniz buzu yoğunluğu (SIC), buzsuz kaya (bare rock).
  SST ve SIC **yaz (Aralık–Şubat)** ortalamaları; kolonilerin **25 km** çevresinden (beslenme alanı) alınmış.
- **Gerekçe:** "Atmosferik (hava sıcaklığı, rüzgâr, deniz seviyesi basıncı) ve okyanusal koşullar arasındaki yüksek
  kovaryans, SST ve SIC'nin hem karadaki yuvalama habitatının kalitesi hem de besin kaynakları için iyi
  vekil olabileceğini düşündürüyor" (makaleden çeviri).
- **Sonuç:** Tüm modellerde AUC > 0.85; SST, SIC ve buzsuz kayanın önemi doğrulandı. Sıcak SST zararlı:
  artan popülasyonların yaşadığı en sıcak yaz SST'si ≈ **1.5 °C**; azalan popülasyonların çoğu bunun üstünü yaşamış.
- **Marguerite Körfezi** için: Batı Antarktika Yarımadası'nın geneline göre "daha yavaş ısınan" bir bölge.

**Bizim katmanlarla eşleşme:** `sst_yaz` ve `buz_yaz` bu çalışmadaki değişkenlerin doğrudan karşılığı.
Buzsuz kaya katmanımız **yok** (bkz. Bölüm 5).

## 2. Deniz buzu, kril ve beslenme

| Kaynak | Bulgu | Bizim katman |
|---|---|---|
| Fraser, W. & Hofmann, E. (2003). A predator's perspective on causal links between climate change, physical forcing and ecosystem response. *Mar. Ecol. Prog. Ser.* 265:1–15. https://doi.org/10.3354/meps265001 *(özet)* | Deniz buzu → kril üremesi → av bulunabilirliği → Adélie beslenme ekolojisi arasında doğrudan nedensel ilişki. | `buz_kis`, `buz_yillik` (kış buzu kril üremesi için) |
| Erdmann, E. S., Ribic, C. A., Patterson-Fraser, D. L. & Fraser, W. R. (2011). Characterization of winter foraging locations of Adélie penguins along the Western Antarctic Peninsula, 2001–2002. *Deep-Sea Res. II* 58:1710–1718. https://doi.org/10.1016/j.dsr2.2010.10.054 *(özet)* | Kış beslenme yerini en çok **deniz derinliği** belirliyor (çoğu kuş < 200 m sığ sularda ve derin çukurların kenarında). Paket buz içindeki değişkenlik ve rüzgâr anlamlı çıkmadı (yazarlar: uydu verisi çözünürlüğü yetersiz olabilir). Çalışma Marguerite Körfezi bölgesinde. | **Yok** — batimetri (Bölüm 5) |
| Ducklow, H. W. vd. (2006). Marine pelagic ecosystems: the West Antarctic Peninsula. *Phil. Trans. R. Soc. B* 362(1477):67–94. https://doi.org/10.1098/rstb.2006.1955 *(künye doğrulandı, içerik okunmadı)* | Batı Antarktika Yarımadası ekosistem değişiminin sentezi (arka plan kaynağı). | — |
| Lynch, H. J., Naveen, R., Trathan, P. N. & Fagan, W. F. (2012). Spatially integrated assessment reveals widespread changes in penguin populations on the Antarctic Peninsula. *Ecology* 93:1367–1377. https://doi.org/10.1890/11-1588.1 *(künye doğrulandı, içerik okunmadı)* | Yarımadada penguen popülasyonlarındaki geniş çaplı değişim (arka plan kaynağı). | — |

## 3. Karadaki üreme habitatı: hava, kar, rüzgâr

| Kaynak | Bulgu | Bizim katman |
|---|---|---|
| Cimino, M., Fraser, W., Patterson-Fraser, D., Saba, V. & Oliver, M. (2014). Large-scale climate and local weather drive interannual variability in Adélie penguin chick fledging mass. *Mar. Ecol. Prog. Ser.* 513:253–268. https://doi.org/10.3354/meps10928 *(özet)* | Palmer İstasyonu, 1989–2011: yavruların uçma ağırlığını beslenmeden çok **iklim ve yerel hava** belirliyor. Hava sıcaklığı ↑ → ağırlık ↑; batı rüzgârı ↑ → ağırlık ↓. | `bio10` (en sıcak çeyreğin sıcaklığı = üreme mevsimi), `bio5`. Rüzgâr **yok** |
| Chapman, E., Hofmann, E., Patterson, D., Ribic, C. & Fraser, W. (2011). Marine and terrestrial factors affecting Adélie penguin chick growth and recruitment off the western Antarctic Peninsula. *Mar. Ecol. Prog. Ser.* 436:273–289. https://doi.org/10.3354/meps09242 *(özet)* | Model çalışması: yavru yüzeyinin yalnızca %10'unun **kar/eriyik suyla ıslanması** uçma ağırlığını hayatta kalma şansını düşürecek kadar azaltıyor. | `bio18` (en sıcak çeyreğin yağışı = üreme mevsimi yağışı) |
| Cimino, M. A., Larsen, G. D., Johnston, D. W. & Groff, D. V. (2025). Long-term, landscape- and wind-driven snow conditions influence Adélie penguin colony extinctions. *Landscape Ecology* 40(4). https://doi.org/10.1007/s10980-025-02088-y *(özet)* | Palmer, 1975–2022: rüzgârın taşıdığı kar alçak, güneye bakan yamaçlarda birikiyor; penguenler yüksek, kuzeye bakan zemini tercih ediyor; güneye bakan alt koloniler yok olmuş. Yağış penguenlere zararlı. | `bio18`, `bio19`, `bio12` (dolaylı). Topografya ve rüzgâr **yok**; 0.25° bu ölçeği zaten yakalayamaz |

## 4. Bizim verimizden çıkan iki önemli bulgu

**4.1 Çeyreklerin hangi mevsime denk geldiği** (`era5/ara/aylik_normaller.nc`, 703 hücre):

| Çeyrek | Hangi aylar | Anlamı |
|---|---|---|
| En sıcak | Ara–Oca–Şub (553 hücre), Oca–Şub–Mar (150) | **Her yerde üreme mevsimi** → `bio10`, `bio18` ekolojik olarak tutarlı |
| En soğuk | Haz–Tem–Ağu (364), Tem–Ağu–Eyl (339) | **Her yerde kış** → `bio11`, `bio19` tutarlı |
| En yağışlı | Ağu–Eki (254), Mar–May (244), Tem–Eyl (87), Ara–Şub (51) ve diğerleri | **Yerden yere farklı mevsim** |
| En kurak | Kas–Oca (418), Ara–Şub (198), Haz–Ağu (83) | Yerden yere farklı |

**4.2 `bio8` ve `bio9` haritalarında yapay kesintiler.** `bio8.png` haritasında komşu hücreler arasında
yaklaşık 7 °C'lik ani sıçramalar ve etrafından çok farklı tek hücreler var (ör. 67.1°G hattı). Bunlar gerçek iklim
farkı değil; "en yağışlı çeyrek" Mart–Mayıs'tan Ağustos–Ekim'e atladığı için oluşuyor.

Booth, T. H. (2022). Checking bioclimatic variables that combine temperature and precipitation data before their
use in species distribution models. *Austral Ecology*. https://doi.org/10.1111/aec.13234 *(özet)* — Sıcaklık ve
yağışı birleştiren dört değişkenin (bio8, bio9, bio18, bio19) hesaplamada kullanılan çeyrek aniden değiştiğinde
kesinti gösterebildiğini, bu yüzden son yıllarda sıkça modelden çıkarıldıklarını; kullanmadan önce haritalarının
kontrol edilmesi gerektiğini belirtiyor.

→ Bizim bölgede **bio8 ve bio9 bu sorunu belirgin biçimde taşıyor**. bio18 ve bio19'da çeyrek yalnızca komşu
aylar arasında kayıyor (Ara–Şub ↔ Oca–Mar), sorun daha hafif; haritaları yine de kontrol edilmeli.

## 5. Literatürde olup bizim katmanlarımızda olmayanlar

| Değişken | Kaynak | Not |
|---|---|---|
| Buzsuz kaya (yuvalama zemini) | Cimino vd. 2016 | Penguen yalnızca buzsuz kayada yuva yapar. Hazır veri: SCAR Antarctic Digital Database kaya alanları (eklenirse 0.25° ızgarada "hücredeki kaya oranı" olarak). Karar: öğrenci + danışman |
| Batimetri (deniz derinliği) | Erdmann vd. 2011 | Kış beslenmesinde en etkili değişken. Hazır veri: GEBCO. Karar: öğrenci + danışman |
| Rüzgâr | Cimino vd. 2014, 2025 | ERA5'te var (10 m rüzgâr); eklemek teknik olarak kolay. Karar: öğrenci + danışman |
| Deniz yüzeyi tuzluluğu | — | Öğrencinin önerisi (K-016); bu taramada Adélie habitat modellerinde kullanıldığına dair doğrulanmış kaynak bulunamadı |

## 6. Eşdoğrusallık (collinearity) için standart uygulama

Dormann, C. F., Elith, J., Bacher, S. vd. (2013). Collinearity: a review of methods to deal with it and a simulation
study evaluating their performance. *Ecography* 36:27–46. https://doi.org/10.1111/j.1600-0587.2012.07348.x *(özet)*

- Değişkenler arası **|r| = 0.7** "halk arasında kullanılan" eşiğin, eşdoğrusallığın tahminleri ciddi bozmaya
  başladığı noktanın uygun bir göstergesi olduğu bulunmuş.
- Analizden önce **ekolojik bilgiyle ön seçim** eşdoğrusallık sorununu azaltır ama tamamen çözmez.

**Bizim matriste:** |r| > 0.8 → **49 çift**, |r| > 0.7 → **64 çift**. Hangi eşiğin kullanılacağı da raporda
gerekçesiyle yazılmalı. (`era5/output/yuksek_korelasyon.txt` 0.8 eşiğiyle üretildi; 0.7 istenirse `korelasyon.py`
içindeki `ESIK` değiştirilip yeniden çalıştırılır.)

## 7. Gruplar ve literatür bağlantısı (karar tablosu DEĞİL)

| Grup | Katmanlar | Literatür bağlantısı | Dikkat |
|---|---|---|---|
| Yaz denizi | `sst_yaz`, `sst_yillik` (r = 0.97) | Cimino 2016: yaz SST ana değişken, sıcak SST zararlı | İkisi neredeyse aynı bilgi |
| Deniz buzu | `buz_yaz`, `buz_yillik`, `buz_kis` | Cimino 2016 (yaz SIC), Fraser & Hofmann 2003 (kış buzu → kril) | `buz_yillik` hem yaz (0.98) hem kışla (0.88) çok yüksek korelasyonlu |
| Üreme mevsimi sıcaklığı | `bio10`, `bio5`, `bio1`, `bio6`, `bio11` | Cimino 2014: yaz hava sıcaklığı ↑ → yavru ağırlığı ↑ | Grup içi r = 0.83–0.999 |
| Üreme mevsimi yağışı | `bio18` (ve yağış grubu `bio12–14, 16, 17, 19`) | Chapman 2011, Cimino 2025: kar/ıslanma zararlı | `bio18` yağış grubunun geri kalanıyla r ≈ 0.91–0.94 |
| Mevsimsellik / günlük değişim | `bio4`, `bio7`, `bio2`, `bio3`, `bio15` | Doğrudan Adélie kaynağı bulunamadı | `bio15` diğer tüm katmanlarla \|r\| < 0.6 |
| Sorunlu | `bio8`, `bio9` | Booth 2022 | Bizim bölgede yapay kesintiler var (Bölüm 4.2) |

## 8. Danışmanla konuşulacak sorular

1. Cimino vd. (2016) gibi az sayıda, ekolojik gerekçeli değişkenle mi; yoksa referans projedeki gibi bioclim ağırlıklı mı ilerlenecek?
2. Eşdoğrusallık eşiği 0.7 mi, 0.8 mi?
3. bio8 / bio9 (yapay kesintiler) çıkarılsın mı?
4. Buzsuz kaya, batimetri, rüzgâr eklensin mi? (Teknik olarak eklenebilir; her biri ayrı bir veri kaynağı ve karar.)
5. 67 noktayla kaç değişken makul? (Az noktayla çok değişken modelin aşırı uyum yapmasına yol açabilir.)
