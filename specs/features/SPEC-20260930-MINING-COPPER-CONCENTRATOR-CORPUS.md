# Specification: Copper-Gold Concentrator Engineering Corpus & Profile-Driven OKF Cockpit

**Document ID:** SPEC-20260930-MINING-COPPER-CONCENTRATOR-CORPUS  
**Status:** Approved  
**Date:** 2026-09-30  
**Target Project:** `ut-interaction-demo`  
**Git Repository:** `https://github.com/viveksubraman-dotcom/PIDtoOKFV2.git`  
**Target Runtime:** Google Cloud Run (`extracter-agent-web`, `asia-southeast1`) + Vertex AI Gemini (`gemini-3.8-flash`, `global`)  

---

## 1. Problem Statement & Objectives

### 1.1 Context & Motivation
The `extracter-agent` demonstration application was originally constructed over a petrochemical phenol/cumene (UOP Unit 23) reference dataset in `reference/raw/` (`136` PDFs). When presenting the P&ID-to-OKF compiler to mining and mineral processing customers, petrochemical equipment tags (`D-2304`, `V-2301`), process fluids (cumene hydroperoxide, alpha-methylstyrene), and chemical units reduce domain resonance.

At the same time, Repository Rule 14 mandates that `reference/` remain strictly read-only and unmodified. Therefore, we introduce a self-contained, explicitly synthetic **60,000 t/d Copper-Gold Concentrator Engineering Document Pack** (`corpora/copper-concentrator/`) together with a profile-driven cockpit architecture (`scripts/corpus_profiles/`) that makes the mining concentrator the default experience while preserving 100% backward compatibility with the phenol-plant corpus.

### 1.2 Goals
1. **Single Source of Physical Truth (`plant_model.py`):** Define a deterministic steady-state mass balance (`60,000 t/d` nameplate, `2,688 t/h` fresh feed at `93%` availability, `300%` circulating load, `P80 = 150 µm`), 17 equipment tags across Areas 21–61, 9 instrument/SIS loops, 6 flotation reagents, 5 HAZOP nodes, 11 seeded cross-document conflicts (`C01`–`C11`), and 1 revision-supersession decoy (`PP-5101A` Rev A `180 m³/h` → Rev B `210 m³/h`).
2. **Synthetic Multi-Document Engineering Pack (`generate_corpus.py`):** Render 45 realistic engineering PDFs (21 Process Data Sheets, 10 vector SVG P&IDs & lists, 4 PFDs, 1 Operating Manual, and 9 Standards/C&E/HAZOP/SDS files) in `corpora/copper-concentrator/raw/`, each carrying a prominent `SYNTHETIC DEMONSTRATION DOCUMENT` disclaimer.
3. **Real ADK Live Extraction (`run_extraction.py`):** Execute the unmodified `extracter_orchestrator` ADK agent (Mode B file-by-file incremental extraction) across all 45 PDFs to compile `corpora/copper-concentrator/wiki/` without hardcoded heuristics.
4. **Automated Conflict Evaluation (`eval_conflicts.py`):** Score the compiled OKF v0.2 bundle against the 11 seeded discrepancies (`SEEDED_CONFLICTS`) and verify that the revision decoy (`PP-5101A` Rev A → Rev B) is updated in-place rather than flagged as a conflict.
5. **Profile-Driven 4-Screen Cockpit (`scripts/corpus_profiles/`):** Refactor `scripts/build_demo_assets.py`, `extracter_agent/static/index.template.html`, and `extracter_agent/static/app.js` so `DEMO_CORPUS=copper-concentrator` (default) builds the mining concentrator cockpit and `DEMO_CORPUS=phenol-plant` reproduces the original phenol cockpit.

### 1.3 Non-Goals
- Modifying, deleting, or adding any file inside `reference/raw/` or `reference/wiki/` (Rule 14).
- Introducing regex or keyword routing inside the ADK agent (`extracter_agent/agent/`).
- Using real customer names or confidential mine data; all plant entities belong to the fictional *Cymbal Copper Pty Ltd — Ridgeback Concentrator (Project RB-4410)*.

---

## 2. System Architecture & Component Interaction

### 2.1 Runtime Allocation & Corpus Switching

| Layer | Component | Mining Concentrator (`DEMO_CORPUS=copper-concentrator`) | Legacy Phenol (`DEMO_CORPUS=phenol-plant`) |
| :--- | :--- | :--- | :--- |
| **Source PDFs** | `REFERENCE_RAW_DIR` | `corpora/copper-concentrator/raw` (45 PDFs) | `reference/raw` (136 PDFs) |
| **Compiled OKF Wiki** | `REFERENCE_WIKI_DIR` | `corpora/copper-concentrator/wiki` | `reference/wiki` |
| **GCS Prefix** | `DESTINATION_GCS_PREFIX` | `okf-bundles/copper-concentrator` | `okf-bundles/phenol-plant` |
| **UI Profile** | `scripts/corpus_profiles/` | `copper_concentrator.py` | `phenol.py` |
| **Web Runtime** | `extracter_agent/web_server.py` | FastAPI + Google ADK on Cloud Run (`extracter-agent-web`) | FastAPI + Google ADK on Cloud Run |

### 2.2 End-to-End Pipeline Flow
```
plant_model.py (SSOT: Mass Balance + 17 Equipment + 11 Seeded Conflicts + 1 Decoy)
      │
      ▼
generate_corpus.py (Headless Chrome HTML/SVG -> 45 PDFs in corpora/copper-concentrator/raw/)
      │
      ▼
run_extraction.py (Live ADK extracter_orchestrator Mode B -> corpora/copper-concentrator/wiki/)
      │
      ▼
eval_conflicts.py (Scores compiled wiki against SEEDED_CONFLICTS -> eval_results.json)
      │
      ▼
build_demo_assets.py (Loads corpus_profiles.copper_concentrator -> static/data.js + index.html)
```

---

## 3. Data Models & Type Contracts

### 3.1 Plant Model & Seeded Conflict Contract (`scripts/mining_corpus/plant_model.py`)
- `Equip`: dataclass with `tag: str`, `name: str`, `area: str`, `cls: str`, `params: dict[str, tuple[str, str]]`, `function: str`, `connections: list[str]`.
- `SEEDED_CONFLICTS`: list of 11 structured dictionaries (`id` `C01`..`C11`, `tag`, `parameter`, `true_doc`, `true`, `conflict_doc`, `conflict`, `class`, `why`).
- `REVISION_DECOY`: `{"tag": "PP-5101A", "parameter": "Rated flow", "old": ("Rev A", "180 m3/h"), "new": ("Rev B", "210 m3/h")}`.

### 3.2 Corpus Profile Contract (`scripts/corpus_profiles/__init__.py`)
- `Profile`: dataclass with `name: str`, `raw_dir: Path`, `wiki_dir: Path`, `gcs_prefix: str`, `build: Callable`, `harness_required: list[str]`, `harness_forbidden: list[str]`.

---

## 4. API Contracts & Integrations

All existing FastAPI endpoints in `extracter_agent/web_server.py` preserve their HTTP signatures and dynamically serve the active corpus configured via `AppConfig`:
- `GET /api/demo/status`: returns `project_id`, `region`, `gemini_model`, `raw_pdf_count`, `okf_concept_count`, `conflict_count`, and `is_valid_okf`.
- `GET /api/demo/raw-pdfs` & `GET /api/demo/raw-pdf/{subfolder}/{filename}`: serves the active corpus PDFs from `cfg.reference_raw_dir`.
- `GET /api/demo/okf-catalog` & `GET /api/demo/okf-concept/{concept_id:path}`: serves compiled OKF v0.2 concepts and conflict callouts from `cfg.output_bundle_dir` (seeded from `cfg.reference_wiki_dir`).
- `POST /api/demo/parse-pdf`, `POST /api/demo/guardrail-check`, `POST /api/demo/extract-live`: execute live PyMuPDF/Vision parsing, Model Armor pre-flight checks, and ADK extraction against the active corpus.

---

## 5. UI/UX & Behavioral Specifications

1. **Screen 01 (`#macro` — Executive Thesis):** Displays 4 concentrator scenarios (`01 · SAG Shutdown & Isolation`, `02 · Grinding Design Basis`, `03 · Reagent Safety`, `04 · Tailings Pipeline`), empirical conflict recall (`eval_results.json`), and a document-pair discrepancy breakdown chart.
2. **Screen 02 (`#schematic` — Plant & Conflict Twin):** Renders a 12-node concentrator topology across Crushing & SAG Milling (Area 21/31), Ball Milling & Classification (Area 32/41), Reagents & SIS (Area 45/SIS), and Thickening & Tailings (Area 51/61), with interactive node inspection and conflict status derived from `eval_results.json`.
3. **Screen 03 (`#ecosystem` — Persona & Live Workbench):** Presents 4 mining engineering personas (`Maintenance & Shutdown Planner`, `Instrumentation, SIS & Process Safety Engineer`, `Process / Metallurgy Superintendent`, `Tailings Engineer`) coupled to the Dual-Mode Live ADK Workbench.
4. **Screen 04 (`#architecture` — OKF Graph & Cloud Stack):** Interactive SVG property graph of all compiled concentrator concepts and cross-links alongside the 7-layer Google Cloud architecture blueprint.

---

## 6. DevOps, Security & Governance Checklist

- **Rule 8 (Single `.env`):** `DEMO_CORPUS`, `REFERENCE_RAW_DIR`, `REFERENCE_WIKI_DIR`, and `DESTINATION_GCS_PREFIX` managed through `.env` and `extracter_agent/config.py`.
- **Rule 14 (`reference/` Immutability):** Verified via `git status` and automated tests that `reference/raw/` and `reference/wiki/` have 0 modified, added, or deleted files.
- **Model Armor Pre-Flight Security:** `before_agent_callback` remains active across all live workbench requests.
- **SAST & Linting:** `ruff check` and `bandit` pass with zero issues.

---

## 7. Step-by-Step Implementation Plan & Test Design

1. **Step 1 — Plant Model & Synthetic PDF Generator:** Implement `plant_model.py` and `generate_corpus.py`; verify 45 PDFs render cleanly across 5 subfolders.
2. **Step 2 — Live ADK Extraction & Conflict Eval:** Run `run_extraction.py` across all 45 PDFs and score with `eval_conflicts.py` to generate `corpora/copper-concentrator/eval_results.json`.
3. **Step 3 — Profile-Driven Asset Builder & UI Controller:** Wire `scripts/build_demo_assets.py`, `extracter_agent/static/index.template.html`, and `extracter_agent/static/app.js` to `scripts/corpus_profiles/`.
4. **Step 4 — Verification Harness, Unit Tests & E2E UAT:** Run `build_demo_assets.py` (55-check harness), `pytest`, and `run_uat_and_e2e_suite.py`, plus headless browser screenshots of all 4 screens.

---

## 8. Plan Progress Tracking & Living Spec Synchronization

Tracked in the workspace task tracker (`task.md`) and verified against `corpora/copper-concentrator/eval_results.json`.
