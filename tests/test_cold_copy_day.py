"""The Cold Copy's days, written beside the GRIB from the same wrfout (#73, ADR-0001).

`hpc/cold_copy_day.py` is the one module that knows this repo's staging layout and
hands the Ingest of CHAPTER_INHOUSE (`cold-copy-day`, its #45) what it holds. The
Ingest itself is tested there; here it is a fake that answers with the exit status a
test asks for, and the module is judged by what it hands over, what it logs and what
it deletes.
"""
import json
import os
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODULE = ROOT / "hpc" / "cold_copy_day.py"


def touch(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"wrfout")
    return path


def staging(tmp):
    """A staging tree as the driver leaves it: archived states under their valid
    date, the spin-up 00Z under its run (fetch_step.sh, raw_path and ensure_spinup)."""
    wrfout, spinup = tmp / "wrfout_rebuild", tmp / "wrfout_rebuild_spinup"
    files = {
        "00Z of 02-01, archived": touch(wrfout / "2018-02-01" / "wrfout_d02_2018-02-01_00:00:00"),
        "01Z of 02-01": touch(wrfout / "2018-02-01" / "wrfout_d02_2018-02-01_01:00:00"),
        "23Z of 02-01": touch(wrfout / "2018-02-01" / "wrfout_d02_2018-02-01_23:00:00"),
        "23Z of 01-31": touch(wrfout / "2018-01-31" / "wrfout_d02_2018-01-31_23:00:00"),
        "00Z of 02-01, spin-up": touch(spinup / "2018013118" / "wrfout_d02_2018-02-01_00:00:00"),
    }
    return wrfout, spinup, files


def holdings_of(tmp, lost=()):
    wrfout, spinup, _ = staging(tmp)
    conf = tmp / "lost.json"
    conf.write_text(json.dumps(list(lost)))
    out = subprocess.run([sys.executable, str(MODULE), "holdings", "--wrfout-dir", str(wrfout),
                          "--lost", str(conf)], capture_output=True, text=True, cwd=ROOT)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_each_staged_wrfout_is_named_by_its_run_and_lead(tmp_path):
    # By ADR-0028 and #72, written out by hand: the archived 00Z of 2018-02-01 is lead
    # 30 of the run for 01-31 (init 2018013018), the spin-up 00Z beside it lead 6 of
    # the run for 02-01 (init 2018013118). Their file names are identical.
    _, _, files = staging(tmp_path)
    got = {(e["run"], e["lead"]): e["path"] for e in holdings_of(tmp_path)}
    assert got == {
        ("2018013018", 30): str(files["00Z of 02-01, archived"]),
        ("2018013118", 7): str(files["01Z of 02-01"]),
        ("2018013118", 29): str(files["23Z of 02-01"]),
        ("2018013018", 29): str(files["23Z of 01-31"]),
        ("2018013118", 6): str(files["00Z of 02-01, spin-up"]),
    }


def test_a_wrfout_declared_lost_is_handed_over_as_a_hole_with_its_reason(tmp_path):
    lost = {"run": "2018013118", "lead": 12, "reason": "absent on LRZ, ticket 1234"}
    entries = holdings_of(tmp_path, lost=[lost])
    assert {"run": "2018013118", "lead": 12,
            "hole": {"kind": "lost", "reason": "absent on LRZ, ticket 1234"}} in entries


def test_a_wrfout_declared_lost_that_is_staged_is_refused(tmp_path):
    # The declaration is a person's word after checking LRZ: if the file is here, the
    # word is wrong, and writing the day with a Hole would throw the file away.
    wrfout, _, _ = staging(tmp_path)
    conf = tmp_path / "lost.json"
    conf.write_text(json.dumps([{"run": "2018013118", "lead": 7, "reason": "x"}]))
    out = subprocess.run([sys.executable, str(MODULE), "holdings", "--wrfout-dir", str(wrfout),
                          "--lost", str(conf)], capture_output=True, text=True, cwd=ROOT)
    assert out.returncode == 1
    assert "run 2018013118 lead 7 is declared lost" in out.stderr


# cold-copy-day as a test wants it: records what it was handed, answers with the
# exit status and the word FAKE_STATUS and FAKE_SAYS give it.
FAKE = """#!/bin/bash
echo "$@" > "$FAKE_RECORD.args"
while [ $# -gt 0 ]; do [ "$1" = --holdings ] && cp "$2" "$FAKE_RECORD.holdings"; shift; done
[ -n "${FAKE_SAYS:-}" ] && echo "$FAKE_SAYS"
[ "${FAKE_STATUS:-0}" = 0 ] || echo "cold-copy-day: fake failure" >&2
exit "${FAKE_STATUS:-0}"
"""


def fake_ingest(tmp):
    path = tmp / "cold-copy-day"
    path.write_text(FAKE)
    path.chmod(0o755)
    return path


def write_day(tmp, day="2018-02-01", status=0, says="written"):
    """The array task for `day`, against the fake; (exit status, ledger lines, record)."""
    wrfout, _, _ = staging(tmp)
    record = tmp / "record"
    env = dict(os.environ, COLD_COPY_DAY=str(fake_ingest(tmp)), FAKE_RECORD=str(record),
               FAKE_STATUS=str(status), FAKE_SAYS=says)
    ledger = tmp / "logs" / "cold_copy_status.log"
    out = subprocess.run([sys.executable, str(MODULE), "write", day, "--wrfout-dir", str(wrfout),
                          "--out", str(tmp / "cold_copy"), "--status-log", str(ledger)],
                         capture_output=True, text=True, cwd=ROOT, env=env)
    lines = [[f.strip() for f in ln.split("|")] for ln in ledger.read_text().splitlines()] \
        if ledger.exists() else []
    return out.returncode, lines, record


def test_a_day_is_handed_the_staged_wrfout_and_written_into_the_cold_copy(tmp_path):
    status, lines, record = write_day(tmp_path)
    assert status == 0
    assert record.with_suffix(".args").read_text().split()[:4] == \
        ["write", "2018-02-01", "--out", str(tmp_path / "cold_copy")]
    handed = json.loads(record.with_suffix(".holdings").read_text())
    assert ("2018013118", 6) in {(e["run"], e["lead"]) for e in handed}
    assert [(ln[1], ln[2]) for ln in lines] == [("2018-02-01", "CC_WRITTEN")]


@pytest.mark.parametrize("status, says, token, task_status", [
    # done: the day has its checksum file now, or had it already
    (0, "checked", "CC_CHECKED", 0),
    (0, "already", "CC_ALREADY", 0),
    # waiting, not failing: the array task succeeds, the day stays to do
    (3, "", "CC_INCOMPLETE", 0),
    # every wrfout of the day declared lost: nothing to write, by decision
    (4, "", "CC_WHOLLY_LOST", 0),
    # anything else is for a person: the task fails, so sacct shows it too
    (1, "", "CC_ERROR", 1),
])
def test_each_answer_of_the_ingest_is_one_ledger_token(tmp_path, status, says, token,
                                                       task_status):
    got, lines, _ = write_day(tmp_path, status=status, says=says)
    assert got == task_status
    assert [(ln[1], ln[2]) for ln in lines] == [("2018-02-01", token)]


GRIB_PATTERN = "grib/%Y/%m/chapter_%Y%m%d%H.grib"


def grib(tmp, stamp):
    """The GRIB of the hour `stamp` (YYYYMMDDHH), written."""
    path = tmp / "grib" / stamp[:4] / stamp[4:6] / f"chapter_{stamp}.grib"
    return touch(path)


def snapshot(tmp, valid, run):
    """The accumulator snapshot of state (valid, run), as accum_hourly.snapshot_path lays
    it out: accum_snap/YYYY/MM/accum_<valid>_run<run>.npz."""
    return touch(tmp / "accum_snap" / valid[:4] / valid[4:6] / f"accum_{valid}_run{run}.npz")


def sweep(tmp, released, span=("2018-01-01", "2018-12-31"), extra=()):
    """The sweep after an array, the Ingest releasing `released`; the ledger lines."""
    wrfout, _, _ = staging(tmp)
    env = dict(os.environ, COLD_COPY_DAY=str(fake_ingest(tmp)), FAKE_RECORD=str(tmp / "rec"),
               FAKE_SAYS="\n".join(str(p) for p in released))
    ledger = tmp / "logs" / "cold_copy_status.log"
    out = subprocess.run([sys.executable, str(MODULE), "sweep", "--wrfout-dir", str(wrfout),
                          "--out", str(tmp / "cold_copy"), "--status-log", str(ledger),
                          "--grib-pattern", str(tmp / GRIB_PATTERN),
                          "--snap-dir", str(tmp / "accum_snap"), "--span", *span, *extra],
                         capture_output=True, text=True, cwd=ROOT, env=env)
    assert out.returncode == 0, out.stderr
    lines = [[f.strip() for f in ln.split("|")] for ln in ledger.read_text().splitlines()] \
        if ledger.exists() else []
    return lines


def test_a_released_wrfout_whose_grib_is_written_and_state_saved_is_deleted(tmp_path):
    _, _, files = staging(tmp_path)
    grib(tmp_path, "2018020101")
    snapshot(tmp_path, "2018020101", "2018013118")
    lines = sweep(tmp_path, [files["01Z of 02-01"]])
    assert not files["01Z of 02-01"].exists()
    assert [(ln[1], ln[2]) for ln in lines] == [("2018-02-01T01", "CC_WRFOUT_DELETED")]


def test_a_released_wrfout_whose_grib_is_not_written_is_kept(tmp_path):
    # Released by the Cold Copy, not by the archive: its convert has yet to run.
    _, _, files = staging(tmp_path)
    snapshot(tmp_path, "2018020101", "2018013118")
    assert sweep(tmp_path, [files["01Z of 02-01"]]) == []
    assert files["01Z of 02-01"].exists()


def test_a_released_wrfout_whose_state_the_next_hour_still_needs_is_kept(tmp_path):
    # GRIB written, but no snapshot of its state and 02Z not converted: 02Z's
    # accumulations are differenced against this file (#71).
    _, _, files = staging(tmp_path)
    grib(tmp_path, "2018020101")
    assert sweep(tmp_path, [files["01Z of 02-01"]]) == []
    assert files["01Z of 02-01"].exists()


def test_a_released_spinup_00z_whose_snapshot_is_saved_is_deleted(tmp_path):
    # The spin-up 00Z has no GRIB of its own; the archive needs it only as the state
    # 01Z is differenced against, which its snapshot holds.
    _, _, files = staging(tmp_path)
    snapshot(tmp_path, "2018020100", "2018013118")
    lines = sweep(tmp_path, [files["00Z of 02-01, spin-up"]])
    assert not files["00Z of 02-01, spin-up"].exists()
    assert [(ln[1], ln[2]) for ln in lines] == [("2018-02-01T00", "CC_WRFOUT_DELETED")]


def test_a_released_path_that_is_not_a_staged_wrfout_is_never_deleted(tmp_path):
    # Whatever the Ingest answers, the sweep deletes only what it handed over.
    staging(tmp_path)
    stranger = touch(tmp_path / "elsewhere" / "wrfout_d02_2018-02-01_05:00:00")
    grib(tmp_path, "2018020105")
    snapshot(tmp_path, "2018020105", "2018013118")
    assert sweep(tmp_path, [stranger]) == []
    assert stranger.exists()


def test_the_sweep_asks_the_ingest_only_for_the_days_of_the_campaign(tmp_path):
    # The state before the campaign's first 00Z is read by the day before too, which no
    # one here will write: the Ingest waits only for the days the campaign delivers.
    sweep(tmp_path, [], span=("2018-01-01", "2018-12-31"))
    args = (tmp_path / "rec.args").read_text().split()
    assert args[0] == "released"
    assert args[args.index("--span") + 1:args.index("--span") + 3] == ["2018-01-01", "2018-12-31"]


def test_a_released_state_before_the_campaign_needs_only_its_snapshot(tmp_path):
    # 23Z of 01-31 lies before a campaign starting 02-01: no GRIB of it will ever be
    # written here, and the archive needed it only as the start of 02-01T00.
    _, _, files = staging(tmp_path)
    snapshot(tmp_path, "2018013123", "2018013018")
    lines = sweep(tmp_path, [files["23Z of 01-31"]], span=("2018-02-01", "2018-02-28"))
    assert not files["23Z of 01-31"].exists()
    assert [(ln[1], ln[2]) for ln in lines] == [("2018-01-31T23", "CC_WRFOUT_DELETED")]


def test_a_released_state_before_the_campaign_without_its_snapshot_is_kept(tmp_path):
    _, _, files = staging(tmp_path)
    assert sweep(tmp_path, [files["23Z of 01-31"]], span=("2018-02-01", "2018-02-28")) == []
    assert files["23Z of 01-31"].exists()


def lost_from(tmp, yaml_text):
    """`cold_copy_day.py lost` on a pipeline configuration; (exit status, stdout, stderr)."""
    conf = tmp / "pipeline.yaml"
    conf.write_text(yaml_text)
    out = subprocess.run([sys.executable, str(MODULE), "lost", "--conf", str(conf)],
                         capture_output=True, text=True, cwd=ROOT)
    return out.returncode, out.stdout, out.stderr


def test_an_empty_lost_list_is_read_as_no_wrfout_lost(tmp_path):
    # What stopped the first launch of the trial (0f87a6b): OmegaConf's empty list is
    # falsy, and `or []` turned it into a list its own to_container refuses.
    status, out, err = lost_from(tmp_path, "pipeline:\n  lost_wrfouts: []\n")
    assert status == 0, err
    assert json.loads(out) == []


def test_a_configuration_without_lost_wrfouts_declares_none(tmp_path):
    # Configurations from before #73 have no such key: nothing is lost by default.
    status, out, err = lost_from(tmp_path, "pipeline:\n  missing_00z_days: []\n")
    assert status == 0, err
    assert json.loads(out) == []


def test_each_declared_wrfout_is_handed_on_with_its_run_lead_and_reason(tmp_path):
    status, out, err = lost_from(tmp_path, """pipeline:
  lost_wrfouts:
    - {run: "2018031018", lead: 30, reason: "ASSENTE on LRZ, ticket 1234"}
    - {run: "2018031118", lead: 12, reason: "0 bytes after recall"}
""")
    assert status == 0, err
    assert json.loads(out) == [
        {"run": "2018031018", "lead": 30, "reason": "ASSENTE on LRZ, ticket 1234"},
        {"run": "2018031118", "lead": 12, "reason": "0 bytes after recall"},
    ]


@pytest.mark.parametrize("entry, missing", [
    ('{run: "2018031018", lead: 30}', "reason"),
    ('{run: "2018031018", reason: "x"}', "lead"),
    ('{lead: 30, reason: "x"}', "run"),
])
def test_a_declaration_missing_its_run_lead_or_reason_is_refused(tmp_path, entry, missing):
    # A Hole carries its reason into the day file for whoever reads it (ADR-0028 of
    # CHAPTER_INHOUSE); one without run or lead names no wrfout at all. Refused here, at
    # the start of the sequence, not in the middle of a month's array.
    status, _, err = lost_from(tmp_path, f"pipeline:\n  lost_wrfouts:\n    - {entry}\n")
    assert status == 1
    assert f"no {missing}" in err


@pytest.mark.parametrize("entry, says", [
    ('{run: "2018031018", lead: 30, reason: null}', "reason"),
    ('{run: "2018031018", lead: 30, reason: ""}', "reason"),
    ('{run: "2018031018", lead: "30h", reason: "x"}', "lead"),
    ('{run: "2018031018", lead: 31, reason: "x"}', "lead"),
    ('{run: "2018031018", lead: 5, reason: "x"}', "lead"),
    ('{run: "2018-03-10T18", lead: 30, reason: "x"}', "run"),
    ('{run: "2018031012", lead: 30, reason: "x"}', "run"),
    ('"2018031018 30 x"', "not a mapping"),
    ('2018031018', "not a mapping"),
])
def test_a_declaration_whose_values_name_no_wrfout_or_give_no_reason_is_refused(
        tmp_path, entry, says):
    # A run is initialised at 18Z (YYYYMMDD18) and gives leads 6 to 30 to the Cold Copy
    # (ADR-0028 of CHAPTER_INHOUSE); anything else names no wrfout either side reads, and
    # would fail inside a month's array, or match nothing and be ignored in silence.
    status, _, err = lost_from(tmp_path, f"pipeline:\n  lost_wrfouts:\n    - {entry}\n")
    assert status == 1, err
    assert says in err
    assert "Traceback" not in err


def test_a_wrfout_declared_twice_is_refused(tmp_path):
    status, _, err = lost_from(tmp_path, """pipeline:
  lost_wrfouts:
    - {run: "2018031018", lead: 30, reason: "x"}
    - {run: "2018031018", lead: 30, reason: "y"}
""")
    assert status == 1
    assert "twice" in err


def test_with_on_nas_the_sweep_waits_for_the_days_to_be_on_the_nas(tmp_path):
    # With the Cold Copy, a wrfout goes only once the days reading it are on CIMA's NAS
    # (#73, 2026-11-02): the Ingest is asked for exactly that.
    ledger = tmp_path / "nas_push"
    sweep(tmp_path, [], extra=("--on-nas", str(ledger)))
    args = (tmp_path / "rec.args").read_text().split()
    assert args[0] == "released"
    assert args[args.index("--on-nas") + 1] == str(ledger)


def test_without_on_nas_the_sweep_asks_for_delivered_days_as_before(tmp_path):
    sweep(tmp_path, [])
    assert "--on-nas" not in (tmp_path / "rec.args").read_text().split()
