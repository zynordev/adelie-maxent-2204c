"""Record public-input and code hashes and package versions, never credentials."""
import argparse
from datetime import datetime,timezone
import hashlib
from importlib.metadata import version,PackageNotFoundError
import json
from pathlib import Path
import platform
import subprocess

from revizyon_denetimi import ROOT,dump


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    if args.output.exists():raise FileExistsError('Existing manifest protected; use a new filename')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    patterns=['maxent/revizyon_*.py','maxent/koloni_*.py','maxent/cmip6_cokdosya.py',
              'maxent/izgara.py','maxent/mekansal_dogrulama.py','maxent/cmip6_erisim_kontrolu.py',
              'maxent/test_*.py','era5/denetim_indir.py','gbif/revizyon_kaynaklari.py',
              'gbif/koloni_denetimi.py','harita/bas_kaynak_indir.py','maxent/maxent.jar',
              'gbif/veri_ham/revizyon_20261112/*','harita/veri_ham/revizyon_20261112/*',
              'era5/veri_ham/denetim_20261112/*','era5/veri_ham/peninsula_20261112/*',
              'maxent/girdi/cmip6_peninsula_20261112/*/receipt.json',
              'maxent/girdi/cmip6_peninsula_20261112/*/*klimatoloji.npz']
    inputs=[]
    for path in sorted({p for glob in patterns for p in ROOT.glob(glob) if p.is_file()}):
        # No shell environment, home config or private credentials are inspected.
        inputs.append({'path':str(path.relative_to(ROOT)),'bytes':path.stat().st_size,
                       'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    packages={}
    for name in ['numpy','scipy','xarray','pydap','cftime','requests','h5netcdf','h5py',
                 'shapely','pyproj','matplotlib','cdsapi','ecmwf-datastores-client']:
        try:packages[name]=version(name)
        except PackageNotFoundError:packages[name]=None
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    dump(args.output,{'timestamp_UTC':datetime.now(timezone.utc).isoformat(),'base_commit':commit,
        'worktree_committed':False,'python':platform.python_version(),'packages':packages,
        'inputs':inputs,'MAPPPD_version':'5.0','MAPPPD_license':'CC BY 4.0',
        'SST_QC_resolved':False,'daily_phenology_ready':(ROOT/'era5/veri_ham/denetim_20261112/marine_daily_2000_2025.nc').is_file(),
        'source_snapshots_not_refreshed':True,'final_report_released':False})
    print(json.dumps({'manifest_files':len(inputs),'output':str(args.output)}))


if __name__=='__main__':main()
