"""Çıktıların zorunlu doğrulaması + özet istatistik tablosu.

Kullanım:  .venv/bin/python dogrula.py

Kontroller:
 1. 24 .asc başlığı birebir aynı (ncols, nrows, köşe, cellsize, NODATA)
 2. Hiçbir MaxEnt katmanında NoData/NaN yok
 3. Rothera hücresi: Bio1 sıfırın birkaç derece altında; Bio5 > Bio1 > Bio6; Bio12 > 0
 4. Yaz deniz yüzeyi sıcaklığı yaklaşık −2 … birkaç °C; kış deniz buzu > yaz deniz buzu (deniz hücrelerinde)
Çıktılar: output/ozet_istatistik.csv, ara/rothera.json
"""
import json

import numpy as np
import pandas as pd

from ayarlar import ARA, CIKTI, CIKTI_HAM, DENIZEL, KATMANLAR, ROTHERA
from ortak import asc_baslik, asc_oku

sorunlar = []


def kontrol(kosul, mesaj):
    print(("  ✔ " if kosul else "  ✘ ") + mesaj)
    if not kosul:
        sorunlar.append(mesaj)


def main():
    print("1) Başlıklar")
    basliklar = {ad: asc_baslik(CIKTI / f"{ad}.asc") for ad in KATMANLAR}
    referans = basliklar["bio1"]
    farkli = [ad for ad, b in basliklar.items() if b != referans]
    kontrol(not farkli, f"24 başlık aynı {'' if not farkli else farkli}")
    print("     " + " | ".join(referans))

    veri = {ad: asc_oku(CIKTI / f"{ad}.asc") for ad in KATMANLAR}
    kara = np.load(ARA / "kara_maskesi.npy")
    doldurma = json.loads((ARA / "doldurma.json").read_text())

    print("2) NoData")
    for ad, d in veri.items():
        if np.isnan(d).any():
            kontrol(False, f"{ad}: {int(np.isnan(d).sum())} NoData hücre")
    kontrol(all(not np.isnan(d).any() for d in veri.values()), "MaxEnt katmanlarında NoData yok")

    print("3) Rothera hücresi")
    h = {b.split()[0]: float(b.split()[1]) for b in referans}   # asc başlığı → sözlük
    satir = int((h["yllcorner"] + h["nrows"] * h["cellsize"] - ROTHERA["enlem"]) // h["cellsize"])
    sutun = int((ROTHERA["boylam"] - h["xllcorner"]) // h["cellsize"])
    merkez = (h["yllcorner"] + (h["nrows"] - satir - 0.5) * h["cellsize"],
              h["xllcorner"] + (sutun + 0.5) * h["cellsize"])
    r = {ad: round(float(veri[ad][satir, sutun]), 3) for ad in KATMANLAR}
    r["hucre_merkezi"] = {"enlem": merkez[0], "boylam": merkez[1]}
    r["kara_hucresi_mi"] = bool(kara[satir, sutun])
    print(f"     hücre merkezi {merkez[0]:.2f}, {merkez[1]:.2f}  (kara hücresi: {r['kara_hucresi_mi']})")
    print("     " + "  ".join(f"{k}={r[k]}" for k in ["bio1", "bio5", "bio6", "bio12", "sst_yaz", "buz_kis"]))
    kontrol(-10 < r["bio1"] < 0, "Bio1 sıfırın birkaç derece altında")
    kontrol(r["bio5"] > r["bio1"] > r["bio6"], "Bio5 > Bio1 > Bio6")
    kontrol(r["bio12"] > 0, "Bio12 > 0")
    (ARA / "rothera.json").write_text(json.dumps(r, indent=1, ensure_ascii=False))

    print("4) Denizel tutarlılık (deniz hücreleri)")
    deniz = ~kara
    sst_yaz = veri["sst_yaz"][deniz]
    kontrol(sst_yaz.min() > -2.5 and sst_yaz.max() < 6,
            f"yaz SST aralığı {sst_yaz.min():.2f} … {sst_yaz.max():.2f} °C")
    kis_buyuk = veri["buz_kis"][deniz] >= veri["buz_yaz"][deniz]
    kontrol(kis_buyuk.all(), f"kış buzu ≥ yaz buzu: {int(kis_buyuk.sum())}/{int(deniz.sum())} deniz hücresi")
    kontrol(veri["buz_kis"][deniz].mean() > veri["buz_yaz"][deniz].mean(), "ortalama kış buzu > yaz buzu")
    for ad in DENIZEL:
        ham = asc_oku(CIKTI_HAM / f"{ad}.asc")
        kontrol(np.allclose(ham[deniz], veri[ad][deniz]), f"{ad}: doldurma deniz hücrelerini değiştirmedi")

    satirlar = []
    for ad in KATMANLAR:
        d = veri[ad]
        satirlar.append({
            "katman": ad, "min": round(float(np.nanmin(d)), 4), "max": round(float(np.nanmax(d)), 4),
            "ortalama": round(float(np.nanmean(d)), 4), "nodata_sayisi": int(np.isnan(d).sum()),
            "doldurulan_hucre": doldurma.get(ad, 0),
        })
    pd.DataFrame(satirlar).to_csv(CIKTI / "ozet_istatistik.csv", index=False)

    print("\nSONUÇ:", "tüm kontroller geçti" if not sorunlar else f"{len(sorunlar)} sorun: {sorunlar}")
    raise SystemExit(1 if sorunlar else 0)


if __name__ == "__main__":
    main()
