"""The daily run switch (#72): RMS / p99 / max of the change between two GRIB files.

Since #72 00Z of day D is the last hour of the run for D-1 and 01Z the first published
hour of the run for D, so the switch between runs falls between 00Z and 01Z. This
compares that change against an ordinary hour within one run, on the archive's own files.

Usage: python tools/audit/run_switch.py LABEL:A.grib:B.grib [...]
Measured 2026-10-14 on 2024-01-18/19 (runs 2024011718, 2024011818):
docs/audit/f5-water-cycle.md, CHAPTER_KNOWN_PROPERTIES.md section 8.5.
"""
import sys

import eccodes
import numpy as np

FIELDS = ('2t', 'sp', '10u', '10v', 'tcwv', 't@850', 'z@500')


def read(path):
    out = {}
    with open(path, 'rb') as fh:
        while (g := eccodes.codes_grib_new_from_file(fh)) is not None:
            try:
                name = eccodes.codes_get(g, 'shortName')
                if eccodes.codes_get(g, 'typeOfLevel') == 'isobaricInhPa':
                    name = f"{name}@{eccodes.codes_get(g, 'level')}"
                if name in FIELDS:
                    v = eccodes.codes_get_values(g)
                    if eccodes.codes_get(g, 'bitmapPresent'):
                        v = np.where(v == eccodes.codes_get(g, 'missingValue'), np.nan, v)
                    out[name] = v
            finally:
                eccodes.codes_release(g)
    out['ws10'] = np.hypot(out.pop('10u'), out.pop('10v'))
    out['sp'] = out['sp'] / 100.0      # hPa
    return out


cache = {}
rows = []
for arg in sys.argv[1:]:
    label, a, b = arg.split(':')
    for p in (a, b):
        cache.setdefault(p, read(p))
    for name in sorted(cache[a]):
        d = cache[b][name] - cache[a][name]
        d = d[np.isfinite(d)]
        rows.append((name, label, np.sqrt(np.mean(d ** 2)), np.percentile(np.abs(d), 99), np.abs(d).max()))
for name, label, rms, p99, mx in sorted(rows):
    print(f"{name:6s} {label:34s} rms {rms:8.3f}  p99 {p99:8.3f}  max {mx:8.3f}")
