"""ERA5 aylık deniz yüzeyi sıcaklığı ve deniz buzundan 5 denizel katman üretir.

Kullanım:  .venv/bin/python denizel_hesapla.py      (önce indir.py çalışmış olmalı)

Katmanlar (2000–2025 takvim ayı normallerinden):
  sst_yillik  12 ayın ortalaması (°C)       buz_yillik  12 ayın ortalaması (%)
  sst_yaz     Aralık–Şubat ortalaması (°C)  buz_yaz     Aralık–Şubat ortalaması (%)
                                            buz_kis     Haziran–Ağustos ortalaması (%)

KARA HÜCRELERİ: ERA5'te bu iki değişken karada tanımsızdır (NaN). Penguen kolonileri kıyıda/karada
olduğu için MaxEnt bu kayıtları atmasın diye:
  - Doldurulmamış hali  → output/ham/
  - MaxEnt sürümü      → output/  (her kara hücresine, küre üzerindeki gerçek uzaklığa göre
                          EN YAKIN deniz hücresinin değeri atanır)
"""
import json

import numpy as np
from scipy.spatial import cKDTree

from ayarlar import ARA, CIKTI, CIKTI_HAM, HAM_VERI, YILLAR
from ortak import ac, asc_yaz, izgara_bilgisi, png_yaz, tif_yaz

YAZ = [12, 1, 2]
KIS = [6, 7, 8]


def normaller(kisa, birimler):
    da = ac(HAM_VERI / "aylik" / f"{kisa}_{YILLAR[0]}_{YILLAR[-1]}.nc")
    assert da.sizes["zaman"] == 12 * len(YILLAR)
    assert da.attrs.get("units") in birimler, f"{kisa} birimi beklenmedik: {da.attrs.get('units')}"
    # skipna=False: bir hücre herhangi bir ayda NaN ise kara kabul edilir (sonradan sayılır)
    return da.groupby("zaman.month").mean("zaman", skipna=False)


def katmanlar():
    sst = normaller("sst", ["K"]) - 273.15
    buz = normaller("siconc", ["(0 - 1)"]) * 100
    return {
        "sst_yillik": (sst.mean("month", skipna=False), "°C", "Yıllık ort. deniz yüzeyi sıcaklığı"),
        "sst_yaz": (sst.sel(month=YAZ).mean("month", skipna=False), "°C", "Yaz (Ara–Şub) deniz yüzeyi sıcaklığı"),
        "buz_yillik": (buz.mean("month", skipna=False), "%", "Yıllık ort. deniz buzu"),
        "buz_yaz": (buz.sel(month=YAZ).mean("month", skipna=False), "%", "Yaz (Ara–Şub) deniz buzu"),
        "buz_kis": (buz.sel(month=KIS).mean("month", skipna=False), "%", "Kış (Haz–Ağu) deniz buzu"),
    }


def kure_xyz(enlem, boylam):
    """Derece → birim küre üzerinde 3B nokta (en yakın komşu gerçek uzaklıkla bulunsun diye)."""
    e, b = np.deg2rad(enlem), np.deg2rad(boylam)
    return np.column_stack([np.cos(e) * np.cos(b), np.cos(e) * np.sin(b), np.sin(e)])


def en_yakin_doldur(dizi, enlem, boylam):
    """NaN hücreleri en yakın geçerli hücrenin değeriyle doldurur. (dolu dizi, doldurulan sayısı) döndürür."""
    B, E = np.meshgrid(boylam, enlem)
    gecerli = np.isfinite(dizi)
    agac = cKDTree(kure_xyz(E[gecerli], B[gecerli]))
    _, indis = agac.query(kure_xyz(E[~gecerli], B[~gecerli]))
    sonuc = dizi.copy()
    sonuc[~gecerli] = dizi[gecerli][indis]
    return sonuc, int((~gecerli).sum())


def main():
    CIKTI_HAM.mkdir(parents=True, exist_ok=True)
    ARA.mkdir(exist_ok=True)
    doldurma = {}
    kara_maskesi = None

    for ad, (da, birim, baslik) in katmanlar().items():
        da = da.transpose("latitude", "longitude")
        izg = izgara_bilgisi(da)
        ham = da.values.astype(float)
        if kara_maskesi is None:
            kara_maskesi = ~np.isfinite(ham)
        assert np.array_equal(~np.isfinite(ham), kara_maskesi), f"{ad}: NaN deseni diğer katmanlardan farklı"

        dolu, sayi = en_yakin_doldur(ham, da.latitude.values, da.longitude.values)
        doldurma[ad] = sayi
        cmap = "RdYlBu_r" if birim == "°C" else "Blues_r"
        donem = f"{YILLAR[0]}–{YILLAR[-1]}"

        asc_yaz(CIKTI_HAM / f"{ad}.asc", ham, izg)
        tif_yaz(CIKTI_HAM / f"{ad}.tif", ham, izg)
        png_yaz(CIKTI_HAM / f"{ad}.png", ham, izg, f"{baslik} — ham ({donem})", birim, kara_maskesi, cmap)

        asc_yaz(CIKTI / f"{ad}.asc", dolu, izg)
        tif_yaz(CIKTI / f"{ad}.tif", dolu, izg)
        png_yaz(CIKTI / f"{ad}.png", dolu, izg, f"{baslik} — kara dolduruldu ({donem})", birim, kara_maskesi, cmap)
        print(f"{ad:11s} min {np.nanmin(ham):7.2f}  max {np.nanmax(ham):7.2f} {birim}  doldurulan hücre: {sayi}")

    (ARA / "doldurma.json").write_text(json.dumps(doldurma, indent=1))
    np.save(ARA / "kara_maskesi.npy", kara_maskesi)


if __name__ == "__main__":
    main()
