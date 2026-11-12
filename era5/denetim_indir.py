"""Recover small, source-authenticated ERA5 monthly marine fields for audit.

No secrets are copied into the project. The request, source DOI and payload
checksum are recorded. Existing files are never overwritten. Daily phenology
must be requested separately: monthly fields cannot identify retreat dates.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import logging

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=ROOT / 'era5/veri_ham/denetim_20261112')
    parser.add_argument('--frequency', choices=['monthly','daily'], default='monthly')
    parser.add_argument('--request-id', help='Resume an already submitted CDS job; never resubmit it')
    parser.add_argument('--status-only', action='store_true')
    parser.add_argument('--area',type=float,nargs=4,default=[-66,-73,-70.5,-64],
                        metavar=('NORTH','WEST','SOUTH','EAST'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    target = args.output / f'marine_{args.frequency}_2000_2025.nc'
    receipt = args.output / f'receipt_{args.frequency}.json'
    if target.exists():
        raise FileExistsError('Existing raw payload is protected')
    request = {
        'product_type': ['monthly_averaged_reanalysis'],
        'variable': ['sea_surface_temperature', 'sea_ice_cover'],
        'year': [str(y) for y in range(2000, 2026)],
        'month': [f'{m:02d}' for m in range(1, 13)], 'time': ['00:00'],
        'area': args.area,
        'data_format': 'netcdf', 'download_format': 'unarchived',
    }
    dataset='reanalysis-era5-single-levels-monthly-means'
    if args.frequency=='daily':
        dataset='reanalysis-era5-single-levels'
        request['product_type']=['reanalysis']
        request['day']=[f'{d:02d}' for d in range(1,32)]
    record = {'dataset': dataset,
              'doi': '10.24381/cds.f17050d7' if args.frequency=='monthly' else '10.24381/cds.adbb2d47', 'request': request,
              'status': 'submitted', 'daily_phenology_available':args.frequency=='daily',
              'temporal_definition':'monthly means' if args.frequency=='monthly' else 'daily 00 UTC snapshot'}
    receipt.write_text(json.dumps(record, indent=2) + '\n')
    logging.getLogger('cdsapi').setLevel(logging.CRITICAL)
    logging.getLogger('ecmwf.datastores').setLevel(logging.CRITICAL)
    try:
        import cdsapi
        client = cdsapi.Client(quiet=True, progress=False, timeout=60,
                               retry_max=2, sleep_max=5)
        if args.request_id:
            remote=client.client.get_remote(args.request_id)
        else:
            remote=client.client.submit(collection_id=record['dataset'],request=request)
        record.update(request_id=remote.request_id,status=remote.status)
        receipt.write_text(json.dumps(record,indent=2)+'\n')
        if args.status_only:
            print(json.dumps({'request_id':remote.request_id,'status':record['status']}))
            return 0
        remote.download(str(target))
        record.update(status='downloaded', bytes=target.stat().st_size,
                      sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    except Exception as exc:
        # Deliberately omit exception text, URLs, headers and configuration.
        record.update(status='failed', error_type=type(exc).__name__)
        receipt.write_text(json.dumps(record, indent=2) + '\n')
        print(json.dumps({'status': 'failed', 'error_type': type(exc).__name__}))
        return 1
    receipt.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'status': record['status'], 'bytes': record['bytes']}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
