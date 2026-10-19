"""GBIF'ten Adélie pengueni bulunuş kayıtlarını resmi indirme API'siyle indirir.

Kullanım:  ../era5/.venv/bin/python indir_gbif.py
Gereken:   ~/.gbif_sifre  (yalnızca GBIF şifresi, izin 600 — öğrenci kendisi oluşturur)

Sitedeki "Download → Simple" ile aynı ürünü (SIMPLE_CSV + DOI) üretir. Kullanılan filtre
'sorgu.json' dosyasına yazılır; raporda indirmenin hangi sorguyla yapıldığı tam olarak gösterilebilir.

- Yeniden başlatılabilir: istek bir kez gönderilir, anahtarı 'indirme_bilgisi.json'a yazılır;
  script tekrar çalışırsa yeni istek açmaz, mevcut indirmeyi bekler/indirir.
- Şifre hiçbir yere yazılmaz/yazdırılmaz.
"""
import json
import time
from pathlib import Path

import requests

KULLANICI = "halilerdemyanik"
SIFRE_DOSYASI = Path.home() / ".gbif_sifre"
API = "https://api.gbif.org/v1/occurrence/download"

KOK = Path(__file__).resolve().parent
HAM = KOK / "ham"
BILGI = KOK / "indirme_bilgisi.json"

# GBIF Backbone Taxonomy — taxonKey 2481663 = Pygoscelis adeliae (Hombron & Jacquinot, 1841)
BACKBONE = "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"
TAKSON = "2481663"

# İklim katmanlarının (era5/output) tam sınırı; köşeler saat yönünün tersine (GBIF kuralı)
ALAN_WKT = "POLYGON((-73.125 -70.625,-63.875 -70.625,-63.875 -65.875,-73.125 -65.875,-73.125 -70.625))"

SORGU = {
    "format": "SIMPLE_CSV",
    "sendNotification": False,
    "checklistKey": BACKBONE,
    "predicate": {
        "type": "and",
        "predicates": [
            {"type": "equals", "key": "TAXON_KEY", "value": TAKSON},
            {"type": "greaterThanOrEquals", "key": "YEAR", "value": "2000"},
            {"type": "lessThanOrEquals", "key": "YEAR", "value": "2026"},
            {"type": "equals", "key": "HAS_COORDINATE", "value": "true"},
            {"type": "equals", "key": "HAS_GEOSPATIAL_ISSUE", "value": "false"},
            {"type": "equals", "key": "OCCURRENCE_STATUS", "value": "PRESENT"},
            {"type": "within", "geometry": ALAN_WKT},
        ],
    },
}


def sifre():
    assert SIFRE_DOSYASI.exists(), f"{SIFRE_DOSYASI} yok — öğrencinin oluşturması gerekiyor"
    assert SIFRE_DOSYASI.stat().st_mode & 0o077 == 0, f"{SIFRE_DOSYASI} izinleri 600 olmalı"
    return SIFRE_DOSYASI.read_text().strip()


def istek_gonder():
    yanit = requests.post(f"{API}/request", json={"creator": KULLANICI, **SORGU},
                          auth=(KULLANICI, sifre()), timeout=60)
    if yanit.status_code == 401:
        raise SystemExit("GBIF kimlik doğrulaması başarısız: kullanıcı adı/şifre yanlış olabilir")
    yanit.raise_for_status()
    return yanit.text.strip()


def main():
    HAM.mkdir(parents=True, exist_ok=True)
    (KOK / "sorgu.json").write_text(json.dumps(SORGU, indent=2, ensure_ascii=False) + "\n")

    bilgi = json.loads(BILGI.read_text()) if BILGI.exists() else {}
    if "anahtar" not in bilgi:
        bilgi["anahtar"] = istek_gonder()
        bilgi["istek_tarihi"] = time.strftime("%Y-%m-%d %H:%M")
        BILGI.write_text(json.dumps(bilgi, indent=2, ensure_ascii=False) + "\n")
        print("istek gönderildi, anahtar:", bilgi["anahtar"])

    while True:
        durum = requests.get(f"{API}/{bilgi['anahtar']}", timeout=60).json()
        print(time.strftime("%H:%M:%S"), durum["status"])
        if durum["status"] in ("SUCCEEDED", "FAILED", "KILLED", "CANCELLED"):
            break
        time.sleep(30)
    if durum["status"] != "SUCCEEDED":
        raise SystemExit(f"GBIF indirmesi başarısız: {durum['status']}")

    bilgi.update({
        "doi": durum.get("doi"),
        "kayit_sayisi": durum.get("totalRecords"),
        "veri_seti_sayisi": durum.get("numberDatasets"),
        "olusturma": durum.get("created"),
        "baglanti": durum.get("downloadLink"),
        "atif": f"GBIF.org ({durum.get('created', '')[:10]}) GBIF Occurrence Download https://doi.org/{durum.get('doi')}",
    })
    BILGI.write_text(json.dumps(bilgi, indent=2, ensure_ascii=False) + "\n")

    hedef = HAM / f"{bilgi['anahtar']}.zip"
    if not hedef.exists():
        with requests.get(durum["downloadLink"], stream=True, timeout=300) as r:
            r.raise_for_status()
            gecici = hedef.with_suffix(".zip.part")
            with open(gecici, "wb") as f:
                for parca in r.iter_content(1 << 20):
                    f.write(parca)
            gecici.rename(hedef)
    print(f"indi: {hedef.name}  ({bilgi['kayit_sayisi']} kayıt, {bilgi['veri_seti_sayisi']} veri seti)")
    print("DOI:", bilgi["doi"])
    print("Atıf:", bilgi["atif"])


if __name__ == "__main__":
    main()
