"""The Cold Copy's days, written from the wrfout this repo fetched for its GRIB (#73, ADR-0001).

From 2018 back each wrfout is fetched once and feeds both the archive and the Cold
Copy. The Cold Copy is written by CHAPTER_INHOUSE's Ingest, through its command
`cold-copy-day` (its #45), run from a clone pinned to a tag. This module is the one
place that knows this repo's staging layout, and hands the Ingest what it holds:

  holdings   the staged wrfout by run and lead, plus those declared lost
             (pipeline.lost_wrfouts), as the JSON list `cold-copy-day` reads
  write DAY  one day of the Cold Copy: a task of the per-phase SLURM array
  sweep      once the array is done: delete every wrfout the Ingest releases and,
             for an archived hour, whose GRIB is written and whose state is saved

A file's run and lead come from accum_hourly, never from a second copy of the rule:
the archived 00Z of D and the spin-up 00Z of D share a name, and only the directory
tells them apart (`<wrfout_dir>/<D>/` against `<wrfout_dir>_spinup/<run>/`).

Not here: deciding a wrfout is lost (a person does, after checking LRZ), and the
crossing to CIMA's NAS (CHAPTER_INHOUSE #38).
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import accum_hourly  # noqa: E402

_NAME = re.compile(r"^wrfout_d02_(\d{4}-\d{2}-\d{2})_(\d{2}):00:00$")
_RUN = "%Y%m%d%H"


def spinup_dir(wrfout_dir: Path) -> Path:
    """Where the driver keeps the spin-up 00Z of each run (fetch_step.sh, SPINUP_DIR)."""
    return Path(str(wrfout_dir).rstrip("/") + "_spinup")


def _lead(state) -> int:
    return int((state.valid - state.run).total_seconds() // 3600)


def _valid(name: str):
    m = _NAME.match(name)
    return datetime.strptime(f"{m[1]} {m[2]}", "%Y-%m-%d %H") if m else None


def staged(wrfout_dir: Path) -> dict[tuple[str, int], Path]:
    """Every staged wrfout, by (run, lead): the archived states under their valid date,
    the spin-up 00Z under its run."""
    found: dict[tuple[str, int], Path] = {}

    def add(state, path):
        key = (state.run.strftime(_RUN), _lead(state))
        if key in found:
            raise ValueError(f"{path} and {found[key]} are both run {key[0]} lead {key[1]}")
        found[key] = path

    for path in sorted(Path(wrfout_dir).glob("*/wrfout_d02_*")):
        valid = _valid(path.name)
        if valid is not None and path.parent.name == f"{valid:%Y-%m-%d}":
            add(accum_hourly.archive_state(valid), path)
    for path in sorted(spinup_dir(wrfout_dir).glob("*/wrfout_d02_*")):
        valid = _valid(path.name)
        if valid is None or valid.hour != 0:
            continue
        state = accum_hourly.spinup_state(valid)
        if path.parent.name != state.run.strftime(_RUN):
            raise ValueError(f"{path}: the spin-up 00Z of {valid:%Y-%m-%d} belongs to run "
                             f"{state.run:{_RUN}}, not {path.parent.name}")
        add(state, path)
    return found


def holdings(wrfout_dir: Path, lost: list[dict]) -> list[dict]:
    """What `cold-copy-day` reads: each staged wrfout, and each declared lost, by run and
    lead. A wrfout both staged and declared lost is a mistake in the declaration."""
    entries = [{"run": run, "lead": lead, "path": str(path)}
               for (run, lead), path in sorted(staged(wrfout_dir).items())]
    have = {(e["run"], e["lead"]) for e in entries}
    for item in lost:
        key = (str(item["run"]), int(item["lead"]))
        if key in have:
            raise ValueError(f"run {key[0]} lead {key[1]} is declared lost "
                             f"(pipeline.lost_wrfouts) but is staged")
        entries.append({"run": key[0], "lead": key[1],
                        "hole": {"kind": "lost", "reason": str(item["reason"])}})
    return entries


# What `cold-copy-day write` answers (CHAPTER_INHOUSE #45): the word it prints on
# success, its exit status otherwise.
_DONE = {"written": "CC_WRITTEN", "checked": "CC_CHECKED", "already": "CC_ALREADY"}
_INCOMPLETE, _WHOLLY_LOST = 3, 4


def log_status(status_log: Path, key: str, token: str, detail: str = "") -> None:
    """One ledger line, as fetch_step.sh writes them: `ts | key | TOKEN | detail`."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    status_log.parent.mkdir(parents=True, exist_ok=True)
    with open(status_log, "a") as f:
        f.write(f"{ts} | {key} | {token} | {detail}\n")


def _ingest_command() -> str:
    command = os.environ.get("COLD_COPY_DAY")
    if not command:
        raise ValueError("COLD_COPY_DAY is not set: the path of cold-copy-day in the pinned "
                         "CHAPTER_INHOUSE clone (set by hpc/run_year_rebuild.sh)")
    return command


def write(day: str, wrfout_dir: Path, out: Path, status_log: Path, lost: list[dict]) -> int:
    """One day of the Cold Copy, through `cold-copy-day write`; its outcome in the ledger.
    A day still missing wrfout, or lost whole, is not a failed task: the ledger says
    which, and the day stays to do. Anything else fails the task."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", prefix=f"holdings_{day}_") as f:
        json.dump(holdings(wrfout_dir, lost), f)
        f.flush()
        run = subprocess.run([_ingest_command(), "write", day, "--out", str(out),
                              "--holdings", f.name], capture_output=True, text=True)
    said = run.stdout.strip()
    why = run.stderr.strip().splitlines()[-1] if run.stderr.strip() else ""
    if run.returncode == 0 and said in _DONE:
        log_status(status_log, day, _DONE[said], str(out))
        return 0
    if run.returncode == _INCOMPLETE:
        log_status(status_log, day, "CC_INCOMPLETE", why)
        return 0
    if run.returncode == _WHOLLY_LOST:
        log_status(status_log, day, "CC_WHOLLY_LOST", why)
        return 0
    log_status(status_log, day, "CC_ERROR",
               f"cold-copy-day exited {run.returncode}: {why or said}")
    return 1


def _archive_may_drop(valid: datetime, snap_dir: Path, grib_pattern: str,
                      span: tuple[str, str]) -> bool:
    """The archive is done with an archived wrfout: its GRIB is written, unless its
    timestep lies outside the campaign (`span`) and no GRIB of it will ever be written
    here - the state before the first 00Z, fetched for its snapshot alone - and its state
    is saved, or no timestep still to convert reads it (accum_hourly.wrfout_may_go)."""
    grib_of = lambda v: v.strftime(grib_pattern)  # noqa: E731
    inside = span[0] <= f"{valid:%Y-%m-%d}" <= span[1]
    return (os.path.isfile(grib_of(valid)) or not inside) and \
        accum_hourly.wrfout_may_go(valid, str(snap_dir), grib_of)


def _spinup_may_drop(valid: datetime, snap_dir: Path, grib_pattern: str) -> bool:
    """The archive is done with a spin-up 00Z: its snapshot is saved, or 01Z, the one
    hour differenced against it, is converted (#72; fetch_step.sh, evict_spinup_00z)."""
    state = accum_hourly.spinup_state(valid)
    one = valid.replace(hour=1)
    return os.path.isfile(accum_hourly.snapshot_path(str(snap_dir), state)) or \
        os.path.isfile(one.strftime(grib_pattern))


def sweep(wrfout_dir: Path, out: Path, status_log: Path, grib_pattern: str, snap_dir: Path,
          lost: list[dict], span: tuple[str, str]) -> int:
    """Delete every staged wrfout the archive and the Cold Copy are done with: the Ingest
    releases it (`cold-copy-day released`: every Cold Copy day reading it within `span`, the
    campaign's first and last day, is delivered), and the archive no longer needs it.
    Only what this module handed over is ever deleted."""
    have = staged(wrfout_dir)
    with tempfile.NamedTemporaryFile("w", suffix=".json", prefix="holdings_sweep_") as f:
        json.dump(holdings(wrfout_dir, lost), f)
        f.flush()
        run = subprocess.run([_ingest_command(), "released", "--out", str(out),
                              "--holdings", f.name, "--span", *span],
                             capture_output=True, text=True)
    if run.returncode != 0:
        raise ValueError(f"cold-copy-day released exited {run.returncode}: "
                         f"{run.stderr.strip()}")
    released = {Path(line) for line in run.stdout.splitlines() if line.strip()}
    spinup = spinup_dir(wrfout_dir)
    for (run_init, lead), path in sorted(have.items(), key=lambda kv: str(kv[1])):
        if path not in released:
            continue
        valid = _valid(path.name)
        if path.parent.parent == spinup:
            done, what = _spinup_may_drop(valid, snap_dir, grib_pattern), "spin-up 00Z"
        else:
            done, what = _archive_may_drop(valid, snap_dir, grib_pattern, span), "archived"
        if not done:
            continue
        path.unlink()
        log_status(status_log, f"{valid:%Y-%m-%dT%H}", "CC_WRFOUT_DELETED",
                   f"{what}, run {run_init} lead {lead}: {path}")
    return 0


def _load_lost(path: Path) -> list[dict]:
    return json.loads(Path(path).read_text()) if path else []


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="cold_copy_day.py",
                                     description=__doc__.splitlines()[0])
    verbs = parser.add_subparsers(dest="verb", required=True)
    held = verbs.add_parser("holdings")
    held.add_argument("--wrfout-dir", required=True, type=Path)
    held.add_argument("--lost", type=Path, help="JSON list of pipeline.lost_wrfouts")
    one = verbs.add_parser("write")
    one.add_argument("day")
    one.add_argument("--wrfout-dir", required=True, type=Path)
    one.add_argument("--out", required=True, type=Path, help="the Cold Copy's directory")
    one.add_argument("--status-log", required=True, type=Path)
    one.add_argument("--lost", type=Path, help="JSON list of pipeline.lost_wrfouts")
    free = verbs.add_parser("sweep")
    free.add_argument("--wrfout-dir", required=True, type=Path)
    free.add_argument("--out", required=True, type=Path, help="the Cold Copy's directory")
    free.add_argument("--status-log", required=True, type=Path)
    free.add_argument("--grib-pattern", required=True,
                      help="the GRIB path of any hour, as a strftime pattern")
    free.add_argument("--snap-dir", required=True, type=Path)
    free.add_argument("--lost", type=Path, help="JSON list of pipeline.lost_wrfouts")
    free.add_argument("--span", nargs=2, required=True, metavar=("FIRST", "LAST"),
                      help="the campaign's first and last day: the days it delivers")
    args = parser.parse_args(argv)
    try:
        if args.verb == "holdings":
            json.dump(holdings(args.wrfout_dir, _load_lost(args.lost)), sys.stdout, indent=1)
            print()
            return 0
        if args.verb == "write":
            return write(args.day, args.wrfout_dir, args.out, args.status_log,
                         _load_lost(args.lost))
        if args.verb == "sweep":
            return sweep(args.wrfout_dir, args.out, args.status_log, args.grib_pattern,
                         args.snap_dir, _load_lost(args.lost), tuple(args.span))
    except ValueError as e:
        print(f"cold_copy_day.py: {e}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
