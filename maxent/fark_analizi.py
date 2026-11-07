#!/usr/bin/env python3
"""Paired suitability change on original grids; no habitat/refugia claims."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
from izgara import read_grid, aligned, write_grid, cell_areas_km2
from hazirla_2050_katmanlari import transform_values

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'maxent/cikti/deneme_2050'


def summarize(delta,areas,valid,threshold):
    labels={'azalma':delta < -threshold,'kararli':abs(delta)<=threshold,'artis':delta>threshold}
    n,area=int(valid.sum()),float(areas[valid].sum())
    if n==0:raise ValueError('Empty common valid domain')
    return {k:{'cells':int((v&valid).sum()),'cell_percent':100*float((v&valid).sum())/n,
               'domain_area_km2':float(areas[v&valid].sum()),
               'domain_area_percent':100*float(areas[v&valid].sum())/area}
            for k,v in labels.items()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'maxent/cikti/duyarlilik_analizi_v1')
    args=parser.parse_args()
    scenario_path=ROOT/'maxent/senaryo_duyarlilik.json'
    scenario=json.loads(scenario_path.read_text())
    if scenario['kind']!='hypothetical_sensitivity' or scenario.get('ssp') is not None:
        raise ValueError('Legacy run is hypothetical, never CMIP6')
    source=RUN/'Pygoscelis_adeliae_avg.asc'
    g,current=read_grid(source)
    future_path=RUN/'Pygoscelis_adeliae_gelecek_2050_ssp245_avg.asc'
    future=aligned(g,future_path)
    valid=np.isfinite(current)&np.isfinite(future)
    for a in (current,future):
        if np.any((a[valid]<0)|(a[valid]>1)):raise ValueError('Expected cloglog [0,1]')
    delta=future-current;areas=cell_areas_km2(g)
    args.output.mkdir(parents=True,exist_ok=True)
    used=[scenario_path,source,future_path]
    for name,transform in scenario['transformations'].items():
        baseline=ROOT/f'maxent/girdi/katmanlar/{name}.asc'
        legacy=ROOT/scenario['legacy_input_directory']/f'{name}.asc'
        original=aligned(g,baseline);actual=aligned(g,legacy)
        if not np.allclose(transform_values(original,transform),actual,atol=1e-6,rtol=0,equal_nan=True):
            raise ValueError(f'Scenario metadata does not describe saved inputs: {name}')
        used.extend([baseline,legacy])
    differences=[];novelties=[];clamp=[]
    for i in range(10):
        pair=[]
        for name in [f'Pygoscelis_adeliae_{i}.asc',f'Pygoscelis_adeliae_{i}_gelecek_2050_ssp245.asc',
                     f'Pygoscelis_adeliae_{i}_gelecek_2050_ssp245_novel.asc',
                     f'Pygoscelis_adeliae_{i}_gelecek_2050_ssp245_clamping.asc']:
            path=RUN/name;used.append(path);pair.append(aligned(g,path))
        if any(not np.array_equal(np.isfinite(x),valid) for x in pair):
            raise ValueError('Replicate coverage differs')
        differences.append(pair[1]-pair[0]);novelties.append(pair[2]);clamp.append(pair[3])
    stack=np.stack(differences)
    disagreement=(stack.min(0)<0)&(stack.max(0)>0)&valid
    novelty=np.any(np.stack(novelties)<0,axis=0)&valid
    max_clamp=np.max(np.abs(np.stack(clamp)),axis=0)
    agreement=np.maximum(np.mean(stack>0,axis=0),np.mean(stack<0,axis=0))
    q10,q90=np.quantile(stack,[.1,.9],axis=0)
    metrics={
        'scenario':scenario,'valid_cells':int(valid.sum()),
        'domain':'entire original rectangular model domain; not ecologically masked habitat',
        'domain_area_km2':float(areas[valid].sum()),
        'area_method':'WGS84 ellipsoid lat/lon rectangle surface integral',
        'threshold_unit':'absolute cloglog score difference (not relative percent change)',
        'by_difference_threshold':{str(t):summarize(delta,areas,valid,t) for t in [.025,.05,.1,.25]},
        'novel_any_fold_cells':int(novelty.sum()),
        'sign_disagreement_cells':int(disagreement.sum()),
        'clamping_nonzero_any_fold_cells':int(((max_clamp>0)&valid).sum()),
        'max_clamping_effect':float(max_clamp[valid].max()),
        'not_extrapolated':summarize(delta,areas,valid&~novelty,.05),
        'replicate_uncertainty':'paired overlapping cross-validation folds; not GCM ensemble or confidence interval',
        'habitat_area_loss':None,
        'habitat_area_loss_note':'No ecologically justified domain or independently justified suitability threshold; not calculated.'
    }
    names={'gunumuz':current,'duyarlilik':future,'uygunluk_farki':delta,'fark_sd':stack.std(0),
           'fark_q10':q10,'fark_q90':q90,'isaret_uyumu':agreement,
           'isaret_belirsiz':disagreement.astype(float),'ekstrapolasyon':novelty.astype(float),
           'clamping_max':max_clamp,'tanisal_sinif':novelty.astype(float)+2*disagreement.astype(float)}
    for name,data in names.items():
        write_grid(args.output/f'{name}.asc',g,np.where(valid,data,np.nan))
    with (args.output/'hucre_analizi.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['row_north','col','longitude','latitude','area_km2',*names])
        for i,j in zip(*np.nonzero(valid)):
            w.writerow([int(i),int(j),g.xllcorner+(j+.5)*g.cellsize,
                g.yllcorner+(g.nrows-i-.5)*g.cellsize,areas[i,j],*[data[i,j] for data in names.values()]])
    (args.output/'ozet.json').write_text(json.dumps(metrics,indent=2,ensure_ascii=False)+'\n')
    manifest={'input_files':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in used],
              'source_scripts':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in [Path(__file__),ROOT/'maxent/izgara.py']}}
    (args.output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:metrics[k] for k in ['valid_cells','novel_any_fold_cells','sign_disagreement_cells','max_clamping_effect']},indent=2))
    print('Uygunluk değişimi; habitat kaybı / CMIP6 projeksiyonu değildir:',args.output)


if __name__=='__main__':main()
