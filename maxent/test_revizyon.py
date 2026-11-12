"""Numerical and design checks for the 2026-11-12 scientific revision."""
import unittest
from pathlib import Path
import tempfile
import numpy as np
from revizyon_denetimi import mess, vif_values
from revizyon_katmanlari import first_persistent
from revizyon_karsilastirma import score_metrics, auc, feature_args
from revizyon_projeksiyon import aicc
from koloni_gelecek import marine_anomaly


class RevisionTests(unittest.TestCase):
    def test_mess_detects_outside_and_constant_columns(self):
        reference=np.array([[0,2],[1,2],[2,2],[3,2]])
        scores=mess(reference,np.array([[1.5,2],[-1,2],[4,2],[1,3]]))
        self.assertAlmostEqual(scores[0],100)
        self.assertTrue(np.all(scores[1:]<0))

    def test_vif_independent_balanced_columns(self):
        x=np.array([[-1,-1],[-1,1],[1,-1],[1,1]],float)
        x=np.tile(x,(3,1))
        for item in vif_values(x,['a','b']):self.assertAlmostEqual(item['vif'],1)

    def test_vif_collinearity_is_explicit(self):
        x=np.arange(12,dtype=float)
        values=vif_values(np.column_stack([x,2*x]),['a','b'])
        self.assertTrue(all(r['singular'] and r['vif'] is None for r in values))

    def test_vif_constant_is_not_silently_finite(self):
        x=np.arange(12,dtype=float)
        values=vif_values(np.column_stack([x,np.ones(12)]),['a','constant'])
        self.assertAlmostEqual(values[0]['vif'],1)
        self.assertTrue(values[1]['constant'])
        self.assertIsNone(values[1]['vif'])

    def test_auc_ties_and_constant_prediction(self):
        self.assertEqual(auc([1,1],[1,1]),.5)
        result=score_metrics(np.ones(5),np.ones(3),np.ones(9))
        self.assertEqual(result['auc'],.5)
        self.assertEqual(result['omission_p10'],0)
        self.assertIsNone(result['boyce_fixed_10_bins'])
        self.assertAlmostEqual(result['partial_roc_ratio_sensitivity95'],1)

    def test_auc_perfect_order(self):
        self.assertEqual(auc([.8,.9],[.1,.2]),1)

    def test_explicit_feature_flags(self):
        flags=feature_args('LQH')
        self.assertIn('autofeature=false',flags)
        self.assertIn('threshold=false',flags)
        self.assertIn('hinge=true',flags)

    def test_persistent_ice_requires_consecutive_days(self):
        a=np.array([0,1,1,0,1,1,1,1,1,0],bool)[:,None,None]
        self.assertEqual(first_persistent(a)[0,0],4)
        self.assertEqual(first_persistent(a[:8])[0,0],-1)

    def test_aicc_invalid_when_parameters_exhaust_sample(self):
        raw=np.array([[1,2],[3,4]],float)
        result=aicc(raw,np.array([[0,0],[1,0]]),2,np.ones_like(raw,bool))
        self.assertIsNone(result['aicc'])

    def test_aicc_normalizes_raw_density(self):
        raw=np.array([[1,2],[3,4]],float);rc=np.array([[0,0],[0,1],[1,0],[1,1]])
        x=aicc(raw,rc,1,np.ones_like(raw,bool))
        y=aicc(raw*10,rc,1,np.ones_like(raw,bool))
        self.assertAlmostEqual(x['aicc'],y['aicc'])

    def test_colony_monthly_anomaly_and_ice_bounds(self):
        lat=np.array([[-66.,-66.],[-67.,-67.]])
        lon=np.array([[-70.,-69.],[-70.,-69.]])
        donor=np.arange(4).reshape(2,2)
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'ice.npz'
            np.savez(path,units=np.array('%'),month=np.arange(1,13),lat=lat,lon=lon,
                baseline=np.zeros((12,2,2)),future=np.full((12,2,2),20.),
                baseline_valid_year_count=np.full((12,2,2),26),future_valid_year_count=np.full((12,2,2),20))
            future,baseline,distance,index=marine_anomaly(np.full((12,2,2),95.),path,lat,lon,donor,'%')
            self.assertTrue(np.all(future==100))
            self.assertTrue(np.all(baseline==0))
            self.assertTrue(np.allclose(distance,0))
            self.assertTrue(np.array_equal(index,donor))
            with self.assertRaises(ValueError):marine_anomaly(np.zeros((12,2,2)),path,lat,lon,donor,'degC')


if __name__=='__main__':unittest.main()
