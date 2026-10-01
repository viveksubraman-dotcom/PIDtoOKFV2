"""Copper-gold concentrator (Ridgeback, fictional) corpus profile.

Content rules
-------------
* Plant numbers come from ``scripts/mining_corpus/plant_model.py`` - the same module that
  generated the synthetic PDFs - so the cockpit and the documents cannot drift.
* Detection claims come from ``corpora/copper-concentrator/eval_results.json`` (written by
  ``eval_conflicts.py``) and the extraction run log. Nothing is shown as "flagged" unless the
  compiled bundle actually contains the CONFLICT callout.
* No speed-up or benchmark figures that were not measured on this corpus.
* The pack is labelled synthetic wherever the corpus is described.
"""

from __future__ import annotations

import copy
import html
import json
import re
import sys
from typing import Any

from corpus_profiles import REPO_ROOT, Profile

sys.path.insert(0, str(REPO_ROOT / "scripts" / "mining_corpus"))
from plant_model import DESIGN, EQ, FRESH_TPH, MB, SEEDED_CONFLICTS, SITE

CORPUS_DIR = REPO_ROOT / "corpora" / "copper-concentrator"
EVAL_JSON = CORPUS_DIR / "eval_results.json"
RUN_LOG = CORPUS_DIR / "wiki" / "_run_log.jsonl"
GCS_PREFIX = "okf-bundles/copper-concentrator"

SAFETY_IDS = {"C04", "C05", "C06", "C09", "C10"}
DOC_LABEL = {
    "DS": "data sheet", "PID": "P&ID", "PFD": "PFD", "OM": "operating manual", "CE": "cause & effect",
    "EL": "equipment list", "HAZOP": "HAZOP",
}

RAW = {
    "ds_cr2101": "data_sheets/RB-4410-PS-CR2101_PRIMARY GYRATORY CRUSHER PROCESS DATA SHEET_B.pdf",
    "ds_ml3101": "data_sheets/RB-4410-PS-ML3101_SAG MILL PROCESS DATA SHEET_B.pdf",
    "ds_ml3201": "data_sheets/RB-4410-PS-ML3201_BALL MILL PROCESS DATA SHEET_B.pdf",
    "ds_pp3201": "data_sheets/RB-4410-PS-PP3201_CYCLONE FEED PUMP PROCESS DATA SHEET_B.pdf",
    "ds_cy3201": "data_sheets/RB-4410-PS-CY3201_CYCLONE CLUSTER PROCESS DATA SHEET_B.pdf",
    "ds_fc4101": "data_sheets/RB-4410-PS-FC4101_ROUGHER FLOTATION TANK CELLS PROCESS DATA SHEET_B.pdf",
    "ds_tk4501": "data_sheets/RB-4410-PS-TK4501_PAX XANTHATE MIXING TANK PROCESS DATA SHEET_B.pdf",
    "ds_tk4511": "data_sheets/RB-4410-PS-TK4511_FROTHER STORAGE TANK PROCESS DATA SHEET_B.pdf",
    "ds_th5101": "data_sheets/RB-4410-PS-TH5101_CONCENTRATE THICKENER PROCESS DATA SHEET_B.pdf",
    "ds_pp5101b": "data_sheets/RB-4410-PS-PP5101_CONCENTRATE THICKENER UNDERFLOW PUMP PROCESS DATA SHEET_RevB.pdf",
    "ds_pp6101": "data_sheets/RB-4410-PS-PP6101_TAILINGS PUMPS PROCESS DATA SHEET_B.pdf",
    "ds_temp": "data_sheets/RB-4410-PS-0034_TEMPERATURE INSTRUMENT PROCESS DATA SHEET_B.pdf",
    "pid_3102": "pid/RB-4410-PID-31-002_P&ID SAG MILL HYDROSTATIC LIFT & LUBE SYSTEM_B.pdf",
    "pid_4501": "pid/RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf",
    "pid_6101": "pid/RB-4410-PID-61-001_P&ID TAILINGS THICKENING & PUMPING TO TSF_B.pdf",
    "pfd_001": "pfd/RB-4410-PFD-001_PROCESS FLOW DIAGRAM CRUSHING AND GRINDING_B.pdf",
    "sg005": "standards/RB-4410-SG-005_GRINDING MILL ISOLATION AND ENTRY STANDARD_R3.pdf",
    "hazop": "standards/RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _e(s: str) -> str:
    return html.escape(s, quote=False)


def _load_eval() -> dict[str, Any]:
    if EVAL_JSON.exists():
        return json.loads(EVAL_JSON.read_text(encoding="utf-8"))
    return {"results": [], "seeded_total": len(SEEDED_CONFLICTS), "seeded_detected": 0,
            "decoy_flagged_as_conflict": False, "conflict_lines_total": 0}


def _run_stats() -> dict[str, Any]:
    ok, secs, files = 0, 0.0, set()
    if RUN_LOG.exists():
        last: dict[str, dict] = {}
        for line in RUN_LOG.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                last[rec["file"]] = rec
        for f, rec in last.items():
            files.add(f)
            if rec.get("ok"):
                ok += 1
                secs += float(rec.get("sec", 0.0))
    return {"ok": ok, "attempted": len(files), "seconds": round(secs)}


def _doc_kind(doc_id: str) -> str:
    head = doc_id.split("-")[0]
    if doc_id.startswith("DS-INST"):
        return "instrument data sheet"
    if "(Sheet" in doc_id:
        return "same data sheet"
    return DOC_LABEL.get(head, doc_id)


def _mw(v: str) -> str:
    n = float(v.replace(",", "").split()[0])
    return f"{n / 1000:.1f} MW"


class _Ctx:
    def __init__(self, ctx: dict[str, Any]):
        self.raw_pdfs = ctx["raw_pdfs"]
        self.concepts = ctx["concepts"]
        self.nodes = ctx["nodes"]
        self.edges = ctx["edges"]
        self.conflict_nodes = ctx["conflict_nodes"]
        self.base = ctx["base"]
        self.md_files = ctx.get("md_file_count", len(self.concepts))
        self.ev = _load_eval()
        self.run = _run_stats()
        self.by_id = {r["id"]: r for r in self.ev.get("results", [])}
        self.cids = {c["concept_id"] for c in self.concepts}

    # counts ---------------------------------------------------------------
    @property
    def n_pdf(self) -> int:
        return len(self.raw_pdfs)

    @property
    def n_concepts(self) -> int:
        return len(self.concepts)

    @property
    def n_seeded(self) -> int:
        return int(self.ev.get("seeded_total", len(SEEDED_CONFLICTS)))

    @property
    def n_found(self) -> int:
        return int(self.ev.get("seeded_detected", 0))

    def folder_count(self, sub: str) -> int:
        return sum(1 for p in self.raw_pdfs if p["subfolder"] == sub)

    # detection ------------------------------------------------------------
    def found(self, cid: str) -> bool:
        return bool(self.by_id.get(cid, {}).get("detected"))

    def evidence(self, cid: str) -> str:
        ev = self.by_id.get(cid, {}).get("evidence") or []
        return ev[0]["text"] if ev else ""

    def found_count(self, ids: list[str]) -> int:
        return sum(self.found(i) for i in ids)

    # concepts -------------------------------------------------------------
    def concept_for_tag(self, tag: str) -> str:
        base = re.sub(r"[A-Z]$", "", tag)
        for cand in (f"equipment/{tag}", f"equipment/{base}"):
            if cand in self.cids:
                return cand
        low = base.lower()
        hits = sorted(c for c in self.cids if low in c.lower())
        return hits[0] if hits else self.fallback_concept()

    def concept_for_source(self, needle: str) -> str:
        for c in self.concepts:
            if any(needle in s for s in c.get("sources", [])) and not c["concept_id"].startswith("sources/"):
                return c["concept_id"]
        for c in self.concepts:
            if needle.lower() in c["concept_id"].lower():
                return c["concept_id"]
        return self.fallback_concept()

    def fallback_concept(self) -> str:
        for cand in ("units/copper-concentrator", "parameters/concentrator-design-basis"):
            if cand in self.cids:
                return cand
        return min(self.cids) if self.cids else "units/copper-concentrator"


def _conf(cid: str) -> dict[str, Any]:
    return next(c for c in SEEDED_CONFLICTS if c["id"] == cid)


# ---------------------------------------------------------------------------
# Schematic nodes (12)
# ---------------------------------------------------------------------------
def _node(x: _Ctx, nid: str, tag: str, label: str, title: str, area: str, raw: str,
          conflicts: list[str], metrics: list[tuple[str, str]], design_note: str,
          decoy: bool = False) -> dict[str, Any]:
    hits = [c for c in conflicts if x.found(c)]
    if hits:
        health = "CRITICAL" if any(c in SAFETY_IDS for c in hits) else "WARNING"
    else:
        health = "OPTIMAL"
    if hits:
        lines = []
        for c in hits:
            s = _conf(c)
            lines.append(f"{c} {s['parameter']}: {_doc_kind(s['true_doc'])} {s['true']} vs "
                         f"{_doc_kind(s['conflict_doc'])} {s['conflict']}")
        lines.append("Extracted callout: " + x.evidence(hits[0])[:220])
        formula = "\n".join(lines)
        sap = f"{hits[0]} · {tag} {_conf(hits[0])['parameter'].upper()}"
    elif decoy:
        formula = design_note
        sap = f"{tag} · REV A \u2192 REV B SUPERSEDED (NO CONFLICT)"
    else:
        missed = [c for c in conflicts if not x.found(c)]
        formula = design_note + (f"\nSeeded {', '.join(missed)} not flagged in the compiled bundle." if missed else "")
        sap = f"OKF · {tag}"
    return {
        "id": nid, "label": label, "title": title, "isa95": area, "health": health,
        "concept_id": x.concept_for_tag(tag), "raw_pdf": raw,
        "swarm": "Mode B file-by-file extraction",
        "coord": "generate_equipment_okf_tool" if tag[:2] not in ("TT", "PS") else "generate_okf_concept_tool",
        "solver": "Cross-document reconciliation" if conflicts else ("Revision supersession" if decoy else "Data sheet authority"),
        "sap_id": sap, "formula": formula,
        "metrics": [{"k": k, "v": v} for k, v in metrics],
        "_conflicts": conflicts,
    }


def _schematic_nodes(x: _Ctx) -> list[dict[str, Any]]:
    s321, s322, s621 = MB["S-321"], MB["S-322"], MB["S-621"]
    return [
        _node(x, "cr2101", "CR-2101", "CR-2101", "CR-2101 — Primary Gyratory Crusher", "AREA 21 // PRIMARY CRUSHING",
              RAW["ds_cr2101"], ["C08"],
              [("Installed power (DS)", "1,200 kW"), ("Equipment list", "1,000 kW"), ("Design throughput", "5,500 t/h"), ("Product P80", "150 mm")],
              "Gyratory 60 x 113; CSS 165 mm; discharges to overland conveyor CV-2101."),
        _node(x, "ml3101", "ML-3101", "ML-3101", "ML-3101 — SAG Mill (40 ft x 22 ft, gearless drive)", "AREA 31 // SAG MILLING",
              RAW["ds_ml3101"], ["C01"],
              [("Installed power (DS)", "22,000 kW"), ("PID-31-001", "20,000 kW"), ("Fresh feed", f"{FRESH_TPH:,} t/h"), ("Specific energy", "8.2 kWh/t")],
              "12.2 m x 6.7 m EGL; 60-80 % critical speed; ball charge 12-15 % vol."),
        _node(x, "sis3101", "TT-3101", "SAG SIS", "TT-3101 / PSV-3105 — SAG Bearing Trip & Lift-Oil Relief", "AREA 31 // SIS & RELIEF",
              RAW["pid_3102"], ["C04", "C10"],
              [("TT-3101 TAHH (inst. DS)", "75 °C"), ("TT-3101 TAHH (C&E)", "85 °C"), ("PSV-3105 set (inst. DS)", "160 bar(g)"), ("PSV-3105 set (PID-31-002)", "180 bar(g)")],
              "SIF-3101 (SIL 1) stops the SAG mill on TAHH; lift-oil system design pressure 170 bar(g)."),
        _node(x, "ml3201", "ML-3201", "ML-3201", "ML-3201 — Ball Mill (27 ft x 44 ft, gearless drive)", "AREA 32 // BALL MILLING",
              RAW["ds_ml3201"], ["C11"],
              [("Installed power (sheet 1)", "22,000 kW"), ("Installed power (sheet 3)", "20,500 kW"), ("Ball charge", "32-35 % vol"), ("Specific energy", "8.0 kWh/t")],
              "Closed circuit with cyclone cluster CY-3201; 75 % critical speed."),
        _node(x, "pp3201", "PP-3201A", "PP-3201", "PP-3201A/B/C — Cyclone Feed Pumps (2 duty + 1 standby)", "AREA 32 // CLASSIFICATION",
              RAW["ds_pp3201"], ["C02"],
              [("Duty per pump (PFD S-322)", f"{s322['slurry_m3h']:,} m³/h"), ("Rated flow (DS)", "4,650 m³/h"), ("Slurry SG", f"{s322['slurry_sg']}"), ("Circulating load", f"{int(DESIGN['circulating_load'] * 100)} %")],
              f"Cyclone feed S-321 {s321['slurry_m3h']:,} m³/h total at {s321['solids_w_pct']} % solids."),
        _node(x, "cy3201", "CY-3201", "CY-3201", "CY-3201 — Cyclone Cluster (16 x 660 mm)", "AREA 32 // CLASSIFICATION",
              RAW["ds_cy3201"], ["C03"],
              [("Feed density (PFD)", f"{s321['solids_w_pct']} % w/w"), ("Operating manual", "65 % w/w"), ("Overflow P80", "150 µm"), ("Feed pressure", "100-130 kPa")],
              "Overflow at 35 % solids to rougher flotation."),
        _node(x, "fc4101", "FC-4101", "FC-4101", "FC-4101…4107 — Rougher Flotation Tank Cells", "AREA 41 // ROUGHER FLOTATION",
              RAW["ds_fc4101"], [],
              [("Cells", "7 x 300 m³"), ("Residence time", "32 min"), ("Rougher feed pH", f"{DESIGN['rougher_feed_ph']}"), ("Cu recovery (design)", f"{int(DESIGN['cu_recovery'] * 100)} %")],
              "Rougher concentrate to regrind ML-4201 (P80 38 µm) and cleaner column FC-4301."),
        _node(x, "tk4501", "TK-4501", "TK-4501", "TK-4501 — PAX Xanthate Mixing Tank (CS2 hazard)", "AREA 45 // REAGENTS",
              RAW["pid_4501"], ["C09"],
              [("HAZOP HZ-45-03", "AT-4501 required"), ("PID-45-001", "AT-4501 not shown"), ("CS2 LEL", "1.3 %"), ("Extraction fan", "FN-4501")],
              "PAX decomposes with moisture, heat or acid, releasing CS2 (auto-ignition 90 °C)."),
        _node(x, "tk4511", "TK-4511", "TK-4511", "TK-4511 — Frother Storage Tank", "AREA 45 // REAGENTS",
              RAW["ds_tk4511"], ["C06"],
              [("Reagent (DS)", "MIBC, FP 41 °C"), ("Reagent (PID-45-001)", "Polyglycol (DF-250 type)"), ("Hazardous area", "Zone 2"), ("Volume", "30 m³")],
              "Frother identity sets flammability and hazardous-area classification (HZ-45-06)."),
        _node(x, "th5101", "TH-5101", "TH-5101", "TH-5101 — Concentrate Thickener", "AREA 51 // CONCENTRATE",
              RAW["ds_th5101"], ["C07"],
              [("Diameter (DS)", "30 m"), ("PID-51-001", "25 m"), ("Underflow density", "65 % w/w"), ("Concentrate", f"{MB['_meta']['conc_tph']} t/h at 26 % Cu")],
              "High-rate thickener ahead of filter press FP-5101 (cake 8.5 % vs TML 9.8 %)."),
        _node(x, "pp5101", "PP-5101A", "PP-5101", "PP-5101A — Concentrate Underflow Pump (Rev A \u2192 Rev B)", "AREA 51 // CONCENTRATE",
              RAW["ds_pp5101b"], [],
              [("Rated flow Rev A", "180 m³/h (superseded)"), ("Rated flow Rev B", "210 m³/h"), ("TDH", "28 m"), ("Motor", "75 kW")],
              "Same document, newer revision: value updated in place, not a conflict.",
              decoy=True),
        _node(x, "pp6101", "PP-6101A", "PP-6101", "PP-6101A/B/C — Tailings Pumps to TSF (3 stages)", "AREA 61 // TAILINGS",
              RAW["ds_pp6101"], ["C05"],
              [("Stage-3 casing (DS)", "40 bar(g)"), ("PID-61-001", "4.0 bar(g)"), ("Stage-3 discharge", "34 bar(g)"), ("Flow", f"{s621['slurry_m3h']:,} m³/h, SG {s621['slurry_sg']}")],
              "6.2 km pipeline to the TSF; PT-6103 PAHH 38 bar(g) trips SIF-6101 (SIL 2)."),
    ]


# ---------------------------------------------------------------------------
# Scenarios & personas
# ---------------------------------------------------------------------------
def _scenarios(x: _Ctx) -> list[dict[str, Any]]:
    s321, s322, s621 = MB["S-321"], MB["S-322"], MB["S-621"]

    def k(ids: list[str]) -> str:
        return f"{x.found_count(ids)}/{len(ids)} conflicts flagged"

    return [
        {
            "id": "sag_shutdown", "code": "SCENARIO 01 // SAG MILL SHUTDOWN, RELINE & ISOLATION",
            "short_label": "01 · SAG Shutdown & Isolation",
            "title": "SAG Mill ML-3101 Reline: One Isolation Pack From Eight Documents",
            "beyond_hazop": True, "tag_text": "SHUTDOWN", "badge": "SHUTDOWN • ISOLATION",
            "kpi_delta": k(["C01", "C04", "C10"]), "speedup": "8 source documents",
            "concept_id": x.concept_for_tag("ML-3101"), "secondary_concept_id": x.concept_for_source("SG-005"),
            "raw_pdf": RAW["sg005"], "schematic_node_id": "ml3101", "persona_idx": 0,
            "challenge": ("A reline needs the mill rating, lift-oil relief setting and bearing trip set points from one "
                          "consistent source. The pack gives the SAG motor as 22,000 kW (data sheet) and 20,000 kW "
                          "(PID-31-001); PSV-3105 as 160 bar(g) (instrument data sheet) and 180 bar(g) (PID-31-002); "
                          "the trunnion bearing TAHH as 75 °C (data sheet) and 85 °C (cause & effect)."),
            "derivation": ("Equipment data sheet governs ratings; instrument data sheet governs set points; differing "
                           "P&ID / C&E values are recorded as CONFLICT with both sources. "
                           "PSV set pressure ≤ system design pressure 170 bar(g) (HZ-31-02)."),
            "impact": f"{x.found_count(['C01', 'C04', 'C10'])} of 3 discrepancies flagged with source citations before the isolation plan is written.",
        },
        {
            "id": "grinding_basis", "code": "SCENARIO 02 // GRINDING CIRCUIT DESIGN BASIS",
            "short_label": "02 · Grinding Design Basis",
            "title": "Cyclone Feed Pumps, Cyclone Density and Ball Mill Power vs the Mass Balance",
            "beyond_hazop": True, "tag_text": "DESIGN BASIS", "badge": "THROUGHPUT • RECOVERY",
            "kpi_delta": k(["C02", "C03", "C11"]), "speedup": "4 source documents",
            "concept_id": x.concept_for_tag("PP-3201A"), "secondary_concept_id": x.concept_for_tag("CY-3201"),
            "raw_pdf": RAW["pfd_001"], "schematic_node_id": "pp3201", "persona_idx": 2,
            "challenge": (f"The PFD sets cyclone feed at {s321['slurry_m3h']:,} m³/h ({s322['slurry_m3h']:,} m³/h per duty "
                          f"pump) at {s321['solids_w_pct']} % solids for a 300 % circulating load. The pump data sheet "
                          "rates each pump at 4,650 m³/h, the operating manual targets 65 % solids, and the ball mill "
                          "data sheet gives 22,000 kW on sheet 1 and 20,500 kW on sheet 3."),
            "derivation": ("Q_pump = Q_S-321 / 2 duty pumps, Q_S-321 = F·(1 + CL) as slurry volume. PFD mass balance "
                           "governs process duty; data sheet governs rating; differences are recorded as CONFLICT."),
            "impact": (f"{x.found_count(['C02', 'C03', 'C11'])} of 3 flagged. Under-rated pumps risk sanding and cyclone "
                       "roping; a 65 % density target risks overflow coarser than P80 150 µm."),
        },
        {
            "id": "reagent_safety", "code": "SCENARIO 03 // REAGENT SAFETY: XANTHATE & FROTHER",
            "short_label": "03 · Reagent Safety",
            "title": "CS2 Detector Missing From the Xanthate P&ID; Frother Identity Mismatch",
            "beyond_hazop": False, "tag_text": "PROCESS SAFETY", "badge": "HAZOP CLOSE-OUT • SDS",
            "kpi_delta": k(["C09", "C06"]), "speedup": "5 source documents",
            "concept_id": x.concept_for_tag("TK-4501"), "secondary_concept_id": x.concept_for_tag("TK-4511"),
            "raw_pdf": RAW["pid_4501"], "schematic_node_id": "tk4501", "persona_idx": 1,
            "challenge": ("HAZOP HZ-45-03 requires CS2 detector AT-4501 (alarm 10 % LEL, interlocked to fan FN-4501) in "
                          "the PAX mixing room; PID-45-001 does not show it. Frother tank TK-4511 is MIBC on its data "
                          "sheet (flash point 41 °C, Zone 2) and a polyglycol frother (DF-250 type, > 100 °C) on the P&ID."),
            "derivation": ("PAX + moisture / heat / acid \u2192 CS2 (LEL 1.3 %, auto-ignition 90 °C). HAZOP actions must "
                           "appear on the P&ID; reagent identity must match data sheet and SDS because it sets the "
                           "hazardous-area classification."),
            "impact": f"{x.found_count(['C09', 'C06'])} of 2 flagged, each cited to the HAZOP node and SDS.",
        },
        {
            "id": "tailings_pressure", "code": "SCENARIO 04 // TAILINGS PIPELINE TO TSF",
            "short_label": "04 · Tailings Pipeline",
            "title": "Tailings Pump Stage-3 Casing Rating: 40 bar(g) vs 4.0 bar(g)",
            "beyond_hazop": False, "tag_text": "TAILINGS", "badge": "TAILINGS • PRESSURE INTEGRITY",
            "kpi_delta": k(["C05", "C07"]), "speedup": "4 source documents",
            "concept_id": x.concept_for_tag("PP-6101A"), "secondary_concept_id": x.concept_for_tag("TH-5101"),
            "raw_pdf": RAW["pid_6101"], "schematic_node_id": "pp6101", "persona_idx": 3,
            "challenge": (f"Three pumps in series move {s621['slurry_m3h']:,} m³/h of thickened tailings (SG "
                          f"{s621['slurry_sg']}) 6.2 km to the TSF at 34 bar(g) stage-3 discharge. The data sheet rates "
                          "the stage-3 casing at 40 bar(g); PID-61-001 shows 4.0 bar(g). The concentrate thickener is "
                          "30 m on its data sheet and 25 m on PID-51-001."),
            "derivation": ("Discharge 34 bar(g) < PAHH 38 bar(g) < casing design 40 bar(g) (SIF-6101, SIL 2). "
                           "A 4.0 bar(g) drawing value is a 10x decimal error. Data sheet governs; P&ID value recorded as CONFLICT."),
            "impact": f"{x.found_count(['C05', 'C07'])} of 2 flagged: a cited record of pipeline and thickener ratings for design review and change management.",
        },
    ]


def _personas() -> list[dict[str, Any]]:
    def sq(*ids: str) -> list[dict[str, str]]:
        roles = {
            "TOOL-01": ("find_raw_documents_tool", "Finds every document that mentions the tag"),
            "TOOL-02": ("process_raw_pdf_tool", "Reads data sheet tables and P&ID drawings"),
            "TOOL-03": ("inspect_existing_okf_concept_tool", "Reads the current concept before merging"),
            "TOOL-04": ("generate_equipment_okf_tool", "Merges equipment ratings; records CONFLICT with sources"),
            "TOOL-05": ("generate_okf_concept_tool", "Builds instrument, HAZOP and reagent concepts"),
            "TOOL-06": ("build_okf_indexes_and_validate_tool", "Rebuilds indexes; checks links and schema"),
            "TOOL-07": ("validate_okf_bundle_tool", "Validates the bundle before publishing"),
        }
        return [{"id": i, "name": roles[i][0], "role": roles[i][1]} for i in ids]

    return [
        {
            "id": "p1", "code": "PERSONA 01 // MAINTENANCE & SHUTDOWN PLANNING", "initials": "SP",
            "name": "Maintenance & Shutdown Planner (Grinding)",
            "mandate": "Plans SAG and ball mill relines: isolation points, electrical ratings, lube and lift-oil relief settings, and entry permits under standard SG-005.",
            "jtbd": "Assemble one isolation and reline pack for ML-3101 whose ratings and set points agree across data sheets, P&IDs, the cause & effect matrix and SG-005.",
            "broken": "Each value is checked by opening the data sheet, P&ID and C&E side by side. A 20,000 vs 22,000 kW rating or a 180 vs 160 bar(g) relief setting is caught only if someone compares both documents.",
            "agentic": "Opens the ML-3101 concept: every rating is listed with its source document, and differences between documents appear as CONFLICT callouts citing both sources.",
            "squad": sq("TOOL-01", "TOOL-02", "TOOL-04", "TOOL-07"),
        },
        {
            "id": "p2", "code": "PERSONA 02 // INSTRUMENTATION, SIS & PROCESS SAFETY", "initials": "IS",
            "name": "Instrumentation, SIS & Process Safety Engineer",
            "mandate": "Owns SIF set points, relief devices, gas detection and HAZOP close-out for the concentrator (IEC 61511).",
            "jtbd": "Confirm every trip set point, relief setting and HAZOP-required safeguard is the same in instrument data sheets, P&IDs and the cause & effect matrix.",
            "broken": "HAZOP actions are tracked in a register; whether the P&ID was updated is checked by hand. The missing CS2 detector AT-4501 and the 75 vs 85 °C TAHH sit in different documents.",
            "agentic": "Reviews CONFLICT callouts for TT-3101, PSV-3105, TK-4501 and TK-4511 with the HAZOP node and SDS cited next to each.",
            "squad": sq("TOOL-01", "TOOL-02", "TOOL-05", "TOOL-07"),
        },
        {
            "id": "p3", "code": "PERSONA 03 // PROCESS & METALLURGY", "initials": "PM",
            "name": "Process / Metallurgy Superintendent",
            "mandate": f"Owns grinding and flotation performance: {FRESH_TPH:,} t/h fresh feed, grind P80 150 µm, copper recovery {int(DESIGN['cu_recovery'] * 100)} %.",
            "jtbd": "Check that pump ratings, cyclone targets and mill power in the equipment documents support the PFD mass balance.",
            "broken": "Operating targets in the manual drift from the design basis, and data sheets can be sized on an older circulating-load assumption.",
            "agentic": "Compares PFD stream values with equipment ratings in one place; PP-3201, CY-3201 and ML-3201 differences are flagged with sources.",
            "squad": sq("TOOL-01", "TOOL-02", "TOOL-03", "TOOL-05"),
        },
        {
            "id": "p4", "code": "PERSONA 04 // TAILINGS", "initials": "TE",
            "name": "Tailings Engineer",
            "mandate": "Maintains the design and operating record for tailings thickening and pumping to the tailings storage facility (TSF).",
            "jtbd": "Keep a consistent, cited record of pipeline pressures, pump ratings and thickener data for design reviews and change management.",
            "broken": "Pressure ratings on drawings are not checked against data sheets unless a change triggers a review, so a 4.0 vs 40 bar(g) decimal error can persist.",
            "agentic": "Uses the PP-6101 and TH-5101 concepts, with CONFLICT callouts and the source document for every rating.",
            "squad": sq("TOOL-01", "TOOL-02", "TOOL-04", "TOOL-06"),
        },
    ]


# ---------------------------------------------------------------------------
# Screen-1 evidence panels
# ---------------------------------------------------------------------------
def _benchmark(x: _Ctx) -> list[dict[str, Any]]:
    decoy_ok = not x.ev.get("decoy_flagged_as_conflict", False)
    run = x.run
    bars = [
        {"label": "Seeded cross-document conflicts flagged", "val": round(100 * x.n_found / max(x.n_seeded, 1), 1),
         "display": f"{x.n_found}/{x.n_seeded}", "primary": True},
        {"label": "Safety-critical conflicts flagged (SIS, relief, CS2, frother, casing)",
         "val": round(100 * x.found_count(sorted(SAFETY_IDS)) / len(SAFETY_IDS), 1),
         "display": f"{x.found_count(sorted(SAFETY_IDS))}/{len(SAFETY_IDS)}", "primary": True},
        {"label": "Revision decoy (PP-5101A Rev A \u2192 B) updated in place, not flagged",
         "val": 100.0 if decoy_ok else 0.0, "display": "1/1" if decoy_ok else "0/1", "primary": True},
        {"label": "Documents extracted by the live ADK agent (Mode B, file by file)",
         "val": round(100 * run["ok"] / max(x.n_pdf, 1), 1), "display": f"{run['ok']}/{x.n_pdf}", "primary": True},
    ]
    return bars


def _headwinds(x: _Ctx) -> list[dict[str, Any]]:
    drawings = x.folder_count("pid") + x.folder_count("pfd")
    return [
        {"title": "Drawings Carry the Numbers", "badge": f"{drawings} DRAWINGS", "val": str(drawings),
         "unit": "P&IDs and PFDs", "baseline": f"of {x.n_pdf} documents",
         "desc": "Ratings, set points and stream values sit as text on vector drawings. Keyword search does not connect a value on PID-31-002 to the row for the same tag on its data sheet.",
         "fill": round(100 * drawings / max(x.n_pdf, 1))},
        {"title": "Same Tag, Different Numbers", "badge": f"{x.n_seeded} SEEDED", "val": str(x.n_seeded),
         "unit": "Discrepancies", "baseline": "7 document-type pairs",
         "desc": "Data sheet vs P&ID, PFD vs data sheet, PFD vs operating manual, instrument data sheet vs cause & effect, HAZOP vs P&ID, equipment list vs data sheet, and two sheets of one data sheet.",
         "fill": round(100 * x.n_seeded / len(EQ))},
        {"title": "Safety Values in Several Places", "badge": "SIS • RELIEF • GAS", "val": str(len(SAFETY_IDS)),
         "unit": "Safety-critical items", "baseline": "3+ documents each",
         "desc": "TT-3101 trip, PSV-3105 set pressure, CS2 detection AT-4501, frother identity and the tailings casing rating each appear in three or more documents that must agree.",
         "fill": round(100 * len(SAFETY_IDS) / max(x.n_seeded, 1))},
    ]


def _levers() -> list[dict[str, Any]]:
    return [
        {"tag": "LEVER 01 // MANUAL CROSS-CHECK", "title": "Engineer Takeoffs",
         "desc": "Engineers compare data sheets, P&IDs and the C&E by hand; coverage depends on which pairs someone chooses to compare.",
         "status": "LIMITED", "active": False},
        {"tag": "LEVER 02 // OCR & CHUNKING", "title": "Static Document Chunks",
         "desc": "Splits drawings and multi-sheet data sheets into disconnected chunks; a tag and its value can land in different chunks.",
         "status": "LIMITED", "active": False},
        {"tag": "LEVER 03 // VECTOR SEARCH", "title": "Similarity Retrieval",
         "desc": "Returns the most similar passage; two documents that disagree are not reconciled, and a superseded revision can be returned.",
         "status": "LIMITED", "active": False},
        {"tag": "LEVER 04 // ADK OKF COMPILER", "title": "Read-Merge-Upsert per Document",
         "desc": "Gemini with ADK tools reads each PDF, merges it into the tag's concept, keeps both values with sources when documents disagree, and updates in place for a newer revision.",
         "status": "ACTIVE LEVER", "active": True},
    ]


def _outcomes(x: _Ctx) -> list[dict[str, Any]]:
    decoy_ok = not x.ev.get("decoy_flagged_as_conflict", False)
    return [
        {"label": "Synthetic Concentrator Document Pack", "val": f"{x.n_pdf} PDFs",
         "sub": (f"{x.folder_count('data_sheets')} data sheets · {x.folder_count('pid')} P&IDs & lists · "
                 f"{x.folder_count('pfd')} PFDs · {x.folder_count('standards')} C&E, HAZOP, SDS, standard · "
                 f"{x.folder_count('operating_manuals')} operating manual")},
        {"label": "Compiled OKF Knowledge Bundle", "val": f"{x.n_concepts} Concepts",
         "sub": f"{len(x.nodes)} graph nodes · {len(x.edges)} cross-links · every concept lists its source PDFs"},
        {"label": "Seeded Conflicts Flagged", "val": f"{x.n_found}/{x.n_seeded}",
         "sub": "Revision decoy handled as supersession" if decoy_ok else "Revision decoy was flagged as a conflict"},
        {"label": "Live Extraction Run", "val": f"{x.run['ok']}/{x.n_pdf} PDFs",
         "sub": f"Gemini on Vertex AI, file by file, {round(x.run['seconds'] / 60)} min total agent time"},
    ]


# ---------------------------------------------------------------------------
# Agent tools / architecture (patch the corpus-independent phenol defaults)
# ---------------------------------------------------------------------------
def _agent_tools(x: _Ctx) -> list[dict[str, Any]]:
    tools = copy.deepcopy(x.base["agent_tools"])
    over = {
        "AGENT-ROOT": {"value": f"{x.n_found}/{x.n_seeded} Found", "period": "Seeded-conflict eval",
                       "stake": f"Compiles {x.n_pdf} concentrator PDFs into {x.n_concepts} cross-linked OKF concepts.",
                       "pl": "Gives shutdown, SIS, metallurgy and tailings roles one cited knowledge base with document conflicts made explicit.",
                       "answers": "Shutdown Planner, SIS & Process Safety Engineer, Metallurgy Superintendent, Tailings Engineer.",
                       "cannot": "Cannot modify any source PDF in the raw corpus directory (strict read-only inputs)."},
        "TOOL-01": {"value": f"{x.n_pdf} PDFs", "period": "5 document folders",
                    "pl": "Finds every document for a tag (e.g. data sheet PS-ML3101 + PID-31-001 + PFD-001) before extraction.",
                    "owns": "Searching the raw corpus directory (or its GCS prefix) with MD5 digest verification."},
        "TOOL-02": {"pl": f"Reads {x.folder_count('pid') + x.folder_count('pfd')} P&IDs and PFDs plus data sheet tables."},
        "TOOL-03": {"pl": f"Prevents schema drift when {x.n_pdf} PDFs are merged one after another."},
        "TOOL-04": {"value": f"{sum(1 for c in x.concepts if c['concept_id'].startswith('equipment/'))} Equipment",
                    "pl": "Keeps both values and both sources when documents disagree (e.g. ML-3101 22,000 vs 20,000 kW)."},
        "TOOL-05": {"value": f"{sum(1 for c in x.concepts if not c['concept_id'].startswith(('equipment/', 'sources/')))} Concepts",
                    "pl": "Lets 10 P&IDs, the C&E and the HAZOP populate shared instrument and hazard registers row by row."},
        "TOOL-06": {"period": f"{x.md_files} Markdown Files"},
        "TOOL-08": {"value": f"{x.md_files} Files", "owns": f"Synchronisation to gs://ut-interaction-demo-okf-knowledge/{GCS_PREFIX}/."},
    }
    for t in tools:
        for key, val in over.get(t["id"], {}).items():
            t[key] = val
        for key in ("code", "stake", "pl", "owns"):
            if isinstance(t.get(key), str):
                t[key] = (t[key].replace("equipment/D-2304", "equipment/ML-3101")
                          .replace("PS-V2301 + DWG 0004 + PFD 0001", "PS-ML3101 + PID-31-001 + PFD-001")
                          .replace("reference/raw/", "corpora/copper-concentrator/raw/"))
    return tools


def _arch_layers(x: _Ctx) -> list[dict[str, Any]]:
    layers = copy.deepcopy(x.base["arch_layers"])
    for layer in layers:
        if layer["band"].startswith("LAYER 06"):
            layer["blurb"] = "Distinguishes a newer revision of the same document (Rev A \u2192 Rev B, updated in place) from active cross-document conflicts (data sheet vs P&ID)."
            layer["chips"] = ["merge_equipment_entity", "merge_markdown_bodies", f"{x.n_found}/{x.n_seeded} seeded conflicts"]
            layer["up"] = f"{x.n_concepts} OKF concepts + progressive indexes"
        if layer["band"].startswith("LAYER 07"):
            layer["blurb"] = f"MD5-verified sync between the local bundle and gs://ut-interaction-demo-okf-knowledge/{GCS_PREFIX}/."
            layer["chips"] = ["gs://ut-interaction-demo-okf-knowledge", f"{x.n_pdf} Raw PDFs", f"{x.md_files} OKF Markdown Files"]
        if layer["band"].startswith("LAYER 05"):
            layer["down"] = "Byte-verified raw PDFs from the corpus directory or GCS"
        if layer["band"].startswith("LAYER 03"):
            layer["up"] = "Adversarial prompts blocked before any model call (see Security Test)"
    return layers


def _arch_controls(x: _Ctx) -> list[dict[str, Any]]:
    ctrls = copy.deepcopy(x.base["arch_controls"])
    for c in ctrls:
        if c["name"].startswith("Rule 14"):
            c["name"] = "Rule 14: Read-Only Source Corpus"
            c["rule"] = "Neither the agent nor any FunctionTool may create, modify or delete a source PDF. Outputs go only to the OKF bundle."
        if c["name"].startswith("Datasheet"):
            c["rule"] = ("Equipment data sheets govern ratings; instrument data sheets govern set points; PFD mass balance "
                         "governs process duty. Differences between active documents are recorded as CONFLICT with both sources.")
    return ctrls


# ---------------------------------------------------------------------------
# HTML tokens
# ---------------------------------------------------------------------------
def _zones_html(nodes: list[dict[str, Any]]) -> str:
    by = {n["id"]: n for n in nodes}

    def sub(n: dict[str, Any], text: str) -> str:
        colour = {"CRITICAL": "var(--m3-critical)", "WARNING": "var(--m3-critical)"}.get(n["health"], "var(--m3-text-secondary)")
        return f'<span style="font-size:9.5px; color:{colour};">{_e(text)}</span>'

    def box(nid: str, text: str, width: int = 118, primary: bool = False) -> str:
        n = by[nid]
        border = " border-color:var(--m3-critical);" if n["health"] in ("CRITICAL", "WARNING") else ""
        cls = "schematic-node node-primary" if primary and not border else "schematic-node"
        return (f'<div class="{cls}" id="node-{nid}" data-node="{nid}" style="width:{width}px; height:44px;{border}">\n'
                f'                  <span>{_e(n["label"])} {_e(n["title"].split(" — ")[1].split(" (")[0])[:16]}</span>\n'
                f'                  {sub(n, text)}\n'
                f'                </div>')

    def vals(nid: str, flagged: str, normal: str) -> str:
        return flagged if by[nid]["health"] in ("CRITICAL", "WARNING") else normal

    ml = by["ml3101"]
    ml_crit = ml["health"] in ("CRITICAL", "WARNING")
    ml_block = (
        f'<div class="{"node-crusher-critical" if ml_crit else "schematic-node node-primary"}" id="node-ml3101" data-node="ml3101" style="width:132px; height:{96 if ml_crit else 44}px;">\n'
        + ('                  <div class="crusher-dot"></div>\n'
           '                  <div style="font-size:11.5px; font-weight:700; color:#D93025; line-height:1.2;">ML-3101 SAG Mill</div>\n'
           '                  <div style="font-size:8.5px; font-weight:700; color:#C5221F; text-transform:uppercase; letter-spacing:0.3px;">RATING CONFLICT</div>\n'
           '                  <div class="tnum" style="font-size:10.5px; font-family:var(--font-mono); font-weight:700; color:#D93025; margin-top:2px;">22.0 vs 20.0 MW</div>\n'
           if ml_crit else
           '                  <span>ML-3101 SAG Mill</span>\n'
           '                  <span style="font-size:9.5px; color:var(--m3-text-secondary);">22.0 MW &middot; GMD</span>\n')
        + '                </div>'
    )
    col = 'style="display:flex; flex-direction:column; gap:14px; position:absolute; left:{l}px; top:48px;"'
    return "\n".join([
        '            <!-- Zone 1: Crushing & SAG milling -->',
        '            <div class="schematic-zone-box" style="height:265px;">',
        '              <div class="zone-title">Area 21 &amp; 31 // Crushing &amp; SAG Milling</div>',
        f'              <div {col.format(l=16)}>',
        '                ' + box("cr2101", vals("cr2101", "1,200 vs 1,000 kW", "1,200 kW · 5,500 t/h"), 124),
        '                ' + ml_block,
        '              </div>',
        '            </div>',
        '',
        '            <!-- Zone 2: Ball milling, classification & rougher flotation -->',
        '            <div class="schematic-zone-box" style="height:265px;">',
        '              <div class="zone-title">Area 32 &amp; 41 // Ball Mill, Cyclones &amp; Rougher Flotation</div>',
        f'              <div {col.format(l=18)}>',
        '                ' + box("ml3201", vals("ml3201", "22.0 vs 20.5 MW (sheets)", "22.0 MW"), 140),
        '                ' + box("pp3201", vals("pp3201", f"{MB['S-322']['slurry_m3h']:,} vs 4,650 m³/h", f"{MB['S-322']['slurry_m3h']:,} m³/h"), 140, primary=True),
        '              </div>',
        f'              <div {col.format(l=190)}>',
        '                ' + box("cy3201", vals("cy3201", "60 vs 65 % solids", "60 % solids · P80 150 µm"), 140),
        '                ' + box("fc4101", "7 x 300 m³ · pH 10.5", 140, primary=True),
        '              </div>',
        '            </div>',
        '',
        '            <!-- Zone 3: Reagents & SAG SIS -->',
        '            <div class="schematic-zone-box" style="height:265px;">',
        '              <div class="zone-title">Area 45 &amp; SIS // Reagents &amp; Safety Functions</div>',
        f'              <div {col.format(l=16)}>',
        '                ' + box("tk4501", vals("tk4501", "AT-4501 missing on P&ID", "PAX · CS2 hazard"), 150),
        '                ' + box("tk4511", vals("tk4511", "MIBC vs polyglycol", "MIBC · Zone 2"), 150),
        '                ' + box("sis3101", vals("sis3101", "75 vs 85 °C · 160 vs 180 bar", "TAHH 75 °C · PSV 160 bar(g)"), 150),
        '              </div>',
        '            </div>',
        '',
        '            <!-- Zone 4: Thickening, filtration & tailings -->',
        '            <div class="schematic-zone-box" style="grid-column: 1 / 4; height:110px; margin-top:6px;">',
        '              <div class="zone-title">Area 51 &amp; 61 // Concentrate Thickening &amp; Tailings to TSF</div>',
        '              <div style="display:flex; gap:28px; position:absolute; left:24px; top:44px; align-items:center;">',
        '                ' + box("th5101", vals("th5101", "30 vs 25 m diameter", "30 m · 65 % solids"), 150),
        '                ' + box("pp5101", "Rev A 180 \u2192 Rev B 210 m³/h", 170, primary=True),
        '                ' + box("pp6101", vals("pp6101", "40 vs 4.0 bar(g) casing", "40 bar(g) · 6.2 km"), 160),
        '              </div>',
        '            </div>',
    ])


def _pairs_chart(x: _Ctx) -> str:
    groups: dict[str, list[str]] = {}
    for c in SEEDED_CONFLICTS:
        a, b = _doc_kind(c["true_doc"]), _doc_kind(c["conflict_doc"])
        key = "Two sheets of one data sheet" if "same" in b else f"{a.capitalize()} vs {b}"
        groups.setdefault(key, []).append(c["id"])
    rows = sorted(groups.items(), key=lambda kv: -len(kv[1]))
    max_n = max(len(v) for _, v in rows)
    out = ['          <!-- Seeded discrepancies by document pair (grey = seeded, blue = flagged by the agent) -->',
           '          <text x="16" y="150" font-family="\'Roboto Mono\', monospace" font-size="9.5" font-weight="700" fill="#5F6368" letter-spacing="0.5">WHERE THE DOCUMENTS DISAGREE // SEEDED vs FLAGGED BY THE AGENT</text>']
    y = 166
    for label, ids in rows:
        n, f = len(ids), x.found_count(ids)
        w_all = round(360 * n / max_n)
        w_found = round(360 * f / max_n)
        out.append(f'          <text x="16" y="{y + 10}" font-family="\'Plus Jakarta Sans\', sans-serif" font-size="10" font-weight="600" fill="#202124">{_e(label)}</text>')
        out.append(f'          <rect x="232" y="{y}" width="{w_all}" height="13" rx="3" fill="#FCE8E6" stroke="#F6AEA9" stroke-width="1"/>')
        if w_found:
            out.append(f'          <rect x="232" y="{y}" width="{w_found}" height="13" rx="3" fill="#1A73E8"/>')
        out.append(f'          <text x="{240 + w_all}" y="{y + 10}" font-family="\'Roboto Mono\', monospace" font-size="10" font-weight="700" fill="#202124">{f}/{n} &middot; {", ".join(ids)}</text>')
        y += 21
    return "\n".join(out)


def _html_tokens(x: _Ctx, nodes: list[dict[str, Any]], scenarios: list[dict[str, Any]],
                 personas: list[dict[str, Any]]) -> dict[str, str]:
    n, c, d, s = x.n_pdf, x.n_concepts, x.n_found, x.n_seeded
    k_nodes = len(x.conflict_nodes)
    safety = x.found_count(sorted(SAFETY_IDS))
    decoy_ok = not x.ev.get("decoy_flagged_as_conflict", False)
    sc0, p0 = scenarios[0], personas[0]
    ind8, ind10, ind12 = " " * 8, " " * 10, " " * 12
    t = {
        "PAGE_TITLE": "P&amp;ID-to-OKF &middot; Copper Concentrator Engineering Knowledge Compiler (Synthetic Demo Pack)",
        "BRAND_TITLE": "P&amp;ID-to-OKF &middot; Concentrator Knowledge Compiler",
        "S1_EYEBROW": "COPPER-GOLD CONCENTRATOR &bull; ENGINEERING DOCUMENT RECONCILIATION &bull; SYNTHETIC DOCUMENT PACK",
        "S1_H1": "One Verified Knowledge Base From a Concentrator&rsquo;s Engineering Documents",
        "S1_HERO_DESC": (f"{ind10}A Google ADK agent on Gemini reads {n} engineering PDFs for a 60,000 t/d copper-gold concentrator "
                         "&mdash; data sheets, P&amp;IDs, PFDs, cause &amp; effect, HAZOP, SDS &mdash; and compiles "
                         f"{c} cross-linked OKF concepts. Where two documents give different values for the same tag, it keeps both, with their sources."),
        "S1_HERO_BADGES": "\n".join([
            f'{ind8}<span class="badge badge-primary tnum">4 CONCENTRATOR SCENARIOS</span>',
            f'{ind8}<span class="badge badge-optimal tnum">{d}/{s} SEEDED CONFLICTS FLAGGED</span>',
            f'{ind8}<span class="badge badge-stable tnum">SYNTHETIC DOCUMENT PACK &bull; AGENTS = f(PHYSICAL DISCREPANCY)</span>',
        ]),
        "S1_SPOT_BADGE": _e(sc0["badge"]).replace("•", "&bull;") + "</span>",
        "S1_SPOT_CODE": _e(sc0["code"]).replace("&amp;", "&amp;") + "</span>",
        "S1_SPOT_TITLE": _e(sc0["title"]) + "</div>",
        "S1_KPI_RIBBON": "\n".join([
            f'{ind8}<div class="vkpi-card">',
            f'{ind8}  <div class="vkpi-top"><span class="vkpi-label">01 // CONCENTRATOR DOCUMENT PACK</span><span class="badge badge-primary">SYNTHETIC</span></div>',
            f'{ind8}  <div class="vkpi-val tnum">{n} PDFs</div>',
            f'{ind8}  <div class="vkpi-sub">{x.folder_count("data_sheets")} Data Sheets &middot; {x.folder_count("pid")} P&amp;IDs &amp; Lists &middot; {x.folder_count("pfd")} PFDs &middot; {x.folder_count("standards")} C&amp;E, HAZOP, SDS &middot; {x.folder_count("operating_manuals")} Manual</div>',
            f'{ind8}</div>',
            f'{ind8}<div class="vkpi-card vkpi-success">',
            f'{ind8}  <div class="vkpi-top"><span class="vkpi-label">02 // DESIGN BASIS</span><span class="badge badge-optimal">PFD-000</span></div>',
            f'{ind8}  <div class="vkpi-val tnum" style="color:var(--m3-success);">60,000 t/d</div>',
            f'{ind8}  <div class="vkpi-sub">{FRESH_TPH:,} t/h &middot; SAG 22 MW + Ball 22 MW &middot; P80 150 &micro;m &middot; {DESIGN["head_cu_pct"]} % Cu</div>',
            f'{ind8}</div>',
            f'{ind8}<div class="vkpi-card vkpi-critical">',
            f'{ind8}  <div class="vkpi-top"><span class="vkpi-label">03 // CROSS-DOCUMENT CONFLICTS</span><span class="badge badge-critical">MEASURED</span></div>',
            f'{ind8}  <div class="vkpi-val tnum" style="color:var(--m3-critical);">{d} / {s} Flagged</div>',
            f'{ind8}  <div class="vkpi-sub">Seeded ground truth &middot; revision decoy {"not flagged (correct)" if decoy_ok else "flagged (incorrect)"}</div>',
            f'{ind8}</div>',
            f'{ind8}<div class="vkpi-card">',
            f'{ind8}  <div class="vkpi-top"><span class="vkpi-label">04 // SAFETY-CRITICAL FINDINGS</span><span class="badge badge-primary">SIS &bull; HAZOP</span></div>',
            f'{ind8}  <div class="vkpi-val tnum" style="color:var(--m3-primary);">{safety} / {len(SAFETY_IDS)}</div>',
            f'{ind8}  <div class="vkpi-sub">Bearing trip &middot; relief set pressure &middot; CS2 detector &middot; frother identity &middot; tailings casing</div>',
            f'{ind8}</div>',
        ]),
        "S1_CHART_TITLE": "Where Concentrator Documents Disagree &mdash; and What the Agent Flagged",
        "S1_CHART_LEGEND": ('<div class="legend-item"><span class="dot-blue"></span> FLAGGED BY THE AGENT</div>\n'
                            '            <div class="legend-item"><span class="dot-red"></span> SEEDED IN THE DOCUMENTS</div>'),
        "S1_SVG_ARIA": "Concentrator document-to-OKF pipeline and seeded discrepancies by document pair",
        "S1_SVG_BAND_TITLE": "CONCENTRATOR COMPILER FLOW // CLICK ANY STAGE TO EXPLORE",
        "S1_NODE_A": "\n".join([
            f'{ind12}<text x="108" y="47" text-anchor="middle" font-family="\'Roboto Mono\', monospace" font-size="9" font-weight="700" fill="#C5221F">1. DOCUMENT PACK ({n} PDFs)</text>',
            f'{ind12}<text x="26" y="66" font-family="\'Plus Jakarta Sans\', sans-serif" font-size="10.5" font-weight="700" fill="#202124">&bull; {x.folder_count("pid") + x.folder_count("pfd")} P&amp;IDs, Lists &amp; PFDs</text>',
            f'{ind12}<text x="26" y="83" font-family="\'Plus Jakarta Sans\', sans-serif" font-size="10.5" font-weight="700" fill="#D93025">&bull; {s} Seeded Discrepancies</text>',
            f'{ind12}<text x="26" y="100" font-family="\'Plus Jakarta Sans\', sans-serif" font-size="10.5" font-weight="600" fill="#5F6368">&bull; C&amp;E, HAZOP, SDS, Manual</text>',
        ]),
        "S1_NODE_B": "\n".join([
            f'{ind12}<text x="343" y="47" text-anchor="middle" font-family="\'Roboto Mono\', monospace" font-size="9" font-weight="700" fill="#FFFFFF">2. GEMINI + ADK FUNCTION TOOLS</text>',
            f'{ind12}<text x="248" y="66" font-family="\'Plus Jakarta Sans\', sans-serif" font-size="10.5" font-weight="700" fill="#174EA6">&bull; Table text + drawing vision</text>',
            f'{ind12}<text x="248" y="83" font-family="\'Plus Jakarta Sans\', sans-serif" font-size="10.5" font-weight="700" fill="#174EA6">&bull; File-by-file read-merge-upsert</text>',
            f'{ind12}<text x="248" y="100" font-family="\'Plus Jakarta Sans\', sans-serif" font-size="10.5" font-weight="700" fill="#137333">&bull; Revision-aware (Rev A &rarr; B)</text>',
        ]),
        "S1_NODE_C": "\n".join([
            f'{ind12}<text x="574" y="47" text-anchor="middle" font-family="\'Roboto Mono\', monospace" font-size="9" font-weight="700" fill="#137333">3. OKF KNOWLEDGE BUNDLE</text>',
            f'{ind12}<text x="495" y="66" font-family="\'Plus Jakarta Sans\', sans-serif" font-size="10.5" font-weight="700" fill="#202124">&bull; {c} Concepts &bull; {len(x.edges)} Links</text>',
            f'{ind12}<text x="495" y="83" font-family="\'Plus Jakarta Sans\', sans-serif" font-size="10.5" font-weight="700" fill="#1E8E3E">&bull; {d}/{s} Conflicts, Cited</text>',
            f'{ind12}<text x="495" y="100" font-family="\'Plus Jakarta Sans\', sans-serif" font-size="10.5" font-weight="600" fill="#5F6368">&bull; Equipment, SIS, HAZOP</text>',
        ]),
        "S1_SVG_BOTTOM": _pairs_chart(x),
        "S1_BENCH_HEAD": "\n".join([
            '            <h2 class="section-title" style="font-size:16.5px; margin-bottom:0;">Measured on This Document Pack</h2>',
            f'            <span class="badge badge-primary tnum">{s} SEEDED + 1 DECOY</span>',
            '          </div>',
            '          <p class="section-subtitle" style="margin-bottom:10px;">',
            '            Ground truth fixed when the pack was generated; scored automatically against the compiled bundle.',
            '          </p>',
        ]),
        "S1_LEVER_TITLE": "WHY SEARCH AND CHUNKING ARE NOT ENOUGH",
        "S1_DRAWER_SUMMARY": "+ INSPECT DOCUMENTATION HEADWINDS &amp; MEASURED OUTCOMES",
        "S1_OUTCOMES_TITLE": "Measured Outcomes on the Ridgeback Concentrator Pack (synthetic)",
        "S1_SOWHAT": (f"{ind8}<span>One compiled knowledge base answers shutdown, SIS, reagent-safety and tailings questions "
                      "with the source document for every number &mdash; and shows where the documents disagree.</span>"),
        "S2_EYEBROW": "CONCENTRATOR PROCESS TOPOLOGY &bull; CRUSHING &rarr; GRINDING &rarr; FLOTATION &rarr; TAILINGS",
        "S2_H1": "12-Node Concentrator Twin With Cross-Document Conflicts",
        "S2_STEPPER_DEFAULT": "NODE 2/12 &bull; ML-3101",
        "S2_CONFLICT_BADGE": f"{d} Conflicts Flagged by the Agent",
        "S2_ZONES": _zones_html(nodes),
        "S2_DRAWER_ISA": ">AREA 31 // SAG MILLING</span>",
        "S2_DRAWER_TITLE": "ML-3101 &mdash; SAG Mill (40 ft x 22 ft, gearless drive)",
        "S2_DRAWER_LENS": "SHUTDOWN &bull; SIS &bull; DESIGN BASIS",
        "S2_DRAWER_SAP": ">" + _e(nodes[1]["sap_id"]) + "</div>",
        "S2_TELEMETRY_SUMMARY": "+ EXPAND ALL 12 CONCENTRATOR EQUIPMENT CARDS (DOCUMENT VALUES &amp; CONFLICTS)",
        "S2_TELEMETRY_BADGE": ">12 NODES</span>",
        "S2_SOWHAT": (f"{ind8}<span>Each node shows the value in every document that mentions the tag. Red nodes are items the agent "
                      "flagged as a cross-document conflict, with the governing source and the conflicting source.</span>"),
        "S3_EYEBROW": "CONCENTRATOR ROLES &amp; LIVE ADK WORKBENCH",
        "S3_COUNT_BADGE": f"{c} CONCEPTS &bull; {n} PDFS",
        "S3_PERSONA_ARIA": "Select Concentrator Engineering Persona",
        "S3_PERSONA_INITIALS": f'<span id="persona-hero-initials">{p0["initials"]}</span>',
        "S3_PERSONA_CODE": _e(p0["code"]) + "</span>",
        "S3_PERSONA_TITLE": _e(p0["name"]) + "</strong>",
        "S3_PERSONA_SPEED": "SOURCE-CITED ANSWERS",
        "S3_DAG_STEP1": f"{n} PDFs &bull; MD5 Index",
        "S3_DAG_STEP4": f'#D93025">{d}/{s} Conflicts Flagged</text>\n            <text x="82"',
        "S3_DAG_STEP5": f"{x.md_files} Files &bull; Validated",
        "S3_MODE_A": f"Mode A: Entity-Centric ({c} OKF Concepts)",
        "S3_MODE_B": f"Mode B: File-by-File Incremental ({n} Raw PDFs)",
        "S3_MD_BADGE": f"{x.md_files} MD FILES",
        "S3_CONCEPT_LABEL": f"Select Compiled OKF v0.2 Concept ({c} Concepts)",
        "S3_PDF_LABEL": f"Select Governing Raw Engineering PDF ({n} PDFs, synthetic pack)",
        "S3_PROMPT_DEFAULT": ("Mode A Entity-Centric: Extract and compile OKF v0.2 concept 'equipment/ML-3101' reconciling "
                              "the SAG mill data sheet, P&amp;ID and PFD sources."),
        "S3_OUTPUT_TITLE": f"build/okf_bundle/{nodes[1]['concept_id']}.md",
        "S4_H1": f"{len(x.nodes)}-Node Cross-Linked OKF Graph &amp; 7-Layer Cloud Stack",
        "S4_GCS_PATH": f"gs://ut-interaction-demo-okf-knowledge/{GCS_PREFIX}",
        "S4_GRAPH_H2": f"Interactive OKF v0.2 Property Graph ({len(x.nodes)} Domain Nodes &bull; {len(x.edges)} Cross-Links)",
        "S4_STAT_PDFS": f'<div class="datagraph-stat-value tnum">{n}</div>',
        "S4_STAT_CONCEPTS": f'<div class="datagraph-stat-value tnum">{c}</div>',
        "S4_STAT_CONFLICTS": f'color:var(--m3-critical);">{k_nodes}</div>',
        "S4_LEGEND_CONFLICT": f"Conflict Flagged ({k_nodes})",
        "S4_ARCH_SUPERSESSION": "Rev A&rarr;B Supersession",
        "S4_ARCH_CONFLICTS": f'#D93025">{d}/{s} Seeded Conflicts</text>\n          <text x="97"',
        "S4_ARCH_RAW": f"{n} Raw PDFs (Read-Only)",
        "S4_ARCH_MD": f"{x.md_files} OKF Markdown Files",
        "S4_SOWHAT": (f"{ind8}<span>Every concept in the {len(x.nodes)}-node graph lists the raw PDFs it came from; red nodes "
                      "carry at least one CONFLICT callout between two active documents.</span>"),
    }
    return t


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def build(ctx: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str], dict[str, Any]]:
    x = _Ctx(ctx)
    nodes = _schematic_nodes(x)
    scenarios = _scenarios(x)
    personas = _personas()
    meta = dict(x.base["meta"])
    meta.update({"gcs_prefix": GCS_PREFIX, "total_markdown_files": x.md_files, "corpus": "copper-concentrator",
                 "synthetic": True, "site": SITE["site"], "owner": SITE["owner"],
                 "seeded_conflicts": x.n_seeded, "seeded_detected": x.n_found})
    for node in nodes:
        node.pop("_conflicts", None)
    overrides = {
        "meta": meta,
        "manufacturing_scenarios": scenarios,
        "benchmark_bars": _benchmark(x),
        "headwinds": _headwinds(x),
        "levers": _levers(),
        "outcomes": _outcomes(x),
        "schematic_nodes": nodes,
        "personas": personas,
        "agent_tools": _agent_tools(x),
        "arch_layers": _arch_layers(x),
        "arch_controls": _arch_controls(x),
        "conflict_eval": x.ev,
    }
    ui = {
        "default_node_index": 1,
        "critical_dom_id": "node-ml3101",
        "flow_pairs": [
            ["node-cr2101", "node-ml3101"], ["node-ml3101", "node-pp3201"], ["node-ml3201", "node-pp3201"],
            ["node-pp3201", "node-cy3201"], ["node-cy3201", "node-ml3201"], ["node-cy3201", "node-fc4101"],
            ["node-sis3101", "node-ml3101"], ["node-tk4501", "node-fc4101"], ["node-tk4511", "node-fc4101"],
            ["node-fc4101", "node-th5101"], ["node-th5101", "node-pp5101"], ["node-fc4101", "node-pp6101"],
        ],
        "persona_flagship_concepts": [s["concept_id"] for s in sorted(scenarios, key=lambda s: s["persona_idx"])],
        "default_concept": nodes[1]["concept_id"],
        "default_graph_node": nodes[1]["concept_id"],
        "canvas_caption": "N\u25b2  CONCENTRATOR FLOW  |  CRUSHING \u2192 GRINDING \u2192 FLOTATION \u2192 TAILINGS",
        "raw_dir_label": "corpora/copper-concentrator/raw/",
    }
    return overrides, _html_tokens(x, nodes, scenarios, personas), ui


PROFILE = Profile(
    name="copper-concentrator",
    raw_dir=CORPUS_DIR / "raw",
    wiki_dir=CORPUS_DIR / "wiki",
    gcs_prefix=GCS_PREFIX,
    build=build,
    harness_required=["CONCENTRATOR", "SYNTHETIC"],
    harness_forbidden=["phenol", "Phenol", "cumene", "Cumene", "D-2304", "UOP", "AMS Selectivity",
                       "PAMA", "United Tractors", "Petrosea", "98.6%", "14d", "RED TEAM", "Red-Team"],
)
