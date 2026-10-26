"""QGIS haritası için hazır katmanları üretir (harita/qgis_katmanlari.gpkg + uygunluk GeoTIFF).

Kullanım:  ../era5/.venv/bin/python -I hazirla.py

Girdiler:
  veri_ham/add_coastline_high_res_polygon_v7_11.gpkg — SCAR ADD kıyı çizgisi v7.11
    (Gerrish, Ireland, Fretwell, Cooper & Skachkova 2025, doi:10.5285/7d6793c2-2513-4752-8f37-11db5b791fb5, CC BY 4.0)
  ../maxent/cikti/deneme3/Pygoscelis_adeliae_avg.asc — 10 katlı ÇD ortalama uygunluk (cloglog, 0–1)
  ../gbif/temiz/adelie_maxent.csv — 67 MaxEnt noktası
Çıktılar (harita/):
  qgis_katmanlari.gpkg  katmanlar: kiyi_cizgi (kıyı çizgisi — haritada bunu kullan), kiyi (poligonlar),
                        noktalar, istasyonlar
  uygunluk_ortalama.tif MaxEnt ortalaması, EPSG:4326 tanımlı (asc dosyasında koordinat sistemi yok)
Tüm vektörler EPSG:3031'de (Antarktika Kutup Stereografik) — haritanın projeksiyonu da bu olmalı.
"""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent
sys.path.insert(0, str(KOK.parent / "era5"))
from ortak import asc_baslik, asc_oku, tif_yaz  # noqa: E402

import geopandas as gpd  # noqa: E402
import pandas as pd  # noqa: E402
import pyogrio  # noqa: E402
from shapely.geometry import Point, box  # noqa: E402

KIYI = KOK / "veri_ham" / "add_coastline_high_res_polygon_v7_11.gpkg"
MAXENT = KOK.parent / "maxent" / "cikti" / "deneme3" / "Pygoscelis_adeliae_avg.asc"
NOKTALAR = KOK.parent / "gbif" / "temiz" / "adelie_maxent.csv"
CIKTI = KOK / "qgis_katmanlari.gpkg"
KUTUP = "EPSG:3031"
PAY = 1.0   # harita kenarında boşluk kalmasın diye alanın 1° dışına kadar kıyı

ISTASYONLAR = [   # konumlar: COMNAP istasyon listesi düzeyinde yaklaşık değerler
    ("Rothera (BİK)", -67.568, -68.127),
    ("San Martín (AR)", -68.130, -67.103),
    ("Horseshoe Adası (Türk Bilim Kampı; ada konumu, yaklaşık)", -67.83, -67.22),
]


def main():
    h = {s.split()[0]: float(s.split()[1]) for s in asc_baslik(MAXENT)}
    bati, guney, c = h["xllcorner"], h["yllcorner"], h["cellsize"]
    dogu, kuzey = bati + h["ncols"] * c, guney + h["nrows"] * c

    katman = [k for k in pyogrio.list_layers(KIYI)[:, 0] if k != "layer_styles"][0]
    alan = gpd.GeoSeries([box(bati - PAY, guney - PAY, dogu + PAY, kuzey + PAY).segmentize(0.05)],
                         crs="EPSG:4326").to_crs(pyogrio.read_info(KIYI, layer=katman)["crs"])
    kiyi = pyogrio.read_dataframe(KIYI, layer=katman, bbox=tuple(alan.total_bounds))
    kiyi = kiyi.to_crs(KUTUP)
    # Çizgi sürümü: sınır ÖNCE çıkarılır, SONRA kırpılır → kırpma kutusunun kenarları kıyı gibi çizilmez
    cizgi = gpd.GeoDataFrame(kiyi[["surface"]], geometry=kiyi.boundary, crs=KUTUP)
    cizgi = gpd.clip(cizgi, alan.to_crs(KUTUP))
    kiyi = gpd.clip(kiyi, alan.to_crs(KUTUP))
    print(f"kıyı katmanı '{katman}': {len(kiyi)} poligon, {len(cizgi)} çizgi")
    kiyi.to_file(CIKTI, layer="kiyi", driver="GPKG")            # dolgu için (kırpma kenarları içerir)
    cizgi.to_file(CIKTI, layer="kiyi_cizgi", driver="GPKG")     # haritada kıyı çizgisi olarak bu kullanılmalı

    m = pd.read_csv(NOKTALAR)
    gpd.GeoDataFrame(m, geometry=[Point(x, y) for x, y in zip(m.longitude, m.latitude)],
                     crs="EPSG:4326").to_crs(KUTUP).to_file(CIKTI, layer="noktalar", driver="GPKG")
    gpd.GeoDataFrame({"ad": [a for a, _, _ in ISTASYONLAR]},
                     geometry=[Point(x, y) for _, y, x in ISTASYONLAR],
                     crs="EPSG:4326").to_crs(KUTUP).to_file(CIKTI, layer="istasyonlar", driver="GPKG")

    izg = {"ncols": int(h["ncols"]), "nrows": int(h["nrows"]), "cellsize": c, "bati": bati, "kuzey": kuzey}
    tif_yaz(KOK / "uygunluk_ortalama.tif", asc_oku(MAXENT), izg)
    kutup_kopyasi(KOK / "uygunluk_ortalama.tif", KOK / "uygunluk_ortalama_3031.tif")
    print(f"yazıldı: {CIKTI.name} (kiyi, noktalar={len(m)}, istasyonlar), uygunluk_ortalama.tif")


def kutup_kopyasi(kaynak, hedef, cozunurluk=1000):
    """Raster'ı EPSG:3031'e EN YAKIN KOMŞU ile 1 km ızgaraya çevirir.

    QGIS 4326 → 3031 anlık dönüşümünde hücre kenarlarını yumuşatıyordu. 1 km'lik ince ızgara + en yakın komşu:
    her ERA5 hücresi (≈10 × 28 km) keskin, tek renkli bir blok olarak kalır; değerler değişmez, enterpolasyon yok.
    """
    import rasterio
    from rasterio.warp import Resampling, calculate_default_transform, reproject

    with rasterio.open(kaynak) as k:
        donusum, gen, yuk = calculate_default_transform(k.crs, KUTUP, k.width, k.height, *k.bounds,
                                                        resolution=cozunurluk)
        profil = k.profile | {"crs": KUTUP, "transform": donusum, "width": gen, "height": yuk}
        with rasterio.open(hedef, "w", **profil) as h:
            reproject(rasterio.band(k, 1), rasterio.band(h, 1), resampling=Resampling.nearest,
                      src_nodata=k.nodata, dst_nodata=k.nodata)


if __name__ == "__main__":
    main()
