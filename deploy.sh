#!/usr/bin/env bash
# ==============================================================================
# Unified Deployment Script for Extracter Agent (ADK Agent Runtime + ADK Web UI)
#
# Targets:
#   - agent_runtime (agent): Deploys ADK Root Orchestrator to Gemini Enterprise
#                            Agent Platform (Vertex AI Reasoning Engine).
#   - cloud_run (web):       Deploys interactive ADK Web UI (--with_ui) to
#                            Google Cloud Run connected to Agent Engine sessions
#                            and GCS artifacts (Rule 10 compliant: zero allUsers).
#   - all (default):         Deploys both agent_runtime and cloud_run.
#
# Usage:
#   ./deploy.sh                         # Deploy both Agent Runtime and ADK Web UI
#   ./deploy.sh --target agent_runtime  # Deploy only ADK Agent Runtime
#   ./deploy.sh --target cloud_run      # Deploy only ADK Web UI on Cloud Run
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

PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-cs-poc-y03r7kmfyov4kilzg50fd7s}"
REGION="${GOOGLE_CLOUD_LOCATION:-asia-southeast1}"
AGENT_DIR="extracter_agent"
AGENT_DISPLAY_NAME="${SERVICE_NAME:-extracter-agent}"
WEB_SERVICE_NAME="${CLOUD_RUN_WEB_SERVICE:-extracter-agent-web}"
GCS_BUCKET="${DESTINATION_GCS_BUCKET:-${PROJECT_ID}-okf-knowledge}"
GCS_PREFIX="${DESTINATION_GCS_PREFIX:-okf-bundles/phenol-plant}"
RAW_PREFIX="${SOURCE_GCS_RAW_PREFIX:-reference/raw}"
MODEL_NAME="${GEMINI_MODEL:-gemini-3.8-flash}"

# Extract numeric Reasoning Engine ID from NONPROD_AGENT_RUNTIME_ID if full resource path is configured
RAW_ENGINE_ID="${NONPROD_AGENT_RUNTIME_ID:-8210246838649880576}"
AGENT_ENGINE_ID="${RAW_ENGINE_ID##*/}"

ADK_BIN=".venv/bin/adk"
if [[ ! -x "${ADK_BIN}" ]]; then
  ADK_BIN="$(command -v adk || true)"
fi
if [[ -z "${ADK_BIN}" ]]; then
  echo "Error: 'adk' CLI not found in .venv/bin/adk or PATH." >&2
  exit 1
fi

TARGET="all"
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
  echo "=============================================================================="
  echo "[1/2] Deploying ADK Agent to Gemini Enterprise Agent Platform (agent_runtime)"
  echo "  Project:          ${PROJECT_ID}"
  echo "  Region:           ${REGION}"
  echo "  Agent Engine ID:  ${AGENT_ENGINE_ID}"
  echo "  Display Name:     ${AGENT_DISPLAY_NAME}"
  echo "=============================================================================="

  "${ADK_BIN}" deploy agent_engine \
    --project="${PROJECT_ID}" \
    --region="${REGION}" \
    --agent_engine_id="${AGENT_ENGINE_ID}" \
    --display_name="${AGENT_DISPLAY_NAME}" \
    "${AGENT_DIR}"
}

deploy_adk_web_cloud_run() {
  local session_uri="agentengine://projects/${PROJECT_ID}/locations/${REGION}/reasoningEngines/${AGENT_ENGINE_ID}"
  local artifact_uri="gs://${GCS_BUCKET}"

  echo "=============================================================================="
  echo "[2/2] Deploying ADK Web UI (--with_ui) to Google Cloud Run (cloud_run)"
  echo "  Project:          ${PROJECT_ID}"
  echo "  Region:           ${REGION}"
  echo "  Service Name:     ${WEB_SERVICE_NAME}"
  echo "  Session URI:      ${session_uri}"
  echo "  Artifact URI:     ${artifact_uri}"
  echo "  Ingress Policy:   --no-invoker-iam-check (Rule 10: zero allUsers)"
  echo "=============================================================================="

  "${ADK_BIN}" deploy cloud_run \
    --project="${PROJECT_ID}" \
    --region="${REGION}" \
    --service_name="${WEB_SERVICE_NAME}" \
    --app_name="extracter_agent" \
    --with_ui \
    --session_service_uri="${session_uri}" \
    --artifact_service_uri="${artifact_uri}" \
    --env "PYTHONPATH=/app/agents" \
    --env "GOOGLE_GENAI_USE_VERTEXAI=true" \
    --env "GEMINI_MODEL=${MODEL_NAME}" \
    --env "USE_GCS_STORAGE=true" \
    --env "SOURCE_GCS_RAW_PREFIX=${RAW_PREFIX}" \
    --env "DESTINATION_GCS_BUCKET=${GCS_BUCKET}" \
    --env "DESTINATION_GCS_PREFIX=${GCS_PREFIX}" \
    --env "OUTPUT_BUNDLE_DIR=/tmp/okf_bundle" \
    "${AGENT_DIR}" \
    -- \
    --no-invoker-iam-check \
    --memory=2Gi \
    --cpu=2 \
    --timeout=600 \
    --min-instances="${NONPROD_MIN_INSTANCES:-0}" \
    --max-instances="${NONPROD_MAX_INSTANCES:-3}"

  local web_url
  web_url="$(gcloud run services describe "${WEB_SERVICE_NAME}" \
    --project="${PROJECT_ID}" \
    --region="${REGION}" \
    --format='value(status.url)' 2>/dev/null || true)"
  if [[ -n "${web_url}" ]]; then
    echo ""
    echo "ADK Web UI Live on Cloud Run: ${web_url}"
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
