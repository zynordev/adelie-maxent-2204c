#!/usr/bin/env python3
"""Project immutable saved MaxEnt fold lambdas to real single-GCM inputs.

This is an exploratory transfer of the OLD model, not an accepted final model.
First checks density.Project against the existing current/hypothetical fold0.
No model training or selection is performed here.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np
from izgara import read_grid,aligned,write_grid,cell_areas_km2
from fark_analizi import summarize

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'maxent/girdi/cmip6_ipsl_ssp245_2041_2060_v1'
OLD=ROOT/'maxent/cikti/deneme_2050'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'maxent/cikti/cmip6_ipsl_ssp245_2041_2060_v1')
    parser.add_argument('--java',default='/usr/lib/jvm/java-21-openjdk/bin/java')
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError('Use a fresh output directory')
    scenario=json.loads((INPUT/'scenario.json').read_text())
    manifest=json.loads((INPUT/'manifest.json').read_text())
    if scenario['kind']!='cmip6_delta_projection':raise ValueError('Real scenario manifest required')
    for name,digest in manifest['output_files'].items():
        if hashlib.sha256((INPUT/name).read_bytes()).hexdigest()!=digest:raise ValueError('Scenario hash mismatch')
    args.output.mkdir(parents=True)
    jar=ROOT/'maxent/maxent.jar';commands=[]
    def project(lambdas,layers,dest):
        cmd=[args.java,'-Djava.awt.headless=true','-cp',str(jar),'density.Project',str(lambdas),str(layers),str(dest),
             'outputformat=cloglog','doclamp=true','writeclampgrid=true','extrapolate=true']
        commands.append(cmd)
        result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=120)
        dest.with_suffix('.log').write_text(result.stdout+'\n'+result.stderr)
        if result.returncode or not dest.is_file():raise RuntimeError('density.Project failed; inspect run log')
    g,current=read_grid(OLD/'Pygoscelis_adeliae_avg.asc')
    checks={}
    for label,folder,saved in [('current',ROOT/'maxent/girdi/katmanlar',OLD/'Pygoscelis_adeliae_0.asc'),
                               ('legacy_sensitivity',ROOT/'maxent/girdi/gelecek_2050_ssp245',
                                OLD/'Pygoscelis_adeliae_0_gelecek_2050_ssp245.asc')]:
        dest=args.output/f'control_{label}_fold0.asc'
        project(OLD/'Pygoscelis_adeliae_0.lambdas',folder,dest)
        actual=aligned(g,dest);expected=aligned(g,saved)
        error=float(np.max(abs(actual-expected)));checks[label]=error
        if error>5e-6:raise ValueError('Saved-model projection does not reproduce original fold')
    inputs={name:aligned(g,INPUT/f'{name}.asc') for name in ['bio18','buz_yillik','kaya','sst_yillik']}
    used=[jar,INPUT/'manifest.json',INPUT/'scenario.json',OLD/'Pygoscelis_adeliae_avg.asc',
          OLD/'Pygoscelis_adeliae_0_gelecek_2050_ssp245.asc',
          *[(INPUT/f'{n}.asc') for n in inputs],
          *[ROOT/f'maxent/girdi/katmanlar/{n}.asc' for n in inputs],
          *[ROOT/f'maxent/girdi/gelecek_2050_ssp245/{n}.asc' for n in inputs]]
    future_folds=[];current_folds=[];novel=[];clamp=[]
    for i in range(10):
        lambdas=OLD/f'Pygoscelis_adeliae_{i}.lambdas';used.append(lambdas)
        dest=args.output/f'fold_{i}.asc';project(lambdas,INPUT,dest)
        future_folds.append(aligned(g,dest))
        path=OLD/f'Pygoscelis_adeliae_{i}.asc';used.append(path);current_folds.append(aligned(g,path))
        clamp.append(aligned(g,args.output/f'fold_{i}_clamping.asc'))
        ranges={}
        with lambdas.open() as f:
            for row in csv.reader(f):
                if row[0] in inputs and len(row)==4:ranges[row[0]]=(float(row[2]),float(row[3]))
        if set(ranges)!=set(inputs):raise ValueError('Missing native predictor range in lambda file')
        novel.append(np.any([(inputs[n]<lo)|(inputs[n]>hi) for n,(lo,hi) in ranges.items()],axis=0))
    a,b=np.stack(current_folds),np.stack(future_folds)
    if np.max(abs(a.mean(0)-current))>5e-6:raise ValueError('Paired baseline mismatch')
    changes=b-a;future=b.mean(0);delta=future-current
    valid=np.isfinite(current)&np.isfinite(future);areas=cell_areas_km2(g)
    novelty=np.any(novel,axis=0);disagree=(changes.min(0)<0)&(changes.max(0)>0)
    metrics={'scenario':scenario,'valid_cells':int(valid.sum()),
        'interpretation':'EXPLORATORY transfer of original random10-fold model; geographic validation weak; not final scientific result',
        'model_source':'immutable 2026-10-31 fold lambda files; no retraining',
        'control_max_abs_error':checks,'domain':'entire rectangular calibration domain, not habitat area',
        'area_method':'WGS84 ellipsoid lat/lon rectangle surface integral','domain_area_km2':float(areas.sum()),
        'by_difference_threshold':{str(t):summarize(delta,areas,valid,t) for t in [.025,.05,.1,.25]},
        'novel_any_fold_cells':int(novelty.sum()),
        'novelty_method':'any native predictor outside lambda min/max; univariate range flag, not MESS',
        'sign_disagreement_cells':int(disagree.sum()),'max_clamping_effect':float(np.max(clamp)),
        'clamping_nonzero_any_fold_cells':int((np.max(clamp,axis=0)>0).sum()),
        'habitat_area_loss':None,'replicate_uncertainty':'paired overlapping saved model folds, not climate ensemble'}
    names={'gunumuz':current,'duyarlilik':future,'uygunluk_farki':delta,'fark_sd':changes.std(0),
        'fark_q10':np.quantile(changes,.1,axis=0),'fark_q90':np.quantile(changes,.9,axis=0),
        'isaret_uyumu':np.maximum(np.mean(changes>0,axis=0),np.mean(changes<0,axis=0)),
        'isaret_belirsiz':disagree.astype(float),'ekstrapolasyon':novelty.astype(float),
        'clamping_max':np.max(clamp,axis=0),
        'tanisal_sinif':novelty.astype(float)+2*disagree.astype(float)}
    for name,values in names.items():write_grid(args.output/f'{name}.asc',g,values)
    with (args.output/'hucre_analizi.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['row_north','col','area_km2',*names])
        for i,j in zip(*np.nonzero(valid)):
            w.writerow([int(i),int(j),areas[i,j],*[x[i,j] for x in names.values()]])
    (args.output/'ozet.json').write_text(json.dumps(metrics,indent=2,ensure_ascii=False)+'\n')
    (args.output/'manifest.json').write_text(json.dumps({'commands':commands,
        'java_version':subprocess.run([args.java,'-version'],capture_output=True,text=True).stderr,
        'input_files':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in used],
        'source_scripts':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in [Path(__file__),ROOT/'maxent/izgara.py',ROOT/'maxent/fark_analizi.py']},
        'output_files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(args.output.iterdir()) if p.is_file()}},indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'control_error':checks,
        'novel_cells':metrics['novel_any_fold_cells'],'sign_disagreement':metrics['sign_disagreement_cells']},indent=2))


if __name__=='__main__':main()
