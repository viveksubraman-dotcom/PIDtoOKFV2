#!/usr/bin/env bash
# ==============================================================================
# Unified Deployment Script for Extracter Agent (Mining M3 Light Cockpit + ADK)
#
# Targets:
#   - cloud_run (web):       Deploys the unified Mining M3 Light Executive Demo
#                            Cockpit + Google ADK Web UI (extracter_agent.web_server:app)
#                            to Google Cloud Run connected to GCS knowledge store.
#   - agent_runtime (agent): Deploys ADK Root Orchestrator to Gemini Enterprise
#                            Agent Platform (Vertex AI Reasoning Engine).
#   - all:                   Deploys both agent_runtime and cloud_run.
#
# Usage:
#   ./deploy.sh --target cloud_run      # Deploy Mining M3 Light Cockpit + ADK Web UI
#   ./deploy.sh --target agent_runtime  # Deploy ADK Agent Runtime
#   ./deploy.sh                         # Deploy Cloud Run Customer Demo (default)
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

# Load unified .env configuration if present (Rule 8)
if [[ -f ".env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source ".env"
  set +a
fi

PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-ut-interaction-demo}"
REGION="${NONPROD_REGION:-asia-southeast1}"
MODEL_LOCATION="${GEMINI_LOCATION:-global}"
AGENT_DIR="extracter_agent"
AGENT_DISPLAY_NAME="${SERVICE_NAME:-extracter-agent}"
WEB_SERVICE_NAME="${CLOUD_RUN_WEB_SERVICE:-extracter-agent-web}"
GCS_BUCKET="${DESTINATION_GCS_BUCKET:-${PROJECT_ID}-okf-knowledge}"
GCS_PREFIX="${DESTINATION_GCS_PREFIX:-okf-bundles/phenol-plant}"
RAW_PREFIX="${SOURCE_GCS_RAW_PREFIX:-reference/raw}"
MODEL_NAME="${GEMINI_MODEL:-gemini-3.8-flash}"

# Ensure gcloud uses fresh Application Default Credentials token when running in Argolis
if command -v gcloud >/dev/null 2>&1; then
  ADC_TOKEN="$(gcloud auth application-default print-access-token 2>/dev/null || true)"
  if [[ -n "${ADC_TOKEN}" ]]; then
    export CLOUDSDK_AUTH_ACCESS_TOKEN="${ADC_TOKEN}"
  fi
fi

TARGET="cloud_run"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --target|-t)
      TARGET="$2"
      shift 2
      ;;
    agent|agent_runtime|agent_engine)
      TARGET="agent_runtime"
      shift
      ;;
    web|cloud_run|adk_web)
      TARGET="cloud_run"
      shift
      ;;
    all)
      TARGET="all"
      shift
      ;;
    --help|-h)
      sed -n '2,17p' "${BASH_SOURCE[0]}"
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

deploy_agent_runtime() {
  local raw_engine_id="${NONPROD_AGENT_RUNTIME_ID:-}"
  local agent_engine_id="${raw_engine_id##*/}"
  local adk_bin=".venv/bin/adk"
  if [[ ! -x "${adk_bin}" ]]; then
    adk_bin="$(command -v adk || true)"
  fi

  echo "=============================================================================="
  echo "[1/2] Deploying ADK Agent to Gemini Enterprise Agent Platform (agent_runtime)"
  echo "  Project:          ${PROJECT_ID}"
  echo "  Region:           ${REGION}"
  echo "  Model Location:   ${MODEL_LOCATION}"
  echo "  Display Name:     ${AGENT_DISPLAY_NAME}"
  echo "=============================================================================="

  if [[ -n "${agent_engine_id}" ]]; then
    "${adk_bin}" deploy agent_engine \
      --project="${PROJECT_ID}" \
      --region="${REGION}" \
      --agent_engine_id="${agent_engine_id}" \
      --display_name="${AGENT_DISPLAY_NAME}" \
      "${AGENT_DIR}"
  else
    "${adk_bin}" deploy agent_engine \
      --project="${PROJECT_ID}" \
      --region="${REGION}" \
      --display_name="${AGENT_DISPLAY_NAME}" \
      "${AGENT_DIR}"
  fi
}

deploy_adk_web_cloud_run() {
  echo "=============================================================================="
  echo "[Cloud Run] Deploying Mining M3 Light Cockpit + ADK Web Server"
  echo "  Project:          ${PROJECT_ID}"
  echo "  Region:           ${REGION}"
  echo "  Model Location:   ${MODEL_LOCATION}"
  echo "  Model Name:       ${MODEL_NAME}"
  echo "  Service Name:     ${WEB_SERVICE_NAME}"
  echo "  GCS Bucket:       gs://${GCS_BUCKET}/${GCS_PREFIX}"
  echo "=============================================================================="

  gcloud run deploy "${WEB_SERVICE_NAME}" \
    --source="." \
    --project="${PROJECT_ID}" \
    --region="${REGION}" \
    --no-invoker-iam-check \
    --memory=2Gi \
    --cpu=2 \
    --timeout=600 \
    --min-instances="${NONPROD_MIN_INSTANCES:-0}" \
    --max-instances="${NONPROD_MAX_INSTANCES:-3}" \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GOOGLE_CLOUD_LOCATION=${REGION},NONPROD_REGION=${REGION},GOOGLE_GENAI_USE_VERTEXAI=true,GEMINI_LOCATION=${MODEL_LOCATION},GEMINI_MODEL=${MODEL_NAME},USE_GCS_STORAGE=true,SOURCE_GCS_RAW_PREFIX=${RAW_PREFIX},DESTINATION_GCS_BUCKET=${GCS_BUCKET},DESTINATION_GCS_PREFIX=${GCS_PREFIX},OUTPUT_BUNDLE_DIR=/tmp/okf_bundle" \
    --quiet

  local web_url
  web_url="$(gcloud run services describe "${WEB_SERVICE_NAME}" \
    --project="${PROJECT_ID}" \
    --region="${REGION}" \
    --format='value(status.url)' 2>/dev/null || true)"
  if [[ -n "${web_url}" ]]; then
    echo ""
    echo "=============================================================================="
    echo "Mining M3 Light Executive Cockpit Live: ${web_url}"
    echo "Architecture Diagram Live:              ${web_url}/architecture-diagram"
    echo "Google ADK Developer UI Live:           ${web_url}/dev-ui/?app=extracter_agent"
    echo "Live Telemetry Status API:              ${web_url}/api/demo/status"
    echo "=============================================================================="
  fi
}

case "${TARGET}" in
  agent_runtime)
    deploy_agent_runtime
    ;;
  cloud_run)
    deploy_adk_web_cloud_run
    ;;
  all)
    deploy_agent_runtime
    deploy_adk_web_cloud_run
    ;;
  *)
    echo "Invalid target '${TARGET}'. Expected: all | agent_runtime | cloud_run" >&2
    exit 1
    ;;
esac
