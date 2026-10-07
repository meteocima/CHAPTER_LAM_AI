"""The hour 23Z -> 00Z of a day, which the 0-H archive did not hold (#70).

The run for day D starts at 18Z of D-1 and ends at 00Z of D+1, and the archive
took 00Z of D+1 from the NEXT run. So the last hour of D lives only in the 24 h
file of D's own run. This compares, for the 19 native accumulators:

  the hour from the same run      24 h file - 23Z            (must be >= 0)
  its share of the day            (24 h - 23Z) / (24 h - 00Z)
  the naive cross-run difference  next run's 00Z - 23Z      (what the archive
                                                              could have offered)

and T2 of the two runs at the same instant.

Usage: python tools/audit/dayend_hour.py <24h file of run D> <23Z of D> <00Z of D> <00Z of D+1, next run>
Measured 2026-10-07 on 2019-02-10 (run 2019020918): docs/audit/f5-water-cycle.md.
"""
import sys, numpy as np, netCDF4
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parents[2]))
from accum_ref import ACCUMULATED_VARS
f24, f23, f00, fnext = sys.argv[1:5]   # run D 24h, run D 23Z, run D 00Z of day D, run D+1 00Z of D+1
A, B, R, C = (netCDF4.Dataset(p) for p in (f24, f23, f00, fnext))
for d in (A, B, R, C):
    print(d.filepath().split('/')[-1], 'START_DATE', d.getncattr('START_DATE'), 'Times', bytes(d['Times'][0]).decode())
print(f"{'var':10s} {'h23-24 mean':>12s} {'min(A-B)':>10s} {'share of 24h':>12s} {'naive C-B mean':>15s} {'naive<0 pts%':>12s}")
for v in ACCUMULATED_VARS:
    if v not in A.variables: print(v, 'absent'); continue
    a, b, r, c = (np.asarray(x[v][0], dtype=np.float64) for x in (A, B, R, C))
    hour = a - b; day = a - r; naive = c - b
    share = hour.mean() / day.mean() if day.mean() != 0 else float('nan')
    print(f"{v:10s} {hour.mean():12.4e} {hour.min():10.3e} {share:12.4f} {naive.mean():15.4e} {100*(naive < -1e-6).mean():12.2f}")
t = np.asarray(A['T2'][0]) - np.asarray(C['T2'][0])
print(f"T2 run D vs run D+1 at the same instant: mean {t.mean():+.3f} K, abs max {np.abs(t).max():.2f} K")
