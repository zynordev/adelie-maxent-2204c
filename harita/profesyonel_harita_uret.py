#!/usr/bin/env python3
"""Legacy entry point: validated, isolated current-model QGIS export.

Exports to harita/duzeltilmis_v1 and never overwrites harita/a1.qgz.
"""
from duzeltilmis_haritalar import main

if __name__ == '__main__':
    main(default_kinds=['gunumuz'])
