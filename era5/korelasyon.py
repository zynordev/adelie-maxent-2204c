"""24 katman arasında Pearson korelasyon matrisi.

Kullanım:  .venv/bin/python korelasyon.py

Çıktılar (output/): korelasyon_matrisi.csv, korelasyon_matrisi.png, yuksek_korelasyon.txt (|r| > 0.8)
Hücreler: tüm ızgara hücreleri (MaxEnt'e girecek, kara hücreleri doldurulmuş sürümler).
NOT: Bu script değişken SEÇMEZ; seçim öğrenci ve danışmanındır.
"""
import numpy as np
import pandas as pd

from ayarlar import CIKTI, KATMANLAR
from ortak import asc_oku

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ESIK = 0.8


def main():
    tablo = pd.DataFrame({ad: asc_oku(CIKTI / f"{ad}.asc").ravel() for ad in KATMANLAR})
    assert not tablo.isnull().any().any(), "katmanlarda NoData var"
    r = tablo.corr(method="pearson")
    r.round(4).to_csv(CIKTI / "korelasyon_matrisi.csv")

    satirlar = []
    for i, a in enumerate(KATMANLAR):
        for b in KATMANLAR[i + 1:]:
            if abs(r.loc[a, b]) > ESIK:
                satirlar.append((abs(r.loc[a, b]), f"{a:11s} {b:11s} r = {r.loc[a, b]:+.3f}"))
    satirlar.sort(reverse=True)
    with open(CIKTI / "yuksek_korelasyon.txt", "w") as f:
        f.write(f"|r| > {ESIK} olan katman çiftleri ({len(satirlar)} çift, {len(tablo)} hücre, Pearson)\n")
        f.write("Büyükten küçüğe sıralı. Değişken seçimi öğrenci + danışman tarafından yapılacaktır.\n\n")
        f.write("\n".join(s for _, s in satirlar) + "\n")

    fig, ax = plt.subplots(figsize=(11, 9.5))
    im = ax.imshow(r.values, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(KATMANLAR)), KATMANLAR, rotation=90)
    ax.set_yticks(range(len(KATMANLAR)), KATMANLAR)
    for i in range(len(KATMANLAR)):
        for j in range(len(KATMANLAR)):
            v = r.values[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=5.5,
                    color="white" if abs(v) > 0.6 else "black")
    fig.colorbar(im, ax=ax, label="Pearson r", shrink=0.8)
    ax.set_title(f"Katmanlar arası Pearson korelasyonu ({len(tablo)} hücre)")
    fig.tight_layout()
    fig.savefig(CIKTI / "korelasyon_matrisi.png", dpi=150)
    print(f"{len(satirlar)} çift |r| > {ESIK}")


if __name__ == "__main__":
    main()
