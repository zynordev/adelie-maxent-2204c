import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm

DIR = "/home/halil/adelie-maxent-2204c/maxent/cikti/deneme_2050"
GUNCEL_ASC = os.path.join(DIR, "Pygoscelis_adeliae_avg.asc")
FUTURE_ASC = os.path.join(DIR, "Pygoscelis_adeliae_gelecek_2050_ssp245_avg.asc")
FARK_ASC = os.path.join(DIR, "habitat_degisimi_2050_ssp245.asc")
OUT_PNG = "/home/halil/adelie-maxent-2204c/harita_2050_karsilastirma.png"
OUT_PDF = "/home/halil/adelie-maxent-2204c/harita_2050_karsilastirma.pdf"

def read_asc(path):
    with open(path, 'r') as f:
        meta = {}
        for _ in range(6):
            parts = f.readline().split()
            meta[parts[0]] = float(parts[1])
        data = np.loadtxt(f)
    return meta, data

meta, guncel = read_asc(GUNCEL_ASC)
_, future = read_asc(FUTURE_ASC)
_, fark = read_asc(FARK_ASC)

nodata = -9999.0
guncel = np.ma.masked_values(guncel, nodata)
future = np.ma.masked_values(future, nodata)
fark = np.ma.masked_values(fark, nodata)

# Koordinat sınırları
x_min = meta['xllcorner']
x_max = x_min + meta['ncols'] * meta['cellsize']
y_min = meta['yllcorner']
y_max = y_min + meta['nrows'] * meta['cellsize']
extent = [x_min, x_max, y_min, y_max]

plt.rcParams['font.family'] = 'sans-serif'
fig, axes = plt.subplots(1, 3, figsize=(19, 6.5), dpi=300, sharex=True, sharey=True)
plt.subplots_adjust(wspace=0.15, top=0.86, bottom=0.15, left=0.06, right=0.96)

# Ortak renk paleti (Uygunluk: 0-1)
cmap_suit = plt.cm.Spectral_r

# Panel A: Günümüz
im_a = axes[0].imshow(guncel, cmap=cmap_suit, vmin=0, vmax=1, extent=extent, origin='upper')
axes[0].set_title("(A) Gunumuz Habitat Uygunlugu\n(2000-2025 ERA5 Referansi)", fontsize=12, fontweight='bold', pad=10)
axes[0].set_ylabel("Enlem (Guney Derece)", fontsize=11)
axes[0].set_xlabel("Boylam (Bati Derece)", fontsize=11)
axes[0].grid(True, linestyle='--', alpha=0.3)

# Panel B: 2050 Gelecek
im_b = axes[1].imshow(future, cmap=cmap_suit, vmin=0, vmax=1, extent=extent, origin='upper')
axes[1].set_title("(B) 2050 Gelecek Projeksiyonu\n(IPCC CMIP6 SSP2-4.5 Senaryosu)", fontsize=12, fontweight='bold', pad=10)
axes[1].set_xlabel("Boylam (Bati Derece)", fontsize=11)
axes[1].grid(True, linestyle='--', alpha=0.3)

# Panel C: Değişim / Kayıp-Kazanç
cmap_fark = plt.cm.RdYlGn
norm_fark = BoundaryNorm([-1.0, -0.25, -0.05, 0.05, 0.25, 1.0], cmap_fark.N)
im_c = axes[2].imshow(fark, cmap=cmap_fark, norm=norm_fark, extent=extent, origin='upper')
axes[2].set_title("(C) Iklim Krizinde Habitat Degisimi\n(2050 vs Gunumuz Farki)", fontsize=12, fontweight='bold', pad=10)
axes[2].set_xlabel("Boylam (Bati Derece)", fontsize=11)
axes[2].grid(True, linestyle='--', alpha=0.3)

# Renk çubukları (Colorbars)
cbar_a = fig.colorbar(im_a, ax=axes[0:2], orientation='horizontal', fraction=0.046, pad=0.18, shrink=0.7)
cbar_a.set_label('Habitat Uygunluk Indeksi (0: Uygun Degil -> 1: Cok Yuksek Uygunluk / Koloni)', fontsize=10, fontweight='bold')

cbar_c = fig.colorbar(im_c, ax=axes[2], orientation='horizontal', fraction=0.046, pad=0.18, shrink=0.85)
cbar_c.set_label('Degisim (Kirmizi: Kayip | Gri: Kararli | Yesil: Siginak)', fontsize=10, fontweight='bold')
cbar_c.set_ticks([-0.62, -0.15, 0, 0.15, 0.62])
cbar_c.set_ticklabels(['Yuksek Kayip', 'Hafif Kayip', 'Kararli', 'Hafif Artma', 'Guclu Siginak'])

fig.suptitle("ADELIE PENGUENI (Pygoscelis adeliae) IKLIM DEGISIKLIGI ETKI ANALIZI (MARGUERITE KORFEZI)", 
             fontsize=14, fontweight='bold', y=0.98)

plt.savefig(OUT_PNG, dpi=300, bbox_inches='tight')
plt.savefig(OUT_PDF, dpi=300, bbox_inches='tight')
print("Tamamlandi.")
print("PNG:", OUT_PNG)
print("PDF:", OUT_PDF)
