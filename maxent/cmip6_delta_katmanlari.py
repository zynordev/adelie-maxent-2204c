#!/usr/bin/env python3
"""Documented single-GCM monthly-delta inputs; exploratory, not downscaling.

Consumes verified, regional IPSL climatologies from cmip6_erisim_kontrolu.py.
Preserves original ERA5 grid and inputs. Needs NumPy and GDAL, no network.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from osgeo import gdal
from izgara import read_grid, aligned, write_grid

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'maxent/girdi/cmip6_2041_2060'


def sphere_xyz(latitude,longitude):
    lat,lon=np.deg2rad(latitude),np.deg2rad(longitude)
    return np.stack([np.cos(lat)*np.cos(lon),np.cos(lat)*np.sin(lon),np.sin(lat)],axis=-1)


def nearest_indices(source_lat,source_lon,target_lat,target_lon,valid):
    """Great-circle nearest valid native cell; deterministic ties by flat index."""
    indices=np.flatnonzero(valid.ravel())
    if not len(indices):raise ValueError('No valid native source cells')
    sources=sphere_xyz(source_lat.ravel()[indices],source_lon.ravel()[indices])
    targets=sphere_xyz(target_lat.ravel(),target_lon.ravel())
    dots=np.clip(targets@sources.T,-1,1);chosen=np.argmax(dots,axis=1)
    distance=6371*np.arccos(dots[np.arange(len(chosen)),chosen])
    return indices[chosen].reshape(target_lat.shape),distance.reshape(target_lat.shape)


def warm_quarter_precip(tavg,prec):
    if tavg.shape!=prec.shape or tavg.shape[0]!=12:raise ValueError('Need 12 aligned months')
    if not np.isfinite(tavg).all() or not np.isfinite(prec).all() or (prec<0).any():
        raise ValueError('Invalid monthly climate')
    tq=tavg+np.roll(tavg,-1,0)+np.roll(tavg,-2,0)
    pq=prec+np.roll(prec,-1,0)+np.roll(prec,-2,0)
    quarter=tq.argmax(0)
    return np.take_along_axis(pq,quarter[None],axis=0)[0],quarter


def precipitation_ratio(baseline,future):
    # Refuse poorly supported ratios instead of silently inventing a cap.
    if not np.isfinite(baseline).all() or not np.isfinite(future).all():raise ValueError('Invalid precipitation')
    if np.any(baseline<1) or np.any(future<0):
        raise ValueError('Baseline precipitation <1 mm/month: choose an explicit alternate method')
    return future/baseline


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'maxent/girdi/cmip6_ipsl_ssp245_2041_2060_v1')
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError('Use a fresh output directory')
    inventory_path=SOURCE/'bolgesel_uretim_envanteri.json'
    inventory=json.loads(inventory_path.read_text())
    if not inventory['regional_monthly_fields_complete'] or inventory['source_id']!='IPSL-CM6A-LR':
        raise ValueError('Verified complete regional inputs required')
    expected={f['path']:f['sha256'] for v in inventory['variables'] for f in v['files']}
    sources={}
    used=[inventory_path]
    for name,unit in [('tas','degC'),('pr','mm month-1'),('tos','degC'),('siconc','%')]:
        path=SOURCE/f'IPSL-CM6A-LR_r1i1p1f1/{name}_aylik_klimatoloji.npz'
        key=str(path.relative_to(SOURCE))
        if expected.get(key)!=hashlib.sha256(path.read_bytes()).hexdigest():raise ValueError('Input hash mismatch')
        used.append(path)
        with np.load(path) as src:sources[name]={k:src[k].copy() for k in src.files}
        s=sources[name]
        if str(s['units'])!=unit or not np.array_equal(s['month'],np.arange(1,13)):
            raise ValueError('Units/month identity mismatch')
        valid=(np.isfinite(s['baseline']).all(0)&np.isfinite(s['future']).all(0)
               &(s['baseline_valid_year_count']==26).all(0)&(s['future_valid_year_count']==20).all(0))
        if not valid.any():raise ValueError('No complete 26/20 year native cells')
        s['valid']=valid
    g,kaya=read_grid(ROOT/'maxent/girdi/katmanlar/kaya.asc')
    lon,lat=np.meshgrid(g.xllcorner+(np.arange(g.ncols)+.5)*g.cellsize,
                        g.yllcorner+(g.nrows-np.arange(g.nrows)-.5)*g.cellsize)
    mask_path=ROOT/'era5/ara/kara_maskesi.npy';land=np.load(mask_path)
    if land.shape!=lat.shape:raise ValueError('Land mask shape mismatch')
    sea_index,sea_distance=nearest_indices(lat,lon,lat,lon,~land)
    # Marine anomalies on land follow the already documented nearest ERA5 sea
    # cell convention; never mix land sentinel values into ocean interpolation.
    marine_lat=lat.ravel()[sea_index];marine_lon=lon.ravel()[sea_index]
    mapped={};diagnostics={};indices={}
    for name,s in sources.items():
        targetlat,targetlon=(marine_lat,marine_lon) if name in ('tos','siconc') else (lat,lon)
        index,distance=nearest_indices(s['lat'],s['lon'],targetlat,targetlon,s['valid'])
        if distance.max()>300:raise ValueError('Native source too distant (>300 km)')
        indices[name]=index
        mapped[name]={k:s[k].reshape(12,-1)[:,index.ravel()].reshape(12,g.nrows,g.ncols)
                      for k in ['baseline','future']}
        diagnostics[name]={'unique_native_cells':int(len(np.unique(index))),
                           'nearest_distance_km_min':float(distance.min()),
                           'nearest_distance_km_max':float(distance.max()),
                           'nearest_distance_km_median':float(np.median(distance)),
                           'native_units':str(s['units'])}
    gdal.UseExceptions()
    normals=ROOT/'era5/ara/aylik_normaller.nc'
    def monthly(name):
        ds=gdal.Open(f'NETCDF:"{normals}":{name}')
        if ds is None:raise ValueError('ERA5 monthly normal missing')
        expected_transform=(g.xllcorner,g.cellsize,0,g.extent[3],0,-g.cellsize)
        if not np.allclose(ds.GetGeoTransform(),expected_transform):raise ValueError('ERA5 orientation differs')
        return ds.ReadAsArray().astype(float)
    tavg,prec=monthly('tavg'),monthly('prec')
    original_bio=aligned(g,ROOT/'maxent/girdi/katmanlar/bio18.asc')
    baseline_bio,baseline_quarter=warm_quarter_precip(tavg,prec)
    if not np.allclose(baseline_bio,original_bio,rtol=0,atol=.001):raise ValueError('BIO18 baseline reconstruction failed')
    future_tavg=tavg+(mapped['tas']['future']-mapped['tas']['baseline'])
    ratio=precipitation_ratio(mapped['pr']['baseline'],mapped['pr']['future'])
    future_prec=prec*ratio
    future_bio,future_quarter=warm_quarter_precip(future_tavg,future_prec)
    sst_base=aligned(g,ROOT/'maxent/girdi/katmanlar/sst_yillik.asc')
    ice_base=aligned(g,ROOT/'maxent/girdi/katmanlar/buz_yillik.asc')
    sst_delta=(mapped['tos']['future']-mapped['tos']['baseline']).mean(0)
    ice_delta=(mapped['siconc']['future']-mapped['siconc']['baseline']).mean(0)
    unclipped_ice=ice_base+ice_delta
    outputs={'kaya':kaya,'bio18':future_bio,'sst_yillik':sst_base+sst_delta,
             'buz_yillik':np.clip(unclipped_ice,0,100)}
    if not all(np.isfinite(x).all() for x in outputs.values()):raise ValueError('Nonfinite future inputs')
    args.output.mkdir(parents=True)
    for name,values in outputs.items():write_grid(args.output/f'{name}.asc',g,values)
    np.savez_compressed(args.output/'monthly_delta_diagnostics.npz',tavg_baseline=tavg,
        tavg_future=future_tavg,prec_baseline=prec,prec_future=future_prec,prec_ratio=ratio,
        sst_delta=sst_delta,ice_delta_percentage_points=ice_delta,
        warm_quarter_baseline=baseline_quarter,warm_quarter_future=future_quarter,
        era5_sea_source_flat_index=sea_index,era5_sea_distance_km=sea_distance,
        **{f'{n}_native_flat_index':i for n,i in indices.items()})
    scenario={'schema_version':1,'kind':'cmip6_delta_projection','status':'exploratory_inputs_not_validated_final_model',
        'scenario_id':'IPSL-CM6A-LR_r1i1p1f1_ssp245_2041_2060_delta_v1',
        'source_id':'IPSL-CM6A-LR','member_id':'r1i1p1f1','ssp':'ssp245','future_period':'2041-2060',
        'baseline_period':'2000-2025','baseline_continuation':'historical 2000-2014 + ssp245 2015-2025',
        'reference_source':'ERA5 2000-2025; SCAR rock static','grid_crs':'EPSG:4326','grid_cellsize_degrees':.25,
        'regridding':'nearest complete native cell on sphere; land marine anomalies follow nearest ERA5 sea cell',
        'methods':{'tas':'monthly additive anomalies applied to ERA5 tavg',
                   'pr':'monthly future/baseline total precipitation ratio applied to ERA5 monthly totals; refuses baseline<1 mm',
                   'bio18':'recomputed precipitation sum in warmest quarter of future monthly tavg',
                   'sst_yillik':'equal-month annual mean native SST anomaly added to ERA5 annual SST',
                   'buz_yillik':'equal-month annual sea-ice difference in percentage points, additive to ERA5 annual ice then clipped0-100',
                   'kaya':'static original rock fraction'},
        'limitations':['single GCM/member/SSP','nearest-cell anomalies do not add spatial climate information',
                      'annual marine bias adjustment is not monthly clipping','baseline geographic validation weak',
                      'calibration M and final model not resolved','no colony/population/refugium claim'],
        'diagnostics':diagnostics,'warmest_quarter_changed_cells':int((future_quarter!=baseline_quarter).sum()),
        'ice_clipped_cells':int(((unclipped_ice<0)|(unclipped_ice>100)).sum()),
        'precip_ratio_minmax':[float(ratio.min()),float(ratio.max())],
        'future_ranges':{n:[float(x.min()),float(x.max())] for n,x in outputs.items()}}
    (args.output/'scenario.json').write_text(json.dumps(scenario,indent=2,ensure_ascii=False)+'\n')
    used.extend([normals,mask_path,*[ROOT/f'maxent/girdi/katmanlar/{n}.asc' for n in outputs]])
    manifest={'input_files':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in used],
              'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'output_files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in args.output.iterdir() if p.is_file()}}
    (args.output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'future_ranges':scenario['future_ranges'],
                      'warmest_quarter_changed_cells':scenario['warmest_quarter_changed_cells']},indent=2))


if __name__=='__main__':main()
