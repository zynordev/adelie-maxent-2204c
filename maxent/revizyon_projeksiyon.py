"""Full-fit structural sensitivity; AICc, paired clamping and ice-only effects.

All numbers describe provisional general-occurrence model scores, not colony
area, causal effects, or independently validated future habitat predictions.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import hashlib
import json
from pathlib import Path
import shutil

import numpy as np

from izgara import read_grid, aligned, write_grid, cell_areas_km2
from revizyon_denetimi import dump, table, mess
from revizyon_karsilastirma import ROOT, JAVA, CANDIDATES, feature_args, java


def aicc(raw, presence_rc, n_parameters, support):
    r=np.asarray(raw,float)
    total=r[support].sum()
    if total<=0 or not np.isfinite(total):
        raise ValueError('Invalid raw density normalizer')
    probabilities=r[tuple(presence_rc.T)]/total
    if (probabilities<=0).any():
        raise ValueError('Zero likelihood at presence')
    likelihood=float(np.log(probabilities).sum())
    n=len(presence_rc);k=n_parameters
    aic=2*k-2*likelihood
    return {'n_presence_cells':n,'nonzero_feature_coefficients':k,'log_likelihood':likelihood,
            'aic':aic,'aicc':aic+2*k*(k+1)/(n-k-1) if n>k+1 else None,
            'aicc_valid':bool(n>k+1)}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT/'maxent/cikti/revizyon_20261112/projection')
    p.add_argument('--comparison',type=Path,default=ROOT/'maxent/cikti/revizyon_20261112/comparison_v3')
    p.add_argument('--layers',type=Path,default=ROOT/'maxent/girdi/revizyon_20261112')
    p.add_argument('--sets',nargs='+',default=['annual','seasonal_no_sst'])
    args=p.parse_args()
    if args.output.exists():raise FileExistsError('Use a fresh output directory')
    args.output.mkdir(parents=True)
    defs=json.loads((args.layers/'definitions.json').read_text())
    design=json.loads((args.comparison/'design.json').read_text())
    g,support_values=read_grid(Path(design.get('support_mask',ROOT/'maxent/cikti/revizyon_20261112/denetim_v2/coastal_support.asc')))
    support=support_values>.5;area=cell_areas_km2(g)
    focus_path=args.layers/'report_focus.asc'
    focus=aligned(g,focus_path)>.5 if focus_path.is_file() else np.ones_like(support)
    write_grid(args.output/'report_focus_support.asc',g,np.where(support&focus,1,np.nan))
    rows=list(csv.DictReader((args.comparison/'representatives.csv').open()))
    rc=np.array([[g.nrows-1-int(np.floor((float(r['latitude'])-g.yllcorner)/g.cellsize)),
                  int(np.floor((float(r['longitude'])-g.xllcorner)/g.cellsize))] for r in rows])
    samples=[{k:r[k] for k in ['species','longitude','latitude']} for r in rows]
    table(args.output/'train.csv',samples)
    tasks=[]
    for predictor_set in args.sets:
        names=defs['predictor_sets'][predictor_set]
        current={n:aligned(g,args.layers/'current'/f'{n}.asc') for n in names}
        future={n:aligned(g,args.layers/f'future_{defs.get("gcm_label","IPSL")}'/f'{n}.asc') for n in names}
        root=args.output/predictor_set;root.mkdir()
        scenarios={'current':current,'future':future}
        for group,prefix in [('ice','buz_'),('sst','sst_'),('precip','bio18')]:
            if not any(n.startswith(prefix) for n in names):continue
            scenarios[f'only_{group}']={n:future[n] if n.startswith(prefix) else current[n] for n in names}
        for label,layers in scenarios.items():
            for n,a in layers.items():write_grid(root/'scenarios'/label/f'{n}.asc',g,np.where(support,a,np.nan))
        reference=np.column_stack([current[n][support] for n in names])
        write_grid(root/'mess_future.asc',g,np.where(support,mess(reference,
            np.stack([future[n] for n in names],axis=-1)),np.nan))
        for candidate in CANDIDATES:tasks.append((predictor_set,candidate,current,future,scenarios))

    def run(task):
        predictor_set,candidate,current,future,scenarios=task
        root=args.output/predictor_set;out=root/candidate;out.mkdir();(out/'plots').mkdir()
        env=out/'training_layers';env.mkdir()
        for path in (root/'scenarios/current').glob('*.asc'):shutil.copyfile(path,env/path.name)
        for scenario in scenarios:
            private=out/'scenarios'/scenario;private.mkdir(parents=True)
            for path in (root/'scenarios'/scenario).glob('*.asc'):
                shutil.copyfile(path,private/path.name)
        fc,rm=CANDIDATES[candidate]
        cmd=[JAVA,'-Xmx256m','-Djava.awt.headless=true','-jar',str(ROOT/'maxent/maxent.jar'),'-z','autorun',
             f'samplesfile={args.output/"train.csv"}',f'environmentallayers={env}',f'outputdirectory={out}',
             *feature_args(fc),f'betamultiplier={rm}','maximumbackground=10000',
             'addsamplestobackground=false','removeduplicates=false','randomseed=false','threads=1',
             'outputformat=cloglog','outputfiletype=asc','plots=false','responsecurves=false',
             'jackknife=false','visible=false','warnings=false']
        java(cmd,out/'train.log');commands=[cmd];lambda_path=out/'Pygoscelis_adeliae.lambdas'
        arrays={}
        for name in scenarios:
            for clamp in ([True,False] if name in ['current','future'] else [True]):
                tag=f'{name}_{"clamped" if clamp else "unclamped"}'
                dest=out/f'{tag}.asc'
                command=[JAVA,'-Djava.awt.headless=true','-cp',str(ROOT/'maxent/maxent.jar'),
                    'density.Project',str(lambda_path),str(out/'scenarios'/name),str(dest),
                    'outputformat=cloglog',f'doclamp={str(clamp).lower()}','extrapolate=true']
                java(command,out/f'{tag}.log');commands.append(command);arrays[tag]=aligned(g,dest)
        raw_command=[JAVA,'-Djava.awt.headless=true','-cp',str(ROOT/'maxent/maxent.jar'),
            'density.Project',str(lambda_path),str(out/'scenarios/current'),str(out/'raw_current.asc'),
            'outputformat=raw','doclamp=true','extrapolate=true']
        java(raw_command,out/'raw.log');commands.append(raw_command)
        params=list(csv.reader(lambda_path.open()))
        k=sum(len(r)==4 and abs(float(r[1]))>1e-10 for r in params)
        result=aicc(aligned(g,out/'raw_current.asc'),rc,k,support)
        result.update(predictors=predictor_set,candidate=candidate)
        a,b=arrays['current_clamped'],arrays['future_clamped'];delta=b-a
        unclamped=arrays['future_unclamped']-arrays['current_unclamped']
        write_grid(out/'delta_clamped.asc',g,delta)
        write_grid(out/'delta_unclamped.asc',g,unclamped)
        write_grid(out/'delta_clamping_effect.asc',g,delta-unclamped)
        mean_presence=lambda x:float(np.mean(x[tuple(rc.T)]))
        result.update(delta_mean_presence_resubstitution=mean_presence(delta),
            delta_median_presence_resubstitution=float(np.median(delta[tuple(rc.T)])),
            delta_mean_background=float(np.mean(delta[support])),
            delta_mean_presence_unclamped=mean_presence(unclamped),
            clamping_changes_delta_direction_cells=int(np.sum(support&(delta*unclamped<0))),
            clamping_changes_delta_by_more005_cells=int(np.sum(support&(abs(delta-unclamped)>.05))))
        presence_focus=focus[tuple(rc.T)]
        local=support&focus
        result['report_focus_n_presence_cells']=int(presence_focus.sum())
        result['report_focus_n_background_cells']=int(local.sum())
        if presence_focus.any():
            values=delta[tuple(rc.T)][presence_focus]
            result.update(report_focus_delta_mean_presence_resubstitution=float(values.mean()),
                report_focus_delta_median_presence_resubstitution=float(np.median(values)),
                report_focus_delta_mean_presence_unclamped=float(unclamped[tuple(rc.T)][presence_focus].mean()))
        if local.any():
            result['report_focus_delta_mean_background']=float(delta[local].mean())
            write_grid(out/'report_focus_delta.asc',g,np.where(local,delta,np.nan))
        threshold=float(np.quantile(a[tuple(rc.T)],.1))
        for label,value in [('current',a),('future',b)]:
            result[f'{label}_grid_area_above_training_p10_km2']=float(area[support&(value>=threshold)].sum())
            result[f'report_focus_{label}_grid_area_above_training_p10_km2']=float(area[local&(value>=threshold)].sum())
        for threshold_delta in [.025,.05,.1,.25]:
            suffix=str(threshold_delta)
            result[f'decrease_cells_{suffix}']=int(np.sum(support&(delta< -threshold_delta)))
            result[f'increase_cells_{suffix}']=int(np.sum(support&(delta>threshold_delta)))
        for group in ['ice','sst','precip']:
            key=f'only_{group}_clamped'
            if key in arrays:
                effect=arrays[key]-a
                write_grid(out/f'{group}_only_delta.asc',g,effect)
                result[f'{group}_only_delta_mean_presence']=mean_presence(effect)
                if presence_focus.any():
                    result[f'report_focus_{group}_only_delta_mean_presence']=float(effect[tuple(rc.T)][presence_focus].mean())
                if group=='ice':result['ice_only_increase_cells_005']=int(np.sum(support&(effect>.05)))
        dump(out/'commands.json',commands);dump(out/'metrics.json',result)
        return result
    results=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for done in as_completed([pool.submit(run,t) for t in tasks]):results.append(done.result())
    table(args.output/'model_metrics.csv',results)
    for setname in args.sets:
        stack=np.stack([aligned(g,args.output/setname/c/'delta_clamped.asc') for c in CANDIDATES])
        finite=np.where(support,stack,0)
        disagreement=(finite.min(0)<0)&(finite.max(0)>0)
        write_grid(args.output/setname/'structural_sign_disagreement.asc',g,np.where(support,disagreement,np.nan))
    dump(args.output/'interpretation.json',{
        'status':'exploratory structural sensitivity; no selected final model',
        'target':design['target'],'sst_quality_control_resolved':False,
        'n_gcm':1,'gcm':defs.get('gcm_label','IPSL'),'independent_climate_ensemble':False,
        'presence_delta':'full-fit/resubstitution, NOT independent validation',
        'isolated_predictor_changes':'statistical perturbations, not causal effects; contributions need not sum',
        'aicc':'raw prediction normalized over declared background support; n = distinct occupied cells; k = nonzero feature coefficients',
        'aicc_scope':'same domain and same presence sample only; descriptive, never replaces external validation',
        'threshold_areas':'full grid rectangles above training P10 score, NOT colony or habitat area',
        'report_focus':'aligned report_focus.asc when provided; statistics remain full-fit/resubstitution',
        'originals_overwritten':False})
    print(json.dumps({'full_models':len(results),'complete':True,'final_model_selected':False}))


if __name__=='__main__':main()
