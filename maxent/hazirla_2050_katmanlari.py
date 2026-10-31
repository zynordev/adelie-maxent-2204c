#!/usr/bin/env python3
"""
IPCC CMIP6 SSP2-4.5 Senaryosu ile 2050 Gelecek İklim Katmanlarını Üretme
Kaynaklar: IPCC AR6 Chapter 9 & Cimino vd. 2016 (Marguerite Körfezi / WAP)

Değişken Dönüşümleri (2000-2025 Referans -> 2050):
1. buz_yillik : Deniz buzu örtüsünde %20 bölgesel azalma (Delta = * 0.80)
2. sst_yillik : Deniz yüzeyi sıcaklığında +0.8 °C ısınma (Delta = + 0.8 °C)
3. bio18      : En sıcak çeyrek yağışında %15 artış (sıvı yağış / civciv erimesi) (Delta = * 1.15)
4. kaya       : Buzsuz kaya alanları jeolojik olarak sabit (Delta = 0.0)
"""

import os
import shutil
import numpy as np

KAYNAK_DIR = "/home/halil/adelie-maxent-2204c/maxent/girdi/katmanlar"
HEDEF_DIR = "/home/halil/adelie-maxent-2204c/maxent/girdi/gelecek_2050_ssp245"

os.makedirs(HEDEF_DIR, exist_ok=True)

def read_asc(filepath):
    header = []
    with open(filepath, 'r') as f:
        for _ in range(6):
            header.append(f.readline())
        data = np.loadtxt(f)
    return header, data

def write_asc(filepath, header, data):
    with open(filepath, 'w') as f:
        for line in header:
            f.write(line)
        for row in data:
            f.write(" ".join(f"{val:.6f}" for val in row) + "\n")

print("2050 CMIP6 SSP2-4.5 katmanları hazırlanıyor...")

# 1. Kaya (Sabit)
h_kaya, d_kaya = read_asc(os.path.join(KAYNAK_DIR, "kaya.asc"))
write_asc(os.path.join(HEDEF_DIR, "kaya.asc"), h_kaya, d_kaya)
print("✔ kaya.asc hazırlandı (sabit)")

# 2. Deniz Buzu (buz_yillik): %20 azalma
h_buz, d_buz = read_asc(os.path.join(KAYNAK_DIR, "buz_yillik.asc"))
nodata = -9999.0
mask_buz = (d_buz != nodata)
d_buz_2050 = np.copy(d_buz)
d_buz_2050[mask_buz] = np.clip(d_buz[mask_buz] * 0.80, 0.0, 100.0)
write_asc(os.path.join(HEDEF_DIR, "buz_yillik.asc"), h_buz, d_buz_2050)
print(f"✔ buz_yillik.asc hazırlandı (Ortalama buz: {d_buz[mask_buz].mean():.1f}% -> {d_buz_2050[mask_buz].mean():.1f}%)")

# 3. Deniz Yüzeyi Sıcaklığı (sst_yillik): +0.8 °C ısınma
h_sst, d_sst = read_asc(os.path.join(KAYNAK_DIR, "sst_yillik.asc"))
mask_sst = (d_sst != nodata)
d_sst_2050 = np.copy(d_sst)
d_sst_2050[mask_sst] = d_sst[mask_sst] + 0.80
write_asc(os.path.join(HEDEF_DIR, "sst_yillik.asc"), h_sst, d_sst_2050)
print(f"✔ sst_yillik.asc hazırlandı (Ortalama SST: {d_sst[mask_sst].mean():.2f}°C -> {d_sst_2050[mask_sst].mean():.2f}°C)")

# 4. Yaz Yağışı (bio18): %15 artış
h_bio, d_bio = read_asc(os.path.join(KAYNAK_DIR, "bio18.asc"))
mask_bio = (d_bio != nodata)
d_bio_2050 = np.copy(d_bio)
d_bio_2050[mask_bio] = d_bio[mask_bio] * 1.15
write_asc(os.path.join(HEDEF_DIR, "bio18.asc"), h_bio, d_bio_2050)
print(f"✔ bio18.asc hazırlandı (Ortalama bio18: {d_bio[mask_bio].mean():.1f}mm -> {d_bio_2050[mask_bio].mean():.1f}mm)")

print("\nTüm 2050 katmanları başarıyla üretildi:")
print(f"Konum: {HEDEF_DIR}")
