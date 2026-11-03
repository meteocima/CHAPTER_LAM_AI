"""The sequence reads its chains' driver logs right under `set -o pipefail` (#73).

On 2026-11-02 the 2018 campaign stopped at its first month: r18_01's download chain
printed "Window complete" and ended, but run_year_rebuild.sh's wait_chain never saw
it and declared the chain dead an hour later. Its check was `tail -c +N log | grep -q`
under `set -o pipefail`: grep -q exits at the first match, tail is killed by SIGPIPE
(141) while writing the rest, and pipefail makes the whole test false. It bites when
the log is past a pipe's 64 KB and lines follow the match -- as they do with
COLD_COPY=1, where the state before the window is fetched after "Window complete".
Measured on the real log (237 680 bytes): 48 misses in 50, and on copies of it cut to
other sizes anything from 0 to 16 in 20. What decides is not the size but whether tail's
last write() comes after grep has read the match and left: tail splits the log into
writes as its reads from Lustre fall (st_blksize 4 MiB there, 4 KiB on /scratch_local,
where the same log was read right every time), so it happens or not with the file.
Never with nothing after the match. `producer | grep -q` under pipefail is wrong whenever
anything can follow the match.

The check is the sequence's chain_log_says, extracted from between its markers and
run here under pipefail, as the sequence runs it.
"""
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEQUENCE = ROOT / "hpc" / "run_year_rebuild.sh"
BEGIN = "# --- chain log (extracted by tests/test_sequence_chain_log.py; keep the markers) ---"
END = "# --- end chain log ---"


def chain_log_functions():
    text = SEQUENCE.read_text()
    assert BEGIN in text and END in text, "the chain-log markers are gone from run_year_rebuild.sh"
    return text[text.index(BEGIN):text.index(END)]


def a_month_of_driver_log(tmp_path):
    """A driver log as r18_01's was: ~300 KB of fetch lines, "Window complete", then the
    lines of the state before the window fetched after it."""
    log = tmp_path / "driver.log"
    fetches = "".join(f"  [2018-01-{d:02d}T{h:02d}] fetched (download-only: no convert, "
                      f"wrfout kept).\n" for d in range(31, 0, -1) for h in range(23, -1, -1))
    log.write_text(fetches * 4 + "\nWindow complete (reached backward edge). Closing it, "
                   "then no further respawn.\n"
                   + "  [2017-12-31T23] state before the window: fetching it.\n" * 20)
    assert log.stat().st_size > 2 * 65536
    return log


# Fault injection: a tail whose write after the match comes once grep -q may have left,
# what GNU tail does on Lustre for some sizes and not others; here every time, so the
# test does not depend on the filesystem or on the size of the log.
LATE_TAIL = """#!/usr/bin/env python3
import os, sys, time
start = int(sys.argv[2].lstrip("+")) - 1
data = open(sys.argv[3], "rb").read()[start:]
cut = data.find(b"Window complete")
cut = len(data) if cut < 0 else data.index(b"\\n", cut) + 1
try:
    os.write(1, data[:cut])
    time.sleep(0.05)
    os.write(1, data[cut:])
except BrokenPipeError:
    sys.exit(141)
"""


def says(log, text, times=50):
    """How many of `times` runs of chain_log_says find `text` in `log`, under pipefail,
    with tail's last write after the match (LATE_TAIL)."""
    shim = log.parent / "bin"
    shim.mkdir(exist_ok=True)
    (shim / "tail").write_text(LATE_TAIL)
    (shim / "tail").chmod(0o755)
    script = (f"set -uo pipefail\nPATH={shim}:$PATH\n{chain_log_functions()}\n"
              f"n=0; for i in $(seq {times}); do chain_log_says \"$1\" 1 \"$2\" && n=$((n+1)); done; "
              f"echo $n")
    out = subprocess.run(["bash", "-c", script, "_", str(log), text], capture_output=True,
                         text=True, timeout=120)
    assert out.returncode == 0, out.stderr
    return int(out.stdout.strip())


def test_a_log_with_lines_after_the_match_is_read_right_every_time(tmp_path):
    assert says(a_month_of_driver_log(tmp_path), "Window complete", times=20) == 20


def test_a_line_that_is_not_there_is_not_found(tmp_path):
    assert says(a_month_of_driver_log(tmp_path), "STOP flag present", times=5) == 0
