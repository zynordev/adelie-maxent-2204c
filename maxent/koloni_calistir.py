"""Checkpointed census-colony analysis, optionally waiting for queued CDS data.

Never submits another CDS request. A completed stage is reused only with an
identical command and script digest. Partial output directories are protected.
This computes sensitivity evidence; it never selects a validated final model.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

from revizyon_denetimi import ROOT,dump


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--results-root',type=Path,default=ROOT/'maxent/cikti/koloni_20261112')
    p.add_argument('--data-root',type=Path,default=ROOT/'maxent/girdi/koloni_20261112_run')
    p.add_argument('--wait-minutes',type=float,default=0)
    p.add_argument('--skip-oof',action='store_true',help='Leave future held-out projection stage explicitly pending')
    args=p.parse_args()
    results=args.results_root.resolve();data=args.data_root.resolve()
    results.mkdir(parents=True,exist_ok=True);data.mkdir(parents=True,exist_ok=True)
    ledger=results/'pipeline.json'
    record=json.loads(ledger.read_text()) if ledger.exists() else {
        'target':'MAPPPD positive nest-census colony occurrence, not abundance',
        'report_focus':'Marguerite Bay','final_model_selected':False,'stages':{}}
    raw=ROOT/'era5/veri_ham/peninsula_20261112/marine_monthly_2000_2025.nc'
    receipt_path=raw.parent/'receipt_monthly.json'
    def ready():
        if not raw.is_file() or not receipt_path.is_file():return False
        return json.loads(receipt_path.read_text()).get('status')=='downloaded'
    deadline=time.monotonic()+max(0,args.wait_minutes)*60
    while not ready():
        record.update(status='waiting_for_existing_CDS_job',source_ready=False,
                      request_id='fe4b03ad-fe98-4618-91e6-dbd4acc0d7d8')
        dump(ledger,record)
        if time.monotonic()>=deadline:
            print(json.dumps({'status':record['status'],'new_request_submitted':False}),flush=True)
            return 3
        time.sleep(min(30,max(0,deadline-time.monotonic())))
    if shutil.disk_usage(results).free<2*1024**3:
        raise RuntimeError('Need >=2 GiB free on results filesystem; choose another --results-root')
    record.update(status='running',source_ready=True)
    raw_sha=hashlib.sha256(raw.read_bytes()).hexdigest()
    if raw_sha!=json.loads(receipt_path.read_text()).get('sha256'):raise ValueError('ERA5 checksum disagrees with receipt')
    if 'ERA5_sha256' in record and record['ERA5_sha256']!=raw_sha:raise ValueError('ERA5 source changed')
    record['ERA5_sha256']=raw_sha;dump(ledger,record)
    python=str(ROOT/'.venv-cmip/bin/python')
    def run(stage,script,arguments,expected):
        cmd=[python,str(ROOT/script),*[str(a) for a in arguments]]
        digest=hashlib.sha256((json.dumps(cmd)+hashlib.sha256((ROOT/script).read_bytes()).hexdigest()).encode()).hexdigest()
        old=record['stages'].get(stage)
        if old:
            if old['digest']!=digest:raise ValueError(f'Stage code/settings changed: {stage}; use a fresh run root')
            if old['status']=='complete' and expected.is_file():return
            raise RuntimeError(f'Partial stage protected: {stage}; inspect logs and use fresh run roots')
        record['stages'][stage]={'status':'running','command':cmd,'digest':digest}
        dump(ledger,record);print(json.dumps({'stage':stage,'status':'running'}),flush=True)
        with (results/f'{stage}.log').open('w') as stream:
            result=subprocess.run(cmd,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
        status='complete' if result.returncode==0 and expected.is_file() else 'failed'
        record['stages'][stage].update(status=status,exit_code=result.returncode)
        dump(ledger,record)
        if status!='complete':raise RuntimeError(f'Stage failed: {stage}; inspect its log')
        print(json.dumps({'stage':stage,'status':status}),flush=True)
    layers=data/'current';future=data/'future'
    run('colony_inputs','maxent/koloni_hazirla.py',[
        '--raw',raw,'--output',layers,'--geometry-directory',ROOT/'maxent/girdi/koloni_geometry_20261112'],
        layers/'definitions.json')
    run('GCM_inputs','maxent/koloni_gelecek.py',['--layers',layers,'--raw',raw,'--output',future],
        future/'ice_baseline_comparison.csv')
    sets=['colony_ice','colony_sst_sensitivity']
    for bg,mask in [('rocky_coast','rocky_coastal_support.asc'),('target_group','target_group_support.asc')]:
        comp=results/f'CV_{bg}'
        run(f'CV_{bg}','maxent/revizyon_karsilastirma.py',[
            '--output',comp,'--layers',layers,'--samples-csv',layers/'colony_samples.csv',
            '--support-mask',layers/mask,'--sets',*sets,
            '--target-description',record['target'],'--background-description',bg],comp/'summary.csv')
        for gcm in ['IPSL','GFDL','MPI']:
            out=results/f'projection_{bg}_{gcm}'
            run(f'projection_{bg}_{gcm}','maxent/revizyon_projeksiyon.py',[
                '--output',out,'--comparison',comp,'--layers',future/gcm,'--sets',*sets],out/'model_metrics.csv')
        if not args.skip_oof:
            out=results/f'crossfit_{bg}'
            run(f'crossfit_{bg}','maxent/revizyon_oof.py',[
                '--output',out,'--comparison',comp,'--layers-template',str(future/'{gcm}'),
                '--sets',*sets],out/'summary.csv')
    record.update(status='analysis_complete_not_final_report',heldout_future_stage_skipped=args.skip_oof,
                  daily_phenology_pending=True,SST_physical_QC_resolved=False)
    dump(ledger,record)
    print(json.dumps({'status':record['status'],'final_model_selected':False}),flush=True)
    return 0


if __name__=='__main__':sys.exit(main())
