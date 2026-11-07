#!/usr/bin/env python3
"""Public CMIP6 catalog/metadata/time audit; never creates climate rasters.

The catalog audit uses Python's standard library and an existing system
libblosc (ctypes). Optional --regional needs xarray, pydap, scipy and cftime;
neither mode needs authentication or installs dependencies.
Run from anywhere: python3 maxent/cmip6_erisim_kontrolu.py
"""

import argparse
import concurrent.futures
import csv
import ctypes
import ctypes.util
import datetime as dt
import hashlib
import io
import json
import math
from pathlib import Path
import re
import struct
import sys
import urllib.error
import urllib.request
import urllib.parse
import zlib

CATALOG = "https://storage.googleapis.com/cmip6/pangeo-cmip6.csv"
CATALOG_DESCRIPTION = "https://storage.googleapis.com/cmip6/pangeo-cmip6.json"
MODELS = ("MPI-ESM1-2-LR", "GFDL-ESM4", "IPSL-CM6A-LR")
MEMBER = "r1i1p1f1"
TABLES = {"tos": "Omon", "siconc": "SImon", "pr": "Amon", "tas": "Amon"}
PERIODS = {
    "historical": [("baseline_historical", 2000, 2014)],
    "ssp245": [("baseline_scenario", 2015, 2025), ("future", 2041, 2060)],
}
ROOT = Path(__file__).resolve().parent / "girdi" / "cmip6_2041_2060"
ESGF_SEARCH = "https://esgf-data.dkrz.de/esg-search/search/"


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def fetch(url, limit, timeout, method="GET"):
    req = urllib.request.Request(url, method=method,
                                 headers={"User-Agent": "adelie-cmip6-provenance/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = b"" if method == "HEAD" else response.read(limit + 1)
        if len(body) > limit:
            raise ValueError("response exceeds configured byte limit")
        return body, {"url": response.url, "http_status": response.status,
                      "checked_at_utc": utc_now(), "bytes_received": len(body),
                      "content_length": response.headers.get("Content-Length"),
                      "etag": response.headers.get("ETag"),
                      "last_modified": response.headers.get("Last-Modified"),
                      "sha256": hashlib.sha256(body).hexdigest() if body else None}


def safe_error(exc):
    # No exception strings: avoid leaking authentication/proxy configuration.
    return {"type": type(exc).__name__,
            "http_status": exc.code if isinstance(exc, urllib.error.HTTPError) else None}


def decode_numeric(raw, spec):
    if spec.get("filters"):
        raise ValueError("unsupported coordinate filters")
    compressor = spec.get("compressor")
    expected = math.prod(spec["chunks"]) * int(spec["dtype"][2:])
    if expected > 1024 * 1024:
        raise ValueError("coordinate chunk exceeds 1 MiB decoded budget")
    if compressor and compressor["id"] == "blosc":
        name = ctypes.util.find_library("blosc")
        if not name:
            raise RuntimeError("system libblosc unavailable")
        lib = ctypes.CDLL(name)
        # Blosc header bytes 4..7 encode the decoded size, little endian.
        if len(raw) < 16 or struct.unpack_from("<I", raw, 4)[0] != expected:
            raise ValueError("invalid blosc coordinate header")
        source = ctypes.create_string_buffer(raw)
        target = ctypes.create_string_buffer(expected)
        lib.blosc_decompress_ctx.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                            ctypes.c_size_t, ctypes.c_int]
        lib.blosc_decompress_ctx.restype = ctypes.c_int
        count = lib.blosc_decompress_ctx(source, target, expected, 1)
        if count != expected:
            raise ValueError("blosc coordinate decode size mismatch")
        raw = target.raw
    elif compressor and compressor["id"] in ("zlib", "gzip"):
        decoder = zlib.decompressobj(31 if compressor["id"] == "gzip" else 15)
        raw = decoder.decompress(raw, expected + 1)
        if len(raw) > expected or not decoder.eof:
            raise ValueError("compressed coordinate exceeds decode budget")
    elif compressor:
        raise ValueError("unsupported coordinate compressor")
    dtype = spec["dtype"]
    codes = {"i8": "q", "f8": "d", "i4": "i", "f4": "f"}
    if dtype[1:] not in codes or dtype[0] not in "<>":
        raise ValueError("unsupported coordinate dtype")
    if len(raw) != expected:
        raise ValueError("coordinate size mismatch")
    return [v[0] for v in struct.iter_unpack(dtype[0] + codes[dtype[1:]], raw)]


def month_of(value, units, calendar):
    match = re.fullmatch(r"(days|hours|seconds) since (\d{4})-(\d{1,2})-(\d{1,2})(.*)", units)
    if not match:
        raise ValueError("unsupported CF time units")
    unit, year, month, day, tail = match.groups()
    year, month, day = int(year), int(month), int(day)
    clock = re.search(r"(\d{1,2}):(\d{2}):(\d{2}(?:\.\d+)?)", tail)
    fraction = (int(clock[1]) / 24 + int(clock[2]) / 1440 + float(clock[3]) / 86400
                if clock else 0)
    offset = value / {"days": 1, "hours": 24, "seconds": 86400}[unit]
    if calendar in ("proleptic_gregorian", "gregorian", "standard"):
        date = dt.datetime(year, month, day) + dt.timedelta(days=fraction + offset)
        return date.year, date.month
    if calendar in ("noleap", "365_day", "360_day"):
        lengths = [30] * 12 if calendar == "360_day" else [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        yearlen = sum(lengths)
        absolute = (year - 1) * yearlen + sum(lengths[:month - 1]) + day - 1 + fraction + offset
        outyear, rem = divmod(math.floor(absolute), yearlen)
        outmonth = 1
        for length in lengths:
            if rem < length:
                break
            rem -= length
            outmonth += 1
        return outyear + 1, outmonth
    raise ValueError("unsupported CF calendar")


def check_dataset(row, timeout):
    item = {"catalog_record": row, "status": "not_checked",
            "climate_values_downloaded": False, "checked_at_utc": utc_now()}
    try:
        if not row["zstore"].startswith("gs://cmip6/"):
            raise ValueError("unsupported public store")
        base = row["zstore"].replace("gs://", "https://storage.googleapis.com/", 1).rstrip("/")
        raw, response = fetch(base + "/.zmetadata", 4 * 1024 * 1024, timeout)
        item["metadata_response"] = response
        meta = json.loads(raw)["metadata"]
        attrs = meta[".zattrs"]
        variable = row["variable_id"]
        data = meta[variable + "/.zarray"]
        varattrs = meta[variable + "/.zattrs"]
        timespec, timeattrs = meta["time/.zarray"], meta["time/.zattrs"]
        keep = ("source_id", "institution_id", "experiment_id", "variant_label", "table_id",
                "grid_label", "grid", "nominal_resolution", "frequency", "version_id",
                "parent_source_id", "parent_experiment_id", "parent_variant_label",
                "branch_time_in_parent", "branch_time_in_child", "parent_time_units",
                "tracking_id", "netcdf_tracking_ids", "further_info_url", "license", "references")
        item.update(global_attributes={k: attrs[k] for k in keep if k in attrs},
                    variable_attributes=varattrs, array=data, time_attributes=timeattrs,
                    time_array=timespec,
                    coordinates={k[:-8]: {"array": v, "attributes": meta.get(k[:-8] + "/.zattrs", {})}
                                 for k, v in meta.items() if k.endswith("/.zarray")
                                 and k.split("/")[0] in ("lat", "lon", "latitude", "longitude")})
        identities = {"source_id": row["source_id"], "experiment_id": row["experiment_id"],
                      "variant_label": row["member_id"], "table_id": row["table_id"],
                      "grid_label": row["grid_label"]}
        item["identity_matches"] = {k: attrs.get(k) == v for k, v in identities.items()}
        if not all(item["identity_matches"].values()) or attrs.get("frequency") != "mon":
            raise ValueError("catalog/metadata identity or frequency mismatch")
        if row["experiment_id"] == "ssp245":
            item["historical_parent_matches"] = (
                attrs.get("parent_source_id") == row["source_id"]
                and attrs.get("parent_variant_label") == row["member_id"]
                and attrs.get("parent_experiment_id") == "historical")
            if not item["historical_parent_matches"]:
                raise ValueError("scenario parent mismatch")
        months, receipts = [], []
        if len(timespec["shape"]) != 1:
            raise ValueError("time coordinate is not one dimensional")
        for chunk in range(math.ceil(timespec["shape"][0] / timespec["chunks"][0])):
            blob, receipt = fetch(base + "/time/" + str(chunk), 1024 * 1024, timeout)
            receipts.append(receipt)
            values = decode_numeric(blob, timespec)
            remaining = timespec["shape"][0] - len(months)
            months.extend(month_of(v, timeattrs["units"], timeattrs.get("calendar", "standard"))
                          for v in values[:remaining])
        item["time_chunk_responses"] = receipts
        ordered = all(a < b for a, b in zip(months, months[1:]))
        item["time_coverage"] = {"first_month": "%04d-%02d" % months[0],
                                 "last_month": "%04d-%02d" % months[-1],
                                 "minimum_month": "%04d-%02d" % min(months),
                                 "maximum_month": "%04d-%02d" % max(months),
                                 "months": len(months), "unique_months": len(set(months)),
                                 "strictly_increasing_months": ordered,
                                 "ordering_break_examples": [
                                     {"index": i + 1, "previous": "%04d-%02d" % a,
                                      "current": "%04d-%02d" % b}
                                     for i, (a, b) in enumerate(zip(months, months[1:])) if a >= b][:10]}
        periods = []
        for name, start, end in PERIODS[row["experiment_id"]]:
            expected = {(y, m) for y in range(start, end + 1) for m in range(1, 13)}
            missing = sorted(expected - set(months))
            indices = [i for i, ym in enumerate(months) if ym in expected]
            periods.append({"name": name, "start": f"{start}-01", "end": f"{end}-12",
                            "expected_months": len(expected), "found_months": len(indices),
                            "missing_months": ["%04d-%02d" % ym for ym in missing],
                            "complete": not missing and ordered and len(indices) == len(expected),
                            "time_index_start": min(indices) if indices and ordered else None,
                            "time_index_stop_exclusive": max(indices) + 1 if indices and ordered else None})
        item["requested_periods"] = periods
        dims = varattrs["_ARRAY_DIMENSIONS"]
        time_axis = dims.index("time")
        first = periods[0]["time_index_start"]
        chunk_indices = [0] * len(dims)
        chunk_indices[time_axis] = first // data["chunks"][time_axis] if first is not None else 0
        key = data.get("dimension_separator", ".").join(map(str, chunk_indices))
        _, head = fetch(base + "/" + variable + "/" + key, 0, timeout, "HEAD")
        item["example_climate_chunk_head"] = head
        item["example_chunk_note"] = "HEAD only; spatial index zero, not a regional value validation"
        full_spatial = all(c >= n for i, (c, n) in enumerate(zip(data["chunks"], data["shape"]))
                           if i != time_axis)
        item["subset_feasibility"] = {
            "spatial_chunk_covers_entire_native_grid": full_spatial,
            "one_chunk_uncompressed_bytes": math.prod(data["chunks"]) * int(data["dtype"][2:]),
            "decision": "metadata_and_time_only; regional extraction requires a separately budgeted climate-chunk read",
        }
        item["status"] = ("time_coverage_verified_chunk_head_ok"
                          if all(p["complete"] for p in periods) else "time_coverage_incomplete")
    except Exception as exc:
        item["status"] = "check_failed"
        item["error"] = safe_error(exc)
    return item


def regional_source(item, timeout):
    """Locate a version-matched original ESGF file with public CEDA DAP2."""
    row = item["catalog_record"]
    params = {"project": "CMIP6", "source_id": row["source_id"],
              "experiment_id": row["experiment_id"], "member_id": row["member_id"],
              "variable_id": row["variable_id"], "table_id": row["table_id"],
              "type": "File", "format": "application/solr+json", "limit": 100, "latest": "true"}
    query = ESGF_SEARCH + "?" + urllib.parse.urlencode(params)
    raw, receipt = fetch(query, 4 * 1024 * 1024, timeout)
    response = json.loads(raw)["response"]
    token = f".{row['grid_label']}.v{row['version'].lstrip('v')}."
    docs = [d for d in response["docs"] if d.get("data_node") == "esgf.ceda.ac.uk"
            and token in d["instance_id"] and not d.get("retracted", False)]
    if len(docs) != 1 or response["numFound"] > 100:
        raise ValueError("expected one complete version-matched CEDA source file")
    doc = docs[0]
    urls = [u.split("|")[0].removesuffix(".html") for u in doc["url"] if u.endswith("|OPENDAP")]
    if len(urls) != 1:
        raise ValueError("missing unique OPeNDAP URL")
    return {"catalog_record": row, "search_response": receipt, "opendap_url": urls[0],
            "original_file_id": doc["instance_id"], "original_file_bytes": doc["size"],
            "original_file_checksum": doc.get("checksum"),
            "original_file_checksum_type": doc.get("checksum_type"),
            "original_tracking_id": doc.get("tracking_id"), "retracted": doc.get("retracted", False)}


def extract_regional(variable, items, output, timeout):
    """Read only regional hyperslabs over DAP2; retain native grids and masks."""
    import numpy as np
    import requests
    import xarray as xr
    sources, pieces, geo = [], {}, None
    session = requests.Session()
    session.trust_env = False  # no .netrc, cloud credentials, or authentication
    for experiment in PERIODS:
        item = next(i for i in items if i["catalog_record"]["variable_id"] == variable
                    and i["catalog_record"]["experiment_id"] == experiment)
        source = regional_source(item, timeout)
        with xr.open_dataset(source["opendap_url"], engine="pydap", session=session,
                             timeout=timeout, mask_and_scale=False) as remote:
            row = item["catalog_record"]
            for key, expected in (("source_id", row["source_id"]), ("variant_label", MEMBER),
                                  ("experiment_id", experiment), ("grid_label", row["grid_label"])):
                if remote.attrs.get(key) != expected:
                    raise ValueError("original ESGF identity mismatch")
            field = remote[variable]
            if field.ndim != 3 or field.dims[0] != "time":
                raise ValueError("expected monthly time and two native spatial dimensions")
            ydim, xdim = field.dims[1:]
            latname = "nav_lat" if "nav_lat" in remote else "lat"
            lonname = "nav_lon" if "nav_lon" in remote else "lon"
            lat, lon = remote[latname].values, remote[lonname].values
            if lat.ndim == lon.ndim == 1:
                lon, lat = np.meshgrid(lon, lat)
            lon = (lon + 180) % 360 - 180
            mask = (lat >= -70.5) & (lat <= -66.0) & (lon >= -73.0) & (lon <= -64.0)
            yy, xx = np.where(mask)
            if not len(yy):
                raise ValueError("no native cells inside requested region")
            y0, y1 = max(0, int(yy.min()) - 1), min(lat.shape[0], int(yy.max()) + 2)
            x0, x1 = max(0, int(xx.min()) - 1), min(lat.shape[1], int(xx.max()) + 2)
            latitude, longitude = lat[y0:y1, x0:x1], lon[y0:y1, x0:x1]
            if geo is not None and (not np.array_equal(geo[0], latitude)
                                    or not np.array_equal(geo[1], longitude)):
                raise ValueError("historical/scenario native coordinates differ")
            geo = latitude, longitude, np.arange(y0, y1), np.arange(x0, x1)
            source["native_spatial_slice"] = {ydim: [y0, y1], xdim: [x0, x1]}
            source["time_calendar"] = remote.time.encoding.get("calendar", "standard")
            source["source_units"] = field.attrs.get("units")
            source["variable_attributes"] = dict(field.attrs)
            source["regional_requests"] = []
            for label, start, end in PERIODS[experiment]:
                selected = field.sel(time=slice(f"{start}-01-01", f"{end}-12-31")).isel(
                    {ydim: slice(y0, y1), xdim: slice(x0, x1)})
                expected = (end - start + 1) * 12
                if selected.sizes["time"] != expected:
                    raise ValueError("regional source does not contain all requested months")
                months = [(int(y), int(m)) for y, m in zip(selected.time.dt.year.values,
                                                         selected.time.dt.month.values)]
                if months != [(y, m) for y in range(start, end + 1) for m in range(1, 13)]:
                    raise ValueError("regional months missing, duplicated or unsorted")
                source["regional_requests"].append({"role": label, "start": months[0], "end": months[-1],
                                                    "months": expected, "shape": list(selected.shape)})
                if selected.size * 8 > 16 * 1024 * 1024:
                    raise ValueError("regional payload exceeds 16 MiB memory budget")
                values = np.asarray(selected.values, dtype=np.float64)
                # DAP2 may expose a float32 sentinel as a rounded float64 DAS
                # attribute. Match the documented missing marker tolerantly.
                for key in ("_FillValue", "missing_value"):
                    if key in field.attrs:
                        values[np.isclose(values, float(field.attrs[key]), rtol=1e-6, atol=0)] = np.nan
                if np.isinf(values).any() or np.any(np.abs(values[np.isfinite(values)]) >= 1e19):
                    raise ValueError("unrecognized nonfinite or missing climate value")
                units = field.attrs.get("units")
                days = selected.time.dt.days_in_month.values.astype(np.float64)
                if variable == "tas" and units == "K":
                    values -= 273.15
                elif variable == "tos" and units in ("degC", "degrees_C", "degree_Celsius"):
                    pass
                elif variable == "siconc" and units == "%":
                    if np.any((values[np.isfinite(values)] < 0) | (values[np.isfinite(values)] > 100.001)):
                        raise ValueError("sea ice outside percentage bounds")
                elif variable == "pr" and units == "kg m-2 s-1":
                    if np.any(values[np.isfinite(values)] < 0):
                        raise ValueError("negative precipitation")
                    values *= days[:, None, None] * 86400
                else:
                    raise ValueError("unexpected source units")
                unit = {"tas": "degC", "tos": "degC", "siconc": "%", "pr": "mm month-1"}[variable]
                local = xr.Dataset({variable: (("time", "y", "x"), values),
                                    "days_in_month": ("time", days)},
                                   coords={"time": selected.time.values,
                                           "latitude": (("y", "x"), latitude),
                                           "longitude": (("y", "x"), longitude),
                                           "y": np.arange(y0, y1), "x": np.arange(x0, x1)})
                local[variable].attrs = {"units": unit, "source_units": units}
                local.time.encoding = {"calendar": "proleptic_gregorian", "units": "days since 1850-01-01"}
                pieces[label] = local
        sources.append(source)
    baseline = xr.concat([pieces["baseline_historical"], pieces["baseline_scenario"]], dim="time")
    baseline.attrs = {"period": "2000-2025", "scenario_continuation": "ssp245 from 2015-01"}
    future = pieces["future"]
    future.attrs = {"period": "2041-2060", "experiment_id": "ssp245"}
    climatologies, daymeans, counts = [], [], []
    files, stats = [], {}
    for name, dataset in (("baseline_2000_2025", baseline), ("future_2041_2060", future)):
        dataset.attrs.update(source_id="IPSL-CM6A-LR", member_id=MEMBER, native_grid_preserved="true")
        path = output / f"{variable}_{name}.nc"
        if path.exists():
            raise FileExistsError("regional output exists; choose another output directory")
        dataset.to_netcdf(path, engine="scipy")
        files.append(path)
        climatologies.append(dataset[variable].groupby("time.month").mean("time", skipna=True))
        counts.append(dataset[variable].groupby("time.month").count("time"))
        daymeans.append(dataset.days_in_month.groupby("time.month").mean("time"))
        arr = dataset[variable].values
        stats[name] = {"shape": list(arr.shape), "finite_values": int(np.isfinite(arr).sum()),
                       "nan_values": int(np.isnan(arr).sum()), "min": float(np.nanmin(arr)),
                       "max": float(np.nanmax(arr))}
    clim = xr.concat(climatologies, dim=xr.IndexVariable("period", [0, 1])).to_dataset(name=variable)
    clim["valid_year_count"] = xr.concat(counts, dim=xr.IndexVariable("period", [0, 1]))
    clim["mean_days_in_month"] = xr.concat(daymeans, dim=xr.IndexVariable("period", [0, 1]))
    clim["period_start_year"] = ("period", [2000, 2041])
    clim["period_end_year"] = ("period", [2025, 2060])
    clim[variable].attrs["units"] = {"tos": "degC", "tas": "degC", "siconc": "%", "pr": "mm month-1"}[variable]
    clim.attrs = {"source_id": "IPSL-CM6A-LR", "member_id": MEMBER,
                  "period_labels": "0=baseline_2000_2025;1=future_ssp245_2041_2060",
                  "climatology_method": "arithmetic mean across years for each calendar month; pr converted before averaging",
                  "spatial_method": "native bounding rectangle with one native cell halo; no interpolation",
                  "missing_method": "source missing markers become NaN; no spatial filling"}
    path = output / f"{variable}_aylik_klimatoloji.nc"
    clim.to_netcdf(path, engine="scipy")
    files.append(path)
    path = output / f"{variable}_aylik_klimatoloji.npz"
    np.savez_compressed(path, baseline=clim[variable].isel(period=0).values,
                        future=clim[variable].isel(period=1).values,
                        lat=geo[0], lon=geo[1], month=np.arange(1, 13),
                        units=np.array(clim[variable].attrs["units"]),
                        baseline_valid_year_count=clim.valid_year_count.isel(period=0).values,
                        future_valid_year_count=clim.valid_year_count.isel(period=1).values,
                        baseline_mean_days_in_month=clim.mean_days_in_month.isel(period=0).values,
                        future_mean_days_in_month=clim.mean_days_in_month.isel(period=1).values)
    files.append(path)
    receipts = []
    for path in files:
        if path.suffix == ".nc":
            with xr.open_dataset(path, engine="scipy") as reread:
                if not np.array_equal(reread.latitude.values, geo[0]):
                    raise ValueError("saved latitude mismatch")
                if np.isinf(reread[variable].values).any():
                    raise ValueError("saved data contains infinity")
        receipts.append({"path": str(path.relative_to(output.parent)), "bytes": path.stat().st_size,
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    session.close()
    return {"variable_id": variable, "status": "regional_monthly_fields_produced",
            "sources": sources, "files": receipts, "statistics": stats,
            "climatology_dimensions": dict(clim.sizes), "units": clim[variable].attrs["units"]}


def regional_main(output, timeout):
    import importlib.metadata
    manifest = json.loads((output / "erisim_envanteri.json").read_text())
    items = [i for i in manifest["datasets"] if i["catalog_record"]["source_id"] == "IPSL-CM6A-LR"]
    if len(items) != 8 or any(i["status"] != "time_coverage_verified_chunk_head_ok" for i in items):
        raise ValueError("IPSL access inventory must verify all eight sources first")
    destination = output / "IPSL-CM6A-LR_r1i1p1f1"
    destination.mkdir(parents=True, exist_ok=True)
    result = {"schema_version": 1, "started_at_utc": utc_now(), "source_id": "IPSL-CM6A-LR",
              "member_id": MEMBER, "regional_monthly_fields_complete": False,
              "maxent_future_inputs_complete": False, "remapping_performed": False,
              "source_access": "ESGF CEDA DAP2 server-side regional hyperslabs",
              "packages": {p: importlib.metadata.version(p) for p in
                           ("xarray", "pydap", "numpy", "scipy", "cftime", "requests")},
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "variables": []}
    # Separate variables can download concurrently; each has its own session.
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(extract_regional, v, items, destination, timeout): v for v in TABLES}
        for future in concurrent.futures.as_completed(futures):
            variable = futures[future]
            try:
                record = future.result()
            except Exception as exc:
                record = {"variable_id": variable, "status": "failed", "error": safe_error(exc)}
            result["variables"].append(record)
            print(json.dumps({"variable": variable, "status": record["status"]}), flush=True)
            result["finished_at_utc"] = utc_now()
            result["regional_monthly_fields_complete"] = len(result["variables"]) == 4 and all(
                v["status"] == "regional_monthly_fields_produced" for v in result["variables"])
            (output / "bolgesel_uretim_envanteri.json").write_text(
                json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    return 0 if result["regional_monthly_fields_complete"] else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--overwrite", action="store_true", help="replace this script's JSON inventories")
    parser.add_argument("--regional", action="store_true", help="extract IPSL regional fields using existing inventory; requires xarray/pydap/scipy")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    if args.regional:
        return regional_main(args.output_dir, args.timeout)
    paths = [args.output_dir / name for name in ("erisim_envanteri.json", "istek_envanteri.json")]
    if not args.overwrite and any(p.exists() for p in paths):
        parser.error("inventory exists; choose a new --output-dir or use --overwrite")
    manifest = {"schema_version": 1, "started_at_utc": utc_now(), "catalog_url": CATALOG,
                "catalog_description_url": CATALOG_DESCRIPTION,
                "production_complete": False, "climate_values_downloaded": False,
                "regional_subset_produced": False, "final_model_selection": False,
                "credential_file_presence_only": {
                    name: (Path.home() / name).is_file() for name in
                    (".cdsapirc", ".esg/credentials.pem", ".config/gcloud/application_default_credentials.json")},
                "runtime": {"python": sys.version.split()[0],
                            "system_libblosc_present": bool(ctypes.util.find_library("blosc")),
                            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
                "baseline": "2000-2025 (historical 2000-2014 + ssp245 2015-2025)",
                "future": "ssp245 2041-2060", "existing_analysis_grid_degrees": 0.25,
                "existing_occurrence_interpretation": "general occurrence; unchanged",
                "datasets": [], "model_checks": []}
    requests = {"schema_version": 1, "status": "planned_not_submitted",
                "area_north_west_south_east": [-66.0, -73.0, -70.5, -64.0],
                "target_grid_degrees": 0.25, "remapping_performed": False,
                "note": "Native GCM grids differ; this inventory does not define a remapping or bias adjustment method.",
                "requests": []}
    try:
        description, receipt = fetch(CATALOG_DESCRIPTION, 128 * 1024, args.timeout)
        manifest["catalog_description_response"] = receipt
        if json.loads(description)["catalog_file"] != CATALOG:
            raise ValueError("catalog descriptor URL mismatch")
        raw, receipt = fetch(CATALOG, 128 * 1024 * 1024, args.timeout)
        manifest["catalog_response"] = receipt
        rows = [r for r in csv.DictReader(io.StringIO(raw.decode("utf-8")))
                if r["source_id"] in MODELS and r["member_id"] == MEMBER
                and r["experiment_id"] in PERIODS
                and TABLES.get(r["variable_id"]) == r["table_id"]]
        selected = []
        for model in MODELS:
            for variable in TABLES:
                matching = [r for r in rows if r["source_id"] == model and r["variable_id"] == variable]
                grids = [{r["grid_label"] for r in matching if r["experiment_id"] == exp} for exp in PERIODS]
                common = grids[0] & grids[1]
                if not common:
                    manifest.setdefault("missing_pairs", []).append({"model": model, "variable": variable})
                    continue
                grid = sorted(common, key=lambda g: (g != "gn", g))[0]
                for exp in PERIODS:
                    options = [r for r in matching if r["grid_label"] == grid and r["experiment_id"] == exp]
                    selected.append(sorted(options, key=lambda r: (r["version"], r["zstore"]))[-1])
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            manifest["datasets"] = list(pool.map(lambda r: check_dataset(r, args.timeout), selected))
        for model in MODELS:
            items = [i for i in manifest["datasets"] if i["catalog_record"]["source_id"] == model]
            calendars = sorted({i.get("time_attributes", {}).get("calendar", "unknown") for i in items})
            # Gregorian and proleptic Gregorian have the same dates throughout
            # these post-1850 stores. Preserve original labels in the inventory.
            normalized = {"gregorian_post_1582" if c in
                          ("gregorian", "standard", "proleptic_gregorian") else c for c in calendars}
            post_reform = all(i.get("time_coverage", {}).get("minimum_month", "0000") >= "1583-01"
                              for i in items)
            compatible = len(normalized) == 1 and (len(calendars) == 1 or post_reform)
            ok = len(items) == 8 and compatible and all(
                i["status"] == "time_coverage_verified_chunk_head_ok" for i in items)
            manifest["model_checks"].append({"source_id": model, "member_id": MEMBER,
                "dataset_count": len(items), "calendars": calendars,
                "calendars_compatible_over_checked_dates": compatible,
                "all_eight_datasets_verified": ok,
                "status": "available_not_produced" if ok else "incomplete_or_failed"})
        for item in manifest["datasets"]:
            r = item["catalog_record"]
            for label, start, end in PERIODS[r["experiment_id"]]:
                requests["requests"].append({"source_id": r["source_id"], "member_id": r["member_id"],
                    "experiment_id": r["experiment_id"], "variable_id": r["variable_id"],
                    "table_id": r["table_id"], "grid_label": r["grid_label"], "version": r["version"],
                    "zstore": r["zstore"], "period_role": label,
                    "start_month": f"{start}-01", "end_month": f"{end}-12",
                    "access_check_status": item["status"],
                    "eligible_for_next_stage": item["status"] == "time_coverage_verified_chunk_head_ok",
                    "download_status": "not_downloaded"})
    except Exception as exc:
        manifest["catalog_error"] = safe_error(exc)
    manifest["finished_at_utc"] = utc_now()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for path, payload in zip(paths, (manifest, requests)):
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    complete = sum(m["all_eight_datasets_verified"] for m in manifest["model_checks"])
    print(json.dumps({"verified_models": complete, "datasets": len(manifest["datasets"]),
                      "production_complete": False, "output_dir": str(args.output_dir)}, ensure_ascii=False))
    return 0 if complete == len(MODELS) else 2


if __name__ == "__main__":
    raise SystemExit(main())
