"""Version-checked CMIP6 regional extraction across time-split source files."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import re
import urllib.parse

import numpy as np
import requests
import xarray as xr

from cmip6_erisim_kontrolu import ROOT, TABLES, PERIODS, ESGF_SEARCH, fetch, safe_error
from revizyon_denetimi import dump


def select_sources(item, timeout=30):
    row=item['catalog_record']
    query=ESGF_SEARCH+'?'+urllib.parse.urlencode({
        'project':'CMIP6','source_id':row['source_id'],'experiment_id':row['experiment_id'],
        'member_id':row['member_id'],'variable_id':row['variable_id'],'table_id':row['table_id'],
        'type':'File','format':'application/solr+json','limit':100,'latest':'true'})
    payload,receipt=fetch(query,4*1024*1024,timeout)
    response=json.loads(payload)['response']
    if response['numFound']>100:raise ValueError('Source query truncated')
    selected={}
    for doc in response['docs']:
        token=f'.{row["grid_label"]}.v{row["version"].lstrip("v") }.'
        if doc.get('data_node')!='esgf.ceda.ac.uk' or token not in doc['instance_id'] or doc.get('retracted'):
            continue
        match=re.search(r'_(\d{6})-(\d{6})\.nc$',doc['instance_id'])
        if not match:continue
        first,last=map(int,match.groups())
        if not any(first<=end*100+12 and last>=start*100+1
                   for _,start,end in PERIODS[row['experiment_id']]):continue
        urls=[u.split('|')[0].removesuffix('.html') for u in doc['url'] if u.endswith('|OPENDAP')]
        if len(urls)!=1:raise ValueError('Source has no unique DAP URL')
        selected[doc['instance_id']]={'id':doc['instance_id'],'opendap_url':urls[0],
            'file_checksum':doc.get('checksum'),'file_checksum_type':doc.get('checksum_type'),
            'first_month':first,'last_month':last,'query_receipt':receipt}
    if not selected:raise ValueError('No matching regional source files')
    return sorted(selected.values(),key=lambda d:d['first_month'])


def extract(variable,items,out,area=(-66,-73,-70.5,-64)):
    parts={};sources=[];geo=None;source_id=items[0]['catalog_record']['source_id']
    session=requests.Session();session.trust_env=False
    for experiment in PERIODS:
        item=next(i for i in items if i['catalog_record']['variable_id']==variable and
                  i['catalog_record']['experiment_id']==experiment)
        for source in select_sources(item):
            with xr.open_dataset(source['opendap_url'],engine='pydap',session=session,
                                 timeout=40,mask_and_scale=False) as remote:
                row=item['catalog_record']
                for key,value in [('source_id',source_id),('variant_label',row['member_id']),
                                  ('experiment_id',experiment),('grid_label',row['grid_label'])]:
                    if remote.attrs.get(key)!=value:raise ValueError('Native source identity mismatch')
                field=remote[variable]
                latname=next((n for n in ['nav_lat','latitude','lat'] if n in remote),None)
                lonname=next((n for n in ['nav_lon','longitude','lon'] if n in remote),None)
                if latname is None or lonname is None:raise ValueError('Native latitude/longitude coordinates missing')
                lat,lon=remote[latname].values,remote[lonname].values
                if lat.ndim==lon.ndim==1:lon,lat=np.meshgrid(lon,lat)
                lon=(lon+180)%360-180
                north,west,south,east=area
                yy,xx=np.where((lat>=south)&(lat<=north)&(lon>=west)&(lon<=east))
                if not len(yy):raise ValueError('No native regional cells')
                y0,y1=max(0,yy.min()-1),min(lat.shape[0],yy.max()+2)
                x0,x1=max(0,xx.min()-1),min(lat.shape[1],xx.max()+2)
                coords=(lat[y0:y1,x0:x1],lon[y0:y1,x0:x1])
                if geo is not None and any(not np.array_equal(a,b) for a,b in zip(coords,geo)):
                    raise ValueError('Time chunks use different spatial grids')
                geo=coords
                for role,start,end in PERIODS[experiment]:
                    if source['first_month']>end*100+12 or source['last_month']<start*100+1:continue
                    selected=field.sel(time=slice(f'{start}-01-01',f'{end}-12-31')).isel(
                        {field.dims[1]:slice(y0,y1),field.dims[2]:slice(x0,x1)})
                    values=np.asarray(selected.values,float)
                    for marker in ['_FillValue','missing_value']:
                        if marker in field.attrs:
                            values[np.isclose(values,float(field.attrs[marker]),rtol=1e-6,atol=0)]=np.nan
                    if np.any(np.abs(values[np.isfinite(values)])>=1e19):raise ValueError('Unrecognized missing marker')
                    units=field.attrs['units'];days=selected.time.dt.days_in_month.values.astype(float)
                    if variable in ['tas','tos']:
                        if units=='K':values-=273.15
                        elif units not in ['degC','degrees_C','degree_Celsius']:raise ValueError('Temperature units')
                    elif variable=='siconc':
                        if units in ['1','0-1','(0 - 1)']:values*=100
                        elif units!='%':raise ValueError('Ice units')
                        finite=values[np.isfinite(values)]
                        if (finite<0).any() or (finite>100.001).any():raise ValueError('Ice bounds')
                    elif variable=='pr':
                        if units!='kg m-2 s-1':raise ValueError('Precipitation units')
                        values*=days[:,None,None]*86400
                        if (values[np.isfinite(values)]<0).any():raise ValueError('Negative precipitation')
                    piece=xr.Dataset({variable:(('time','y','x'),values),
                        'days_in_month':('time',days)},coords={'time':selected.time.values,
                        'latitude':(('y','x'),geo[0]),'longitude':(('y','x'),geo[1])})
                    piece.time.encoding={'calendar':remote.time.encoding.get('calendar','standard'),
                                         'units':'days since 1850-01-01'}
                    parts.setdefault(role,[]).append(piece)
                source.update(source_units=field.attrs['units'],native_slice=[int(y0),int(y1),int(x0),int(x1)],
                              calendar=remote.time.encoding.get('calendar','standard'))
                sources.append(source)
    # Sort datasets together with their coordinates, never the coordinates alone.
    merged={}
    for experiment,periods in PERIODS.items():
        for role,start,end in periods:
            a=xr.concat(parts[role],dim='time').sortby('time')
            actual=list(zip(a.time.dt.year.values.tolist(),a.time.dt.month.values.tolist()))
            if actual!=[(y,m) for y in range(start,end+1) for m in range(1,13)]:
                raise ValueError('Source months duplicated or missing')
            merged[role]=a
    datasets={'baseline_2000_2025':xr.concat([merged['baseline_historical'],merged['baseline_scenario']],dim='time'),
              'future_2041_2060':merged['future']}
    unit={'tas':'degC','tos':'degC','pr':'mm month-1','siconc':'%'}[variable]
    normals=[];counts=[];days=[];files=[]
    for role,d in datasets.items():
        d.attrs.update(source_id=source_id,member_id=items[0]['catalog_record']['member_id'])
        d[variable].attrs['units']=unit
        path=out/f'{variable}_{role}.nc';d.to_netcdf(path,engine='scipy');files.append(path)
        normals.append(d[variable].groupby('time.month').mean('time',skipna=True))
        counts.append(d[variable].groupby('time.month').count('time'))
        days.append(d.days_in_month.groupby('time.month').mean('time'))
    path=out/f'{variable}_aylik_klimatoloji.npz'
    np.savez_compressed(path,baseline=normals[0].values,future=normals[1].values,
        lat=geo[0],lon=geo[1],month=np.arange(1,13),units=np.array(unit),
        baseline_valid_year_count=counts[0].values,future_valid_year_count=counts[1].values,
        baseline_mean_days_in_month=days[0].values,future_mean_days_in_month=days[1].values)
    files.append(path);session.close()
    return {'variable':variable,'source_files':sources,'status':'complete',
            'outputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model',required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--area',type=float,nargs=4,default=[-66,-73,-70.5,-64])
    args=p.parse_args()
    if args.output.exists():raise FileExistsError('Fresh directory required')
    args.output.mkdir(parents=True)
    inventory=json.loads((ROOT/'erisim_envanteri.json').read_text())
    items=[i for i in inventory['datasets'] if i['catalog_record']['source_id']==args.model]
    if len(items)!=8:raise ValueError('Eight catalog entries required')
    result={'model':args.model,'area_NWSE':args.area,'variables':[],'complete':False}
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs={pool.submit(extract,v,items,args.output,args.area):v for v in TABLES}
        for done in as_completed(jobs):
            try:item=done.result()
            except Exception as exc:
                item={'variable':jobs[done],'status':'failed','error':safe_error(exc)}
                if isinstance(exc,ValueError):item['validation_error']=str(exc)
            result['variables'].append(item)
            result['complete']=len(result['variables'])==4 and all(v['status']=='complete' for v in result['variables'])
            dump(args.output/'receipt.json',result)
            print(json.dumps({'variable':jobs[done],'status':item['status']}),flush=True)
    return 0 if result['complete'] else 1


if __name__=='__main__':raise SystemExit(main())
