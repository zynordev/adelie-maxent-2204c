"""Prepare census-only colony candidates and two explicit background designs.

The rectangle is a download envelope. Suitable rocky coastal cells and surveyed
Pygoscelis sites are alternative background supports, not observed absences.
"""
import argparse
import csv
from pathlib import Path
import sqlite3
import subprocess

import numpy as np
from pyproj import Transformer
import shapely
from shapely.geometry import box
from shapely.ops import transform, unary_union
from shapely.strtree import STRtree
import xarray as xr

from izgara import Grid,write_grid,aligned
from revizyon_denetimi import ROOT,gpkg_geometry,dump,table
from revizyon_katmanlari import nearest_index,BREEDING


def vector_subset(source,region,out):
    bounds=region.bounds
    command=['ogr2ogr','-f','GPKG',str(out),f'/vsizip/{source.resolve()}',
             '-nln','features','-spat',*[str(v) for v in bounds],'-clipsrc',region.wkt]
    result=subprocess.run(command,capture_output=True,text=True,timeout=300)
    if result.returncode:raise RuntimeError('SCAR vector subsetting failed')
    with sqlite3.connect(out) as c:
        columns=[a[1] for a in c.execute('pragma table_info(features)')]
        fields='geom,surface' if 'surface' in columns else 'geom'
        rows=list(c.execute('select '+fields+' from features'))
    return [(shapely.make_valid(gpkg_geometry(r[0])),r[1] if len(r)>1 else 'rock') for r in rows]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--raw',type=Path,default=ROOT/'era5/veri_ham/peninsula_20261112/marine_monthly_2000_2025.nc')
    p.add_argument('--output',type=Path,default=ROOT/'maxent/girdi/koloni_20261112')
    p.add_argument('--geometry-only',action='store_true',help='Prepare only source SCAR geometry while climate job is queued')
    p.add_argument('--geometry-directory',type=Path,help='Reuse aligned SCAR fractions, never climate placeholders')
    p.add_argument('--area',type=float,nargs=4,default=[-60,-78,-74,-53])
    args=p.parse_args()
    if args.output.exists():raise FileExistsError('Fresh colony dataset required')
    if not args.geometry_only and not args.raw.is_file():raise FileNotFoundError('ERA5 marine source is not ready yet')
    args.output.mkdir(parents=True)
    if args.geometry_only:
        north,west,south,east=args.area
        lat=np.arange(north,south-.125,-.25);lon=np.arange(west,east+.125,.25)
    else:
        with xr.open_dataset(args.raw,engine='h5netcdf') as f:d=f.load()
        if d.sst.attrs.get('GRIB_paramId')!=34 or d.siconc.attrs.get('GRIB_paramId')!=31:
            raise ValueError('Marine source identity mismatch')
        if d.sst.attrs.get('units')!='K' or d.siconc.attrs.get('units')!='(0 - 1)':
            raise ValueError('Marine source unit mismatch')
        expected=np.arange('2000-01','2026-01',dtype='datetime64[M]')
        if not np.array_equal(d.valid_time.values.astype('datetime64[M]'),expected):
            raise ValueError('Missing or repeated source months')
        lat,lon=d.latitude.values,d.longitude.values
    if not np.allclose(np.diff(lat),-.25) or not np.allclose(np.diff(lon),.25):raise ValueError('Grid alignment')
    grid=Grid(len(lon),len(lat),float(lon.min()-.125),float(lat.min()-.125),.25)
    west,south,east,north=grid.extent
    ll_to_polar=Transformer.from_crs(4326,3031,always_xy=True).transform
    polar_to_equal=Transformer.from_crs(3031,
        '+proj=laea +lat_0=-90 +lon_0=0 +datum=WGS84 +units=m',always_xy=True).transform
    ll_to_equal=Transformer.from_crs(4326,
        '+proj=laea +lat_0=-90 +lon_0=0 +datum=WGS84 +units=m',always_xy=True).transform
    region=transform(ll_to_polar,box(west,south,east,north).segmentize(.05))
    source=ROOT/'harita/veri_ham/revizyon_20261112'
    coast=[] if args.geometry_directory else vector_subset(source/'coast_v7_11.shp.zip',region,args.output/'coast_subset.gpkg')
    rocks=[] if args.geometry_directory else vector_subset(source/'rock_v7_11.shp.zip',region,args.output/'rock_subset.gpkg')
    geometry={
        'rock':[transform(polar_to_equal,g) for g,_ in rocks if not g.is_empty],
        'land':[transform(polar_to_equal,g.simplify(50,preserve_topology=True)) for g,k in coast if k=='land' and not g.is_empty],
        'shelf':[transform(polar_to_equal,g.simplify(50,preserve_topology=True)) for g,k in coast if k!='land' and not g.is_empty],
    }
    trees={k:STRtree(v) for k,v in geometry.items()}
    fractions={k:np.zeros((grid.nrows,grid.ncols)) for k in geometry}
    xx,yy=np.meshgrid(lon,lat)
    if args.geometry_directory:
        fractions={k:aligned(grid,args.geometry_directory/f'{k}_fraction.asc') for k in geometry}
    for r in range(0 if args.geometry_directory else grid.nrows):
        for c in range(grid.ncols):
            cell=transform(ll_to_equal,box(xx[r,c]-.125,yy[r,c]-.125,xx[r,c]+.125,yy[r,c]+.125).segmentize(.025))
            for kind,tree in trees.items():
                candidates=tree.query(cell,predicate='intersects')
                if len(candidates):
                    intersection=unary_union([geometry[kind][int(i)].intersection(cell) for i in candidates])
                    fractions[kind][r,c]=intersection.area/cell.area
        if r%10==0:print(f'geometry rows {r+1}/{grid.nrows}',flush=True)
    for k,a in fractions.items():write_grid(args.output/f'{k}_fraction.asc',grid,a)
    if args.geometry_only:
        dump(args.output/'geometry.json',{'area_NWSE':args.area,'climate_fields_created':False,
             'source':'SCAR ADD v7.11 rock/coast','coast_simplification_m':50,'rock_simplification_m':0})
        print('SCAR geometry ready; no climate placeholders created',flush=True)
        return
    norm=d.astype({'sst':'float64','siconc':'float64'}).groupby('valid_time.month').mean('valid_time',skipna=False)
    sst=norm.sst.values-273.15;ice=norm.siconc.values*100
    valid=np.isfinite(sst).all(0)&np.isfinite(ice).all(0)
    donor,dist=nearest_index(yy,xx,yy,xx,valid)
    filled={name:a.reshape(12,-1)[:,donor.ravel()].reshape(a.shape) for name,a in [('sst',sst),('ice',ice)]}
    features={
        'kaya':100*fractions['rock'],
        'buz_breeding':filled['ice'][np.array(BREEDING)-1].mean(0),
        'buz_kis':filled['ice'][np.array([6,7,8])-1].mean(0),
        'sst_breeding':filled['sst'][np.array(BREEDING)-1].mean(0),
    }
    for name,a in features.items():write_grid(args.output/'current'/f'{name}.asc',grid,a)
    write_grid(args.output/'marine_donor_distance_km.asc',grid,dist)
    # A priori marine-data support and rock/shelf screen; no response values used.
    support=(fractions['rock']>0)&(fractions['shelf']<.5)&(dist<=50)
    write_grid(args.output/'rocky_coastal_support.asc',grid,support.astype(float))
    raw=list(csv.DictReader((ROOT/'gbif/veri_ham/revizyon_20261112/mapppd_all_counts.csv').open()))
    candidates=[];survey=np.zeros_like(support);focal={};excluded=[]
    for a in raw:
        if a['common_name'] not in ['adelie penguin','gentoo penguin','chinstrap penguin']:continue
        if not a['year'] or not 2000<=int(a['year'])<=2025:continue
        if a['count_type']!='nests' or not a['penguin_count'] or float(a['penguin_count'])<=0:continue
        x,y=float(a['longitude_epsg_4326']),float(a['latitude_epsg_4326'])
        if not (west<=x<east and south<=y<north):continue
        r=grid.nrows-1-int(np.floor((y-south)/.25));c=int(np.floor((x-west)/.25))
        record=dict(a,row=r,col=c,support_valid=bool(support[r,c]))
        candidates.append(record)
        if not support[r,c]:excluded.append(record);continue
        survey[r,c]=True
        if a['common_name']=='adelie penguin':
            key=r,c
            if key not in focal or int(a['year'])>int(focal[key]['year']):focal[key]=record
    write_grid(args.output/'target_group_support.asc',grid,survey.astype(float))
    table(args.output/'census_evidence.csv',candidates)
    table(args.output/'excluded_censuses.csv',excluded)
    table(args.output/'colony_samples.csv',[
        dict(species='Pygoscelis_adeliae',longitude=float(xx[r,c]),latitude=float(yy[r,c]),
             sample_id=f'MAPPPD:{a["site_id"]}',site_id=a['site_id'],last_census_year=a['year'],
             row=r,col=c) for (r,c),a in sorted(focal.items())])
    dump(args.output/'definitions.json',{
        'target':'positive breeding-nest census occurrence footprint 2000-2025; not colony abundance',
        'download_rectangle_NWSE':[float(lat.max()),float(lon.min()),float(lat.min()),float(lon.max())],
        'report_focus':'Marguerite Bay original rectangle',
        'training_presence_cells':len(focal),'rocky_coastal_background_cells':int(support.sum()),
        'target_group_background_cells':int(survey.sum()),'excluded_nest_census_rows':len(excluded),
        'background_1':'uniform rocky coastal cells, shelf fraction <.5, marine donor <=50 km',
        'background_2':'Pygoscelis positive nest-census cells; includes focal cells, not true absences',
        'climate_native_grid_spacing_km':31,'output_grid_degrees':.25,
        'coast_simplification_m':50,'rock_simplification_m':0,
        'sst_physical_qc_resolved':False,'daily_phenology_used':False,
        'predictor_sets':{'colony_ice':['kaya','buz_breeding','buz_kis'],
                          'colony_sst_sensitivity':['kaya','buz_breeding','sst_breeding']},
        'main_candidate':'colony_ice; SST sensitivity flagged, no final winner selected',
        'future_rock_assumption':'static substrate, not prediction of ice-free land emergence'})
    print(f'colony presence cells {len(focal)}, coastal cells {support.sum()}, survey cells {survey.sum()}')


if __name__=='__main__':main()
