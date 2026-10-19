"""Katman okuma/yazma yardımcıları: ESRI ASCII Grid (.asc), GeoTIFF (.tif), önizleme (.png)."""
import os

# rasterio 1.5.2'nin ARM (aarch64) wheel'indeki GDAL 3.12.2 açılışta zararsız "apszKnownConfigOptions[]
# isn't correctly sorted" satırları basıyor. Bunları susturur; gerçek hatalarda rasterio yine istisna fırlatır.
os.environ.setdefault("CPL_LOG", os.devnull)

import numpy as np  # noqa: E402
import rasterio  # noqa: E402
import xarray as xr  # noqa: E402
from rasterio.transform import from_origin  # noqa: E402

from ayarlar import HUCRE, NODATA  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def ac(yol):
    """NetCDF açar, tek veri değişkenini (enlem kuzeyden güneye sıralı) DataArray olarak döndürür."""
    ds = xr.open_dataset(yol)
    ad = [v for v in ds.data_vars][0]
    da = ds[ad]
    if "valid_time" in da.dims:
        da = da.rename(valid_time="zaman")
    return da.sortby("latitude", ascending=False).sortby("longitude")


def izgara_bilgisi(da):
    """Izgara köşesi ve boyutları. ERA5 koordinatları hücre MERKEZİdir; asc köşesi yarım hücre kaydırılır."""
    enlem = da["latitude"].values
    boylam = da["longitude"].values
    assert np.allclose(np.diff(boylam), HUCRE) and np.allclose(np.diff(enlem), -HUCRE), "ızgara 0.25° değil"
    return {
        "ncols": len(boylam),
        "nrows": len(enlem),
        "xllcorner": float(boylam.min() - HUCRE / 2),
        "yllcorner": float(enlem.min() - HUCRE / 2),
        "cellsize": HUCRE,
        "bati": float(boylam.min() - HUCRE / 2),
        "kuzey": float(enlem.max() + HUCRE / 2),
    }


def asc_yaz(yol, dizi, izg):
    """ESRI ASCII Grid yazar (ondalık ayırıcı nokta, NaN → NODATA)."""
    veri = np.where(np.isfinite(dizi), dizi, NODATA)
    with open(yol, "w") as f:
        f.write(f"ncols {izg['ncols']}\n")
        f.write(f"nrows {izg['nrows']}\n")
        f.write(f"xllcorner {izg['xllcorner']:.6f}\n")
        f.write(f"yllcorner {izg['yllcorner']:.6f}\n")
        f.write(f"cellsize {izg['cellsize']:.6f}\n")
        f.write(f"NODATA_value {NODATA}\n")
        for satir in veri:  # ilk satır en kuzey
            f.write(" ".join(f"{d:.6f}" if d != NODATA else str(NODATA) for d in satir) + "\n")


def asc_baslik(yol):
    with open(yol) as f:
        return [next(f).strip() for _ in range(6)]


def asc_oku(yol):
    veri = np.loadtxt(yol, skiprows=6)
    return np.where(veri == NODATA, np.nan, veri)


def tif_yaz(yol, dizi, izg):
    donusum = from_origin(izg["bati"], izg["kuzey"], izg["cellsize"], izg["cellsize"])
    with rasterio.open(
        yol, "w", driver="GTiff", height=izg["nrows"], width=izg["ncols"], count=1,
        dtype="float32", crs="EPSG:4326", transform=donusum, nodata=NODATA,
    ) as f:
        f.write(np.where(np.isfinite(dizi), dizi, NODATA).astype("float32"), 1)


def png_yaz(yol, dizi, izg, baslik, birim, kara_maskesi=None, cmap="viridis"):
    """Renk skalası ve birimli önizleme. kara_maskesi verilirse kıyı çizgisi olarak çizilir."""
    kapsam = [izg["bati"], izg["bati"] + izg["ncols"] * HUCRE,
              izg["kuzey"] - izg["nrows"] * HUCRE, izg["kuzey"]]
    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(np.ma.masked_invalid(dizi), extent=kapsam, cmap=cmap, origin="upper")
    if kara_maskesi is not None:
        enlem = np.linspace(kapsam[3] - HUCRE / 2, kapsam[2] + HUCRE / 2, izg["nrows"])
        boylam = np.linspace(kapsam[0] + HUCRE / 2, kapsam[1] - HUCRE / 2, izg["ncols"])
        ax.contour(boylam, enlem, kara_maskesi.astype(float), levels=[0.5], colors="k", linewidths=0.8)
    fig.colorbar(im, ax=ax, label=birim)
    ax.set_title(baslik)
    ax.set_xlabel("Boylam (°)")
    ax.set_ylabel("Enlem (°)")
    ax.set_aspect(1 / np.cos(np.deg2rad(68)))  # 68°G'de 1° boylam ≈ 0.37° enlem uzunluğunda
    fig.tight_layout()
    fig.savefig(yol, dpi=120)
    plt.close(fig)
