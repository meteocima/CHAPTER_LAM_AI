"""The two converter paths #72 added for 00Z, on synthetic GRIB2 files on a 3 x 2 grid.

`--missing-timestep` writes a 00Z whose 24 h file is verified lost: every message,
all missing, encoded exactly as a real timestep would be. `--accum-from-grib`
re-converts a 00Z from its 24 h file while copying the hourly accumulations of
the file it replaces, byte for byte.
"""
import eccodes  # not importorskip: a GRIB test that skips in silence is a test nobody runs
import numpy as np
import pandas as pd
import pytest

import accum_hourly as ah
import convert_to_pressure_levels as conv
from wrf_era5_comparison import EXPECTED_MESSAGES, WRF_TO_ECMWF_PARAMID

GRID = {'ni': 3, 'nj': 2, 'lat0': 40.0, 'lon0': 5.0, 'lat1': 40.05, 'lon1': 5.06,
        'truelat1': 44.67, 'dx': 3000.0, 'dy': 3000.0}
VALID = pd.Timestamp('2019-02-11 00:00')


def _messages(path):
    out = []
    with open(path, 'rb') as fh:
        while (gid := eccodes.codes_grib_new_from_file(fh)) is not None:
            try:
                out.append({k: eccodes.codes_get(gid, k) for k in
                            ('paramId', 'numberOfMissing', 'numberOfDataPoints',
                             'validityDate', 'validityTime')})
            finally:
                eccodes.codes_release(gid)
    return out


def test_a_lost_00z_is_every_message_missing_at_its_own_validity(tmp_path, monkeypatch):
    monkeypatch.setattr(conv.static_ref, 'load_static',
                        lambda d: ({}, {k: str(v) for k, v in GRID.items()}))
    out = tmp_path / 'lost.grib'
    conv.write_missing_timestep(str(out), VALID, 'unused')
    msgs = _messages(out)
    assert len(msgs) == EXPECTED_MESSAGES
    assert all(m['numberOfMissing'] == m['numberOfDataPoints'] == 6 for m in msgs)
    assert {(m['validityDate'], m['validityTime']) for m in msgs} == {(20190211, 0)}
    # The accumulations carry the hour ending at 00Z, so the archive's own test of an
    # hourly file accepts it, and the snapshots of the 23Z before it can be released.
    assert ah.is_hourly_grib(str(out), VALID.to_pydatetime())


def _accum_file(path, valid, value):
    """A GRIB holding only the accumulated fields of `valid`, each = `value`."""
    keys = [k for k, v in WRF_TO_ECMWF_PARAMID.items() if v.get('stepType') == 'accum']
    with open(path, 'wb') as fout:
        for key in keys:
            info = WRF_TO_ECMWF_PARAMID[key]
            conv.write_message(fout, np.full((2, 3), value), info, info['levels'][0], GRID, valid)
    return keys


def test_accumulations_are_copied_from_the_file_they_replace_byte_for_byte(tmp_path):
    old = tmp_path / 'old.grib'
    keys = _accum_file(old, VALID, 0.25)
    found = conv.accumulated_messages(str(old), VALID)
    assert sorted(found) == sorted(WRF_TO_ECMWF_PARAMID[k]['paramId'] for k in keys)
    with open(old, 'rb') as fh:
        assert b''.join(found[WRF_TO_ECMWF_PARAMID[k]['paramId']][1] for k in keys) == fh.read()
    values, _ = found[WRF_TO_ECMWF_PARAMID[keys[0]]['paramId']]
    assert np.allclose(values, 0.25)


def test_accumulations_of_another_timestep_are_refused(tmp_path):
    old = tmp_path / 'old.grib'
    _accum_file(old, VALID - pd.Timedelta(hours=1), 0.25)
    with pytest.raises(SystemExit, match='hourly accumulations'):
        conv.accumulated_messages(str(old), VALID)
