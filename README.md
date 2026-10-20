# Adélie Pengueni Ekolojik Niş Modeli — Marguerite Körfezi

**Program:** TÜBİTAK 2204-C
**Tür:** *Pygoscelis adeliae* (Adélie pengueni)
**Yöntem:** GBIF bulunuş kayıtları (2000–2026) + çevresel katmanlar → klasik MaxEnt → habitat uygunluk haritası + AUC
**Başarı ölçütü:** AUC > 0.70

Projenin tam bağlamı, alınan kararlar ve kurallar için: [`CLAUDE.md`](CLAUDE.md)

**Depo:** https://github.com/zynordev/adelie-maxent-2204c (private)

## Klasör yapısı

```
adelie-maxent/
├── CLAUDE.md          # Proje bağlamı ve AI çalışma kuralları (ana kaynak)
├── README.md          # Bu dosya
├── docs/
│   ├── README.md      # Kayıt sistemi: hangi dosya ne için, şablonlar
│   ├── GUNLUK.md      # Kronolojik çalışma günlüğü
│   ├── KARARLAR.md    # Numaralı karar kaydı (K-001, K-002, ...)
│   ├── ASAMALAR.md    # Aşama / yol haritası takibi
│   ├── literatur/     # Doğrulanmış literatür özetleri
│   └── toplantilar/   # Danışman toplantı notları
├── era5/              # İklim katmanı üretimi: kod + output/ (25 aday katman + README)
├── kaya/              # Buzsuz kaya katmanı üretimi (SCAR ADD v7.11)
├── gbif/              # Bulunuş kayıtları: indirme + temizlik → temiz/adelie_maxent.csv
└── maxent/            # MaxEnt girdileri (girdi/: seçilen 4 katman + 67 nokta) ve çalıştırmaları
```

İleride eklenecek: `rapor/`.

> Dosya/klasör adlarında Türkçe karakter ve boşluk kullanılmaz.
