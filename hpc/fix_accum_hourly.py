#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Turn grib_v3's accumulations into hourly ones (issue #70).

Until #70 every accumulated field was written referred to 00Z of the same day,
step 0-H, and 00Z itself held zero. ERA5, ITINERE and ICON-2I all publish the
hour ending at the validity time, and the hour 23Z -> 00Z was in no file at
all. After this pass each of the 19 accumulations covers the hour ending at
its validity: reference time = validity - 1 h, step 0-1 (template 8 as before).

    01Z of D        already the hour 00Z -> 01Z: nothing to change
    02Z..23Z of D   cum(H) - cum(H-1), both from the archive, same run
    00Z of D        the hour 23Z(D-1) -> 00Z(D), from the run for D-1:
                    published(snap24 - ref00(D-1)) - cum(23Z, D-1)   [GRIB of D-1]
                    or published(snap24 - snap23)                    [no GRIB of D-1]

snap24/snap23 are accumulator snapshots of that run (accum_hourly.py, fetched
by hpc/fetch_snapshots.sh), ref00 the 00Z sidecar of D-1 (accum_ref.py).
Packing is 24-bit with a quantum of 3.7e-9 m on tp and 1-2 J/m^2 on radiation,
so the difference of two archived values is exact to one quantum.

Only the accumulated messages are re-encoded; every other message is copied
byte for byte. Each file is rewritten to a temporary file, checked, fsync'ed
and renamed over the original.
"""

import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone

import numpy as np
from eccodes import (codes_get, codes_get_message, codes_get_values,
                     codes_grib_new_from_file, codes_release, codes_set,
                     codes_set_values, codes_write)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import accum_hourly  # noqa: E402
import accum_ref  # noqa: E402

MISSING = 9999.0    # the converter's GRIB missing-value sentinel, with a bitmap


def _set_hourly_time(gid, valid):
    ref = valid - timedelta(hours=1)
    codes_set(gid, 'dataDate', int(ref.strftime('%Y%m%d')))
    codes_set(gid, 'dataTime', int(ref.strftime('%H%M')))
    codes_set(gid, 'stepUnits', 'h')
    codes_set(gid, 'startStep', 0)
    codes_set(gid, 'endStep', 1)


def rewrite_hour(path, valid, values):
    """Rewrite the accumulations of `path` (valid at `valid`) as the hour ending
    there. `values` maps paramId -> new values (NaN = missing); every message
    whose paramId is a key is re-encoded, all others are copied unchanged."""
    path = str(path)
    fd, tmp = tempfile.mkstemp(prefix=os.path.basename(path) + '.', suffix='.tmp',
                               dir=os.path.dirname(path))
    done, n_in = set(), 0
    try:
        with open(path, 'rb') as src, os.fdopen(fd, 'wb') as dst:
            while (gid := codes_grib_new_from_file(src)) is not None:
                try:
                    n_in += 1
                    param = codes_get(gid, 'paramId')
                    if param not in values:
                        dst.write(codes_get_message(gid))
                        continue
                    if codes_get(gid, 'productDefinitionTemplateNumber') != 8:
                        raise ValueError(f"{path}: paramId {param} is not template 8")
                    _set_hourly_time(gid, valid)
                    flat = np.asarray(values[param], dtype=np.float64).ravel()
                    if np.isnan(flat).any():
                        codes_set(gid, 'missingValue', MISSING)
                        codes_set(gid, 'bitmapPresent', 1)
                        flat = np.where(np.isnan(flat), MISSING, flat)
                    codes_set_values(gid, flat)
                    codes_write(gid, dst)
                    done.add(param)
                finally:
                    codes_release(gid)
            dst.flush()
            os.fsync(dst.fileno())
        if done != set(values):
            raise ValueError(f"{path}: no message for paramId {sorted(set(values) - done)}")
        if _count(tmp) != n_in:
            raise ValueError(f"{path}: rewritten file does not hold {n_in} messages")
        os.chmod(tmp, os.stat(path).st_mode & 0o777)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def _count(path):
    n = 0
    with open(path, 'rb') as fh:
        while (gid := codes_grib_new_from_file(fh)) is not None:
            codes_release(gid)
            n += 1
    return n


# ---------------------------------------------------------------------------
# One day
# ---------------------------------------------------------------------------
def registry_params():
    """registry key -> paramId of every accumulated field (19)."""
    from wrf_era5_comparison import WRF_TO_ECMWF_PARAMID
    return {k: v['paramId'] for k, v in WRF_TO_ECMWF_PARAMID.items()
            if v.get('stepType') == 'accum'}


def read_accum(path, valid, paramids):
    """{paramId: (values, quantum)} and whether the file is already hourly.
    A file is hourly when every accumulation is referred to valid - 1 h with a
    one-hour step; 01Z is hourly in both encodings, which is what it should be."""
    ref = valid - timedelta(hours=1)
    out, hourly = {}, set()
    with open(path, 'rb') as fh:
        while (gid := codes_grib_new_from_file(fh)) is not None:
            try:
                p = codes_get(gid, 'paramId')
                if p not in paramids:
                    continue
                q = 2.0 ** codes_get(gid, 'binaryScaleFactor') * 10.0 ** -codes_get(gid, 'decimalScaleFactor')
                out[p] = (codes_get_values(gid).astype(np.float64), q)
                hourly.add(codes_get(gid, 'dataDate') == int(ref.strftime('%Y%m%d'))
                           and codes_get(gid, 'dataTime') == int(ref.strftime('%H%M'))
                           and codes_get(gid, 'endStep') - codes_get(gid, 'startStep') == 1)
            finally:
                codes_release(gid)
    if set(out) != set(paramids):
        raise ValueError(f"{path}: missing accumulations {sorted(set(paramids) - set(out))}")
    if len(hourly) != 1:
        raise ValueError(f"{path}: accumulations in mixed encodings")
    return out, hourly.pop()


def _difference(key, now, before):
    """Hourly value from two 0-H values of the same run. Sums of monotone
    accumulators are clipped at zero: one packing quantum of noise either way."""
    d = now - before
    return d if key in accum_hourly.NET_RADIATION else np.where(d < 0, 0.0, d)


def _ref00(ref_dir, day, run):
    fields, meta = accum_ref.load_sidecar(accum_ref.sidecar_path(str(ref_dir), day))
    start = meta.get('SIMULATION_START_DATE')
    if start != f"{run:%Y-%m-%d_%H:%M:%S}":
        raise ValueError(f"00Z sidecar of {day:%Y-%m-%d} is from run {start}, not {run:%Y%m%d%H}")
    return fields


def fix_00z(valid, path_of, ref_dir, snap_dir, params, use_archive_23z):
    """The hour 23Z(D-1) -> 00Z(D), from the run for D-1."""
    curr, prev = accum_hourly.window(valid)
    snap24 = accum_hourly.load_snapshot(snap_dir, curr)
    if use_archive_23z:
        ref00 = _ref00(ref_dir, prev.valid, curr.run)
        cum24 = accum_hourly.published({v: snap24[v].astype(np.float64) - ref00[v] for v in snap24})
        cum23, hourly23 = read_accum(path_of(prev.valid), prev.valid, set(params.values()))
        if hourly23:
            raise RuntimeError(f"{path_of(prev.valid)} is already hourly: the hour ending at "
                               f"{valid:%Y-%m-%dT%H} needs a native snapshot of {prev}")
        values = {pid: _difference(key, cum24[key].ravel(), cum23[pid][0])
                  for key, pid in params.items()}
    else:
        snap23 = accum_hourly.load_snapshot(snap_dir, prev)
        hour = accum_hourly.published({v: snap24[v].astype(np.float64) - snap23[v] for v in snap24})
        values = {pid: hour[key].ravel() for key, pid in params.items()}
    rewrite_hour(path_of(valid), valid, values)


def _write_missing(path, valid, params):
    """The hour ending at `valid` as all-missing (bitmap): for a source declared lost."""
    with open(path, 'rb') as fh:
        gid = codes_grib_new_from_file(fh)
        try:
            size = codes_get(gid, 'numberOfDataPoints')
        finally:
            codes_release(gid)
    rewrite_hour(path, valid, {pid: np.full(size, np.nan) for pid in params.values()})


def fix_day(day, archive_days, path_of, ref_dir, snap_dir, params=None,
            missing_00z_as_bitmap=False):
    """Make every accumulation of `day` hourly, and the 00Z that closes it.

    Order is what makes a crash harmless: the next day's 00Z first (it needs
    this day's 23Z still in the 0-H encoding), then 23Z down to 02Z (each needs
    the hour before it still untouched). A file already hourly is skipped.

    A 00Z whose snapshot is absent is never guessed. By default the day's OWN
    00Z (start of a block) is left as it was and reported, since nothing
    depends on it, while a missing NEXT-day 00Z stops the day before 23Z is
    touched: once 23Z is hourly, that hour could only come from a native
    snapshot of 23Z, i.e. from fetching a 9 GB file again. A snapshot may just
    not have arrived yet, so that is the default. `missing_00z_as_bitmap` is
    for a source declared lost: the 00Z is written all-missing (a bitmap,
    never zero) and the rest of the day goes on.

    Returns the problems that did not stop the day.
    """
    params = params or registry_params()
    pids = set(params.values())
    d0 = datetime(day.year, day.month, day.day)
    is_hourly = lambda v: read_accum(path_of(v), v, pids)[1]   # noqa: E731
    problems = []
    absent = [f"{d0 + timedelta(hours=h):%Y-%m-%dT%H}" for h in range(1, 24)
              if not os.path.isfile(path_of(d0 + timedelta(hours=h)))]
    if absent:
        raise FileNotFoundError(f"{d0:%Y-%m-%d} incomplete, nothing rewritten: no GRIB for {absent}")

    if (d0 - timedelta(days=1)).date() not in archive_days and os.path.isfile(path_of(d0)) \
            and not is_hourly(d0):
        try:
            fix_00z(d0, path_of, ref_dir, snap_dir, params, use_archive_23z=False)
        except FileNotFoundError as exc:
            if missing_00z_as_bitmap:
                _write_missing(path_of(d0), d0, params)
                problems.append(f"{d0:%Y-%m-%dT%H} written missing: {exc}")
            else:
                problems.append(f"{d0:%Y-%m-%dT%H} left 0-H: {exc}")
    nxt = d0 + timedelta(days=1)
    if os.path.isfile(path_of(nxt)) and not is_hourly(nxt):
        try:
            fix_00z(nxt, path_of, ref_dir, snap_dir, params,
                    use_archive_23z=not is_hourly(d0 + timedelta(hours=23)))
        except FileNotFoundError as exc:
            if not missing_00z_as_bitmap:
                raise
            _write_missing(path_of(nxt), nxt, params)
            problems.append(f"{nxt:%Y-%m-%dT%H} written missing: {exc}")
    for h in range(23, 1, -1):
        v = d0 + timedelta(hours=h)
        now, hourly = read_accum(path_of(v), v, pids)
        if hourly:
            continue
        before, before_hourly = read_accum(path_of(v - timedelta(hours=1)), v - timedelta(hours=1), pids)
        if before_hourly and h > 2:
            raise RuntimeError(f"{path_of(v)} is 0-H but the hour before is already hourly")
        rewrite_hour(path_of(v), v, {pid: _difference(key, now[pid][0], before[pid][0])
                                     for key, pid in params.items()})
    return problems


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
WORK_DIR = '/leonardo_work/AIFPT_AILAMIT/CHAPTER'


def archive_path(grib_root):
    """valid time -> archived GRIB path (conf/pipeline.yaml name_template)."""
    return lambda v: os.path.join(grib_root, f"{v:%Y}", f"{v:%m}",
                                  f"ailam-an-cima-3km-{v:%Y}-{v:%Y}-1h-v1-{v:%Y%m%d%H}.grib")


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--grib-root', default=f'{WORK_DIR}/grib_v3')
    ap.add_argument('--accum-ref-dir', default=f'{WORK_DIR}/accum_ref_v2')
    ap.add_argument('--snap-dir', default=f'{WORK_DIR}/accum_snap')
    ap.add_argument('--ledger', default=f'{WORK_DIR}/logs/fix_accum_hourly_status.log')
    ap.add_argument('--month', action='append', default=[], help='YYYY-MM (repeatable)')
    ap.add_argument('--date', action='append', default=[], help='YYYY-MM-DD (repeatable)')
    ap.add_argument('--missing-00z-as-bitmap', action='store_true',
                    help='write a 00Z whose snapshot is absent as all-missing instead of '
                         'stopping: ONLY for a source declared lost, never for one in transit')
    args = ap.parse_args()
    if not args.month and not args.date:
        ap.error('give --month and/or --date')

    path_of = archive_path(args.grib_root)
    days = {datetime.strptime(d, '%Y-%m-%d') for d in args.date}
    for m in args.month:
        d = datetime.strptime(m, '%Y-%m')
        while d.strftime('%Y-%m') == m:
            days.add(d)
            d += timedelta(days=1)
    # A day is in the archive when its 23Z is: that is what the next 00Z needs.
    in_archive = lambda d: os.path.isfile(path_of(d + timedelta(hours=23)))   # noqa: E731
    params = registry_params()
    failed = 0
    for day in sorted(days):
        if not in_archive(day):
            present = [h for h in range(24) if os.path.isfile(path_of(day + timedelta(hours=h)))]
            if not present:
                continue                  # not converted at all: not this pass's business
            status, detail, failed = 'INCOMPLETE', f"no 23Z GRIB; {len(present)}/24 hours present", failed + 1
        else:
            neighbours = {(day + timedelta(days=k)).date() for k in (-1, 0)
                          if in_archive(day + timedelta(days=k))}
            try:
                problems = fix_day(day, neighbours, path_of, args.accum_ref_dir, args.snap_dir,
                                   params, args.missing_00z_as_bitmap)
                status, detail = ('PARTIAL', ' ; '.join(problems)) if problems else ('FIXED', '')
                failed += bool(problems)
            except Exception as exc:      # noqa: BLE001 - recorded, the next day goes on
                status, detail, failed = 'ERROR', f"{type(exc).__name__}: {exc}", failed + 1
        line = f"{datetime.now(timezone.utc):%Y-%m-%dT%H:%M:%SZ} | {day:%Y-%m-%d} | {status} | {detail}"
        print(line, flush=True)
        with open(args.ledger, 'a') as fh:
            fh.write(line + '\n')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
