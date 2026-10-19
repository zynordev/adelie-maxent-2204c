"""ERA5 saatlik sıcaklık + aylık yağıştan 2000–2025 Bio1–Bio19 katmanlarını üretir.

Kullanım:  .venv/bin/python bioclim_hesapla.py      (önce indir.py çalışmış olmalı)

Adımlar:
 1. Saatlik 2 m sıcaklık → günlük Tmax/Tmin (UTC günü) → her yıl-ay için ortalama → °C
 2. Aylık yağış (m/gün, aylık ortalama ürün) → mm/ay = ×1000 × ayın gün sayısı (artık yıllar dahil)
 3. 2000–2025 üzerinden takvim ayı ortalamaları → 12 aylık normaller
 4. biovars() (dismo::biovars ile aynı tanımlar) → output/bio1..bio19 (.asc, .tif, .png)
"""
import numpy as np
import xarray as xr

from ayarlar import ARA, CIKTI, HAM_VERI, YILLAR
from biovars import biovars
from ortak import ac, asc_yaz, izgara_bilgisi, png_yaz, tif_yaz

BIRIM = {
    **{f"bio{i}": "°C" for i in (1, 2, 5, 6, 7, 8, 9, 10, 11)},
    "bio3": "% (izotermalite)",
    "bio4": "°C sd × 100",
    **{f"bio{i}": "mm" for i in (12, 13, 14, 16, 17, 18, 19)},
    "bio15": "% (değişim katsayısı)",
}

TANIM = {
    "bio1": "Yıllık ortalama sıcaklık", "bio2": "Ortalama günlük sıcaklık aralığı",
    "bio3": "İzotermalite", "bio4": "Sıcaklık mevsimselliği",
    "bio5": "En sıcak ayın maks. sıcaklığı", "bio6": "En soğuk ayın min. sıcaklığı",
    "bio7": "Yıllık sıcaklık aralığı", "bio8": "En yağışlı çeyreğin ort. sıcaklığı",
    "bio9": "En kurak çeyreğin ort. sıcaklığı", "bio10": "En sıcak çeyreğin ort. sıcaklığı",
    "bio11": "En soğuk çeyreğin ort. sıcaklığı", "bio12": "Yıllık yağış",
    "bio13": "En yağışlı ayın yağışı", "bio14": "En kurak ayın yağışı",
    "bio15": "Yağış mevsimselliği", "bio16": "En yağışlı çeyreğin yağışı",
    "bio17": "En kurak çeyreğin yağışı", "bio18": "En sıcak çeyreğin yağışı",
    "bio19": "En soğuk çeyreğin yağışı",
}


def gunluk_uc_degerler(yil):
    """Bir yılın saatlik 2 m sıcaklığından günlük maks ve min (K).

    CDS'in 'derived-era5-single-levels-daily-statistics' ürünüyle aynı: UTC günü, 24 saatlik değerin
    maks/min'i. Birebir aynı sonuç verdiği doğrulandı (saatlik_gunluk_karsilastir.py).
    """
    saatlik = ac(HAM_VERI / "saatlik" / f"t2m_saatlik_{yil}.nc")
    assert saatlik.attrs.get("units") == "K", f"{yil}: sıcaklık birimi K değil"
    gun_sayisi = 366 if (yil % 4 == 0 and (yil % 100 != 0 or yil % 400 == 0)) else 365
    assert saatlik.sizes["zaman"] == gun_sayisi * 24, f"{yil}: {saatlik.sizes['zaman']} saat ≠ {gun_sayisi * 24}"
    assert int(saatlik.isnull().sum()) == 0, f"{yil}: saatlik sıcaklıkta NaN var"
    gunler = saatlik.resample(zaman="1D")
    return gunler.max(), gunler.min()


def aylik_sicaklik():
    """2000–2025 her yıl-ay için ortalama günlük Tmax ve Tmin (°C)."""
    eksik = [y for y in YILLAR if not (HAM_VERI / "saatlik" / f"t2m_saatlik_{y}.nc").exists()]
    assert not eksik, f"eksik yıllar: {eksik} — önce indir.py"
    tmax, tmin = zip(*(gunluk_uc_degerler(y) for y in YILLAR))
    tmax, tmin = xr.concat(tmax, "zaman"), xr.concat(tmin, "zaman")
    return tmax.resample(zaman="MS").mean() - 273.15, tmin.resample(zaman="MS").mean() - 273.15


def aylik_yagis():
    da = ac(HAM_VERI / "aylik" / f"tp_{YILLAR[0]}_{YILLAR[-1]}.nc")
    # ERA5 aylık ortalama üründe tp = ayın günlük ortalama birikimi (m/gün); metadata 'm' yazar
    assert da.attrs.get("units") == "m", f"tp birimi beklenmedik: {da.attrs.get('units')}"
    assert da.sizes["zaman"] == 12 * len(YILLAR)
    gun_sayisi = da["zaman"].dt.days_in_month
    return da * 1000 * gun_sayisi


def normal(da):
    """Yıl-ay serisinden 12 takvim ayı ortalaması → numpy (12, enlem, boylam)."""
    return da.groupby("zaman.month").mean("zaman").transpose("month", "latitude", "longitude")


def main():
    ARA.mkdir(exist_ok=True)
    CIKTI.mkdir(exist_ok=True)

    tmax_aylik, tmin_aylik = aylik_sicaklik()
    tmax, tmin = normal(tmax_aylik), normal(tmin_aylik)
    prec = normal(aylik_yagis())
    assert np.allclose(tmax.latitude, prec.latitude) and np.allclose(tmax.longitude, prec.longitude), \
        "sıcaklık ve yağış ızgaraları farklı"
    assert bool((tmax >= tmin).all()), "Tmax < Tmin olan hücre var"

    xr.Dataset({"tmax": tmax, "tmin": tmin, "tavg": (tmax + tmin) / 2, "prec": prec}).assign_attrs(
        aciklama=f"ERA5 aylık normaller {YILLAR[0]}-{YILLAR[-1]}; sıcaklık °C, yağış mm/ay"
    ).to_netcdf(ARA / "aylik_normaller.nc")

    izg = izgara_bilgisi(tmax)
    bio = biovars(tmin.values, tmax.values, prec.values)

    sst_yolu = HAM_VERI / "aylik" / f"sst_{YILLAR[0]}_{YILLAR[-1]}.nc"
    kara = ac(sst_yolu).isel(zaman=0).isnull().values if sst_yolu.exists() else None

    for ad, dizi in bio.items():
        asc_yaz(CIKTI / f"{ad}.asc", dizi, izg)
        tif_yaz(CIKTI / f"{ad}.tif", dizi, izg)
        cmap = "Blues" if BIRIM[ad] == "mm" else "RdYlBu_r"
        png_yaz(CIKTI / f"{ad}.png", dizi, izg, f"{ad.upper()} — {TANIM[ad]} ({YILLAR[0]}–{YILLAR[-1]})",
                BIRIM[ad], kara, cmap)
        print(f"{ad:6s} min {np.nanmin(dizi):9.2f}  max {np.nanmax(dizi):9.2f}  {BIRIM[ad]}")


if __name__ == "__main__":
    main()
