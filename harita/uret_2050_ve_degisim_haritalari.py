#!/usr/bin/env python3
"""Legacy entry point: isolated, correctly labelled sensitivity/change maps.

Original 2050-named exports and the original QGIS project are retained.
Use --smooth-display for display-only interpolation; analytical grids never change.
"""
from duzeltilmis_haritalar import main

if __name__ == '__main__':
    main(default_kinds=['duyarlilik','degisim','belirsizlik'])
