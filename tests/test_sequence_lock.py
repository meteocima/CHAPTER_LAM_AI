"""One sequence at a time, and an adopted chain judged on its own run (#74).

On 2026-11-11 the 2019-2025 Cold Copy campaign was relaunched on login05 while the
sequence of 2026-11-09 was still alive on login02, frozen behind a `nas_push` in D state
(`ps | grep run_year` missed it: a sequence runs from its snapshot, `.rebuild_sequence_*.sh`).
Once unfrozen the two ran side by side for four days: two arrays wrote the same Cold Copy
days into the same `.partial` (`NetCDF: HDF error`, all of 2019-09), two sweeps raced
(`FileNotFoundError` on unlink), and a phase whose download chain one sequence had launched
was adopted by the other with offset 1, so the "Window complete" of an earlier run of the
same label in that driver log closed it at once: 2020-10's array ran on a month still
downloading, 31 days `CC_INCOMPLETE` twice, `CC_RETRY_EXHAUSTED`.

The lock is `flock` on `<logs>/rebuild_sequence.lock`, which holds across login nodes on
/leonardo_work (as the NAS copy's own lock does), held by the detached sequence for its
whole life and by nothing it launches: a download chain outliving a dead sequence must not
keep the next one from starting and adopting it.
"""
import fcntl
import os
import pathlib
import subprocess
import time

from test_sequence_chain_log import ROOT, SEQUENCE, chain_log_functions

PHASE = "t19x 2019-01-01 0 2019-01-01 0"


def run_sequence(work, **env):
    """Start the sequence on a scratch W with its stop flag present: once detached it
    logs START and leaves at its first phase, touching nothing outside `work`."""
    logs = work / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    (logs / "rebuild_sequence.stop").touch()
    e = dict(os.environ, W=str(work), PHASES_SPEC=PHASE, COLD_COPY="false",
             PROJECT_DIR=str(ROOT), **env)
    e.pop("SEQ_DETACHED", None)
    return subprocess.run(["bash", str(SEQUENCE)], env=e, capture_output=True, text=True,
                          timeout=60)


def wait_for(path, text, seconds=30):
    end = time.time() + seconds
    while time.time() < end:
        if path.exists() and text in path.read_text():
            return True
        time.sleep(0.2)
    return False


def test_a_second_sequence_is_refused_while_one_holds_the_lock(tmp_path):
    logs = tmp_path / "logs"
    logs.mkdir()
    with open(logs / "rebuild_sequence.lock", "a") as held:
        fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
        r = run_sequence(tmp_path)
        time.sleep(2)  # a sequence wrongly detached would have logged START by now
    assert r.returncode != 0, r.stdout + r.stderr
    assert "already running" in r.stdout + r.stderr
    assert not list(logs.glob(".rebuild_sequence_*.sh")), "it detached anyway"
    seq_log = logs / "rebuild_sequence.log"
    assert not (seq_log.exists() and "| START |" in seq_log.read_text())


def test_the_sequence_runs_and_lets_the_lock_go_when_it_ends(tmp_path):
    r = run_sequence(tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    seq_log = tmp_path / "logs" / "rebuild_sequence.log"
    assert wait_for(seq_log, "| STOPPED |"), seq_log.read_text() if seq_log.exists() else ""
    assert "| START |" in seq_log.read_text()
    deadline = time.time() + 10
    with open(tmp_path / "logs" / "rebuild_sequence.lock", "a") as lk:
        while True:
            try:
                fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                assert time.time() < deadline, "the lock outlived the sequence"
                time.sleep(0.2)


def test_what_the_sequence_launches_does_not_inherit_the_lock(tmp_path):
    """The detached body runs without the lock's descriptor: anything it starts
    (a download chain, the NAS copy) cannot hold it once the sequence is gone."""
    logs = tmp_path / "logs"
    logs.mkdir()
    probe = tmp_path / "fds"
    # The body's first line after the shebang-less start: list its open descriptors
    # onto the lock file. Run the detach path, then read what the body saw.
    r = run_sequence(tmp_path, SEQ_FD_PROBE=str(probe))
    assert r.returncode == 0, r.stdout + r.stderr
    assert wait_for(probe, "/", seconds=30), "the body never wrote its descriptors"
    held = [l for l in probe.read_text().splitlines() if l.endswith("rebuild_sequence.lock")]
    assert not held, f"the body (and so its children) holds the lock: {held}"


def adopt(log_text, tmp_path):
    """The offset launch_chain hands wait_chain for a chain it adopts, and whether the
    log from there says "Window complete"."""
    log = tmp_path / "driver.log"
    log.write_text(log_text)
    script = (chain_log_functions()
              + f'\noff=$(adopt_offset {log})\necho "$off"\n'
              + f'chain_log_says {log} "$off" "Window complete" && echo complete || echo running\n')
    out = subprocess.run(["bash", "-c", "set -uo pipefail\n" + script],
                         capture_output=True, text=True, check=True).stdout.split()
    return int(out[0]), out[1]


def test_an_adopted_chain_is_not_closed_by_an_earlier_run_of_its_label(tmp_path):
    earlier = ("  [2020-10-01T01] fetched.\n\nWindow complete (reached backward edge). "
               "Closing it, then no further respawn.\n")
    now = "Window: 2020-10-01T00..2020-10-31T23\n  [2020-10-15T01] fetch attempt 1/3 via datamover...\n"
    off, said = adopt(earlier + now, tmp_path)
    assert said == "running"
    assert off == len((earlier).encode()) + 1


def test_an_adopted_chain_with_a_fresh_log_is_read_from_the_start(tmp_path):
    off, said = adopt("Window: 2020-10-01T00..2020-10-31T23\n  [2020-10-31T23] fetched.\n", tmp_path)
    assert (off, said) == (1, "running")


def test_an_earlier_stop_is_not_this_run_stopping(tmp_path):
    earlier = "STOP flag present (/x/rebuild_r20_10_dl.stop); stopping.\n"
    now = "  [2020-10-15T01] fetch attempt 1/3 via datamover...\n"
    off, _ = adopt(earlier + now, tmp_path)
    assert off == len(earlier.encode()) + 1
