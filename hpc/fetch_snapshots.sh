#!/bin/bash
# Fetch individual wrfout states from the LRZ relay and keep only their
# accumulator snapshot (accum_hourly.py): fetch -> snapshot -> delete the wrfout.
#
# What it is for (issue #70): the hour 23Z(D-1) -> 00Z(D) exists only in the 24 h
# file of the run for D-1, which the step pipeline never fetches, and at the start
# of a converted block also that run's 23Z. Neither is a timestep of the archive,
# so this script does not touch the archive's wrfout tree, ledger or GRIBs.
#
# LOGIN NODE ONLY: the datamover is reachable from the regular login nodes and not
# from lrd_all_serial. The transfer runs on the datamover, so this process and its
# ssh sit at ~0 s CPU; each snapshot is its own python process (~11 s CPU).
#
# Usage (detached, so the session can be closed):
#   setsid nohup hpc/fetch_snapshots.sh <list> > $W/logs/snapshots_driver.log 2>&1 &
#   <list>: one "<run folder> <wrfout name>" per line, e.g.
#           2019020918 wrfout_d02_2019-02-11_00:00:00
# Stop:   touch $W/logs/snapshots.stop   (finishes the transfers in flight)
# Re-entrant: a state whose snapshot exists is skipped.
set -uo pipefail

LIST="${1:?usage: fetch_snapshots.sh <list of \"<run folder> <wrfout name>\" lines>}"
PROJECT_DIR="${PROJECT_DIR:-/leonardo/home/userexternal/lmonaco0/CHAPTER}"
W="${W:-/leonardo_work/AIFPT_AILAMIT/CHAPTER}"
STAGE="${STAGE:-${W}/wrfout_dayend}"        # never the pipeline's wrfout dirs: a
                                            # 24 h file is named like the next
                                            # day's 00Z and would be taken for it
SNAP_DIR="${SNAP_DIR:-${W}/accum_snap}"
LEDGER="${LEDGER:-${W}/logs/snapshots_status.log}"
STOP="${STOP:-${W}/logs/snapshots.stop}"
PARALLEL="${PARALLEL:-6}"                    # the relay's knee (#69)
MIN_BYTES=8000000000

# Transfer settings from the pipeline config, so there is one source for them.
cfg() { (cd "$PROJECT_DIR" && ~/.local/bin/uv run python -c \
    "from omegaconf import OmegaConf; print(OmegaConf.load('conf/pipeline.yaml').datamover.$1)"); }
DATAMOVER_HOST="$(cfg host)"; REMOTE_HOST="$(cfg remote_host)"
IDENTITY_FILE="$(cfg identity_file)"; SFTP_OPTS="$(cfg sftp_opts)"
BASE_2023="$(cfg base_2023)"; BASE_PRE2023="$(cfg base_pre2023)"
FETCH_TIMEOUT="$(cfg fetch_timeout)"; FETCH_RETRIES="$(cfg fetch_retries)"
export PROJECT_DIR STAGE SNAP_DIR LEDGER STOP MIN_BYTES DATAMOVER_HOST REMOTE_HOST \
       IDENTITY_FILE SFTP_OPTS BASE_2023 BASE_PRE2023 FETCH_TIMEOUT FETCH_RETRIES

log_status() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | $1 | $2 | ${3:-}" >> "$LEDGER"; }
export -f log_status

fetch_and_snapshot() {
    local run="$1" name="$2" valid snap base remote dest rc attempt errf
    [ -e "$STOP" ] && return 0
    valid="${name:11:4}${name:16:2}${name:19:2}${name:22:2}"
    snap="${SNAP_DIR}/${valid:0:4}/${valid:4:2}/accum_${valid}_run${run}.npz"
    if [ -s "$snap" ]; then log_status "$run/$name" SKIP_SNAPSHOT_EXISTS; return 0; fi
    # Base by the run's TARGET day (init + 6 h), as hpc/dates.py does.
    if [ "$(TZ=UTC date -d "${run:0:8} ${run:8:2}:00 UTC + 6 hours" +%Y)" -ge 2023 ]; then
        base="$BASE_2023"; else base="$BASE_PRE2023"; fi
    remote="${base}/${run}/${name}"
    mkdir -p "${STAGE}/${run}"
    dest="${STAGE}/${run}/${name}"
    errf=$(mktemp); rc=1
    for attempt in $(seq 1 $((FETCH_RETRIES + 1))); do
        rm -f "$dest"
        if timeout "$FETCH_TIMEOUT" ssh -nxT "$DATAMOVER_HOST" \
             "sftp -i ${IDENTITY_FILE} ${SFTP_OPTS} ${REMOTE_HOST}:${remote} ${STAGE}/${run}/" \
             >/dev/null 2>"$errf"; then rc=0; break; else rc=$?; fi
        grep -qiE 'No such file|not a regular file|File .* not found' "$errf" && break
        sleep 30
    done
    if [ "$rc" -ne 0 ]; then
        log_status "$run/$name" FETCH_FAILED "rc=${rc} $(tr '\n' ' ' <"$errf" | cut -c1-200)"
        rm -f "$errf" "$dest"; return 0
    fi
    rm -f "$errf"
    if [ "$(stat -c%s "$dest" 2>/dev/null || echo 0)" -lt "$MIN_BYTES" ]; then
        log_status "$run/$name" UNREADABLE "size=$(stat -c%s "$dest" 2>/dev/null || echo 0)B"
        rm -f "$dest"; return 0
    fi
    if (cd "$PROJECT_DIR" && ~/.local/bin/uv run python accum_hourly.py snapshot "$dest" "$SNAP_DIR") >/dev/null 2>"${dest}.err"; then
        # The snapshot is named after the state READ from the file. If that is not
        # the state asked for, the relay holds another run under this name: say so,
        # rather than OK, so the hour is not believed covered.
        if [ -s "$snap" ]; then
            log_status "$run/$name" SNAPSHOT_OK "$snap"
        else
            log_status "$run/$name" RUN_MISMATCH "the file is not from run ${run}; its snapshot was kept under its own state"
        fi
        rm -f "$dest" "${dest}.err"
    else
        log_status "$run/$name" SNAPSHOT_FAILED "$(tail -n 2 "${dest}.err" | tr '\n' ' ' | cut -c1-200)"
        rm -f "$dest"
    fi
}
export -f fetch_and_snapshot

echo "$(date -u +%FT%TZ) start: $(wc -l <"$LIST") states, parallel ${PARALLEL}, ledger ${LEDGER}"
before=$(grep -c SNAPSHOT_OK "$LEDGER" 2>/dev/null || true)
xargs -P "$PARALLEL" -L 1 bash -c 'fetch_and_snapshot "$0" "$1"' < "$LIST"
after=$(grep -c SNAPSHOT_OK "$LEDGER" 2>/dev/null || true)
echo "$(date -u +%FT%TZ) done: $(( ${after:-0} - ${before:-0} )) snapshots written by this run"
