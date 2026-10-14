#!/bin/bash
# One 00Z of grib_v3 re-converted from the 24 h file of the run for the day before
# (issue #72). Submitted by hpc/fix_00z_run.sh, one job per day, on dcgp_usr_prod.
#
#   DAY       YYYY-MM-DD of the 00Z
#   INPUT     the 24 h file of the run for DAY-1 (the converter refuses any other)
#   GRIB      the 00Z GRIB it replaces; its 19 accumulated messages are copied as
#             they are, everything else is converted from INPUT
#   LEDGER    FIXED / ERROR, one line per day
#
# Atomic: written to GRIB.tmp, checked with check_grib_sanity, fsync'ed, renamed
# over GRIB. The wrfout goes only on success; on failure it stays for a re-run.
set -uo pipefail
cd "${PROJECT_DIR:?}"
source tools/eccodes_env.sh
TMP="${GRIB}.fix00.tmp"
trap 'rm -f "${TMP}"' EXIT
log_status() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | ${DAY} | $1 | ${2:-}" >> "${LEDGER}"; }

echo "=== fix_00z ${DAY} @ $(hostname) $(date -u +%FT%TZ) ==="
echo "Input: ${INPUT}"
echo "GRIB:  ${GRIB}"
if ! ~/.local/bin/uv run python convert_to_pressure_levels.py --input "${INPUT}" \
        --output "${TMP}" --accum-from-grib "${GRIB}" --static-ref-dir "${STATIC_REF_DIR}"; then
    log_status ERROR "conversion failed, see logs/fix00/fix00_${DAY//-/}_${SLURM_JOB_ID:-}.out"
    exit 1
fi
if ! ~/.local/bin/uv run python hpc/check_grib_sanity.py "${TMP}"; then
    log_status ERROR "check_grib_sanity refused the new file; the old one is untouched"
    exit 1
fi
sync "${TMP}" && mv -f "${TMP}" "${GRIB}"
log_status FIXED "$(stat -c%s "${GRIB}")B"
timeout 60 rm -f "${INPUT}"
