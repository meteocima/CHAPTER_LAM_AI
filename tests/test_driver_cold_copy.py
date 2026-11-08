"""The driver with COLD_COPY=1 keeps what the Cold Copy reads (#73, ADR-0001).

Two files the archive needs only for their snapshot are deleted right after it: the
spin-up 00Z of each day (the state 01Z is differenced against, #72) and the state
before the window's oldest hour. The Cold Copy reads both - the spin-up 00Z is lead
6 of the day's run, the start of its 01Z; the state before a month's first 00Z is
lead 29 of the previous run, the start of that 00Z (ADR-0028 of CHAPTER_INHOUSE) -
so with COLD_COPY=1 they stay, and the second is fetched even when its snapshot is
already there. The driver runs for real, in DRY_RUN, and is judged by what it prints.
"""
import os
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRIVER = ROOT / "hpc" / "fetch_step.sh"
TEMPLATE = "ailam-an-cima-3km-{year}-{year}-1h-v1-{date_compact}{hour:02d}.grib"


def snapshot(tmp, d, h, run):
    p = tmp / "accum_snap" / d[:4] / d[5:7] / f"accum_{d.replace('-', '')}{h}_run{run}.npz"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"x")


# The Ingest itself, from the clone the campaigns run (hpc/run_year_rebuild.sh): which days
# read a wrfout is its rule, and the driver is judged on applying it, not on a fake's word.
# Missing, these tests fail rather than skip, as the GRIB tests do without eccodes.
INGEST = pathlib.Path("/leonardo_work/AIFPT_AILAMIT/CHAPTER/cold_copy_src/cold_copy/.venv/bin/cold-copy-day")


def grib(tmp, d, h):
    name = TEMPLATE.replace("{year}", d[:4]).replace("{date_compact}", d.replace("-", ""))
    p = tmp / "grib" / d[:4] / d[5:7] / name.replace("{hour:02d}", h)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"GRIB")


def delivered(tmp, day):
    """The day's checksum file, as cold-copy-day writes it once the day is read back whole."""
    p = tmp / "cold_copy" / "_checksums" / f"{day}.sha256"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"x  chapter_cc_surface_{day.replace('-', '')}.nc\n")


def run_driver(tmp, start, end, cold_copy, download_only=True, **extra):
    """A dry chain over [start, end], as run_year_rebuild.sh launches a phase's two
    (download, then convert); its stdout."""
    assert INGEST.is_file(), f"the pinned Ingest is missing: {INGEST}"
    env = dict(os.environ, COLD_COPY_DAY=str(INGEST),
               DRY_RUN="1", DOWNLOAD_ONLY="1" if download_only else "0", DIRECTION="backward",
               COLD_COPY="1" if cold_copy else "0", COLD_COPY_DIR=str(tmp / "cold_copy"),
               START_DT=start, END_DT=end, CURRENT_DT=end,
               WRFOUT_DIR=str(tmp / "wrfout_rebuild"), GRIB_DIR=str(tmp / "grib"),
               GRIB_TEMPLATE=TEMPLATE, ACCUM_SNAP_DIR=str(tmp / "accum_snap"),
               PROJECT_DIR=str(ROOT), LOG_DIR=str(tmp / "logs"),
               STOP_FLAG=str(tmp / "logs" / "stop"),
               DATAMOVER_HOST="dm.invalid", REMOTE_HOST="relay.invalid",
               BASE_2023="/b23", BASE_PRE2023="/b", INIT_HOUR="18",
               DRIVER_SCRIPT=str(DRIVER), CONVERT_SCRIPT="/bin/false",
               CONVERT_PARTITION="p", CONVERT_WALLTIME="1", CONVERT_MEM="1G",
               BATCH_SIZE="24", FETCH_PARALLEL="1")
    env.update(extra)
    out = subprocess.run(["bash", str(DRIVER)], env=env, capture_output=True,
                         text=True, timeout=120)
    assert out.returncode == 0, out.stdout + out.stderr
    return out.stdout


SPINUP = "wrfout_rebuild_spinup/2018013118/wrfout_d02_2018-02-01_00:00:00"
EDGE = "wrfout_d02_2018-01-31_23:00:00"


def test_without_cold_copy_the_spinup_00z_goes_after_its_snapshot(tmp_path):
    # Today's behaviour, which the Cold Copy must not get.
    out = run_driver(tmp_path, "2018-02-01T01", "2018-02-01T01", cold_copy=False)
    assert f"[DRY] rm {tmp_path / SPINUP}" in out


def test_with_cold_copy_the_spinup_00z_is_kept_after_its_snapshot(tmp_path):
    out = run_driver(tmp_path, "2018-02-01T01", "2018-02-01T01", cold_copy=True)
    assert f"[DRY] snapshot {tmp_path / SPINUP}" in out
    assert "[DRY] rm" not in out
    assert f"[COLD_COPY] keeping {tmp_path / SPINUP}" in out


def test_without_cold_copy_a_saved_edge_state_is_not_fetched(tmp_path):
    # The state before the window's 00Z is saved already: the archive needs nothing more.
    snapshot(tmp_path, "2018-01-31", "23", "2018013018")
    out = run_driver(tmp_path, "2018-02-01T00", "2018-02-01T00", cold_copy=False)
    assert EDGE not in out


def test_with_cold_copy_a_saved_edge_state_is_fetched_and_kept(tmp_path):
    # Cold Copy 2018-02-01 reads 23Z of 01-31 as the start of its 00Z: one fetch, kept
    # for the sweep after the next array, not a second fetch later.
    snapshot(tmp_path, "2018-01-31", "23", "2018013018")
    out = run_driver(tmp_path, "2018-02-01T00", "2018-02-01T00", cold_copy=True)
    edge = tmp_path / "wrfout_rebuild" / "2018-01-31" / EDGE
    assert f"/2018013018/{EDGE}" in out                       # fetched from its run folder
    assert f"[COLD_COPY] keeping {edge}" in out
    assert "[DRY] rm" not in out


def test_the_convert_chain_never_fetches_the_edge_state_for_the_cold_copy(tmp_path):
    # The convert chain sees local files only (run_year_rebuild.sh): if the edge is gone,
    # the sweep deleted it once its days were delivered, and fetching it again would
    # spend the relay on a file nobody reads.
    snapshot(tmp_path, "2018-01-31", "23", "2018013018")
    out = run_driver(tmp_path, "2018-02-01T00", "2018-02-01T00", cold_copy=True,
                     download_only=False)
    assert EDGE not in out


def test_a_relaunched_download_chain_does_not_fetch_an_edge_its_day_no_longer_needs(tmp_path):
    # 2018-02-01 is delivered (its checksum file is there): the edge was read and swept.
    snapshot(tmp_path, "2018-01-31", "23", "2018013018")
    sums = tmp_path / "cold_copy" / "_checksums" / "2018-02-01.sha256"
    sums.parent.mkdir(parents=True)
    sums.write_text("x  chapter_cc_surface_20180201.nc\n")
    out = run_driver(tmp_path, "2018-02-01T00", "2018-02-01T00", cold_copy=True)
    assert EDGE not in out


def tokens(out):
    """{timestep: [ledger tokens]} of a dry run's stdout."""
    seen = {}
    for line in out.splitlines():
        if "[LOG]" in line:
            _, dt, tok, *_ = [f.strip() for f in line.split("|")]
            seen.setdefault(dt, []).append(tok)
    return seen


def all_gribs(tmp, first_day, last_day):
    import datetime as dtm
    d = dtm.date.fromisoformat(first_day)
    while d <= dtm.date.fromisoformat(last_day):
        for h in range(24):
            grib(tmp, d.isoformat(), f"{h:02d}")
        d += dtm.timedelta(days=1)


# --- 2019-2025: every GRIB written, the Cold Copy still to write (#74 generalised) ---

def test_with_every_grib_written_the_cold_copy_still_fetches_what_its_days_read(tmp_path):
    # 2019: the archive is done, no day of the Cold Copy is. The window's hours, the
    # spin-up 00Z of its day and the state before it are all fetched -- and none is
    # snapshotted, since no convert will ever read the snapshot.
    all_gribs(tmp_path, "2019-01-31", "2019-02-01")
    out = run_driver(tmp_path, "2019-02-01T00", "2019-02-01T02", cold_copy=True,
                     COLD_COPY_SPAN="2019-01-01 2019-12-31")
    seen = tokens(out)
    for h in ("00", "01", "02"):
        assert "FETCH_OK" in seen[f"2019-02-01T{h}"]
    assert "/2019013118/wrfout_d02_2019-02-01_00:00:00" in out      # the spin-up 00Z
    assert "/2019013018/wrfout_d02_2019-01-31_23:00:00" in out      # the state before
    assert "[DRY] snapshot" not in out
    assert "[DRY] rm" not in out


def test_an_hour_whose_reading_days_are_all_delivered_is_skipped(tmp_path):
    all_gribs(tmp_path, "2019-02-01", "2019-02-01")
    delivered(tmp_path, "2019-02-01")
    out = run_driver(tmp_path, "2019-02-01T10", "2019-02-01T10", cold_copy=True,
                     COLD_COPY_SPAN="2019-01-01 2019-12-31")
    assert tokens(out)["2019-02-01T10"] == ["SKIP_CC_DELIVERED"]
    assert "[DRY] ssh" not in out


def test_the_last_23z_of_a_month_is_fetched_while_the_next_month_first_day_waits(tmp_path):
    # #74 at a month boundary: 01-31 is delivered and both hours have their GRIB, but
    # 23Z of 01-31 is also the start of 02-01's 00Z, and 02-01 is not delivered. 22Z is
    # read by 01-31 alone.
    all_gribs(tmp_path, "2019-01-31", "2019-01-31")
    delivered(tmp_path, "2019-01-31")
    out = run_driver(tmp_path, "2019-01-31T22", "2019-01-31T23", cold_copy=True,
                     COLD_COPY_SPAN="2019-01-01 2019-12-31")
    seen = tokens(out)
    assert "FETCH_OK" in seen["2019-01-31T23"]
    assert seen["2019-01-31T22"] == ["SKIP_CC_DELIVERED"]


def test_the_trial_edge_of_74_is_fetched_again_for_the_day_after_the_trial(tmp_path):
    # The case of #74 itself: the trial t18a/t18b delivered 01-30..02-02 and swept 23Z of
    # 02-02; the February chain must fetch it again for 02-03, GRIB or no GRIB.
    all_gribs(tmp_path, "2018-02-02", "2018-02-02")
    for day in ("2018-01-30", "2018-01-31", "2018-02-01", "2018-02-02"):
        delivered(tmp_path, day)
    out = run_driver(tmp_path, "2018-02-02T23", "2018-02-02T23", cold_copy=True,
                     COLD_COPY_SPAN="2018-01-01 2018-12-31")
    assert "FETCH_OK" in tokens(out)["2018-02-02T23"]


def test_when_the_ingest_cannot_answer_every_hour_not_local_is_fetched(tmp_path):
    # Never a guess: 9 GB too many rather than a day that cannot be written.
    all_gribs(tmp_path, "2019-02-01", "2019-02-01")
    delivered(tmp_path, "2019-02-01")
    out = run_driver(tmp_path, "2019-02-01T10", "2019-02-01T10", cold_copy=True,
                     COLD_COPY_DAY="/bin/false")
    seen = tokens(out)
    assert any("CC_WANTED_FAILED" in toks for toks in seen.values())
    assert "FETCH_OK" in seen["2019-02-01T10"]


def test_without_cold_copy_an_hour_with_its_grib_is_still_skipped_on_it(tmp_path):
    all_gribs(tmp_path, "2019-02-01", "2019-02-01")
    out = run_driver(tmp_path, "2019-02-01T10", "2019-02-01T10", cold_copy=False)
    assert tokens(out)["2019-02-01T10"] == ["SKIP_GRIB_EXISTS"]


def test_the_record_last_hour_is_fetched_without_a_snapshot_nobody_would_release(tmp_path):
    # 2025-07-03T00 never exists: a snapshot of 07-02T23 for it would stay for ever.
    all_gribs(tmp_path, "2025-07-02", "2025-07-02")
    out = run_driver(tmp_path, "2025-07-02T23", "2025-07-02T23", cold_copy=True,
                     COLD_COPY_SPAN="2025-01-01 2025-07-02")
    assert "FETCH_OK" in tokens(out)["2025-07-02T23"]
    assert "[DRY] snapshot" not in out
