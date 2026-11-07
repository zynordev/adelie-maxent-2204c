import unittest
import numpy as np
from cmip6_delta_katmanlari import nearest_indices,warm_quarter_precip,precipitation_ratio


class DeltaTests(unittest.TestCase):
    def test_great_circle_and_mask(self):
        lat=np.array([[-68.,-68.]]);lon=np.array([[-70.,-68.]])
        index,distance=nearest_indices(lat,lon,lat,lon,np.array([[False,True]]))
        np.testing.assert_array_equal(index,[[1,1]])
        self.assertLess(distance[0,1],.001)
        self.assertGreater(distance[0,0],70)

    def test_warm_quarter_reselected(self):
        temp=np.zeros((12,1,1));prec=np.arange(1,13,dtype=float).reshape(12,1,1)
        temp[0:3]=10
        bio,q=warm_quarter_precip(temp,prec)
        self.assertEqual(q[0,0],0);self.assertEqual(bio[0,0],6)
        temp[:]=0;temp[6:9]=10
        bio,q=warm_quarter_precip(temp,prec)
        self.assertEqual(q[0,0],6);self.assertEqual(bio[0,0],24)

    def test_zero_precip_refused(self):
        with self.assertRaises(ValueError):precipitation_ratio(np.array([0.]),np.array([10.]))
        np.testing.assert_array_equal(precipitation_ratio(np.array([10.]),np.array([20.])),[2.])


if __name__=='__main__':unittest.main()
