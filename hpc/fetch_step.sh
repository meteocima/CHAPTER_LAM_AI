#!/bin/bash
#
# Recursive, time-budgeted fetch driver for the step-by-step pipeline.
#
# RUNS ON A LOGIN NODE (NOT via SLURM). The CINECA datamover
# (data.leonardo.cineca.it) is reachable only from regular login nodes -- NOT from
# lrd_all_serial (login08/13 are firewalled off) nor compute nodes. So the fetch
# cannot be a SLURM job. The launcher starts this script detached on the login
# node; it sftp's each wrfout via the datamover and submits the (heavy) convert to
# dcgp_usr_prod via sbatch.
#
# The login-node limit is `ulimit -t` = 600s of CPU TIME per process (not wall time).
# The transfer itself runs on the datamover -- data goes LRZ -> datamover -> the shared
# FS, never through this node -- so the driver and its ssh sit at ~0s CPU and a process
# survives for hours (measured). Only the NetCDF check costs CPU (~1.9s/file, and in its
# own python process). The driver still works to a wall-time
# budget (DRIVER_MAX_SECONDS) and then RE-SPAWNS ITSELF detached (setsid) for the
# next batch -- each process stays well under the limit. The convert jobs are the
# only SLURM jobs.
#
# Per timestep it:
#   1. skips it if the output GRIB already exists (re-entrancy)
#   2. fetches the wrfout via:
#         ssh -nxT <datamover> "sftp -i <key> <opts> <relay>:<remote> <local>/"
#
# The -n matters and is not cosmetic: ssh reads stdin by default and forwards it
# to the remote command, so a backgrounded fetch inherits fd 0 and DRAINS it.
# The driver's own loop reads nothing from stdin and is immune, but a caller
# that drives this from `while read ... done < <(...)` and backgrounds it loses
# the loop's input: the loop ends after about FETCH_PARALLEL iterations AND
# REPORTS SUCCESS. That cut a staging phase to 3 files of 21, twice, before the
# caller was fixed -- and the caller is the wrong place for the defence, which
# is why it lives here now (issue #32).
#      wrapped in `timeout` (cuts tape-recall hangs) with a few retries
#   3. checks the file is a readable NetCDF (catches tape stubs / truncation)
#   3b. snapshots the 19 accumulators of the file (accum_hourly.py), and for 00Z
#      also of the 24 h file of the run for the previous day -- the only file
#      that holds the hour 23Z -> 00Z (#70, #71). Every accumulation is the hour
#      ending at its timestep, differenced against the state before it.
#   4. submits the convert_step.sh job (dcgp_usr_prod) of every hour that is now
#      READY: its own wrfout is local and the snapshots of its hour exist. That is
#      this timestep in forward order, the one after it in backward order, so
#      each worker tries both, and whichever of the two events comes second
#      submits (under a lock). The state before the window's oldest hour is
#      fetched once the window is done; an hour still not ready then is logged.
#      -- UNLESS DOWNLOAD_ONLY=1, in which case it stops at step 3b and KEEPS the
#      wrfout (convert_step.sh deletes it on success), for staging raw files.
# Every outcome is appended to STATUS_LOG (single writer = this driver chain).
# Missing / on-tape / unreadable files are logged and SKIPPED, never fatal.
#
# Required env vars (set by hpc/submit_step_pipeline.py):
#   START_DT, END_DT, CURRENT_DT   - "YYYY-MM-DDTHH"; START=oldest, END=newest edge
#   DIRECTION                      - "backward" (newest->oldest, default) or "forward"
#   BATCH_SIZE                     - max timesteps per process (time budget usually cuts first)
#   DRIVER_MAX_SECONDS             - wall-time budget per process before re-spawning
#   FETCH_PARALLEL                 - concurrent sftp transfers
#   FETCH_TIMEOUT, FETCH_RETRIES   - per-sftp timeout (s) and retry count
#   WRFOUT_DIR, GRIB_DIR, GRIB_TEMPLATE, PROJECT_DIR, ACCUM_SNAP_DIR, STATIC_REF_DIR
#   DATAMOVER_HOST, REMOTE_HOST, IDENTITY_FILE, SFTP_OPTS, BASE_2023, BASE_PRE2023, INIT_HOUR
#   LOG_DIR, STATUS_LOG, DRIVER_LOG, DRIVER_SCRIPT, CONVERT_SCRIPT
#   CONVERT_PARTITION, CONVERT_WALLTIME, CONVERT_MEM, CONVERT_ACCOUNT
#   DOWNLOAD_ONLY                  - "1" to fetch only: no convert submitted, wrfout kept
#   KEEP_WRFOUT                    - "1" to convert but keep the wrfout (passed to convert_step.sh)
#   MAX_QUEUED_CONVERTS            - >0: cap on this user's queued conv_* jobs. A convert is
#                                    submitted whenever fewer than this are queued (#65)
#   DRY_RUN                       - "1" to print commands instead of running them

set -euo pipefail

DRY_RUN="${DRY_RUN:-0}"
# Fetch-only mode: never submit a convert, keep the wrfout on disk. Exported so it
# survives the respawn chain -- losing it mid-chain would silently start deleting
# staged files (convert_step.sh removes its input on success).
DOWNLOAD_ONLY="${DOWNLOAD_ONLY:-0}"; export DOWNLOAD_ONLY
# Convert but keep the input wrfout (e.g. converting files staged for someone else).
KEEP_WRFOUT="${KEEP_WRFOUT:-0}"; export KEEP_WRFOUT
# Queue gate: CINECA frowns on hundreds of queued jobs. With a value > 0 the driver keeps
# at most this many conv_* jobs of this user queued, submitting as soon as there is room.
MAX_QUEUED_CONVERTS="${MAX_QUEUED_CONVERTS:-0}"
DIRECTION="${DIRECTION:-backward}"
INIT_HOUR=$(printf "%02d" "$((10#${INIT_HOUR:-18}))")
FETCH_PARALLEL="${FETCH_PARALLEL:-2}"
BATCH_SIZE="${BATCH_SIZE:-24}"
DRIVER_MAX_SECONDS="${DRIVER_MAX_SECONDS:-1080}"
FETCH_TIMEOUT="${FETCH_TIMEOUT:-600}"
FETCH_RETRIES="${FETCH_RETRIES:-2}"
ACCUM_SNAP_DIR="${ACCUM_SNAP_DIR:-$(dirname "${GRIB_DIR%/}")/accum_snap}"
# The 24 h files land here, never in WRFOUT_DIR: one is named like the next day's
# 00Z, and would be taken for it.
DAYEND_DIR="${DAYEND_DIR:-${WRFOUT_DIR%/}_dayend}"
STATIC_REF_DIR="${STATIC_REF_DIR:-$(dirname "${GRIB_DIR%/}")/static_v1}"
IDENTITY_FILE="${IDENTITY_FILE:-}"
SFTP_OPTS="${SFTP_OPTS:--B 262144 -R 256 -p}"
STATUS_LOG="${STATUS_LOG:-${LOG_DIR}/step_pipeline_status.log}"
DRIVER_LOG="${DRIVER_LOG:-${LOG_DIR}/fetch_step_driver.log}"
# One job-id marker (and its lock) per submitted hour, beside this chain's ledger,
# and the hours waiting for a snapshot or for room in the queue (#71).
SUBMIT_MARKS="${STATUS_LOG%.log}.submitted"
PENDING="${STATUS_LOG%.log}.pending"
# Days whose 00Z hour (23Z -> 00Z of the day before) was verified LOST at the source
# on LRZ, space-separated YYYY-MM-DD: their 00Z is converted with the accumulations
# missing instead of waiting for the 24 h file (#71). A list of days and not a switch,
# so that a file merely late is never published missing. Empty by default.
MISSING_00Z_DAYS="${MISSING_00Z_DAYS:-}"; export MISSING_00Z_DAYS
# Set on the respawns that only drain the pending list past the window edge.
CLOSING="${CLOSING:-0}"
SKIP_LIST="${SKIP_LIST:-}"
# Login nodes cannot ssh/pkill one another, so a flag file on the shared FS is the
# only way to stop a driver chain from a different login node than it runs on.
STOP_FLAG="${STOP_FLAG:-${LOG_DIR}/fetch_step.stop}"
# A genuine wrfout is ~8.6G; far below this after a "successful" sftp is a tape
# stub or a truncated transfer.
MIN_BYTES="${MIN_WRFOUT_BYTES:-1073741824}"  # 1 GiB
DRIVER_START=$(date +%s)

# ---- helpers ---------------------------------------------------------------

# Append a step outcome to the status ledger. One chain writes it, from its main
# loop and from its background workers; each line is one short append.
#   $1 = target timestep "YYYY-MM-DDTHH"   $2 = STATUS   $3 = detail
log_status() {
    local ts
    ts=$(TZ=UTC date -u +%Y-%m-%dT%H:%M:%SZ)
    if [ "${DRY_RUN}" = "1" ]; then
        echo "  [LOG] ${ts} | $1 | $2 | ${3:-}"
    else
        printf '%s | %s | %s | %s\n' "$ts" "$1" "$2" "${3:-}" >> "${STATUS_LOG}"
    fi
}

# Has a stop been requested? Checked at startup, before each timestep, and before
# the respawn, so the chain dies within one in-flight sftp rather than at the window edge.
stop_requested() {
    [ -n "${STOP_FLAG}" ] && [ -e "${STOP_FLAG}" ]
}

# Is the datamover reachable from this node? (TCP :22; the restricted shell
# rejects probe commands, so test the socket directly.)
datamover_reachable() {
    timeout 15 bash -c "cat < /dev/null > /dev/tcp/${DATAMOVER_HOST}/22" 2>/dev/null
}

# Inner command run ON the datamover to pull one file from the LRZ relay.
#   $1 = remote path on the relay   $2 = local destination directory
fetch_cmd() {
    local id_arg=""
    [ -n "${IDENTITY_FILE}" ] && id_arg="-i ${IDENTITY_FILE}"
    echo "sftp ${id_arg} ${SFTP_OPTS} ${REMOTE_HOST}:$1 $2/"
}

# Remote wrfout path on the relay for a given target date/hour.
remote_path() {
    local d="$1" h="$2" year init base
    year="${d:0:4}"
    init="$(TZ=UTC date -d "${d} -1 day" +%Y%m%d)${INIT_HOUR}"
    if [ "$year" -ge 2023 ]; then base="${BASE_2023}"; else base="${BASE_PRE2023}"; fi
    echo "${base}/${init}/wrfout_d02_${d}_${h}:00:00"
}

# Expanded output GRIB path for a given target date/hour (under a YYYY/MM tree).
grib_path() {
    local d="$1" h="$2" out year month dcompact
    year="${d:0:4}"
    month="${d:5:2}"
    dcompact="${d//-/}"
    out="${GRIB_DIR}/${year}/${month}/${GRIB_TEMPLATE}"
    out="${out//\{year\}/$year}"
    out="${out//\{date_compact\}/$dcompact}"
    out="${out//\{hour:02d\}/$h}"
    echo "$out"
}

# Is this timestep already done, and with which ledger tag? Prints the tag and
# returns 0 when it can be skipped. In download-only mode the GRIB never exists, so
# re-entrancy has to key on the staged wrfout instead -- and on its SIZE, or a
# truncated leftover would be mistaken for a finished download.
already_done() {
    local d="$1" h="$2" raw
    if [ "${DOWNLOAD_ONLY}" = "1" ]; then
        raw="${WRFOUT_DIR}/${d}/wrfout_d02_${d}_${h}:00:00"
        if [ -f "$raw" ] && [ "$(stat -c%s "$raw" 2>/dev/null || echo 0)" -ge "$MIN_BYTES" ]; then
            echo "SKIP_RAW_EXISTS"; return 0
        fi
    elif [ -f "$(grib_path "$d" "$h")" ]; then
        echo "SKIP_GRIB_EXISTS"; return 0
    fi
    return 1
}

# Submit a convert job for one timestep. Real mode echoes ONLY the job id
# (--parsable); dry mode prints the command.
submit_convert() {
    # Structural guard: in download-only mode a convert must never reach sbatch --
    # it would delete the wrfout we just staged. Belt and braces with the call sites.
    if [ "${DOWNLOAD_ONLY}" = "1" ]; then
        echo "  [BUG] submit_convert called in download-only mode; refusing." >&2
        return 0
    fi
    local d="$1" h="$2" dcompact local_dir convert_env
    dcompact="${d//-/}"
    local_dir="${WRFOUT_DIR}/${d}"
    convert_env="TARGET_DATE=${d},HOUR=${h},WRFOUT_DIR=${local_dir},GRIB_DIR=${GRIB_DIR},PROJECT_DIR=${PROJECT_DIR},GRIB_TEMPLATE=${GRIB_TEMPLATE},ACCUM_SNAP_DIR=${ACCUM_SNAP_DIR},STATIC_REF_DIR=${STATIC_REF_DIR},KEEP_WRFOUT=${KEEP_WRFOUT},MISSING_00Z_AS_BITMAP=$(lost_00z "$d" "$h" && echo 1 || true)"

    local acct_args=()
    [ -n "${CONVERT_ACCOUNT:-}" ] && acct_args=(--account "${CONVERT_ACCOUNT}")

    local args=(
        --partition "${CONVERT_PARTITION}"
        --time "${CONVERT_WALLTIME}"
        --mem "${CONVERT_MEM}"
        --job-name "conv_${dcompact}${h}"
        --output "${LOG_DIR}/convert_${dcompact}${h}_%j.out"
        --export "${convert_env}"
        "${acct_args[@]}"
        "${CONVERT_SCRIPT}"
    )
    if [ "${DRY_RUN}" = "1" ]; then
        echo "  [DRY] sbatch ${args[*]}"
    else
        sbatch --parsable "${args[@]}"
    fi
}

# Fetch one timestep via the datamover (unless already local) and validate it.
# Failures are logged in STATUS_LOG with a grep-able tag; returns 1 on failure.
#   $3 = remote path, $4 = local directory: optional, for a file that is not one of
#   the archive's timesteps (the 24 h file of a run, see ensure_dayend); $5 =
#   "quiet" leaves the ledger to the caller, so such a file's failure is not
#   recorded against the archived timestep that shares its name.
fetch_wrfout() {
    local d="$1" h="$2" quiet="${5:-}"
    local dt="${d}T${h}"
    local local_dir remote fname dest
    local_dir="${4:-${WRFOUT_DIR}/${d}}"
    remote="${3:-$(remote_path "$d" "$h")}"
    fname="wrfout_d02_${d}_${h}:00:00"
    dest="${local_dir}/${fname}"
    mkdir -p "$local_dir"

    if [ "${DRY_RUN}" = "1" ]; then
        echo "  [DRY] ssh -nxT ${DATAMOVER_HOST} \"$(fetch_cmd "$remote" "$local_dir")\""
        return 0
    fi

    # -s alone would accept a multi-GB partial left by a driver killed mid-sftp:
    # the fetch would be skipped, the size gate below would then delete it, and the
    # timestep would only come back on a later full re-run. Re-fetch it instead.
    if [ -s "$dest" ] && [ "$(stat -c%s "$dest" 2>/dev/null || echo 0)" -ge "$MIN_BYTES" ]; then
        echo "  [${dt}] wrfout already present locally."
    else
        [ -e "$dest" ] && { echo "  [${dt}] partial wrfout on disk, re-fetching."; timeout 30 rm -f "$dest" 2>/dev/null || true; }
        local attempt rc errf snippet max_attempts
        max_attempts=$((FETCH_RETRIES + 1))
        errf=$(mktemp)
        rc=1
        for attempt in $(seq 1 "$max_attempts"); do
            echo "  [${dt}] fetch attempt ${attempt}/${max_attempts} via datamover..."
            if timeout "${FETCH_TIMEOUT}" ssh -nxT "${DATAMOVER_HOST}" \
                 "$(fetch_cmd "$remote" "$local_dir")" 2>"$errf"; then
                rc=0; break
            else
                rc=$?
            fi
            # A genuinely missing source never appears -> stop retrying. sftp words it
            # as 'File "<path>" not found.' or 'remote open(...): No such file or
            # directory'; match 'File ... not found' rather than a bare 'not found' so a
            # missing sftp binary on the datamover stays a FETCH_ERROR. A timeout
            # (rc=124), though, is usually transient datamover/relay congestion (an sftp
            # crawling past ${FETCH_TIMEOUT}s while other transfers also succeed), NOT
            # a file on tape -> retry it with a longer backoff. Only a persistent
            # timeout across all attempts is logged as a problem.
            if grep -qiE 'No such file|not a regular file|File .* not found' "$errf"; then break; fi
            if [ "$rc" -eq 124 ]; then
                echo "  [${dt}] sftp timed out (attempt ${attempt}/${max_attempts}); likely congestion, backing off"
                sleep 30
            else
                sleep 5
            fi
        done

        if [ "$rc" -ne 0 ]; then
            snippet=$(tr '\n' ' ' <"$errf" | tr -s ' ' | cut -c1-200)
            rm -f "$errf"; timeout 30 rm -f "$dest" 2>/dev/null || true
            if [ "$rc" -eq 124 ]; then
                echo "  WARN [${dt}] FETCH_TIMEOUT (sftp > ${FETCH_TIMEOUT}s x${max_attempts})"
                [ -n "$quiet" ] || log_status "$dt" "FETCH_TIMEOUT" "sftp exceeded ${FETCH_TIMEOUT}s on all ${max_attempts} attempts; usually datamover/relay congestion (re-run re-entrant), occasionally a file truly on tape (recall only if it persists across re-runs)"
            elif echo "$snippet" | grep -qiE 'No such file|not a regular file|File .* not found'; then
                echo "  WARN [${dt}] MISSING_ON_LRZ"
                [ -n "$quiet" ] || log_status "$dt" "MISSING_ON_LRZ" "$snippet"
            else
                echo "  WARN [${dt}] FETCH_ERROR rc=${rc}"
                [ -n "$quiet" ] || log_status "$dt" "FETCH_ERROR" "rc=${rc} ${snippet}"
            fi
            return 1
        fi
        rm -f "$errf"
    fi

    # Integrity check: size sanity + NetCDF header open. A truncated/0-byte transfer
    # (datamover hiccup) or, rarely, a tape stub fails here -> drop it and flag.
    # Re-entrant re-run re-fetches; only a persistent failure points to real tape.
    local size
    size=$(stat -c%s "$dest" 2>/dev/null || echo 0)
    if [ "$size" -lt "$MIN_BYTES" ] || \
       ! ( cd "$PROJECT_DIR" && uv run python -c "import sys,netCDF4; netCDF4.Dataset(sys.argv[1]).close()" "$dest" ) >/dev/null 2>&1; then
        echo "  WARN [${dt}] UNREADABLE (size=${size}B)"
        [ -n "$quiet" ] || log_status "$dt" "UNREADABLE" "size=${size}B not a readable NetCDF; truncated/0-byte transfer or tape stub -> re-run re-entrant, recall only if it persists"
        timeout 30 rm -f "$dest" 2>/dev/null || true
        return 1
    fi
}

# ---- hourly accumulations (accum_hourly.py, #71) ---------------------------
raw_path() { echo "${WRFOUT_DIR}/$1/wrfout_d02_$1_$2:00:00"; }
raw_ok() { [ -f "$1" ] && [ "$(stat -c%s "$1" 2>/dev/null || echo 0)" -ge "$MIN_BYTES" ]; }

# --- hourly states (extracted by tests/test_accum_hourly.py; keep the markers) ---
# accum_hourly.py computes these in python; bash cannot import it, so the test
# runs what lies between the markers and insists the two agree.
# Run init "YYYYMMDDHH" of the run whose 24 files make up day $1.
run_for_day() { echo "$(TZ=UTC date -d "$1 -1 day" +%Y%m%d)${INIT_HOUR}"; }
day_shift() { TZ=UTC date -d "$1 $2 day" +%Y-%m-%d; }
epoch_of() { TZ=UTC date -d "$1 $((10#$2)):00:00" +%s; }

# Snapshot path of the state (valid day $1, hour $2) of run $3 -- the layout of
# accum_hourly.snapshot_path.
snap_path() { echo "${ACCUM_SNAP_DIR}/${1:0:4}/${1:5:2}/accum_${1//-/}$2_run$3.npz"; }

# Snapshot of the state the archived file of (day $1, hour $2) holds.
own_snap() { snap_path "$1" "$2" "$(run_for_day "$1")"; }

# Is (day $1, hour $2) a 00Z whose hour was verified lost (MISSING_00Z_DAYS)?
lost_00z() { [ "$2" = "00" ] && [[ " ${MISSING_00Z_DAYS} " == *" $1 "* ]]; }

# The snapshots the hour ending at (day $1, hour $2) is differenced from, one per
# line (accum_hourly.window): the state before it in the run for its day, or for
# 00Z the 24 h file and the 23Z of the run for the day before.
window_snaps() {
    local d="$1" h="$2" p
    if [ "$h" = "00" ]; then
        p=$(day_shift "$d" -1)
        snap_path "$d" 00 "$(run_for_day "$p")"
        snap_path "$p" 23 "$(run_for_day "$p")"
    else
        snap_path "$d" "$(printf %02d $((10#$h - 1)))" "$(run_for_day "$d")"
    fi
}
# --- end hourly states ---

# Snapshot one local wrfout. Its own python process (~11 s CPU on a login node).
make_snapshot() {
    local file="$1" key="$2" out
    if [ "${DRY_RUN}" = "1" ]; then echo "  [DRY] snapshot ${file}"; return 0; fi
    if ! out=$(cd "$PROJECT_DIR" && uv run python accum_hourly.py snapshot "$file" "$ACCUM_SNAP_DIR" 2>&1); then
        log_status "$key" "SNAPSHOT_FAILED" "$(printf '%s' "$out" | tail -n 1 | cut -c1-200)"
        return 1
    fi
    # Only for an archived state: the 24 h file shares its key with the archived
    # 00Z, and its success must not clear a problem logged against that file.
    [ -n "${3:-}" ] && log_status "$key" "SNAPSHOT_OK" "$(printf '%s' "$out" | tail -n 1 | cut -c1-200)"
    return 0
}

# Snapshot of the archived state (day $1, hour $2), from its local wrfout.
ensure_archive_snapshot() {
    local d="$1" h="$2" raw
    [ -s "$(own_snap "$d" "$h")" ] && return 0
    raw=$(raw_path "$d" "$h")
    [ -f "$raw" ] || return 1
    make_snapshot "$raw" "${d}T${h}" archived
}

# Snapshot of the 24 h file of the run for the day before $1, i.e. the state at
# 00Z of $1 that closes the previous day: fetched into DAYEND_DIR, snapshotted,
# deleted. The relay base follows the run's target day, as remote_path does.
ensure_dayend() {
    local d="$1" p run snap dir base
    p=$(day_shift "$d" -1)
    run=$(run_for_day "$p")
    snap=$(snap_path "$d" 00 "$run")
    [ -s "$snap" ] && return 0
    dir="${DAYEND_DIR}/${run}"
    [ "${DRY_RUN}" = "1" ] || mkdir -p "$dir"
    if [ "${p:0:4}" -ge 2023 ]; then base="${BASE_2023}"; else base="${BASE_PRE2023}"; fi
    if ! fetch_wrfout "$d" "00" "${base}/${run}/wrfout_d02_${d}_00:00:00" "$dir" quiet; then
        log_status "${d}T00" "DAYEND_UNAVAILABLE" "24 h file of run ${run} not fetched (missing, empty or timed out; see the driver log): the hour 23Z->00Z of ${p} cannot be computed. Verify on LRZ; if lost, list the day in pipeline.missing_00z_days and re-run"
        return 1
    fi
    make_snapshot "${dir}/wrfout_d02_${d}_00:00:00" "${d}T00" || return 1
    [ "${DRY_RUN}" = "1" ] || timeout 60 rm -f "${dir}/wrfout_d02_${d}_00:00:00" 2>/dev/null || true
}

# Submit the convert of (day $1, hour $2) if it is READY: in the window, no GRIB
# yet, its wrfout fetched AND validated (proved by its own snapshot, written only
# after the NetCDF check -- a file still arriving is past MIN_BYTES long before it
# is whole), and the snapshots of its hour present. Called by the worker that
# fetched it, by the one that fetched the state before it, and from the pending
# list; the lock and the job-id marker keep them from submitting it twice.
# Returns 0 (submitted or nothing to do), 1 (not ready), 2 (the queue is full).
# An hour that is local but cannot go yet is put on the pending list.
submit_if_ready() {
    local d="$1" h="$2" dt="$1T$2" s rc=0
    [ "${DOWNLOAD_ONLY}" = "1" ] && return 0
    within_window "$(epoch_of "$d" "$h")" || return 0
    [ -f "$(grib_path "$d" "$h")" ] && return 0
    raw_ok "$(raw_path "$d" "$h")" || return 1
    if [ "${DRY_RUN}" = "1" ]; then submit_convert "$d" "$h"; return 0; fi
    [ -s "$(own_snap "$d" "$h")" ] || rc=1
    for s in $(window_snaps "$d" "$h"); do
        [ -s "$s" ] && continue
        # A 24 h file verified lost: the convert publishes the hour missing. The
        # 23Z state is still awaited (accum_hourly.increments does the same).
        lost_00z "$d" "$h" && [[ "$s" == */accum_${d//-/}00_run* ]] && continue
        rc=1
    done
    if [ "$rc" -eq 0 ]; then
        mkdir -p "$SUBMIT_MARKS"
        (
            flock 9
            mark="${SUBMIT_MARKS}/${dt}"
            # Submitted already: the job is in the queue -- or was submitted under two
            # minutes ago, since squeue can take seconds to show a fresh job, and an
            # hour taken for unsubmitted would be logged CONVERT_WAITING after its
            # CONVERT_SUBMITTED (seen on the 2026-10-07 end-to-end run).
            if [ -s "$mark" ] && { [ $(( $(date +%s) - $(stat -c %Y "$mark") )) -lt 120 ] || \
                 timeout 60 squeue -h -j "$(cat "$mark")" 2>/dev/null | grep -q .; }; then
                exit 0
            fi
            [ -f "$(grib_path "$d" "$h")" ] && exit 0
            # The gate admits dispatches in the main loop; this is the hard cap, here
            # because a dispatch may now submit 0, 1 or 2 converts. Count-then-submit
            # under ONE lock for the whole chain: two workers reading 47 of 48 must
            # not both go.
            if [ "$GATED" = "1" ]; then
                exec 7>"${SUBMIT_MARKS}/.gate.lock"
                flock 7
                nq=$(queued_converts) || exit 2
                [ "$nq" -ge "$MAX_QUEUED_CONVERTS" ] && exit 2
            fi
            jobid=$(submit_convert "$d" "$h") || jobid=""
            if ! [[ "$jobid" =~ ^[0-9]+$ ]]; then
                rm -f "$mark"
                log_status "$dt" "SUBMIT_FAILED" "sbatch returned '${jobid}'"
                exit 1
            fi
            echo "$jobid" > "$mark"
            echo "  [${dt}] convert submitted (job ${jobid})"
            log_status "$dt" "CONVERT_SUBMITTED" "job=${jobid}"
        ) 9>"${SUBMIT_MARKS}/${dt}.lock" || rc=$?
    fi
    [ "$rc" -ne 0 ] && add_pending "$dt"
    return "$rc"
}

# The pending list: one "YYYY-MM-DDTHH" per line, shared by the workers (lock).
# The first time an hour is put there it is logged CONVERT_WAITING; the submit
# that eventually lets it go clears that with CONVERT_SUBMITTED.
add_pending() {
    (
        flock 8
        grep -qx "$1" "$PENDING" 2>/dev/null && exit 0
        echo "$1" >> "$PENDING"
        grep -qx "$1" "${PENDING}.seen" 2>/dev/null && exit 0
        echo "$1" >> "${PENDING}.seen"
        log_status "$1" "CONVERT_WAITING" "local, but its snapshots or the queue are not ready yet"
    ) 8>"${PENDING}.lock"
}

# Try every pending hour once; keep those still waiting. Prints how many wait on
# the queue alone (the rest wait on a snapshot or failed to submit).
drain_pending() {
    local dt rc gate_only=0 items=()
    [ -s "$PENDING" ] || { echo 0; return 0; }
    mapfile -t items < <(sort -u "$PENDING")
    : > "$PENDING"
    for dt in "${items[@]}"; do
        rc=0; submit_if_ready "${dt%T*}" "${dt#*T}" >&2 || rc=$?
        [ "$rc" -eq 2 ] && gate_only=$((gate_only + 1))
    done
    echo "$gate_only"
}

# The hour after (day $1, hour $2): the one this state is the previous state of.
next_hour() { TZ=UTC date -d "@$(( $(epoch_of "$1" "$2") + 3600 ))" '+%Y-%m-%d %H'; }

# Fetch one timestep, snapshot it, then submit whatever became ready. Never aborts
# the driver.
process_one() {
    local d="$1" h="$2"
    local dt="${d}T${h}" size nd nh
    fetch_wrfout "$d" "$h" || return 1
    if [ "${DRY_RUN}" = "1" ]; then
        log_status "$dt" "FETCH_OK" "(dry-run)"
        make_snapshot "$(raw_path "$d" "$h")" "$dt"
        [ "$h" = "00" ] && ensure_dayend "$d"
        if [ "${DOWNLOAD_ONLY}" != "1" ]; then
            submit_convert "$d" "$h"
            log_status "$dt" "CONVERT_SUBMITTED" "(dry-run)"
        fi
        return 0
    fi
    size=$(stat -c%s "$(raw_path "$d" "$h")" 2>/dev/null || echo 0)

    log_status "$dt" "FETCH_OK" "size=${size}B"
    ensure_archive_snapshot "$d" "$h" || true
    [ "$h" = "00" ] && { ensure_dayend "$d" || true; }
    if [ "${DOWNLOAD_ONLY}" = "1" ]; then
        echo "  [${dt}] fetched (download-only: no convert, wrfout kept)."
        return 0
    fi
    submit_if_ready "$d" "$h" || true
    read -r nd nh <<< "$(next_hour "$d" "$h")"
    submit_if_ready "$nd" "$nh" || true
}

# An hour whose GRIB exists is not fetched -- but the hour after it may still need
# its state. Fetch it for the snapshot alone, then let the next hour go.
#   $3 = "edge": the state lies outside the window, so its wrfout goes whatever
#   the mode -- no chain of this window will ever convert it.
snapshot_only() {
    local d="$1" h="$2" edge="${3:-}" nd nh raw fetched=0
    raw=$(raw_path "$d" "$h")
    if ! [ -f "$raw" ]; then
        fetch_wrfout "$d" "$h" || return 1
        fetched=1
    fi
    ensure_archive_snapshot "$d" "$h" || return 1
    if [ "$fetched" = "1" ] && { [ -n "$edge" ] || { [ "${KEEP_WRFOUT}" != "1" ] && [ "${DOWNLOAD_ONLY}" != "1" ]; }; }; then
        timeout 60 rm -f "$raw" 2>/dev/null || true
    fi
    read -r nd nh <<< "$(next_hour "$d" "$h")"
    submit_if_ready "$nd" "$nh" || true
}

# Does the hour after (day $1, hour $2) still need this state's snapshot?
next_needs_snapshot() {
    local d="$1" h="$2" nd nh
    [ "${DOWNLOAD_ONLY}" = "1" ] && return 1
    read -r nd nh <<< "$(next_hour "$d" "$h")"
    within_window "$(epoch_of "$nd" "$nh")" || return 1
    [ -f "$(grib_path "$nd" "$nh")" ] && return 1
    [ -s "$(own_snap "$d" "$h")" ] && return 1
    return 0
}

# Once the window is done: fetch the state before its oldest hour, which no
# timestep of the window brings -- in download-only mode too, so that the convert
# chain over the staged files never needs the datamover -- then put every hour
# still without a GRIB on the pending list and work it off. Hours that wait only
# on the queue keep the chain alive (it respawns past the window edge and comes
# back here); hours that wait on a missing snapshot are logged CONVERT_BLOCKED
# with what they wait for, and the chain ends.
# The state before the window's oldest hour, which no timestep of the window brings
# -- in download-only mode too, so that the convert chain over the staged files never
# needs the datamover -- and, if that hour is a 00Z, its 24 h file.
fetch_edge_state() {
    local sd sh pd ph
    sd="${START_DT%T*}"; sh="${START_DT#*T}"
    read -r pd ph <<< "$(TZ=UTC date -d "@$(( START_EPOCH - 3600 ))" '+%Y-%m-%d %H')"
    if ! [ -f "$(grib_path "$sd" "$sh")" ] && ! ensure_archive_snapshot "$pd" "$ph"; then
        echo "  [${pd}T${ph}] state before the window: fetching it for its snapshot."
        snapshot_only "$pd" "$ph" edge || true
    fi
    [ "$sh" = "00" ] && { ensure_dayend "$sd" || true; }
    return 0
}

close_window() {
    local e d h dt s missing gate_only
    if [ "${DRY_RUN}" = "1" ]; then echo "  [DRY] close_window: edge state + pending sweep"; return 0; fi
    # In forward order the edge was fetched by the first process; a CLOSING respawn
    # has done it already.
    [ "${DIRECTION}" = "backward" ] && [ "${CLOSING}" != "1" ] && fetch_edge_state
    [ "${DOWNLOAD_ONLY}" = "1" ] && return 0

    e=$START_EPOCH
    while [ "$e" -le "$END_EPOCH" ]; do
        d=$(TZ=UTC date -d "@${e}" +%Y-%m-%d); h=$(TZ=UTC date -d "@${e}" +%H)
        if ! [ -f "$(grib_path "$d" "$h")" ] && raw_ok "$(raw_path "$d" "$h")"; then
            add_pending "${d}T${h}"
        fi
        e=$((e + 3600))
    done
    while [ -s "$PENDING" ]; do
        gate_only=$(drain_pending)
        [ -s "$PENDING" ] || break
        if [ "$gate_only" -eq 0 ]; then
            while read -r dt; do
                missing=""
                for s in $(window_snaps "${dt%T*}" "${dt#*T}") $(own_snap "${dt%T*}" "${dt#*T}"); do
                    [ -s "$s" ] || missing="${missing} $(basename "$s")"
                done
                log_status "$dt" "CONVERT_BLOCKED" "missing snapshot(s):${missing:- none, see SUBMIT_FAILED}"
            done < <(sort -u "$PENDING")
            : > "$PENDING"
            break
        fi
        # Only the queue holds them. Not gate_wait: its estimate can admit while the
        # hard cap in submit_if_ready refuses, and the loop would spin on squeue.
        if stop_requested; then
            echo "STOP flag present (${STOP_FLAG}); ${gate_only} hour(s) left pending."
            return 0
        fi
        if [ "$(( $(date +%s) - DRIVER_START ))" -ge "$DRIVER_MAX_SECONDS" ]; then
            echo "Time budget reached with ${gate_only} hour(s) waiting on the queue; respawning to drain them."
            CLOSING=1 respawn "$(TZ=UTC date -d "@$(( END_EPOCH + 3600 ))" +%Y-%m-%dT%H)"
            return 0
        fi
        sleep 60
    done
}

# Re-spawn this driver detached for the next timestep (fresh login-node clock).
respawn() {
    local next_dt="$1"
    if stop_requested; then
        echo "STOP flag present (${STOP_FLAG}); not respawning. Remove it and re-launch to resume."
        return 0
    fi
    # The chain re-execs the driver FROM DISK on every respawn, so a script edited
    # mid-run -- or caught half-written by a non-atomic rewrite -- kills the chain
    # silently (observed 2026-09-07: a doc edit landed during a respawn and the whole
    # 2024 window stopped after 22 files). The launcher now respawns from a snapshot,
    # but validate anyway and leave a ledger entry instead of dying without a trace.
    if ! bash -n "${DRIVER_SCRIPT}" 2>/dev/null; then
        echo "FATAL: ${DRIVER_SCRIPT} is unparsable; not respawning."
        log_status "DRIVER@$(hostname)" "RESPAWN_FAILED" "driver script unparsable (edited mid-run?); re-launch the window, it is re-entrant"
        return 1
    fi
    if [ "${DRY_RUN}" = "1" ]; then
        echo "[DRY] setsid bash ${DRIVER_SCRIPT}   (CURRENT_DT=${next_dt}, DOWNLOAD_ONLY=${DOWNLOAD_ONLY})"
    else
        CURRENT_DT="${next_dt}" DOWNLOAD_ONLY="${DOWNLOAD_ONLY}" KEEP_WRFOUT="${KEEP_WRFOUT}" \
            CLOSING="${CLOSING}" setsid bash "${DRIVER_SCRIPT}" >> "${DRIVER_LOG}" 2>&1 < /dev/null &
        echo "Respawned driver (pid $!) for ${next_dt}."
    fi
}

# ---- main ------------------------------------------------------------------

if [ "${DIRECTION}" = "forward" ]; then STEP=3600; else STEP=-3600; DIRECTION="backward"; fi

echo "=== CHAPTER fetch_step @ $(hostname) $(date -u +%FT%TZ) ==="
echo "Window:    ${START_DT} (oldest)  ..  ${END_DT} (newest)"
echo "Direction: ${DIRECTION}    Current: ${CURRENT_DT}"
echo "Budget:    ${DRIVER_MAX_SECONDS}s wall, batch<=${BATCH_SIZE}, ${FETCH_PARALLEL} parallel, fetch timeout ${FETCH_TIMEOUT}s"
echo "Datamover: ${DATAMOVER_HOST}  (relay: ${REMOTE_HOST})"
echo "StatusLog: ${STATUS_LOG}"
if [ "${DOWNLOAD_ONLY}" = "1" ]; then
    echo "Mode:      DOWNLOAD_ONLY (no convert, wrfout kept)"
else
    echo "Mode:      fetch + convert (keep wrfout: ${KEEP_WRFOUT}, queue gate: ${MAX_QUEUED_CONVERTS})"
fi
echo "RawDir:    ${WRFOUT_DIR}"
echo "Dry run:   ${DRY_RUN}"

if stop_requested; then
    echo "STOP flag present (${STOP_FLAG}); exiting without fetching. Remove it to resume."
    exit 0
fi
echo ""

mkdir -p "${LOG_DIR}" "$(dirname "${STATUS_LOG}")"

# Refuse to run where the datamover is unreachable (e.g. lrd_all_serial / compute).
if [ "${DRY_RUN}" != "1" ] && ! datamover_reachable; then
    echo "FATAL: datamover ${DATAMOVER_HOST}:22 unreachable from $(hostname)."
    echo "       Launch the pipeline from a regular login node (NOT lrd_all_serial)."
    log_status "DRIVER@$(hostname)" "DATAMOVER_UNREACHABLE" "datamover unreachable; run from a regular login node"
    exit 1
fi

# Load the a-priori skip-list (timesteps whose source is known unavailable, e.g. on
# tape/OFFLINE and not yet recalled). Accepts absolute wrfout paths (the mmlsattr
# stagelist) or bare YYYY-MM-DDTHH lines; '#'/blank ignored. Re-parsed each respawn
# (SKIP_LIST is inherited via the environment, like STATUS_LOG).
declare -A SKIP_SET=()
if [ -n "${SKIP_LIST}" ] && [ -f "${SKIP_LIST}" ]; then
    while IFS= read -r line || [ -n "$line" ]; do
        line="${line%$'\r'}"
        [ -z "$line" ] && continue
        case "$line" in \#*) continue ;; esac
        if [[ "$line" =~ wrfout_d02_([0-9]{4}-[0-9]{2}-[0-9]{2})_([0-9]{2}): ]]; then
            SKIP_SET["${BASH_REMATCH[1]}T${BASH_REMATCH[2]}"]=1
        elif [[ "$line" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2})T([0-9]{2})$ ]]; then
            SKIP_SET["${BASH_REMATCH[1]}T${BASH_REMATCH[2]}"]=1
        fi
    done < "${SKIP_LIST}"
    echo "Skip-list: ${SKIP_LIST}  (${#SKIP_SET[@]} timesteps to skip a-priori)"
elif [ -n "${SKIP_LIST}" ]; then
    echo "WARN: SKIP_LIST set but file not found: ${SKIP_LIST}"
fi

# All timestamp arithmetic is done in UTC (WRF timesteps are UTC) via epoch
# seconds, to avoid local-timezone/DST artifacts in hour labels.
CUR_DATE="${CURRENT_DT%T*}"; CUR_HOUR="${CURRENT_DT#*T}"
CUR_EPOCH=$(TZ=UTC date -d "${CUR_DATE} $((10#${CUR_HOUR})):00:00" +%s)
START_EPOCH=$(TZ=UTC date -d "${START_DT%T*} $((10#${START_DT#*T})):00:00" +%s)
END_EPOCH=$(TZ=UTC date -d "${END_DT%T*} $((10#${END_DT#*T})):00:00" +%s)

# A timestep is in scope if it lies within [oldest, newest], regardless of direction.
within_window() { [ "$1" -ge "$START_EPOCH" ] && [ "$1" -le "$END_EPOCH" ]; }

# Number of this user's convert jobs in the queue (pending + running). Prints
# nothing and returns 1 when squeue fails, so the gate waits instead of guessing.
queued_converts() {
    local out
    out=$(timeout 60 squeue -h -u "${USER}" -o %j 2>/dev/null) || return 1
    printf '%s\n' "$out" | awk '/^conv_/ {n++} END {print n+0}'
}

GATED=0
if [ "${MAX_QUEUED_CONVERTS}" -gt 0 ] && [ "${DOWNLOAD_ONLY}" != "1" ] && [ "${DRY_RUN}" != "1" ]; then
    GATED=1
fi
# BATCH_SIZE is no longer capped to MAX_QUEUED_CONVERTS. It used to be, because a batch
# drained the queue to zero and then refilled it; now the two are independent -- the gate
# bounds how many converts are IN the queue, BATCH_SIZE how many timesteps one driver
# process handles before respawning.

# --- convert gate (extracted by tests/test_convert_gate.py; keep the markers) ---
# Sliding window, not a barrier (#65). The old gate waited for ZERO queued conv_* between
# batches, so every batch cost as much as its slowest job: measured on the 2026-09-29
# campaign, three quarters of a 96-job batch finished in four minutes and the last quarter
# took another six. Admitting on "fewer than N queued" gives that tail back.
#
# squeue is NOT called once per timestep. Q_CACHED holds the last measured count and
# Q_SINCE the dispatches made since it, so a fresh count is only fetched when the
# optimistic estimate reaches the limit -- roughly one squeue per N submissions instead of
# one per timestep, which matters when the wrfout are already local and a timestep costs a
# second. Since #71 the estimate counts dispatches, not converts: a dispatch may submit 0, 1
# or 2 of them (its own hour and the next), and the pending list submits outside any
# dispatch. So the estimate only paces the dispatches; the cap itself is enforced again
# where sbatch is called (submit_if_ready, under one lock for the chain), which can delay a
# submission but never admit past the cap.
Q_CACHED=0
# Primed so the FIRST admission of every driver process asks slurm for real. A cold cache
# of zero would admit N converts before looking, and the driver respawns every ~18 min --
# so an already-full queue (a respawn, or the other campaign script running alongside)
# would be overshot by up to N each time. Caught by tests/test_convert_gate.py.
Q_SINCE="${MAX_QUEUED_CONVERTS}"

# 0 = a convert may be submitted now, 1 = the caller must wait.
gate_admit() {
    [ "$GATED" = "1" ] || return 0
    if [ $((Q_CACHED + Q_SINCE)) -lt "$MAX_QUEUED_CONVERTS" ]; then
        Q_SINCE=$((Q_SINCE + 1))
        return 0
    fi
    local nq
    if ! nq=$(queued_converts); then
        echo "  [queue] squeue failed; waiting rather than guessing."
        return 1
    fi
    Q_CACHED="$nq"
    # A dispatch already admitted may not have reached sbatch yet: with
    # FETCH_PARALLEL > 1 the submit happens inside a backgrounded process_one, after
    # a multi-minute sftp, so squeue cannot see it. Zeroing the estimate here forgot
    # exactly those, and the cap was exceeded by up to FETCH_PARALLEL -- measured at
    # 7 committed against a cap of 4 with a 3-deep lag. At most FETCH_PARALLEL can be
    # in flight -- the main loop waits once that many are RUNNING, so when we are about
    # to dispatch at most FETCH_PARALLEL-1 others are outstanding. Reserving that many
    # is exact rather than merely safe: at FETCH_PARALLEL=1 process_one is synchronous,
    # nothing is ever in flight, and the reserve is correctly zero.
    local reserve=$(( ${FETCH_PARALLEL:-1} - 1 ))
    [ "$reserve" -lt 0 ] && reserve=0
    [ "$reserve" -ge "$MAX_QUEUED_CONVERTS" ] && reserve=$((MAX_QUEUED_CONVERTS - 1))
    [ "$reserve" -lt 0 ] && reserve=0
    Q_SINCE="$reserve"
    if [ $((nq + reserve)) -ge "$MAX_QUEUED_CONVERTS" ]; then
        echo "  [queue] ${nq}/${MAX_QUEUED_CONVERTS} conv_* queued (+${reserve} in flight);" \
             "waiting for room before ${GATE_DT:-the next timestep} ($(date -u +%H:%M)Z)."
        return 1
    fi
    Q_SINCE=$((reserve + 1))
    return 0
}

# Block until there is room.
#   0 = go ahead
#   1 = a stop was requested while waiting
#   2 = the driver's time budget is spent; the caller should respawn, not keep waiting
#
# The budget check is not optional. The gate this replaced slept and re-entered the
# main loop, where the DRIVER_MAX_SECONDS check fires; looping here instead parked a
# login-node process for as long as the queue stayed full -- hours, if DCGP is busy --
# and a parked chain writes no ledger entry at all, so `report=true` shows nothing and
# the only evidence is the driver log. Found in review of 0f674cf.
gate_wait() {
    GATE_DT="${1:-}"
    while ! gate_admit; do
        if stop_requested; then
            echo "STOP flag present (${STOP_FLAG}); stopping while waiting on the queue."
            return 1
        fi
        if [ "$(( $(date +%s) - DRIVER_START ))" -ge "$DRIVER_MAX_SECONDS" ]; then
            echo "Time budget (${DRIVER_MAX_SECONDS}s) reached while waiting on the queue;" \
                 "will respawn for the rest of the window."
            return 2
        fi
        sleep 60
    done
    return 0
}
# --- end convert gate ---

# In forward order the window's oldest hour comes first, so the state before it is
# fetched now rather than at the close -- or that hour would wait the whole chain.
if [ "${DIRECTION}" = "forward" ] && [ "${CURRENT_DT}" = "${START_DT}" ] && [ "${DRY_RUN}" != "1" ]; then
    fetch_edge_state
fi

# Hours left waiting by an earlier process of this chain (snapshot or queue).
if [ "${DOWNLOAD_ONLY}" != "1" ] && [ "${DRY_RUN}" != "1" ]; then
    drain_pending > /dev/null || true
fi

processed=0
running=0
budget_hit=0
while [ "$processed" -lt "$BATCH_SIZE" ] && within_window "$CUR_EPOCH"; do
    if [ "$(( $(date +%s) - DRIVER_START ))" -ge "$DRIVER_MAX_SECONDS" ]; then
        echo "Time budget (${DRIVER_MAX_SECONDS}s) reached; will respawn for the rest of the window."
        budget_hit=1
        break
    fi

    d=$(TZ=UTC date -d "@${CUR_EPOCH}" +%Y-%m-%d)
    h=$(TZ=UTC date -d "@${CUR_EPOCH}" +%H)
    dt="${d}T${h}"

    if stop_requested; then
        echo "STOP flag present (${STOP_FLAG}); stopping batch before ${dt}."
        break
    fi

    if [ -n "${SKIP_SET[$dt]:-}" ]; then
        echo "  [${dt}] on skip-list (source OFFLINE / not recalled), skipping."
        log_status "$dt" "SKIP_OFFLINE" "on paths.skip_list; source unavailable (recall on LRZ then re-run)"
    elif done_tag=$(already_done "$d" "$h"); then
        case "$done_tag" in
            SKIP_RAW_EXISTS) echo "  [${dt}] wrfout already staged, skipping." ;;
            *)               echo "  [${dt}] GRIB already exists, skipping." ;;
        esac
        log_status "$dt" "$done_tag" ""
        if [ "${DRY_RUN}" != "1" ]; then
            if [ "$done_tag" = "SKIP_RAW_EXISTS" ]; then
                # Staged before snapshots existed, or by a chain that was stopped.
                ensure_archive_snapshot "$d" "$h" || true
                [ "$h" = "00" ] && { ensure_dayend "$d" || true; }
            elif next_needs_snapshot "$d" "$h"; then
                snapshot_only "$d" "$h" &
                running=$((running + 1))
                if [ "$running" -ge "$FETCH_PARALLEL" ]; then wait -n || true; running=$((running - 1)); fi
            fi
        fi
    elif [ "${DRY_RUN}" = "1" ] || [ "${FETCH_PARALLEL}" -le 1 ]; then
        grc=0; gate_wait "$dt" || grc=$?
        [ "$grc" -eq 2 ] && { budget_hit=1; break; }
        [ "$grc" -ne 0 ] && break
        process_one "$d" "$h" || true
    else
        grc=0; gate_wait "$dt" || grc=$?
        [ "$grc" -eq 2 ] && { budget_hit=1; break; }
        [ "$grc" -ne 0 ] && break
        process_one "$d" "$h" &
        running=$((running + 1))
        if [ "$running" -ge "$FETCH_PARALLEL" ]; then
            wait -n || true
            running=$((running - 1))
        fi
    fi

    CUR_EPOCH=$((CUR_EPOCH + STEP))
    processed=$((processed + 1))
done

# Wait for any in-flight background fetch+convert dispatches
wait || true
if [ "${DOWNLOAD_ONLY}" != "1" ] && [ "${DRY_RUN}" != "1" ]; then
    drain_pending > /dev/null || true
fi

# Re-spawn for the next timestep if the window is not exhausted
if within_window "$CUR_EPOCH"; then
    NEXT_DT=$(TZ=UTC date -d "@${CUR_EPOCH}" +%Y-%m-%dT%H)
    echo ""
    [ "$budget_hit" -eq 1 ] && echo "Batch stopped on time budget." || echo "Batch done (${processed} timesteps)."
    echo "Continuing from ${NEXT_DT} (${DIRECTION})..."
    respawn "${NEXT_DT}"
else
    echo ""
    echo "Window complete (reached ${DIRECTION} edge). Closing it, then no further respawn."
    close_window
    wait || true
fi
