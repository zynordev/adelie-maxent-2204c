#!/usr/bin/env python3
"""Prepare an explicitly hypothetical sensitivity experiment, never CMIP6.

Legacy input files are preserved. New outputs use a separate directory.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from izgara import read_grid, write_grid

ROOT = Path(__file__).resolve().parents[1]


def transform_values(data,transform):
    valid=np.isfinite(data);result=data.copy()
    if transform['operation']=='add':result[valid]+=transform['value']
    elif transform['operation']=='multiply':result[valid]*=transform['value']
    elif transform['operation']!='identity':raise ValueError('Unknown transformation')
    if 'clip' in transform:result[valid]=np.clip(result[valid],*transform['clip'])
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'maxent/girdi/duyarlilik_delta_v1')
    args=parser.parse_args()
    scenario=json.loads((ROOT/'maxent/senaryo_duyarlilik.json').read_text())
    if scenario['kind']!='hypothetical_sensitivity':
        raise ValueError('Only hypothetical experiments supported')
    if args.output.resolve()==(ROOT/scenario['legacy_input_directory']).resolve():
        raise ValueError('Original inputs are immutable; choose a new directory')
    args.output.mkdir(parents=True,exist_ok=True)
    manifest={'scenario':scenario,'inputs':[],'outputs':[]}
    reference=None
    for name,transform in scenario['transformations'].items():
        source=ROOT/f'maxent/girdi/katmanlar/{name}.asc'
        g,data=read_grid(source)
        if reference is not None and not reference.compatible(g):
            raise ValueError('Input grids differ')
        reference=g
        result=transform_values(data,transform)
        dest=args.output/f'{name}.asc'
        write_grid(dest,g,result)
        for category,path in [('inputs',source),('outputs',dest)]:
            manifest[category].append({'path':str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
                'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (args.output/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    print(scenario['warning_tr'])
    print(args.output)


if __name__=='__main__':main()
