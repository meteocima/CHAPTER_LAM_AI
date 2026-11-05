"""The sequence writes a failed Cold Copy day once more, and only once its array is over (#73).

On 2026-11-04 run_year_rebuild.sh took April's array for gone from the queue while
its 30 tasks were running (`squeue -h -j` came back empty, once), and every day of
the month looked failed: their last ledger token was the CC_INCOMPLETE the relay
outage of 2026-11-03 had left. A second array wrote the same days beside the first,
each pair spoiling the other's .partial files ("Permission denied", "No such file"),
and the whole month ended CC_RETRY_EXHAUSTED.

Two functions decide it now, extracted from between their markers and run here as the
sequence runs them: cc_array_done (sacct, every task in a final state; a failed query
is not an answer, it is "unknown") and cc_failed_days (only what was written since the
array was submitted counts, and a day with no outcome since -- its task killed before
writing any -- counts as failed).
"""
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEQUENCE = ROOT / "hpc" / "run_year_rebuild.sh"
BEGIN = "# --- cold copy retry (extracted by tests/test_cold_copy_retry.py; keep the markers) ---"
END = "# --- end cold copy retry ---"


def retry_functions():
    text = SEQUENCE.read_text()
    assert BEGIN in text and END in text, "the cold-copy-retry markers are gone from run_year_rebuild.sh"
    return text[text.index(BEGIN):text.index(END)]


def run(tmp_path, call, env=None):
    """`call` in bash under the sequence's options, with the retry functions defined."""
    script = f"set -uo pipefail\nPATH={tmp_path / 'bin'}:$PATH\n{retry_functions()}\n{call}"
    out = subprocess.run(["bash", "-c", script], capture_output=True, text=True, timeout=60,
                         env={"PATH": "/usr/bin:/bin", **(env or {})})
    return out


def fake_sacct(tmp_path, states, status=0):
    """A sacct that prints one task state per line (as `-n -X -P -o State` does), or fails."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    body = "".join(f"echo '{s}'\n" for s in states)
    (bin_dir / "sacct").write_text(f"#!/bin/bash\n{body}exit {status}\n")
    (bin_dir / "sacct").chmod(0o755)


def done(tmp_path, states, status=0):
    fake_sacct(tmp_path, states, status)
    out = run(tmp_path, "cc_array_done 63524714; echo $?").stdout.strip()
    return {"0": "done", "1": "running", "2": "unknown"}[out]


def test_an_array_with_a_task_still_running_is_not_done(tmp_path):
    assert done(tmp_path, ["COMPLETED", "RUNNING", "PENDING"]) == "running"


def test_an_array_whose_tasks_all_ended_is_done(tmp_path):
    assert done(tmp_path, ["COMPLETED", "FAILED", "CANCELLED by 0", "OUT_OF_MEMORY",
                           "TIMEOUT", "NODE_FAIL", "REVOKED", "SPECIAL_EXIT"]) == "done"


def test_a_failed_or_empty_answer_is_unknown_not_done(tmp_path):
    # What happened to April: the query answered nothing, and nothing is not "gone". Unknown
    # is its own answer, so the sequence can give up on an array no query ever sees again.
    assert done(tmp_path, [], status=1) == "unknown"
    assert done(tmp_path, []) == "unknown"


def ledger_and_checksums(tmp_path, lines, delivered=()):
    """The Cold Copy ledger with `lines` (ts, day, token), and checksum files for `delivered`."""
    log = tmp_path / "cold_copy_status.log"
    log.write_text("".join(f"{ts} | {day} | {tok} | detail\n" for ts, day, tok in lines))
    sums = tmp_path / "cold_copy" / "_checksums"
    sums.mkdir(parents=True)
    for day in delivered:
        (sums / f"{day}.sha256").write_text("x\n")
    return {"CC_STATUS_LOG": str(log), "COLD_COPY_DIR": str(tmp_path / "cold_copy")}


def failed(tmp_path, env, since="2026-11-04T17:10:58Z"):
    out = run(tmp_path, f"cc_failed_days 2018-04-01 2018-04-05 {since}", env)
    assert out.returncode == 0, out.stderr
    return out.stdout.strip()


def test_a_token_from_before_the_array_does_not_decide_its_day(tmp_path):
    # The relay outage's CC_INCOMPLETE of 2026-11-03, left in the ledger, says nothing of
    # the array of 2026-11-04: 2018-04-02 was lost whole in this one, by decision, and is
    # not written again; 2018-04-03 was written.
    env = ledger_and_checksums(tmp_path, [
        ("2026-11-03T09:58:25Z", "2018-04-02", "CC_INCOMPLETE"),
        ("2026-11-04T19:00:00Z", "2018-04-02", "CC_WHOLLY_LOST"),
        ("2026-11-03T09:58:25Z", "2018-04-03", "CC_INCOMPLETE"),
        ("2026-11-04T19:00:00Z", "2018-04-03", "CC_CHECKED"),
    ], delivered=["2018-04-01", "2018-04-04", "2018-04-05"])
    assert failed(tmp_path, env) == ""


def test_a_day_whose_task_left_nothing_since_the_array_is_written_again(tmp_path):
    # A task SLURM killed before it wrote a token (TIMEOUT, NODE_FAIL, scancel): only the
    # stale token of 2026-11-03 is there, and the day must not be dropped in silence.
    env = ledger_and_checksums(tmp_path, [
        ("2026-11-03T09:58:25Z", "2018-04-02", "CC_INCOMPLETE"),
    ], delivered=["2018-04-01", "2018-04-03", "2018-04-04", "2018-04-05"])
    assert failed(tmp_path, env) == "1"


def test_a_day_that_failed_in_this_array_is_written_again(tmp_path):
    # Indices are days from the first: 2018-04-02 is task 1, 2018-04-05 task 4.
    env = ledger_and_checksums(tmp_path, [
        ("2026-11-03T09:58:25Z", "2018-04-02", "CC_INCOMPLETE"),
        ("2026-11-04T19:14:01Z", "2018-04-02", "CC_ERROR"),
        ("2026-11-04T21:00:00Z", "2018-04-05", "CC_INCOMPLETE"),
        ("2026-11-04T21:30:00Z", "2018-04-03", "CC_WRITTEN"),
    ], delivered=["2018-04-01", "2018-04-03", "2018-04-04"])
    assert failed(tmp_path, env) == "1,4"


def test_a_delivered_day_is_never_written_again(tmp_path):
    # 2018-04-02 failed once in this array and was delivered by a later task: its
    # checksum file is the truth, whatever the ledger said before.
    env = ledger_and_checksums(tmp_path, [("2026-11-04T19:14:01Z", "2018-04-02", "CC_ERROR")],
                               delivered=["2018-04-01", "2018-04-02", "2018-04-03",
                                          "2018-04-04", "2018-04-05"])
    assert failed(tmp_path, env) == ""
