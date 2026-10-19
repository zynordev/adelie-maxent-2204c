"""ERA5 verisini Copernicus CDS'ten indirir.

Kullanım:  .venv/bin/python indir.py
Gereken:   ~/.cdsapirc (url + key) ve veri setlerinin lisanslarının CDS sitesinde kabul edilmiş olması.

İndirilenler (veri_ham/):
  saatlik/t2m_saatlik_YYYY.nc   2 m sıcaklık, saatlik (günlük maks/min bundan hesaplanır), yıl yıl
  aylik/tp_2000_2025.nc         toplam yağış, aylık ortalama
  aylik/sst_2000_2025.nc        deniz yüzeyi sıcaklığı, aylık ortalama
  aylik/siconc_2000_2025.nc     deniz buzu, aylık ortalama

Neden saatlik veri? Planlanan 'derived-era5-single-levels-daily-statistics' veri seti günlük maks/min'i
CDS sunucusunda saatlik veriden hesaplar, ancak kuyruğu çok yavaştır (2026-10-19'da 35 dk'da hiç
başlamadı). Aynı hesabı saatlik veriden kendimiz yapınca sonuç birebir aynı çıktı (fark 0.0 K,
bkz. saatlik_gunluk_karsilastir.py ve docs/KARARLAR.md K-013).

- Yeniden başlatılabilir: inmiş dosyalar atlanır, yarım kalanlar ('.part') baştan alınır.
- CDS kuyruk sınırına takılan istek bekleyip yeniden denenir.
- Her başarılı indirme 'veri_ham/indirme_kaydi.csv' dosyasına tarihiyle yazılır (README için).
"""
import csv
import datetime as dt
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import cdsapi

from ayarlar import ALAN, DS_AYLIK, DS_SAATLIK, HAM_VERI, YILLAR

AYLAR = [f"{a:02d}" for a in range(1, 13)]
GUNLER = [f"{g:02d}" for g in range(1, 32)]   # CDS geçersiz günleri (ör. 30 Şubat) yok sayar
SAATLER = [f"{s:02d}:00" for s in range(24)]

# Aynı anda CDS kuyruğuna gönderilecek istek sayısı
ESZAMANLI = 4

# CDS "temporarily limited" / 429 derse bu kadar bekleyip yeniden dener
BEKLEME_SN = 120
DENEME = 30

HAM_VERI.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(HAM_VERI.parent / "indirme.log")],
)
log = logging.getLogger("indir")


def gorevler():
    """(veri seti, istek, hedef dosya) üçlülerini üretir. Küçük aylık dosyalar önce."""
    for degisken, kisa in [
        ("total_precipitation", "tp"),
        ("sea_surface_temperature", "sst"),
        ("sea_ice_cover", "siconc"),
    ]:
        istek = {
            "product_type": ["monthly_averaged_reanalysis"],
            "variable": [degisken],
            "year": [str(y) for y in YILLAR],
            "month": AYLAR,
            "time": ["00:00"],
            "area": ALAN,
            "data_format": "netcdf",
            "download_format": "unarchived",
        }
        yield DS_AYLIK, istek, HAM_VERI / "aylik" / f"{kisa}_{YILLAR[0]}_{YILLAR[-1]}.nc"

    for yil in YILLAR:
        istek = {
            "product_type": ["reanalysis"],
            "variable": ["2m_temperature"],
            "year": [str(yil)],
            "month": AYLAR,
            "day": GUNLER,
            "time": SAATLER,
            "area": ALAN,
            "data_format": "netcdf",
            "download_format": "unarchived",
        }
        yield DS_SAATLIK, istek, HAM_VERI / "saatlik" / f"t2m_saatlik_{yil}.nc"


def indir(istemci, veri_seti, istek, hedef):
    if hedef.exists():
        return hedef, "atlandı (zaten var)"
    hedef.parent.mkdir(parents=True, exist_ok=True)
    gecici = hedef.with_suffix(".nc.part")
    for deneme in range(1, DENEME + 1):
        gecici.unlink(missing_ok=True)
        try:
            log.info("istek gönderildi: %s", hedef.name)
            istemci.retrieve(veri_seti, istek, str(gecici))
            break
        except Exception as e:
            sinir = "temporarily limited" in str(e) or "429" in str(e)
            if not sinir or deneme == DENEME:
                raise
            log.info("CDS kuyruk sınırı, %d sn sonra tekrar (%d/%d): %s", BEKLEME_SN, deneme, DENEME, hedef.name)
            time.sleep(BEKLEME_SN)
    gecici.rename(hedef)
    with open(HAM_VERI / "indirme_kaydi.csv", "a", newline="") as f:
        csv.writer(f).writerow([dt.date.today().isoformat(), veri_seti, hedef.name])
    return hedef, "indi"


def main():
    istemci = cdsapi.Client(quiet=True, progress=False)
    liste = list(gorevler())
    log.info("toplam %d dosya", len(liste))
    hatalar = []
    with ThreadPoolExecutor(ESZAMANLI) as havuz:
        isler = {havuz.submit(indir, istemci, *g): g[2] for g in liste}
        for i, gorev in enumerate(as_completed(isler), 1):
            try:
                hedef, durum = gorev.result()
                log.info("[%d/%d] %s: %s", i, len(liste), hedef.name, durum)
            except Exception as e:  # bir dosya başarısız olsa da diğerleri devam etsin
                hatalar.append(isler[gorev].name)
                log.error("[%d/%d] HATA %s: %s", i, len(liste), isler[gorev].name, str(e)[:300])
    if hatalar:
        log.error("%d dosya inemedi, scripti tekrar çalıştırın: %s", len(hatalar), ", ".join(hatalar))
        raise SystemExit(1)
    log.info("tüm dosyalar hazır")


if __name__ == "__main__":
    main()
