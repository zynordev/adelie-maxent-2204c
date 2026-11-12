"""Fixed-candidate spatial sensitivity benchmark with geographic baselines.

This evaluates provisional overall occurrence, not breeding colonies. No winner
is selected on these test folds. Regional resampling intervals are conditional
on each fixed partition and are not population confidence intervals.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import json
from pathlib import Path
import subprocess
import shutil

import numpy as np
from pyproj import Transformer
from scipy.optimize import minimize
from scipy.stats import spearmanr
from scipy.spatial import cKDTree

from izgara import read_grid, aligned, write_grid, cell_areas_km2
from mekansal_dogrulama import band_partition, cells
from revizyon_denetimi import dump, table, mess, vif_values

ROOT=Path(__file__).resolve().parents[1]
JAVA='/usr/lib/jvm/java-21-openjdk/bin/java'
CANDIDATES={'L_RM1':('L',1),'LQ_RM1':('LQ',1),'LQ_RM2':('LQ',2),
            'LQH_RM1':('LQH',1),'LQH_RM2':('LQH',2)}


def feature_args(fc):
    return ['autofeature=false', *[f'{key}={str(token in fc).lower()}' for key,token in
        [('linear','L'),('quadratic','Q'),('hinge','H'),('threshold','T'),('product','P')]]]


def auc(p,b):
    d=np.asarray(p)[:,None]-np.asarray(b)[None,:]
    return float(np.mean((d>0)+.5*(d==0)))


def score_metrics(train,test,bg):
    train,test,bg=map(np.asarray,(train,test,bg))
    if any(not len(x) or not np.isfinite(x).all() for x in (train,test,bg)):
        raise ValueError('Invalid evaluation scores')
    q=float(np.quantile(train,.1))
    lo,hi=min(bg.min(),test.min()),max(bg.max(),test.max())
    boyce=None
    if hi>lo:
        edges=np.linspace(lo,hi,11)
        p=np.histogram(test,edges)[0]/len(test)
        e=np.histogram(bg,edges)[0]/len(bg)
        valid=e>0
        ratios=p[valid]/e[valid];centres=(edges[:-1]+edges[1:])[valid]/2
        if len(ratios)>2 and np.ptp(ratios)>0:
            boyce=float(spearmanr(centres,ratios).statistic)
    thresholds=np.r_[np.inf,np.sort(np.unique(np.r_[test,bg]))[::-1],-np.inf]
    fpr=np.array([np.mean(bg>=v) for v in thresholds])
    tpr=np.array([np.mean(test>=v) for v in thresholds])
    # Explicit diagnostic definition: integrate ROC above sensitivity .95.
    start=np.flatnonzero(tpr>=.95)[0]
    if start>0 and tpr[start]>.95:
        fraction=(.95-tpr[start-1])/(tpr[start]-tpr[start-1])
        x0=fpr[start-1]+fraction*(fpr[start]-fpr[start-1])
        xs=np.r_[x0,fpr[start:]];ys=np.r_[.95,tpr[start:]]
    else:
        xs=fpr[start:];ys=tpr[start:]
    denominator=(1-xs[0]**2)/2
    ratio=float(np.trapezoid(ys,xs)/denominator) if denominator>0 else None
    return {'auc':auc(test,bg),'omission_p10':float(np.mean(test<q)),
            'training_threshold_p10':q,'boyce_fixed_10_bins':boyce,
            'partial_roc_ratio_sensitivity95':ratio,'n_test':len(test),'n_test_background':len(bg)}


def geographic_scores(trainxy,allxy,trainbgxy):
    nearest=-cKDTree(trainxy).query(allxy)[0]
    # Position-only reference, fitted using training data/background only.
    x=np.r_[trainxy,trainbgxy]; y=np.r_[np.ones(len(trainxy)),np.zeros(len(trainbgxy))]
    mu=x.mean(0);sd=x.std(0)
    z=np.column_stack([np.ones(len(x)),(x-mu)/sd])
    def objective(beta):
        eta=z@beta
        value=np.logaddexp(0,eta).sum()-y@eta+1e-3*np.sum(beta[1:]**2)
        probability=1/(1+np.exp(-np.clip(eta,-700,700)))
        grad=z.T@(probability-y)+np.r_[0,2e-3*beta[1:]]
        return value,grad
    fit=minimize(objective,np.zeros(3),jac=True,method='BFGS',options={'gtol':1e-6})
    if not fit.success and np.linalg.norm(fit.jac)>1e-3:
        raise RuntimeError('Geographic reference optimization failed')
    prediction=np.column_stack([np.ones(len(allxy)),(allxy-mu)/sd])@fit.x
    return {'distance_null':nearest,'coordinates_reference':prediction}


def java(command,log):
    with log.open('w') as stream:
        result=subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT,timeout=180,cwd=ROOT)
    if result.returncode:
        raise RuntimeError(f'Java failure; inspect {log}')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT/'maxent/cikti/revizyon_20261112/comparison')
    p.add_argument('--layers',type=Path,default=ROOT/'maxent/girdi/revizyon_20261112')
    p.add_argument('--audit',type=Path,default=ROOT/'maxent/cikti/revizyon_20261112/denetim_v2')
    p.add_argument('--sets',nargs='+',default=['annual','seasonal_no_sst'])
    p.add_argument('--samples-csv',type=Path,help='Explicit census-only cell representatives; bypass GBIF selection')
    p.add_argument('--support-mask',type=Path,help='Explicit aligned background support; presence cells retained')
    p.add_argument('--target-description',default='provisional overall occurrence; breeding not inferred')
    p.add_argument('--background-description',default='uniform valid coastal support cells')
    p.add_argument('--workers',type=int,default=4)
    args=p.parse_args()
    if args.output.exists():raise FileExistsError('Use a fresh output directory')
    args.output.mkdir(parents=True)
    definitions=json.loads((args.layers/'definitions.json').read_text())
    g,kaya=read_grid(args.layers/'current/kaya.asc')
    support=aligned(g,args.support_mask or args.audit/'coastal_support.asc')>.5
    if args.samples_csv:
        records=list(csv.DictReader(args.samples_csv.open()))
    else:
        with (ROOT/'gbif/temiz/kayitlar_temiz.csv').open() as f: records=list(csv.DictReader(f))
        records=[r for r in records if 2000<=int(r['year'])<=2025]
    h={'nrows':g.nrows,'ncols':g.ncols,'xllcorner':g.xllcorner,'yllcorner':g.yllcorner,'cellsize':g.cellsize}
    def key(r):
        if args.samples_csv:return str(r['sample_id'])
        return (float(r['coordinateUncertaintyInMeters'] or 'inf'),int(r['gbifID']))
    selected={};excluded=[]
    for r in sorted(records,key=key):
        x,y=('longitude','latitude') if args.samples_csv else ('decimalLongitude','decimalLatitude')
        row,col=cells([[float(r[x]),float(r[y])]],h)[0]
        if not (0<=row<g.nrows and 0<=col<g.ncols):raise ValueError('Presence outside grid')
        if support[row,col]:selected.setdefault((row,col),r)
        else:excluded.append(r)
    if args.samples_csv and excluded:raise ValueError('Both backgrounds must retain identical census presence cells')
    rc=np.array(sorted(selected));n=len(rc)
    if n<25:raise ValueError('Too few occupied cells for the specified four-fold design')
    lon,lat=np.meshgrid(g.xllcorner+(np.arange(g.ncols)+.5)*g.cellsize,
                       g.yllcorner+(g.nrows-np.arange(g.nrows)-.5)*g.cellsize)
    project=Transformer.from_crs(4326,3031,always_xy=True)
    px,py=project.transform(lon,lat);xy=np.column_stack([px.ravel(),py.ravel()])/1000
    presence_flat=np.ravel_multi_index(rc.T,support.shape)
    samples=[dict(species='Pygoscelis_adeliae',longitude=lon[r,c],latitude=lat[r,c],
                  **({'sample_id':selected[r,c]['sample_id']} if args.samples_csv else
                     {'gbifID':selected[r,c]['gbifID']})) for r,c in rc]
    table(args.output/'representatives.csv',samples)
    designs={}
    for axis,j in [('latitude',0),('longitude',1)]:
        _,meta=band_partition(rc[:,j],4)
        coords=np.indices(support.shape)[j]
        designs[axis]=np.searchsorted(meta['cuts_grid_index'],coords,side='right')
    for width,offset in [(40,0),(40,.5),(80,0),(80,.5)]:
        a=np.floor(px/(width*1000)+offset).astype(int)
        b=np.floor(py/(width*1000)+offset).astype(int)
        designs[f'checker_{width}km_shift{offset}']=(a%2)+2*(b%2)
    design_info=[];valid_designs={}
    for name,labels in designs.items():
        count=np.bincount(labels[tuple(rc.T)],minlength=4)
        accepted=bool((count>=5).all() and (n-count>=20).all())
        design_info.append({'scheme':name,'test_counts':count.tolist(),'accepted':accepted,
            'rule':'at least 5 heldout and 20 training presence cells; fixed before model scores'})
        write_grid(args.output/f'partition_{name}.asc',g,labels.astype(float))
        if accepted:valid_designs[name]=labels
    dump(args.output/'design.json',{'target':args.target_description,
        'record_years':[2000,2025],'n_presence_cells':n,'n_background_cells':int(support.sum()),
        'presence_cells_in_background':True,'background':args.background_description,
        'support_mask':str((args.support_mask or args.audit/'coastal_support.asc').resolve()),
        'bias_correction':'background-design sensitivity, not proof observation bias removed',
        'validation_background':'heldout spatial region only',
        'training_background':'heldout spatial region excluded',
        'candidate_selection':'fixed grid; no winner selected, no test-fold tuning',
        'models':CANDIDATES,'partitions':design_info,
        'small_sample_warning':'per-fold Boyce and partial ROC diagnostic; unstable with small test samples',
        'interval':'paired spatial-fold cluster resampling, conditional on scheme; not independent repeated datasets',
        'originals_modified':False})
    area=cell_areas_km2(g)
    jobs=[];results=[];commands=[]
    for setname in args.sets:
        names=definitions['predictor_sets'][setname]
        features={n:aligned(g,args.layers/'current'/f'{n}.asc') for n in names}
        for scheme,labels in valid_designs.items():
            for fold in range(4):
                testid=np.flatnonzero(labels[tuple(rc.T)]==fold)
                trainid=np.flatnonzero(labels[tuple(rc.T)]!=fold)
                trainmask=support&(labels!=fold);testmask=support&(labels==fold)
                base=args.output/setname/scheme/f'fold{fold}';base.mkdir(parents=True)
                env=base/'training_layers';env.mkdir()
                full=base/'projection_layers';full.mkdir()
                for name,a in features.items():
                    write_grid(env/f'{name}.asc',g,np.where(trainmask,a,np.nan))
                    write_grid(full/f'{name}.asc',g,np.where(support,a,np.nan))
                table(base/'train.csv',[{k:samples[i][k] for k in ['species','longitude','latitude']} for i in trainid])
                table(base/'test.csv',[samples[i] for i in testid])
                null=geographic_scores(xy[presence_flat[trainid]],xy,xy[trainmask.ravel()])
                for name,score in null.items():
                    results.append(dict(predictors=setname,scheme=scheme,fold=fold,candidate=name,
                        **score_metrics(score[presence_flat[trainid]],score[presence_flat[testid]],score[testmask.ravel()])))
                table(base/'training_vif.csv',[dict(scope='training_background',**r) for r in
                    vif_values(np.column_stack([features[n][trainmask] for n in names]),names)])
                for candidate,(fc,rm) in CANDIDATES.items():
                    jobs.append((setname,scheme,fold,candidate,fc,rm,base,env,full,features,trainmask,testmask,trainid,testid))

    def fit(job):
        setname,scheme,fold,candidate,fc,rm,base,env,full,features,trainmask,testmask,trainid,testid=job
        out=base/candidate;out.mkdir();(out/'plots').mkdir()
        # MaxEnt writes .mxe caches next to input layers. Each worker requires
        # its own cache directory, even when the ASCII values are identical.
        private_env=out/'training_layers';private_env.mkdir()
        for path in env.glob('*.asc'):
            shutil.copyfile(path,private_env/path.name)
        command=[JAVA,'-Xmx256m','-Djava.awt.headless=true','-jar',str(ROOT/'maxent/maxent.jar'),
            '-z','autorun',f'samplesfile={base/"train.csv"}',f'environmentallayers={private_env}',
            f'outputdirectory={out}',*feature_args(fc),f'betamultiplier={rm}',
            'maximumbackground=10000','addsamplestobackground=false','removeduplicates=false',
            'randomseed=false','threads=1','outputformat=cloglog','outputfiletype=asc',
            'plots=false','responsecurves=false','jackknife=false','visible=false','warnings=false']
        java(command,out/'train.log')
        projection=[JAVA,'-Djava.awt.headless=true','-cp',str(ROOT/'maxent/maxent.jar'),
            'density.Project',str(out/'Pygoscelis_adeliae.lambdas'),str(full),str(out/'test_projection.asc'),
            'outputformat=cloglog','doclamp=true','extrapolate=true']
        java(projection,out/'projection.log')
        score=aligned(g,out/'test_projection.asc')
        tr=score[tuple(rc[trainid].T)];te=score[tuple(rc[testid].T)];bg=score[testmask]
        metrics=score_metrics(tr,te,bg)
        x=np.column_stack([features[n][trainmask] for n in features])
        novel=mess(x,np.stack([features[n][testmask] for n in features],axis=-1))<0
        metrics.update(test_novel_fraction=float(np.mean(novel)),
                       test_area_fraction_above_training_p10=float(
                           area[testmask][bg>=metrics['training_threshold_p10']].sum()/area[testmask].sum()))
        row=dict(predictors=setname,scheme=scheme,fold=fold,candidate=candidate,**metrics)
        table(out/'heldout_scores.csv',[dict(**{k:v for k,v in samples[i].items() if k in ['gbifID','sample_id']},
                    score=float(s),row=int(rc[i,0]),col=int(rc[i,1])) for i,s in zip(testid,te)])
        dump(out/'commands.json',[command,projection])
        return row
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        pending=[pool.submit(fit,job) for job in jobs]
        for i,result in enumerate(as_completed(pending),1):
            results.append(result.result())
            table(args.output/'fold_metrics.csv',results)
            if i%10==0 or i==len(jobs):print(json.dumps({'fits_completed':i,'total':len(jobs)}),flush=True)
    summary=[];rng=np.random.default_rng(20261112)
    for setname in args.sets:
        for scheme in valid_designs:
            null=np.array([r['auc'] for r in results if r['predictors']==setname and
                r['scheme']==scheme and r['candidate']=='distance_null'])
            for candidate in [*CANDIDATES,'distance_null','coordinates_reference']:
                rows=sorted([r for r in results if r['predictors']==setname and r['scheme']==scheme and
                    r['candidate']==candidate],key=lambda r:r['fold'])
                a=np.array([r['auc'] for r in rows]);diff=a-null
                draws=diff[rng.integers(0,len(diff),(2000,len(diff)))].mean(1)
                summary.append(dict(predictors=setname,scheme=scheme,candidate=candidate,
                    auc_mean=float(a.mean()),auc_sd=float(a.std(ddof=1)),
                    omission_pooled=sum(r['omission_p10']*r['n_test'] for r in rows)/sum(r['n_test'] for r in rows),
                    auc_minus_distance_null=float(diff.mean()),
                    paired_block_resampling_q025=float(np.quantile(draws,.025)),
                    paired_block_resampling_q975=float(np.quantile(draws,.975))))
    table(args.output/'summary.csv',summary)
    print(json.dumps({'complete':True,'fits':len(jobs),'presence_cells':n,
                      'schemes':list(valid_designs),'winner_selected':False}),flush=True)


if __name__=='__main__':main()
