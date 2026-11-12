"""Census evidence inventory; never interprets arbitrary land points as nests."""
import csv
import hashlib
import html
import json
from pathlib import Path
import re
import sys

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'maxent'))
from izgara import read_grid
from revizyon_denetimi import dump,table


def main():
    path=ROOT/'gbif/veri_ham/revizyon_20261112/mapppd_all_counts.csv'
    out=ROOT/'gbif/temiz/revizyon_20261112'
    if out.exists():raise FileExistsError('Fresh census inventory required')
    out.mkdir(parents=True)
    all_rows=list(csv.DictReader(path.open()))
    g,_=read_grid(ROOT/'maxent/girdi/katmanlar/kaya.asc')
    west,south,east,north=g.extent
    local=[]
    for a in all_rows:
        x,y=float(a['longitude_epsg_4326']),float(a['latitude_epsg_4326'])
        if a['common_name']!='adelie penguin' or not (west<=x<east and south<=y<north):continue
        count=float(a['penguin_count']) if a['penguin_count'] else None
        year=int(a['year']) if a['year'] else None
        eligible=bool(year and 2000<=year<=2025 and count and count>0 and a['count_type']=='nests')
        row=g.nrows-1-int(np.floor((y-south)/g.cellsize));col=int(np.floor((x-west)/g.cellsize))
        local.append(dict(site_id=a['site_id'],site_name=a['site_name'],longitude=x,latitude=y,
            year=year,penguin_count=count,count_type=a['count_type'],eligible_nest_census=eligible,
            row=row,col=col,reference=html.unescape(re.sub('<[^>]+>','',a['reference']))))
    table(out/'mapppd_local_censuses.csv',local)
    eligible=[r for r in local if r['eligible_nest_census']]
    representatives={}
    for r in sorted(eligible,key=lambda a:(-a['year'],a['site_id'])):
        representatives.setdefault((r['row'],r['col']),r)
    table(out/'mapppd_colony_grid_representatives.csv',list(representatives.values()))
    summary={'source':'MAPPPD all-counts public CSV snapshot',
        'source_url':'https://penguinmap.com/mapppd/DownloadAll',
        'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'raw_census_rows_global':len(all_rows),'local_census_rows_all_years':len(local),
        'local_sites_all_years':len(set(r['site_id'] for r in local)),
        'eligible_positive_nest_censuses_2000_2025':len(eligible),
        'eligible_sites':len(set(r['site_id'] for r in eligible)),
        'eligible_grid_cells':len(representatives),
        'same_cell_sites_not_independent':True,
        'independent_validation_status':'unestablished; GBIF source overlap must be checked',
        'decision_needed':'broader calibration domain for colony model or retain local occurrence/methodological scope',
        'all_species_target_group_background':'not applied to mixed GBIF records; sampling processes differ'}
    dump(out/'colony_summary.json',summary);print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
