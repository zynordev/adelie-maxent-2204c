# Uygulama kapsamı ve yöntem kaydı

Kullanıcının 2026-11-08 tarihli “Tamam başla” talebiyle çözüm planının teknik uygulaması başlatıldı. Bu kayıt danışman onayı yerine geçmez.

## Korunan kapsam

- Tür: *Pygoscelis adeliae*. Alan: mevcut Marguerite Körfezi dikdörtgeni.
- Kayıtlar: mevcut 2000-2026 GBIF indirmesinden 67 hücre temsilcisi; hiçbir kayıt sessizce elenmedi veya taşınmadı.
- Şimdiki yorum: genel bulunuş için modellenen çevresel uygunluk. Üreme kolonisi, nüfus veya beslenme davranışı doğrudan modellenmiş sayılmıyor.
- Günümüz: ERA5 2000-2025, 0,25° ızgara; kaya SCAR ADD tek dönemli katman.
- Değişkenler: kaya, BIO18, yıllık SST, yıllık deniz buzu. Temel model ve orijinal çıktılar korunuyor.
- Kalibrasyon alanı mevcut tam dikdörtgen olarak yalnızca karşılaştırılabilir başlangıç deneyi için korundu. Bunun nihai ekolojik erişilebilir alan (M) olduğu iddia edilmiyor.

## Senaryoların ayrımı

1. **Tarihsel duyarlılık denemesi:** SST +0,8°C, deniz buzu ×0,80, BIO18 ×1,15. Kaynak `maxent/senaryo_duyarlilik.json`. Gerçek CMIP6 veya SSP etiketi yok. Eski dosya yolları geriye dönük izlenebilirlik için korunuyor.
2. **Gerçek CMIP6 hazırlığı:** SSP2-4.5 / 2041-2060, 2000-2025 tabanı önerisi için kaynak ve erişim doğrulanıyor. Aynı model/üye/ızgaradaki historical 2000-2014 ile SSP 2015-2025 referans devamı eşleştirilecek. Erişilebilir katalog, indirilmiş bölgesel veri ve doğrulanmış model girdisi üç ayrı durum olarak raporlanacak.

## İstatistik ve görselleştirme

- Uygunluk farkı = deneme puanı eksi günümüz puanı. ±0,05 **mutlak puan** aralığı kararlı sınıf olarak kullanılıyor; göreli %5 değişim değil.
- Hücre payı ile WGS84 elipsoidi üzerinde model dikdörtgeni alan payı ayrı hesaplanıyor. İkisi de gerçek habitat kaybı değildir.
- Gerekçelendirilmiş habitat eşiği ve ekolojik maske henüz yok; “uygun habitat km² kaybı” üretilmiyor.
- Aynı MaxEnt katının günümüz/deneme farkı eşleniyor. Dağılım, işaret uyumu, novelty ve clamping ayrı veriliyor. Bu katlar bağımsız iklim modelleri veya güven aralığı değil.
- Sürekli uygunluk haritalarındaki bilinear gösterim yalnız görseldir. 1 km gösterim TIFF'leri analize veya eğitime girmez. Kaynak çözünürlük 0,25° olarak yazılır.
- Sınıflanmış fark ve belirsizlik haritaları yumuşatılmaz. QGIS çıktıları ayrı projelerdir; `harita/a1.qgz` değişmez.

## Açık bilimsel kararlar

- Danışmanla üreme kolonisi hedefi seçilirse kayıtların doğrulanması ve model tasarımı değişmelidir.
- M alanı, bağımsız örnekleme çabası/target-group verisi, kayıt kalitesi duyarlılığı ve değişken mevsimselliği ayrıca gerekçelendirilmelidir.
- Coğrafi test performansı zayıfken daha iyi görünen harita veya bir yüksek AUC seçimi sorunu çözmez. Son model seçimi ve gelecek çıkarımlarında bu sonuç açıklanmalıdır.
- Çoklu GCM/SSP, bağımsız gözlem ve arazi doğrulaması elde edilmediyse varmış gibi raporlanamaz.

## Kaynak yöntem belgeleri

- [MaxEnt resmi sayfası ve öğretici](https://biodiversityinformatics.amnh.org/open_source/maxent/)
- [CMIP6 resmi CDS kataloğu](https://cds.climate.copernicus.eu/datasets/projections-cmip6?tab=overview)
- [Pangeo / ESGF bulut veri erişimi](https://pangeo-data.github.io/pangeo-cmip6-cloud/accessing_data.html)
- [Mekânsal çapraz doğrulama: Roberts vd.](https://doi.org/10.1111/ecog.02881)
