# Kayıt Sistemi

Bu klasör projenin resmi kayıtlarını tutar. Amaç: her adımın **ne zaman, neden, kim tarafından** yapıldığının izlenebilmesi ve raporun "Yöntem" bölümünün bu kayıtlardan yazılabilmesi.

| Dosya | Ne zaman güncellenir | İçerik |
|---|---|---|
| `GUNLUK.md` | Her çalışma oturumunun sonunda | Tarih, yapılanlar, üretilen dosyalar, sorunlar, sıradaki adım |
| `KARARLAR.md` | Her yeni karar alındığında | Numaralı karar, gerekçe, kim karar verdi, durum |
| `ASAMALAR.md` | Bir aşamanın durumu değiştiğinde | Aşama listesi ve durumları |
| `toplantilar/` | Her danışman toplantısından sonra | Toplantı başına bir dosya |

## Kurallar

1. **Tarih biçimi:** `YYYY-AA-GG` (ör. 2026-10-19).
2. **En yeni kayıt en üstte** (`GUNLUK.md`). `KARARLAR.md`'de numaralar artan sırada.
3. **Kayıtlar silinmez.** Bir karar değişirse eski kaydın durumu `Değiştirildi → K-0xx` yapılır, yeni karar ayrı numara alır.
4. **Kaynak belirt.** Bir bilgi makaleden/dokümandan geldiyse DOI veya bağlantı eklenir.
5. **Gizli bilgi yazılmaz** (CDS API anahtarı, şifreler vb.).
6. "Kim" alanı: `Öğrenci`, `Danışman`, `Öğrenci + Danışman`, `Claude (öğrencinin isteğiyle)`.

## Şablonlar

### Günlük kaydı

```markdown
## YYYY-AA-GG — Kısa başlık

**Yapılanlar**
- ...

**Üretilen / değişen dosyalar**
- ...

**Sorunlar / notlar**
- ...

**Sıradaki adım**
- ...
```

### Karar kaydı

```markdown
### K-0xx — Karar başlığı
- **Tarih:** YYYY-AA-GG
- **Karar veren:** ...
- **Durum:** Geçerli | Onay bekliyor | Değiştirildi → K-0yy | İptal
- **Karar:** ...
- **Gerekçe:** ...
- **Alternatifler:** ...
- **Kaynak:** ...
```

### Toplantı notu (`toplantilar/YYYY-AA-GG-konu.md`)

```markdown
# Danışman toplantısı — YYYY-AA-GG

**Katılanlar:** ...
**Gündem:** ...

## Konuşulanlar
- ...

## Alınan kararlar
- (KARARLAR.md'ye K-0xx olarak işlendi)

## Yapılacaklar
- [ ] ... (kim, ne zamana)
```
