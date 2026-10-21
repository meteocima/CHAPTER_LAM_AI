"""Download-only re-entrancy across a converted hour (2026-10-21).

A download-only chain decided "done" by the staged wrfout alone. Relaunched over a
month whose hours were partly converted already (and their wrfout deleted by
convert_step.sh), it fetched every one of them again: the convert chain then skipped
them on the GRIB and never deleted them. Measured on the 2020-23 sequence after the
relay outage of 2026-10-19: ~1300 files, ~12 TB, ~12 h of relay for nothing.

The driver is run for real, in DRY_RUN over a two-hour window, and judged by the
ledger lines it prints -- the same thing `report=true` reads.
"""
import os
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRIVER = ROOT / "hpc" / "fetch_step.sh"
TEMPLATE = "ailam-an-cima-3km-{year}-{year}-1h-v1-{date_compact}{hour:02d}.grib"


def grib(tmp, d, h):
    name = TEMPLATE.replace("{year}", d[:4]).replace("{date_compact}", d.replace("-", ""))
    p = tmp / "grib" / d[:4] / d[5:7] / name.replace("{hour:02d}", h)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"GRIB")


def snapshot(tmp, d, h, run):
    p = tmp / "accum_snap" / d[:4] / d[5:7] / f"accum_{d.replace('-', '')}{h}_run{run}.npz"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"x")


def run_driver_tokens(tmp, start="2021-03-10T10", end="2021-03-10T11"):
    """Run a download-only dry chain over [start, end]; {timestep: [tokens]}."""
    env = dict(os.environ,
               DRY_RUN="1", DOWNLOAD_ONLY="1", DIRECTION="backward",
               START_DT=start, END_DT=end, CURRENT_DT=end,
               WRFOUT_DIR=str(tmp / "wrfout"), GRIB_DIR=str(tmp / "grib"),
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
    seen = {}
    for line in out.stdout.splitlines():
        if "[LOG]" in line:
            _, dt, tok, *_ = [f.strip() for f in line.split("|")]
            seen.setdefault(dt, []).append(tok)
    return seen


def test_converted_hour_is_not_fetched_again(tmp_path):
    # Both hours converted: nothing in the window needs a wrfout.
    grib(tmp_path, "2021-03-10", "10")
    grib(tmp_path, "2021-03-10", "11")
    seen = run_driver_tokens(tmp_path)
    assert seen["2021-03-10T11"] == ["SKIP_GRIB_EXISTS"]
    assert seen["2021-03-10T10"] == ["SKIP_GRIB_EXISTS"]


def test_converted_hour_still_fetched_when_the_next_one_needs_its_state(tmp_path):
    # 10Z converted and its snapshot released, 11Z not converted: the hour 10->11
    # is the difference against 10Z's state, so 10Z must be staged after all.
    grib(tmp_path, "2021-03-10", "10")
    seen = run_driver_tokens(tmp_path)
    assert "FETCH_OK" in seen["2021-03-10T10"]
    assert "FETCH_OK" in seen["2021-03-10T11"]


def test_converted_hour_skipped_when_its_state_is_saved(tmp_path):
    grib(tmp_path, "2021-03-10", "10")
    snapshot(tmp_path, "2021-03-10", "10", "2021030918")
    seen = run_driver_tokens(tmp_path)
    assert seen["2021-03-10T10"] == ["SKIP_GRIB_EXISTS"]
    assert "FETCH_OK" in seen["2021-03-10T11"]
