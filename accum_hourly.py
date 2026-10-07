#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hourly accumulations: every accumulated field covers the hour ENDING at its
validity time, as ERA5, ITINERE and ICON-2I publish them (issue #70).

    field(H) = WRF(H) - WRF(H - 1 h)      both states from the SAME run

The run for target day D starts at 18Z of D-1 and lasts 30 h, so it ends at
00Z of D+1. The archive takes 00Z of D from the run for D (6 h of spin-up),
whose accumulators start there; the hour 23Z(D-1) -> 00Z(D) exists only in
the run for D-1, as its 24 h file -- which the archive never fetched. So:

    01Z..23Z of D  -> run for D:    the archived file and the one before it
    00Z of D       -> run for D-1:  its 24 h file and its 23Z file

A state is a (valid time, run init) pair: 00Z of D exists in two runs.
"""

import os
import sys
from collections import namedtuple
from datetime import datetime, timedelta

import numpy as np

import accum_ref

INIT_HOUR = 18

State = namedtuple('State', 'valid run')


def run_for_day(day):
    """Init time of the run whose 24 files make up target day `day`."""
    d = day.replace(hour=0, minute=0, second=0, microsecond=0)
    return d - timedelta(days=1) + timedelta(hours=INIT_HOUR)


def archive_state(valid):
    """The state an archived file valid at `valid` holds: the run for its own day."""
    return State(valid, run_for_day(valid))


def window(valid):
    """(current, previous) states whose difference is the hour ending at `valid`."""
    day = valid if valid.hour else valid - timedelta(days=1)
    run = run_for_day(day)
    return State(valid, run), State(valid - timedelta(hours=1), run)


def state_of(wrfout):
    """The State a wrfout holds, read from the file itself -- never from its
    name: two different files on the relay are called wrfout_d02_<D>_00:00:00.
    The run is SIMULATION_START_DATE (a restart keeps it, and keeps
    accumulating), the instant is Times."""
    from netCDF4 import Dataset
    with Dataset(wrfout) as ds:
        run = ds.SIMULATION_START_DATE
        valid = ds.variables['Times'][0].tobytes().decode()
    fmt = '%Y-%m-%d_%H:%M:%S'
    return State(datetime.strptime(valid, fmt), datetime.strptime(run, fmt))


def source_file(state):
    """(run folder, wrfout name) holding `state` on the relay."""
    return (f"{state.run:%Y%m%d%H}",
            f"wrfout_d02_{state.valid:%Y-%m-%d_%H}:00:00")


# ---------------------------------------------------------------------------
# What is published, from the native hourly increments
# ---------------------------------------------------------------------------
# Net radiation, ECMWF sign convention: downward minus upward. There is no
# downward longwave at the top of the atmosphere (ACLWDNT is identically zero),
# so ttr/ttrc are just minus the upward flux and come out negative.
NET_RADIATION = {
    'ssr':  ('ACSWDNB', 'ACSWUPB'),    'ssrc': ('ACSWDNBC', 'ACSWUPBC'),
    'str':  ('ACLWDNB', 'ACLWUPB'),    'strc': ('ACLWDNBC', 'ACLWUPBC'),
    'tsr':  ('ACSWDNT', 'ACSWUPT'),    'tsrc': ('ACSWDNTC', 'ACSWUPTC'),
    'ttr':  (None, 'ACLWUPT'),         'ttrc': (None, 'ACLWUPTC'),
}

# Native accumulators published as they are, with the factor to their ECMWF units.
DIRECT = {
    'RAINNC': 1e-3,                     # tp,   mm -> m
    'SFROFF': 1e-3, 'UDROFF': 1e-3,     # sro/ssro, mm -> m
    'ACSWDNB': 1.0, 'ACLWDNB': 1.0, 'ACSWDNBC': 1.0, 'ACLWDNBC': 1.0,   # J/m^2
    'ACSWDNT': 1.0,                     # tisr
}


def _clip(values):
    """Increments of a monotone accumulator cannot be negative: what is below
    zero is reference or packing noise. Clip only that, and say so when it is
    larger than noise, so a real defect stays visible."""
    low = float(np.nanmin(values)) if values.size else 0.0
    if low < -1e-3:
        print(f"  WARNING: accumulated increment reaches {low:.3e}")
    return np.where(values < 0, 0.0, values)


def published(delta):
    """{registry key: values in GRIB units} for every accumulated field.

    `delta` maps each native accumulator to its increment over the window
    (current state minus previous state, native WRF units). Everything that
    is a sum of monotone accumulators is clipped at zero; net radiation is a
    difference and keeps its sign.
    """
    f = lambda n: np.asarray(delta[n], dtype=np.float64)   # noqa: E731
    out = {k: _clip(f(k)) * scale for k, scale in DIRECT.items()}
    # sf is ECMWF's paramId 144, "snowfall": ALL solid precipitation reaching
    # the surface. IFS has no graupel category; WSM6 does, so it is added back
    # or the archive's solid precipitation is short by whatever froze into
    # graupel rather than snow -- 6.4% of the published snowfall in the domain
    # mean on a February day, 11.97 mm at a point (issue #52). HAILNC is not
    # added: WSM6 has no hail and the field is identically zero.
    out['SNOWNC'] = _clip(f('SNOWNC') + f('GRAUPELNC')) * 1e-3
    out['tirf'] = _clip(f('RAINNC') - f('SNOWNC') - f('GRAUPELNC'))      # kg/m^2
    out['ro'] = _clip(f('SFROFF') + f('UDROFF')) * 1e-3
    for key, (down, up) in NET_RADIATION.items():
        out[key] = -f(up) if down is None else f(down) - f(up)
    return out


# ---------------------------------------------------------------------------
# Snapshots: the 19 native accumulators of one state, so that a conversion or
# the post-pass never depends on a 9 GB wrfout still being on disk. Keyed by
# (valid, run) because 00Z of a day exists in two runs; the state is read
# from the wrfout itself, never from its name.
# ---------------------------------------------------------------------------
def snapshot_path(snap_dir, state):
    return os.path.join(str(snap_dir), f"{state.valid:%Y}", f"{state.valid:%m}",
                        f"accum_{state.valid:%Y%m%d%H}_run{state.run:%Y%m%d%H}.npz")


def write_snapshot(wrfout, snap_dir):
    """Snapshot `wrfout` (atomically) and return the State it holds."""
    state = state_of(wrfout)
    fields, meta = accum_ref.extract_from_wrfout(str(wrfout))
    missing = [v for v in accum_ref.ACCUMULATED_VARS if v not in fields]
    if missing:
        raise KeyError(f"{wrfout} lacks {missing}")
    accum_ref.write_sidecar(snapshot_path(snap_dir, state), fields, meta)
    return state


def load_snapshot(snap_dir, state):
    """{native name: float32 array} of `state`; FileNotFoundError if absent."""
    path = snapshot_path(snap_dir, state)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"no snapshot of {state.valid:%Y-%m-%dT%H} from run "
                                f"{state.run:%Y%m%d%H}: {path}")
    fields, _ = accum_ref.load_sidecar(path)
    return fields


def _local_wrfout(state, near):
    """A wrfout of `state` next to `near`: in the same directory, or in the
    pipeline's <wrfout_dir>/<date>/ layout. Checked by its content."""
    name = source_file(state)[1]
    here = os.path.dirname(os.path.abspath(str(near)))
    for cand in (os.path.join(here, name),
                 os.path.join(os.path.dirname(here), f"{state.valid:%Y-%m-%d}", name)):
        if os.path.isfile(cand) and state_of(cand) == state:
            return cand
    return None


def _snapshot_or_local(snap_dir, state, near):
    try:
        return load_snapshot(snap_dir, state)
    except FileNotFoundError:
        local = _local_wrfout(state, near)
        if local is None:
            raise
        write_snapshot(local, snap_dir)
        return load_snapshot(snap_dir, state)


def increments(input_file, snap_dir, dayend_lost=False):
    """{native accumulator: its increment over the hour ending at the input's
    validity}, native units, float64. For 01Z..23Z the input itself is the
    current state; for 00Z it is not -- it belongs to the next run, 6 h into
    its spin-up -- and both states come from the run for the previous day.
    A state with neither a snapshot nor a local wrfout raises FileNotFoundError:
    an hour is never guessed.

    `dayend_lost` is for a 24 h file verified lost at the source: then a 00Z
    with no 24 h state returns None, and the hour is published missing. It does
    not excuse a 23Z state that has simply not arrived yet."""
    own = state_of(input_file)
    curr, prev = window(own.valid)
    if own == curr:
        fields, _ = accum_ref.extract_from_wrfout(str(input_file))
    elif own.valid.hour == 0:
        try:
            fields = _snapshot_or_local(snap_dir, curr, input_file)
        except FileNotFoundError:
            if dayend_lost:
                return None
            raise
    else:
        raise ValueError(f"{input_file} is from run {own.run:%Y%m%d%H}, not the run for its "
                         f"day ({curr.run:%Y%m%d%H})")
    before = _snapshot_or_local(snap_dir, prev, input_file)
    return {v: fields[v].astype(np.float64) - before[v] for v in accum_ref.ACCUMULATED_VARS}


def consumed(valid):
    """The snapshots the hour ending at `valid` reads -- and nothing else reads:
    each state is the previous state of exactly one hour."""
    curr, prev = window(valid)
    return [curr, prev] if valid.hour == 0 else [prev]


def release(valid, snap_dir, grib_of):
    """Delete the snapshots that nobody needs any more, once the hour ending at
    `valid` has its GRIB. A state is needed by two jobs: the hour it belongs to
    (which must not drop its wrfout before the state is saved, wrfout_may_go)
    and the hour after it (which differences against it). Jobs finish in any
    order, so each one deletes a state only when BOTH have their GRIB:
      - this hour's own state, if the next hour is converted;
      - the state before, if its own hour is converted;
      - for 00Z, the 24 h state, which belongs to no archived hour.
    `grib_of(datetime)` is the GRIB path of an hour. Returns the deleted paths."""
    hour = timedelta(hours=1)
    curr, prev = window(valid)
    candidates = [(archive_state(valid), valid + hour), (prev, prev.valid)]
    if valid.hour == 0:
        candidates.append((curr, valid))
    deleted = []
    for state, other in candidates:
        path = snapshot_path(snap_dir, state)
        if os.path.isfile(path) and os.path.isfile(grib_of(valid)) and os.path.isfile(grib_of(other)):
            os.remove(path)
            deleted.append(path)
    return deleted


def wrfout_may_go(valid, snap_dir, grib_of):
    """May the archived wrfout valid at `valid` be deleted? Only if its state is
    saved, or the hour after it -- the only one that reads that state -- is
    already converted."""
    return (os.path.isfile(snapshot_path(snap_dir, archive_state(valid)))
            or os.path.isfile(grib_of(valid + timedelta(hours=1))))


def _cli(argv):
    if len(argv) == 3 and argv[0] == 'snapshot':
        state = write_snapshot(argv[1], argv[2])
        print(f"written: {snapshot_path(argv[2], state)}")
        return 0
    if len(argv) == 4 and argv[0] in ('release', 'may-delete'):
        # Run by the convert scripts once the GRIB is in place. <grib_pattern> is
        # the GRIB path as a strftime pattern, since the two scripts lay it out
        # differently.
        valid = datetime.strptime(argv[1], '%Y-%m-%dT%H')
        grib_of = lambda v: v.strftime(argv[3])     # noqa: E731
        if argv[0] == 'may-delete':
            return 0 if wrfout_may_go(valid, argv[2], grib_of) else 1
        for path in release(valid, argv[2], grib_of):
            print(f"deleted: {path}")
        return 0
    print("usage: python accum_hourly.py snapshot <wrfout> <snap_dir>\n"
          "       python accum_hourly.py release|may-delete <YYYY-MM-DDTHH> <snap_dir> <grib_pattern>")
    return 2


if __name__ == '__main__':
    sys.exit(_cli(sys.argv[1:]))
