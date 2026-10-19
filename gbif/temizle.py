"""GBIF Adélie kayıtlarını temizler ve MaxEnt "Samples" dosyasını üretir.

Kullanım:  ../era5/.venv/bin/python -I temizle.py
Girdi:     ham/<indirme anahtarı>.zip  (indir_gbif.py ile indi; dokunulmaz)
Çıktılar (temiz/):
  kayitlar_temiz.csv     tüm adımlardan geçen kayıtlar (seyreltme öncesi)
  atilan_kayitlar.csv    atılan her kayıt + hangi adımda/neden atıldığı
  adelie_maxent.csv      MaxEnt girdisi: species,longitude,latitude — ERA5 hücresi başına 1 nokta
  temizlik_raporu.md     adım adım kayıt sayıları (otomatik)
  noktalar.png           kontrol haritası

Her eşik aşağıda sabit olarak durur; değiştirmek için yalnızca sabiti değiştirip yeniden çalıştırın.
Kararların gerekçesi: docs/KARARLAR.md K-018.
"""
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

KOK = Path(__file__).resolve().parent
sys.path.insert(0, str(KOK.parent / "era5"))   # ızgara ve çizim yardımcıları era5/ altında
from ortak import asc_baslik, asc_oku, png_yaz  # noqa: E402

CIKTI = KOK / "temiz"
ERA5_CIKTI = KOK.parent / "era5" / "output"

# --- Eşikler / seçimler (K-018) ---
MAKS_BELIRSIZLIK_M = 10_000       # ERA5 hücresinin dar kenarı ≈ 0.25° × cos(68°) × 111 km ≈ 10.4 km
# Gözlem yeri değil, bölge etiketi olan konum adları (koordinatları bölge merkezi/yer tutucu)
BOLGESEL_KONUMLAR = {"Western Antarctic Peninsula", "Marguerite Bay Antartica"}
YER_TUTUCU_ADIM = 0.5             # belirsizliği yok + iki koordinat da 0.5°'nin tam katı → bölge merkezi sayılır
# NOT: ondalık basamak sayısına göre eleme YAPILMAZ — metinde sondaki sıfırlar kaybolur
# (ör. −67.00 → "−67.0") ve hassas kayıtlar haksız yere elenir (2026-10-19'da denendi, geri alındı).
TUR_ADI = "Pygoscelis adeliae"

TUTULAN_SUTUNLAR = ["gbifID", "datasetKey", "basisOfRecord", "decimalLatitude", "decimalLongitude",
                    "coordinateUncertaintyInMeters", "eventDate", "year", "individualCount",
                    "locality", "occurrenceID"]


def oku():
    bilgi = json.loads((KOK / "indirme_bilgisi.json").read_text())
    with zipfile.ZipFile(KOK / "ham" / f"{bilgi['anahtar']}.zip") as z:
        with z.open(f"{bilgi['anahtar']}.csv") as f:
            # GBIF "Simple" dosyası: sekmeyle ayrılmış, tırnaksız (quoting=3 → QUOTE_NONE)
            d = pd.read_csv(f, sep="\t", quoting=3, low_memory=False, dtype={"gbifID": str})
    return d, bilgi


def izgara():
    h = {s.split()[0]: float(s.split()[1]) for s in asc_baslik(ERA5_CIKTI / "sst_yillik.asc")}
    kara = ~np.isfinite(asc_oku(ERA5_CIKTI / "ham" / "sst_yillik.asc"))
    return h, kara


def hucre(d, h):
    """MaxEnt'in yaptığı gibi: hücre = taban((x − köşe) / hücre boyu)."""
    kuzey = h["yllcorner"] + h["nrows"] * h["cellsize"]
    satir = np.floor((kuzey - d.decimalLatitude) / h["cellsize"]).astype(int)
    sutun = np.floor((d.decimalLongitude - h["xllcorner"]) / h["cellsize"]).astype(int)
    return satir, sutun


def main():
    CIKTI.mkdir(exist_ok=True)
    d, bilgi = oku()
    h, kara = izgara()
    d = d[TUTULAN_SUTUNLAR].copy()
    d["satir"], d["sutun"] = hucre(d, h)
    d["kara_hucresi"] = False
    alan_ici = d.satir.between(0, h["nrows"] - 1) & d.sutun.between(0, h["ncols"] - 1)
    d.loc[alan_ici, "kara_hucresi"] = kara[d.satir[alan_ici], d.sutun[alan_ici]]

    adimlar, atilan = [("GBIF indirmesi (ham)", len(d), "")], []

    def at(maske, adim, neden):
        nonlocal d
        secilen = d[maske].copy()
        secilen["adim"], secilen["neden"] = adim, neden
        atilan.append(secilen)
        d = d[~maske]
        adimlar.append((adim, len(d), f"−{int(maske.sum())}: {neden}"))

    at(~alan_ici, "1. Çalışma alanı", "ERA5 katmanlarının dışında")
    at(d.coordinateUncertaintyInMeters > MAKS_BELIRSIZLIK_M, "2. Koordinat belirsizliği",
       f"belirsizlik > {MAKS_BELIRSIZLIK_M / 1000:g} km")
    at(d.locality.isin(BOLGESEL_KONUMLAR), "3. Bölgesel konum", "konum adı yalnızca bölge (gözlem yeri değil)")
    yer_tutucu = (d.coordinateUncertaintyInMeters.isna()
                  & (d.decimalLatitude / YER_TUTUCU_ADIM).round(9).mod(1).eq(0)
                  & (d.decimalLongitude / YER_TUTUCU_ADIM).round(9).mod(1).eq(0))
    at(yer_tutucu, "4. Yer tutucu koordinat", f"belirsizlik yok ve koordinatlar {YER_TUTUCU_ADIM}°'nin tam katı")
    at(d.duplicated(["decimalLatitude", "decimalLongitude", "eventDate"], keep="first"),
       "5. Tekrar kayıt", "aynı koordinat + aynı tarih")

    d.drop(columns=["satir", "sutun"]).to_csv(CIKTI / "kayitlar_temiz.csv", index=False)
    pd.concat(atilan).drop(columns=["satir", "sutun"]).to_csv(CIKTI / "atilan_kayitlar.csv", index=False)

    # 6. Seyreltme: ERA5 hücresi başına 1 nokta. Temsilci = en küçük belirsizlikli kayıt
    #    (belirsizliği bilinmeyenler sona), eşitlikte en küçük gbifID → sonuç her çalıştırmada aynı.
    temsil = (d.assign(_b=d.coordinateUncertaintyInMeters.fillna(np.inf), _id=d.gbifID.astype(np.int64))
                .sort_values(["satir", "sutun", "_b", "_id"])
                .drop_duplicates(["satir", "sutun"]))
    adimlar.append(("6. Seyreltme (MaxEnt dosyası)", len(temsil), "ERA5 hücresi başına 1 nokta"))
    maxent = pd.DataFrame({"species": TUR_ADI, "longitude": temsil.decimalLongitude.round(6),
                           "latitude": temsil.decimalLatitude.round(6)})
    maxent.to_csv(CIKTI / "adelie_maxent.csv", index=False, float_format="%.6f")

    # Rapor
    kara_n = int(temsil.kara_hucresi.sum())
    satirlar = [
        "# GBIF temizlik raporu (otomatik — `temizle.py`)", "",
        f"- İndirme: {bilgi['atif']}",
        f"- Sorgu: `sorgu.json` · Ham dosya: `ham/{bilgi['anahtar']}.zip`", "",
        "| Adım | Kalan kayıt | Değişiklik |", "|---|---|---|",
        *[f"| {a} | {n} | {not_} |" for a, n, not_ in adimlar], "",
        f"**MaxEnt dosyası:** `adelie_maxent.csv` — {len(temsil)} nokta ({kara_n} kara, "
        f"{len(temsil) - kara_n} deniz hücresinde; kara/deniz ayrımı ERA5 kara–deniz maskesine göre).", "",
        "## Seyreltme öncesi temiz kayıtların dağılımı", "",
        "| Veri seti (datasetKey) | Kayıt |", "|---|---|",
        *[f"| `{k}` | {n} |" for k, n in d.datasetKey.value_counts().items()], "",
        "| basisOfRecord | Kayıt |", "|---|---|",
        *[f"| {k} | {n} |" for k, n in d.basisOfRecord.value_counts().items()], "",
        f"Yıl aralığı: {int(d.year.min())}–{int(d.year.max())} · Belirsizliği bilinmeyen kayıt: "
        f"{int(d.coordinateUncertaintyInMeters.isna().sum())} (tutuldu; GBIF'te çoğu kaynak bu alanı doldurmuyor).",
    ]
    (CIKTI / "temizlik_raporu.md").write_text("\n".join(satirlar) + "\n")

    # Kontrol haritası: kış deniz buzu katmanı üzerinde noktalar
    izg = {"ncols": int(h["ncols"]), "nrows": int(h["nrows"]), "cellsize": h["cellsize"],
           "bati": h["xllcorner"], "kuzey": h["yllcorner"] + h["nrows"] * h["cellsize"]}
    png_yaz(CIKTI / "noktalar.png", asc_oku(ERA5_CIKTI / "buz_kis.asc"), izg,
            "Adélie kayıtları (GBIF, 2000–2026)", "Kış deniz buzu (%)", kara, "Blues_r",
            noktalar=[
                (d.decimalLongitude, d.decimalLatitude,
                 dict(s=7, c="0.4", lw=0, label=f"temiz kayıt ({len(d)})")),
                (temsil.decimalLongitude, temsil.decimalLatitude,
                 dict(s=18, c="red", ec="k", lw=0.4, label=f"MaxEnt noktası ({len(temsil)})")),
            ])

    for a, n, not_ in adimlar:
        print(f"{a:32s} {n:5d}  {not_}")


if __name__ == "__main__":
    main()
