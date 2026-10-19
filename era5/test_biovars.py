"""biovars() için elle hesaplanmış sentetik 12 aylık örnekle test.

Çalıştırma:  .venv/bin/python test_biovars.py

Örnek veri:
  tmin = 0, 1, ..., 11           tmax = tmin + 10       → tavg = 5, 6, ..., 16
  prec = 5, 0, 0, 0, 10, 20, 30, 0, 0, 0, 0, 40          (toplam 105, ortalama 8.75)

Çeyrek (3 ay) yağış toplamları, pencere başlangıç ayına göre (0 = Ocak):
  0:5  1:0  2:10  3:30  4:60  5:50  6:30  7:0  8:0  9:40  10:45  11:45
  → en yağışlı = pencere 4 (May-Haz-Tem, 60), en kurak = pencere 1 (ilk 0)
Çeyrek ortalama sıcaklıkları:
  pencere 4: (9+10+11)/3 = 10      pencere 1: (6+7+8)/3 = 7
  en sıcak = pencere 9: (14+15+16)/3 = 15   en soğuk = pencere 0: (5+6+7)/3 = 6
"""
import math

import numpy as np

from biovars import biovars

tmin = np.arange(12.0)
tmax = tmin + 10
prec = np.array([5, 0, 0, 0, 10, 20, 30, 0, 0, 0, 0, 40], dtype=float)

beklenen = {
    "bio1": 10.5,                               # mean(5..16)
    "bio2": 10.0,                               # tmax - tmin hep 10
    "bio3": 10 / 21 * 100,                      # bio2 / bio7 * 100
    "bio4": math.sqrt(13) * 100,                # 1..12'nin örneklem varyansı = 13
    "bio5": 21.0,                               # max tmax
    "bio6": 0.0,                                # min tmin
    "bio7": 21.0,
    "bio8": 10.0,                               # en yağışlı çeyreğin sıcaklığı
    "bio9": 7.0,                                # en kurak çeyreğin sıcaklığı
    "bio10": 15.0,
    "bio11": 6.0,
    "bio12": 105.0,
    "bio13": 40.0,
    "bio14": 0.0,
    "bio15": math.sqrt(2106.25 / 11) / (1 + 8.75) * 100,  # sapma kareleri toplamı = 2106.25
    "bio16": 60.0,
    "bio17": 0.0,
    "bio18": 40.0,                              # en sıcak çeyreğin (9) yağışı
    "bio19": 5.0,                               # en soğuk çeyreğin (0) yağışı
}


def test_tek_hucre():
    sonuc = biovars(tmin, tmax, prec)
    for ad, deger in beklenen.items():
        assert math.isclose(float(sonuc[ad]), deger, rel_tol=1e-9, abs_tol=1e-9), (ad, float(sonuc[ad]), deger)


def test_izgara():
    """Aynı örnek 2x3'lük bir ızgaraya kopyalanınca her hücre aynı sonucu vermeli."""
    def izgara(a):
        return np.broadcast_to(a[:, None, None], (12, 2, 3))
    sonuc = biovars(izgara(tmin), izgara(tmax), izgara(prec))
    for ad, deger in beklenen.items():
        assert sonuc[ad].shape == (2, 3)
        assert np.allclose(sonuc[ad], deger), ad


def test_hucre_bazli_secim():
    """İki hücrede en yağışlı çeyrek farklıysa Bio8 her hücre için kendi çeyreğinden gelmeli."""
    p2 = np.roll(prec, 3)                       # en yağışlı çeyrek 3 ay kayar → pencere 7: (12+13+14)/3 = 13
    sonuc = biovars(np.stack([tmin, tmin], 1), np.stack([tmax, tmax], 1), np.stack([prec, p2], 1))
    assert np.allclose(sonuc["bio8"], [10.0, 13.0])


if __name__ == "__main__":
    test_tek_hucre()
    test_izgara()
    test_hucre_bazli_secim()
    print("Tüm testler geçti (19 değişken).")
