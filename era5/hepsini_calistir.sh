#!/usr/bin/env bash
# indir.py bitince hesaplama zincirini sırayla çalıştırır; çıktı: hesaplama.log
# Kullanım:  setsid nohup ./hepsini_calistir.sh >/dev/null 2>&1 &
set -u
cd "$(dirname "$0")"
LOG=hesaplama.log
PY=.venv/bin/python

echo "=== $(date '+%F %T') indir.py'nin bitmesi bekleniyor" >> "$LOG"
while pgrep -f 'python indir.py' >/dev/null; do sleep 60; done

n=$(ls veri_ham/saatlik/t2m_saatlik_*.nc 2>/dev/null | wc -l)
echo "=== $(date '+%F %T') indir.py bitti; saatlik dosya: $n/26" >> "$LOG"
if [ "$n" -ne 26 ]; then
    echo "!!! eksik dosya var, hesaplama başlatılmadı (indir.py'yi tekrar çalıştırın)" >> "$LOG"
    exit 1
fi

for adim in test_biovars.py saatlik_gunluk_karsilastir.py denizel_hesapla.py bioclim_hesapla.py korelasyon.py dogrula.py; do
    echo "=== $(date '+%F %T') $adim" >> "$LOG"
    if ! $PY "$adim" >> "$LOG" 2>&1; then
        echo "!!! $adim başarısız (çıkış kodu $?)" >> "$LOG"
        exit 1
    fi
done
echo "=== $(date '+%F %T') TAMAMLANDI" >> "$LOG"
