"""Deterministic geographic-band MaxEnt sidecar; never changes original inputs.

python3 maxent/mekansal_dogrulama.py [--run-java]
An existing output directory is refused. No ecological M or independent optimum
is inferred. numpy is the only non-stdlib dependency.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform
import shlex
import shutil
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = (("L_RM1", False, 1), ("LQ_RM1", True, 1), ("LQ_RM2", True, 2))
ALL_CANDIDATES = CANDIDATES + (("AUTO_RM1", None, 1),)


def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields=None):
    rows = list(rows)
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields or list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2,
                                     allow_nan=False) + "\n", encoding="utf-8")


def hashes(paths):
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(paths) if p.is_file()}


def read_asc(path):
    with Path(path).open() as f:
        header = dict((k.lower(), float(v)) for k, v in
                      (f.readline().split() for _ in range(6)))
        a = np.loadtxt(f, ndmin=2)
    if a.shape != (int(header["nrows"]), int(header["ncols"])):
        raise ValueError(f"Raster shape mismatch: {path}")
    if not np.isfinite(a).all():
        raise ValueError(f"Nonfinite raster: {path}")
    return header, a


def cells(xy, header):
    xy = np.asarray(xy, dtype=float)
    col = np.floor((xy[:, 0] - header["xllcorner"]) / header["cellsize"]).astype(int)
    row = int(header["nrows"]) - 1 - np.floor(
        (xy[:, 1] - header["yllcorner"]) / header["cellsize"]).astype(int)
    if ((row < 0) | (row >= header["nrows"]) |
            (col < 0) | (col >= header["ncols"])).any():
        raise ValueError("Coordinate outside raster")
    return np.column_stack((row, col))


def band_partition(values, k=4):
    """Globally minimize sum squared deviations from n/k; never split ties.

    Dynamic programming over sorted unique grid rows/columns; stable first
    boundary wins ties. This uses counts alone, never environmental/model scores.
    """
    unique, counts = np.unique(values, return_counts=True)
    m = len(unique)
    if m < k:
        raise ValueError("Not enough distinct coordinates for contiguous bands")
    prefix = np.r_[0, np.cumsum(counts)]
    dp = {(0, 0): (0.0, [])}
    for b in range(1, k + 1):
        for end in range(b, m + 1):
            choices = [(dp[b - 1, start][0] +
                        (prefix[end] - prefix[start] - len(values) / k) ** 2,
                        dp[b - 1, start][1] + [end])
                       for start in range(b - 1, end) if (b - 1, start) in dp]
            dp[b, end] = min(choices, key=lambda item: item[0])
    score, ends = dp[k, m]
    cuts = [(float(unique[e - 1]) + float(unique[e])) / 2 for e in ends[:-1]]
    labels = np.searchsorted(cuts, values, side="right")
    return labels, {"squared_imbalance": score, "cuts_grid_index": cuts,
                    "counts": np.bincount(labels, minlength=k).tolist()}


def geographic_folds(rc):
    options = {}
    assignments = {}
    for axis, column in (("latitude", 0), ("longitude", 1)):
        assignments[axis], options[axis] = band_partition(rc[:, column])
    # Fixed latitude preference for an exact count-balance tie.
    axis = min(options, key=lambda a: options[a]["squared_imbalance"])
    return assignments[axis], {"chosen_axis": axis, "alternatives": options,
                              "tie_rule": "latitude first", "uses_scores": False}


def random_folds(spatial_labels, seed=20261108):
    """One PCG64 permutation, allocated in spatial fold-size order; no retries."""
    counts = np.bincount(spatial_labels, minlength=4)
    if len(counts) != 4 or (counts == 0).any():
        raise ValueError("Expected four nonempty reference folds")
    permutation = np.random.Generator(np.random.PCG64(seed)).permutation(len(spatial_labels))
    labels = np.empty(len(spatial_labels), dtype=int)
    start = 0
    for fold, count in enumerate(counts):
        labels[permutation[start:start + count]] = fold
        start += count
    return labels


def feature_arguments(quadratic):
    # AUTO uses jar defaults for enabled feature families and sample-size rules.
    if quadratic is None:
        return ["autofeature=true"]
    return ["autofeature=false", "linear=true", f"quadratic={str(quadratic).lower()}",
            "product=false", "threshold=false", "hinge=false"]


def matched_comparison(out, sources, labels, header, valid, rc):
    """Validate saved spatial inputs/settings and recompute their raster metrics.

    Reuses existing spatial fits; never changes those historical output trees.
    """
    random_rows = read_csv(out / "metrics.csv")
    random_commands = json.loads((out / "commands.json").read_text())
    spatial_rows = {}
    source_hashes = {}
    def controls(command):
        return sorted(a for a in command if not a.startswith(
            ("samplesfile=", "environmentallayers=", "outputdirectory=")))
    for source in sources:
        source = source.resolve()
        manifest = json.loads((source / "manifest.json").read_text())
        design = json.loads((source / "design.json").read_text())
        if design.get("partition", "spatial") != "spatial":
            raise ValueError("Comparison source must be spatial")
        # Historical source code hashes may differ; actual environmental/model
        # inputs must match. Check recorded outputs used in this comparison too.
        for rel, expected in manifest["input_sha256"].items():
            if rel.startswith("maxent/girdi/katmanlar/") or rel in (
                    "maxent/girdi/adelie_maxent.csv", "maxent/maxent.jar"):
                if hashes([ROOT / rel])[rel] != expected:
                    raise ValueError(f"Spatial input hash mismatch: {rel}")
        selected_files = [source / n for n in
                          ("metrics.csv", "commands.json", "assignments.csv", "design.json")]
        assignments = read_csv(source / "assignments.csv")
        source_labels = np.array([int(r["fold"]) for r in assignments])
        # Match sample identities and their original order, not just sample counts.
        current_assignments = read_csv(out / "assignments.csv")
        if [{k: v for k, v in r.items() if k != "fold"} for r in assignments] != [
                {k: v for k, v in r.items() if k != "fold"} for r in current_assignments]:
            raise ValueError("Spatial/random sample identities differ")
        if not np.array_equal(np.bincount(labels), np.bincount(source_labels)):
            raise ValueError("Spatial/random fold sizes differ")
        source_commands = json.loads((source / "commands.json").read_text())
        for row in read_csv(source / "metrics.csv"):
            name, fold = row["candidate"], int(row["fold"])
            if name not in {r["candidate"] for r in random_rows}:
                continue
            if (name, fold) in spatial_rows:
                raise ValueError("Duplicate spatial comparison candidate/fold")
            target = f"/{name}/fold_{fold}"
            sc = [c for c in source_commands if f"outputdirectory={source}{target}" in c]
            random = [c for c in random_commands if f"outputdirectory={out}{target}" in c]
            if len(sc) != 1 or len(random) != 1 or controls(sc[0]) != controls(random[0]):
                raise ValueError(f"Non-partition settings differ for {name}, fold {fold}")
            raster = source / name / f"fold_{fold}" / "Pygoscelis_adeliae.asc"
            selected_files.append(raster)
            h, a = read_asc(raster)
            if h != header or (a[valid] == h["nodata_value"]).any():
                raise ValueError("Spatial comparison raster invalid")
            scores = a[tuple(rc.T)]
            recalculated = metrics(scores[source_labels != fold], scores[source_labels == fold], a[valid])
            for key, value in recalculated.items():
                if not np.isclose(float(row[key]), value, rtol=0, atol=1e-14):
                    raise ValueError(f"Spatial saved metrics differ: {name}/{fold}/{key}")
            spatial_rows[name, fold] = dict(candidate=name, fold=fold, **recalculated)
        for path in selected_files:
            rel = str(path.relative_to(ROOT))
            actual = hashes([path])[rel]
            if manifest["output_sha256"].get(rel) != actual:
                raise ValueError(f"Spatial output hash mismatch: {rel}")
            source_hashes[rel] = actual
        source_hashes.update(hashes([source / "manifest.json"]))
    combined, comparison = [], []
    for name in dict.fromkeys(r["candidate"] for r in random_rows):
        sr = [spatial_rows[name, fold] for fold in range(4)]
        rr = [r for r in random_rows if r["candidate"] == name]
        if len(rr) != 4:
            raise ValueError("Incomplete random comparison")
        item = {"candidate": name}
        for partition, rows in (("spatial4", sr), ("random4", rr)):
            for row in rows:
                combined.append(dict(partition=partition, **row))
            aucs = [float(r["test_background_auc"]) for r in rows]
            item[partition + "_auc_mean"] = float(np.mean(aucs))
            item[partition + "_auc_sd_population"] = float(np.std(aucs))
            item[partition + "_omission_pooled"] = sum(
                float(r["test_omission_p10"]) * int(r["n_test"]) for r in rows) / len(labels)
        item["random_minus_spatial_auc"] = item["random4_auc_mean"] - item["spatial4_auc_mean"]
        comparison.append(item)
    write_csv(out / "matched_fold_metrics.csv", combined)
    write_csv(out / "matched_comparison.csv", comparison)
    write_json(out / "matched_sources.json", {
        "sha256": source_hashes, "settings_matched_except_partition": True,
        "old_outputs_provisional": True, "final_winner_selected": False,
        "limitations": "One random seed, shared full-domain background, not nested CV; no uncertainty inference from paired fold indices"})


def distance_diagnostics(xy, rc, train, test):
    if not len(train) or not len(test) or set(train) & set(test):
        raise ValueError("Empty or overlapping split")
    a, b = np.radians(xy[test]), np.radians(xy[train])
    dlon = a[:, None, 0] - b[None, :, 0]
    dlat = a[:, None, 1] - b[None, :, 1]
    hav = np.sin(dlat / 2) ** 2 + np.cos(a[:, None, 1]) * np.cos(
        b[None, :, 1]) * np.sin(dlon / 2) ** 2
    dist = 6371.0 * 2 * np.arcsin(np.sqrt(np.clip(hav, 0, 1)))
    delta = np.abs(rc[test, None, :] - rc[None, train, :])
    adjacent = (delta.max(axis=2) == 1).any(axis=1)
    same = (delta.max(axis=2) == 0).any(axis=1)
    return [{"sample_index": int(i), "nearest_train_km": float(d),
             "adjacent_train_8": bool(adj), "same_train_cell": bool(s)}
            for i, d, adj, s in zip(test, dist.min(axis=1), adjacent, same)]


def metrics(training, test, background):
    arrays = [np.asarray(x, dtype=float) for x in (training, test, background)]
    if any(x.ndim != 1 or not x.size or not np.isfinite(x).all() for x in arrays):
        raise ValueError("Metrics require finite nonempty one-dimensional scores")
    training, test, background = arrays
    # Pairwise presence-background AUC; ties contribute one half.
    diff = test[:, None] - background[None, :]
    auc = float(((diff > 0).sum() + 0.5 * (diff == 0).sum()) / diff.size)
    threshold = float(np.quantile(training, 0.10, method="linear"))
    return {"test_background_auc": auc, "training_p10_threshold": threshold,
            "test_omission_p10": float(np.mean(test < threshold)),
            "training_omission_p10": float(np.mean(training < threshold)),
            "n_train": len(training), "n_test": len(test),
            "n_background": len(background)}


def summarize_distances(rows):
    d = np.array([r["nearest_train_km"] for r in rows])
    return {"n_test_assignments": len(rows),
            "adjacent_train_8_count": sum(r["adjacent_train_8"] for r in rows),
            "same_train_cell_count": sum(r["same_train_cell"] for r in rows),
            "nearest_train_km_min": float(d.min()),
            "nearest_train_km_median": float(np.median(d)),
            "nearest_train_km_max": float(d.max())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-java", action="store_true")
    parser.add_argument("--partition", choices=("spatial", "random4"), default="spatial")
    parser.add_argument("--seed", type=int, default=20261108)
    parser.add_argument("--candidates", nargs="+", choices=[c[0] for c in ALL_CANDIDATES],
                        default=[c[0] for c in CANDIDATES])
    parser.add_argument("--compare-spatial", type=Path, nargs="+",
                        help="Saved spatial runs covering the selected random4 candidates")
    parser.add_argument("--output", type=Path, default=ROOT / "maxent/cikti/mekansal_20261108")
    parser.add_argument("--java", default="/usr/lib/jvm/java-21-openjdk/bin/java")
    args = parser.parse_args()
    if len(set(args.candidates)) != len(args.candidates):
        parser.error("Duplicate candidates")
    if args.compare_spatial and (args.partition != "random4" or not args.run_java):
        parser.error("--compare-spatial requires --partition random4 --run-java")
    candidates = [c for c in ALL_CANDIDATES if c[0] in args.candidates]
    out = args.output.resolve()
    allowed = ROOT / "maxent/cikti/mekansal_20261108"
    if out != allowed and allowed not in out.parents:
        parser.error("Output must be inside maxent/cikti/mekansal_20261108")
    if out.exists():
        parser.error("Output already exists; use a new child directory")
    layers = sorted((ROOT / "maxent/girdi/katmanlar").glob("*.asc"))
    if {p.stem for p in layers} != {"bio18", "buz_yillik", "kaya", "sst_yillik"}:
        raise ValueError("Unexpected environmental layers")
    samples_path = ROOT / "maxent/girdi/adelie_maxent.csv"
    baseline_dir = ROOT / "maxent/cikti/deneme3"
    # Only this workflow's original inputs: other agents may prepare new climate
    # scenarios elsewhere in girdi concurrently; those are not our inputs.
    protected = list((ROOT / "maxent/girdi/katmanlar").rglob("*"))
    protected += [samples_path] + list(baseline_dir.rglob("*"))
    protected += [ROOT / "maxent/maxent.jar", ROOT / "gbif/temiz/adelie_maxent.csv",
                  ROOT / "gbif/temiz/kayitlar_temiz.csv", Path(__file__)]
    before = hashes(protected)
    samples = read_csv(samples_path)
    if samples != read_csv(ROOT / "gbif/temiz/adelie_maxent.csv"):
        raise ValueError("GBIF and model sample copies differ")
    xy = np.array([[float(r["longitude"]), float(r["latitude"])] for r in samples])
    header, first = read_asc(layers[0])
    valid = first != header["nodata_value"]
    for path in layers[1:]:
        h, a = read_asc(path)
        if h != header:
            raise ValueError("Environmental grids differ")
        valid &= a != h["nodata_value"]
    rc = cells(xy, header)
    if len(set(map(tuple, rc))) != len(samples) or not valid[tuple(rc.T)].all():
        raise ValueError("Samples duplicated in cells or lack environmental data")
    labels, design = geographic_folds(rc)
    spatial_counts = np.bincount(labels, minlength=4).tolist()
    if args.partition == "random4":
        labels = random_folds(labels, args.seed)
    design.update({"partition": args.partition, "reference_spatial_counts": spatial_counts,
                   "partition_seed": args.seed if args.partition == "random4" else None,
                   "partition_rng": "numpy.PCG64 single permutation" if args.partition == "random4" else None,
                   "actual_counts": np.bincount(labels, minlength=4).tolist(),
                   "old_outputs_provisional": True, "final_winner_selected": False})
    design.update({"target": "provisional general occurrence", "ecological_M_final": False,
                   "background": "all valid cells in existing full domain, equal cell weights",
                   "n_background": int(valid.sum()), "seed": "partition_seed above; Java randomseed=false",
                   "candidates": [c[0] for c in candidates],
                   "threshold": "linear training-score 0.10 quantile; omission score < threshold",
                   "limitations": "No buffer; shared full-domain background; not nested CV; tuning bias; no independent optimum"})
    out.mkdir(parents=True)
    write_json(out / "design.json", design)
    write_json(out / "original_hashes.json", before)
    env = out / "layers"
    env.mkdir()
    for path in layers:
        shutil.copyfile(path, env / path.name)
    write_csv(out / "assignments.csv", [dict(sample_index=i, fold=int(labels[i]),
              row=int(rc[i, 0]), col=int(rc[i, 1]), **s) for i, s in enumerate(samples)])
    all_diag, all_metrics, commands = [], [], []
    indices = np.arange(len(samples))
    splits = []
    partition_name = "spatial4" if args.partition == "spatial" else "random4"
    for fold in range(4):
        train, test = indices[labels != fold], indices[labels == fold]
        splits.append((fold, train, test))
        folder = out / f"fold_{fold}"
        folder.mkdir()
        write_csv(folder / "train.csv", [samples[i] for i in train])
        write_csv(folder / "test.csv", [samples[i] for i in test])
        all_diag.extend(dict(design=partition_name, fold=fold, **r)
                        for r in distance_diagnostics(xy, rc, train, test))
    lookup = {tuple(np.round(p, 6)): i for i, p in enumerate(xy)}
    baseline_seen = []
    baseline_metrics = []
    for fold in range(10):
        p = baseline_dir / f"Pygoscelis_adeliae_{fold}_samplePredictions.csv"
        rows = read_csv(p)
        ids = {kind: [lookup[(round(float(r["X"]), 6), round(float(r["Y"]), 6))]
                      for r in rows if r["Test or train"].strip().lower() == kind]
               for kind in ("train", "test")}
        train, test = np.array(ids["train"]), np.array(ids["test"])
        if sorted(list(train) + list(test)) != list(indices):
            raise ValueError("Baseline split does not cover samples exactly")
        baseline_seen.extend(test.tolist())
        all_diag.extend(dict(design="baseline10", fold=fold, **r)
                        for r in distance_diagnostics(xy, rc, train, test))
        write_csv(out / f"baseline_fold_{fold}_assignments.csv",
                  [dict(sample_index=int(i), role=kind) for kind in ids for i in ids[kind]])
        h, a = read_asc(baseline_dir / f"Pygoscelis_adeliae_{fold}.asc")
        if h != header or (a[valid] == h["nodata_value"]).any():
            raise ValueError("Baseline prediction grid mismatch or missing scores")
        scores = a[tuple(rc.T)]
        baseline_metrics.append(dict(candidate="original_default", fold=fold,
                                     **metrics(scores[train], scores[test], a[valid])))
    if sorted(baseline_seen) != list(indices):
        raise ValueError("Baseline held-out samples do not partition observations")
    write_csv(out / "distance_diagnostics.csv", all_diag)
    write_json(out / "distance_summary.json", {name: summarize_distances(
        [r for r in all_diag if r["design"] == name]) for name in (partition_name, "baseline10")})
    write_csv(out / "baseline_metrics_recomputed.csv", baseline_metrics)
    version = {"python": sys.version, "numpy": np.__version__, "platform": platform.platform(),
               "invocation": sys.argv, "java": args.java}
    blocker = None
    if args.run_java:
        try:
            v = subprocess.run([args.java, "-version"], capture_output=True, text=True, check=True)
            version["java_version"] = v.stderr + v.stdout
            for candidate, quadratic, rm in candidates:
                for fold, train, test in splits:
                    folder = out / candidate / f"fold_{fold}"
                    folder.mkdir(parents=True)
                    command = [args.java, "-Xmx512m", "-Djava.awt.headless=true", "-jar",
                               str(ROOT / "maxent/maxent.jar"), "-z", "autorun", "nowarnings",
                               f"samplesfile={out / f'fold_{fold}' / 'train.csv'}",
                               f"environmentallayers={env}", f"outputdirectory={folder}",
                               *feature_arguments(quadratic),
                               f"betamultiplier={rm}", "randomseed=false", "threads=1",
                               "maximumbackground=10000", "addsamplestobackground=false",
                               "removeduplicates=false", "outputformat=cloglog", "outputfiletype=asc",
                               "plots=false", "responsecurves=false", "jackknife=false",
                               "writeplotdata=false", "warnings=false", "visible=false"]
                    commands.append(command)
                    write_json(out / "commands.json", commands)
                    with (folder / "console.log").open("w") as log:
                        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                                                timeout=240, cwd=out)
                    if result.returncode:
                        raise RuntimeError(f"Java exit={result.returncode}; see {folder / 'console.log'}")
                    prediction = folder / "Pygoscelis_adeliae.asc"
                    h, a = read_asc(prediction)
                    if h != header or (a[valid] == h["nodata_value"]).any():
                        raise ValueError("Prediction grid mismatch or missing scores")
                    scores = a[tuple(rc.T)]
                    result_metrics = dict(candidate=candidate, fold=fold,
                                          **metrics(scores[train], scores[test], a[valid]))
                    all_metrics.append(result_metrics)
                    write_csv(folder / "heldout_scores.csv", [dict(sample_index=int(i),
                              score=float(scores[i]), omitted=bool(scores[i] < result_metrics[
                                  "training_p10_threshold"])) for i in test])
                    write_csv(out / "metrics.csv", all_metrics)
                    print(json.dumps(result_metrics), flush=True)
        except (OSError, subprocess.SubprocessError, ValueError, RuntimeError) as exc:
            blocker = f"{type(exc).__name__}: {exc}"
    else:
        blocker = "Java not requested; rerun with --run-java in a new output child directory"
    write_json(out / "versions.json", version)
    summary = []
    for name in [c[0] for c in candidates]:
        rows = [r for r in all_metrics if r["candidate"] == name]
        if len(rows) == 4:
            aucs = [r["test_background_auc"] for r in rows]
            summary.append({"candidate": name, "auc_macro_mean": float(np.mean(aucs)),
                            "auc_fold_sd_population": float(np.std(aucs)),
                            "omission_macro_mean": float(np.mean([r["test_omission_p10"] for r in rows])),
                            "omission_pooled": sum(r["test_omission_p10"] * r["n_test"] for r in rows) / len(samples)})
    write_json(out / "summary.json", {"candidates": summary, "blocker": blocker,
                                      "complete": len(all_metrics) == 4 * len(candidates)})
    (out / "commands.sh").write_text("\n".join(shlex.join(c) for c in commands) + "\n")
    if args.compare_spatial and not blocker:
        matched_comparison(out, args.compare_spatial, labels, header, valid, rc)
    after = hashes(protected)
    if before != after:
        raise RuntimeError("Protected source hashes changed during execution")
    write_json(out / "manifest.json", {"input_sha256": before, "originals_unchanged": True,
               "output_sha256": hashes(out.rglob("*")), "blocker": blocker})
    if blocker:
        print(blocker, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
