"""Eşdeğerlik kontrolü: saatlik veriden bizim hesapladığımız günlük maks sıcaklık
= CDS'in 'derived-era5-single-levels-daily-statistics' ürünündeki günlük maks sıcaklık mı?

Kullanım:  .venv/bin/python saatlik_gunluk_karsilastir.py

veri_ham/cds_gunluk_karsilastirma/ altında CDS'ten inmiş günlük maks dosyaları (2000, 2001) bulunur.
Fark 0 ise saatlik veriye geçmek sonucu değiştirmez (docs/KARARLAR.md K-013).
"""
import numpy as np

from ayarlar import HAM_VERI
from bioclim_hesapla import gunluk_uc_degerler
from ortak import ac


def main():
    klasor = HAM_VERI / "cds_gunluk_karsilastirma"
    for dosya in sorted(klasor.glob("t2m_tmax_*.nc")):
        yil = int(dosya.stem.split("_")[-1])
        if not (HAM_VERI / "saatlik" / f"t2m_saatlik_{yil}.nc").exists():
            print(f"{yil}: saatlik dosya yok, atlandı")
            continue
        bizim, _ = gunluk_uc_degerler(yil)
        cds = ac(dosya)
        assert bizim.shape == cds.shape, (bizim.shape, cds.shape)
        fark = np.abs(bizim.values - cds.values)
        print(f"{yil}: {cds.sizes['zaman']} gün × {cds.sizes['latitude'] * cds.sizes['longitude']} hücre  "
              f"en büyük fark = {fark.max():.6f} K   birebir aynı değer oranı = {(fark == 0).mean():.4f}")


if __name__ == "__main__":
    main()
