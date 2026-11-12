# Veri beklemeyen rapor revizyonu

Kapsam: kullanıcının “tmm 1 devam et” isteği. Bu adımda model eğitilmedi, yeni veri kaynağına geçilmedi, CDS işleri iptal edilmedi/çoğaltılmadı. Tamamlanan denetimler rapora aktarıldı; yeni koloni sonuçları tamamlanmış gibi yazılmadı.

## Çıktılar ve sürüm ayrımı

- Düzenlenebilir ana metin: `rapor/TUBITAK_2204C_PROJE_RAPORU.md`.
- Aynı metinden üretilen Word: `rapor/TUBITAK_2204C_PROJE_RAPORU.docx`.
- Son görsel kontrolden sonra yenilenen PDF: `rapor/TUBITAK_2204C_PROJE_RAPORU.pdf`.
- Önceki MD/Word/PDF ve üretici değişmeden `rapor/arsiv/2026-11-12_veri_oncesi/` altında korundu. Kaynak raporun kullanıcının verdiği Downloads kopyasına dokunulmadı.
- Bu sürüm tamamlanmış koloni araştırması veya yarışmaya sunulacak nihai rapor değildir. İlk sayfa, özet, yöntem ve bulgular tamamlanma sınırını açıkça belirtir.

## Yapılan bilimsel ve editoryal düzeltmeler

1. Yinelenen kapak metni kaldırıldı; amaç yalnız doğrulanmış koloni bulunuşu olarak tanımlandı. Genel GBIF gözlemi ile pozitif yuva sayımı birbirinin yerine kullanılmadı.
2. 704 temiz GBIF kaydındaki 163 adet 2026 kaydı açıklandı. Eski 67, denetimdeki 61 ve yerel MAPPPD 14 hücre farklı örneklemler olarak ayrıldı; “bağımsız hücre” iddiası kaldırıldı.
3. Kaya kaynağı SCAR ADD v7.11 olarak düzeltildi; kullanılmayan REMA, yükseklik/eğim/bakı üretimi iddiası çıkarıldı. Kıyı ve kaya DOI'leri, MAPPPD sürümü/lisansı ve ERA5 DOI'leri eklendi.
4. 0,25° çıktı ızgarası ile yaklaşık 31 km ERA5 yerel çözünürlüğü ayrıldı. Tam çevresel dikdörtgenin gerçek WGS84 alanı 202681,64 km² olarak düzeltildi; koloni/habitat alanı diye etiketlenmedi. Adelaide'ın konum cümlesi düzeltildi.
5. Özellik sınıfı HTML kanıtına göre LQH; eski LQTH etiketi düzeltildi. L'nin tek başına ekolojik olarak imkânsız, LQH'nin karmaşık olduğu için doğru olduğu savunması çıkarıldı. AICc duyarlılık hesabı ENMeval veya kesin optimum diye sunulmadı.
6. Gerçek VIF tablosu, 240 eğitim/altı şema ve coğrafi null karşılaştırması eklendi. Şema koşullu yeniden örnekleme aralıkları genel güven aralığı diye adlandırılmadı. AUC 0,70 başarı skalası çıkarıldı.
7. Jackknife mavi=tek değişken, turkuaz=değişken çıkarılınca kalan kazanç, kırmızı=tümü olarak düzeltildi. Renk/çubuk açıklaması grafikten görsel olarak kontrol edildi.
8. Buz eğrisinin alt sınırı optimum, kaya zorunlu koşul, BIO18 sıvı yağmur/hipotermi ve SST kril toleransı kanıtı diye yorumlanmadı. SST kaynak kimliğinin doğrulanması fiziksel uç değer nedeninin çözülmesiyle karıştırılmadı.
9. Üç GCM'deki tam-model delta tablosu ve yerel buz klimatolojisi sapma/RMSE karşılaştırması eklendi. Bu tablolar yeni koloni, bağımsız gelecek doğrulaması veya bütün Bellingshausen başarım testi değildir.
10. Eski %42,2 ve benzeri kayıp/alan sonuçları yeni ekolojik sonuç olarak çıkarıldı. Eski 243 artış hücresinde 59 aralık dışı, 22 kat yön uyuşmazlığı; kuzeyde 24/24 yeni aralık bulgusu denetim olarak korundu. Toplam 246 uyuşmazlığın iklim katmanları değil eğitilmiş model katları olduğu düzeltildi.
11. Eski gelecek haritaları yeni koloni haritası gibi taşınmadı. George VI sığınak, CCAMLR kota ve tüm biyolojik gereksinimlerin karşılandığı iddiaları çıkarıldı. Bekleyen yeni koloni sonuçları ayrı paragrafta sıralandı.
12. Wang atfı PubMed PMID 42209243 üzerinden doğrulandı: yazarlar Jin-Rui Wang, Ai-Lian Hu, Juan Yang; doğru DOI sonu .037. .028 eski üreticideki hatalı kayıttır. SSP5-8.5/yüzyıl sonu/kıta ölçeği yerel SSP2-4.5/2050 doğrulaması sayılmadı.
13. Gallagher 2025 DOI 10.1002/ecs2.70091 eklendi; lojistik regresyon ve 500 m karasal hücrelerin bu çalışmayla doğrudan AUC kıyası oluşturmadığı açıklandı. Kullanılmayan ve delta eşiğini desteklemeyen Liu atfı kaynakçadan çıkarıldı.

## Sayısal kanıt dosyaları

| Rapor unsuru | Yerel kaynak |
|---|---|
| Kayıt/SST/alan/özellik denetimi | `maxent/cikti/revizyon_20261112/denetim_v2/summary.json`, `actual_features.csv` |
| MAPPPD 45 sayım / 19 yerleşim / 14 hücre | `gbif/temiz/revizyon_20261112/colony_summary.json` |
| Tablo 2 VIF | `maxent/cikti/revizyon_20261112/denetim_v2/vif.csv` |
| Tablo 3 AUC, kat standart sapması ve null farkları | `maxent/cikti/revizyon_20261112/comparison_v3/summary.csv`, `fold_metrics.csv` |
| Şekil 1 | `maxent/cikti/revizyon_20261112/figures/spatial_null_comparison.png` |
| Şekil 2 eski Jackknife | `maxent/cikti/deneme3/plots/Pygoscelis_adeliae_jacknife.png` |
| Tablo 4 tam-model deltaları | `maxent/cikti/revizyon_20261112/projection_IPSL/model_metrics.csv`; `projection_GFDL/model_metrics.csv`; `projection_MPI/model_metrics.csv` |
| Tablo 5 buz sapma/RMSE | `maxent/girdi/revizyon_IPSL_20261112_v2/ice_baseline_comparison.json`; GFDL ve MPI karşılıkları |
| Artış bileşenleri ve kuzey örtüşmesi | `maxent/cikti/revizyon_20261112/denetim_v2/legacy_increase_components.csv`, `summary.json` |
| İklim kaynak kimlikleri, parça sürümleri ve hash'ler | `maxent/girdi/cmip6_peninsula_20261112/*/receipt.json`; `docs/REPRO_MANIFEST_2026-11-12_v2.json` |

## Tek kaynaktan derleme

Eski `make_perfect_report.py`, kendi içinde kopyalanmış eski bilimsel metni yeniden yazabildiği için doğrudan çalıştırıldığında açıklama ile durur. Arşivdeki kopyasına dokunulmadı. Yeni üretici bilimsel metin üretmez; Markdown'ı Word'e biçimlendirir. Fontu küçülterek tam 18 sayfa hedeflenmedi; okunabilir A4 düzeni kullanıldı.

```bash
cd /home/halil/adelie-maxent-2204c
/home/halil/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 rapor/rapor_derle.py
/home/halil/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  /home/halil/.codex/plugins/cache/openai-primary-runtime/documents/26.1111.10930/skills/documents/render_docx.py \
  rapor/TUBITAK_2204C_PROJE_RAPORU.docx --output_dir work/rapor_qa_20261112_v2 --emit_pdf --dpi 110
```

Son görsel kontrolden sonra bu dizindeki PDF ana rapor PDF'sine kopyalandı. Özgün dosyalar arşivlenmeden üzerine yazılmadı. `rapor_derle.py` Markdown/Word SHA256 ve kullanılan şekilleri `.build.json` içinde kaydeder.

## Tamamlanan son kontrol

Son v2 renderin 10 sayfası tek tek incelendi; başlık çizgisi/fontları düzeltildi, tablolar ve şekil açıklamaları kontrol edildi. Beş tablo ve iki şekil vardır. `rapor/rapor_dogrula.py` ile Word tablolarının Markdown eşitliği, bütün kaynak paragraflarının aktarımı, VIF/AUC/delta/buz karşılaştırmasındaki 69 sayısal hücre ve eski iddiaların çıkarılması doğrulandı. PDF metninde bekleyen sonuçlar açıklamasının korunduğu da kontrol edildi.

Doğrulama komutu:

```bash
/home/halil/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 rapor/rapor_dogrula.py
```

Geçen kontrolün kaydı ve üç dosyanın SHA256 değerleri `rapor/TUBITAK_2204C_PROJE_RAPORU.verification.json` içindedir. Bu kontrol belge tutarlılığı içindir; yeni ekolojik model doğrulaması değildir. Yeni veri indirme veya MaxEnt çalıştırma yapılmadı. Commit/push yapılmadı.

## Kaynak doğrulaması

DOI metadata kontrolünde ERA5 aylık veri yayın yılı 2019, saatlik veri 2018; kaya poligonunun yaratıcıları Skachkova, Gerrish, Fretwell, Cooper; sürüm 7.11/yıl 2025 olarak doğrulandı. MAPPPD v5.0 web kaynağında CC BY 4.0, 5487 sayım ve 729 yerleşim doğrulandı. Bu kaynaklar metin/kaynakça uyumunda kullanıldı; 26 eski kaynağın hepsi doğrulanmış gibi bir iddia bırakılmadı.

## Kalan iş

Geniş alan koloni girdisi ve eğitimi, alan/kapsam seçimi, hedef-grup kıyası, günlük fenoloji ve yeni koloni haritaları tamamlanmadan bekleyen yerler sonuçla doldurulmayacak. Bu oturum yalnız kullanıcının seçtiği veri bağımsız rapor çalışmasını kapsamaktadır.
