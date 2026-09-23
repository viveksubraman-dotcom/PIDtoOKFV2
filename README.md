# Spec-Driven Development (SDD) & DevSecOps Platform

An enterprise platform and engineering framework operating under strict **Spec-Driven Development (SDD)**, Google Agent Development Kit (ADK) standards, Gemini Enterprise Agent Platform runtime, and multi-tier DevOps/Security governance.

---

## 🏛️ Core Architecture & Governance Pillars

This repository is governed by four core pillars codified under [`_agents/rules/`](./_agents/rules/) and orchestrated via [`AGENTS.md`](./AGENTS.md):

```
+-------------------------------------------------------------------------------------------------+
|                                    Spec-Driven Development (SDD)                                |
|  - Spec First, Code Second  - Brownfield Baseline Required  - Unit & Property Tests at Every Step |
+-------------------------------------------------------------------------------------------------+
                                                  │
                 ┌────────────────────────────────┴───────────────────────────────┐
                 ▼                                                                ▼
+--------------------------------------------------+    +--------------------------------------------------+
|           Enterprise DevOps & Security           |    |            Google ADK & Agent Runtime            |
| - Multi-Branch SCM (main -> prod)                |    | - Gemini Enterprise Agent Platform (agent_runtime)|
| - Pre-Build SAST with CodeMender (cm)            |    | - ADK Orchestrator & Domain Subagents            |
| - Google Cloud Build CI/CD                       |    | - Model-Driven Reasoning (Zero Regex/Heuristics) |
| - Cloud Run Web Frontends & Streaming Gateways   |    | - Continuous Live Evaluation (agents-cli eval)   |
| - Infrastructure Manager Terraform IaC           |    | - FunctionTool Registries & Model Armor Hooks    |
| - Domain Restricted Sharing (Zero allUsers)      |    |                                                  |
+--------------------------------------------------+    +--------------------------------------------------+
                                                  │
                                                  ▼
+-------------------------------------------------------------------------------------------------+
|                         Root Cause Investigation & Zero Quick-Patch Standard                    |
|  - Mandatory 4-Step RCA Protocol  - Zero Quick Fixes / Mockups  - Await User Architectural Direction|
+-------------------------------------------------------------------------------------------------+
```

---

## ⚡ Runtime Architecture & Separation of Responsibilities

Workloads in this project are strictly decoupled across two runtime environments:

| Dimension | Conversational AI Agents & Reasoning Engine | Web Frontend, API Gateway & Streaming Proxies |
| :--- | :--- | :--- |
| **Target Runtime** | **Gemini Enterprise Agent Platform (`agent_runtime`)** | **Google Cloud Run (`cloud_run`)** |
| **Deployed Artifacts** | ADK Root Coordinator (`OrchestratorAgent`), Domain Subagents, cognitive system prompts, Model Armor security callbacks, and `FunctionTool` registries. | React/Vite web client, Express/FastAPI proxy, WebSocket/SSE streaming endpoints, and background worker jobs. |
| **Deployment Mechanism** | `agents-cli deploy --deployment-target agent_runtime` | Google Cloud Build (`cloudbuild.yaml`) + Terraform via Google Cloud Infrastructure Manager |
| **Core Responsibilities** | Autonomous multi-turn reasoning, session persistence (`agentengine://`), live tool execution, and trajectory evaluation (`agents-cli eval`). | HTTP/HTTPS ingress, IAP authentication gateway, client UI rendering, health probes (`/healthz`), and thin proxying to the Agent Platform. |
| **Governance Rule** | [`_agents/rules/google_adk_and_agent_runtime.md`](./_agents/rules/google_adk_and_agent_runtime.md) | [`_agents/rules/devops_security_and_quality_standards.md`](./_agents/rules/devops_security_and_quality_standards.md) |

---

## 📁 Repository Structure

```
├── AGENTS.md                      # Authoritative Agent Operating Manual & Repository Guidelines
├── README.md                      # Project root documentation & architecture overview
├── _agents/                       # Agent governance rules and specialized skill toolkits
│   ├── rules/                     # Core engineering and behavioral rules
│   │   ├── spec_driven_development.md
│   │   ├── devops_security_and_quality_standards.md
│   │   ├── google_adk_and_agent_runtime.md
│   │   └── root_cause_investigation_and_zero_quick_patch.md
│   └── skills/                    # Agent operational skills
│       ├── architecture_diagram/  # Technical architecture diagrams & standalone HTML assets
│       ├── codemender/            # Pre-build SAST vulnerability discovery, triage, and patching
│       └── gcp_cost_estimator/    # Live GCP Billing API cost estimation & BoM calculation
├── reference/                     # Immutable read-only reference materials (raw/ and wiki/)
├── specs/                         # Single Source of Truth for specifications (SDD)
│   ├── README.md                  # Specifications index and SDD registry
│   ├── templates/                 # Reusable SDD templates (sdd-template.md)
│   ├── baseline/                  # Brownfield baseline specifications (as-is state)
│   ├── features/                  # Proposed feature specifications & implementation plans
│   └── plan/                      # Living execution progress reports and milestone tracking
└── docs/                          # Operational audit reports, cost models & diagram assets
    ├── README.md                  # Documentation index & naming conventions
    ├── *-architecture.md          # Architecture designs & HTML companion visual assets
    ├── codemender-*.md            # SAST security vulnerability scan & patch reports
    └── gcp_cost_estimate_*.md     # Live cloud cost models & itemized BoMs
```

---

## 🔄 Spec-Driven Development (SDD) Workflow

Every development task progresses through these sequential phases:

```
[Phase 0: Baseline Discovery (Brownfield)]
               │
               ▼
[Phase 1: Specification Authoring (specs/features/)]
               │
               ▼
[Phase 2: Detailed Implementation Plan + Test Design (Unit + PBT)]
               │
               ▼
[Phase 3: Stakeholder Alignment & Review]
               │
               ▼
[Phase 4: Step-by-Step Implementation + Unit & Property Tests]
               │
               ▼
[Phase 5: Verification, Spec Sync & Living Plan Progress Tracking (specs/plan/)]
```

### Mandatory Testing Standards for Every Step
- **Unit Tests:** Deterministic boundary, edge-case, and error-handling tests.
- **Property-Based Tests (PBT):** Invariant testing across generative fuzzed inputs using `fast-check` (TypeScript) or `hypothesis` (Python).
- **Live Agent Evaluation:** Trajectory fidelity and tool selection evaluated using `agents-cli eval run` ($\ge 95\%$ tool selection precision, 1.000 groundedness).
- **RCA Protocol on Failure:** Zero quick-patches or mockups; execute the 4-step RCA protocol.

---

## 🛠️ Integrated Skills & Capabilities

- **`codemender`:** Pre-build SAST orchestration discovering vulnerabilities (`cm find`), generating PoC exploit verification (`cm verify`), and producing remediated code diffs (`cm fix`).
- **`gcp_cost_estimator`:** Enterprise cloud cost modeling querying real-time unit pricing strictly from the live Google Cloud Billing API (zero local caching) and calculating itemized BoMs with CUD savings.
- **`architecture_diagram`:** Generates professional, dark-themed technical system diagrams with interactive SVG/HTML companion visualizers.

---

## 🧪 Chemical Engineering OKF Extracter Agent (`gemini-3.8-flash`)

The **Extracter Agent** (`extracter_agent`) is an autonomous Google ADK multi-file engineering extraction engine deployed to the **Gemini Enterprise Agent Platform (`agent_runtime`)**. It reads complex chemical engineering PDFs (Process Data Sheets, P&IDs, PFDs, Operating Manuals, and SDS) directly from Google Cloud Storage (`gs://cs-poc-y03r7kmfyov4kilzg50fd7s-okf-knowledge/reference/raw/`) and automatically persists verified **Open Knowledge Format (OKF v0.2)** knowledge bundles directly to Google Cloud Storage (`gs://cs-poc-y03r7kmfyov4kilzg50fd7s-okf-knowledge/okf-bundles/phenol-plant/`).

### Key Capabilities & Enhancements
1. **End-to-End Cloud Storage (GCS) Ingestion & Persistence (`USE_GCS_STORAGE=true`):**
   - **Step 1 (`find_raw_documents_tool`):** Autonomous multi-folder discovery listing PDF blobs directly from `gs://cs-poc-y03r7kmfyov4kilzg50fd7s-okf-knowledge/reference/raw/` (`data_sheets/`, `pid/`, `pfd/`, `operating_manuals/`, `standards/`).
   - **Step 2 (`process_raw_pdf_tool`):** Streams source PDFs from GCS (`source_gcs_uri`) for multi-page text/table extraction and high-resolution (300 DPI) multimodal visual inspection of vector engineering drawings (`gemini-3.8-flash`).
   - **Step 3 (Cross-Document Precedence, `⚠️ CONFLICT` Callouts & Topology):** Reconciles Process Data Sheets (Rev Z1) against P&IDs and PFDs, flags multi-sheet/cross-document conflicts explicitly (`⚠️ CONFLICT`), extracts upstream/downstream gravity drainage elevation heads (`≥ 2500 mm`, `≥ 5000 mm`), and documents SIS/ESD valve trip philosophies (`UC-2301` vs. `UC-2302`).
   - **Step 4 (`generate_equipment_okf_tool` / `generate_okf_concept_tool`):** Synthesizes schema-validated OKF v0.2 Markdown concepts with slash-sanitized filenames (`sanitize_tag_filename`, e.g., `D-2204A/B/C` $\rightarrow$ `equipment/D-2204ABC.md`) and **automatically uploads every generated `.md` file and `log.md` entry directly to `gs://cs-poc-y03r7kmfyov4kilzg50fd7s-okf-knowledge/okf-bundles/phenol-plant/`**.
   - **Step 5 (`build_okf_indexes_and_validate_tool`):** Compiles progressive disclosure `index.md` catalogs (`index.md`, `equipment/index.md`), validates 100% OKF v0.2 compliance, and syncs all indexes to GCS.
   - **Step 6 (`export_bundle_to_gcs_tool`):** Full-bundle synchronization and GCS manifest verification (`gs://cs-poc-y03r7kmfyov4kilzg50fd7s-okf-knowledge/okf-bundles/phenol-plant/`).
2. **Vertex AI Preemption Resilience (`Option A`):**
   - Built-in `HttpRetryOptions` (5 attempts, exponential backoff on HTTP `429, 500, 502, 503, 504`) and turn-level stream recovery with `--resume` checkpointing for `gemini-3.8-flash`.

### Live Vertex AI Evaluation Results (`Zero Mocks`)

| Metric | Phase 1 (`9` Cases) | Phase 2 (`11` Cases) | Combined (`20` Cases) | Rule 12 Target |
| :--- | :--- | :--- | :--- | :--- |
| **End-to-End Pass Rate** | **9 / 9 (100.0%)** | **10 / 11 (90.9%)** | **19 / 20 (95.0%)** | $\ge 95.0\%$ (**PASS**) |
| **Intent Classification Accuracy** | **100.0%** | **100.0%** | **100.0%** | $\ge 95.0\%$ (**PASS**) |
| **Tool Trajectory Precision** | **100.0%** | **100.0%** | **100.0%** | $\ge 95.0\%$ (**PASS**) |
| **Negative Constraint Adherence** | **100.0%** | **100.0%** | **100.0%** | $100.0\%$ (**PASS**) |
| **Model Armor Security Interception** | **100.0%** | **100.0%** | **100.0%** | $100.0\%$ (**PASS**) |
| **Unit & Property-Based Tests (PBT)** | **45 / 45 Passed** | **45 / 45 Passed** | **100.0%** | $100.0\%$ (**PASS**) |

### Running Detached Live Evaluations on Cloudtop (Against Deployed Agent Runtime)
To run or resume the full 130-case evaluation suite against the deployed **Vertex AI Agent Runtime (`projects/114618371568/locations/asia-southeast1/reasoningEngines/8210246838649880576`)** inside a detached `tmux` session that survives client disconnects:
```bash
tmux new-session -d -s extracter_eval \
  "cd /usr/local/google/home/pantana/lab/extracter-agent && \
   PYTHONPATH=. ./.venv/bin/python -u evals/run_live_vertex_eval.py \
   --use-agent-runtime --limit 130 --resume \
   --output evals/reports/live_vertex_eval_full.json \
   > evals/reports/full_eval_live.log 2>&1"
```

---

## 📖 Key References
- **Operating Manual:** [`AGENTS.md`](./AGENTS.md)
- **Specification Registry:** [`specs/README.md`](./specs/README.md)
- **Feature Specification:** [`specs/features/SPEC-20260922-OKF-EXTRACTER-AGENT.md`](./specs/features/SPEC-20260922-OKF-EXTRACTER-AGENT.md)
- **Plan Progress Report:** [`specs/plan/PROGRESS_REPORT_20260922.md`](./specs/plan/PROGRESS_REPORT_20260922.md)
- **Operational Reports & Diagrams:** [`docs/README.md`](./docs/README.md)
- **Rules Catalog:** [`_agents/rules/README.md`](./_agents/rules/README.md)
- **Skills Catalog:** [`_agents/skills/README.md`](./_agents/skills/README.md)

