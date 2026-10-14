#!/bin/bash
# Re-convert the 00Z timesteps already in grib_v3 from the run for the day before
# (issue #72), no other hour touched.
#
# Until #72 the 00Z file of day D took its instantaneous fields from the run for D,
# 6 h into its spin-up, and its accumulations (the hour 23Z -> 00Z) from the run for
# D-1. Since #72 the whole timestep is the 24 h file of the run for D-1. Per day:
#   fetch that file (datamover, into STAGE) -> sbatch hpc/fix_00z_convert.sh, which
#   converts it copying the 19 accumulated messages of the old file byte for byte
#   (they are already right, and the 23Z state they came from is gone), checks the
#   result, renames it over the old file and deletes the wrfout.
#
# LOGIN NODE ONLY: the datamover is reachable from the regular login nodes. The
# transfer runs on the datamover, so this process sits at ~0 s CPU.
#
# Which days: the 00Z GRIBs older than CUTOFF, a file touched just before the
# chains were relaunched with the #72 driver -- everything newer was written
# from the 24 h file already. The list is made once, at the first launch, and kept.
#
# Usage (detached):
#   touch $W/logs/fix_00z_run.cutoff        # once, BEFORE relaunching the chains
#   setsid nohup hpc/fix_00z_run.sh > $W/logs/fix_00z_run_driver.log 2>&1 < /dev/null &
# Stop:   touch $W/logs/fix_00z_run.stop    (finishes the transfers in flight)
# Re-entrant: a day logged FIXED, or whose GRIB is newer than CUTOFF, is skipped.
# PARALLEL shares the relay with any running chain: the two together stay <= 6 (#69).
set -uo pipefail

PROJECT_DIR="${PROJECT_DIR:-/leonardo/home/userexternal/lmonaco0/CHAPTER}"
W="${W:-/leonardo_work/AIFPT_AILAMIT/CHAPTER}"
GRIB_DIR="${GRIB_DIR:-${W}/grib_v3}"
STAGE="${STAGE:-${W}/wrfout_fix00z}"          # never the pipeline's wrfout dirs
STATIC_REF_DIR="${STATIC_REF_DIR:-${W}/static_v1}"
CUTOFF="${CUTOFF:-${W}/logs/fix_00z_run.cutoff}"
LIST="${LIST:-${W}/logs/fix_00z_run.list}"
LEDGER="${LEDGER:-${W}/logs/fix_00z_run_status.log}"
STOP="${STOP:-${W}/logs/fix_00z_run.stop}"
PARALLEL="${PARALLEL:-2}"
MAX_JOBS="${MAX_JOBS:-12}"                    # fix00_* jobs queued at once
MIN_BYTES=8000000000

cfg() { (cd "$PROJECT_DIR" && ~/.local/bin/uv run python -c \
    "from omegaconf import OmegaConf; c = OmegaConf.load('conf/pipeline.yaml'); print(OmegaConf.select(c, '$1'))"); }
DATAMOVER_HOST="$(cfg datamover.host)"; REMOTE_HOST="$(cfg datamover.remote_host)"
IDENTITY_FILE="$(cfg datamover.identity_file)"; SFTP_OPTS="$(cfg datamover.sftp_opts)"
BASE_2023="$(cfg datamover.base_2023)"; BASE_PRE2023="$(cfg datamover.base_pre2023)"
FETCH_TIMEOUT="$(cfg datamover.fetch_timeout)"; FETCH_RETRIES="$(cfg datamover.fetch_retries)"
INIT_HOUR="$(cfg datamover.init_hour)"; TEMPLATE="$(cfg grib.name_template)"
ACCOUNT="$(cfg slurm.step_convert_account)"
export PROJECT_DIR W GRIB_DIR STAGE STATIC_REF_DIR CUTOFF LEDGER STOP MAX_JOBS MIN_BYTES \
       DATAMOVER_HOST REMOTE_HOST IDENTITY_FILE SFTP_OPTS BASE_2023 BASE_PRE2023 \
       FETCH_TIMEOUT FETCH_RETRIES INIT_HOUR TEMPLATE ACCOUNT

[ -e "$CUTOFF" ] || { echo "no ${CUTOFF}: touch it before relaunching the chains"; exit 1; }

log_status() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | $1 | $2 | ${3:-}" >> "$LEDGER"; }
grib_of() {     # the 00Z GRIB of day $1
    local d="$1" n="$TEMPLATE"
    n="${n//\{year\}/${d:0:4}}"; n="${n//\{date_compact\}/${d//-/}}"; n="${n//\{hour:02d\}/00}"
    echo "${GRIB_DIR}/${d:0:4}/${d:5:2}/${n}"
}
export -f log_status grib_of

fix_day() {
    local d="$1" p run base name dest grib errf rc attempt jobid
    [ -e "$STOP" ] && return 0
    grib=$(grib_of "$d")
    grep -q "| ${d} | FIXED" "$LEDGER" 2>/dev/null && return 0
    [ "$grib" -nt "$CUTOFF" ] && return 0
    [ -f "$grib" ] || { log_status "$d" NO_GRIB "$grib"; return 0; }
    # The 24 h file of the run for D-1: in that run's folder, named like D's 00Z.
    p=$(TZ=UTC date -d "$d -1 day" +%Y-%m-%d)
    run="$(TZ=UTC date -d "$p -1 day" +%Y%m%d)${INIT_HOUR}"
    if [ "${p:0:4}" -ge 2023 ]; then base="$BASE_2023"; else base="$BASE_PRE2023"; fi
    name="wrfout_d02_${d}_00:00:00"
    dest="${STAGE}/${run}/${name}"
    mkdir -p "${STAGE}/${run}"
    if ! [ "$(stat -c%s "$dest" 2>/dev/null || echo 0)" -ge "$MIN_BYTES" ]; then
        errf=$(mktemp); rc=1
        for attempt in $(seq 1 $((FETCH_RETRIES + 1))); do
            rm -f "$dest"
            if timeout "$FETCH_TIMEOUT" ssh -nxT "$DATAMOVER_HOST" \
                 "sftp -i ${IDENTITY_FILE} ${SFTP_OPTS} ${REMOTE_HOST}:${base}/${run}/${name} ${STAGE}/${run}/" \
                 >/dev/null 2>"$errf"; then rc=0; break; else rc=$?; fi
            grep -qiE 'No such file|not a regular file|File .* not found' "$errf" && break
            sleep 30
        done
        if [ "$rc" -ne 0 ] || [ "$(stat -c%s "$dest" 2>/dev/null || echo 0)" -lt "$MIN_BYTES" ]; then
            log_status "$d" FETCH_FAILED "run ${run} rc=${rc} size=$(stat -c%s "$dest" 2>/dev/null || echo 0)B $(tr '\n' ' ' <"$errf" | cut -c1-160)"
            rm -f "$errf" "$dest"; return 0
        fi
        rm -f "$errf"
    fi
    # Room in the queue; one lock so two workers reading 11 of 12 do not both go.
    (
        flock 9
        while [ "$(timeout 60 squeue -h -u "$USER" -o %j 2>/dev/null | grep -c '^fix00_')" -ge "$MAX_JOBS" ]; do
            [ -e "$STOP" ] && exit 0
            sleep 60
        done
        jobid=$(sbatch --parsable --partition dcgp_usr_prod --account "$ACCOUNT" \
            --time 01:00:00 --mem 32G --job-name "fix00_${d//-/}" \
            --output "${W}/logs/fix00/fix00_${d//-/}_%j.out" \
            --export "ALL,DAY=${d},INPUT=${dest},GRIB=${grib},LEDGER=${LEDGER},PROJECT_DIR=${PROJECT_DIR},STATIC_REF_DIR=${STATIC_REF_DIR}" \
            "${PROJECT_DIR}/hpc/fix_00z_convert.sh") || jobid=""
        if [[ "$jobid" =~ ^[0-9]+$ ]]; then
            log_status "$d" SUBMITTED "job=${jobid} run=${run}"
            sleep 2     # let squeue see it before the next worker counts
        else
            log_status "$d" SUBMIT_FAILED "sbatch returned '${jobid}'"
        fi
    ) 9>"${W}/logs/fix_00z_run.lock"
}
export -f fix_day

mkdir -p "${W}/logs/fix00"
if ! [ -s "$LIST" ]; then
    find "$GRIB_DIR" -name '*00.grib' ! -newer "$CUTOFF" -printf '%f\n' \
        | sed -E 's/.*-([0-9]{4})([0-9]{2})([0-9]{2})00\.grib$/\1-\2-\3/' | sort -u > "$LIST"
fi
echo "$(date -u +%FT%TZ) start: $(wc -l <"$LIST") days, parallel ${PARALLEL}, ledger ${LEDGER}"
xargs -P "$PARALLEL" -n 1 bash -c 'fix_day "$0"' < "$LIST"
echo "$(date -u +%FT%TZ) done: $(grep -c '| SUBMITTED' "$LEDGER" 2>/dev/null || echo 0) submitted so far, $(grep -c '| FIXED' "$LEDGER" 2>/dev/null || echo 0) fixed"
