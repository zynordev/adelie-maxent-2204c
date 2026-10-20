"""Buzsuz kaya katmanı: her ERA5 hücresinde alanın yüzde kaçı buzsuz kaya (rock outcrop)?

Kullanım:  ../era5/.venv/bin/python -I kaya_hesapla.py

Girdi:  veri_ham/add_rock_outcrop_high_res_polygon_v7_11.gpkg
        SCAR Antarctic Digital Database — High resolution vector polygons of Antarctic rock outcrop, v7.11
        (Skachkova, Gerrish, Fretwell & Cooper 2025, UK Polar Data Centre, doi:10.5285/815525ca-cefe-4fbf-9224-3ee784e7de4e,
        CC BY 4.0). Bu bölgede (20°B–80°B) 2024/25 Sentinel-2 mozaiğinden otomatik çıkarılmıştır.
Çıktı:  ../era5/output/kaya.asc, .tif, .png  (diğer 24 katmanla birebir aynı ızgara; MaxEnt aynı klasörü ister)

Yöntem: ERA5 hücresi (0.25° × 0.25°) kenarları sıklaştırılarak eşit alanlı Lambert azimutal (Güney Kutbu)
projeksiyonuna çevrilir; kaya poligonlarıyla kesişim alanı / hücre alanı × 100 = % kaya örtüsü.
Denizdeki ve tamamen buzla kaplı hücreler 0'dır (NoData değil).
"""
import sys
from pathlib import Path

import numpy as np

KOK = Path(__file__).resolve().parent
sys.path.insert(0, str(KOK.parent / "era5"))
from ortak import asc_baslik, asc_oku, asc_yaz, png_yaz, tif_yaz  # noqa: E402

import geopandas as gpd  # noqa: E402
import pyogrio  # noqa: E402
from shapely.geometry import box  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

GPKG = KOK / "veri_ham" / "add_rock_outcrop_high_res_polygon_v7_11.gpkg"
KATMAN = "add_rock_outcrop_high_res_polygon_v7_11"   # dosyada ayrıca "layer_styles" katmanı var
ERA5_CIKTI = KOK.parent / "era5" / "output"
ESIT_ALAN = "+proj=laea +lat_0=-90 +lon_0=0 +datum=WGS84 +units=m +no_defs"


def main():
    h = {s.split()[0]: float(s.split()[1]) for s in asc_baslik(ERA5_CIKTI / "bio1.asc")}
    nrow, ncol, c = int(h["nrows"]), int(h["ncols"]), h["cellsize"]
    bati, guney = h["xllcorner"], h["yllcorner"]
    kuzey = guney + nrow * c

    # ERA5 hücreleri (satır 0 = en kuzey), kenarlar sıklaştırılarak (eğri kenarlar doğru projekte edilsin)
    hucreler = gpd.GeoDataFrame(
        {"satir": np.repeat(np.arange(nrow), ncol), "sutun": np.tile(np.arange(ncol), nrow)},
        geometry=[box(bati + j * c, kuzey - (i + 1) * c, bati + (j + 1) * c, kuzey - i * c).segmentize(0.01)
                  for i in range(nrow) for j in range(ncol)],
        crs="EPSG:4326",
    ).to_crs(ESIT_ALAN)

    # Yalnızca alanımızı kapsayan poligonları oku (dosyanın kendi CRS'inde sınır kutusu, 0.5° pay)
    bilgi = pyogrio.read_info(GPKG, layer=KATMAN)
    alan = gpd.GeoSeries([box(bati - 0.5, guney - 0.5, bati + ncol * c + 0.5, kuzey + 0.5).segmentize(0.05)],
                         crs="EPSG:4326").to_crs(bilgi["crs"])
    kaya = pyogrio.read_dataframe(GPKG, layer=KATMAN, bbox=tuple(alan.total_bounds))
    print(f"katman: {bilgi.get('layer_name', '?')} | CRS: {bilgi['crs']} | alandaki poligon: {len(kaya)}")
    kaya = kaya.to_crs(ESIT_ALAN)
    kaya["geometry"] = kaya.geometry.make_valid()
    kaya_birlesik = unary_union(kaya.geometry.values)   # örtüşen poligonlar iki kez sayılmasın

    oran = np.zeros((nrow, ncol))
    for hucre in hucreler.itertuples():
        kesisim = hucre.geometry.intersection(kaya_birlesik).area
        oran[hucre.satir, hucre.sutun] = 100 * kesisim / hucre.geometry.area

    izg = {"ncols": ncol, "nrows": nrow, "xllcorner": bati, "yllcorner": guney, "cellsize": c,
           "bati": bati, "kuzey": kuzey}
    asc_yaz(ERA5_CIKTI / "kaya.asc", oran, izg)
    tif_yaz(ERA5_CIKTI / "kaya.tif", oran, izg)
    kara = ~np.isfinite(asc_oku(ERA5_CIKTI / "ham" / "sst_yillik.asc"))
    png_yaz(ERA5_CIKTI / "kaya.png", oran, izg, "Buzsuz kaya örtüsü (SCAR ADD v7.11)", "% hücre alanı",
            kara, "copper_r", donem="Sentinel-2 2024/25",
            kaynak="SCAR Antarctic Digital Database v7.11 (Skachkova vd. 2025)")

    dolu = oran > 0
    print(f"kaya içeren hücre: {int(dolu.sum())}/{oran.size} | en yüksek: %{oran.max():.1f} | "
          f"kaya içeren hücrelerde ortanca: %{np.median(oran[dolu]):.2f} | toplam kaya alanı: "
          f"{kaya_birlesik.intersection(unary_union(hucreler.geometry.values)).area / 1e6:.0f} km²")


if __name__ == "__main__":
    main()
