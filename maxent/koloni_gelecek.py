"""Apply three source-checked GCM marine anomalies to census-colony layers.

Monthly anomalies are mapped to each ERA5 cell's actual marine donor. Static
rock is not an ice-free-land forecast. No daily ice dates are invented from
monthly GCM data. All outputs are distinct from the source directory.
"""
import argparse
import json
from pathlib import Path
import shutil

import numpy as np
import xarray as xr

from izgara import read_grid,aligned,write_grid,cell_areas_km2
from revizyon_denetimi import ROOT,dump,table
from revizyon_katmanlari import nearest_index,BREEDING

MODELS={'IPSL':'IPSL-CM6A-LR','GFDL':'GFDL-ESM4','MPI':'MPI-ESM1-2-LR'}


def marine_anomaly(base,model_file,lat,lon,donor,units):
    with np.load(model_file) as x:
        if str(x['units'])!=units:raise ValueError('GCM unit mismatch')
        if not np.array_equal(x['month'],np.arange(1,13)):raise ValueError('GCM month ordering')
        ok=np.isfinite(x['baseline']).all(0)&np.isfinite(x['future']).all(0)
        ok&=(x['baseline_valid_year_count']==26).all(0)&(x['future_valid_year_count']==20).all(0)
        if not ok.any():raise ValueError('No complete marine source cells')
        index,distance=nearest_index(x['lat'],x['lon'],lat.ravel()[donor],lon.ravel()[donor],ok)
        b=x['baseline'].reshape(12,-1)[:,index.ravel()].reshape(base.shape)
        f=x['future'].reshape(12,-1)[:,index.ravel()].reshape(base.shape)
    future=base+f-b
    if units=='%':future=np.clip(future,0,100)
    return future,b,distance,index


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--layers',type=Path,default=ROOT/'maxent/girdi/koloni_20261112')
    p.add_argument('--raw',type=Path,default=ROOT/'era5/veri_ham/peninsula_20261112/marine_monthly_2000_2025.nc')
    p.add_argument('--cmip-root',type=Path,default=ROOT/'maxent/girdi/cmip6_peninsula_20261112')
    p.add_argument('--output',type=Path,default=ROOT/'maxent/girdi/koloni_future_20261112')
    args=p.parse_args()
    defs=json.loads((args.layers/'definitions.json').read_text())
    if args.output.exists():raise FileExistsError('Fresh future directory required')
    g,rock=read_grid(args.layers/'current/kaya.asc')
    with xr.open_dataset(args.raw,engine='h5netcdf') as d:
        if d.sst.attrs.get('GRIB_paramId')!=34 or d.siconc.attrs.get('GRIB_paramId')!=31:
            raise ValueError('Marine source identity mismatch')
        norm=d.astype({'sst':'float64','siconc':'float64'}).groupby('valid_time.month').mean('valid_time',skipna=False).load()
        lon,lat=np.meshgrid(d.longitude.values,d.latitude.values)
    if lat.shape!=rock.shape:raise ValueError('ERA5 and colony grid mismatch')
    sst=norm.sst.values-273.15;ice=100*norm.siconc.values
    valid=np.isfinite(sst).all(0)&np.isfinite(ice).all(0)
    donor,donor_distance=nearest_index(lat,lon,lat,lon,valid)
    filled={v:a.reshape(12,-1)[:,donor.ravel()].reshape(a.shape) for v,a in [('tos',sst),('siconc',ice)]}
    support=aligned(g,args.layers/'rocky_coastal_support.asc')>.5
    focus=(lat<=-66)&(lat>=-70.5)&(lon>=-73)&(lon<=-64)
    args.output.mkdir(parents=True)
    performance=[]
    for label,model in MODELS.items():
        receipt=json.loads((args.cmip_root/model/'receipt.json').read_text())
        if not receipt['complete'] or receipt['model']!=model:raise ValueError('Incomplete/wrong GCM receipt')
        out=args.output/label;out.mkdir()
        shutil.copytree(args.layers/'current',out/'current')
        for name in ['rocky_coastal_support.asc','target_group_support.asc','colony_samples.csv']:
            shutil.copyfile(args.layers/name,out/name)
        mapped={};mapping={}
        for var,unit in [('tos','degC'),('siconc','%')]:
            a,b,dist,index=marine_anomaly(filled[var],args.cmip_root/model/f'{var}_aylik_klimatoloji.npz',lat,lon,donor,unit)
            mapped[var]=a
            mapping[var]={'native_cells_at_support':len(np.unique(index[support])),
                          'max_support_donor_distance_km':float(dist[support].max())}
            if var=='siconc':
                for scope,mask in [('download_envelope_ocean',valid),('Marguerite_ocean',valid&focus)]:
                    delta=b[:,mask]-ice[:,mask];weights=cell_areas_km2(g)[mask]
                    if not mask.any():raise ValueError('Missing local evaluation region')
                    performance.append(dict(model=model,scope=scope,n_ERA5_cells=int(mask.sum()),
                        n_distinct_native_cells=len(np.unique(index[mask])),
                        mean_bias_percentage_points=float(np.average(delta.mean(0),weights=weights)),
                        rmse_percentage_points=float(np.sqrt(np.average((delta**2).mean(0),weights=weights)))))
        current={'buz_breeding':filled['siconc'][np.array(BREEDING)-1].mean(0),
                 'buz_kis':filled['siconc'][np.array([6,7,8])-1].mean(0),
                 'sst_breeding':filled['tos'][np.array(BREEDING)-1].mean(0)}
        for name,a in current.items():
            if not np.allclose(a,aligned(g,args.layers/'current'/f'{name}.asc'),atol=1e-6,rtol=1e-6):
                raise ValueError('Current colony predictors disagree with marine source')
        future={'kaya':rock,'buz_breeding':mapped['siconc'][np.array(BREEDING)-1].mean(0),
                'buz_kis':mapped['siconc'][np.array([6,7,8])-1].mean(0),
                'sst_breeding':mapped['tos'][np.array(BREEDING)-1].mean(0)}
        for name,a in future.items():write_grid(out/f'future_{label}'/f'{name}.asc',g,a)
        write_grid(out/'report_focus.asc',g,focus.astype(float))
        dump(out/'definitions.json',dict(defs,gcm_label=label,gcm_source_id=model,
            GCM_source_directory=str(args.cmip_root/model),current_years=[2000,2025],future_years=[2041,2060],
            baseline_GCM='historical 2000–2014 plus SSP245 2015–2025',scenario='SSP245',
            marine_mapping=mapping,monthly_ice_clipped_after_anomaly=True,
            future_validation=False,final_model_selected=False))
    table(args.output/'ice_baseline_comparison.csv',performance)
    dump(args.output/'interpretation.json',{
        'n_GCM':3,'members_per_GCM':1,'probabilistic_ensemble':False,
        'baseline_performance':'area-weighted climatological comparison to ERA5; not independent in-situ validation',
        'unresolved':'interannual variance, model skill ranking and observational product uncertainty not resolved',
        'daily_phenology_projected':False,'report_focus':'Marguerite Bay; training envelope wider'})
    print(json.dumps({'complete':True,'GCM':list(MODELS)}),flush=True)


if __name__=='__main__':main()
