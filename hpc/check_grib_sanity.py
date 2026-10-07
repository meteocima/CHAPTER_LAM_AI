#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sanity check of CHAPTER GRIB2 files against partly-empty sources and schema drift.

Three independent failure modes are covered:

1. A wrfout that is partly zero-filled (truncated transfer, stub) still opens as
   NetCDF and converts "fine": 2024-12-29T18 came out with lsm, surface z, slor,
   skt, tcc and tp all zero. Some fields can never be all-zero over the domain
   whatever the timestep (NEVER_EMPTY below), so they are the tell.
2. A field that raises inside the converter is reported and the run aborts, but a
   file produced by an older schema would pass unnoticed -- so the full set of
   (shortName -> number of messages) is compared against the registry.
3. Every accumulated field must cover the hour ending at the file's validity
   (issue #70): reference time = validity - 1 h and a one-hour step. That is
   what ERA5 publishes; until #70 the archive referred them to 00Z instead.

Usage (eccodes env as in hpc/convert_step.sh):
    python hpc/check_grib_sanity.py <grib> [<grib> ...]
    python hpc/check_grib_sanity.py --since-minutes 600 --month 2025-04
Exit code 1 if any file is BAD.
"""

import argparse
import collections
import glob
import os
import sys
import time
from datetime import datetime, timedelta

from eccodes import codes_get, codes_grib_new_from_file, codes_release

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from wrf_era5_comparison import WRF_TO_ECMWF_PARAMID  # noqa: E402

# How many messages each shortName must contribute ('z' appears both on the
# pressure levels and at the surface, hence the accumulation).
EXPECTED = collections.Counter()
for _info in WRF_TO_ECMWF_PARAMID.values():
    EXPECTED[_info['shortName']] += len(_info['levels'])

# Fields that can never be all-zero over the domain, whatever the timestep. This
# is a smoke test for a variable that silently failed to compute, not a statement
# about time: skt and the soil layers change every hour. (Not snowc, tsn, fal or
# ci: those are legitimately empty out of season or at night.) The geo_em statics
# belong here because the domain always contains vegetation, soil, lakes and a
# classified soil type; the eight soil layers because even the driest STATSGO
# class has DRYSMC > 0 and every temperature is in kelvin. Note the check reads
# the max of the PRESENT values under a bitmap, which is what is wanted for the
# masked ones (tvl, slt, dl, swvl*, stl*).
NEVER_EMPTY = {'lsm', 'z', 'sdor', 'slor', 'skt', 'al',
               'cvl', 'cvh', 'tvl', 'tvh', 'slt', 'cl', 'dl',
               'swvl1', 'swvl2', 'swvl3', 'swvl4', 'stl1', 'stl2', 'stl3', 'stl4'}
ACCUMULATED = {i['paramId'] for i in WRF_TO_ECMWF_PARAMID.values() if i.get('stepType') == 'accum'}


def accumulation_problem(gid):
    """None, or why an accumulated message is not the hour ending at its validity."""
    param = codes_get(gid, 'paramId')
    if param not in ACCUMULATED:
        return None
    valid = datetime.strptime(f"{codes_get(gid, 'validityDate')}{codes_get(gid, 'validityTime'):04d}", '%Y%m%d%H%M')
    ref = datetime.strptime(f"{codes_get(gid, 'dataDate')}{codes_get(gid, 'dataTime'):04d}", '%Y%m%d%H%M')
    length = codes_get(gid, 'endStep') - codes_get(gid, 'startStep')
    if ref != valid - timedelta(hours=1) or length != 1:
        return (f"{codes_get(gid, 'shortName')} not hourly "
                f"(reference {ref:%Y-%m-%dT%H}, step {codes_get(gid, 'stepRange')})")
    return None


def check(path):
    problems = []
    found = collections.Counter()
    all_zero = set()
    not_hourly = []
    with open(path, 'rb') as fh:
        while True:
            gid = codes_grib_new_from_file(fh)
            if gid is None:
                break
            try:
                name = codes_get(gid, 'shortName')
                found[name] += 1
                if name in NEVER_EMPTY and codes_get(gid, 'maximum') == 0 and codes_get(gid, 'minimum') == 0:
                    all_zero.add(name)
                problem = accumulation_problem(gid)
                if problem:
                    not_hourly.append(problem)
            finally:
                codes_release(gid)

    for name in sorted(all_zero):
        problems.append(f"{name} all zero")
    for name in sorted(set(EXPECTED) | set(found)):
        want, got = EXPECTED[name], found[name]
        if want != got:
            problems.append(f"{name}: {got} messages, expected {want}")
    if not_hourly:
        problems.append(f"{len(not_hourly)} accumulations not hourly, e.g. {not_hourly[0]}")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('files', nargs='*')
    ap.add_argument('--grib-dir', default='/leonardo_work/AIFPT_AILAMIT/CHAPTER/grib_v3')
    ap.add_argument('--month', action='append', default=[], help='YYYY-MM (repeatable)')
    ap.add_argument('--since-minutes', type=float, default=None,
                    help='with --month: only files modified in the last N minutes')
    args = ap.parse_args()
    files = list(args.files)
    for m in args.month:
        for p in sorted(glob.glob(os.path.join(args.grib_dir, m[:4], m[5:7], '*.grib'))):
            if args.since_minutes is None or time.time() - os.path.getmtime(p) < args.since_minutes * 60:
                files.append(p)
    bad = 0
    for p in files:
        problems = check(p)
        print(f"{'BAD ' if problems else 'OK  '} {p}" + (f"  <- {'; '.join(problems)}" if problems else ''),
              flush=True)
        bad += bool(problems)
    print(f"\nchecked={len(files)} bad={bad}")
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
