# Adélie Pengueni Ekolojik Niş Modeli — Marguerite Körfezi

**Program:** TÜBİTAK 2204-C
**Tür:** *Pygoscelis adeliae* (Adélie pengueni)
**Yöntem:** GBIF bulunuş kayıtları (2000–2026) + çevresel katmanlar → klasik MaxEnt → habitat uygunluk haritası + AUC
**Başarı ölçütü:** AUC > 0.70

Projenin tam bağlamı, alınan kararlar ve kurallar için: [`CLAUDE.md`](CLAUDE.md)

## Klasör yapısı

```
adelie-maxent/
├── CLAUDE.md          # Proje bağlamı ve AI çalışma kuralları (ana kaynak)
├── README.md          # Bu dosya
└── docs/
    ├── README.md      # Kayıt sistemi: hangi dosya ne için, şablonlar
    ├── GUNLUK.md      # Kronolojik çalışma günlüğü
    ├── KARARLAR.md    # Numaralı karar kaydı (K-001, K-002, ...)
    ├── ASAMALAR.md    # Aşama / yol haritası takibi
    └── toplantilar/   # Danışman toplantı notları
```

İleride eklenecekler (iş başladıkça): `era5/` (iklim katmanı üretimi: kod + `output/`), `gbif/` (bulunuş kayıtları), `maxent/` (model çalıştırmaları), `rapor/`.

> Dosya/klasör adlarında Türkçe karakter ve boşluk kullanılmaz.
