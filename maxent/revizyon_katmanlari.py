"""Source-based monthly seasonal predictors and experimental CMIP delta layers.

All products are separate from historical rasters. Daily phenology, when
available, is descriptive only: future monthly GCM data cannot supply dates.
"""
import argparse
import calendar
import hashlib
import json
from pathlib import Path

import numpy as np
import xarray as xr
from scipy.spatial import cKDTree

from izgara import read_grid, aligned, write_grid
from revizyon_denetimi import dump

ROOT=Path(__file__).resolve().parents[1]
BREEDING=[11,12,1,2,3]


def nearest_index(slat,slon,tlat,tlon,valid):
    def xyz(lat,lon):
        a,b=np.deg2rad(lat),np.deg2rad(lon)
        return np.stack([np.cos(a)*np.cos(b),np.cos(a)*np.sin(b),np.sin(a)],axis=-1)
    ids=np.flatnonzero(valid)
    distance,index=cKDTree(xyz(slat.ravel()[ids],slon.ravel()[ids])).query(
        xyz(tlat.ravel(),tlon.ravel()))
    km=2*6371*np.arcsin(np.clip(distance/2,0,1))
    return ids[index].reshape(tlat.shape),km.reshape(tlat.shape)


def first_persistent(binary,length=5):
    """First start index of length consecutive True; -1 when absent."""
    b=np.asarray(binary,bool)
    out=np.full(b.shape[1:],-1,dtype=int)
    for start in range(len(b)-length+1):
        m=(out<0)&b[start:start+length].all(0)
        out[m]=start
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT/'maxent/girdi/revizyon_20261112')
    p.add_argument('--daily',type=Path)
    p.add_argument('--cmip',type=Path,default=ROOT/'maxent/girdi/cmip6_2041_2060/IPSL-CM6A-LR_r1i1p1f1')
    p.add_argument('--gcm-label',default='IPSL')
    args=p.parse_args()
    if args.output.exists():
        raise FileExistsError('Choose a fresh output directory')
    args.output.mkdir(parents=True)
    raw=ROOT/'era5/veri_ham/denetim_20261112/marine_monthly_2000_2025.nc'
    with xr.open_dataset(raw,engine='h5netcdf') as source:
        if source.sst.attrs.get('GRIB_paramId')!=34 or source.sst.attrs.get('units')!='K':
            raise ValueError('SST source identity mismatch')
        if source.siconc.attrs.get('GRIB_paramId')!=31:
            raise ValueError('Sea ice source identity mismatch')
        ds=source.load()
    expected=np.arange('2000-01','2026-01',dtype='datetime64[M]')
    if not np.array_equal(ds.valid_time.values.astype('datetime64[M]'),expected):
        raise ValueError('Incomplete monthly years')
    normal=ds.astype({'sst':'float64','siconc':'float64'}).groupby('valid_time.month').mean('valid_time',skipna=False)
    sst=normal.sst.values-273.15; ice=normal.siconc.values*100
    grid,kaya=read_grid(ROOT/'maxent/girdi/katmanlar/kaya.asc')
    xx,yy=np.meshgrid(ds.longitude.values,ds.latitude.values)
    if xx.shape!=kaya.shape:
        raise ValueError('Grid mismatch')
    valid=np.isfinite(sst).all(0)&np.isfinite(ice).all(0)
    donor,donor_distance=nearest_index(yy,xx,yy,xx,valid)
    # Record donor distance, preserving the legacy coastal filling only as an
    # explicit experimental support convention, not proof of habitat.
    sst_filled=sst.reshape(12,-1)[:,donor.ravel()].reshape(sst.shape)
    ice_filled=ice.reshape(12,-1)[:,donor.ravel()].reshape(ice.shape)
    write_grid(args.output/'marine_donor_distance_km.asc',grid,donor_distance)
    write_grid(args.output/'source_monthly_sst_min.asc',grid,np.nanmin(sst_filled,axis=0))
    ids=np.array(BREEDING)-1
    features={
        'kaya':kaya,
        'bio18':aligned(grid,ROOT/'maxent/girdi/katmanlar/bio18.asc'),
        'buz_yillik':ice_filled.mean(0),'sst_yillik':sst_filled.mean(0),
        'buz_breeding':ice_filled[ids].mean(0),'sst_breeding':sst_filled[ids].mean(0),
        'buz_son':ice_filled[np.array([9,10,11])-1].mean(0),
        'buz_kis':ice_filled[np.array([6,7,8])-1].mean(0),
    }
    for name,a in features.items():
        write_grid(args.output/'current'/f'{name}.asc',grid,a)
    cmip=args.cmip.resolve()
    future=dict(features)
    mapping={}
    mapped_monthly={}
    for var,base in [('tos',sst_filled),('siconc',ice_filled)]:
        with np.load(cmip/f'{var}_aylik_klimatoloji.npz') as x:
            ok=np.isfinite(x['baseline']).all(0)&np.isfinite(x['future']).all(0)
            ok&=(x['baseline_valid_year_count']==26).all(0)&(x['future_valid_year_count']==20).all(0)
            if str(x['units'])!=('degC' if var=='tos' else '%'):
                raise ValueError('GCM marine units mismatch')
            index,distance=nearest_index(x['lat'],x['lon'],yy.ravel()[donor],xx.ravel()[donor],ok)
            model_baseline=x['baseline'].reshape(12,-1)[:,index.ravel()].reshape(base.shape)
            model_future=x['future'].reshape(12,-1)[:,index.ravel()].reshape(base.shape)
            change=model_future-model_baseline
            mapped=base+change
            if var=='siconc':mapped=np.clip(mapped,0,100)
            mapped_monthly[var]=mapped
            mapping[var]={'native_cells':len(np.unique(index)),
                          'max_distance_km':float(distance.max())}
            if var=='siconc':
                bias=model_baseline-ice_filled
                dump(args.output/'ice_baseline_comparison.json',{
                    'reference':'ERA5 monthly sea ice; not independent in-situ validation',
                    'region':'available Marguerite-domain native ocean cells, not whole Bellingshausen sector',
                    'n_ERA5_cells':int(valid.sum()),'n_native_GCM_cells':len(np.unique(index)),
                    'mean_bias_percentage_points':float(np.mean(bias[:,valid])),
                    'rmse_percentage_points':float(np.sqrt(np.mean(bias[:,valid]**2))),
                    'monthly_mean_bias_percentage_points':np.mean(bias[:,valid],axis=1).tolist()})
    future['sst_yillik']=mapped_monthly['tos'].mean(0)
    future['sst_breeding']=mapped_monthly['tos'][ids].mean(0)
    future['buz_yillik']=mapped_monthly['siconc'].mean(0)
    future['buz_breeding']=mapped_monthly['siconc'][ids].mean(0)
    future['buz_son']=mapped_monthly['siconc'][np.array([9,10,11])-1].mean(0)
    future['buz_kis']=mapped_monthly['siconc'][np.array([6,7,8])-1].mean(0)
    with xr.open_dataset(ROOT/'era5/ara/aylik_normaller.nc',engine='h5netcdf') as atm:
        tavg=atm.tavg.values.astype(float);prec=atm.prec.values.astype(float)
    for var in ['tas','pr']:
        with np.load(cmip/f'{var}_aylik_klimatoloji.npz') as x:
            ok=np.isfinite(x['baseline']).all(0)&np.isfinite(x['future']).all(0)
            ok&=(x['baseline_valid_year_count']==26).all(0)&(x['future_valid_year_count']==20).all(0)
            index,distance=nearest_index(x['lat'],x['lon'],yy,xx,ok)
            baseline=x['baseline'].reshape(12,-1)[:,index.ravel()].reshape(tavg.shape)
            projected=x['future'].reshape(12,-1)[:,index.ravel()].reshape(tavg.shape)
            if var=='tas':tavg=tavg+projected-baseline
            else:
                if (baseline<1).any() or (projected<0).any():raise ValueError('Unsupported precipitation ratio')
                prec=prec*projected/baseline
            mapping[var]={'native_cells':len(np.unique(index)),'max_distance_km':float(distance.max())}
    tq=tavg+np.roll(tavg,-1,axis=0)+np.roll(tavg,-2,axis=0)
    pq=prec+np.roll(prec,-1,axis=0)+np.roll(prec,-2,axis=0)
    future['bio18']=np.take_along_axis(pq,tq.argmax(0)[None],axis=0)[0]
    for name,a in future.items():
        write_grid(args.output/f'future_{args.gcm_label}'/f'{name}.asc',grid,a)
    definitions={
        'breeding_months':BREEDING,'seasonal_definition':'unweighted arithmetic month means',
        'current_years':[2000,2025], 'future_years':[2041,2060],
        'baseline_GCM':'historical 2000-2014 plus ssp245 2015-2025',
        'gcm_label':args.gcm_label,'GCM_source_directory':str(cmip.relative_to(ROOT)),
        'future_annual_ice':'monthly anomalies added, then monthly clipping 0..100; differs from legacy annual clipping',
        'sst_source_confirmed':True,
        'sst_physical_QC_resolved':False,
        'SST_use':'flagged sensitivity candidate; no SST correction or clipping invented',
        'mapping':mapping,'phenology_days_inferred_from_monthly':False,
        'predictor_sets':{
            'annual':['bio18','buz_yillik','kaya','sst_yillik'],
            'seasonal':['bio18','buz_breeding','kaya','sst_breeding'],
            'seasonal_no_sst':['bio18','buz_breeding','kaya'],
            'ice_seasonality':['buz_breeding','buz_kis','kaya'],
        },'final_model_selected':False}
    dump(args.output/'definitions.json',definitions)
    if args.daily:
        with xr.open_dataset(args.daily,engine='h5netcdf') as d:
            daily=d.siconc.load().astype(float)*100
        if daily.shape[1:]!=kaya.shape:
            raise ValueError('Daily grid mismatch')
        # March-February seasons avoid joining unrelated southern summer dates.
        summaries=[];free=[];advance=[];retreat=[]
        for year in range(2000,2025):
            selection=daily.sel(valid_time=slice(f'{year}-03-01',f'{year+1}-02-{29 if calendar.isleap(year+1) else 28}'))
            a=selection.values
            if len(a) not in [365,366]:
                raise ValueError('Incomplete daily cycle')
            complete=np.isfinite(a).all(0)
            frozen=a>=15
            onset=first_persistent(frozen)
            # Retreat: day after the last persistent icy period in the cycle.
            reverse=first_persistent(frozen[::-1])
            end=np.where(reverse>=0,len(a)-reverse,-1)
            onset=np.where(complete&(onset>0),onset,np.nan)
            end=np.where(complete&(end<len(a))&(end>=0),end,np.nan)
            free.append(np.where(complete,(a<15).sum(0),np.nan))
            advance.append(onset);retreat.append(end)
            summaries.append({'cycle_start_year':year,'n_days':len(a)})
        for name,a in [('ice_free_days',free),('ice_advance_day_from_Mar1',advance),
                       ('ice_retreat_day_from_Mar1',retreat)]:
            stack=np.stack(a);count=np.isfinite(stack).sum(0)
            mean=np.divide(np.nansum(stack,0),count,out=np.full_like(stack[0],np.nan),where=count>0)
            write_grid(args.output/'phenology'/f'{name}.asc',grid,mean)
            write_grid(args.output/'phenology'/f'{name}_valid_cycles.asc',grid,count.astype(float))
        dump(args.output/'phenology'/'definition.json',{
            'threshold_percent':15,'persistence_days':5,'time':'00UTC daily snapshot',
            'cycles':summaries,'dates_indexed_from':'March 1 = 0',
            'boundary_censored_events':'NaN; zero/365 dates not invented',
            'retreat':'first day after last five-day icy interval',
            'future_dates_available':False,'future_model_predictor':False})
    dump(args.output/'manifest.json',{'source_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),
        'source_doi':'10.24381/cds.f17050d7',
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'outputs':{str(p.relative_to(args.output)):hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in args.output.rglob('*') if p.is_file()}})
    print(json.dumps(definitions,indent=2))


if __name__=='__main__':main()
