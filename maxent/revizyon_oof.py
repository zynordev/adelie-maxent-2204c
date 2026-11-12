"""Paired future-current changes at strictly held-out occurrence cells.

Future predictions have no future observations to validate against. Cross-fit
describes exclusion of current occurrence records from fitting, not validation
of future ecology. Repeated partition schemes are summarized separately.
"""
import argparse
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import shutil
import numpy as np

from izgara import read_grid, aligned
from revizyon_denetimi import dump, table
from revizyon_karsilastirma import ROOT,JAVA,CANDIDATES,java


def main():
    root=ROOT/'maxent/cikti/revizyon_20261112'
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--comparison',type=Path,default=root/'comparison_v3')
    p.add_argument('--output',type=Path,default=root/'crossfit_delta')
    p.add_argument('--layers-template',default=str(ROOT/'maxent/girdi/revizyon_{gcm}_20261112_v2'))
    p.add_argument('--sets',nargs='+',default=['annual','seasonal_no_sst'])
    args=p.parse_args()
    baseline=args.comparison;out=args.output
    out.mkdir(exist_ok=False)
    grid,_=read_grid(Path(args.layers_template.format(gcm='IPSL'))/'current/kaya.asc')
    focus_path=Path(args.layers_template.format(gcm='IPSL'))/'report_focus.asc'
    focus=aligned(grid,focus_path)>.5 if focus_path.is_file() else None
    designs=json.loads((baseline/'design.json').read_text())
    schemes=[d['scheme'] for d in designs['partitions'] if d['accepted']]
    tasks=[]
    for gcm in ['IPSL','GFDL','MPI']:
        layers=Path(args.layers_template.format(gcm=gcm))
        definitions=json.loads((layers/'definitions.json').read_text())
        for predictors in args.sets:
            for scheme in schemes:
                for fold in range(4):
                    for candidate in CANDIDATES:
                        source=baseline/predictors/scheme/f'fold{fold}'/candidate
                        tasks.append((gcm,predictors,scheme,fold,candidate,source,layers,
                                      definitions['predictor_sets'][predictors]))
    def project(task):
        gcm,predictors,scheme,fold,candidate,source,layers,names=task
        target=out/gcm/predictors/scheme/f'fold{fold}'/candidate
        env=target/'future_layers';env.mkdir(parents=True)
        for n in names:shutil.copyfile(layers/f'future_{gcm}'/f'{n}.asc',env/f'{n}.asc')
        command=[JAVA,'-Xmx128m','-Djava.awt.headless=true','-cp',str(ROOT/'maxent/maxent.jar'),
            'density.Project',str(source/'Pygoscelis_adeliae.lambdas'),str(env),str(target/'future.asc'),
            'outputformat=cloglog','doclamp=true','extrapolate=true']
        java(command,target/'project.log')
        future=aligned(grid,target/'future.asc')
        current=aligned(grid,source/'test_projection.asc')
        records=list(csv.DictReader((source/'heldout_scores.csv').open()))
        result=[]
        for r in records:
            row,col=int(r['row']),int(r['col'])
            if not np.isclose(current[row,col],float(r['score']),rtol=0,atol=1e-10):
                raise ValueError('Current prediction and saved heldout score differ')
            result.append(dict(gcm=gcm,predictors=predictors,scheme=scheme,fold=fold,candidate=candidate,
                **{k:v for k,v in r.items() if k in ['gbifID','sample_id']},row=row,col=col,current=float(current[row,col]),
                future=float(future[row,col]),delta=float(future[row,col]-current[row,col]),
                report_focus=bool(focus[row,col]) if focus is not None else True))
        dump(target/'command.json',command)
        return result
    results=[]
    with ThreadPoolExecutor(max_workers=6) as pool:
        for i,done in enumerate(as_completed([pool.submit(project,t) for t in tasks]),1):
            results.extend(done.result())
            if i%100==0:print(json.dumps({'paired_projections':i,'total':len(tasks)}),flush=True)
    table(out/'heldout_delta.csv',results)
    summary=[]
    for gcm in ['IPSL','GFDL','MPI']:
        for predictors in args.sets:
            for scheme in schemes:
                for candidate in CANDIDATES:
                    rows=[r for r in results if r['gcm']==gcm and r['predictors']==predictors and
                          r['scheme']==scheme and r['candidate']==candidate]
                    if len(rows)!=designs['n_presence_cells'] or len(set((r['row'],r['col']) for r in rows))!=len(rows):
                        raise ValueError('Heldout occurrence cells must occur exactly once per scheme')
                    d=np.array([r['delta'] for r in rows])
                    summary.append(dict(gcm=gcm,predictors=predictors,scheme=scheme,candidate=candidate,
                        n_unique_heldout_cells=len(rows),delta_mean=float(d.mean()),delta_median=float(np.median(d)),
                        delta_q10=float(np.quantile(d,.1)),delta_q90=float(np.quantile(d,.9)),
                        fraction_below_minus005=float(np.mean(d<-.05)),fraction_above005=float(np.mean(d>.05))))
    table(out/'summary.csv',summary)
    local_summary=[]
    if focus is not None:
        for original in summary:
            rows=[r for r in results if r['report_focus'] and all(r[k]==original[k]
                for k in ['gcm','predictors','scheme','candidate'])]
            if not rows:continue
            if len({(r['row'],r['col']) for r in rows})!=len(rows):raise ValueError('Duplicated local heldout cells')
            d=np.array([r['delta'] for r in rows])
            local_summary.append(dict(**{k:original[k] for k in ['gcm','predictors','scheme','candidate']},
                n_unique_heldout_cells=len(rows),delta_mean=float(d.mean()),delta_median=float(np.median(d)),
                delta_q10=float(np.quantile(d,.1)),delta_q90=float(np.quantile(d,.9))))
        table(out/'report_focus_summary.csv',local_summary)
    dump(out/'interpretation.json',{'n_paired_projections':len(tasks),
        'target':designs['target'],
        'future_validation':False,'clamping':True,'new_model_training':False,
        'repeated_schemes':f'same {designs["n_presence_cells"]} occurrence cells; never pooled as independent observations'})
    print(json.dumps({'complete':True,'n_projections':len(tasks)}))


if __name__=='__main__':main()
