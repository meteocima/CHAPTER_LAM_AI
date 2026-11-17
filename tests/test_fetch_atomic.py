"""A wrfout killed mid-transfer is never taken for a whole one (2026-11-17, #74).

sftp wrote straight into the final name. On 2026-11-14 23:01Z, while two sequences ran
side by side, six transfers stopped at once and left 7.4-8.2 GB of the 9.14 GB wrfout
under their final names. Every later pass took them for staged files: the driver's
guard was "at least MIN_BYTES" (1 GiB) and its NetCDF check opens only the header,
which a truncated classic file keeps. Read past the cut, a NETCDF3 file gives zeros
without an error, so 17 of the 19 accumulators of 2020-09-10T23 read 0, and the Cold
Copy's 2020-09-11, which subtracts that state from its 00Z, was delivered with a whole
run's accumulation in one hour.

`fetch_wrfout` is taken from the driver as it is and run for real, with an `ssh` on PATH
that plays the datamover's sftp: it writes the file into the directory it is given and
either ends, or writes the head of the file and kills the whole process group, as the
login node did.
"""
import os
import pathlib
import subprocess

import netCDF4
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRIVER = ROOT / "hpc" / "fetch_step.sh"
NAME = "wrfout_d02_2020-09-10_23:00:00"
REMOTE = f"/b/2020090918/{NAME}"

FAKE_SSH = r"""#!/bin/bash
# ssh -nxT <host> "sftp [-i key] <opts> <relay>:<remote> <localdir>/"
cmd="${@: -1}"
dir="${cmd##* }"; remote="${cmd% *}"; remote="${remote##* }"; remote="${remote#*:}"
dest="${dir%/}/$(basename "$remote")"
if [ "$FAKE_SFTP" = "die" ]; then
    head -c "$FAKE_PART" "$FAKE_SOURCE" > "$dest"
    # timeout gives its child a process group of its own: the whole session goes, as on
    # 2026-11-14, driver included.
    pkill -9 -s "$(ps -o sid= -p $$ | tr -d ' ')"
fi
cp "$FAKE_SOURCE" "$dest"
"""


def functions(*names):
    text = DRIVER.read_text().splitlines()
    out = []
    for name in names:
        start = text.index(f"{name}() {{")
        end = start + text[start:].index("}")
        out += text[start:end + 1]
    return "\n".join(out)


def a_wrfout(path):
    """A NETCDF3 file shaped like a wrfout: a header, then a record of fields."""
    with netCDF4.Dataset(path, "w", format="NETCDF3_64BIT_OFFSET") as d:
        d.createDimension("Time", None)
        d.createDimension("y", 200)
        d.createDimension("x", 200)
        for name in ("T2", "RAINNC", "ACSWDNB", "XLAT_U"):
            v = d.createVariable(name, "f4", ("Time", "y", "x"))
            v[0] = np.full((200, 200), 7.0, dtype="f4")
    return path


def fetch(tmp, mode):
    """Run fetch_wrfout once for 2020-09-10T23; its exit code."""
    bin_dir = tmp / "bin"
    bin_dir.mkdir(exist_ok=True)
    (bin_dir / "ssh").write_text(FAKE_SSH)
    (bin_dir / "ssh").chmod(0o755)
    source = tmp / "source.nc"
    if not source.exists():
        a_wrfout(source)
    script = "\n".join([
        "set -uo pipefail",
        f'DRY_RUN=0 MIN_BYTES=1000 FETCH_RETRIES=0 FETCH_TIMEOUT=60',
        f'DATAMOVER_HOST=dm.invalid REMOTE_HOST=relay.invalid IDENTITY_FILE= SFTP_OPTS=',
        f'WRFOUT_DIR={tmp}/wrfout STATUS_LOG={tmp}/status.log PROJECT_DIR={ROOT}',
        functions("log_status", "fetch_cmd", "fetch_wrfout"),
        f'fetch_wrfout 2020-09-10 23 {REMOTE}',
    ])
    env = dict(os.environ, PATH=f"{bin_dir}:{os.environ['PATH']}", FAKE_SFTP=mode,
               FAKE_SOURCE=str(source), FAKE_PART=str(source.stat().st_size // 2))
    r = subprocess.run(["bash", "-c", script], env=env, capture_output=True, text=True,
                       timeout=120, start_new_session=True)
    return r.returncode


def staged(tmp):
    return tmp / "wrfout" / "2020-09-10" / NAME


def test_a_transfer_killed_midway_leaves_nothing_under_the_final_name(tmp_path):
    assert fetch(tmp_path, "die") != 0
    assert not staged(tmp_path).exists(), f"{staged(tmp_path).stat().st_size} B left as if staged"


def test_the_next_pass_fetches_it_again_whole(tmp_path):
    fetch(tmp_path, "die")
    assert fetch(tmp_path, "ok") == 0
    assert staged(tmp_path).stat().st_size == (tmp_path / "source.nc").stat().st_size
    with netCDF4.Dataset(staged(tmp_path)) as d:
        assert float(d["XLAT_U"][0].min()) == 7.0
