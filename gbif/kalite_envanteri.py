"""Reconstruct original representatives from existing clean metadata, stdlib only.

This preserves every column available in kayitlar_temiz.csv, not unavailable raw
GBIF fields. Never downloads, filters, or overwrites original records.
"""
import argparse
import csv
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def missing(value):
    return value.strip().lower() in ("", "nan", "null", "none")


def cell(record, h):
    col = math.floor((float(record["decimalLongitude"]) - h["xllcorner"]) / h["cellsize"])
    row = int(h["nrows"]) - 1 - math.floor(
        (float(record["decimalLatitude"]) - h["yllcorner"]) / h["cellsize"])
    if not (0 <= row < h["nrows"] and 0 <= col < h["ncols"]):
        raise ValueError("Clean record outside grid")
    return row, col


def reconstruct(records, h):
    def key(r):
        uncertainty = r["coordinateUncertaintyInMeters"]
        return (*cell(r, h), math.inf if missing(uncertainty) else float(uncertainty),
                int(r["gbifID"]))
    selected = {}
    for record in sorted(records, key=key):
        selected.setdefault(cell(record, h), record)
    return [dict(r, row=rc[0], col=rc[1]) for rc, r in selected.items()]


def season(record):
    # eventDate may be a date, timestamp, partial date or interval. Do not invent months.
    date = record["eventDate"]
    try:
        month = int(date[5:7]) if "/" not in date else 0
    except ValueError:
        month = 0
    return {12: "DJF", 1: "DJF", 2: "DJF", 3: "MAM", 4: "MAM", 5: "MAM",
            6: "JJA", 7: "JJA", 8: "JJA", 9: "SON", 10: "SON", 11: "SON"}.get(month, "unknown")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "gbif/temiz/kalite_20261108")
    args = parser.parse_args()
    out = args.output.resolve()
    allowed = ROOT / "gbif/temiz/kalite_20261108"
    if out != allowed and allowed not in out.parents:
        parser.error("Output must be inside gbif/temiz/kalite_20261108")
    if out.exists():
        parser.error("Output exists; choose a new child directory")
    clean_path = ROOT / "gbif/temiz/kayitlar_temiz.csv"
    sample_path = ROOT / "gbif/temiz/adelie_maxent.csv"
    grid = ROOT / "maxent/girdi/katmanlar/sst_yillik.asc"
    paths = [clean_path, sample_path, grid, ROOT / "gbif/temizle.py", Path(__file__)]
    def hashes(files):
        return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(files) if p.is_file()}
    before = hashes(paths)
    with grid.open() as f:
        h = dict((k.lower(), float(v)) for k, v in (f.readline().split() for _ in range(6)))
    clean = read_csv(clean_path)
    reps = reconstruct(clean, h)
    expected = read_csv(sample_path)
    rebuilt = [{"species": "Pygoscelis adeliae",
                "longitude": f'{float(r["decimalLongitude"]):.6f}',
                "latitude": f'{float(r["decimalLatitude"]):.6f}'} for r in reps]
    if rebuilt != expected:
        raise ValueError("Reconstructed coordinates/order differ from original samples")
    out.mkdir(parents=True)
    write_csv(out / "temsilciler_metadata.csv", reps)
    write_csv(out / "adelie_maxent_reconstructed.csv", rebuilt)
    same_bytes = (out / "adelie_maxent_reconstructed.csv").read_text() == sample_path.read_text()
    groups = []
    summaries = {}
    for population, records in (("clean", clean), ("representatives", reps)):
        summaries[population] = {"n": len(records), "uncertainty_missing": sum(
            missing(r["coordinateUncertaintyInMeters"]) for r in records),
            "seasons": dict(Counter(season(r) for r in records)),
            "years": dict(sorted(Counter(r["year"] for r in records).items())),
            "land_grid_cell": dict(Counter(r["kara_hucresi"] for r in records))}
        for field in ("datasetKey", "basisOfRecord", "season", "datasetKey+basisOfRecord"):
            by = defaultdict(list)
            for r in records:
                value = (season(r) if field == "season" else
                         r["datasetKey"] + " | " + r["basisOfRecord"]
                         if field == "datasetKey+basisOfRecord" else r[field])
                by[value].append(r)
            for value, subset in sorted(by.items()):
                absent = sum(missing(r["coordinateUncertaintyInMeters"]) for r in subset)
                groups.append(dict(population=population, group=field, value=value,
                                   n=len(subset), uncertainty_missing=absent,
                                   uncertainty_known=len(subset) - absent))
    write_csv(out / "quality_groups.csv", groups)
    summary = {"coordinate_selection_identical": True, "sample_text_identical": same_bytes,
               "selection": "grid row,column; uncertainty ascending (missing last); numeric gbifID ascending",
               "metadata_scope": "all existing clean columns; unavailable raw GBIF fields not reconstructed",
               "populations": summaries,
               "limitations": "No breeding validation; no target-group background data; no ecological M finalized"}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    if before != hashes(paths):
        raise RuntimeError("Source files changed")
    manifest = {"input_sha256": before, "originals_unchanged": True,
                "output_sha256": hashes(out.rglob("*")), "python": sys.version,
                "platform": platform.platform(), "command": sys.argv}
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
