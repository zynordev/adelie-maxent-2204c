import tempfile
import unittest
from pathlib import Path
import numpy as np
from izgara import Grid,read_grid,aligned,cell_areas_km2,write_grid
from fark_analizi import summarize
from hazirla_2050_katmanlari import transform_values


class GridTests(unittest.TestCase):
    def test_roundtrip_and_alignment(self):
        g=Grid(2,2,-70,-69,.25)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.asc';a=np.array([[.1,np.nan],[.2,.3]])
            write_grid(p,g,a);actual,b=read_grid(p)
            self.assertTrue(g.compatible(actual))
            np.testing.assert_allclose(a,b,equal_nan=True)
            with self.assertRaises(ValueError):aligned(Grid(2,2,-69,-69,.25),p)

    def test_nan_inf_and_dimensions_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.asc'
            h='ncols 2\nnrows 1\nxllcorner -70\nyllcorner -69\ncellsize .25\nNODATA_value -9999\n'
            for data in ['nan 1\n','inf 1\n','1\n']:
                p.write_text(h+data)
                with self.assertRaises(ValueError):read_grid(p)

    def test_boundary_thresholds_and_area_denominator(self):
        delta=np.array([[-.1,-.05,0,.05,.1]]);areas=np.array([[2,1,1,1,3]])
        s=summarize(delta,areas,np.ones_like(delta,dtype=bool),.05)
        self.assertEqual(s['kararli']['cells'],3)
        self.assertEqual(s['azalma']['cell_percent'],20)
        self.assertEqual(s['azalma']['domain_area_percent'],25)
        self.assertEqual(s['artis']['domain_area_percent'],37.5)

    def test_ellipsoid_global_surface_area(self):
        area=cell_areas_km2(Grid(360,180,-180,-90,1))
        self.assertAlmostEqual(area.sum(),510065621.724,delta=1)
        self.assertGreater(area[89,0],area[10,0])

    def test_sensitivity_preserves_nodata_and_input(self):
        a=np.array([[90.,np.nan]])
        b=transform_values(a,{'operation':'multiply','value':2,'clip':[0,100]})
        self.assertEqual(b[0,0],100.)
        self.assertTrue(np.isnan(b[0,1]))
        self.assertEqual(a[0,0],90.)


if __name__=='__main__':unittest.main()
