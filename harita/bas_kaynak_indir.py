"""Download the same versioned SCAR vector sources used in the local study."""
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib
import html
import json
from pathlib import Path
import re
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
SOURCES={'rock':'815525ca-cefe-4fbf-9224-3ee784e7de4e',
         'coast':'7d6793c2-2513-4752-8f37-11db5b791fb5'}


def retrieve(kind,uid,out):
    target=out/f'{kind}_v7_11.shp.zip'
    if target.exists():raise FileExistsError('Source already exists')
    metadata=f'https://data.bas.ac.uk/records/{uid}.html'
    with urllib.request.urlopen(metadata,timeout=30) as r:page=r.read().decode()
    links=list(dict.fromkeys(html.unescape(s) for s in re.findall(r'https://ramadda[^\s"<>]+',page)))
    urls=[s for s in links if '.shp.zip?' in s]
    if len(urls)!=1:raise ValueError('Unique versioned shapefile link required')
    digest=hashlib.sha256();size=0
    with urllib.request.urlopen(urls[0],timeout=60) as response, target.with_suffix('.part').open('wb') as f:
        while chunk:=response.read(1024*1024):
            size+=len(chunk)
            if size>200*1024*1024:raise ValueError('Source exceeds 200 MiB budget')
            f.write(chunk);digest.update(chunk)
    target.with_suffix('.part').rename(target)
    return {'kind':kind,'doi':f'10.5285/{uid}','url':urls[0],
            'file':target.name,'bytes':size,'sha256':digest.hexdigest()}


def main():
    out=ROOT/'harita/veri_ham/revizyon_20261112';out.mkdir(parents=True,exist_ok=True)
    rows=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        jobs={pool.submit(retrieve,k,u,out):k for k,u in SOURCES.items()}
        for done in as_completed(jobs):
            try:rows.append(done.result())
            except Exception as e:rows.append({'kind':jobs[done],'status':'failed','type':type(e).__name__})
            (out/'receipts.json').write_text(json.dumps(rows,indent=2)+'\n')
            print(json.dumps({'kind':jobs[done],'finished':True}),flush=True)


if __name__=='__main__':main()
