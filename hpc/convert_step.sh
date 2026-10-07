#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --job-name=chapter_conv_step
#
# Convert a single hourly wrfout to GRIB2 format (single timestep, non-array).
# Submitted by hpc/fetch_step.sh once the wrfout for the timestep has been fetched.
# Runs on a compute node (e.g. dcgp_usr_prod); no network access required.
#
# Required env vars (set via --export at submission):
#   TARGET_DATE   - target date in YYYY-MM-DD format
#   HOUR          - hour of the timestep, zero-padded (00-23)
#   WRFOUT_DIR    - directory containing the wrfout file for this timestep
#   GRIB_DIR      - output directory for GRIB files
#   PROJECT_DIR   - path to CHAPTER repo (for convert_to_pressure_levels.py)
#   GRIB_TEMPLATE - output filename template (Python .format() style)
#   ACCUM_SNAP_DIR- (optional) accumulator snapshots (accum_hourly.py): each hour is
#                   differenced against the state before it; default: <GRIB_DIR>/../accum_snap
#   STATIC_REF_DIR- (optional) geo_em sidecar for the static land fields
#                   (static_ref.py); default: <GRIB_DIR>/../static_v1
#   KEEP_WRFOUT   - (optional) "1" to keep the input wrfout after a successful convert

set -euo pipefail

HOUR=$(printf "%02d" "$((10#${HOUR}))")
DATE_COMPACT=$(echo "${TARGET_DATE}" | tr -d '-')

INPUT="${WRFOUT_DIR}/wrfout_d02_${TARGET_DATE}_${HOUR}:00:00"

# Output goes under a YYYY/MM tree below GRIB_DIR
YEAR="${TARGET_DATE:0:4}"
MONTH="${TARGET_DATE:5:2}"
OUTPUT="${GRIB_DIR}/${YEAR}/${MONTH}/${GRIB_TEMPLATE}"

# Expand template variables in output filename
OUTPUT=$(echo "${OUTPUT}" | sed "s/{year}/${YEAR}/g; s/{date_compact}/${DATE_COMPACT}/g; s/{hour:02d}/${HOUR}/g")
mkdir -p "$(dirname "${OUTPUT}")"
# Accumulations are the hour ending now, against the snapshot of the state before
ACCUM_SNAP_DIR="${ACCUM_SNAP_DIR:-$(dirname "${GRIB_DIR%/}")/accum_snap}"
# cvl/cvh/tvl/tvh/slt/cl/dl come from geo_em, read once into this sidecar
STATIC_REF_DIR="${STATIC_REF_DIR:-$(dirname "${GRIB_DIR%/}")/static_v1}"
TMPOUT="${OUTPUT}.tmp"

# Clean up partial output on failure
trap 'rm -f "${TMPOUT}"' EXIT

echo "=== CHAPTER convert_step ==="
echo "Date:   ${TARGET_DATE}"
echo "Hour:   ${HOUR}"
echo "Input:  ${INPUT}"
echo "Output: ${OUTPUT}"
echo ""

# Re-entrancy: skip only if the existing output is at the CURRENT schema.
# Keying the skip on the file merely EXISTING is what forced a new output tree
# at every schema change (grib -> grib_v2 -> grib_v3), because a wider schema
# written into the old tree silently skipped every hour already converted at
# the narrower one. Counting the messages makes a re-run self-healing instead.
if [ -f "${OUTPUT}" ]; then
    if SCHEMA=$(python3 "${PROJECT_DIR}/hpc/grib_schema_ok.py" "${OUTPUT}"); then
        echo "Output GRIB already exists at the current schema (${SCHEMA}), skipping."
        exit 0
    fi
    echo "SCHEMA_MISMATCH: ${OUTPUT} is ${SCHEMA} messages; reconverting."
fi

# Check input exists
if [ ! -f "${INPUT}" ]; then
    echo "ERROR: Input wrfout not found: ${INPUT}"
    exit 1
fi

cd "${PROJECT_DIR}"

# Load eccodes C library (built with gcc-12, needs matching runtime)
module load eccodes/2.34.0--gcc--12.2.0 2>/dev/null
GCC12_RT="/leonardo/prod/spack/06/install/0.22/linux-rhel8-icelake/gcc-12.2.0/gcc-runtime-12.2.0-dqfwf7yjtbtdzllj66jx6suk34ir2ct3/lib"
ECCODES_LIB="/leonardo/prod/spack/06/install/0.22/linux-rhel8-icelake/gcc-12.2.0/eccodes-2.34.0-msheephhj7zirdzmqcfdrf4jat5w545r/lib64"
export LD_PRELOAD="$GCC12_RT/libstdc++.so.6"
export LD_LIBRARY_PATH="$GCC12_RT:$ECCODES_LIB:${LD_LIBRARY_PATH:-}"

uv run python convert_to_pressure_levels.py \
    --input "${INPUT}" \
    --output "${TMPOUT}" \
    --accum-snap-dir "${ACCUM_SNAP_DIR}" \
    --static-ref-dir "${STATIC_REF_DIR}"

# Atomic rename on success
mv "${TMPOUT}" "${OUTPUT}"

echo ""
# The next hour is differenced against this file's state: never delete a wrfout
# whose snapshot is missing (the converter writes it). Then drop the snapshots
# this hour consumed -- no other hour reads them (accum_hourly.consumed).
if ! uv run python -c "import accum_hourly, os, sys; sys.exit(not os.path.isfile(accum_hourly.snapshot_path(sys.argv[2], accum_hourly.state_of(sys.argv[1]))))" "${INPUT}" "${ACCUM_SNAP_DIR}"; then
    echo "ERROR: no snapshot of ${INPUT} in ${ACCUM_SNAP_DIR}; keeping it"
    exit 1
fi
if [ "${KEEP_WRFOUT:-0}" = "1" ]; then
    echo "Conversion successful. KEEP_WRFOUT=1: keeping ${INPUT}"
    exit 0
fi
echo "Conversion successful. Cleaning up wrfout..."
timeout 60 rm -f "${INPUT}"
echo "Deleted: ${INPUT}"
uv run python accum_hourly.py consumed "${TARGET_DATE}T${HOUR}" "${ACCUM_SNAP_DIR}" || true
