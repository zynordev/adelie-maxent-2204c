"""Tüm scriptlerin ortak sabitleri. Bir şey değişecekse yalnızca burası değişir."""
from pathlib import Path

# Çalışma alanı [Kuzey, Batı, Güney, Doğu] — CDS 'area' biçimi (Marguerite Körfezi)
ALAN = [-66.0, -73.0, -70.5, -64.0]

# Dönem (iki uç dahil)
BASLANGIC_YILI = 2000
BITIS_YILI = 2025
YILLAR = list(range(BASLANGIC_YILI, BITIS_YILI + 1))

# ERA5 yerel ızgara aralığı (derece). Yeniden örnekleme yapılmaz.
HUCRE = 0.25

NODATA = -9999

# Klasörler
KOK = Path(__file__).resolve().parent
HAM_VERI = KOK / "veri_ham"          # CDS'ten inen NetCDF dosyaları (dokunulmaz)
ARA = KOK / "ara"                    # Hesaplanmış aylık normaller (ara ürün)
CIKTI = KOK / "output"               # MaxEnt'e girecek katmanlar
CIKTI_HAM = CIKTI / "ham"            # Denizel katmanların doldurulmamış hali

# CDS veri setleri
DS_SAATLIK = "reanalysis-era5-single-levels"
DS_GUNLUK = "derived-era5-single-levels-daily-statistics"   # yalnızca eşdeğerlik kontrolü için (bkz. K-013)
DS_AYLIK = "reanalysis-era5-single-levels-monthly-means"

# Doğrulama noktası: Rothera Araştırma İstasyonu
ROTHERA = {"enlem": -67.57, "boylam": -68.13}

# MaxEnt'e aday katmanlar (değişken SEÇİMİ öğrenci + danışmanındır)
DENIZEL = ["sst_yillik", "sst_yaz", "buz_yillik", "buz_yaz", "buz_kis"]
KARASAL = ["kaya"]   # buzsuz kaya örtüsü, ../kaya/kaya_hesapla.py (SCAR ADD v7.11)
KATMANLAR = [f"bio{i}" for i in range(1, 20)] + DENIZEL + KARASAL
