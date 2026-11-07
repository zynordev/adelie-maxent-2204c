# Düzeltilmiş QGIS harita paketi

- `gunumuz_A4`: mevcut günümüz modelinin çevresel uygunluğu.
- `duyarlilik_A4`: eski 2050 denemesinin kaynakları doğru etiketlenmiş gösterimi; varsayımsal çevre değişimi.
- `degisim_A4`: sürekli uygunluk puanı farkının sınıfları; habitat alanı kaybı değil.
- `belirsizlik_A4`: novelty uyarısı ve katlar arasında değişim işareti uyuşmazlığı.

Her ürünün PNG, PDF ve ayrı QGIS proje kopyası vardır. Kaynak `harita/a1.qgz` ve eski haritalar korunmuştur. 300 DPI baskı çıktısı, gerçek iklim verisinin 0,25° çözünürlüğünden farklıdır.

`*_yalniz_gosterim_1km.tif` bilinear gösterim kopyalarıdır. Bunlar model girdisi veya istatistik kaynağı değildir. Fark ve belirsizlik haritaları özgün hücre sınırlarını korur.

Yeniden üretim (sistem Python + QGIS/GDAL + NumPy):

```bash
python maxent/fark_analizi.py
QT_QPA_PLATFORM=offscreen python harita/duzeltilmis_haritalar.py --smooth-display
```

Sayılar `maxent/cikti/duyarlilik_analizi_v1/ozet.json` içinden alınır. Dosya adındaki veya eski dizindeki 2050/ssp245 sözcüğü gerçek CMIP6 veri kökeni sayılmaz. Kaynak/model/dönem doğrulaması tamamlanmış yeni projeksiyonlar ayrı koşu ve manifestle saklanmalıdır.
