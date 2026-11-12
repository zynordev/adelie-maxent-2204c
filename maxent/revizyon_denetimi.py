"""Reproducible, non-destructive audit before ecological model refitting.

Outputs are diagnostic evidence, never a validated ecological M or final model.
Run with .venv-cmip/bin/python maxent/revizyon_denetimi.py --output PATH.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import struct

import numpy as np
from pyproj import Transformer
from scipy.ndimage import label
import shapely
from shapely.geometry import box, Point
from shapely.ops import transform, unary_union

from izgara import read_grid, aligned, write_grid, cell_areas_km2

ROOT = Path(__file__).resolve().parents[1]


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2,
                               allow_nan=False) + '\n')


def table(path, rows):
    if not rows:
        return
    with path.open('w', newline='') as stream:
        fields=list(dict.fromkeys(k for row in rows for k in row))
        w = csv.DictWriter(stream, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def gpkg_geometry(blob):
    """Decode OGC GeoPackage binary header before parsing WKB."""
    if blob[:2] != b'GP':
        raise ValueError('Not GeoPackage binary')
    envelope = (blob[3] >> 1) & 7
    size = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}.get(envelope)
    if size is None:
        raise ValueError('Unsupported geometry envelope')
    return shapely.from_wkb(blob[8 + size:])


def vif_values(matrix, names):
    """VIF with intercept, calculated on explicit complete-case domain."""
    x = np.asarray(matrix, float)
    if x.ndim != 2 or len(x) < x.shape[1] + 2 or not np.isfinite(x).all():
        raise ValueError('Invalid VIF design')
    sd=x.std(0);constant=sd<=np.finfo(float).eps
    z=(x-x.mean(0))/np.where(constant,1,sd)
    result = []
    for j, name in enumerate(names):
        if constant[j]:
            result.append({'variable':name,'n_cells':len(z),'vif':None,
                           'singular':True,'constant':True})
            continue
        others=(np.arange(x.shape[1])!=j)&~constant
        design = np.column_stack([np.ones(len(z)), z[:,others]])
        error = z[:, j] - design @ np.linalg.lstsq(design, z[:, j], rcond=None)[0]
        unexplained = np.sum(error ** 2) / np.sum(z[:, j] ** 2)
        result.append({'variable': name, 'n_cells': len(z),
                       'vif': float(1 / unexplained) if unexplained > 1e-12 else None,
                       'singular': bool(unexplained <= 1e-12),'constant':False})
    return result


def mess(reference, target):
    """Univariate percentile MESS minimum; multivariate novelty not inferred."""
    reference, target = np.asarray(reference), np.asarray(target)
    if reference.ndim != 2 or target.shape[-1] != reference.shape[1]:
        raise ValueError('MESS column mismatch')
    if not np.isfinite(reference).all() or not np.isfinite(target).all():
        raise ValueError('MESS requires finite data')
    scores = []
    for j in range(reference.shape[1]):
        values = np.sort(reference[:, j]); lo, hi = values[0], values[-1]
        t = target[..., j]
        if hi == lo:
            scores.append(np.where(t == lo, 100., -100.))
            continue
        rank = (np.searchsorted(values, t, side='left') +
                np.searchsorted(values, t, side='right')) / (2 * len(values))
        inside = 200 * np.minimum(rank, 1 - rank)
        score = np.where(t < lo, 100 * (t - lo) / (hi - lo), inside)
        score = np.where(t > hi, 100 * (hi - t) / (hi - lo), score)
        scores.append(score)
    return np.min(scores, axis=0)


def audit(out):
    if out.exists():
        raise FileExistsError('Choose a fresh output directory')
    out.mkdir(parents=True)
    used = []
    def use(path):
        path = ROOT / path; used.append(path); return path
    names = ['bio18', 'buz_yillik', 'kaya', 'sst_yillik']
    grid, first = read_grid(use('maxent/girdi/katmanlar/bio18.asc'))
    layers = {names[0]: first}
    for name in names[1:]:
        layers[name] = aligned(grid, use(f'maxent/girdi/katmanlar/{name}.asc'))
    lat = grid.yllcorner + (grid.nrows - np.arange(grid.nrows) - .5) * grid.cellsize
    lon = grid.xllcorner + (np.arange(grid.ncols) + .5) * grid.cellsize
    xx, yy = np.meshgrid(lon, lat)
    rows = []
    for folder in ['deneme3', 'deneme_2050']:
        for p in sorted((ROOT / 'maxent/cikti' / folder).glob('*.html')):
            text = p.read_text(); found = re.search(r'Feature types used: ([^<]+)', text)
            if found:
                used.append(p)
                rows.append({'file': str(p.relative_to(ROOT)), 'features': found[1].strip()})
    table(out / 'actual_features.csv', rows)
    raw_sst = aligned(grid, use('era5/output/ham/sst_yillik.asc'))
    raw_ice = aligned(grid, use('era5/output/ham/buz_yillik.asc'))
    ocean = np.isfinite(raw_sst) & np.isfinite(raw_ice)
    sst_bad = np.isfinite(raw_sst) & (raw_sst < -2.0)
    table(out / 'sst_suspect_cells.csv', [
        {'row': int(r), 'col': int(c), 'latitude': float(yy[r,c]),
         'longitude': float(xx[r,c]), 'sst_c': float(raw_sst[r,c]),
         'ice_percent': float(raw_ice[r,c])} for r,c in zip(*np.nonzero(sst_bad))])
    c = sqlite3.connect(use('harita/qgis_katmanlari.gpkg'))
    coast = {kind: unary_union([gpkg_geometry(b[0]) for b in c.execute(
        'select geom from kiyi where surface=?', (kind,))]) for kind in ['land', 'ice shelf']}
    c.close()
    project = Transformer.from_crs(4326, 3031, always_xy=True).transform
    equal = Transformer.from_crs(4326,
        '+proj=laea +lat_0=-90 +lon_0=0 +datum=WGS84 +units=m', always_xy=True).transform
    from_polar = Transformer.from_crs(3031,
        '+proj=laea +lat_0=-90 +lon_0=0 +datum=WGS84 +units=m', always_xy=True).transform
    equal_coast = {k: transform(from_polar, v) for k,v in coast.items()}
    covered_coast = unary_union(list(equal_coast.values()))
    fractions = {k: np.zeros_like(first) for k in coast}
    fractions['open_marine'] = np.zeros_like(first)
    cell_polygons = {}
    for r in range(grid.nrows):
        for col in range(grid.ncols):
            poly = box(xx[r,col]-.125, yy[r,col]-.125,
                       xx[r,col]+.125, yy[r,col]+.125).segmentize(.01)
            ep = transform(equal, poly); cell_polygons[r,col] = ep
            for k, geo in equal_coast.items():
                fractions[k][r,col] = ep.intersection(geo).area / ep.area
            covered = ep.intersection(covered_coast).area / ep.area
            fractions['open_marine'][r,col] = max(0, 1-covered)
    for k,a in fractions.items():
        write_grid(out / (k.replace(' ', '_') + '_fraction.asc'), grid, a)
    # These are measurement-support diagnostics. They are not a final accessible M.
    marine_support = ocean & (fractions['open_marine'] >= .5)
    coastal_support = marine_support | ((layers['kaya'] > 0) & (fractions['ice shelf'] < .5))
    for name,mask in [('raw_ocean',ocean), ('marine_support',marine_support),
                      ('coastal_support',coastal_support)]:
        write_grid(out / f'{name}.asc', grid, mask.astype(float))
    vif = []
    for domain, mask in [('rectangle',np.ones_like(ocean)),('raw_ocean',ocean),
                         ('marine_support', marine_support),('coastal_support', coastal_support)]:
        x = np.column_stack([layers[n][mask] for n in names])
        vif.extend(dict(domain=domain, **v) for v in vif_values(x,names))
        corr = np.corrcoef(x, rowvar=False)
        table(out/f'correlation_{domain}.csv', [dict(variable=n, **{
            names[k]:float(corr[j,k]) for k in range(len(names))}) for j,n in enumerate(names)])
    table(out/'vif.csv', vif)
    with use('gbif/temiz/kayitlar_temiz.csv').open() as f:
        records = list(csv.DictReader(f))
    groups = []
    for rec in records:
        point = Point(*project(float(rec['decimalLongitude']),float(rec['decimalLatitude'])))
        location = ('ice_shelf' if coast['ice shelf'].covers(point) else
                    'land' if coast['land'].covers(point) else 'marine')
        evidence = ' '.join([rec.get('locality',''),rec.get('occurrenceID','')]).lower()
        # No point is inferred to be a breeding colony merely from its position.
        groups.append(dict(gbifID=rec['gbifID'], surface=location, year=rec['year'],
            basisOfRecord=rec['basisOfRecord'], breeding_verified=False,
            explicit_breeding_text=any(x in evidence for x in ['breeding','colony','nesting']),
            uncertainty_missing=not bool(rec['coordinateUncertaintyInMeters']),
            datasetKey=rec['datasetKey']))
    table(out/'record_evidence.csv',groups)
    analysis=ROOT/'maxent/cikti/cmip6_ipsl_ssp245_2041_2060_v1'
    delta=aligned(grid,use(analysis/'uygunluk_farki.asc'))
    novelty=aligned(grid,use(analysis/'ekstrapolasyon.asc'))>0
    disagreement=aligned(grid,use(analysis/'isaret_belirsiz.asc'))>0
    clamp=aligned(grid,use(analysis/'clamping_max.asc'))>0
    areas=cell_areas_km2(grid)
    components,n=label(delta>.05)
    overlaps=[]
    for index in range(1,n+1):
        m=components==index
        overlaps.append(dict(component=index,cells=int(m.sum()),
            latitude_min=float(yy[m].min()),latitude_max=float(yy[m].max()),
            area_grid_km2=float(areas[m].sum()),
            range_novel_cells=int((m&novelty).sum()),
            sign_disagreement_cells=int((m&disagreement).sum()),
            clamp_effect_cells=int((m&clamp).sum()),
            raw_ocean_cells=int((m&ocean).sum()),
            mean_shelf_fraction=float(fractions['ice shelf'][m].mean())))
    table(out/'legacy_increase_components.csv',overlaps)
    future=np.stack([aligned(grid,use(f'maxent/girdi/cmip6_ipsl_ssp245_2041_2060_v1/{n}.asc'))
                     for n in names],axis=-1)
    reference=np.column_stack([layers[n].ravel() for n in names])
    write_grid(out/'legacy_mess.asc',grid,mess(reference,future))
    summary={
        'purpose':'source and design audit; no final model selection',
        'features_in_original_folds':sorted(set(r['features'] for r in rows)),
        'sst_raw_ocean_min_c':float(np.nanmin(raw_sst)),
        'sst_raw_below_minus2_cells':int(sst_bad.sum()),
        'sst_bad_is_from_unfilled_grid':True,
        'raw_source_monthly_files_present':(ROOT/'era5/veri_ham/aylik/sst_2000_2025.nc').exists(),
        'n_raw_ocean_cells':int(ocean.sum()),
        'n_marine_support_cells':int(marine_support.sum()),
        'n_coastal_support_cells':int(coastal_support.sum()),
        'clean_records':len(records),
        'record_surface_counts':{k:sum(r['surface']==k for r in groups)
                                 for k in ['land','marine','ice_shelf']},
        'records_2026':sum(r['year']=='2026' for r in records),
        'verified_breeding_records_from_existing_metadata':0,
        'legacy_increase_cells':int((delta>.05).sum()),
        'legacy_increase_novel_cells':int(((delta>.05)&novelty).sum()),
        'legacy_increase_disagreement_cells':int(((delta>.05)&disagreement).sum()),
        'legacy_domain_area_km2':float(areas.sum()),
        'mask_status':'candidate support masks based on existing SCAR polygon; ecological M not finalized',
        'scientific_gate':'SST source audit and record evidence must precede a new ecological conclusion',
    }
    dump(out/'summary.json',summary)
    dump(out/'manifest.json',{'inputs':{str(p.relative_to(ROOT)):
        hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(used))},
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'outputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in out.iterdir() if p.is_file()},
        'protected_originals_overwritten':False})
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT/'maxent/cikti/revizyon_20261112/denetim')
    audit(p.parse_args().output)
