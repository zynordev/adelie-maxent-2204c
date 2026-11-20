# Rapor taslağı — Yöntem 1.1 ve 1.2 (öğrencinin kendi cümleleri)

> Durum: 2026-11-21 itibarıyla taslak. Metinler öğrencinin elle yazdığı haliyle, **aynen** kaydedilmiştir.
> Yazım ve noktalama düzeltmesi tüm rapor bittikten sonra son turda yapılacaktır (öğrencinin kararı).
> Rehber: `docs/RAPOR_YAZMA_REHBERI.pdf` (Bölüm 6.1). Rakamlar kaynak dosyalarla doğrulandı.

## 1.1 Araştırma sahası ve ızgara

Çalışma alanı, Antarktika Yarımadasının batı kıyısı kesminde yer alan Marguerite Körfezidir.
Modelleme ızgaramız 65,875–70,625° Güney Paralelleri  ile 63,875–73,125° Batı meridyenleri arasında tanımlanmıştır. 37 sütun  x 19 satır olmak üzere 703 adet  0,25°   10x28km kutba yaklaşınca boylam çizgileri birbirine yaklaştığından kare olmayan hücreler şeklinde oluşturlmuş, Izgara derece cinsinden tanımlanmış, haritalar EPSG:3031'de hazırlanmıştır

### Son turda yapılacaklar (1.1)
- Çalışma alanı = "Marguerite Körfezi ve çevresi" (alan, körfezin kendisi değil; ızgara körfezi içine alır).
- Hücre boyutu: derece olarak 0,25° × 0,25°, kilometre olarak **yaklaşık** 10 × 28 km (68°G'de; boylam boyu 9–11 km arası değişir). İki ölçüyü ayrı söyle.
- Üslup: "ızgaramız" → "ızgarası" (biz/bizim kullanılmaz); "Yarımadası'nın", "kesiminde", "Körfezi'dir".
- Uzun ikinci cümleyi ikiye böl; "x" yerine "×".

## 1.2 Varlık (presence) verisi

GBİF den 2000-2026 yılları arasında  çalışma alanı içerisindeki Adelie penguenlerininin verisi indirildi(DOI 10.15468/dl.jt3gt7)  Bilgilerin güvenilirliği için belirsizliği 10kmden büyük olan kayıtlar,  tekrar kayıtları, temizlenmiştir ve bir hücreye yığılan kayıt modeli yanıltabildiğinden her hücre başına tek kayıt bırakılmıştır
 Filtrelerin ardından ilk baştaki 1001 kayıt sayısı önce 704 seyreltmenin ardından 67ye düşmüştür .kalan 67 her bir penguen kaydını temsil eden 67 hücrenin 19u kara 48i deniz veya denizdeki kayalardır Bu kayıtlar  genel bulunuş yeri içerdiği için, 67 hücre herhangi bir penguenin  herhangi bir anda görüldüğü yerleri göstermektedir.”

### Son turda yapılacaklar (1.2)
- "Tekrar kayıtları": tanımı ekle (aynı koordinat + aynı tarih; 157 kayıt).
- "Bölgesel konum" filtresini (44 kayıt; konum adı yalnızca bölge) ekle ya da "başlıca filtreler" de.
- "19 kara / 48 deniz": ayrımın ERA5'in kaba kara-deniz maskesine göre olduğunu yaz; 48 "deniz" hücresinin 33'ünde kaya var (docs/KARARLAR.md K-021).
- Kayıt yıllarını açık yaz: temiz 704 kaydın 163'ü 2026 yılına ait.
- Fazladan tırnak işaretini sil; yazım ve noktalama.

## Sıradaki bölüm
1.3 Çevresel katmanlar (ERA5, 4 değişken, kara hücrelerinin doldurulması, katmanların hakemli olmadığı).
Dikkat: bio18 için Chapman (2011) atfını doğrulanana kadar koyma; korelasyon rakamı 0,65 (bio18 ↔ buz_yillik); Bio6'dan söz etme.
