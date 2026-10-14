"""50 hPa against the model's highest level (CHAPTER_KNOWN_PROPERTIES.md section 4.3).

The model top is 50 hPa and the highest mass level sits at ~51.9 hPa, so 50 hPa lies
above the last level, where wrf-python's vinterp copies the top level
(fortran/wrf_vinterp.f90, "Assign the highest model level"). This checks that t and z
at 50 hPa ARE the top level, and how far the hydrostatic 50 hPa surface lies above it.

Usage: python tools/audit/f1_top_level.py <GRIB of a timestep> <its wrfout>
Measured 2026-10-14 on 2024-01-19 00Z: docs/audit/f1-pressure-levels.md.
"""
import sys

import eccodes
import netCDF4 as nc
import numpy as np

want = {('z', 50), ('t', 50), ('z', 100), ('t', 100)}
v = {}
with open(sys.argv[1], 'rb') as fh:
    while (g := eccodes.codes_grib_new_from_file(fh)) is not None:
        try:
            if eccodes.codes_get(g, 'typeOfLevel') == 'isobaricInhPa':
                k = (eccodes.codes_get(g, 'shortName'), eccodes.codes_get(g, 'level'))
                if k in want:
                    v[k] = eccodes.codes_get_values(g)
        finally:
            eccodes.codes_release(g)
d = nc.Dataset(sys.argv[2])
P = (d['P'][0, -1] + d['PB'][0, -1]).ravel() / 100
PH = d['PH'][0, -2:] + d['PHB'][0, -2:]
zt = (0.5 * (PH[0] + PH[1]) / 9.81).ravel()
T = ((d['T'][0, -1] + 300).ravel()) * (P / 1000) ** 0.2857
print('top mass level p hPa: mean %.2f' % P.mean())
print('t@50 - T_top: max abs %.4f K' % np.abs(v[('t', 50)] - T).max())
print('z@50/9.80665 - z_top: max abs %.2f m' % np.abs(v[('z', 50)] / 9.80665 - zt).max())
dz = 287.05 * T / 9.81 * np.log(P / 50)
print('hydrostatic gap top level -> 50 hPa: mean %.0f m, range %.0f..%.0f m' % (dz.mean(), dz.min(), dz.max()))
print('z 100->50 thickness as published, mean %.0f m' % ((v[('z', 50)] - v[('z', 100)]) / 9.80665).mean())
