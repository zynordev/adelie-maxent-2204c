"""Meaningful synthetic and real-input checks; no Java or output writes required."""
import importlib.util
from itertools import combinations
import unittest

import numpy as np

from mekansal_dogrulama import (ROOT, band_partition, cells, distance_diagnostics,
                               feature_arguments, geographic_folds, metrics,
                               random_folds, read_asc, read_csv)

spec = importlib.util.spec_from_file_location("quality", ROOT / "gbif/kalite_envanteri.py")
quality = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quality)


class SpatialTests(unittest.TestCase):
    def test_random4_matched_sizes_seed_and_disjoint_coverage(self):
        spatial = np.repeat(np.arange(4), [17, 17, 16, 17])
        labels = random_folds(spatial)
        np.testing.assert_array_equal(np.bincount(labels), [17, 17, 16, 17])
        np.testing.assert_array_equal(labels, random_folds(spatial, 20261108))
        self.assertFalse(np.array_equal(labels, random_folds(spatial, 20261109)))
        self.assertFalse(np.array_equal(labels, spatial))
        covered = []
        for fold, n_train in enumerate([50, 50, 51, 50]):
            train, test = np.flatnonzero(labels != fold), np.flatnonzero(labels == fold)
            self.assertEqual(len(train), n_train)
            self.assertFalse(set(train) & set(test))
            covered.extend(test.tolist())
        self.assertEqual(sorted(covered), list(range(67)))
        # With one original sample per cell, disjoint indices also imply disjoint cells.
        with self.assertRaises(ValueError):
            random_folds(np.array([0, 1, 2]))

    def test_auto_uses_unrestricted_jar_defaults(self):
        self.assertEqual(feature_arguments(None), ["autofeature=true"])
        self.assertIn("quadratic=true", feature_arguments(True))
        self.assertIn("quadratic=false", feature_arguments(False))
        for manual in (False, True):
            self.assertIn("autofeature=false", feature_arguments(manual))
            for family in ("product", "threshold", "hinge"):
                self.assertIn(f"{family}=false", feature_arguments(manual))

    def test_contiguous_balanced_ties(self):
        values = np.repeat(np.arange(8), 3)
        labels, design = band_partition(values)
        self.assertEqual(design["counts"], [6, 6, 6, 6])
        self.assertTrue(np.all(np.diff(labels) >= 0))
        for value in set(values):
            self.assertEqual(len(set(labels[values == value])), 1)
        with self.assertRaises(ValueError):
            band_partition([1, 1, 2])

    def test_band_balance_matches_exhaustive_optimum(self):
        counts = np.array([9, 2, 7, 3, 8, 1, 4])
        values = np.repeat(np.arange(len(counts)), counts)
        _, design = band_partition(values)
        costs = []
        for cuts in combinations(range(1, len(counts)), 3):
            totals = [part.sum() for part in np.split(counts, cuts)]
            costs.append(sum((n - counts.sum() / 4) ** 2 for n in totals))
        self.assertEqual(design["squared_imbalance"], min(costs))

    def test_real_partition_no_point_or_cell_overlap(self):
        rows = read_csv(ROOT / "maxent/girdi/adelie_maxent.csv")
        xy = np.array([[float(r["longitude"]), float(r["latitude"])] for r in rows])
        h, _ = read_asc(ROOT / "maxent/girdi/katmanlar/kaya.asc")
        rc = cells(xy, h)
        labels, design = geographic_folds(rc)
        self.assertEqual(len(labels), 67)
        self.assertGreaterEqual(min(np.bincount(labels)), 10)
        covered = []
        for fold in range(4):
            train, test = np.flatnonzero(labels != fold), np.flatnonzero(labels == fold)
            self.assertFalse(set(train) & set(test))
            self.assertFalse(set(map(tuple, rc[train])) & set(map(tuple, rc[test])))
            self.assertEqual(len(train) + len(test), 67)
            covered.extend(test.tolist())
        self.assertEqual(sorted(covered), list(range(67)))
        col = 0 if design["chosen_axis"] == "latitude" else 1
        self.assertTrue(np.all(np.diff(labels[np.argsort(rc[:, col])]) >= 0))
        np.testing.assert_array_equal(labels, geographic_folds(rc)[0])

    def test_auc_ties_and_training_only_threshold(self):
        result = metrics([0, 1, 2, 3, 4], [0, 2], [0, 1, 2])
        self.assertAlmostEqual(result["test_background_auc"], 0.5)
        self.assertAlmostEqual(result["training_p10_threshold"], 0.4)
        self.assertEqual(result["test_omission_p10"], 0.5)
        self.assertEqual(metrics([1, 1], [1], [1])["test_omission_p10"], 0)
        self.assertEqual(metrics([0, 1], [3], [0, 1, 2])["test_background_auc"], 1)
        self.assertEqual(metrics([0, 1], [-1], [0, 1, 2])["test_background_auc"], 0)
        self.assertEqual(metrics([0, 1, 2, 3, 4], [999], [0])["training_p10_threshold"], 0.4)
        for bad in ([], [float("nan")], [float("inf")]):
            with self.assertRaises(ValueError):
                metrics([0, 1], bad, [1])

    def test_distance_and_adjacency(self):
        xy = np.array([[0., 0.], [1., 0.], [3., 0.]])
        rc = np.array([[0, 0], [0, 1], [0, 3]])
        rows = distance_diagnostics(xy, rc, np.array([0]), np.array([1, 2]))
        self.assertAlmostEqual(rows[0]["nearest_train_km"], 111.1949266, places=5)
        self.assertTrue(rows[0]["adjacent_train_8"])
        self.assertFalse(rows[1]["adjacent_train_8"])
        with self.assertRaises(ValueError):
            distance_diagnostics(xy, rc, np.array([0]), np.array([0]))

    def test_grid_boundary_and_reconstruction(self):
        h, _ = read_asc(ROOT / "maxent/girdi/katmanlar/kaya.asc")
        xy = np.array([[h["xllcorner"] + h["cellsize"], h["yllcorner"] + h["cellsize"]]])
        np.testing.assert_array_equal(cells(xy, h), [[int(h["nrows"]) - 2, 1]])
        reps = quality.reconstruct(read_csv(ROOT / "gbif/temiz/kayitlar_temiz.csv"), h)
        expected = read_csv(ROOT / "gbif/temiz/adelie_maxent.csv")
        self.assertEqual(len(reps), 67)
        for rep, point in zip(reps, expected):
            self.assertEqual(f'{float(rep["decimalLongitude"]):.6f}', point["longitude"])
            self.assertEqual(f'{float(rep["decimalLatitude"]):.6f}', point["latitude"])

    def test_representative_uncertainty_and_numeric_id_ties(self):
        h = dict(nrows=2, ncols=2, xllcorner=0, yllcorner=0, cellsize=1)
        records = [dict(decimalLongitude="0.2", decimalLatitude="0.2",
                        coordinateUncertaintyInMeters=u, gbifID=i)
                   for u, i in (("", "1"), ("10", "2"), ("5", "100"), ("5", "9"))]
        self.assertEqual(quality.reconstruct(records, h)[0]["gbifID"], "9")
        self.assertEqual(quality.reconstruct(records[::-1], h)[0]["gbifID"], "9")


if __name__ == "__main__":
    unittest.main()
