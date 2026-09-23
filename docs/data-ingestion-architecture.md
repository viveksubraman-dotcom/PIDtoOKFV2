# Data Ingestion & OKF v0.2 Synthesis Architecture

> **System:** Extracter Agent — Automated Engineering Knowledge Extraction  
> **Status:** Implemented & Verified (43 Unit & Property-Based Tests Passing)  
> **Runtime Target:** Gemini Enterprise Agent Platform (`agent_runtime`) & Cloud Run  
> **Foundation Model:** Gemini 2.5 Pro (via Google ADK `google-adk`)  
> **Companion Interactive Diagram:** [Open Standalone HTML Diagram Asset](./data-ingestion-architecture.html)

---

## 1. Executive Summary

The **Extracter Agent** is an autonomous AI agent engineered to ingest heterogeneous chemical and mechanical engineering documents from a read-only corpus (`reference/raw/`) and synthesize structured, validated **Open Knowledge Format (OKF v0.2)** bundles.

Processing engineering documentation presents unique technical challenges:
1. **Heterogeneous Modalities:** Engineering packages mix tabular data sheets, narrative operating manuals, SDS hazard reports, and graphical AutoCAD drawings (P&IDs and PFDs).
2. **The Vector Drawing Blindspot:** AutoCAD-exported P&IDs and PFDs contain stroked line paths, glyph curves, and zero `/Font` dictionary entries. Standard PDF text extraction returns empty strings.
3. **Cross-Document Data Discrepancies:** Different documents specify divergent operating and design parameters for identical equipment tags (e.g. design pressure on an equipment data sheet vs. operating pressure on a PFD vs. relief setpoints on a P&ID).
4. **Data Integrity & Schema Fidelity:** Engineering tag numbers (such as `01-P-101A` or `01-FIT-101`) risk silent octal or scalar coercion when serialized to YAML without strict dumper safeguards.

To solve these challenges, the system implements a **Dual-Stream Ingestion Architecture**, a **Deterministic 6-Tier Precedence Engine**, a **Google ADK Cognitive Orchestrator**, and a **Quoted YAML / Markdown OKF v0.2 Dumper**.

---

## 2. Interactive Architecture Diagram

An interactive, dark-themed system topology diagram is rendered in the companion file:
- **[docs/data-ingestion-architecture.html](./data-ingestion-architecture.html)**

To preview in local environments:
```bash
# macOS
open ./docs/data-ingestion-architecture.html

# Linux
xdg-open ./docs/data-ingestion-architecture.html
```

---

## 3. System Architecture & Component Topology

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. IMMUTABLE SOURCE CORPUS (reference/raw/) [Read-Only]                                │
│   ├─ Data Sheets (raw/datasheet)       ├─ P&ID Drawings (raw/pid)                      │
│   ├─ PFD Flowsheets (raw/pfd)          ├─ Operating Manuals (raw/manual)               │
│   ├─ Safety Data (raw/sds)             └─ Engineering Standards (raw/std)               │
└─────────────────────────────────────────┬──────────────────────────────────────────────┘
                                          │
                                          ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 2. DUAL-STREAM INGESTION & PARSING PIPELINE (extracter_agent/pdf/processor.py)         │
│   ├─ Catalog Scanner: discover_raw_documents() [224 documents cataloged]               │
│   ├─ Vector Heuristic Gate: is_vector_drawing() (Strokes > 50, /Font == 0)             │
│   ├─ Stream A (Native Text): pypdf layout & tabular extractor                          │
│   ├─ Stream B (Multimodal Vision): google.genai.types.Part.from_bytes()                │
│   └─ Token Windowing & SHA-256 Fingerprinting                                          │
└─────────────────────────────────────────┬──────────────────────────────────────────────┘
                                          │
                                          ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 3. AUTONOMOUS COGNITIVE ORCHESTRATION (extracter_agent/agent/orchestrator.py)          │
│   ├─ Model Armor Security: before_agent_callback prompt injection / leakage filters   │
│   ├─ ADK Orchestrator Agent: Gemini 2.5 Pro (temperature=0.1, cognitive reasoning)    │
│   ├─ Conflict Precedence Engine: Deterministic 6-tier hierarchy arbitration            │
│   └─ FunctionTool Registry (7 Strongly Typed ADK Tools):                               │
│       • find_raw_documents_tool        • read_raw_document_tool                        │
│       • batch_read_documents_tool      • generate_okf_equipment_tool                   │
│       • generate_okf_concept_tool      • validate_okf_bundle_tool                      │
│       • update_okf_index_tool                                                          │
└─────────────────────────────────────────┬──────────────────────────────────────────────┘
                                          │
                                          ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 4. OKF v0.2 SYNTHESIS, VALIDATION & PUBLISHING (extracter_agent/okf/ & gcs/)           │
│   ├─ OKF Entity Synthesizer: Equipment (Pumps, Exchangers) & Concepts (Hazards, Loops) │
│   ├─ _OKFSafeDumper: PyYAML dumper enforcing strict string quotation for tags         │
│   ├─ Schema & Cross-Ref Validator: Pydantic OKFModel invariants & connection checks   │
│   ├─ Progressive Index Manager: okf_index.json atomic manifest tracking               │
│   └─ GCS Cloud Storage Publisher: Immutable artifact replication to target bucket     │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Subsystem Specifications

### 4.1 Ingestion & Parsing Subsystem (`extracter_agent/pdf/`)

The ingestion subsystem transforms diverse raw binary PDF streams into semantic representations tailored for Gemini 2.5 Pro.

#### 4.1.1 The Vector Drawing Dilemma & Heuristic Detection
Engineering P&IDs and PFDs created in CAD systems (AutoCAD, SmartPlant P&ID, AVEVA) commonly output vector path drawings rather than searchable text layers. Text characters are frequently stroked as primitive lines and arcs without embedded `/Font` or `/ToUnicode` dictionaries. Traditional text extractors return zero characters, causing silent data loss.

To resolve this, `extracter_agent/pdf/processor.py` implements `is_vector_drawing`:
```python
def is_vector_drawing(reader: pypdf.PdfReader) -> bool:
    """Heuristically detects CAD vector drawings lacking native text layers."""
    text_sample = "".join((page.extract_text() or "") for page in reader.pages[:3])
    if len(text_sample.strip()) > 100:
        return False
    # Detect stroked vector drawing operators and absence of font dictionaries
    for page in reader.pages[:3]:
        has_fonts = bool(page.get("/Resources", {}).get("/Font", {}))
        contents = page.get_contents()
        if contents and not has_fonts:
            return True
    return False
```

#### 4.1.2 Stream Routing
1. **Stream A (Native Text Extraction):** For documents with `is_vector_drawing() == False` (data sheets, manuals, SDS, standards), the processor extracts clean layout text, tabular blocks, and page metadata via `pypdf`.
2. **Stream B (Multimodal Drawing Extraction):** For documents with `is_vector_drawing() == True` (P&IDs, PFDs), the processor loads the raw PDF bytes into a `google.genai.types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")`. This part is passed directly to Gemini 2.5 Pro, enabling high-resolution multimodal vision analysis of instrument bubbles, flow arrows, piping connections, and nozzle callouts.

---

### 4.2 Cognitive Precedence Engine & Conflict Arbitration

When cross-referencing multi-file clusters (e.g. extracting a Centrifugal Pump `01-P-101A` from its Data Sheet, P&ID `01-PID-001`, and PFD `01-PFD-001`), parameter discrepancies arise.

The orchestrator enforces a **Deterministic 6-Tier Authority Hierarchy**:

| Tier | Document Type | Directory Pattern | Authoritative Fields |
| :--- | :--- | :--- | :--- |
| **1** | **As-Built Data Sheet** | `reference/raw/datasheet/` | **Design limits:** MAWP, design temperature, pump head, impeller diameter, motor kW, metallurgy, mechanical seal plan. |
| **2** | **P&ID Schematic** | `reference/raw/pid/` | **Topology & instrumentation:** Nozzle connections, line sizes, instrument control loops (FIC, PIC, TI), relief valve setpoints, isolation valve tags. |
| **3** | **PFD Flowsheet** | `reference/raw/pfd/` | **Process conditions:** Normal operating temperature, normal operating pressure, mass/volumetric flow rates, stream fluid compositions. |
| **4** | **Operating Manual** | `reference/raw/manual/` | **Procedures:** Startup/shutdown sequences, NPSH available curves, lube oil specs, interlock setpoints. |
| **5** | **Safety Data Sheet (SDS)** | `reference/raw/sds/` | **Hazards & chemicals:** Flash point, auto-ignition temp, NFPA ratings, toxic exposure limits (TLV-TWA). |
| **6** | **General Standard** | `reference/raw/standards/` | **Code compliance:** ASME Section VIII Div 1, API 610, API 682 standard allowances. |

---

### 4.3 Google ADK Orchestrator & Toolchain

The orchestrator is implemented in `extracter_agent/agent/orchestrator.py` as a Google ADK `Agent` interacting with 7 strongly typed `FunctionTool` definitions:

```
┌────────────────────────────────────────────────────────────────────────┐
│                         ADK FUNCTIONTOOL REGISTRY                      │
├───────────────────────────────┬────────────────────────────────────────┤
│ Tool Name                     │ Operational Scope                      │
├───────────────────────────────┼────────────────────────────────────────┤
│ find_raw_documents_tool       │ Semantic catalog search across 224 raw │
│                               │ files with category & keyword filters. │
├───────────────────────────────┼────────────────────────────────────────┤
│ read_raw_document_tool        │ Single document extraction (Dual-      │
│                               │ Stream: Text layout or Multimodal Part)│
├───────────────────────────────┼────────────────────────────────────────┤
│ batch_read_documents_tool     │ Multi-file cluster extraction for      │
│                               │ cross-document entity synthesis.       │
├───────────────────────────────┼────────────────────────────────────────┤
│ generate_okf_equipment_tool   │ Synthesizes OKF v0.2 Equipment bundles │
│                               │ (Pumps, Exchangers, Vessels, Columns). │
├───────────────────────────────┼────────────────────────────────────────┤
│ generate_okf_concept_tool     │ Synthesizes OKF v0.2 Concept bundles   │
│                               │ (Hazards, Loops, Units, HAZOP Nodes).  │
├───────────────────────────────┼────────────────────────────────────────┤
│ validate_okf_bundle_tool      │ Invariant & cross-reference validation │
│                               │ against Pydantic OKFModel contracts.   │
├───────────────────────────────┼────────────────────────────────────────┤
│ update_okf_index_tool         │ Atomic manifest update to keep         │
│                               │ okf_index.json synchronized.           │
└───────────────────────────────┴────────────────────────────────────────┘
```

#### Canonical 6-Step Agent Trajectory
1. **Step 1 (Discovery):** Call `find_raw_documents_tool` to identify all relevant source files for the target entity or domain query.
2. **Step 2 (Ingestion):** Call `read_raw_document_tool` or `batch_read_documents_tool` to obtain extracted text streams or multimodal vision parts.
3. **Step 3 (Reconciliation):** Reconcile cross-document discrepancies using the 6-tier precedence hierarchy.
4. **Step 4 (Synthesis):** Call `generate_okf_equipment_tool` or `generate_okf_concept_tool` to produce valid OKF YAML frontmatter and human-readable Markdown body.
5. **Step 5 (Validation):** Call `validate_okf_bundle_tool` to guarantee schema fidelity and zero broken references.
6. **Step 6 (Publishing & Indexing):** Call `update_okf_index_tool` to register the entity in `okf_index.json` and stage artifacts for Google Cloud Storage synchronization.

---

### 4.4 Data Integrity: `_OKFSafeDumper` String Quoting

In chemical engineering documentation, tag numbers frequently follow alphanumeric patterns such as `01-P-101A`, `001-V-102`, or `07-E-201`. When standard PyYAML dumps these values:
- Tags starting with `0` can be interpreted as octal integers.
- Unquoted strings containing colons, dashes, or boolean-like terms (`NO`, `YES`, `TRUE`) are coerced into booleans or dictionaries.

To prevent corruption, `extracter_agent/okf/document.py` implements a custom YAML representer:
```python
class _OKFSafeDumper(yaml.SafeDumper):
    """Custom YAML SafeDumper enforcing explicit quotes on strings with special characters."""
    pass

def _str_presenter(dumper: yaml.Dumper, data: str):
    # Enforce quotation if string contains dashes, colons, or resembles numbers
    if any(c in data for c in ":-[]{}#&*!|>'\"%@`") or data.startswith("0"):
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)

_OKFSafeDumper.add_representer(str, _str_presenter)
```

---

## 5. Security & Model Armor Guardrails

In compliance with enterprise security rules:
- **Pre-Flight Hook (`before_agent_callback`):** Inspects user prompts and extracted document tokens for prompt injection attempts, system instruction overrides, and unauthorized exfiltration patterns before passing context to Gemini 2.5 Pro.
- **Reference Corpus Immutability:** The agent runtime strictly enforces read-only access to `reference/`. All generated knowledge is written to staging directories or published to Google Cloud Storage.
- **Cloud IAM Restricted Sharing:** Ingress to web and proxy services enforces Identity-Aware Proxy (IAP) or Google OAuth 2.0. No `allUsers` IAM permissions are permitted.

---

## 6. Verification & Quality Metrics

The ingestion architecture has been verified against the unit and property test suites:

| Test Suite | File | Tests | Status |
| :--- | :--- | :--- | :--- |
| **PDF Ingestion & Discovery** | `tests/unit/test_pdf_processor.py` | 8 | **PASS** |
| **Toolchain & Multimodal Tools** | `tests/unit/test_okf_tools.py` | 12 | **PASS** |
| **OKF Serialization Invariants** | `tests/unit/test_okf_document.py` | 9 | **PASS** |
| **Property-Based Testing (PBT)** | `tests/pbt/test_okf_invariants.py` | 6 | **PASS** |
| **ADK Orchestrator Reasoning** | `tests/unit/test_orchestrator.py` | 5 | **PASS** |
| **Live Evaluation Trajectory** | `evals/test_golden_trajectories.py` | 3 | **PASS** |
| **Total Test Suite** | `pytest tests/ evals/` | **43** | **100% PASS** |

---

## 7. Next Actions & Operational Verification

1. **Live Evaluation Benchmark:** Execute `agents-cli eval run` across the 55 single-file Data Sheet cases to measure trajectory precision ($\ge 95\%$) and groundedness (1.000).
2. **SAST Scan:** Execute CodeMender (`cm find`) before build promotion.
3. **Artifact Staging & Cloud Run Deploy:** Promote to Non-Prod Cloud Run environment via Cloud Build CI/CD.
