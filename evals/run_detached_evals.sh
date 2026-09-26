#!/usr/bin/env bash
# ==============================================================================
# SIGHUP-Immune Detached Evaluation Runner
#
# Phase 1: Resumes the 139-case By-Equipment (wiki) evaluation from checkpoint
#          (82/139 -> 139/139) into build/okf_bundle and snapshots a read-only
#          backup at build/okf_bundle_by_equipment.
# Phase 2: Executes the clean 136-case Individual PDF (file-by-file) evaluation
#          from scratch into an isolated bundle directory (build/okf_bundle_by_pdf)
#          and isolated GCS prefix (okf-bundles/phenol-plant-by-pdf) so existing
#          by-equipment results are 100% preserved for side-by-side analysis.
# ==============================================================================

trap '' HUP
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${SCRIPT_DIR}"

mkdir -p evals/reports

echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] === PHASE 1: Resuming By-Equipment (wiki) Evaluation (82/139 -> 139/139) ===" >> evals/reports/full_eval_live.log

OUTPUT_BUNDLE_DIR="build/okf_bundle" \
DESTINATION_GCS_PREFIX="okf-bundles/phenol-plant" \
PYTHONPATH=. .venv/bin/python -u evals/run_live_vertex_eval.py \
  --use-agent-runtime \
  --dataset wiki \
  --limit 130 \
  --concurrency 4 \
  --resume \
  --output evals/reports/live_vertex_eval_full.json >> evals/reports/full_eval_live.log 2>&1

# Preserve an immutable local snapshot of the completed by-equipment bundle
rm -rf build/okf_bundle_by_equipment
cp -a build/okf_bundle build/okf_bundle_by_equipment
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] === PHASE 1 COMPLETE: Snapshot saved to build/okf_bundle_by_equipment ===" >> evals/reports/full_eval_live.log

# Prepare clean, isolated directory for Phase 2 (Individual PDF / file-by-file evaluation)
mkdir -p build/okf_bundle_by_pdf
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] === PHASE 2: Starting Clean Individual PDF (file-by-file) Evaluation (136 Raw PDFs) ===" >> evals/reports/by_pdf_eval_live.log

OUTPUT_BUNDLE_DIR="build/okf_bundle_by_pdf" \
DESTINATION_GCS_PREFIX="okf-bundles/phenol-plant-by-pdf" \
PYTHONPATH=. .venv/bin/python -u evals/run_live_vertex_eval.py \
  --use-agent-runtime \
  --dataset file-by-file \
  --skip-baseline \
  --limit 136 \
  --concurrency 4 \
  --resume \
  --output evals/reports/live_vertex_eval_by_pdf.json >> evals/reports/by_pdf_eval_live.log 2>&1

echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] === PHASE 2 COMPLETE: Individual PDF Evaluation Finished ===" >> evals/reports/by_pdf_eval_live.log
