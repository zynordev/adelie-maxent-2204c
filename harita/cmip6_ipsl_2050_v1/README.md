# Gerçek CMIP6 kaynaklı, deneysel 2050 haritaları

Kaynak: IPSL-CM6A-LR, r1i1p1f1, SSP2-4.5, 2041-2060. ERA5 2000-2025 tabanına kaynaklı delta yöntemi uygulandı. Bu paket eski sabit değişim denemesinden ayrıdır.

- `2050_A4.png/.pdf`: gerçek girdilere aktarılan eski MaxEnt modelinin uygunluğu.
- `gunumuz_A4.png/.pdf`: aynı eski modelin günümüz karşılığı.
- `degisim_A4.png/.pdf`: uygunluk puanı farkı; habitat alanı kaybı değil.
- `belirsizlik_A4.png/.pdf`: prediktör aralığı dışına çıkma ve katlar arasında değişim yönü uyuşmazlığı.

Modelin coğrafi aktarım değerlendirmesi zayıftır; ürünler keşif amaçlı ve nihai olmayan sonuçlardır. Tek GCM ve tek SSP; bağımsız koloni doğrulaması yok. Her haritada bu sınır belirtilir.

Sürekli uygunluk haritalarında bilinear görüntüleme kopyası kullanılır; kaynak bilgi çözünürlüğü 0,25° kalır. Fark ve belirsizlik hücreleri yumuşatılmaz. İstatistik ve model girdileri bu gösterim TIFF'lerinden hesaplanmaz.

Yöntem/komutlar: `docs/CMIP6_DELTA_VE_PROJEKSIYON_2026-11-08.md`. Analiz: `maxent/cikti/cmip6_ipsl_ssp245_2041_2060_v1/ozet.json`.
