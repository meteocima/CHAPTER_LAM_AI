#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=08:00:00
#SBATCH --partition=dcgp_usr_prod
#SBATCH --account=aifpt_ailamit_0
#SBATCH --job-name=fix_accum_h
#
# Make grib_v3's accumulations hourly (hpc/fix_accum_hourly.py, issue #70), one
# month per array task. Months are independent: a month's last day rewrites the
# next month's first 00Z, which the next month's task never touches.
# Re-entrant and idempotent: re-submitting is safe.
#
#   MONTHS="2019-01 2019-06 2019-07"
#   sbatch --array=0-2 --export=ALL,MONTHS="$MONTHS",PROJECT_DIR=$PWD \
#          --output=/leonardo_work/AIFPT_AILAMIT/CHAPTER/logs/fix_accum_h_%A_%a.out hpc/fix_accum_hourly.sh
# Extra args (e.g. --grib-root for a copy) via FIX_ARGS.

set -euo pipefail
read -r -a MONTH_LIST <<< "${MONTHS:?MONTHS not set}"
MONTH="${MONTH_LIST[${SLURM_ARRAY_TASK_ID:-0}]}"
cd "${PROJECT_DIR:?PROJECT_DIR not set}"
source tools/eccodes_env.sh
echo "=== fix_accum_hourly ${MONTH} @ $(hostname) $(date -u +%FT%TZ) ==="
# shellcheck disable=SC2086
~/.local/bin/uv run python hpc/fix_accum_hourly.py --month "${MONTH}" ${FIX_ARGS:-}
