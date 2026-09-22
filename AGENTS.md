# Agent Operating Manual & Project Guidelines

This repository operates strictly under the **Spec-Driven Development (SDD)** process, enterprise DevOps/Security standards, Google Agent Development Kit (ADK) & Agent Runtime standards, and the Mandatory Root Cause Investigation protocol.

## Core References
- Spec-Driven Development Standard: [_agents/rules/spec_driven_development.md](./_agents/rules/spec_driven_development.md)
- DevOps, Security & Quality Standards: [_agents/rules/devops_security_and_quality_standards.md](./_agents/rules/devops_security_and_quality_standards.md)
- Google ADK, Agent Runtime & Model-Driven Reasoning Standards: [_agents/rules/google_adk_and_agent_runtime.md](./_agents/rules/google_adk_and_agent_runtime.md)
- Root Cause Investigation & Zero Quick-Patch Standard: [_agents/rules/root_cause_investigation_and_zero_quick_patch.md](./_agents/rules/root_cause_investigation_and_zero_quick_patch.md)
- System Specifications: [specs/README.md](./specs/README.md)
- Operational & Skill Documentation: [docs/](./docs/)

---

## Repository Governance & Rule Pillars
1. **Spec-Driven Development (SDD):** Spec first, code second. Brownfield baseline required under `specs/baseline/`. Granular implementation plans with Unit and Property-Based Tests (PBT) at every step. Continuous progress tracking in `specs/plan/`.
2. **DevOps, Security & Cloud Run Services:** Single GitHub repository with multi-branch promotion (`main`/`develop` -> `prod`). Pre-build SAST with CodeMender (`cm`). Automated Cloud Build CI/CD, Cloud Run hosting for web frontends and API streaming proxies with health probes, unified single-file `.env` parameter management, Infrastructure Manager Terraform IaC, and strict Domain Restricted Sharing compliance (zero `allUsers`).
3. **Google ADK & Agent Platform Runtime:** Conversational AI agents and autonomous reasoning engines built with official Google ADK (`google-adk`) and deployed exclusively to the Gemini Enterprise Agent Platform (`agent_runtime`). Mandatory cognitive model-driven reasoning and structured FunctionTools; zero hardcoded keywords, regex routing, or static fallback arrays. Live environment evaluation via `agents-cli eval` ($\ge 95\%$ trajectory precision, 1.000 groundedness).
4. **Root Cause Investigation & Zero Quick-Patch Standard:** Mandatory 4-step RCA protocol when tests or evals fail. Zero quick fixes, mockups, or regex patches. Investigate root cause, transparently explain failure to the user, present viable architectural fix options with trade-offs, and await explicit user instruction before coding.
5. **Immutable Reference Directory (`reference/`):** The `reference/` directory contains read-only authoritative domain reference materials (e.g., `reference/raw/` and `reference/wiki/`). Agents are strictly prohibited from modifying, adding, overwriting, or deleting any files or directories in the `reference/` folder under any circumstances.

---

## Runtime Architecture & Separation of Responsibilities

This project enforces a strict architectural boundary between client-facing web workloads and autonomous AI agent reasoning engines:

| Dimension | Conversational AI Agents & Reasoning Engine | Web Frontend, API Gateway & Streaming Proxies |
| :--- | :--- | :--- |
| **Target Runtime** | **Gemini Enterprise Agent Platform (`agent_runtime`)** | **Google Cloud Run (`cloud_run`)** |
| **Deployed Artifacts** | ADK Root Coordinator (`OrchestratorAgent`), Domain Subagents, cognitive prompts, and `FunctionTool` registries. | React/Vite web application, Express/FastAPI reverse proxy, WebSocket/SSE streaming endpoints, and auxiliary jobs. |
| **Deployment Mechanism** | `agents-cli deploy --deployment-target agent_runtime` | Google Cloud Build (`cloudbuild.yaml`) + Terraform via Google Cloud Infrastructure Manager |
| **Core Responsibilities** | LLM reasoning, multi-turn session persistence (`agentengine://`), pre-flight Model Armor guardrails, tool execution, and trajectory evaluation (`agents-cli eval`). | HTTP/HTTPS ingress, IAP authentication gateway, client UI rendering, health probes (`/healthz`), and thin proxying to the Agent Platform. |
| **Governance Rule** | [`_agents/rules/google_adk_and_agent_runtime.md`](./_agents/rules/google_adk_and_agent_runtime.md) | [`_agents/rules/devops_security_and_quality_standards.md`](./_agents/rules/devops_security_and_quality_standards.md) |

---

## Spec-Driven Development (SDD) Directives

1. **Spec First, Code Second:** All development (features, bug fixes, refactoring, API changes) must be preceded by a formal Specification Document in `specs/`.
2. **Brownfield Baseline Requirement:** In brownfield development (such as working on an existing codebase), an accurate **Baseline SDD** reflecting the existing code, architecture, data models, and API contracts must be generated under `specs/baseline/` before making modifications.
3. **Implementation Plan with Step-by-Step Breakdown:** Every spec MUST include a granular, step-by-step Implementation Plan before coding begins.
4. **Mandatory Unit & Property-Based Testing at Every Step:** For *every* step in the implementation plan, developers/agents must implement:
   - **Unit Tests:** Deterministic, example-based tests verifying happy paths, edge cases, and error boundaries.
   - **Property-Based Tests (PBT):** Mathematical/logical invariant tests across generative/fuzzed input spaces (e.g. `fast-check` in TS/JS or `hypothesis` in Python).
5. **Spec Rule Reference:** Read and strictly comply with the governance rules in `_agents/rules/`:
   - `_agents/rules/spec_driven_development.md`
   - `_agents/rules/devops_security_and_quality_standards.md`
   - `_agents/rules/google_adk_and_agent_runtime.md`
   - `_agents/rules/root_cause_investigation_and_zero_quick_patch.md`
6. **Living Specs:** When any code or behavior changes, the corresponding SDD in `specs/` must be synchronized in the same change to prevent spec drift.
7. **Living Plan Progress Tracking:** Maintain continuous, up-to-date execution reports, test verification metrics, and milestone statuses under `specs/plan/` whenever development pauses or major phases complete.

---

## Mandatory Engineering, Quality, Security & Cloud Rules

1. **GitHub Repository Management & Multi-Branch Environment Strategy:** Single repository in GitHub managing Non-Prod (e.g. `main` / `develop`) and Prod (`prod` / `release`) on separate branches. Code promotion to production follows reviewed Pull Requests with passing quality and security gates.
2. **Static Code Quality Analysis:** Perform static code quality analysis to identify bugs, code smells, duplication, and maintainability issues after code commits.
3. **Pre-Build Static Application Security Testing (SAST):** Conduct static application security testing and vulnerability remediation (find, verify, fix) before build and deployment using the **CodeMender skill** (`_agents/skills/codemender/SKILL.md`).
4. **Artifact Analysis & Dependency Scanning:** Use Google Cloud Artifact Analysis (if applicable) to analyze open-source libraries and third-party dependencies for vulnerability and license compliance risks.
5. **Cloud Build & Artifact Registry:** Use Google Cloud Build to build the solution and store container images in Google Cloud Artifact Registry, mapping triggers and image tags to the target environment (`nonprod` vs `prod`).
6. **Cloud Run Observability & Liveness Probe (Web & API Proxy Services):** Web applications and API streaming proxies deploy to Google Cloud Run. Configure Cloud Run Liveness Probe (`/healthz`), Cloud Monitoring, and Cloud Logging for all Cloud Run services.
7. **Post-Deployment Integration Testing:** Run integration tests after deployment against the live deployed service.
8. **Centralized Multi-Environment Parameter Management (Unified Single File):** All configurable parameters for **both Non-Prod and Prod environments** must be maintained in the **same unified `.env` file** (documented in `.env.example`), structured into shared core variables and distinct environment-specific blocks (`NONPROD_*` and `PROD_*`).
9. **Terraform & Google Cloud Infrastructure Manager:** Deployment must be managed by Terraform using Google Cloud Infrastructure Manager with isolated deployment instances per environment (e.g., `<service>-nonprod` vs `<service>-prod`).
10. **IAM Domain Restricted Sharing & Authentication Recommendations:** Organization policy strictly prohibits `allUsers` and non-domain members in IAM policies. Agents must proactively recommend compliant authentication and ingress options: **Identity-Aware Proxy (IAP)** for production external apps, **App-level Google OAuth 2.0** for internal apps requiring user identity, or **Direct Unauthenticated Ingress (`invoker-iam-disabled: 'true'`)** for friction-free public/internal tools.
11. **Google Agent Development Kit (ADK), Agent Runtime & Model-Driven Reasoning (Conversational AI Agents):** All conversational AI agents and tool registries must be built with official `google-adk` (`Agent`, `FunctionTool`, `before_agent_callback` security hooks) and deployed exclusively to the Gemini Enterprise Agent Platform (`agent_runtime`) via `agents-cli deploy`. Agent reasoning is strictly cognitive and model-driven using a project-defined canonical intent topology (e.g., Domain Q&A, Task Execution, `OTHERS`); regex matching, keyword heuristics, static tag fallbacks, and hardcoded clarification lists are strictly prohibited (`_agents/rules/google_adk_and_agent_runtime.md`).
12. **Live Environment Agent Evaluation (`agents-cli eval`):** Agent trajectory fidelity, tool selection precision ($\ge 95\%$), and groundedness ($1.000 / 100\%$) must be continuously evaluated against the live environment (live databases, knowledge catalogs, live agent runtime) using `agents-cli eval run`. Offline synthetic mocks and stubs are strictly forbidden during formal evaluation.
13. **Mandatory Root Cause Investigation & Zero Quick-Patch Standard:** When any test or agent evaluation fails, or a defect is reported, developers/agents are strictly forbidden from applying quick patches, mockup fallback data, regex workarounds, or assertion weakening. Agents must execute the 4-step RCA protocol: deep root cause analysis, transparent failure explanation to the user, presentation of viable architectural fix options with trade-offs, and awaiting explicit user instruction before coding (`_agents/rules/root_cause_investigation_and_zero_quick_patch.md`).
14. **Immutability of Reference Materials (`reference/`):** The `reference/` directory is strictly read-only and reserved for immutable source materials (e.g. `reference/raw/` containing engineering datasheets, P&IDs, operating manuals, and standards; and `reference/wiki/` containing reference knowledge extractions). Agents **CANNOT** create, modify, overwrite, append to, or delete any content in this folder afterward under any circumstance. All derived work, new code, or artifacts must reside outside `reference/`.

---

## Project Structure Overview

- `reference/`: **Strictly read-only reference materials.** Contains immutable domain source data (`reference/raw/` with data sheets, manuals, PFDs, P&IDs, standards; and `reference/wiki/` with equipment, hazards, HAZOP tables, instruments, logs). **Agents cannot change content in this folder afterward.**
- `specs/`: Single source of truth for Spec-Driven Development (SDD) specifications, baseline docs, feature designs, and progress tracking.
  - `specs/baseline/`: Current as-is specifications reverse-engineered from existing code.
  - `specs/features/`: Proposed feature specifications with step-by-step plans & test matrices.
  - `specs/plan/`: Implementation progress reports, milestone execution tracking, and verification metrics.
  - `specs/templates/`: Reusable SDD templates.
- `docs/`: Generated documentation and reports from skills (e.g., CodeMender security audit reports, GCP cost estimates, and interactive architecture diagrams/assets).
- `src/`: Frontend React + Vite + TypeScript + Tailwind CSS application.
- `server/`: Backend Node.js + Express / FastAPI proxy integrating with the Gemini API / Agent Platform.
- `terraform/`: Declarative Infrastructure as Code for Cloud Run, Artifact Registry, IAM, and observability managed via Infrastructure Manager.
- `_agents/rules/`: Agent behavioral rules, SDD standards, and DevOps/Security governance.
  - `_agents/rules/spec_driven_development.md`: Core SDD mandate, baseline requirements, and living plan tracking.
  - `_agents/rules/devops_security_and_quality_standards.md`: 10 foundational DevOps, CI/CD, CodeMender SAST, and IaC rules.
  - `_agents/rules/google_adk_and_agent_runtime.md`: Official Google ADK architecture, Gemini Enterprise Agent Platform deployment, model-driven reasoning, canonical intent topology, and live agent evaluation (`agents-cli eval`).
  - `_agents/rules/root_cause_investigation_and_zero_quick_patch.md`: 4-step RCA investigation protocol, user transparency, and absolute prohibition of quick fixes, mockups, or regex patches on failing tests.
