"""Validated EPSG:4326 ESRI ASCII grids and WGS84 ellipsoidal cell areas."""
from dataclasses import dataclass
from pathlib import Path
import math
import numpy as np


@dataclass(frozen=True)
class Grid:
    ncols: int
    nrows: int
    xllcorner: float
    yllcorner: float
    cellsize: float
    nodata: float = -9999.0

    def compatible(self, other):
        return (self.ncols == other.ncols and self.nrows == other.nrows
                and all(math.isclose(getattr(self,k),getattr(other,k),abs_tol=1e-10,
                    rel_tol=0) for k in ('xllcorner','yllcorner','cellsize')))

    @property
    def extent(self):
        return (self.xllcorner,self.yllcorner,self.xllcorner+self.ncols*self.cellsize,
                self.yllcorner+self.nrows*self.cellsize)


def read_grid(path):
    with Path(path).open() as stream:
        h={}
        for _ in range(6):
            parts=stream.readline().split()
            if len(parts)!=2: raise ValueError(f'Invalid ASCII header: {path}')
            h[parts[0].lower()]=float(parts[1])
        required={'ncols','nrows','xllcorner','yllcorner','cellsize','nodata_value'}
        if set(h)!=required or not all(math.isfinite(x) for x in h.values()):
            raise ValueError(f'Expected finite corner-based ASCII header: {path}')
        for k in ('ncols','nrows'):
            if h[k]<1 or h[k]!=int(h[k]):raise ValueError('Invalid dimensions')
        if h['cellsize']<=0:raise ValueError('cellsize must be positive')
        g=Grid(int(h['ncols']),int(h['nrows']),h['xllcorner'],h['yllcorner'],
               h['cellsize'],h['nodata_value'])
        values=np.loadtxt(stream,ndmin=2)
    if values.shape!=(g.nrows,g.ncols):raise ValueError(f'Grid dimensions disagree: {path}')
    if not np.isfinite(values).all():raise ValueError(f'NaN/Inf requires explicit NoData: {path}')
    return g,np.where(values==g.nodata,np.nan,values)


def aligned(reference,path):
    g,values=read_grid(path)
    if not reference.compatible(g):raise ValueError(f'Grid alignment differs: {path}')
    return values


def write_grid(path,grid,values):
    values=np.asarray(values)
    if values.shape!=(grid.nrows,grid.ncols) or np.isinf(values).any():raise ValueError('Invalid output grid')
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w') as stream:
        stream.write(f'ncols {grid.ncols}\nnrows {grid.nrows}\nxllcorner {grid.xllcorner:.9f}\n'
                     f'yllcorner {grid.yllcorner:.9f}\ncellsize {grid.cellsize:.9f}\n'
                     f'NODATA_value {grid.nodata:g}\n')
        np.savetxt(stream,np.where(np.isnan(values),grid.nodata,values),fmt='%.9f')


def cell_areas_km2(grid):
    """WGS84 surface integral M*N*cos(phi) over parallel-bounded rectangles.

    No resampling, spherical approximation, or polar-stereographic area bias.
    """
    west,south,east,north=grid.extent
    if not (-180<=west<east<=180 and -90<=south<north<=90):
        raise ValueError('Requires EPSG:4326 degrees')
    a,e2=6378137.0,6.6943799901413165e-3;e=math.sqrt(e2)
    def primitive(latitude):
        u=math.sin(math.radians(latitude))
        return a*a*(1-e2)/2*(u/(1-e2*u*u)+math.atanh(e*u)/e)
    rows=[math.radians(grid.cellsize)*(primitive(north-i*grid.cellsize)
          -primitive(north-(i+1)*grid.cellsize))/1e6 for i in range(grid.nrows)]
    return np.repeat(np.asarray(rows)[:,None],grid.ncols,axis=1)
