#!/usr/bin/env python3
"""Legacy entry point: matched individual maps from one validated analysis.

Uses the common scale/layout and correctly identifies the hypothetical scenario.
Original three-panel outputs remain in Git history and at their original paths.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'harita'))
from duzeltilmis_haritalar import main

if __name__ == '__main__':
    main(default_kinds=['gunumuz','duyarlilik','degisim'])
