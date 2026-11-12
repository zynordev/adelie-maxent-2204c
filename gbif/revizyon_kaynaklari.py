"""Download public, versionable occurrence/census sources without credentials."""
import csv
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[1]
SOURCES={
    'gbif_original.zip':'https://api.gbif.org/v1/occurrence/download/request/0034792-260928105237408.zip',
    'mapppd_all_counts.csv':'https://penguinmap.com/mapppd/DownloadAll',
}


def main():
    out=ROOT/'gbif/veri_ham/revizyon_20261112'
    out.mkdir(parents=True,exist_ok=True)
    receipts=[]
    for name,url in SOURCES.items():
        target=out/name
        if target.exists():
            receipts.append({'file':name,'url':url,'status':'existing_snapshot_preserved',
                'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size})
            continue
        try:
            request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (research data retrieval)'})
            with urllib.request.urlopen(request,timeout=40) as response:
                payload=response.read(20*1024*1024+1)
                if len(payload)>20*1024*1024:
                    raise ValueError('Payload exceeds 20 MiB')
                if name.endswith('.csv') and b'<html' in payload[:1000].lower():
                    raise ValueError('Expected CSV, received HTML')
            target.write_bytes(payload)
            receipts.append({'file':name,'url':url,'sha256':hashlib.sha256(payload).hexdigest(),
                             'bytes':len(payload),'status':'downloaded'})
        except Exception as exc:
            receipts.append({'file':name,'url':url,'status':'failed','error_type':type(exc).__name__})
    (out/'receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
    print(json.dumps(receipts,indent=2))


if __name__=='__main__':
    main()
