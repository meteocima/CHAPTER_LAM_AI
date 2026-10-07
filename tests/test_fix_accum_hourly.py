"""The post-pass that turns grib_v3's 0-H accumulations into hourly ones (#70).

Synthetic GRIB2 files on a 3 x 2 grid stand in for the archive: one
accumulation written the way the converter wrote it until now (PDT 8,
reference 00Z, step 0-H) and one instantaneous field, which the post-pass
must leave alone byte for byte.
"""
import importlib.util
import pathlib
import sys
from datetime import datetime, timedelta

import eccodes  # not importorskip: conftest loads the library, and a GRIB test that
import numpy as np  # skips in silence is a test nobody runs (CLAUDE.md, Testing)
import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def fix():
    spec = importlib.util.spec_from_file_location("fix_accum_hourly",
                                                  ROOT / "hpc" / "fix_accum_hourly.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["fix_accum_hourly"] = mod
    spec.loader.exec_module(mod)
    return mod


TP, T2 = 228, 235      # tp and skt: both live on the surface level


def _message(fh, param, values, valid, accum_since_00z):
    gid = eccodes.codes_grib_new_from_samples('GRIB2')
    try:
        if accum_since_00z:
            ref = valid.replace(hour=0)
            eccodes.codes_set(gid, 'productDefinitionTemplateNumber', 8)
            eccodes.codes_set(gid, 'dataDate', int(ref.strftime('%Y%m%d')))
            eccodes.codes_set(gid, 'dataTime', 0)
            eccodes.codes_set(gid, 'stepUnits', 'h')
            eccodes.codes_set(gid, 'startStep', 0)
            eccodes.codes_set(gid, 'endStep', valid.hour)
        else:
            eccodes.codes_set(gid, 'dataDate', int(valid.strftime('%Y%m%d')))
            eccodes.codes_set(gid, 'dataTime', int(valid.strftime('%H%M')))
        eccodes.codes_set(gid, 'paramId', param)
        eccodes.codes_set(gid, 'typeOfLevel', 'surface')
        for k, v in (('Ni', 3), ('Nj', 2), ('latitudeOfFirstGridPointInDegrees', 41.0),
                     ('latitudeOfLastGridPointInDegrees', 40.0),
                     ('longitudeOfFirstGridPointInDegrees', 10.0),
                     ('longitudeOfLastGridPointInDegrees', 12.0),
                     ('iDirectionIncrementInDegrees', 1.0),
                     ('jDirectionIncrementInDegrees', 1.0)):
            eccodes.codes_set(gid, k, v)
        eccodes.codes_set_values(gid, np.asarray(values, dtype=float))
        eccodes.codes_set(gid, 'packingType', 'grid_ccsds')
        eccodes.codes_write(gid, fh)
    finally:
        eccodes.codes_release(gid)


def write_old(path, valid, tp, t2=(280.0, 281, 282, 283, 284, 285)):
    """An archive file as the converter wrote it before #70."""
    with open(path, 'wb') as fh:
        _message(fh, T2, t2, valid, accum_since_00z=False)
        _message(fh, TP, tp, valid, accum_since_00z=True)
    return path


def read(path):
    out = {}
    with open(path, 'rb') as fh:
        while (gid := eccodes.codes_grib_new_from_file(fh)) is not None:
            try:
                p = eccodes.codes_get(gid, 'paramId')
                out[p] = {k: eccodes.codes_get(gid, k) for k in
                          ('dataDate', 'dataTime', 'stepRange', 'validityDate', 'validityTime')}
                out[p]['values'] = eccodes.codes_get_values(gid)
                out[p]['bytes'] = eccodes.codes_get_message(gid)
            finally:
                eccodes.codes_release(gid)
    return out


def test_an_hour_is_rewritten_as_the_hour_ending_at_its_validity(tmp_path, fix):
    valid = datetime(2024, 7, 2, 5)
    path = write_old(tmp_path / 'f.grib', valid, tp=[0.004, 0, 0, 0.001, 0, 0.0005])
    before = read(path)

    fix.rewrite_hour(path, valid, {TP: np.array([0.001, 0, 0, 0.0002, 0, 0])})

    after = read(path)
    tp = after[TP]
    assert (tp['dataDate'], tp['dataTime'], tp['stepRange']) == (20240702, 400, '0-1')
    assert (tp['validityDate'], tp['validityTime']) == (20240702, 500)
    np.testing.assert_allclose(tp['values'], [0.001, 0, 0, 0.0002, 0, 0], atol=1e-8)
    assert after[T2]['bytes'] == before[T2]['bytes']


def test_00z_takes_the_previous_days_23z_as_reference_and_missing_stays_missing(tmp_path, fix):
    valid = datetime(2024, 7, 2, 0)
    path = write_old(tmp_path / 'f.grib', valid, tp=[0.0] * 6)   # old 00Z: zero, step 0
    assert read(path)[TP]['stepRange'] == '0'

    fix.rewrite_hour(path, valid, {TP: np.array([0.0003, np.nan, 0, 0, 0, 0.0001])})

    tp = read(path)[TP]
    assert (tp['dataDate'], tp['dataTime'], tp['stepRange']) == (20240701, 2300, '0-1')
    assert (tp['validityDate'], tp['validityTime']) == (20240702, 0)
    assert tp['values'][1] == 9999.0                               # bitmap, not zero
    with open(path, 'rb') as fh:
        gid = eccodes.codes_grib_new_from_file(fh)       # skt
        eccodes.codes_release(gid)
        gid = eccodes.codes_grib_new_from_file(fh)       # tp
        assert eccodes.codes_get(gid, 'bitmapPresent') == 1
        eccodes.codes_release(gid)
    np.testing.assert_allclose(tp['values'][[0, 5]], [0.0003, 0.0001], atol=1e-8)


# ---------------------------------------------------------------------------
# A whole day. Worked example, not derived from the code: it rains 0.1*H mm in
# the hour ending at H, so the archive's 0-H value at H is 0.1*H*(H+1)/2 mm and
# the hour ending at 24 (00Z of the next day) is 2.4 mm. The run holds 5 mm of
# spin-up at 00Z, so its 24 h file reads 5 + 30 = 35 mm.
# ---------------------------------------------------------------------------
DAY = datetime(2024, 7, 1)
RUN = datetime(2024, 6, 30, 18)          # the run for DAY
PARAMS = {'RAINNC': TP}                  # registry key -> paramId, tp only here
# DAY in the middle of the archive: its own 00Z belongs to the previous day's pass.
MID_ARCHIVE = {(DAY - timedelta(days=1)).date(), DAY.date()}


def hourly_mm(h):
    return 0.1 * h


def build_archive(tmp_path, fix):
    import accum_ref
    arch = tmp_path / 'grib'
    arch.mkdir()
    path_of = lambda v: arch / f"{v:%Y%m%d%H}.grib"            # noqa: E731
    for h in range(24):
        cum_m = 1e-3 * 0.1 * h * (h + 1) / 2
        write_old(path_of(DAY + timedelta(hours=h)), DAY + timedelta(hours=h), tp=[cum_m] * 6)
    write_old(path_of(DAY + timedelta(days=1)), DAY + timedelta(days=1), tp=[0.0] * 6)
    natives = lambda rain: {v: np.full((2, 3), rain if v == 'RAINNC' else 0.0, np.float32)  # noqa: E731
                            for v in accum_ref.ACCUMULATED_VARS}
    ref_dir, snap_dir = tmp_path / 'ref', tmp_path / 'snap'
    accum_ref.write_sidecar(accum_ref.sidecar_path(str(ref_dir), DAY), natives(5.0),
                            {'SIMULATION_START_DATE': f"{RUN:%Y-%m-%d_%H:%M:%S}"})
    import accum_hourly as ah
    snap24 = ah.State(DAY + timedelta(days=1), RUN)
    accum_ref.write_sidecar(ah.snapshot_path(snap_dir, snap24), natives(35.0), {})
    return dict(path_of=path_of, ref_dir=ref_dir, snap_dir=snap_dir, params=PARAMS)


def hourly_values(arch):
    out = {}
    for h in range(1, 25):
        v = DAY + timedelta(hours=h)
        m = read(arch['path_of'](v))[TP]
        out[h] = (m['stepRange'], m['dataDate'] * 100 + m['dataTime'] // 100, m['values'][0])
    return out


def test_a_day_becomes_24_hourly_values_including_23_to_00(tmp_path, fix):
    arch = build_archive(tmp_path, fix)
    fix.fix_day(DAY, archive_days=MID_ARCHIVE, **arch)
    got = hourly_values(arch)
    for h in range(1, 25):
        ref = DAY + timedelta(hours=h - 1)
        assert got[h][:2] == ('0-1', int(ref.strftime('%Y%m%d%H'))), h
        assert abs(got[h][2] - 1e-3 * hourly_mm(h)) < 1e-8, h


def test_a_crash_half_way_through_resumes_to_the_same_result(tmp_path, fix, monkeypatch):
    (tmp_path / 'a').mkdir(), (tmp_path / 'b').mkdir()
    clean = build_archive(tmp_path / 'a', fix)
    fix.fix_day(DAY, archive_days=MID_ARCHIVE, **clean)
    expected = hourly_values(clean)

    crashed = build_archive(tmp_path / 'b', fix)
    real, calls = fix.rewrite_hour, []

    def dies_on_the_sixth(*a, **k):
        calls.append(a)
        if len(calls) == 6:
            raise RuntimeError("node lost")
        return real(*a, **k)

    monkeypatch.setattr(fix, 'rewrite_hour', dies_on_the_sixth)
    with pytest.raises(RuntimeError):
        fix.fix_day(DAY, archive_days=MID_ARCHIVE, **crashed)
    monkeypatch.setattr(fix, 'rewrite_hour', real)
    fix.fix_day(DAY, archive_days=MID_ARCHIVE, **crashed)
    assert hourly_values(crashed) == expected


def test_running_twice_changes_nothing(tmp_path, fix):
    arch = build_archive(tmp_path, fix)
    fix.fix_day(DAY, archive_days=MID_ARCHIVE, **arch)
    files = sorted((tmp_path / 'grib').iterdir())
    before = {p: p.read_bytes() for p in files}
    fix.fix_day(DAY, archive_days=MID_ARCHIVE, **arch)
    assert {p: p.read_bytes() for p in files} == before


def test_at_the_start_of_a_block_00z_comes_from_two_native_snapshots(tmp_path, fix):
    import accum_hourly as ah
    import accum_ref
    arch = build_archive(tmp_path, fix)
    prev_run = datetime(2024, 6, 29, 18)          # the run for the day before DAY
    natives = lambda rain: {v: np.full((2, 3), rain if v == 'RAINNC' else 0.0, np.float32)  # noqa: E731
                            for v in accum_ref.ACCUMULATED_VARS}
    accum_ref.write_sidecar(ah.snapshot_path(arch['snap_dir'], ah.State(DAY, prev_run)),
                            natives(50.0), {})
    accum_ref.write_sidecar(ah.snapshot_path(arch['snap_dir'],
                                             ah.State(DAY - timedelta(hours=1), prev_run)),
                            natives(47.7), {})

    fix.fix_day(DAY, archive_days={DAY.date()}, **arch)   # the day before is not archived

    tp = read(arch['path_of'](DAY))[TP]
    assert (tp['dataDate'], tp['dataTime'], tp['stepRange']) == (20240630, 2300, '0-1')
    assert abs(tp['values'][0] - 0.0023) < 1e-6        # float32 natives: 50.0 - 47.7


def test_a_00z_that_cannot_be_computed_does_not_hold_back_the_rest_of_the_day(tmp_path, fix):
    # Found on real data: a block start with no native snapshot aborted the whole day.
    arch = build_archive(tmp_path, fix)
    problems = fix.fix_day(DAY, archive_days={DAY.date()}, **arch)   # no snapshots for DAY 00Z

    assert len(problems) == 1 and '2024-07-01T00' in problems[0]
    got = hourly_values(arch)
    for h in range(2, 25):
        assert got[h][0] == '0-1' and abs(got[h][2] - 1e-3 * hourly_mm(h)) < 1e-8, h
    assert read(arch['path_of'](DAY))[TP]['stepRange'] == '0'      # left as it was


def test_the_sanity_check_rejects_0h_and_accepts_the_hourly_encoding(tmp_path, fix):
    spec = importlib.util.spec_from_file_location("check_grib_sanity",
                                                  ROOT / "hpc" / "check_grib_sanity.py")
    sanity = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sanity)

    def verdicts(path):
        out = []
        with open(path, 'rb') as fh:
            while (gid := eccodes.codes_grib_new_from_file(fh)) is not None:
                out.append(sanity.accumulation_problem(gid))
                eccodes.codes_release(gid)
        return out

    valid = datetime(2024, 7, 2, 0)
    path = write_old(tmp_path / 'f.grib', valid, tp=[0.0] * 6)
    old = verdicts(path)
    assert old[0] is None and old[1] is not None          # skt untouched; 0-H tp rejected
    fix.rewrite_hour(path, valid, {TP: np.zeros(6)})
    assert verdicts(path) == [None, None]


def test_a_day_with_an_hour_missing_is_refused_before_anything_is_rewritten(tmp_path, fix):
    arch = build_archive(tmp_path, fix)
    arch['path_of'](DAY + timedelta(hours=15)).unlink()
    before = {p: p.read_bytes() for p in (tmp_path / 'grib').iterdir()}
    with pytest.raises(FileNotFoundError, match='2024-07-01T15'):
        fix.fix_day(DAY, archive_days=MID_ARCHIVE, **arch)
    assert {p: p.read_bytes() for p in (tmp_path / 'grib').iterdir()} == before


def test_a_00z_declared_unrecoverable_is_written_missing_and_the_day_completes(tmp_path, fix):
    arch = build_archive(tmp_path, fix)
    import accum_hourly as ah
    ah_snap = ah.snapshot_path(arch['snap_dir'], ah.State(DAY + timedelta(days=1), RUN))
    pathlib.Path(ah_snap).unlink()                        # the 24 h file is a 0-byte stub

    with pytest.raises(FileNotFoundError):                # by default: nothing is guessed
        fix.fix_day(DAY, archive_days=MID_ARCHIVE, **arch)
    # Declaring ANOTHER day lost changes nothing: the flag names days, not a mode.
    with pytest.raises(FileNotFoundError):
        fix.fix_day(DAY, archive_days=MID_ARCHIVE, lost_00z={DAY.date()}, **arch)
    problems = fix.fix_day(DAY, archive_days=MID_ARCHIVE,
                           lost_00z={(DAY + timedelta(days=1)).date()}, **arch)

    assert len(problems) == 1 and '2024-07-02T00' in problems[0]
    nxt = read(arch['path_of'](DAY + timedelta(days=1)))[TP]
    assert nxt['stepRange'] == '0-1' and np.all(nxt['values'] == 9999.0)   # bitmap, not zero
    got = hourly_values(arch)
    for h in range(2, 24):
        assert abs(got[h][2] - 1e-3 * hourly_mm(h)) < 1e-8, h


def test_release_keeps_a_state_whose_consumer_is_still_0h(tmp_path, fix):
    # A new block next to an old one: the 0-H GRIB of the next hour exists, but the
    # post-pass will still need this hour's state to make it hourly.
    import accum_hourly as ah
    snaps = tmp_path / 'snaps'
    grib_of = lambda v: str(tmp_path / f"{v:%Y%m%d%H}.grib")     # noqa: E731
    t23, t00 = datetime(2019, 2, 28, 23), datetime(2019, 3, 1, 0)
    snap = pathlib.Path(ah.snapshot_path(snaps, ah.archive_state(t23)))
    snap.parent.mkdir(parents=True)
    snap.write_bytes(b'x')
    write_old(grib_of(t23), t23, tp=[0.0] * 6)
    fix.rewrite_hour(grib_of(t23), t23, {TP: np.zeros(6)})        # 23Z: converted, hourly
    write_old(grib_of(t00), t00, tp=[0.0] * 6)                     # 00Z: the old 0-H file
    ah.release(t23, snaps, grib_of)
    assert snap.exists()
    fix.rewrite_hour(grib_of(t00), t00, {TP: np.zeros(6)})        # once 00Z is hourly too
    ah.release(t23, snaps, grib_of)
    assert not snap.exists()


# --- releasing snapshots (accum_hourly.release): needs real hourly GRIBs -----
import accum_hourly as ah  # noqa: E402


def _touch_snapshot(snaps, state):
    p = pathlib.Path(ah.snapshot_path(snaps, state))
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b'x')
    return p


def test_a_snapshot_goes_only_when_both_its_producer_and_its_consumer_are_converted(tmp_path, fix):
    snaps = tmp_path / 'snaps'
    grib_of = lambda v: str(tmp_path / f"{v:%Y%m%d%H}.grib")     # noqa: E731

    def converted(v):
        write_old(grib_of(v), v, tp=[0.0] * 6)
        fix.rewrite_hour(grib_of(v), v, {TP: np.zeros(6)})

    t4, t5, t6 = (datetime(2019, 2, 10, h) for h in (4, 5, 6))
    s4, s5 = (_touch_snapshot(snaps, ah.archive_state(v)) for v in (t4, t5))

    # 05Z finishes first: the state of 04Z is consumed, but 04Z itself is not
    # converted yet and its job still has to find its own snapshot.
    converted(t5)
    ah.release(t5, snaps, grib_of)
    assert s4.exists() and s5.exists()
    assert ah.wrfout_may_go(t5, snaps, grib_of)          # its own snapshot is there

    converted(t4)                                        # then 04Z: its state may go now
    ah.release(t4, snaps, grib_of)
    assert not s4.exists() and s5.exists()               # 05Z's state waits for 06Z

    converted(t6)
    ah.release(t6, snaps, grib_of)
    assert not s5.exists()
    s5_gone_but_consumed = ah.wrfout_may_go(t5, snaps, grib_of)
    assert s5_gone_but_consumed                          # 06Z has its GRIB: nothing needs 05Z


def test_the_24h_snapshot_goes_with_the_00z_that_consumed_it(tmp_path, fix):
    snaps = tmp_path / 'snaps'
    grib_of = lambda v: str(tmp_path / f"{v:%Y%m%d%H}.grib")     # noqa: E731
    v = datetime(2019, 2, 11, 0)
    curr, prev = ah.window(v)
    s24 = _touch_snapshot(snaps, curr)
    s23 = _touch_snapshot(snaps, prev)
    write_old(grib_of(v), v, tp=[0.0] * 6)
    fix.rewrite_hour(grib_of(v), v, {TP: np.zeros(6)})
    ah.release(v, snaps, grib_of)
    assert not s24.exists() and s23.exists()             # 23Z of the 10th not converted yet
    assert not ah.wrfout_may_go(v, snaps, grib_of)       # 00Z's own state was never saved
