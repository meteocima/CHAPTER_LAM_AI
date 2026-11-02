#!/bin/bash
#
# Detached sequence that rebuilds the CHAPTER archive in GRIB2 (246 messages) for the
# hours whose wrfout are NOT on local disk: 17 068 timesteps over 2019 (full year),
# 2024 (full year) and 2025 (01-01..07-02 -- the source stops on 07-02T23, measured). Each one is fetched from the LRZ relay,
# converted, and its wrfout deleted as soon as the GRIB exists.
#
# Companion of hpc/run_share_conversion.sh, which converts the 4392 hours already
# staged in wrfout_share/ and wrfout_2024fill/ and never deletes them. The two run in
# parallel: this one is datamover-bound, that one is CPU-bound, and they only meet in
# the conv_* queue gate. The PHASES below are the exact complement of what that script
# covers, so nothing is fetched twice:
#
#   on disk (run_share_conversion): 2019-06-17..09-06, 2024-02-01..02-17, 2024-03-18..03-31,
#                                   2024-06-18..09-12, plus 2024-03-15T04..03-17T23
#   here:                           everything else in 2019, 2024 and 2025 up to 07-02
#
# Keep that complement exact. The download chain is re-entrant on the STAGED WRFOUT, not
# on the GRIB (SKIP_RAW_EXISTS), so a phase that overlaps hours already converted and
# whose wrfout are gone will fetch them again in full -- 9.14 GB each, over the relay.
# Two phases were trimmed on 2026-10-01 for exactly that reason, after the 4800 hours of
# 2026-09-29 landed: r24_02 lost 2024-02-01..17 and r24_03 now stops at 2024-03-15T03, because 03-15T04..03-17T23 are staged in
# wrfout_rebuild while 03-15T00..03Z are not: those four hours are the only part of that
# day the relay still has to supply, and trimming to 03-14T23 would have orphaned them.
#
# Why phases: a year of wrfout is ~80 TB against a 100 TB quota. The window is cut into
# ~monthly phases and, as soon as a phase finishes downloading, its conversion starts IN
# THE BACKGROUND while the next phase downloads. The convert chain only sees local files,
# so it never competes for the datamover. With KEEP_WRFOUT=false each converted wrfout is
# deleted at once, so at most ~2 phases sit on disk (~14 TB).
#
# Per phase:
#   1. wait until the project quota is below QUOTA_STOP_TB
#   2. launch a DOWNLOAD-ONLY chain (no convert, wrfout kept) and wait for "Window complete"
#   3. launch the CONVERT chain for that same phase and DO NOT wait for it
# At the end: wait for every convert chain, drain the queue, write the per-phase reports
# and submit one check_grib_sanity job over every month touched.
#
# RUN ON A REGULAR LOGIN NODE:  bash hpc/run_year_rebuild.sh
# Other years, one phase per month:  YEARS="2020 2021 2022 2023" bash hpc/run_year_rebuild.sh
# It snapshots itself and re-execs detached (setsid), so the terminal / chat can be closed
# and edits to the repo copy do not touch the running sequence. Re-entrant: re-running
# skips staged wrfout (download) and existing GRIBs (convert).
# Stop: touch ${W}/logs/rebuild_sequence.stop  (plus the per-chain
# rebuild_<label>_{dl,cv}.stop to stop a driver itself).
# The Cold Copy beside the GRIB (#73, ADR-0001), from 2018 back:
#   COLD_COPY=true YEARS="2018" bash hpc/run_year_rebuild.sh
# Each wrfout is fetched once and feeds both. Both chains then keep what the Cold Copy
# reads (pipeline.cold_copy) and the convert chain deletes nothing (KEEP_WRFOUT forced
# true). As soon as a phase is downloaded, a SLURM array writes its days, one task per
# day, through CHAPTER_INHOUSE's Ingest (hpc/cold_copy_day.py, cold-copy-day from the
# clone pinned in COLD_COPY_DAY), beside the phase's converts. A sweep, before every
# phase and at every quota poll, deletes each wrfout the archive and the Cold Copy are done with: the
# Ingest releases it and its GRIB is written. Ledger: logs/cold_copy_status.log.
# A trial, or any odd window: PHASES_SPEC="label sd sh ed eh;label sd sh ed eh"
# replaces the phase table (e.g. the two days either side of a month boundary).
#
# Resume after a stop: PHASES_ONLY="<labels>" restricts the run to the phases still to
# do. Since 2026-10-21 the download side also skips an hour whose GRIB exists, so a
# finished phase is no longer fetched again in full; PHASES_ONLY spares walking it.

set -uo pipefail

PROJECT_DIR="${PROJECT_DIR:-/leonardo/home/userexternal/lmonaco0/CHAPTER}"
W="${W:-/leonardo_work/AIFPT_AILAMIT/CHAPTER}"
LOG_DIR="${W}/logs"
STAGING_DIR="${STAGING_DIR:-${W}/wrfout_rebuild}"   # this sequence's own staging slot;
                                                    # KEEP_WRFOUT decides if its wrfout survive
SEQ_LOG="${LOG_DIR}/rebuild_sequence.log"
SEQ_STOP="${LOG_DIR}/rebuild_sequence.stop"
UV="${UV:-${HOME}/.local/bin/uv}"
MAX_QUEUED=48          # convert chain: batch.size and batch.max_queued_converts
# Concurrent sftp streams through the datamover. The knee is at 6 and the relay's
# aggregate ceiling is ~370 MB/s, both measured on 2026-10-06 (#69): 3 streams give
# 187 MB/s (62.4 each), 4 give 244 (61.1), 6 give 359 (59.8), 8 give only 374 -- and at
# 8 every stream measures 46.8 to the decimal, which is an aggregate cap being shared
# equally rather than independent channels. Up to 6 the bottleneck is the single sftp
# channel, so each stream added brings new bandwidth; past it there is nothing left to
# win, only load on a datamover other projects share. Dropping back to 6 restored
# 57.2 per stream, which is how we know the ceiling was ours and not someone else's
# traffic. 6 takes 95% of it.
FETCH_PARALLEL="${FETCH_PARALLEL:-6}"
case "$FETCH_PARALLEL" in
    *[!0-9]*) echo "FETCH_PARALLEL must be a whole number, got '${FETCH_PARALLEL}'" >&2; exit 2 ;;
esac
# 8 is both the highest value ever measured and already past the knee, so refusing more
# costs nothing real. Re-measure before raising this bound, and move #69 with it.
if [ "$FETCH_PARALLEL" -lt 1 ] || [ "$FETCH_PARALLEL" -gt 8 ]; then
    echo "FETCH_PARALLEL must be 1..8: 6 is the measured knee and 8 the highest value measured (#69); got ${FETCH_PARALLEL}" >&2
    exit 2
fi
if [ "$FETCH_PARALLEL" -gt 6 ]; then
    echo "WARNING: FETCH_PARALLEL=${FETCH_PARALLEL} is past the measured knee of 6; it adds load on the shared datamover for no measured gain (#69)" >&2
fi
DEAD_MINUTES=60        # a driver log silent this long without completing is dead
POLL_SECONDS=300
PROJECT_QUOTA_ID=20148120        # lfs project id of /leonardo_work/AIFPT_AILAMIT
QUOTA_STOP_TB=85                 # hold new downloads above this
SANITY_ACCOUNT=aifpt_ailamit_0
# Delete each staged wrfout once its GRIB is in place. The schema is closed at 246
# messages, so there is no longer a reason to keep them, and it is the only way this
# campaign fits in the quota. convert_step.sh still refuses to delete a wrfout whose
# accumulator snapshot is missing while the next hour needs it (#71).
KEEP_WRFOUT="${KEEP_WRFOUT:-false}"
# Restrict the run to these phase labels (space separated). Empty = all.
PHASES_ONLY="${PHASES_ONLY:-}"
# The Cold Copy beside the GRIB (#73): see the header.
COLD_COPY="${COLD_COPY:-false}"
COLD_COPY_DIR="${COLD_COPY_DIR:-${W}/cold_copy}"
# cold-copy-day of the CHAPTER_INHOUSE clone pinned to a tag (ingest-2018-v2), its venv
# built once without the dev group: never the development checkout, which is live code.
COLD_COPY_DAY="${COLD_COPY_DAY:-${W}/cold_copy_src/cold_copy/.venv/bin/cold-copy-day}"
# One day of the Cold Copy on one core (DCGP bills per core, RAM is free). Memory,
# measured: 64G was killed on all four days of the trial (OUT_OF_MEMORY, MaxRSS 66.9 GB,
# 2026-11-01), on the first 3D variable; one 3D variable over 24 Valid Times alone
# peaks at 70.5 GB (74.1 GB MaxRSS), the float64 copies of the Ingest's 16-bit packing
# (job 63155174, synthetic 24x49x1641x1353). PH and W have 50 levels, so 128G leaves
# ~50% above it. Measured on the trial's rerun (2026-11-02, jobs 63155691 and 63156557,
# 2018-01-30..02-02): MaxRSS 75.98 GB on every day, 4:08 to 5:00 wall, so 8 h leaves
# ~60%. A day writes 21.9 GB (3D 19.3, surface 2.6-2.7), 2018 about 8 TB.
CC_ACCOUNT="${CC_ACCOUNT:-aifpt_ailamit_0}"
CC_MEM="${CC_MEM:-128G}"
CC_TIME="${CC_TIME:-08:00:00}"
PHASES_SPEC="${PHASES_SPEC:-}"
export KEEP_WRFOUT PHASES_ONLY FETCH_PARALLEL COLD_COPY COLD_COPY_DIR COLD_COPY_DAY CC_ACCOUNT CC_MEM \
       CC_TIME PHASES_SPEC

# label  start_date start_hour  end_date end_hour
# The first phase is a 72 h shakedown: an end-to-end failure shows up in ~2 h instead of
# after a full month. It is a real slice of 2019-09, not a duplicate of any other phase.
PHASES=(
    "r19_09a 2019-09-07 0 2019-09-09 23"
    "r24_01  2024-01-01 0 2024-01-31 23"
    "r24_02  2024-02-18 0 2024-02-29 23"
    "r24_03  2024-03-01 0 2024-03-15 3"
    "r24_04  2024-04-01 0 2024-04-30 23"
    "r24_05  2024-05-01 0 2024-05-31 23"
    "r24_06  2024-06-01 0 2024-06-17 23"
    "r24_09  2024-09-13 0 2024-09-30 23"
    "r24_10  2024-10-01 0 2024-10-31 23"
    "r24_11  2024-11-01 0 2024-11-30 23"
    "r24_12  2024-12-01 0 2024-12-31 23"
    "r19_01  2019-01-01 0 2019-01-31 23"
    "r19_02  2019-02-01 0 2019-02-28 23"
    "r19_03  2019-03-01 0 2019-03-31 23"
    "r19_04  2019-04-01 0 2019-04-30 23"
    "r19_05  2019-05-01 0 2019-05-31 23"
    "r19_06  2019-06-01 0 2019-06-16 23"
    "r19_09b 2019-09-10 0 2019-09-30 23"
    "r19_10  2019-10-01 0 2019-10-31 23"
    "r19_11  2019-11-01 0 2019-11-30 23"
    "r19_12  2019-12-01 0 2019-12-31 23"
    "r25_01  2025-01-01 0 2025-01-31 23"
    "r25_02  2025-02-01 0 2025-02-28 23"
    "r25_03  2025-03-01 0 2025-03-31 23"
    "r25_04  2025-04-01 0 2025-04-30 23"
    "r25_05  2025-05-01 0 2025-05-31 23"
    "r25_06  2025-06-01 0 2025-06-30 23"
    "r25_07  2025-07-01 0 2025-07-02 23"
)

# YEARS="2020 2021 ...": replace the table above with one phase per calendar month of
# those years, labelled r20_01 .. r23_12 -- the shape every 2019/2025 phase already had.
# Unset, the table above runs as it always did.
YEARS="${YEARS:-}"
export YEARS
if [ -n "$YEARS" ]; then
    PHASES=()
    for y in $YEARS; do
        for m in 01 02 03 04 05 06 07 08 09 10 11 12; do
            last=$(TZ=UTC date -d "${y}-${m}-01 +1 month -1 day" +%d)
            PHASES+=("r${y:2:2}_${m} ${y}-${m}-01 0 ${y}-${m}-${last} 23")
        done
    done
fi

if [ -n "$PHASES_SPEC" ]; then
    PHASES=()
    IFS=';' read -r -a _specs <<<"$PHASES_SPEC"
    for s in "${_specs[@]}"; do PHASES+=("$s"); done
fi

# ---- self-detach from a snapshot --------------------------------------------
if [ -z "${SEQ_DETACHED:-}" ]; then
    mkdir -p "$LOG_DIR"
    snap="${LOG_DIR}/.rebuild_sequence_$(date +%Y%m%d%H%M%S).sh"
    cp "$0" "${snap}.tmp" && mv "${snap}.tmp" "$snap"
    SEQ_DETACHED=1 setsid bash "$snap" >> "$SEQ_LOG" 2>&1 < /dev/null &
    echo "Sequence detached on $(hostname) (pid $!), snapshot ${snap}"
    echo "Log: ${SEQ_LOG}    Stop: touch ${SEQ_STOP}"
    exit 0
fi

log() { echo "$(date -u +%FT%TZ) | $*" >&2; }

check_stop() {
    if [ -e "$SEQ_STOP" ]; then
        log "STOPPED | ${SEQ_STOP} present; exiting."
        exit 0
    fi
}

queued_converts() {
    local out
    out=$(timeout 60 squeue -h -u "${USER}" -o %j 2>/dev/null) || return 1
    printf '%s\n' "$out" | awk '/^conv_/ {n++} END {print n+0}'
}

# Project usage in TB, or empty if lfs did not answer (never guess: a missing
# reading must not be read as "plenty of room").
used_tb() {
    timeout 60 lfs quota -p "$PROJECT_QUOTA_ID" /leonardo_work 2>/dev/null \
        | awk '/leonardo_work/ {gsub(/\*/,"",$2); printf "%.2f", $2/1024/1024/1024}'
}

# ---- the Cold Copy (#73) ---------------------------------------------------
CC_STATUS_LOG="${LOG_DIR}/cold_copy_status.log"
CC_LOST="${LOG_DIR}/cold_copy_lost.json"
# The campaign's first and last day, over the whole phase table (not PHASES_ONLY): the
# days whose Cold Copy it delivers. The state before the first 00Z is also read by the
# day before, and 23Z of the last day by the day after; neither is this campaign's to
# write (the day after the last is the Pass's, which fetches its own), so the sweep
# does not wait for them.
CC_FIRST_DAY=$(printf '%s\n' "${PHASES[@]}" | awk '{print $2}' | sort | head -n 1)
CC_LAST_DAY=$(printf '%s\n' "${PHASES[@]}" | awk '{print $4}' | sort | tail -n 1)
# The GRIB path of any hour, as a strftime pattern: convert_step.sh's GRIB_PATTERN.
GRIB_PATTERN="${W}/grib_v3/%Y/%m/ailam-an-cima-3km-%Y-%Y-1h-v1-%Y%m%d%H.grib"

# One array task per day of the phase [$2, $3], each writing its day of the Cold Copy
# from the staged wrfout. A day still missing wrfout is CC_INCOMPLETE in the ledger,
# not a failed task; a re-run delivers it, and finds the others delivered already.
cc_submit_array() {
    local label="$1" sd="$2" ed="$3" s0 n jid
    s0=$(TZ=UTC date -d "$sd" +%s)
    n=$(( ( $(TZ=UTC date -d "$ed" +%s) - s0 ) / 86400 + 1 ))
    jid=$(sbatch --parsable --partition dcgp_usr_prod --account "$CC_ACCOUNT" \
        --nodes 1 --ntasks 1 --cpus-per-task 1 --mem "$CC_MEM" --time "$CC_TIME" \
        --array "0-$((n - 1))" --job-name "cc_${label}" \
        --output "${LOG_DIR}/cold_copy_${label}_%A_%a.out" \
        --wrap "cd ${PROJECT_DIR}
day=\$(TZ=UTC date -d @\$(( ${s0} + SLURM_ARRAY_TASK_ID * 86400 )) +%F)
export COLD_COPY_DAY=${COLD_COPY_DAY}
/usr/bin/time -v ${UV} run python hpc/cold_copy_day.py write \$day --wrfout-dir ${STAGING_DIR} \
    --out ${COLD_COPY_DIR} --status-log ${CC_STATUS_LOG} --lost ${CC_LOST}")
    log "CC_SUBMITTED | ${label}: array ${jid:-FAILED}, ${n} day(s) ${sd}..${ed} -> ${LOG_DIR}/cold_copy_${label}_<job>_<task>.out"
}

queued_cold_copy() {
    local out
    out=$(timeout 60 squeue -h -u "${USER}" -o %j 2>/dev/null) || return 1
    printf '%s\n' "$out" | awk '/^cc_/ {n++} END {print n+0}'
}

# Delete every staged wrfout the archive and the Cold Copy are done with. Idempotent, cheap (stats
# and one cold-copy-day released), so it runs before every phase and at every quota
# poll: with KEEP_WRFOUT forced true it is the only thing that frees space.
cc_sweep() {
    [ "$COLD_COPY" = "true" ] || return 0
    local before after
    before=$(grep -c CC_WRFOUT_DELETED "$CC_STATUS_LOG" 2>/dev/null); before=${before:-0}
    if ! COLD_COPY_DAY="$COLD_COPY_DAY" timeout 1800 "$UV" run python hpc/cold_copy_day.py sweep \
            --wrfout-dir "$STAGING_DIR" --out "$COLD_COPY_DIR" --status-log "$CC_STATUS_LOG" \
            --grib-pattern "$GRIB_PATTERN" --snap-dir "${W}/accum_snap" --lost "$CC_LOST" \
            --span "$CC_FIRST_DAY" "$CC_LAST_DAY" >&2; then
        log "CC_SWEEP_FAILED | the sweep exited non-zero: nothing is lost, the next one retries"
        return 0
    fi
    after=$(grep -c CC_WRFOUT_DELETED "$CC_STATUS_LOG" 2>/dev/null); after=${after:-0}
    log "CC_SWEEP | $((after - before)) wrfout deleted, $(find "${STAGING_DIR}" "${STAGING_DIR%/}_spinup" -name 'wrfout_d02_*' -type f 2>/dev/null | wc -l) left in staging"
}

# Hold here while the quota is above the threshold: the convert chain of the previous
# phase is deleting wrfout as it goes, so this resolves itself instead of aborting.
wait_for_quota() {
    local label="$1" tb warned=0
    while :; do
        check_stop
        tb=$(used_tb)
        if [ -z "$tb" ]; then
            log "QUOTA_UNKNOWN | ${label}: lfs quota did not answer; waiting ${POLL_SECONDS}s"
            sleep "$POLL_SECONDS"; continue
        fi
        if awk -v u="$tb" -v m="$QUOTA_STOP_TB" 'BEGIN{exit !(u < m)}'; then
            log "QUOTA_OK | ${label}: ${tb} TB used (< ${QUOTA_STOP_TB} TB)"
            return 0
        fi
        cc_sweep
        if [ "$warned" -eq 0 ]; then
            if [ "$COLD_COPY" = "true" ]; then
                log "QUOTA_HOLD | ${label}: ${tb} TB used >= ${QUOTA_STOP_TB} TB; waiting for the Cold Copy's days and the converts, after which the sweep frees space"
            elif [ "$KEEP_WRFOUT" = "true" ]; then
                log "QUOTA_HOLD | ${label}: ${tb} TB used >= ${QUOTA_STOP_TB} TB and KEEP_WRFOUT=true, so nothing will free space on its own: move or delete data, or raise QUOTA_STOP_TB"
            else
                log "QUOTA_HOLD | ${label}: ${tb} TB used >= ${QUOTA_STOP_TB} TB; waiting for converts to free space"
            fi
        fi
        warned=1
        sleep "$POLL_SECONDS"
    done
}

dl_args() {
    local label="$1" sd="$2" sh="$3" ed="$4" eh="$5"
    echo "window.start_date=${sd} window.start_hour=${sh} window.end_date=${ed} window.end_hour=${eh}" \
         "pipeline.download_only=true paths.wrfout_dir=${STAGING_DIR}" \
         "pipeline.cold_copy=${COLD_COPY} paths.cold_copy_dir=${COLD_COPY_DIR}" \
         "batch.fetch_parallel=${FETCH_PARALLEL} batch.size=${MAX_QUEUED} batch.max_queued_converts=0" \
         "paths.status_log=${LOG_DIR}/rebuild_${label}_dl_status.log" \
         "paths.driver_log=${LOG_DIR}/rebuild_${label}_dl_driver.log" \
         "paths.stop_flag=${LOG_DIR}/rebuild_${label}_dl.stop"
}

cv_args() {
    local label="$1" sd="$2" sh="$3" ed="$4" eh="$5"
    echo "window.start_date=${sd} window.start_hour=${sh} window.end_date=${ed} window.end_hour=${eh}" \
         "paths.wrfout_dir=${STAGING_DIR} pipeline.keep_wrfout=${KEEP_WRFOUT}" \
         "pipeline.cold_copy=${COLD_COPY} paths.cold_copy_dir=${COLD_COPY_DIR}" \
         "batch.fetch_parallel=${FETCH_PARALLEL} batch.size=${MAX_QUEUED} batch.max_queued_converts=${MAX_QUEUED}" \
         "paths.status_log=${LOG_DIR}/rebuild_${label}_cv_status.log" \
         "paths.driver_log=${LOG_DIR}/rebuild_${label}_cv_driver.log" \
         "paths.stop_flag=${LOG_DIR}/rebuild_${label}_cv.stop"
}

# Launch a chain unless one is already alive on that driver log. Echoes the byte offset
# from which the driver log belongs to this run (1 = an existing chain we are adopting).
launch_chain() {
    local kind="$1" label="$2" dlog="$3"; shift 3
    local offset alive=""
    # sample freshness before touching, otherwise our own touch makes a stale log look alive
    [ -f "$dlog" ] && alive=$(find "$dlog" -mmin -25 -size +0)
    touch "$dlog"
    offset=$(( $(stat -c%s "$dlog") + 1 ))
    if [ -n "$alive" ] && ! tail -n 3 "$dlog" | grep -q "Window complete\|STOP flag"; then
        log "WAIT | ${label} ${kind}: a chain is already alive (driver log fresh); adopting it"
        echo 1; return 0
    fi
    log "LAUNCH | ${label} ${kind}"
    if ! "$UV" run python hpc/submit_step_pipeline.py "$@" >&2; then
        log "FATAL | ${label} ${kind}: launcher failed"
        echo ""; return 1
    fi
    echo "$offset"
}

# Poll a driver log until it reports the window done. 0 = complete, 1 = dead, 2 = stopped.
wait_chain() {
    local kind="$1" label="$2" dlog="$3" offset="$4"
    while :; do
        sleep "$POLL_SECONDS"
        check_stop
        if tail -c "+${offset}" "$dlog" | grep -q "Window complete"; then
            log "WINDOW_COMPLETE | ${label} ${kind}"
            return 0
        fi
        if tail -c "+${offset}" "$dlog" | grep -q "STOP flag present"; then
            log "STOPPED | ${label} ${kind}: driver stopped by its stop flag"
            return 2
        fi
        if [ -z "$(find "$dlog" -mmin "-${DEAD_MINUTES}")" ]; then
            log "CHAIN_DEAD | ${label} ${kind}: driver log silent > ${DEAD_MINUTES} min without Window complete"
            return 1
        fi
    done
}

# The staging slot belongs to this campaign alone: never a shared tree, never
# another campaign's slot. With KEEP_WRFOUT=false its wrfout are deleted as they
# convert, so pointing it at one of those would destroy someone else's data.
case "$STAGING_DIR" in
    */wrfout|*/wrfout_share|*/wrfout_2024fill)
        log "FATAL | STAGING_DIR must be this sequence's own staging slot, not ${STAGING_DIR}"; exit 1 ;;
esac

if [ "$COLD_COPY" = "true" ]; then
    # The sweep deletes, not convert_step.sh: a wrfout goes only once the archive
    # and the Cold Copy are done with it.
    KEEP_WRFOUT=true
fi
log "START | sequence on $(hostname), pid $$, staging ${STAGING_DIR}, keep_wrfout=${KEEP_WRFOUT}, cold_copy=${COLD_COPY}"
cd "$PROJECT_DIR" || { log "FATAL | cannot cd ${PROJECT_DIR}"; exit 1; }
mkdir -p "$STAGING_DIR"
if [ "$COLD_COPY" = "true" ]; then
    if ! [ -x "$COLD_COPY_DAY" ]; then
        log "FATAL | COLD_COPY_DAY=${COLD_COPY_DAY} is not an executable: build the pinned clone first"
        exit 1
    fi
    mkdir -p "$COLD_COPY_DIR"
    # The wrfout verified lost on LRZ (pipeline.lost_wrfouts), read once for the whole
    # sequence: an entry added later reaches it on a relaunch.
    if ! "$UV" run python -c "import json; from omegaconf import OmegaConf
c = OmegaConf.to_container(OmegaConf.load('conf/pipeline.yaml').pipeline)
print(json.dumps(c.get('lost_wrfouts') or []))" > "$CC_LOST"; then
        log "FATAL | cannot read pipeline.lost_wrfouts from conf/pipeline.yaml"
        exit 1
    fi
    log "CC_START | Cold Copy into ${COLD_COPY_DIR}, $(grep -o '"run"' "$CC_LOST" | wc -l) wrfout declared lost, ingest ${COLD_COPY_DAY}"
fi

CV_PENDING=()   # "label sd sh ed eh offset" of the convert chains still to be waited on
MONTHS=""       # distinct YYYY-MM touched, for the final sanity job

for ph in "${PHASES[@]}"; do
    read -r label sd sh ed eh <<<"$ph"
    check_stop
    if [ -n "$PHASES_ONLY" ] && ! printf '%s\n' $PHASES_ONLY | grep -qx "$label"; then
        log "SKIP_PHASE | ${label}: not in PHASES_ONLY"
        continue
    fi
    case ",${MONTHS}," in *",${sd:0:7},"*) ;; *) MONTHS="${MONTHS:+${MONTHS},}${sd:0:7}" ;; esac
    cc_sweep
    wait_for_quota "$label"

    dl_log="${LOG_DIR}/rebuild_${label}_dl_driver.log"
    # shellcheck disable=SC2046
    dargs=( $(dl_args "$label" "$sd" "$sh" "$ed" "$eh") )
    if ! off=$(launch_chain download "$label" "$dl_log" "${dargs[@]}") || [ -z "$off" ]; then
        log "FATAL | ${label}: download launcher failed; exiting (re-run this script, it is re-entrant)"
        exit 1
    fi
    wait_chain download "$label" "$dl_log" "$off"; rc=$?
    [ "$rc" -eq 2 ] && exit 0
    if [ "$rc" -ne 0 ]; then
        log "FATAL | ${label}: download chain died; exiting (re-run this script, it is re-entrant)"
        exit 1
    fi
    log "STAGED | ${label}: $(find "${STAGING_DIR}" -name 'wrfout_d02_*' -type f | wc -l) wrfout on disk, $(used_tb) TB used"
    # Every wrfout the phase's days read is local now: the month's hours, the spin-up
    # 00Z of each day and the state before the window. The days need no GRIB.
    [ "$COLD_COPY" = "true" ] && cc_submit_array "$label" "$sd" "$ed"

    # Convert this phase in the background (local files only, no datamover) while the
    # next phase downloads. Its wrfout are deleted one by one as the GRIBs appear.
    cv_log="${LOG_DIR}/rebuild_${label}_cv_driver.log"
    # shellcheck disable=SC2046
    cargs=( $(cv_args "$label" "$sd" "$sh" "$ed" "$eh") )
    if ! off=$(launch_chain convert "$label" "$cv_log" "${cargs[@]}") || [ -z "$off" ]; then
        log "FATAL | ${label}: convert launcher failed; exiting (re-run this script, it is re-entrant)"
        exit 1
    fi
    CV_PENDING+=("${label} ${sd} ${sh} ${ed} ${eh} ${off}")
done

log "ALL_DOWNLOADS_DONE | waiting for ${#CV_PENDING[@]} convert chain(s)"

for pend in "${CV_PENDING[@]}"; do
    read -r label sd sh ed eh off <<<"$pend"
    cv_log="${LOG_DIR}/rebuild_${label}_cv_driver.log"
    wait_chain convert "$label" "$cv_log" "$off"; rc=$?
    [ "$rc" -eq 2 ] && exit 0
    [ "$rc" -ne 0 ] && log "WARN | ${label} convert: chain died; its report below will show what is missing"
done

while :; do
    check_stop
    if nq=$(queued_converts) && [ "$nq" -eq 0 ]; then break; fi
    sleep "$POLL_SECONDS"
done
log "QUEUE_EMPTY | all converts left the queue"

if [ "$COLD_COPY" = "true" ]; then
    while :; do
        check_stop
        if nq=$(queued_cold_copy) && [ "$nq" -eq 0 ]; then break; fi
        sleep "$POLL_SECONDS"
    done
    log "CC_QUEUE_EMPTY | every Cold Copy array left the queue"
    cc_sweep
fi

# Phases whose report came back short. The sanity job below still runs -- knowing the
# archive is clean is useful even when it is incomplete -- but the run must not end in DONE.
INCOMPLETE=0

for pend in "${CV_PENDING[@]}"; do
    read -r label sd sh ed eh off <<<"$pend"
    # shellcheck disable=SC2046
    cargs=( $(cv_args "$label" "$sd" "$sh" "$ed" "$eh") )
    rep="${LOG_DIR}/rebuild_${label}_report.txt"
    # report=true exits non-zero when the window is not complete (#68). Before that,
    # this loop logged "0 done, 72 pending" and the run still ended in DONE.
    if "$UV" run python hpc/submit_step_pipeline.py "${cargs[@]}" report=true > "$rep" 2>&1; then
        log "REPORT | ${label}: $(grep '^# summary' "$rep")"
    else
        log "PHASE_INCOMPLETE | ${label}: $(grep '^# summary' "$rep")  -- see ${rep}"
        INCOMPLETE=$((INCOMPLETE + 1))
    fi
done
if [ "$COLD_COPY" = "true" ]; then
    # A day is done when its checksum file is there (cold-copy-day): count them per
    # phase, and name the days missing, with their last ledger line.
    for pend in "${CV_PENDING[@]}"; do
        read -r label sd sh ed eh off <<<"$pend"
        s0=$(TZ=UTC date -d "$sd" +%s); e0=$(TZ=UTC date -d "$ed" +%s)
        done_days=0; lost_days=0; missing=""
        for (( t = s0; t <= e0; t += 86400 )); do
            day=$(TZ=UTC date -d "@$t" +%F)
            last=$(grep " | ${day} | CC_" "$CC_STATUS_LOG" 2>/dev/null | tail -n 1 | cut -d'|' -f3 | tr -d ' ')
            if [ -f "${COLD_COPY_DIR}/_checksums/${day}.sha256" ]; then
                done_days=$((done_days + 1))
            elif [ "$last" = "CC_WHOLLY_LOST" ]; then
                lost_days=$((lost_days + 1))     # every wrfout declared lost: by decision
            else
                missing="${missing} ${day}:${last:-never tried}"
            fi
        done
        if [ -z "$missing" ]; then
            log "CC_REPORT | ${label}: ${done_days} day(s) delivered, ${lost_days} lost whole"
        else
            log "CC_INCOMPLETE | ${label}: ${done_days} day(s) delivered, missing:${missing}"
            INCOMPLETE=$((INCOMPLETE + 1))
        fi
    done
fi
for y in $(printf '%s\n' ${MONTHS//,/ } | cut -c1-4 | sort -u); do
    log "GRIB_COUNT | ${y}: $(find "${W}/grib_v3/${y}" -name '*.grib' 2>/dev/null | wc -l)"
done
log "STAGING_LEFT | $(find "${STAGING_DIR}" -name 'wrfout_d02_*' -type f | wc -l) wrfout still in ${STAGING_DIR}, $(used_tb) TB used"

# One array task per month: a single job reads ~1 200 files an hour, so 48 months
# (~35 000 files) would outlast any wall time. Each task checks its own month.
months_list="${MONTHS//,/ }"
n_months=$(printf '%s\n' $months_list | wc -l)
month_args=" --month \$(echo ${months_list} | cut -d' ' -f\$((SLURM_ARRAY_TASK_ID + 1)))"
jid=$(sbatch --parsable --partition dcgp_usr_prod --account "$SANITY_ACCOUNT" \
    --nodes 1 --ntasks 1 --cpus-per-task 1 --mem 8G --time 04:00:00 \
    --array "0-$((n_months - 1))" \
    --job-name "sanity_rebuild" --output "${LOG_DIR}/rebuild_sanity_%A_%a.out" \
    --wrap "cd ${PROJECT_DIR}
module load eccodes/2.34.0--gcc--12.2.0 2>/dev/null
GCC12_RT=/leonardo/prod/spack/06/install/0.22/linux-rhel8-icelake/gcc-12.2.0/gcc-runtime-12.2.0-dqfwf7yjtbtdzllj66jx6suk34ir2ct3/lib
ECCODES_LIB=/leonardo/prod/spack/06/install/0.22/linux-rhel8-icelake/gcc-12.2.0/eccodes-2.34.0-msheephhj7zirdzmqcfdrf4jat5w545r/lib64
export LD_PRELOAD=\$GCC12_RT/libstdc++.so.6
export LD_LIBRARY_PATH=\$GCC12_RT:\$ECCODES_LIB:\${LD_LIBRARY_PATH:-}
${UV} run python hpc/check_grib_sanity.py${month_args}")
log "SANITY_SUBMITTED | array job ${jid:-FAILED} (${n_months} months) -> ${LOG_DIR}/rebuild_sanity_${jid}_<task>.out"

if [ "$INCOMPLETE" -gt 0 ]; then
    log "INCOMPLETE | ${INCOMPLETE} phase(s) ended short; NOT reporting DONE. Re-run this"
    log "INCOMPLETE | script (re-entrant) or the affected phase before starting another tranche."
    exit 1
fi
log "DONE | all phases processed"
