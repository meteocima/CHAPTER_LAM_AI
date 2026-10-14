#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hourly accumulations: every accumulated field covers the hour ENDING at its
validity time, as ERA5, ITINERE and ICON-2I publish them (issue #70).

    field(H) = WRF(H) - WRF(H - 1 h)      both states from the SAME run

The run for target day D starts at 18Z of D-1 and lasts 30 h, so it ends at
00Z of D+1. Its first six hours are spin-up and are never published: the
archive takes 01Z..23Z of D from the run for D, and the WHOLE of 00Z of D --
instantaneous fields and accumulations alike -- from the run for D-1, as its
24 h file (issue #72). So every archived file is one state of one run:

    01Z..23Z of D  -> run for D:    the archived file and the one before it
    00Z of D       -> run for D-1:  its 24 h file and its 23Z file

The state before 01Z of D is 00Z of the run for D, 6 h into its spin-up: it
is fetched for its snapshot alone, never converted (`spinup_state`).

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
    """The state an archived file valid at `valid` holds: the run for its own day,
    or for 00Z the run for the day before (#72). The current state of its hour."""
    return window(valid)[0]


def spinup_state(day):
    """00Z of `day` in the run for `day`, 6 h into its spin-up: the state the hour
    00Z -> 01Z is differenced against, and nothing else. Never archived."""
    d = day.replace(hour=0, minute=0, second=0, microsecond=0)
    return State(d, run_for_day(d))


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


def increments(input_file, snap_dir):
    """{native accumulator: its increment over the hour ending at the input's
    validity}, native units, float64. The input is the current state of its
    hour -- for 00Z of D the 24 h file of the run for D-1 (#72) -- and the state
    before it comes from a snapshot or a wrfout beside the input. Any other
    file is refused, the 00Z of the run for D above all: it is 6 h into its
    spin-up and is never published. A state with neither a snapshot nor a local
    wrfout raises FileNotFoundError: an hour is never guessed."""
    own = state_of(input_file)
    curr, prev = window(own.valid)
    if own != curr:
        why = (" -- the 00Z of a day comes from the previous day's run, its 24 h file (#72)"
               if own.valid.hour == 0 else "")
        raise ValueError(f"{input_file} is from run {own.run:%Y%m%d%H}, not run "
                         f"{curr.run:%Y%m%d%H}{why}")
    fields, _ = accum_ref.extract_from_wrfout(str(input_file))
    before = _snapshot_or_local(snap_dir, prev, input_file)
    return {v: fields[v].astype(np.float64) - before[v] for v in accum_ref.ACCUMULATED_VARS}


def consumed(valid):
    """The snapshots the hour ending at `valid` reads: the state before it. Its
    current state is the input itself, at 00Z too since #72."""
    return [window(valid)[1]]


def readers(state):
    """The hours whose accumulation reads `state`: its own hour, if it is that
    hour's current state, and the hour after, if it is that one's state before.
    An ordinary hour has both; 00Z's 24 h state only its own (01Z reads the
    spin-up state instead); the spin-up state only 01Z."""
    hour = timedelta(hours=1)
    return [v for v in (state.valid, state.valid + hour) if state in window(v)]


def is_hourly_grib(path, valid):
    """Does the GRIB of the hour `valid` already carry the hour ending there? Read
    off its first accumulation (template 8, statistical process 1). A 0-H file of
    the archive before #71 does not, and still needs the state before it."""
    if not os.path.isfile(path):
        return False
    from eccodes import codes_get, codes_grib_new_from_file, codes_release
    ref = valid - timedelta(hours=1)
    with open(path, 'rb') as fh:
        while (gid := codes_grib_new_from_file(fh)) is not None:
            try:
                if (codes_get(gid, 'productDefinitionTemplateNumber') == 8
                        and codes_get(gid, 'typeOfStatisticalProcessing') == 1):
                    return (codes_get(gid, 'dataDate') == int(f"{ref:%Y%m%d}")
                            and codes_get(gid, 'dataTime') == int(f"{ref:%H%M}")
                            and codes_get(gid, 'endStep') - codes_get(gid, 'startStep') == 1)
            finally:
                codes_release(gid)
    return False


def release(valid, snap_dir, grib_of):
    """Delete the snapshots that nobody needs any more, once the hour ending at
    `valid` has its GRIB. A state goes once every hour that reads it (`readers`)
    has its GRIB -- its own hour too, which must not drop its wrfout before the
    state is saved (wrfout_may_go). Jobs finish in any order, so each one looks
    at the two states its hour touches: its own and the one before.
    "Has its GRIB" means an HOURLY one: a 0-H file left from before #71 still
    needs the state before it, to be made hourly by hpc/fix_accum_hourly.py.
    `grib_of(datetime)` is the GRIB path of an hour. Returns the deleted paths."""
    deleted = []
    for state in (archive_state(valid), window(valid)[1]):
        path = snapshot_path(snap_dir, state)
        if os.path.isfile(path) and all(is_hourly_grib(grib_of(v), v) for v in readers(state)):
            os.remove(path)
            deleted.append(path)
    return deleted


def wrfout_may_go(valid, snap_dir, grib_of):
    """May the archived wrfout valid at `valid` be deleted, once its own hour is
    converted? Only if its state is saved, or every other hour that reads that
    state is converted already -- for 00Z there is none (#72)."""
    state = archive_state(valid)
    return (os.path.isfile(snapshot_path(snap_dir, state))
            or all(os.path.isfile(grib_of(v)) for v in readers(state) if v != valid))


def _cli(argv):
    if len(argv) == 2 and argv[0] == 'state':
        # The driver's check that a local file is the state it is named for:
        # two files on the relay are called wrfout_d02_<D>_00:00:00.
        state = state_of(argv[1])
        print(f"{state.valid:%Y%m%d%H} {state.run:%Y%m%d%H}")
        return 0
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
    print("usage: python accum_hourly.py state <wrfout>\n"
          "       python accum_hourly.py snapshot <wrfout> <snap_dir>\n"
          "       python accum_hourly.py release|may-delete <YYYY-MM-DDTHH> <snap_dir> <grib_pattern>")
    return 2


if __name__ == '__main__':
    sys.exit(_cli(sys.argv[1:]))
