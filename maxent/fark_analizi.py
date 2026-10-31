import os
import numpy as np

DIR = "/home/halil/adelie-maxent-2204c/maxent/cikti/deneme_2050"
GUNCEL_ASC = os.path.join(DIR, "Pygoscelis_adeliae_avg.asc")
FUTURE_ASC = os.path.join(DIR, "Pygoscelis_adeliae_gelecek_2050_ssp245_avg.asc")
FARK_ASC = os.path.join(DIR, "habitat_degisimi_2050_ssp245.asc")

def read_asc(path):
    header = []
    with open(path, 'r') as f:
        for _ in range(6):
            header.append(f.readline())
        data = np.loadtxt(f)
    return header, data

def write_asc(path, header, data):
    with open(path, 'w') as f:
        for line in header:
            f.write(line)
        for row in data:
            f.write(" ".join(f"{val:.6f}" for val in row) + "\n")

h, guncel = read_asc(GUNCEL_ASC)
_, future = read_asc(FUTURE_ASC)

nodata = -9999.0
mask = (guncel != nodata) & (future != nodata)

# Fark = 2050 - Güncel
# Negatif değer = Habitat Kaybı (Azalma)
# Pozitif değer = Habitat Kazancı (Sığınak / Artış)
fark = np.full_like(guncel, nodata)
fark[mask] = future[mask] - guncel[mask]

write_asc(FARK_ASC, h, fark)

val_guncel = guncel[mask]
val_future = future[mask]
val_fark = fark[mask]

azalan = np.sum(val_fark < -0.05)
artan = np.sum(val_fark > 0.05)
kararli = np.sum((val_fark >= -0.05) & (val_fark <= 0.05))
toplam = np.sum(mask)

print("=== 2050 CMIP6 SSP2-4.5 HABİTAT DEĞİŞİM ANALİZİ ===")
print(f"Toplam geçerli model hücresi: {toplam}")
print(f"Ortalama Güncel Uygunluk: {val_guncel.mean():.4f}")
print(f"Ortalama 2050 Uygunluğu: {val_future.mean():.4f}")
print(f"Ortalama Fark: {val_fark.mean():.4f}")
print(f"En Büyük Kayıp: {val_fark.min():.4f}")
print(f"En Büyük Kazanç (Sığınak): {val_fark.max():.4f}")
print("\nDağılım Kategorileri:")
print(f"🔴 Habitat Kaybı Yaşayan Hücreler (< -0.05): {azalan} hücre (%{azalan/toplam*100:.1f})")
print(f"⚪ Kararlı / Değişmeyen Hücreler (±0.05): {kararli} hücre (%{kararli/toplam*100:.1f})")
print(f"🟢 Sığınak / Uygunluğu Artan Hücreler (> +0.05): {artan} hücre (%{artan/toplam*100:.1f})")
