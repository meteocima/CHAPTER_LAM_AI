"""Hourly accumulations (issue #70).

Every accumulated field covers the hour ending at its validity time, from two
states of the SAME run. The expected values below come from the files
themselves, not from re-deriving the rule: on 2026-10-07 the 24 h file of run
2019020918 was fetched and read back, START_DATE 2019-02-09_18, Times
2019-02-11_00, and the archived 00Z of 2019-02-11 carries START_DATE
2019-02-10_18 -- a different run, which is why the 00Z hour cannot come from it.
"""
from datetime import datetime

import accum_hourly as ah


def test_00z_hour_comes_from_the_previous_days_run_24h_file():
    curr, prev = ah.window(datetime(2019, 2, 11, 0))
    assert ah.source_file(curr) == ('2019020918', 'wrfout_d02_2019-02-11_00:00:00')
    assert ah.source_file(prev) == ('2019020918', 'wrfout_d02_2019-02-10_23:00:00')


def test_hours_01_to_23_stay_in_the_run_the_archive_was_fetched_from():
    # The driver fetched 2019-02-02T04 from .../2019020118/ (ledger of r19_02).
    curr, prev = ah.window(datetime(2019, 2, 2, 5))
    assert ah.source_file(prev) == ('2019020118', 'wrfout_d02_2019-02-02_04:00:00')
    assert ah.source_file(curr) == ('2019020118', 'wrfout_d02_2019-02-02_05:00:00')
    # 01Z reaches back to the archived 00Z of the same day, same run.
    curr, prev = ah.window(datetime(2019, 2, 2, 1))
    assert ah.source_file(prev) == ('2019020118', 'wrfout_d02_2019-02-02_00:00:00')


def _deltas(**over):
    """One-point native hourly increments: zero unless given."""
    import numpy as np
    from accum_ref import ACCUMULATED_VARS
    return {v: np.array([float(over.get(v, 0.0))]) for v in ACCUMULATED_VARS}


def test_every_accumulated_registry_field_is_published():
    from wrf_era5_comparison import WRF_TO_ECMWF_PARAMID
    accum = {k for k, v in WRF_TO_ECMWF_PARAMID.items() if v.get('stepType') == 'accum'}
    assert len(accum) == 19
    assert set(ah.published(_deltas())) == accum


def test_published_values_follow_the_ecmwf_definitions():
    # 2 mm of precipitation, of which 0.5 mm snow and 0.25 mm graupel.
    out = ah.published(_deltas(RAINNC=2.0, SNOWNC=0.5, GRAUPELNC=0.25,
                               SFROFF=0.3, UDROFF=0.1,
                               ACSWDNB=1000.0, ACSWUPB=150.0, ACLWUPT=900.0))
    assert out['RAINNC'][0] == 0.002            # tp, m
    assert out['SNOWNC'][0] == 0.00075          # sf: snow AND graupel, m (#52)
    assert out['tirf'][0] == 1.25               # rain only, kg/m^2
    assert abs(out['ro'][0] - 0.0004) < 1e-15   # surface + sub-surface, m
    assert out['SFROFF'][0] == 0.0003
    assert out['ACSWDNB'][0] == 1000.0          # ssrd, J/m^2
    assert out['ssr'][0] == 850.0               # down - up
    assert out['ttr'][0] == -900.0              # no downward LW at the top


def test_negative_noise_is_clipped_except_on_net_radiation():
    out = ah.published(_deltas(RAINNC=-1e-7, ACLWDNB=100.0, ACLWUPB=400.0))
    assert out['RAINNC'][0] == 0.0
    assert out['str'][0] == -300.0              # net longwave is legitimately negative


def _fake_wrfout(path, start, times, scale=0.0):
    """A wrfout with only what identifies the state: run start and valid time."""
    import netCDF4
    import numpy as np
    with netCDF4.Dataset(path, 'w') as ds:
        ds.createDimension('Time', 1)
        ds.createDimension('DateStrLen', 19)
        ds.createDimension('south_north', 2)
        ds.createDimension('west_east', 3)
        ds.START_DATE = start
        ds.SIMULATION_START_DATE = start
        t = ds.createVariable('Times', 'S1', ('Time', 'DateStrLen'))
        t[0, :] = np.array(list(times), 'S1')
        for i, v in enumerate(__import__('accum_ref').ACCUMULATED_VARS):
            ds.createVariable(v, 'f4', ('Time', 'south_north', 'west_east'))[0] = i + scale
    return path


def test_the_state_is_read_from_the_file_so_the_wrong_run_is_refused(tmp_path):
    # The two files named wrfout_d02_2019-02-11_00:00:00 that exist on the relay.
    own = _fake_wrfout(tmp_path / 'a.nc', '2019-02-09_18:00:00', '2019-02-11_00:00:00')
    nxt = _fake_wrfout(tmp_path / 'b.nc', '2019-02-10_18:00:00', '2019-02-11_00:00:00')
    curr, _ = ah.window(datetime(2019, 2, 11, 0))
    assert ah.state_of(own) == curr
    assert ah.state_of(nxt) != curr


def test_a_snapshot_is_found_again_by_its_state_and_only_by_it(tmp_path):
    import pytest
    w = _fake_wrfout(tmp_path / 'a.nc', '2019-02-09_18:00:00', '2019-02-11_00:00:00')
    snaps = tmp_path / 'snaps'
    state = ah.write_snapshot(w, snaps)
    fields = ah.load_snapshot(snaps, state)
    assert fields['RAINNC'].shape == (2, 3) and fields['RAINNC'][0, 0] == 0.0
    assert fields['ACLWUPTC'][1, 2] == 18.0     # the last of the 19 natives
    other_run = ah.State(state.valid, datetime(2019, 2, 10, 18))
    with pytest.raises(FileNotFoundError):
        ah.load_snapshot(snaps, other_run)


def test_an_hour_is_the_input_minus_the_previous_state_of_the_same_run(tmp_path):
    snaps = tmp_path / 'snaps'
    prev = _fake_wrfout(tmp_path / 'w04', '2019-02-01_18:00:00', '2019-02-02_04:00:00', 10.0)
    ah.write_snapshot(prev, snaps)
    inp = _fake_wrfout(tmp_path / 'w05', '2019-02-01_18:00:00', '2019-02-02_05:00:00', 12.5)
    inc = ah.increments(inp, snaps)
    assert inc['RAINNC'][0, 0] == 2.5 and inc['ACLWUPTC'][1, 2] == 2.5


def test_a_missing_snapshot_is_made_from_the_wrfout_next_to_the_input(tmp_path):
    # The pipeline layout: <wrfout_dir>/<date>/wrfout_d02_<date>_<HH>:00:00
    d = tmp_path / '2019-02-02'
    d.mkdir()
    _fake_wrfout(d / 'wrfout_d02_2019-02-02_04:00:00', '2019-02-01_18:00:00', '2019-02-02_04:00:00', 10.0)
    inp = _fake_wrfout(d / 'wrfout_d02_2019-02-02_05:00:00', '2019-02-01_18:00:00',
                       '2019-02-02_05:00:00', 11.0)
    assert ah.increments(inp, tmp_path / 'snaps')['RAINNC'][0, 0] == 1.0


def test_00z_ignores_the_input_and_takes_two_states_of_the_previous_days_run(tmp_path):
    import pytest
    snaps = tmp_path / 'snaps'
    # The archived 00Z (run for 02-11): 6 h of spin-up, useless for the hour.
    inp = _fake_wrfout(tmp_path / 'in', '2019-02-10_18:00:00', '2019-02-11_00:00:00', 3.0)
    with pytest.raises(FileNotFoundError, match='2019020918'):
        ah.increments(inp, snaps)
    ah.write_snapshot(_fake_wrfout(tmp_path / 'a', '2019-02-09_18:00:00',
                                   '2019-02-11_00:00:00', 40.0), snaps)
    ah.write_snapshot(_fake_wrfout(tmp_path / 'b', '2019-02-09_18:00:00',
                                   '2019-02-10_23:00:00', 39.0), snaps)
    assert ah.increments(inp, snaps)['RAINNC'][0, 0] == 1.0


def test_the_snapshots_an_hour_consumes():
    curr, prev = ah.window(datetime(2019, 2, 11, 0))
    assert ah.consumed(datetime(2019, 2, 11, 0)) == [curr, prev]       # 24 h file and 23Z
    assert ah.consumed(datetime(2019, 2, 11, 5)) == [ah.window(datetime(2019, 2, 11, 5))[1]]


# ---------------------------------------------------------------------------
# The driver is bash and cannot import accum_hourly, so it computes the same
# states and snapshot paths a second time. This extracts its functions and
# insists the two agree -- the bridge test_ledger.py builds for the tokens.
# ---------------------------------------------------------------------------
import pathlib  # noqa: E402
import subprocess  # noqa: E402

DRIVER = pathlib.Path(__file__).resolve().parent.parent / "hpc" / "fetch_step.sh"
BEGIN = "# --- hourly states (extracted by tests/test_accum_hourly.py; keep the markers) ---"
END = "# --- end hourly states ---"

# 00Z and ordinary hours; a month, a year and the 2023 relay-base boundary.
CASES = [datetime(2019, 2, 11, 0), datetime(2019, 2, 11, 1), datetime(2019, 2, 2, 5),
         datetime(2019, 3, 1, 0), datetime(2024, 1, 1, 0), datetime(2024, 2, 29, 23),
         datetime(2023, 1, 1, 0), datetime(2023, 1, 1, 13)]


def bash(fn, *args):
    text = DRIVER.read_text()
    assert BEGIN in text and END in text, "the hourly-state markers are gone from hpc/fetch_step.sh"
    src = text.split(BEGIN, 1)[1].split(END, 1)[0]
    out = subprocess.run(['bash', '-c', f"set -euo pipefail\nINIT_HOUR=18\nACCUM_SNAP_DIR=/S\n{src}\n"
                          f"{fn} {' '.join(args)}"], capture_output=True, text=True, check=True)
    return out.stdout.split()


def test_the_driver_names_the_snapshots_an_hour_needs_as_accum_hourly_does():
    for v in CASES:
        d, h = f"{v:%Y-%m-%d}", f"{v:%H}"
        curr, prev = ah.window(v)
        want = [prev] if v.hour else [curr, prev]
        assert bash('window_snaps', d, h) == [ah.snapshot_path('/S', s) for s in want], v


def test_the_driver_names_an_archived_files_own_snapshot_as_accum_hourly_does():
    for v in CASES:
        d, h = f"{v:%Y-%m-%d}", f"{v:%H}"
        assert bash('own_snap', d, h) == [ah.snapshot_path('/S', ah.archive_state(v))], v


def test_a_lost_24h_file_gives_no_increments_only_when_declared_lost(tmp_path):
    import pytest
    snaps = tmp_path / 'snaps'
    inp = _fake_wrfout(tmp_path / 'in', '2019-02-10_18:00:00', '2019-02-11_00:00:00', 3.0)
    ah.write_snapshot(_fake_wrfout(tmp_path / 'b', '2019-02-09_18:00:00',
                                   '2019-02-10_23:00:00', 39.0), snaps)
    with pytest.raises(FileNotFoundError):                    # by default nothing is guessed
        ah.increments(inp, snaps)
    assert ah.increments(inp, snaps, dayend_lost=True) is None   # the hour is missing


def test_declaring_the_24h_file_lost_does_not_excuse_a_23z_still_in_transit(tmp_path):
    import pytest
    snaps = tmp_path / 'snaps'
    inp = _fake_wrfout(tmp_path / 'in', '2019-02-10_18:00:00', '2019-02-11_00:00:00', 3.0)
    ah.write_snapshot(_fake_wrfout(tmp_path / 'a', '2019-02-09_18:00:00',
                                   '2019-02-11_00:00:00', 40.0), snaps)
    with pytest.raises(FileNotFoundError, match='2019-02-10T23'):
        ah.increments(inp, snaps, dayend_lost=True)
