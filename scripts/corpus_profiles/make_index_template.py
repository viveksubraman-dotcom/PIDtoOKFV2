"""One-off migration: turn the phenol-specific index.html into a corpus-neutral template.

Every corpus-specific fragment of ``extracter_agent/static/index.html`` is replaced by a
``{{TOKEN}}`` placeholder. The original (phenol) text of each fragment is written to
``scripts/corpus_profiles/phenol_html_tokens.json`` so that rendering the phenol profile
reproduces the original file byte-for-byte (asserted below).

Run once:  python scripts/corpus_profiles/make_index_template.py
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "extracter_agent" / "static" / "index.html"
TEMPLATE = REPO / "extracter_agent" / "static" / "index.template.html"
TOKENS_OUT = Path(__file__).resolve().parent / "phenol_html_tokens.json"

# (TOKEN, exact substring). Each substring must occur exactly once in the source.
INLINE = [
    ("PAGE_TITLE", "P&amp;ID-to-OKF v0.2 Autonomous Process Manufacturing Compiler | 4-Screen Visual Cockpit (Beyond HAZOP)"),
    ("BRAND_TITLE", "P&amp;ID-to-OKF v0.2 Process Mfg Compiler"),
    ("S1_EYEBROW", "PROCESS MANUFACTURING KNOWLEDGE COMPILER &bull; AGENTS = f(PHYSICAL DISCREPANCY)"),
    ("S1_H1", "Autonomous Plant Engineering Compiler: Yield, Reliability, Startup &amp; Safety"),
    ("S1_SPOT_BADGE", "BEYOND HAZOP &bull; YIELD &amp; QUALITY</span>"),
    ("S1_SPOT_CODE", "SCENARIO 01 // YIELD &amp; SELECTIVITY OPTIMIZATION</span>"),
    ("S1_SPOT_TITLE", "AMS Co-Product Yield (&gt;=80 mol%) &amp; DCP Conversion Optimization</div>"),
    ("S1_CHART_TITLE", "Process Manufacturing Complexity vs. Autonomous OKF Compilation"),
    ("S1_CHART_LEGEND", '<div class="legend-item"><span class="dot-blue"></span> PLANT OPS &amp; MOC COMPLEXITY</div>\n            <div class="legend-item"><span class="dot-red"></span> MANUAL SME CAPACITY</div>'),
    ("S1_SVG_ARIA", "Interactive Process Manufacturing P&ID-to-OKF Transformation Schematic and Complexity Inversion"),
    ("S1_SVG_BAND_TITLE", "PROCESS MANUFACTURING COMPILER FLOW // CLICK ANY STAGE TO EXPLORE"),
    ("S1_LEVER_TITLE", "LEVER EXHAUSTION MATRIX (WHY LEGACY OCR &amp; NAIVE RAG FAIL)"),
    ("S1_DRAWER_SUMMARY", "+ INSPECT DETAILED PROCESS MANUFACTURING DOCUMENTATION HEADWINDS &amp; VERIFIED OUTCOMES"),
    ("S1_OUTCOMES_TITLE", "Agentic OKF v0.2 Compiler Outcomes Across Process Manufacturing (ut-interaction-demo)"),
    ("S2_EYEBROW", "PROCESS MANUFACTURING PLANT TOPOLOGY (YIELD, RELIABILITY, STARTUP &amp; MOC)"),
    ("S2_H1", "12-Node Process Plant &amp; Multi-Scenario Reconciliation Twin"),
    ("S2_STEPPER_DEFAULT", "NODE 5/12 &bull; D-2304"),
    ("S2_CONFLICT_BADGE", "21 Active Conflicts Flagged"),
    ("S2_DRAWER_ISA", '>UNIT-23</span>'),
    ("S2_DRAWER_TITLE", "D-2304 — Decomposer CSTR &amp; Calorimeter X-2308"),
    ("S2_DRAWER_LENS", "YIELD &bull; RELIABILITY &bull; MOC"),
    ("S2_DRAWER_SAP", ">CONFLICT-D2304-X2311</div>"),
    ("S2_TELEMETRY_SUMMARY", "+ EXPAND ALL 12 PROCESS PLANT EQUIPMENT, YIELD, RELIABILITY &amp; MOC TELEMETRY CARDS"),
    ("S2_TELEMETRY_BADGE", ">12 NODES</span>"),
    ("S3_EYEBROW", "PROCESS MANUFACTURING PLANT WORKFORCE &amp; DUAL-MODE LIVE ADK WORKBENCH"),
    ("S3_COUNT_BADGE", "130 CONCEPTS &bull; 136 PDFS"),
    ("S3_PERSONA_ARIA", "Select Process Manufacturing Engineering Persona"),
    ("S3_PERSONA_INITIALS", '<span id="persona-hero-initials">PY</span>'),
    ("S3_PERSONA_CODE", "PERSONA 01 // YIELD &amp; PROCESS OPTIMIZATION</span>"),
    ("S3_PERSONA_TITLE", "Lead Process &amp; Yield Optimization Engineer</strong>"),
    ("S3_PERSONA_SPEED", "16h MANUAL &rarr; 4m AUTONOMOUS"),
    ("S3_DAG_STEP1", "136 PDFs &bull; MD5 Index"),
    ("S3_DAG_STEP4", '#D93025">21 CONFLICT Callouts</text>\n            <text x="82"'),
    ("S3_DAG_STEP5", "139 Files &bull; 0 Broken"),
    ("S3_MODE_A", "Mode A: Entity-Centric (130 OKF Concepts)"),
    ("S3_MODE_B", "Mode B: File-by-File Incremental (136 Raw PDFs)"),
    ("S3_MD_BADGE", "139 MD FILES &bull; 0 BROKEN LINKS"),
    ("S3_CONCEPT_LABEL", "Select Compiled OKF v0.2 Concept (130 Golden Concepts)"),
    ("S3_PDF_LABEL", "Select Governing Raw Engineering PDF (136 PDFs in reference/raw/)"),
    ("S3_PROMPT_DEFAULT", "Mode A Entity-Centric: Extract and compile OKF v0.2 concept 'equipment/D-2304' reconciling Process Data Sheet, P&ID, and PFD sources."),
    ("S3_OUTPUT_TITLE", "build/okf_bundle/equipment/D-2304.md"),
    ("S4_H1", "125-Node Cross-Linked OKF Graph &amp; 7-Layer Cloud Stack"),
    ("S4_GCS_PATH", "gs://ut-interaction-demo-okf-knowledge/okf-bundles/phenol-plant"),
    ("S4_GRAPH_H2", "Interactive OKF v0.2 Property Graph (125 Domain Nodes &bull; 866 Cross-Links)"),
    ("S4_STAT_PDFS", '<div class="datagraph-stat-value tnum">136</div>'),
    ("S4_STAT_CONCEPTS", '<div class="datagraph-stat-value tnum">130</div>'),
    ("S4_STAT_CONFLICTS", 'color:var(--m3-critical);">21</div>'),
    ("S4_LEGEND_CONFLICT", "Conflict Flagged (21)"),
    ("S4_ARCH_SUPERSESSION", "Rev Z0&rarr;Z1 Supersession"),
    ("S4_ARCH_CONFLICTS", '#D93025">21 CONFLICT Callouts</text>\n          <text x="97"'),
    ("S4_ARCH_RAW", "136 Raw PDFs (Read-Only)"),
    ("S4_ARCH_MD", "139 OKF Markdown Blobs"),
]

# (TOKEN, first line, last line) 1-based inclusive line ranges of the ORIGINAL file (whole lines).
BLOCKS = [
    ("S1_HERO_DESC", 50, 50),
    ("S1_HERO_BADGES", 54, 56),
    ("S1_KPI_RIBBON", 88, 107),
    ("S1_NODE_A", 134, 137),
    ("S1_NODE_B", 148, 151),
    ("S1_NODE_C", 162, 165),
    ("S1_SVG_BOTTOM", 168, 201),
    ("S1_BENCH_HEAD", 209, 214),
    ("S1_SOWHAT", 244, 244),
    ("S2_ZONES", 281, 367),
    ("S2_SOWHAT", 440, 440),
    ("S4_SOWHAT", 895, 895),
]


def main() -> None:
    original = SRC.read_text(encoding="utf-8")
    lines = original.split("\n")
    tokens: dict[str, str] = {}

    # 1) Whole-line blocks first (bottom-up so line numbers stay valid).
    for name, a, b in sorted(BLOCKS, key=lambda t: -t[1]):
        chunk = "\n".join(lines[a - 1 : b])
        tokens[name] = chunk
        lines[a - 1 : b] = ["{{" + name + "}}"]
    text = "\n".join(lines)

    # 2) Inline substrings.
    for name, snippet in INLINE:
        cnt = text.count(snippet)
        assert cnt == 1, f"{name}: expected 1 occurrence, found {cnt}"
        tokens[name] = snippet
        text = text.replace(snippet, "{{" + name + "}}", 1)

    # 3) Round-trip proof.
    rendered = text
    for name, val in tokens.items():
        rendered = rendered.replace("{{" + name + "}}", val, 1)
    assert rendered == original, "phenol round-trip is not byte-identical"

    TEMPLATE.write_text(text, encoding="utf-8")
    TOKENS_OUT.write_text(json.dumps(tokens, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"template: {TEMPLATE} | {len(tokens)} tokens | phenol round-trip byte-identical")


if __name__ == "__main__":
    main()
