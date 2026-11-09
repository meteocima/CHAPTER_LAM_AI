"""What run_year_rebuild.sh does with a phase whose GRIB are all written (#74).

From 2019 on the archive is done and the sequence runs for the Cold Copy alone: a phase
with no GRIB missing gets no convert chain, and a campaign that converted nothing
submits no sanity job (grilling of 2026-11-08, Q7 and Q8). The phases of YEARS stop at
CHAPTER's last day, 2025-07-02, at 23Z (Q6); its 24 h file, 07-03T00, is the record's last hour,
converted apart.

Both functions are extracted from between their markers and run as the sequence runs
them.
"""
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEQUENCE = ROOT / "hpc" / "run_year_rebuild.sh"
BEGIN = "# --- phases (extracted by tests/test_sequence_phases.py; keep the markers) ---"
END = "# --- end phases ---"
TEMPLATE = "ailam-an-cima-3km-%Y-%Y-1h-v1-%Y%m%d%H.grib"


def run(call, env=None):
    text = SEQUENCE.read_text()
    assert BEGIN in text and END in text, "the phases markers are gone from run_year_rebuild.sh"
    script = f"set -uo pipefail\n{text[text.index(BEGIN):text.index(END)]}\n{call}"
    out = subprocess.run(["bash", "-c", script], capture_output=True, text=True, timeout=120,
                         env={"PATH": "/usr/bin:/bin", **(env or {})})
    assert out.returncode == 0, out.stderr
    return out.stdout.splitlines()


def test_a_year_is_one_phase_per_month():
    phases = run("year_phases 2019")
    assert len(phases) == 12
    assert phases[0].split() == ["r19_01", "2019-01-01", "0", "2019-01-31", "23"]
    assert phases[1].split() == ["r19_02", "2019-02-01", "0", "2019-02-28", "23"]


def test_2025_stops_at_chapter_last_hour():
    phases = run("year_phases 2025")
    assert [p.split()[0] for p in phases] == [f"r25_0{m}" for m in range(1, 8)]
    assert phases[-1].split() == ["r25_07", "2025-07-01", "0", "2025-07-02", "23"]


def grib(tmp, stamp):
    p = tmp / "grib_v3" / stamp[:4] / stamp[4:6] / \
        f"ailam-an-cima-3km-{stamp[:4]}-{stamp[:4]}-1h-v1-{stamp}.grib"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"GRIB")


def missing(tmp, *window):
    return int(run(f"phase_missing_gribs {' '.join(window)}",
                   env={"GRIB_PATTERN": str(tmp / "grib_v3/%Y/%m" / TEMPLATE)})[0])


def test_a_phase_with_every_grib_written_misses_none(tmp_path):
    for h in range(24):
        grib(tmp_path, f"20190201{h:02d}")
    assert missing(tmp_path, "2019-02-01", "0", "2019-02-01", "23") == 0


def test_a_phase_counts_each_hour_without_its_grib(tmp_path):
    for h in range(22):
        grib(tmp_path, f"20190201{h:02d}")
    assert missing(tmp_path, "2019-02-01", "0", "2019-02-01", "23") == 2
