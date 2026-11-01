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


def run_driver(tmp, start, end, cold_copy, download_only=True):
    """A dry chain over [start, end], as run_year_rebuild.sh launches a phase's two
    (download, then convert); its stdout."""
    env = dict(os.environ,
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
