#!/usr/bin/env python3
"""Builds the Mining M3 Light Executive Demo Cockpit assets from real OKF & PDF artifacts.

Generates:
  1. extracter_agent/static/data.js
  2. extracter_agent/static/app.js
  3. extracter_agent/static/index.html
  4. Standalone self-contained HTML artifact in brain directory
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from corpus_profiles import Profile
from corpus_profiles import load as load_profile

STATIC_DIR = REPO_ROOT / "extracter_agent" / "static"
TEMPLATE_PATH = STATIC_DIR / "index.template.html"
BUNDLE_DIR = REPO_ROOT / "build" / "okf_bundle"
WIKI_DIR = REPO_ROOT / "reference" / "wiki"
RAW_DIR = REPO_ROOT / "reference" / "raw"
BRAIN_ARTIFACT = Path(
    "/usr/local/google/home/viveksubraman/.gemini/jetski/brain/"
    "ebe0626f-e99d-42a7-9bf9-1e8745dcf94f/pid_to_okf_mining_executive_demo.html"
)
CURRENT_BRAIN_ARTIFACT = Path(
    "/usr/local/google/home/viveksubraman/.gemini/jetski/brain/"
    "2de3f51c-4543-4cf1-a604-b3fc52c9e87a/pid_to_okf_mining_executive_demo.html"
)


def _parse_frontmatter_and_body(md_text: str) -> tuple[dict[str, Any], str]:
    if md_text.startswith("---"):
        parts = md_text.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
                if isinstance(fm, dict):
                    return fm, parts[2].strip()
            except Exception as exc:
                print(f"Warning parsing frontmatter: {exc}")
    return {}, md_text.strip()


def collect_raw_pdfs(raw_dir: Path | None = None) -> list[dict[str, Any]]:
    active_raw = raw_dir or RAW_DIR
    pdfs: list[dict[str, Any]] = []
    if not active_raw.exists():
        return pdfs
    for p in sorted(active_raw.rglob("*")):
        if not p.is_file() or p.name.startswith(".") or p.suffix.lower() != ".pdf":
            continue
        rel = p.relative_to(active_raw).as_posix()
        parts = rel.split("/", 1)
        subfolder = parts[0] if len(parts) > 1 else "root"
        filename = parts[1] if len(parts) > 1 else parts[0]
        pdfs.append(
            {
                "subfolder": subfolder,
                "file_name": filename,
                "relative_path": rel,
                "size_kb": round(p.stat().st_size / 1024.0, 1),
                "is_vector_cad": subfolder in ("pid", "pfd"),
                "view_url": f"/api/demo/raw-pdf/{subfolder}/{filename}",
            }
        )
    return pdfs


def collect_okf_concepts(
    wiki_dir: Path | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    if wiki_dir is not None:
        active_dir = wiki_dir
    else:
        active_dir = BUNDLE_DIR if BUNDLE_DIR.exists() else WIKI_DIR
    concepts: list[dict[str, Any]] = []
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    seen_nodes: set[str] = set()

    for p in sorted(active_dir.rglob("*.md")):
        rel = p.relative_to(active_dir).as_posix()
        if rel.endswith("/index.md") or p.name.startswith("_"):
            continue
        txt = p.read_text(encoding="utf-8")
        fm, _body = _parse_frontmatter_and_body(txt)
        concept_id = rel.removesuffix(".md")
        cat = concept_id.split("/")[0] if "/" in concept_id else "root"
        title = str(
            fm.get("title")
            or fm.get("name")
            or fm.get("tag")
            or concept_id.split("/")[-1]
        )
        ctype = str(fm.get("type") or cat.capitalize())
        unit = str(fm.get("unit") or fm.get("code") or "CDN")
        raw_sources = fm.get("sources") or fm.get("source") or fm.get("file") or []
        sources: list[str] = []
        if isinstance(raw_sources, list):
            for s in raw_sources:
                if isinstance(s, dict):
                    sources.append(str(s.get("resource") or s.get("title") or s.get("path") or s))
                else:
                    sources.append(str(s))
        elif isinstance(raw_sources, str) and raw_sources.strip():
            sources.append(raw_sources.strip())
        if not sources:
            sources.append(f"reference/wiki/{rel}")

        conflict_lines = (
            [line.strip() for line in txt.splitlines() if "CONFLICT" in line]
            if rel not in ("index.md", "log.md")
            else []
        )
        links = sorted(set(re.findall(r"\[\[([^\]|#]+)", txt)))

        concepts.append(
            {
                "concept_id": concept_id,
                "category": cat,
                "title": title,
                "type": ctype,
                "unit": unit,
                "tags": [str(t) for t in (fm.get("tags") or [])]
                if isinstance(fm.get("tags"), list)
                else [],
                "sources": sources,
                "has_conflict": len(conflict_lines) > 0,
                "conflict_summary": conflict_lines[0][:220] if conflict_lines else "",
                "cross_links": links[:12],
                "size_bytes": len(txt.encode("utf-8")),
                "markdown": txt,
            }
        )

        if concept_id not in seen_nodes and cat in (
            "equipment",
            "instruments",
            "hazards",
            "procedures",
            "units",
            "hazop",
            "troubleshooting",
            "sources",
        ):
            seen_nodes.add(concept_id)
            nodes.append(
                {
                    "id": concept_id,
                    "label": concept_id.split("/")[-1],
                    "title": title,
                    "category": cat,
                    "unit": unit,
                    "has_conflict": len(conflict_lines) > 0,
                    "sources_count": len(sources),
                    "links_count": len(links),
                }
            )

    has_wiki_syntax = any(c["cross_links"] for c in concepts)
    label_to_cid = {
        n["label"]: n["id"] for n in nodes if len(n["label"]) >= 4
    }
    node_by_id = {n["id"]: n for n in nodes}

    for c in concepts:
        src_id = c["concept_id"]
        if not has_wiki_syntax and src_id not in ("index", "log"):
            txt = c["markdown"]
            md_links = [
                m.lstrip("/").removesuffix(".md")
                for m in re.findall(r"\]\((/[^)#\s]+\.md)", txt)
            ]
            tag_links = [
                target_cid
                for lbl, target_cid in label_to_cid.items()
                if target_cid != src_id and lbl in txt
            ]
            resolved = [
                lnk
                for lnk in sorted(set(md_links + tag_links))
                if lnk in seen_nodes and lnk != src_id
            ][:12]
            c["cross_links"] = resolved
            if src_id in node_by_id:
                node_by_id[src_id]["links_count"] = len(resolved)

        if src_id not in seen_nodes:
            continue
        for target_raw in c["cross_links"]:
            target_clean = target_raw.strip()
            target_clean = target_clean.removesuffix(".md")
            if target_clean in seen_nodes and target_clean != src_id:
                edges.append({"source": src_id, "target": target_clean})

    return concepts, nodes, edges


def _default_phenol_static_data(
    raw_pdfs: list[dict[str, Any]],
    concepts: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    conflict_nodes: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "meta": {
            "project_id": "ut-interaction-demo",
            "region": "asia-southeast1",
            "gemini_location": "global",
            "gemini_model": "gemini-3.8-flash",
            "gcs_bucket": "gs://ut-interaction-demo-okf-knowledge",
            "gcs_prefix": "okf-bundles/phenol-plant",
            "raw_pdf_count": len(raw_pdfs),
            "okf_concept_count": len(concepts),
            "total_markdown_files": 139,
            "conflict_count": len(conflict_nodes),
            "broken_links": 0,
        },
        "summary": {
            "total_raw_pdfs": len(raw_pdfs),
            "total_okf_concepts": len(concepts),
            "conflict_concepts_count": len(conflict_nodes),
            "graph_node_count": len(nodes),
            "graph_edge_count": len(edges),
        },
        "conflict_nodes": conflict_nodes,
        "manufacturing_scenarios": [
            {
                "id": "yield_optimization",
                "code": "SCENARIO 01 // YIELD & SELECTIVITY OPTIMIZATION (BEYOND HAZOP)",
                "short_label": "01 · Yield & Selectivity",
                "title": "AMS Co-Product Yield (>=80 mol%) & DCP Conversion Optimization",
                "beyond_hazop": True,
                "badge": "BEYOND HAZOP • YIELD & QUALITY",
                "kpi_delta": ">= 80 mol% AMS",
                "speedup": "16h -> 4m",
                "concept_id": "troubleshooting/cdn-poor-ams-yield",
                "secondary_concept_id": "parameters/cdn-operating-windows",
                "raw_pdf": "operating_manuals/OM-Phenol Unit UOP-2015.pdf",
                "schematic_node_id": "v2401",
                "persona_idx": 0,
                "challenge": (
                    "Co-product Alpha-Methylstyrene (AMS) selectivity drops below the >= 80 mole% "
                    "licensor target when Dicumylperoxide (DCP) over-converts (< 300 wt ppm vs. "
                    "300-700 wt ppm target) due to E-2308A/B dehydrator temperature exceeding "
                    "125-145 deg C or CSTR H2SO4 catalyst drifting outside 40-60 wt ppm."
                ),
                "derivation": (
                    "dT_calorimeter (X-2308) = 7.2 deg C per wt% CHP (target 7-10 deg C at 1.0-1.5 wt% CHP, "
                    "36s residence) | DCP Target: 300-700 wt ppm (max 900 wt ppm per o-cresol spec)"
                ),
                "impact": (
                    "Restores >= 80 mole% AMS selectivity, protects 99.99 wt% Phenol purity (<= 100 wt ppm H2O), "
                    "and compresses cross-document yield excursion root-cause diagnosis from 16 hours to 4 minutes."
                ),
            },
            {
                "id": "fouling_reliability",
                "code": "SCENARIO 02 // FOULING, ACIDITY & ASSET RELIABILITY (BEYOND HAZOP)",
                "short_label": "02 · Fouling & Reliability",
                "title": "Exchanger Polymer Fouling (E-2308), Flash Acidity & Seal Plan Integrity",
                "beyond_hazop": True,
                "badge": "BEYOND HAZOP • RELIABILITY",
                "kpi_delta": "1-3 mo Cycle Extended",
                "speedup": "2,020 vs 3,020 m3/h",
                "concept_id": "troubleshooting/cdn-dehydrator-plugging",
                "secondary_concept_id": "instruments/pump-seal-plans",
                "raw_pdf": "pid/14780-8120-25-23-0001K_P&ID CDN UNIT TYPICAL PUMP SEAL PLAN(3-4)_Z1.pdf",
                "schematic_node_id": "p2302",
                "persona_idx": 1,
                "challenge": (
                    "Dehydrator E-2308A/B suffers 1-3 month tube plugging from heavy phenolic polymer "
                    "after 300 wt ppm H2SO4 startup spikes; Flash Column crude product pH drops below 2.3 "
                    "(organic acid breakthrough); P-2302A/B exhibits a 1,000 m3/h P&ID vs. Datasheet flow conflict."
                ),
                "derivation": (
                    "Dehydrator dP Surge: H2SO4 > 60 wt ppm + T > 145 deg C -> Polymer Plugging | "
                    "Flash Crude pH: 2.3-2.7 (Spent Air O2 >= 5 vol%) | P-2302A/B API Plan 11/53A Dual Seal"
                ),
                "impact": (
                    "Eliminates premature E-2308A/B tube plugging, prevents column organic acid corrosion (pH < 2.3), "
                    "and reconciles hydraulic curves & API Plan 11/53A / 2/53A seal piping across 14 pump packages."
                ),
            },
            {
                "id": "startup_envelope",
                "code": "SCENARIO 03 // COLD-START & OPERATING ENVELOPE (BEYOND HAZOP)",
                "short_label": "03 · Cold-Start & Envelope",
                "title": "5-Gate Cold-Start Readiness & CSTR Temperature Step-Down Execution",
                "beyond_hazop": True,
                "badge": "BEYOND HAZOP • OPERATIONS",
                "kpi_delta": "5-Gate Feed-In",
                "speedup": "1 deg C / 15 min",
                "concept_id": "procedures/startup-cdn",
                "secondary_concept_id": "parameters/cdn-operating-windows",
                "raw_pdf": "operating_manuals/OM-Phenol Unit UOP-2015.pdf",
                "schematic_node_id": "r2201",
                "persona_idx": 2,
                "challenge": (
                    "Transitioning from cold circulation to exothermic cleavage requires simultaneous "
                    "verification of 5 'Ready for Feed In' gates across SOP manuals, P&IDs, and DCS loops "
                    "before stepping CSTR temperature down from 70 deg C to 60 deg C."
                ),
                "derivation": (
                    "Gate 1: T_decomp = 70 deg C | Gate 2: H2SO4 = 300 wt ppm | Gate 3: H2O < 2 wt% | "
                    "Gate 4: Water Inj = 0 kg/h | Gate 5: Cumene Double-Flush -> Step-down 1 deg C per >= 15 min"
                ),
                "impact": (
                    "Standardizes shift-to-shift cold startup and grade transitions, accounting for 36-second "
                    "Calorimeter X-2308 lag and <= 5% acid steps to prevent startup off-spec slop."
                ),
            },
            {
                "id": "turnaround_hazop",
                "code": "SCENARIO 04 // TURNAROUND LOTO, MOC & PROCESS SAFETY (HAZOP)",
                "short_label": "04 · Turnaround, MOC & HAZOP",
                "title": "As-Built Datasheet vs. P&ID Reconciliation, LOTO Isolation & PHA",
                "beyond_hazop": False,
                "badge": "TURNAROUND, MOC & HAZOP",
                "kpi_delta": "21 Conflicts Flagged",
                "speedup": "14d -> 18m",
                "concept_id": "equipment/D-2304",
                "secondary_concept_id": "equipment/V-2301",
                "raw_pdf": "data_sheets/14780-8120-PS-D2304_D-2304 PROCESS DATA SHEET_Z1.pdf",
                "schematic_node_id": "d2304",
                "persona_idx": 3,
                "challenge": (
                    "Reconciling 55 As-Built Process Data Sheets against 46 AutoCAD P&IDs uncovers 21 active "
                    "mechanical, hydraulic, and chemical conflicts (e.g., D-2304 burst disc 12.16 vs 11.0 kg/cm2g; "
                    "V-2301 21,000 vs 7,550 mm T/T; E-2307 13.0 vs 1.3 kg/cm2g; D-2312 HMDA vs TBC)."
                ),
                "derivation": (
                    "Rule: As-Built Process Data Sheet governs mechanical ratings; P&ID governs SIS/instrument "
                    "loops (2oo3 TXSHH/FXSLL) | Rev Z0->Z1 updated in-place; cross-doc conflicts flagged"
                ),
                "impact": (
                    "Compresses Turnaround LOTO blind-list, Management of Change (MOC), and PHA/HAZOP preparation "
                    "from 14 days to 18 minutes with 100% conflict capture and zero broken links."
                ),
            },
        ],
        "benchmark_bars": [
            {
                "label": "Autonomous ADK OKF v0.2 Compiler (Mode A + Mode B)",
                "val": 98.6,
                "display": "98.6%",
                "primary": True,
            },
            {
                "label": "Mode B Incremental Read-Merge-Upsert (136 Raw PDFs)",
                "val": 97.4,
                "display": "97.4%",
                "primary": True,
            },
            {
                "label": "Cross-Document Conflict Detection (Datasheet vs. P&ID)",
                "val": 100.0,
                "display": "100.0%",
                "primary": True,
            },
            {
                "label": "Model Armor Adversarial Prompt-Injection Block Rate",
                "val": 100.0,
                "display": "100.0%",
                "primary": True,
            },
            {
                "label": "Standard Multi-Document Vector Chunk RAG Baseline",
                "val": 68.2,
                "display": "68.2%",
                "primary": False,
            },
            {
                "label": "Single-Turn Raw PDF Context Stuffing Baseline",
                "val": 51.4,
                "display": "51.4%",
                "primary": False,
            },
        ],
        "headwinds": [
            {
                "title": "Vector CAD P&ID & Seal Plan Blindness",
                "badge": "46 DRAWINGS",
                "val": "0",
                "unit": "Bytes Text Stream",
                "baseline": "300 DPI Vision Required",
                "desc": "AutoCAD-plotted P&IDs (DWG 25-23-0001..0046, including API Seal Plans 11/53A & 2/53A) contain zero embedded text streams. Standard OCR drops nozzle marks, control loops, and seal piping.",
                "fill": 88,
            },
            {
                "title": "Siloed Yield, Fouling & Operating Windows",
                "badge": "SOP VS P&ID",
                "val": "80.0",
                "unit": "mol% AMS Target",
                "baseline": "DCP 300-700 wt ppm",
                "desc": "Licensor operating manuals (125-145 deg C dehydrator window, Calorimeter X-2308 7.2 deg C/wt% CHP, 1-3 mo fouling rules) sit disconnected from P&ID tags and vendor datasheets.",
                "fill": 84,
            },
            {
                "title": "Cross-Document Rating & Flow Conflicts",
                "badge": "21 CONFLICTS",
                "val": "21",
                "unit": "Active Discrepancies",
                "baseline": "Datasheet vs. P&ID",
                "desc": "As-Built Data Sheets (PS-P2302: 2,020 m3/h; PS-V2301: 21,000 mm T/T; PS-D2304: 11.0 kg/cm2g) conflict with P&ID figures (3,020 m3/hr; 7,550 mm; 12.16 kg/cm2g) across reliability, MOC, and HAZOP.",
                "fill": 92,
            },
        ],
        "levers": [
            {
                "tag": "LEVER 01 // MANUAL SME INDEXING",
                "title": "Spreadsheet Tag Takeoffs",
                "desc": "4-6 weeks per plant unit to manually cross-check 55 datasheets, 46 P&IDs, and SOP manuals for yield, turnaround, or HAZOP.",
                "status": "EXHAUSTED",
                "active": False,
            },
            {
                "tag": "LEVER 02 // LEGACY OCR PIPELINES",
                "title": "Static Document Chunking",
                "desc": "Splits multi-sheet vessel sketches, pump seal plans (DWG 0001K), and operating window tables across disconnected chunks.",
                "status": "EXHAUSTED",
                "active": False,
            },
            {
                "tag": "LEVER 03 // NAIVE VECTOR RAG",
                "title": "Cosine Similarity Retrieval",
                "desc": "Silently averages or overwrites conflicting flow rates (2,020 vs 3,020 m3/h) and pressure ratings across Rev Z0 and Rev Z1.",
                "status": "EXHAUSTED",
                "active": False,
            },
            {
                "tag": "LEVER 04 // ADK OKF v0.2 COMPILER",
                "title": "Dual-Mode Read-Merge-Upsert",
                "desc": "Gemini 3.8 Flash (Global) + 8 deterministic ADK tools compile 136 raw PDFs into 130 schema-verified Process Manufacturing concepts.",
                "status": "ACTIVE LEVER",
                "active": True,
            },
        ],
        "outcomes": [
            {
                "label": "Ingested Process Plant Corpus",
                "val": "136 PDFs",
                "sub": "55 Data Sheets, 46 Vector P&IDs, 26 SDS/Standards, 8 PFDs, 1 UOP Operating Manual",
            },
            {
                "label": "Compiled OKF v0.2 Knowledge Bundle",
                "val": "139 Files",
                "sub": "130 Golden Concepts (Yield, Fouling, Startup, Equipment, SIS, HAZOP) + 9 Indexes",
            },
            {
                "label": "Cross-Doc Discrepancy Capture",
                "val": "21 Flagged",
                "sub": "100% distinction between Rev Z0->Z1 supersession vs. active Datasheet/P&ID conflicts",
            },
            {
                "label": "Yield, Turnaround & HAZOP Speed",
                "val": "14d -> 18m",
                "sub": "Supports Yield Optimization, Fouling Reliability, Cold-Start, LOTO & PHA on GCP",
            },
        ],
        "schematic_nodes": [
            {
                "id": "r2201",
                "label": "Oxidation",
                "title": "Unit 22 — Cumene Oxidation & Spent Air Control",
                "isa95": "UNIT-22 // OXIDATION & ACIDITY",
                "health": "OPTIMAL",
                "concept_id": "units/oxidation",
                "raw_pdf": "operating_manuals/OM-Phenol Unit UOP-2015.pdf",
                "swarm": "Mode A + Mode B Compiler",
                "coord": "extracter_orchestrator",
                "solver": "process_raw_pdf_tool (300 DPI Vision)",
                "sap_id": "OKF-UNIT-22-OXID",
                "formula": "Cumene + O2 -> CHP (22.6 wt% in oxidate) | Spent Air O2 >= 5 vol%\nPrevents phenol over-oxidation to organic acids (Flash Crude pH 2.3-2.7)",
                "metrics": [
                    {"k": "Oxidate CHP Conc", "v": "22.6 wt%"},
                    {"k": "Spent Air O2 Floor", "v": ">= 5.0 vol%"},
                    {"k": "Flash Crude Target", "v": "pH 2.3 - 2.7"},
                    {"k": "OKF Concept", "v": "units/oxidation.md"},
                ],
            },
            {
                "id": "v2301",
                "label": "V-2301",
                "title": "V-2301 — Preflash Column (1st Stage Vacuum)",
                "isa95": "UNIT-23 // CONCENTRATION",
                "health": "WARNING",
                "concept_id": "equipment/V-2301",
                "raw_pdf": "data_sheets/14780-8120-PS-V2301_V-2301 PROCESS DATA SHEET_Z1.pdf",
                "swarm": "Cross-Doc Precedence Engine",
                "coord": "generate_equipment_okf_tool",
                "solver": "merge_equipment_entity_with_existing",
                "sap_id": "CONFLICT-V2301-TT",
                "formula": "P_op = 18.5 mmHgA (Deep Vacuum) | Shell ID = 6,600 mm\nCONFLICT: P&ID DWG 0004 states 7,550 mm T/T vs. As-Built DS PS-V2301 21,000 mm T/T",
                "metrics": [
                    {"k": "Shell ID", "v": "6,600 mm"},
                    {"k": "Design Press (INT)", "v": "3.5 kg/cm2g / FV"},
                    {"k": "Operating Vacuum", "v": "18.5 mmHgA"},
                    {"k": "T/T Length Conflict", "v": "21,000 vs 7,550 mm"},
                ],
            },
            {
                "id": "v2302",
                "label": "V-2302",
                "title": "V-2302A/B — Flash Columns (2nd Stage CHP Conc)",
                "isa95": "UNIT-23 // CONCENTRATION",
                "health": "OPTIMAL",
                "concept_id": "equipment/V-2302",
                "raw_pdf": "pfd/14780-8120-20-23-0002_CDN PROCESS FLOW DIAGRAM FLASH COLUMN VAPORIZER _Z1.pdf",
                "swarm": "Vector CAD P&ID Vision",
                "coord": "process_raw_pdf_tool",
                "solver": "Gemini 3.8 Flash 300 DPI Vision",
                "sap_id": "OKF-EQ-V2302",
                "formula": "CHP Concentration: 22.6 wt% -> 80-83 wt% Technical CHP\nAcidity Guard: CWC aqueous pH ~ 14 prevents organic acid carryover (< pH 2.3)",
                "metrics": [
                    {"k": "Product Conc", "v": "80-83 wt% CHP"},
                    {"k": "Crude Acidity Window", "v": "pH 2.3 - 2.7"},
                    {"k": "Source P&ID", "v": "DWG 25-23-0005"},
                    {"k": "OKF Concept", "v": "equipment/V-2302.md"},
                ],
            },
            {
                "id": "d2301",
                "label": "D-2301",
                "title": "D-2301 — CHP Charge / Surge Drum",
                "isa95": "UNIT-23 // CONCENTRATION",
                "health": "WARNING",
                "concept_id": "equipment/D-2301",
                "raw_pdf": "data_sheets/14780-8120-PS-D2301_D-2301 PROCESS DATA SHEET_Z1.pdf",
                "swarm": "Cross-Doc Precedence Engine",
                "coord": "generate_equipment_okf_tool",
                "solver": "Datasheet vs. P&ID Conflict Detector",
                "sap_id": "CONFLICT-D2301-DP",
                "formula": "CONFLICT — DESIGN PRESSURE:\nP&ID DWG 0006 specifies 3.9 kg/cm2g vs. As-Built DS PS-D2301 Rev Z1 specifies 3.5 kg/cm2g",
                "metrics": [
                    {"k": "DS Design Press", "v": "3.5 kg/cm2g"},
                    {"k": "P&ID Design Press", "v": "3.9 kg/cm2g"},
                    {"k": "Runaway Limit", "v": "75.0 deg C"},
                    {"k": "Emergency Dump", "v": "Cumene Diluent"},
                ],
            },
            {
                "id": "d2304",
                "label": "D-2304",
                "title": "D-2304 — Decomposer CSTR & Calorimeter X-2308",
                "isa95": "UNIT-23 // CLEAVAGE & YIELD",
                "health": "CRITICAL",
                "concept_id": "equipment/D-2304",
                "raw_pdf": "data_sheets/14780-8120-PS-D2304_D-2304 PROCESS DATA SHEET_Z1.pdf",
                "swarm": "Yield, Calorimeter & Burst Conflict Guard",
                "coord": "extracter_orchestrator",
                "solver": "generate_equipment_okf_tool",
                "sap_id": "CONFLICT-D2304-X2311",
                "formula": "Calorimeter X-2308: dT = 7.2 deg C / wt% CHP (target 7-10 deg C at 1.0-1.5 wt% CHP)\nBURST CONFLICT: Rupture Disc X-2311 P&ID 12.16 kg/cm2g vs. DS Design Press 11.0 kg/cm2g",
                "metrics": [
                    {"k": "Calorimeter X-2308 dT", "v": "7-10 deg C (1-1.5% CHP)"},
                    {"k": "DCP Selectivity Target", "v": "300 - 700 wt ppm"},
                    {"k": "X-2311 Burst Conflict", "v": "12.16 vs 11.0 kg/cm2g"},
                    {"k": "Acid Catalyst Window", "v": "40 - 60 wt ppm H2SO4"},
                ],
            },
            {
                "id": "e2307",
                "label": "E-2307",
                "title": "E-2307 — Decomposer Cooling / Heat Exchanger",
                "isa95": "UNIT-23 // DECOMPOSITION",
                "health": "WARNING",
                "concept_id": "equipment/E-2307",
                "raw_pdf": "data_sheets/14780-8120-PS-E2307_E-2307 PROCESS DATA SHEET_Z1.pdf",
                "swarm": "Decimal Transcription Guard",
                "coord": "generate_equipment_okf_tool",
                "solver": "Cross-Doc Reconciliation",
                "sap_id": "CONFLICT-E2307-SHELL",
                "formula": "Q_remove = U * A * LMTD | Shell Design Pressure = 13.0 kg/cm2g (PS-E2307)\nCONFLICT: DWG 0017 recorded 1.3 kg/cm2g (10x decimal error)",
                "metrics": [
                    {"k": "DS Shell Design P", "v": "13.0 kg/cm2g"},
                    {"k": "DWG 0017 Value", "v": "1.3 kg/cm2g (Error)"},
                    {"k": "Unit", "v": "CDN Decomposition"},
                    {"k": "OKF Concept", "v": "equipment/E-2307.md"},
                ],
            },
            {
                "id": "p2302",
                "label": "P-2302",
                "title": "P-2302A/B — Circulation Pumps & API Plan 11/53A",
                "isa95": "UNIT-23 // ROTATING RELIABILITY",
                "health": "WARNING",
                "concept_id": "equipment/P-2302",
                "raw_pdf": "data_sheets/14780-8120-PS-P2302_P-2302 PROCESS DATA SHEET_Z1.pdf",
                "swarm": "Hydraulic & Seal Plan Reconciliation",
                "coord": "generate_equipment_okf_tool",
                "solver": "merge_equipment_entity_with_existing",
                "sap_id": "CONFLICT-P2302-FLOW",
                "formula": "API Plan 11/53A Dual Pressurized Seal (DWG 0001K) | Dilution Ratio > 25:1\nCONFLICT: DWG 0017 states 3,020 m3/hr vs. PS-P2302 states 2,020 m3/h",
                "metrics": [
                    {"k": "DS Rated Capacity", "v": "2,020 m3/h"},
                    {"k": "P&ID Stated Flow", "v": "3,020 m3/hr (Conflict)"},
                    {"k": "Mechanical Seal Plan", "v": "API Plan 11 / 53A"},
                    {"k": "OKF Concept", "v": "equipment/P-2302.md"},
                ],
            },
            {
                "id": "d2308",
                "label": "D-2308",
                "title": "D-2308 — Neutralizer Drum",
                "isa95": "UNIT-23 // NEUTRALIZATION",
                "health": "OPTIMAL",
                "concept_id": "equipment/D-2308",
                "raw_pdf": "data_sheets/14780-8120-PS-D2308_D-2308 PROCESS DATA SHEET_Z1.pdf",
                "swarm": "Mode A + Mode B Compiler",
                "coord": "generate_equipment_okf_tool",
                "solver": "Datasheet Authority",
                "sap_id": "OKF-EQ-D2308",
                "formula": "H2SO4 + 2 NaOH (or Sodium Phenate) -> Na2SO4 + 2 H2O\nNLL Discrepancy: P&ID 500 mm vs. DS 550 mm above bottom tangent",
                "metrics": [
                    {"k": "DS NLL Height", "v": "550 mm"},
                    {"k": "P&ID NLL Height", "v": "500 mm"},
                    {"k": "Target pH Window", "v": "5.5 - 6.5"},
                    {"k": "OKF Concept", "v": "equipment/D-2308.md"},
                ],
            },
            {
                "id": "d2312",
                "label": "D-2312",
                "title": "D-2312 — Diamine / TBC Inhibitor Tank",
                "isa95": "UNIT-23 // CHEMICAL ADDITIVE",
                "health": "CRITICAL",
                "concept_id": "equipment/D-2312",
                "raw_pdf": "data_sheets/14780-8120-PS-D2312_D-2312 PROCESS DATA SHEET_Z1.pdf",
                "swarm": "Chemical Identity Conflict Detector",
                "coord": "generate_equipment_okf_tool",
                "solver": "MOC & HAZOP Pre-Gate Blocker",
                "sap_id": "CONFLICT-D2312-CHEM",
                "formula": "CRITICAL CHEMICAL IDENTITY CONFLICT:\nPS-D2312 Rev Z1 Fluid Name = 'DIAMINE(HMDA)' vs. P&ID / SDS TBC / Diamine mapping",
                "metrics": [
                    {"k": "DS Fluid Name", "v": "DIAMINE(HMDA)"},
                    {"k": "P&ID Service", "v": "Diamine / TBC"},
                    {"k": "MOC / HAZOP Status", "v": "HOLD UNTIL RESOLVED"},
                    {"k": "OKF Concept", "v": "equipment/D-2312.md"},
                ],
            },
            {
                "id": "v2401",
                "label": "Unit 24",
                "title": "Unit 24 & E-2308A/B — Dehydrator, AMS Yield & Fractionation",
                "isa95": "UNIT-24 // YIELD & FOULING",
                "health": "OPTIMAL",
                "concept_id": "troubleshooting/cdn-poor-ams-yield",
                "raw_pdf": "operating_manuals/OM-Phenol Unit UOP-2015.pdf",
                "swarm": "Yield & Fouling Diagnostic Compiler",
                "coord": "generate_okf_concept_tool",
                "solver": "merge_markdown_bodies",
                "sap_id": "OKF-YIELD-AMS-E2308",
                "formula": "DCP -> AMS + H2O (T_dehydrator = 125-145 deg C) -> AMS Selectivity >= 80 mole%\nFouling Rule: H2SO4 > 60 wt ppm or T > 145 deg C causes 1-3 mo E-2308A/B polymer plugging",
                "metrics": [
                    {"k": "AMS Selectivity Target", "v": ">= 80.0 mole%"},
                    {"k": "E-2308A/B Window", "v": "125 - 145 deg C"},
                    {"k": "Phenol Product Spec", "v": ">= 99.99 wt%"},
                    {"k": "OKF Concept", "v": "cdn-poor-ams-yield.md"},
                ],
            },
            {
                "id": "sis_cdn",
                "label": "SIS-CDN",
                "title": "UC-2301..2303 — Cold-Start Gates & 2oo3 Interlocks",
                "isa95": "OPS & IEC-61511 // ENVELOPE",
                "health": "OPTIMAL",
                "concept_id": "procedures/startup-cdn",
                "raw_pdf": "operating_manuals/OM-Phenol Unit UOP-2015.pdf",
                "swarm": "Startup Gate & C&E Matrix Compiler",
                "coord": "generate_okf_concept_tool",
                "solver": "Startup & SIS Trip Verifier",
                "sap_id": "OKF-OPS-STARTUP-SIS",
                "formula": "5-Gate Ready-for-Feed-In: 70 deg C | 300 ppm H2SO4 | <2% H2O | 0 kg/h Water | 2x Flush\n2oo3 Voting (TXSHH / FXSLL) -> Solenoid De-energize -> XV Closure + Cumene Quench",
                "metrics": [
                    {"k": "Startup Feed-In Gates", "v": "5 Gates (70C / 300ppm)"},
                    {"k": "CSTR Step-Down Rate", "v": "1 deg C per >= 15m"},
                    {"k": "SIS Logic Controllers", "v": "UC-2301, 2302, 2303"},
                    {"k": "OKF Concept", "v": "procedures/startup-cdn.md"},
                ],
            },
            {
                "id": "hazop_cdn",
                "label": "HAZOP-CDN",
                "title": "Turnaround MOC & ePHA Risk Matrix Governance",
                "isa95": "MOC & OSHA-1910.119 // PHA",
                "health": "OPTIMAL",
                "concept_id": "hazop/risk-matrix",
                "raw_pdf": "standards/SG-(Q-MP)-014_R3.pdf",
                "swarm": "MOC, LOTO & LOPA Safeguard Compiler",
                "coord": "generate_okf_concept_tool",
                "solver": "IPL Credit & Severity Mapper",
                "sap_id": "OKF-HAZOP-MATRIX",
                "formula": "Risk = Severity(People, Env, Social) x Likelihood_mitigated\nRule: Economic severity conflict flagged; People/Env governs",
                "metrics": [
                    {"k": "Governing Std", "v": "SG-(Q-MP)-014_R3"},
                    {"k": "SDS Corroborated", "v": "15 GHS SDS Files"},
                    {"k": "Readiness Check", "v": "Table A6.2-2 / A6.2-3"},
                    {"k": "OKF Concept", "v": "hazop/risk-matrix.md"},
                ],
            },
        ],
        "personas": [
            {
                "id": "p1",
                "code": "PERSONA 01 // YIELD & PROCESS OPTIMIZATION",
                "initials": "PY",
                "name": "Lead Process & Yield Optimization Engineer",
                "mandate": "Maximizing AMS co-product selectivity (>= 80 mole%), Phenol purity (>= 99.99 wt%), and DCP conversion (300-700 wt ppm) across Units 22-24.",
                "jtbd": "Reconcile UOP operating manual windows (E-2308A/B 125-145 deg C, H2SO4 40-60 wt ppm, Calorimeter X-2308 dT = 7.2 deg C/wt% CHP) with P&ID control loops to eliminate AMS yield losses.",
                "broken": "Spends 16+ hours manually cross-referencing static UOP operating manual PDFs against P&IDs (DWG 0013, 0017) and lab DCP analyses when AMS yield drops below 80 mole%, missing the interaction between E-2308A/B temperature (>145 deg C) and heavy dimer/trimer polymer formation.",
                "agentic": "Queries compiled OKF v0.2 concepts (troubleshooting/cdn-poor-ams-yield.md and parameters/cdn-operating-windows.md) where Calorimeter X-2308 equations, DCP targets (300-700 wt ppm, max 900 wt ppm), and DCS loops are unified—diagnosing yield excursions in 4 minutes.",
                "squad": [
                    {"id": "TOOL-01", "name": "find_raw_documents_tool", "role": "Locates UOP Operating Manual, PFDs, and P&IDs for yield & operating windows"},
                    {"id": "TOOL-02", "name": "process_raw_pdf_tool", "role": "Extracts operating window tables, DCP curves, and Calorimeter X-2308 equations"},
                    {"id": "TOOL-03", "name": "inspect_existing_okf_concept_tool", "role": "Audits existing parameters/ and troubleshooting/ concepts before upsert"},
                    {"id": "TOOL-05", "name": "generate_okf_concept_tool", "role": "Compiles cross-linked yield optimization & operating window playbooks"},
                ],
            },
            {
                "id": "p2",
                "code": "PERSONA 02 // FOULING & ASSET RELIABILITY",
                "initials": "RM",
                "name": "Rotating & Static Asset Reliability Lead",
                "mandate": "Eliminating heat-exchanger polymer plugging (E-2308A/B 1-3 mo cycle), flash column acid corrosion (pH 2.3-2.7), and pump hydraulic/seal failures.",
                "jtbd": "Cross-check mechanical seal piping P&IDs (DWG 0001K API Plan 11/53A & 2/53A), pump curves (P-2302, P-2303), and dehydrator fouling root causes before scheduling maintenance.",
                "broken": "Discovers during pump overhaul that P&ID DWG 0017 lists P-2302 capacity as 3,020 m3/hr while datasheet PS-P2302 specifies 2,020 m3/h, or that E-2308A/B tube plugging every 1-3 months is driven by unlogged 300 wt ppm H2SO4 startup spikes.",
                "agentic": "Inspects troubleshooting/cdn-dehydrator-plugging.md, instruments/pump-seal-plans.md, and equipment/P-2302.md where API Plan 11/53A & 2/53A seal specs, hydraulic discrepancies, and fouling triggers are pre-reconciled.",
                "squad": [
                    {"id": "TOOL-01", "name": "find_raw_documents_tool", "role": "Matches equipment tags across data_sheets/, pid/ (0001H-K), and manuals"},
                    {"id": "TOOL-02", "name": "process_raw_pdf_tool", "role": "Parses 300 DPI mechanical seal piping P&IDs and multi-page pump curves"},
                    {"id": "TOOL-04", "name": "generate_equipment_okf_tool", "role": "Applies Process Data Sheet precedence & flags 2,020 vs 3,020 m3/h conflict"},
                    {"id": "TOOL-05", "name": "generate_okf_concept_tool", "role": "Synthesizes fouling troubleshooting and API seal plan registers"},
                ],
            },
            {
                "id": "p3",
                "code": "PERSONA 03 // PLANT OPERATIONS & STARTUP",
                "initials": "OP",
                "name": "Shift Operations Superintendent & Startup Lead",
                "mandate": "Executing 5-gate cold-start feed-in (70 deg C, 300 ppm H2SO4, <2 wt% H2O), CSTR step-down (70->60 deg C), and normal shutdown purges.",
                "jtbd": "Verify every 'Ready for Feed In' prerequisite, 36-second Calorimeter X-2308 residence lag, and <=5% acid step boundary across SOPs and P&IDs before introducing CHP feed.",
                "broken": "Reads 60-page operating manual PDFs alongside rasterized P&IDs during shift handover. Missing the 36-second calorimeter coil lag or stepping CSTR temperature faster than 1 deg C per 15 minutes causes CHP accumulation and off-spec transition slop.",
                "agentic": "Executes from procedures/startup-cdn.md and procedures/normal-operations-cdn.md with 100% bi-directional links to every DCS control valve (TC-2342, FC-2303), piping line number, and SIS trip threshold.",
                "squad": [
                    {"id": "TOOL-02", "name": "process_raw_pdf_tool", "role": "Extracts sequential startup gates, flush steps, and DCS loop tags"},
                    {"id": "TOOL-05", "name": "generate_okf_concept_tool", "role": "Compiles procedures/startup-cdn.md and normal-operations-cdn.md"},
                    {"id": "TOOL-06", "name": "build_okf_indexes_and_validate_tool", "role": "Verifies 0 broken cross-links across all 139 Markdown files"},
                    {"id": "TOOL-08", "name": "export_bundle_to_gcs_tool", "role": "Publishes verified shift playbooks to GCS knowledge bucket"},
                ],
            },
            {
                "id": "p4",
                "code": "PERSONA 04 // TURNAROUND, MOC & PROCESS SAFETY",
                "initials": "PS",
                "name": "Turnaround, MOC & Process Safety (HAZOP) Lead",
                "mandate": "Governing LOTO isolation blind lists, MOC datasheet-vs-P&ID reconciliation (21 conflicts), 2oo3 SIS interlocks, and PHA/HAZOP revalidation.",
                "jtbd": "Verify every ASME design pressure, nozzle schedule, elevation head note (15,500 mm on V-2301), and 2oo3 SIS trip initiator across 55 Process Data Sheets and 46 P&IDs.",
                "broken": "Spends 3 weeks manually flipping between AutoCAD P&IDs and As-Built Process Data Sheets. Discrepancies like E-2307 (1.3 vs 13.0 kg/cm2g), D-2304 burst disc (12.16 vs 11.0 kg/cm2g), or D-2312 chemical identity (HMDA vs TBC) delay turnaround blinding and PHA sign-off.",
                "agentic": "Opens the compiled OKF v0.2 Knowledge Bundle where all 21 cross-document conflicts, complete nozzle schedules, and 15 GHS SDS profiles are pre-flagged with exact PDF citations—cutting preparation from 14 days to 18 minutes.",
                "squad": [
                    {"id": "TOOL-01", "name": "find_raw_documents_tool", "role": "Locates all governing Datasheets, P&IDs, PFDs, and SDS by tag"},
                    {"id": "TOOL-02", "name": "process_raw_pdf_tool", "role": "Extracts nozzle schedules + 300 DPI Gemini Vision on vector CAD P&IDs"},
                    {"id": "TOOL-04", "name": "generate_equipment_okf_tool", "role": "Enforces Datasheet vs. P&ID precedence & 21 CONFLICT callouts"},
                    {"id": "TOOL-07", "name": "validate_okf_bundle_tool", "role": "Confirms 100% OKF v0.2 schema compliance and link integrity"},
                ],
            },
        ],
        "agent_tools": [
            {
                "id": "AGENT-ROOT",
                "apqc": "ORCHESTRATOR // ADK",
                "status": "ONLINE",
                "name": "extracter_orchestrator (Root ADK Agent)",
                "process": "Autonomous 6-Step Process Manufacturing Knowledge Compiler",
                "value": "98.6% Recall",
                "period": "284 Total Eval Cases",
                "stake": "Compiles 136 raw engineering PDFs into 130 cross-linked OKF v0.2 concepts spanning Yield, Reliability, Startup, MOC, and HAZOP.",
                "owns": "End-to-end orchestration of Mode A (Entity & Scenario-Centric) and Mode B (File-by-File Incremental) extraction workflows.",
                "answers": "Yield Optimization Engineer, Reliability Lead, Shift Superintendent, and Turnaround/Process Safety Lead.",
                "pl": "Compresses Yield root-cause, Turnaround LOTO, and HAZOP document reconciliation from 14 days to 18 minutes while surfacing 21 critical rating conflicts.",
                "cannot": "Cannot modify, overwrite, or delete any file in reference/raw/ or reference/wiki/ (Rule 14 strict immutability).",
                "failure": "Halts synthesis if validate_okf_bundle_tool reports schema errors or broken cross-links.",
                "code_lang": "Python 3.13 // Google ADK + Gemini 3.8 Flash (Global)",
                "code": (
                    "llm_model = Gemini(\n"
                    "    model='gemini-3.8-flash',\n"
                    "    retry_options=HttpRetryOptions(attempts=5, initial_delay=2.0),\n"
                    "    client_kwargs={'location': 'global'},\n"
                    ")\n"
                    "agent = Agent(\n"
                    "    name='extracter_orchestrator',\n"
                    "    model=llm_model,\n"
                    "    tools=[find_raw_documents_tool, process_raw_pdf_tool, ...],\n"
                    "    before_agent_callback=before_agent_callback,\n"
                    ")"
                ),
            },
            {
                "id": "GUARD-01",
                "apqc": "SECURITY // MODEL ARMOR",
                "status": "ACTIVE",
                "name": "before_agent_callback (Model Armor Pre-Flight Guardrail)",
                "process": "Deterministic Prompt-Injection, Jailbreak & Path-Traversal Blocker",
                "value": "100% Block",
                "period": "9/9 Adversarial Cases",
                "stake": "Prevents adversarial prompt injections, system-prompt leaks, and ../ path traversal before any LLM token or tool is invoked.",
                "owns": "Pre-flight inspection of every incoming user prompt and ADKInvocationContext.",
                "answers": "Cloud Security Architect & OT Governance Lead.",
                "pl": "Eliminates prompt-induced exfiltration or unauthorized filesystem writes across all 145 evaluation trajectories.",
                "cannot": "Cannot be bypassed by roleplay, base64 encoding, or instruction-override prefixes.",
                "failure": "Raises deterministic SecurityGuardrailError and returns a structured block message without calling Gemini.",
                "code_lang": "Python // extracter_agent/agent/guardrails.py",
                "code": (
                    "def before_agent_callback(callback_context, llm_request=None):\n"
                    "    # Inspects prompt against adversarial injection & path traversal\n"
                    "    if _matches_injection_pattern(user_text):\n"
                    "        raise SecurityGuardrailError(\n"
                    "            'Blocked by Model Armor pre-flight security guardrail.'\n"
                    "        )"
                ),
            },
            {
                "id": "TOOL-01",
                "apqc": "STEP 1 // DISCOVERY",
                "status": "ONLINE",
                "name": "find_raw_documents_tool",
                "process": "Multi-Corpus Raw Engineering PDF Discovery & MD5 Indexing",
                "value": "136 PDFs",
                "period": "5 Engineering Subfolders",
                "stake": "Locates all relevant datasheets, P&IDs, PFDs, operating manuals, and SDS for any equipment tag or document query.",
                "owns": "Searching reference/raw/ and gs://ut-interaction-demo-okf-knowledge/reference/raw/ with MD5 digest verification.",
                "answers": "extracter_orchestrator Step 1 Discovery.",
                "pl": "Ensures 100% recall of multi-sheet packages (e.g., PS-V2301 + DWG 0004 + PFD 0001) prior to extraction.",
                "cannot": "Cannot read outside the designated reference_raw_dir or GCS raw prefix.",
                "failure": "Returns status='success' with match_count=0 and explicit guidance if no matching PDF exists.",
                "code_lang": "Python // extracter_agent/tools/pdf_tools.py",
                "code": (
                    "def find_raw_documents_tool(query: str, subfolder: str | None = None) -> dict:\n"
                    "    # Searches data_sheets/, pid/, pfd/, operating_manuals/, standards/\n"
                    "    return {'status': 'success', 'match_count': len(matches), 'matches': matches}"
                ),
            },
            {
                "id": "TOOL-02",
                "apqc": "STEP 2 // MULTIMODAL PARSER",
                "status": "ONLINE",
                "name": "process_raw_pdf_tool",
                "process": "Hybrid PyMuPDF Table Extraction & 300 DPI Vector CAD Vision",
                "value": "300 DPI",
                "period": "SHA-256 Vision Cache",
                "stake": "Extracts digital text/tables from datasheets and renders vector CAD P&IDs (chars < 50) at 300 DPI for Gemini 3.8 Flash vision.",
                "owns": "Parsing PDF pages, detecting vector drawings, extracting tag candidates, and invoking multimodal vision.",
                "answers": "extracter_orchestrator Step 2 Ingestion.",
                "pl": "Unlocks 46 AutoCAD P&IDs and 8 PFDs that have zero embedded text streams.",
                "cannot": "Never modifies the source PDF file; caches multimodal outputs by SHA-256 content hash.",
                "failure": "Retries Vertex AI multimodal calls up to 5 times with exponential backoff on HTTP 429/503.",
                "code_lang": "Python // extracter_agent/pdf/processor.py",
                "code": (
                    "is_vector_drawing = total_chars < 50\n"
                    "if is_vector_drawing and enable_multimodal:\n"
                    "    pix = page.get_pixmap(dpi=300)\n"
                    "    vision_md = _describe_drawing_with_gemini(png_bytes, pdf_name)"
                ),
            },
            {
                "id": "TOOL-03",
                "apqc": "STEP 3 // STATE INSPECTION",
                "status": "ONLINE",
                "name": "inspect_existing_okf_concept_tool",
                "process": "Incremental Bundle State & Source-Filter Inspector",
                "value": "Stateful",
                "period": "Read-Before-Upsert",
                "stake": "Inspects existing ## headings, Markdown table columns, tags, and sources in build/okf_bundle before incremental enrichment.",
                "owns": "Looking up existing concepts by concept_id or source_filter across the OKF bundle.",
                "answers": "extracter_orchestrator Step 3 Reconciliation.",
                "pl": "Prevents schema drift and column mismatches when 136 PDFs are ingested sequentially in Mode B.",
                "cannot": "Does not mutate bundle files (strictly read-only inspection).",
                "failure": "Returns status='not_found' cleanly when a concept is being created for the first time.",
                "code_lang": "Python // extracter_agent/tools/okf_tools.py",
                "code": (
                    "insp = inspect_existing_okf_concept_tool(\n"
                    "    concept_id='equipment/D-2304',\n"
                    "    output_bundle_dir='build/okf_bundle'\n"
                    ")"
                ),
            },
            {
                "id": "TOOL-04",
                "apqc": "STEP 4A // EQUIPMENT UPSERT",
                "status": "ONLINE",
                "name": "generate_equipment_okf_tool",
                "process": "Revision-Aware Equipment Read-Merge-Upsert & Conflict Compiler",
                "value": "54 Vessels",
                "period": "Zero Data Loss Merge",
                "stake": "Synthesizes and merges equipment/<TAG>.md files across Datasheets, P&IDs, and PFDs with revision supersession and CONFLICT callouts.",
                "owns": "Merging design_data, operating_conditions, connections, instruments, hazards, and source_files by key.",
                "answers": "extracter_orchestrator Step 4 Synthesis.",
                "pl": "Automatically links every instrument tag to its corpus register via resolve_bundle_instrument_link.",
                "cannot": "Never overwrites existing parameters from other active documents without recording a CONFLICT note.",
                "failure": "Validates Pydantic EquipmentEntity schema before writing Markdown to disk and GCS.",
                "code_lang": "Python // extracter_agent/okf/generator.py",
                "code": (
                    "merged_entity = merge_equipment_entity_with_existing(existing_md, new_entity)\n"
                    "markdown_out = generate_equipment_markdown(merged_entity)\n"
                    "_sync_single_file_to_gcs(target_file)"
                ),
            },
            {
                "id": "TOOL-05",
                "apqc": "STEP 4B // CONCEPT & TABLE UPSERT",
                "status": "ONLINE",
                "name": "generate_okf_concept_tool",
                "process": "Universal Domain Concept & Markdown Table Row Merger",
                "value": "76 Concepts",
                "period": "Row-Level Keyed Upsert",
                "stake": "Compiles and incrementally merges instruments/, hazards/, procedures/, units/, troubleshooting/, hazop/, and sources/ concepts.",
                "owns": "Merging ## sections, Markdown table rows (keyed by Tag/Parameter/Stream), bullet lists, and frontmatter sources.",
                "answers": "extracter_orchestrator Step 4 Synthesis.",
                "pl": "Allows 46 P&IDs to incrementally populate shared instrument registers (e.g. pressure-instruments.md) without losing a single row.",
                "cannot": "Never drops top-level CRITICAL PROCESS SAFETY / DISCREPANCY WARNING blockquotes during merges.",
                "failure": "Supersedes older revisions of the same base document (Rev 0 -> Rev 1) in-place.",
                "code_lang": "Python // extracter_agent/okf/generator.py",
                "code": (
                    "merged_body = merge_markdown_bodies(\n"
                    "    existing_body, body_markdown,\n"
                    "    superseded_stems=superseded_stems\n"
                    ")"
                ),
            },
            {
                "id": "TOOL-06",
                "apqc": "STEP 5 // INDEXER & VALIDATOR",
                "status": "ONLINE",
                "name": "build_okf_indexes_and_validate_tool",
                "process": "Progressive Disclosure Index Compiler & OKF v0.2 Validator",
                "value": "0 Broken Links",
                "period": "139 Markdown Files",
                "stake": "Compiles root index.md, 9 category index.md files, and log.md, then validates 100% OKF v0.2 schema compliance.",
                "owns": "Building progressive disclosure navigation and running validate_okf_bundle.",
                "answers": "extracter_orchestrator Step 5 Validation.",
                "pl": "Guarantees every [[concept]] link and frontmatter block in the bundle is valid before publishing.",
                "cannot": "Cannot mark a bundle valid if any Markdown file lacks YAML frontmatter or contains broken internal links.",
                "failure": "Returns detailed validation errors per file if any check fails.",
                "code_lang": "Python // extracter_agent/okf/validator.py",
                "code": (
                    "idx_res = build_okf_indexes_and_validate_tool(bundle_dir='build/okf_bundle')\n"
                    "assert idx_res['is_valid_okf'] is True"
                ),
            },
            {
                "id": "TOOL-08",
                "apqc": "STEP 6 // GCS PUBLISHER",
                "status": "ONLINE",
                "name": "export_bundle_to_gcs_tool",
                "process": "16-Worker Parallel MD5-Verified Google Cloud Storage Publisher",
                "value": "139 Synced",
                "period": "gs://ut-interaction-demo-okf-knowledge",
                "stake": "Publishes the validated OKF v0.2 bundle to Google Cloud Storage with base64 MD5 digest comparison.",
                "owns": "Incremental and full-bundle synchronization to gs://ut-interaction-demo-okf-knowledge/okf-bundles/phenol-plant/.",
                "answers": "extracter_orchestrator Step 6 Publishing.",
                "pl": "Skips unchanged blobs via MD5 digest check and uploads modified concepts in parallel across 16 workers.",
                "cannot": "Never writes to the read-only reference/raw/ prefix.",
                "failure": "Supports dry_run=True verification and full retry on transient network errors.",
                "code_lang": "Python // extracter_agent/gcs/publisher.py",
                "code": (
                    "res = export_bundle_to_gcs_tool(\n"
                    "    bundle_dir='build/okf_bundle',\n"
                    "    destination_bucket='ut-interaction-demo-okf-knowledge'\n"
                    ")"
                ),
            },
        ],
        "arch_layers": [
            {
                "band": "LAYER 01 // UX",
                "name": "Mining M3 Light Executive Cockpit & ADK Dev UI",
                "blurb": "Unified executive presentation and interactive workbench at / and /demo alongside the Google ADK developer console at /dev-ui/.",
                "chips": ["M3 Light Theme", "GET /", "GET /dev-ui/", "POST /api/demo/extract-live"],
                "down": "Equipment Tag (Mode A) or Raw PDF File Request (Mode B)",
                "up": "Compiled OKF v0.2 Markdown + Conflict Callouts + Tool Trace",
            },
            {
                "band": "LAYER 02 // RUNTIME",
                "name": "Google Cloud Run & Vertex AI Agent Engine (asia-southeast1)",
                "blurb": "Containerized FastAPI + ADK Web Server running in asia-southeast1 with persistent session state and zero-cold-start bundle seeding.",
                "chips": ["Cloud Run (2 vCPU / 2 GiB)", "asia-southeast1", "FastAPI + ADK 1.21+"],
                "down": "Authenticated ADK Runner InvocationContext",
                "up": "Streaming SSE Events & Structured JSON Payloads",
            },
            {
                "band": "LAYER 03 // SECURITY",
                "name": "Model Armor Pre-Flight Security Callback (before_agent_callback)",
                "blurb": "Deterministic pre-flight inspection blocking prompt injection, instruction overrides, system-prompt extraction, and ../ path traversal.",
                "chips": ["before_agent_callback", "SecurityGuardrailError", "Zero Path Traversal"],
                "down": "Sanitized Engineering Prompt",
                "up": "100% Block on Adversarial Payloads (9/9 Red-Team Cases)",
            },
            {
                "band": "LAYER 04 // COGNITION",
                "name": "CognitiveClassifier & Gemini 3.8 Flash (Global Endpoint)",
                "blurb": "Routes intents across 7 canonical classes and executes multi-turn ADK tool reasoning and 300 DPI multimodal vision on GEMINI_LOCATION=global.",
                "chips": ["gemini-3.8-flash", "GEMINI_LOCATION=global", "5x HttpRetryOptions"],
                "down": "Structured Tool Calls (8 ADK FunctionTools)",
                "up": "Extracted Tables, Nozzle Schedules, Loops & Discrepancies",
            },
            {
                "band": "LAYER 05 // PARSER",
                "name": "Hybrid PyMuPDF + 300 DPI Vector CAD Vision Engine",
                "blurb": "Extracts text/tables from digital datasheets and renders vector AutoCAD P&IDs (chars < 50) at 300 DPI PNGs backed by a SHA-256 vision cache.",
                "chips": ["PyMuPDF (fitz)", "300 DPI Vector CAD", "SHA-256 Vision Cache"],
                "down": "Byte-Verified Raw PDFs from reference/raw/ or GCS",
                "up": "Normalized Tag Candidates, Stream Balances & Instrument Loops",
            },
            {
                "band": "LAYER 06 // COMPILER",
                "name": "Revision-Aware Read-Merge-Upsert & Precedence Engine",
                "blurb": "Distinguishes newer revisions of the same document (Rev Z0->Z1 in-place update) from active cross-document conflicts (Datasheet vs. P&ID).",
                "chips": ["merge_equipment_entity", "merge_markdown_bodies", "21 CONFLICT Callouts"],
                "down": "Incremental Entity & Markdown Table Upserts",
                "up": "130 Golden Concepts + 9 Progressive Disclosure Indexes",
            },
            {
                "band": "LAYER 07 // STORAGE",
                "name": "Two-Tier Google Cloud Storage & Local OKF v0.2 Bundle Store",
                "blurb": "16-worker parallel MD5-verified sync between local build/okf_bundle/ and gs://ut-interaction-demo-okf-knowledge/okf-bundles/phenol-plant/.",
                "chips": ["gs://ut-interaction-demo-okf-knowledge", "136 Raw PDFs", "139 OKF Markdown Files"],
                "down": "Base64 MD5 Digest Verification & Parallel Upload",
                "up": "Immutable Source Citations & Schema-Valid OKF v0.2 Bundle",
            },
        ],
        "arch_controls": [
            {
                "name": "Rule 14: Strict reference/ Immutability",
                "rule": "Neither the agent nor any FunctionTool may create, modify, or delete any file in reference/raw/ or reference/wiki/. Verified before and after every run.",
                "spans": "BINDS LAYERS 03, 05, 06, 07",
            },
            {
                "name": "Model Armor Pre-Flight Guardrail",
                "rule": "Every prompt passes through before_agent_callback prior to LLM invocation, blocking prompt injection, jailbreaks, and directory traversal.",
                "spans": "BINDS LAYERS 01, 02, 03",
            },
            {
                "name": "Datasheet vs. P&ID Precedence & Conflict Lock",
                "rule": "As-Built Process Data Sheets govern mechanical ratings; P&IDs govern SIS/instrument loops; cross-document discrepancies emit explicit CONFLICT callouts.",
                "spans": "BINDS LAYERS 04, 05, 06",
            },
            {
                "name": "100% OKF v0.2 Schema & Link Gate",
                "rule": "Every compiled concept is verified by validate_okf_bundle_tool for YAML frontmatter completeness, progressive index coverage, and 0 broken links.",
                "spans": "BINDS LAYERS 06, 07",
            },
        ],
        "raw_pdfs": raw_pdfs,
        "concepts": concepts,
        "graph": {
            "nodes": nodes,
            "edges": edges,
        },
    }


def build_static_data(
    profile: Profile | None = None,
) -> tuple[dict[str, Any], dict[str, str], Profile]:
    prof = profile or load_profile()
    raw_pdfs = collect_raw_pdfs(prof.raw_dir)
    concepts, nodes, edges = collect_okf_concepts(prof.wiki_dir)
    conflict_nodes = [c for c in concepts if c["has_conflict"]]
    md_file_count = (
        len([p for p in prof.wiki_dir.rglob("*.md") if not p.name.startswith("_")])
        if prof.wiki_dir.exists()
        else 0
    )

    base = _default_phenol_static_data(raw_pdfs, concepts, nodes, edges, conflict_nodes)
    ctx = {
        "raw_pdfs": raw_pdfs,
        "concepts": concepts,
        "nodes": nodes,
        "edges": edges,
        "conflict_nodes": conflict_nodes,
        "base": base,
        "md_file_count": md_file_count,
    }
    overrides, html_tokens, ui = prof.build(ctx)
    data = dict(base)
    data.update(overrides)
    data["ui"] = ui
    return data, html_tokens, prof


def render_index_html(html_tokens: dict[str, str]) -> str:
    tpl = TEMPLATE_PATH.read_text(encoding="utf-8")
    out = tpl
    for k, v in html_tokens.items():
        placeholder = "{{" + k + "}}"
        assert placeholder in out, f"Template missing placeholder {placeholder}"
        out = out.replace(placeholder, v)
    leftover = re.findall(r"\{\{[A-Z0-9_]+\}\}", out)
    assert not leftover, f"Unresolved template tokens in index.html: {leftover}"
    return out


def _replace_once(src: str, old: str, new: str, label: str) -> str:
    cnt = src.count(old)
    assert cnt == 1, f"replace_once({label}) expected 1 occurrence, found {cnt}"
    return src.replace(old, new, 1)


def run_build_verification_harness(
    html: str,
    css: str,
    js: str,
    profile: Profile | None = None,
) -> dict[str, int]:
    """Runs the 5-Group Build-Time Verification Harness on the compiled 4-Screen Cockpit."""
    if profile is None:
        if "RIDGEBACK CONCENTRATOR" in html.upper():
            profile = load_profile("copper-concentrator")
        elif "PROCESS MANUFACTURING" in html.upper():
            profile = load_profile("phenol-plant")
        else:
            profile = load_profile()

    checks_run = 0

    def _check(cond: bool, msg: str) -> None:
        nonlocal checks_run
        checks_run += 1
        if not cond:
            raise AssertionError(f"[BUILD HARNESS FAIL #{checks_run}] {msg}")

    # -------------------------------------------------------------------------
    # Group A: Design Token Lock & Colour Discipline
    # -------------------------------------------------------------------------
    required_tokens = [
        "--m3-canvas: #F8F9FA",
        "--m3-surface: #FFFFFF",
        "--m3-primary: #1A73E8",
        "--m3-border: #DADCE0",
        "--m3-critical: #D93025",
        "--m3-success: #1E8E3E",
        "--sp-1: 8px",
        "--sp-2: 16px",
        "--sp-3: 24px",
        "--sp-4: 32px",
        "--sp-5: 40px",
        "Playfair Display",
        "Plus Jakarta Sans",
        "Inter",
        "Roboto Mono",
        "scroll-padding-top: 130px",
        "max-width: 1540px",
        "scroll-margin-top: 130px",
    ]
    for tok in required_tokens:
        _check(tok in css, f"Missing required CSS design token: {tok}")

    forbidden_strings = [
        "#131313",
        "#0d1520",
        "🛰️",
        "🎯",
        "📐",
        "🚀",
        "L6 PM",
        "L7 PM",
        "RED-TEAM CRITIC",
        "GEE-BUG",
        "SCADA JOIN",
    ] + list(profile.harness_forbidden)
    combined = html + "\n" + css + "\n" + js
    for fb in forbidden_strings:
        _check(fb not in combined, f"Forbidden string/token detected: {fb}")

    # -------------------------------------------------------------------------
    # Group B: Automated CSS Class-Coverage Audit
    # -------------------------------------------------------------------------
    defined_classes = set(re.findall(r"\.([a-zA-Z_][a-zA-Z0-9_-]*)", css))
    html_class_attrs = re.findall(r'class="([^"\'\n]+)"', html)
    js_class_attrs = re.findall(r'class="([^"\'\n]+)"', js)
    used_classes: set[str] = set()
    for attr in html_class_attrs + js_class_attrs:
        for token in attr.split():
            clean_tok = token.strip()
            if re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*$", clean_tok):
                used_classes.add(clean_tok)
    missing_classes = sorted(used_classes - defined_classes)
    _check(
        len(missing_classes) == 0,
        f"Undefined CSS classes used in HTML/JS: {missing_classes}",
    )

    # -------------------------------------------------------------------------
    # Group C: DOM ID Parity Audit (app.js -> index.html + dynamic templates)
    # -------------------------------------------------------------------------
    html_ids = set(re.findall(r'id="([a-zA-Z0-9_-]+)"', html + "\n" + js))
    js_Static_ids = set(re.findall(r'getElementById\("([a-zA-Z0-9_-]+)"\)', js))
    missing_ids = sorted(js_Static_ids - html_ids)
    _check(
        len(missing_ids) == 0,
        f"DOM IDs queried in app.js but missing in index.html/templates: {missing_ids}",
    )

    # -------------------------------------------------------------------------
    # Group D: JS Bracket Integrity & SVG Tag Safety
    # -------------------------------------------------------------------------
    _check(js.count("(") == js.count(")"), "Unbalanced parentheses () in app.js")
    _check(js.count("[") == js.count("]"), "Unbalanced brackets [] in app.js")
    _check(js.count("{") == js.count("}"), "Unbalanced braces {} in app.js")

    svg_blocks = re.findall(r"<svg[\s\S]*?</svg>", html)
    _check(len(svg_blocks) >= 5, f"Expected >= 5 SVG blocks in index.html, found {len(svg_blocks)}")
    for idx, svg_block in enumerate(svg_blocks):
        _check(
            "<sub" not in svg_block and "<sup" not in svg_block,
            f"Forbidden HTML <sub>/<sup> inside <svg> block #{idx + 1}",
        )

    # -------------------------------------------------------------------------
    # Group E: 4-Screen Visual-First Structure Lock
    # -------------------------------------------------------------------------
    screen_panes = re.findall(r'<div id="pane-([a-z]+)" class="screen-pane', html)
    _check(
        screen_panes == ["macro", "schematic", "ecosystem", "architecture"],
        f"Expected strictly 4 screens ['macro', 'schematic', 'ecosystem', 'architecture'], found {screen_panes}",
    )
    nav_tabs = re.findall(r'id="tab-([a-z]+)"', html)
    _check(
        nav_tabs == ["macro", "schematic", "ecosystem", "architecture"],
        f"Expected strictly 4 header nav tabs, found {nav_tabs}",
    )
    for screen_num in ("SCREEN 01 / 04", "SCREEN 02 / 04", "SCREEN 03 / 04", "SCREEN 04 / 04"):
        _check(screen_num in html, f"Missing screen badge {screen_num}")

    required_visual_ids = [
        "scenario-switcher-strip",
        "s1-scenario-spotlight",
        "btn-scenario-launch-wb",
        "btn-scenario-launch-twin",
        "s1-visual-blueprint-svg",
        "schematic-particle-canvas",
        "radial-risk-gauge",
        "wb-pipeline-dag-svg",
        "datagraph-svg",
        "arch-visual-blueprint-svg",
    ]
    for vid in required_visual_ids:
        _check(vid in html_ids, f"Missing required visual stage ID: {vid}")

    html_upper = html.upper()
    _check(
        all(req.upper() in html_upper for req in profile.harness_required),
        f"Expected explicit {profile.harness_required} framing in index.html",
    )

    _check(
        html.count('class="tech-spec-drawer"') == 4,
        "Expected 1 collapsible .tech-spec-drawer on each of the 4 screens",
    )
    _check(
        html.count('class="storyline-footer"') == 4,
        "Expected 1 .storyline-footer takeaway bar on each of the 4 screens",
    )

    return {
        "total_checks": checks_run,
        "defined_css_classes": len(defined_classes),
        "verified_used_classes": len(used_classes),
        "verified_dom_ids": len(js_Static_ids),
        "svg_blocks": len(svg_blocks),
        "screen_count": len(screen_panes),
    }


def main() -> None:
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    data, html_tokens, profile = build_static_data()
    data_js_path = STATIC_DIR / "data.js"
    data_js_content = "window.OKF_DEMO_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n"
    data_js_path.write_text(data_js_content, encoding="utf-8")
    print(
        f"[{profile.name}] Wrote {data_js_path} ({len(data_js_content):,} bytes) | "
        f"{len(data['raw_pdfs'])} PDFs | {len(data['concepts'])} OKF concepts | "
        f"{len(data['graph']['nodes'])} graph nodes | {len(data['graph']['edges'])} graph edges"
    )

    index_path = STATIC_DIR / "index.html"
    css_path = STATIC_DIR / "app.css"
    js_path = STATIC_DIR / "app.js"
    html = render_index_html(html_tokens)
    index_path.write_text(html, encoding="utf-8")
    css = css_path.read_text(encoding="utf-8")
    js = js_path.read_text(encoding="utf-8")

    harness_stats = run_build_verification_harness(html, css, js, profile=profile)
    print(
        f"[BUILD HARNESS PASS] {harness_stats['total_checks']}/{harness_stats['total_checks']} checks | "
        f"{harness_stats['screen_count']} screens | "
        f"{harness_stats['verified_used_classes']}/{harness_stats['defined_css_classes']} CSS classes verified | "
        f"{harness_stats['verified_dom_ids']} DOM IDs verified | "
        f"{harness_stats['svg_blocks']} SVG blocks verified"
    )

    standalone = _replace_once(
        html,
        '<link rel="stylesheet" href="/static/app.css">',
        "<style>\n" + css + "\n</style>",
        "inline_css",
    )
    standalone = _replace_once(
        standalone,
        '<script src="/static/data.js"></script>\n<script src="/static/app.js"></script>',
        "<script>\n" + data_js_content + "\n</script>\n<script>\n" + js + "\n</script>",
        "inline_js",
    )
    for target_artifact in (BRAIN_ARTIFACT, CURRENT_BRAIN_ARTIFACT):
        target_artifact.parent.mkdir(parents=True, exist_ok=True)
        target_artifact.write_text(standalone, encoding="utf-8")
        print(f"Wrote standalone HTML artifact: {target_artifact} ({len(standalone):,} bytes)")


if __name__ == "__main__":
    main()

