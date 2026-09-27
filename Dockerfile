# ==============================================================================
# Production Container Image for PIDtoOKF v2 — Mining M3 Light Executive Cockpit
# + Google ADK Agent Runtime Web Server
# ==============================================================================
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080 \
    GOOGLE_GENAI_USE_VERTEXAI=true \
    GEMINI_LOCATION=global \
    GEMINI_MODEL=gemini-3.8-flash \
    OUTPUT_BUNDLE_DIR=/tmp/okf_bundle

WORKDIR /app

# Copy project metadata and source code
COPY pyproject.toml README.md ./
COPY extracter_agent ./extracter_agent
COPY docs ./docs
COPY reference ./reference

# Install runtime dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir . uvicorn fastapi

# Pre-seed /tmp/okf_bundle so cold starts have all 139 OKF v0.2 files ready immediately
RUN python3 -c "from extracter_agent.web_server import ensure_bundle_seeded; ensure_bundle_seeded()"

EXPOSE 8080

CMD ["sh", "-c", "uvicorn extracter_agent.web_server:app --host 0.0.0.0 --port ${PORT:-8080}"]
