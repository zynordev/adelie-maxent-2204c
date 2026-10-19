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


def _kara_siniri(kara_maskesi, izg):
    """Kara/deniz hücreleri arasındaki ortak HÜCRE KENARLARI (basamaklı sınır, uydurma yumuşatma yok)."""
    k, b, c = izg["kuzey"], izg["bati"], izg["cellsize"]
    parcalar = []
    m = kara_maskesi
    for i, j in zip(*np.nonzero(m[:, 1:] != m[:, :-1])):        # dikey kenarlar
        x = b + (j + 1) * c
        parcalar.append([(x, k - i * c), (x, k - (i + 1) * c)])
    for i, j in zip(*np.nonzero(m[1:, :] != m[:-1, :])):        # yatay kenarlar
        y = k - (i + 1) * c
        parcalar.append([(b + j * c, y), (b + (j + 1) * c, y)])
    return parcalar


def _derece(deger, yon):
    harf = {"enlem": ("K", "G"), "boylam": ("D", "B")}[yon][int(deger < 0)]
    return f"{abs(deger):g}°{harf}"


def png_yaz(yol, dizi, izg, baslik, birim, kara_maskesi=None, cmap="viridis", donem="2000–2025"):
    """Önizleme haritası. Pikseller ERA5 hücreleridir; görüntü bilerek yumuşatılmaz."""
    from matplotlib.collections import LineCollection
    from matplotlib.ticker import FuncFormatter

    from ayarlar import ROTHERA

    bati, kuzey, c = izg["bati"], izg["kuzey"], izg["cellsize"]
    dogu, guney = bati + izg["ncols"] * c, kuzey - izg["nrows"] * c
    olcek = np.cos(np.deg2rad((kuzey + guney) / 2))      # 1° boylamın 1° enleme oranı (~0.37)

    # Şekil boyu, haritanın gerçek en/boy oranından hesaplanır (boşluk kalmasın)
    gen_in = 7.2 * 0.70                                       # harita genişliği (inç)
    yuk_in = gen_in * (kuzey - guney) / ((dogu - bati) * olcek)
    fig_yuk = yuk_in + 1.35                                   # başlık + eksen + dipnot payı
    alt, yuk = 0.85 / fig_yuk, yuk_in / fig_yuk
    fig = plt.figure(figsize=(7.2, fig_yuk))
    ax = fig.add_axes([0.11, alt, 0.70, yuk])
    cax = fig.add_axes([0.84, alt, 0.03, yuk])

    im = ax.imshow(np.ma.masked_invalid(dizi), extent=[bati, dogu, guney, kuzey], cmap=cmap,
                   origin="upper", interpolation="nearest")
    ax.set_aspect(1 / olcek)

    if kara_maskesi is not None:
        ax.add_collection(LineCollection(_kara_siniri(kara_maskesi, izg), colors="k", linewidths=1.0))

    ax.plot(ROTHERA["boylam"], ROTHERA["enlem"], marker="*", ms=13, mfc="white", mec="k", mew=1.0)
    ax.annotate("Rothera", (ROTHERA["boylam"], ROTHERA["enlem"]), xytext=(7, 5),
                textcoords="offset points", fontsize=9, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.75))

    ax.set_xticks(np.arange(np.ceil(bati), dogu, 1))
    ax.set_yticks(np.arange(np.ceil(guney * 2) / 2, kuzey, 0.5))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: _derece(v, "boylam")))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: _derece(v, "enlem")))
    ax.grid(color="k", alpha=0.18, lw=0.5, ls="--")
    ax.tick_params(labelsize=8.5)
    ax.set_title(baslik, fontsize=11.5, fontweight="bold", loc="left")

    cb = fig.colorbar(im, cax=cax)
    cb.set_label(birim, fontsize=10)
    cb.ax.tick_params(labelsize=8.5)

    fig.text(0.11, 0.12 / fig_yuk,
             f"Veri: ERA5 (Hersbach vd. 2020), {donem}. Izgara 0.25°: her kare bir ERA5 hücresidir,\n"
             "görüntü bilerek yumuşatılmamıştır. Siyah çizgi: ERA5 kara–deniz sınırı (hücre kenarları).",
             fontsize=7, color="0.35", va="bottom")
    fig.savefig(yol, dpi=220)
    plt.close(fig)
