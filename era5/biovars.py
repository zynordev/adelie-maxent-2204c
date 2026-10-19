"""Bio1–Bio19 hesaplama fonksiyonu.

R paketindeki `dismo::biovars` ile birebir aynı tanımlar (WorldClim bioclim tanımları):
https://www.worldclim.org/data/bioclim.html

Girdi dizilerinin İLK ekseni 12 ay olmalıdır (ör. şekil (12, enlem, boylam)).
Sıcaklıklar °C, yağış mm/ay. Çıktıda ×10 ölçekleme yoktur.
"""
import numpy as np


def ceyrekler(x):
    """Ardışık 3 aylık 12 pencere (Ara-Oca-Şub gibi yıl sonundan başa saranlar dahil).

    i. pencere = i, i+1, i+2 numaralı aylar. Çıktı ekseni 0: pencere başlangıç ayı.
    Toplamı döndürür; ortalama için 3'e bölün.
    """
    return x + np.roll(x, -1, axis=0) + np.roll(x, -2, axis=0)


def _sec(dizi, indis):
    """dizi[indis[...], ...] — her hücre için ayrı pencere seçimi."""
    return np.take_along_axis(dizi, indis[np.newaxis, ...], axis=0)[0]


def biovars(tmin, tmax, prec):
    """19 biyoklimatik değişkeni sözlük olarak döndürür: {'bio1': dizi, ...}."""
    tmin, tmax, prec = (np.asarray(a, dtype=float) for a in (tmin, tmax, prec))
    assert tmin.shape[0] == tmax.shape[0] == prec.shape[0] == 12, "ilk eksen 12 ay olmalı"

    tavg = (tmax + tmin) / 2

    b = {}
    b["bio1"] = tavg.mean(axis=0)
    b["bio2"] = (tmax - tmin).mean(axis=0)
    b["bio4"] = tavg.std(axis=0, ddof=1) * 100          # örneklem sd (n-1), dismo gibi
    b["bio5"] = tmax.max(axis=0)
    b["bio6"] = tmin.min(axis=0)
    b["bio7"] = b["bio5"] - b["bio6"]
    b["bio3"] = b["bio2"] / b["bio7"] * 100

    b["bio12"] = prec.sum(axis=0)
    b["bio13"] = prec.max(axis=0)
    b["bio14"] = prec.min(axis=0)
    # dismo: cv(prec + 1) = sd(prec) / (1 + mean(prec)) * 100
    b["bio15"] = prec.std(axis=0, ddof=1) / (1 + prec.mean(axis=0)) * 100

    yagis_c = ceyrekler(prec)            # çeyrek yağış toplamları
    sicak_c = ceyrekler(tavg) / 3        # çeyrek ortalama sıcaklıkları

    # argmax/argmin eşitlikte ilk pencereyi seçer (R'deki which.max/which.min gibi)
    en_yagisli = yagis_c.argmax(axis=0)
    en_kurak = yagis_c.argmin(axis=0)
    en_sicak = sicak_c.argmax(axis=0)
    en_soguk = sicak_c.argmin(axis=0)

    b["bio8"] = _sec(sicak_c, en_yagisli)
    b["bio9"] = _sec(sicak_c, en_kurak)
    b["bio10"] = sicak_c.max(axis=0)
    b["bio11"] = sicak_c.min(axis=0)
    b["bio16"] = yagis_c.max(axis=0)
    b["bio17"] = yagis_c.min(axis=0)
    b["bio18"] = _sec(yagis_c, en_sicak)
    b["bio19"] = _sec(yagis_c, en_soguk)

    return {f"bio{i}": b[f"bio{i}"] for i in range(1, 20)}
