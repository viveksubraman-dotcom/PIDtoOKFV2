"""Ridgeback Concentrator (fictional, Cymbal Copper) - single source of truth for the synthetic mining corpus.

Every number rendered into any PDF of the synthetic document pack comes from this module.
Deliberate cross-document discrepancies are declared ONLY in ``SEEDED_CONFLICTS`` and applied
by the renderer through ``value_in(doc_id, tag, parameter)``; everything else is consistent by
construction. ``SEEDED_CONFLICTS`` doubles as the ground truth for the conflict-detection eval.

SYNTHETIC DEMO DATA. Not a real plant, not a real design. Physically plausible magnitudes only.
"""

from __future__ import annotations

from dataclasses import dataclass, field

SITE = {
    "owner": "Cymbal Copper Pty Ltd (fictional)",
    "site": "Ridgeback Concentrator",
    "project_no": "RB-4410",
    "ore": "Porphyry copper-gold (chalcopyrite dominant)",
    "disclaimer": "SYNTHETIC DEMONSTRATION DOCUMENT - fictional plant generated for a Google Cloud demo. Not for design or operation.",
}

# ---------------------------------------------------------------------------
# Design basis
# ---------------------------------------------------------------------------
DESIGN = {
    "throughput_tpd": 60_000,          # t/d dry, nameplate
    "availability": 0.93,              # grinding circuit availability
    "head_cu_pct": 0.55,
    "head_au_gpt": 0.35,
    "cu_recovery": 0.89,
    "au_recovery": 0.70,
    "conc_cu_pct": 26.0,
    "ore_sg": 2.75,
    "bwi_kwh_t": 15.2,                 # ball mill work index
    "axb": 38.0,                       # JK drop-weight A*b (moderately hard)
    "sag_feed_f80_mm": 150,
    "cyclone_of_p80_um": 150,
    "circulating_load": 3.00,          # 300 %
    "cyclone_feed_solids_w": 0.60,     # 60 % w/w (design)
    "cyclone_of_solids_w": 0.35,
    "rougher_feed_ph": 10.5,
    "regrind_p80_um": 38,
}

FRESH_TPH = round(DESIGN["throughput_tpd"] / (24 * DESIGN["availability"]))  # 2,688 t/h


def _slurry(solids_tph: float, solids_w: float, sg: float = DESIGN["ore_sg"]) -> dict:
    water = solids_tph * (1 - solids_w) / solids_w
    vol = solids_tph / sg + water
    return {
        "solids_tph": round(solids_tph),
        "water_tph": round(water),
        "solids_w_pct": round(solids_w * 100, 1),
        "slurry_m3h": round(vol),
        "slurry_sg": round((solids_tph + water) / vol, 3),
    }


def mass_balance() -> dict[str, dict]:
    """Steady-state design mass balance (grinding + flotation + thickening)."""
    f = FRESH_TPH
    cl = DESIGN["circulating_load"]
    conc = f * DESIGN["head_cu_pct"] / 100 * DESIGN["cu_recovery"] / (DESIGN["conc_cu_pct"] / 100)
    tails = f - conc
    s = {
        "S-101": {"name": "Primary crusher product to stockpile", **_slurry(f, 0.97)},
        "S-301": {"name": "SAG mill fresh feed", **_slurry(f, 0.97)},
        "S-305": {"name": "Pebble crusher recycle", **_slurry(f * 0.18, 0.97)},
        "S-321": {"name": "Cyclone feed (total, 2 duty pumps)", **_slurry(f * (1 + cl), DESIGN["cyclone_feed_solids_w"])},
        "S-323": {"name": "Cyclone underflow to ball mill", **_slurry(f * cl, 0.75)},
        "S-324": {"name": "Cyclone overflow to flotation", **_slurry(f, DESIGN["cyclone_of_solids_w"])},
        "S-411": {"name": "Rougher concentrate to regrind", **_slurry(f * 0.08, 0.30)},
        "S-431": {"name": "Final concentrate to thickener", **_slurry(conc, 0.28)},
        "S-511": {"name": "Concentrate thickener underflow", **_slurry(conc, 0.65, 4.1)},
        "S-611": {"name": "Final tailings to thickener", **_slurry(tails, 0.33)},
        "S-621": {"name": "Tailings thickener underflow to TSF", **_slurry(tails, 0.62)},
    }
    s["S-511"]["name"] = "Concentrate thickener underflow"
    per_pump = dict(s["S-321"])
    per_pump.update({k: round(v / 2) for k, v in s["S-321"].items() if k in ("solids_tph", "water_tph", "slurry_m3h")})
    per_pump["name"] = "Cyclone feed per duty pump (PP-3201A/B, C standby)"
    s["S-322"] = per_pump
    s["_meta"] = {"conc_tph": round(conc, 1), "tails_tph": round(tails), "fresh_tph": f}
    return s


MB = mass_balance()

# ---------------------------------------------------------------------------
# Equipment register (design values = the TRUE values; conflicts override per document)
# ---------------------------------------------------------------------------
@dataclass
class Equip:
    tag: str
    name: str
    area: str
    cls: str
    params: dict[str, tuple[str, str]]          # parameter -> (value, unit)
    function: str = ""
    connections: list[str] = field(default_factory=list)


AREAS = {
    "21": "Primary Crushing",
    "31": "SAG Milling",
    "32": "Ball Milling & Classification",
    "41": "Rougher Flotation",
    "43": "Regrind & Cleaner Flotation",
    "45": "Reagents (Xanthate, Frother, Lime)",
    "51": "Concentrate Thickening & Filtration",
    "61": "Tailings Thickening & Pumping",
}

EQUIPMENT: list[Equip] = [
    Equip("CR-2101", "Primary Gyratory Crusher", "21", "Crusher", {
        "Type": ("Gyratory 60 x 113", ""), "Installed power": ("1,200", "kW"), "Design throughput": ("5,500", "t/h"),
        "Closed side setting": ("165", "mm"), "Product P80": ("150", "mm"), "Feed opening": ("1,525", "mm")},
        "Reduces ROM ore to SAG feed size; discharges to CV-2101 overland conveyor.", ["CV-2101", "FE-2101"]),
    Equip("ML-3101", "SAG Mill", "31", "Grinding Mill", {
        "Diameter x EGL": ("12.2 x 6.7 (40 ft x 22 ft)", "m"), "Installed power": ("22,000", "kW"),
        "Drive": ("Gearless motor drive (GMD), variable speed", ""), "Speed range": ("60 - 80", "% critical"),
        "Ball charge": ("12 - 15", "% vol"), "Total filling max": ("30", "% vol"), "Design throughput": (f"{FRESH_TPH:,}", "t/h"),
        "Specific energy": ("8.2", "kWh/t"), "Liner": ("Cr-Mo steel shell lifters, 50 mm", ""),
        "Trunnion bearings": ("Hydrostatic / hydrodynamic, 2 x 2 pads", "")},
        "Primary autogenous/semi-autogenous grinding of crushed ore; discharges via trommel/screen SC-3101.",
        ["CV-3101", "SC-3101", "CR-3102", "PP-3201A"]),
    Equip("CR-3102", "Pebble Crusher", "31", "Crusher", {
        "Type": ("Cone crusher, extra-coarse", ""), "Installed power": ("750", "kW"), "Design throughput": (f"{round(FRESH_TPH*0.18):,}", "t/h"),
        "Closed side setting": ("12", "mm")}, "Crushes SAG critical-size pebbles; returns to CV-3101.", ["SC-3101", "CV-3101"]),
    Equip("ML-3201", "Ball Mill", "32", "Grinding Mill", {
        "Diameter x EGL": ("8.2 x 13.4 (27 ft x 44 ft)", "m"), "Installed power": ("22,000", "kW"),
        "Drive": ("Gearless motor drive (GMD), fixed speed", ""), "Speed": ("75", "% critical"),
        "Ball charge": ("32 - 35", "% vol"), "Media size": ("65", "mm"), "Specific energy": ("8.0", "kWh/t")},
        "Secondary grinding in closed circuit with cyclone cluster CY-3201.", ["CY-3201", "PP-3201A"]),
    Equip("PP-3201A", "Cyclone Feed Pump (A/B duty, C standby)", "32", "Centrifugal Slurry Pump", {
        "Service": ("Cyclone feed", ""), "Configuration": ("2 duty + 1 standby (PP-3201A/B/C)", ""),
        "Rated flow": (f"{MB['S-322']['slurry_m3h']:,}", "m3/h"), "Slurry SG": (f"{MB['S-322']['slurry_sg']}", ""),
        "Solids concentration": (f"{MB['S-322']['solids_w_pct']}", "% w/w"), "Total dynamic head": ("32", "m"),
        "Motor power": ("1,600", "kW"), "Casing design pressure": ("10", "bar(g)"), "Liner": ("High-chrome white iron", "")},
        "Pumps ball mill discharge + SAG product to cyclone cluster CY-3201.", ["ML-3201", "CY-3201"]),
    Equip("CY-3201", "Cyclone Cluster", "32", "Hydrocyclone", {
        "Cyclones": ("16 x 660 mm (13 operating / 3 standby)", ""), "Feed pressure": ("100 - 130", "kPa"),
        "Feed density": (f"{MB['S-321']['solids_w_pct']}", "% solids w/w"), "Overflow P80": ("150", "um"),
        "Overflow density": ("35", "% solids w/w")}, "Classifies grinding product; overflow to flotation.", ["PP-3201A", "ML-3201", "TK-4101"]),
    Equip("FC-4101", "Rougher Flotation Tank Cells (FC-4101 to FC-4107)", "41", "Flotation Cell", {
        "Cells": ("7 x 300 m3 forced-air tank cells", ""), "Residence time": ("32", "min"),
        "Air rate": ("0.8 - 1.6", "m/s superficial"), "Agitator power": ("7 x 250", "kW")},
        "Rougher flotation of cyclone overflow; rougher concentrate to regrind ML-4201.", ["TK-4101", "ML-4201", "TH-6101"]),
    Equip("ML-4201", "Regrind Mill (vertical stirred)", "43", "Grinding Mill", {
        "Installed power": ("3,000", "kW"), "Product P80": ("38", "um"), "Media": ("Ceramic 3 - 5 mm", "")},
        "Regrinds rougher concentrate for liberation ahead of cleaning.", ["FC-4101", "FC-4301"]),
    Equip("FC-4301", "Cleaner Flotation Column", "43", "Flotation Column", {
        "Diameter x height": ("4.5 x 12", "m"), "Wash water": ("35", "m3/h"), "Concentrate grade": ("26", "% Cu")},
        "Final cleaning stage producing saleable Cu-Au concentrate.", ["ML-4201", "TH-5101"]),
    Equip("TK-4501", "PAX Xanthate Mixing Tank", "45", "Reagent Tank", {
        "Volume": ("40", "m3"), "Solution strength": ("20", "% w/v"), "Material": ("316L stainless steel", ""),
        "Ventilation": ("Enclosed room, extraction fan FN-4501", ""), "Hazard": ("CS2 evolution on decomposition", "")},
        "Mixes solid potassium amyl xanthate (PAX) with process water; transfers to dosing tank TK-4502.", ["TK-4502", "FN-4501"]),
    Equip("TK-4511", "Frother Storage Tank", "45", "Reagent Tank", {
        "Volume": ("30", "m3"), "Reagent": ("MIBC (methyl isobutyl carbinol)", ""), "Flash point": ("41", "degC"),
        "Hazardous area": ("Zone 2 (flammable liquid, Class 3)", "")}, "Stores and doses frother to flotation.", ["FC-4101", "FC-4301"]),
    Equip("TK-4521", "Milk-of-Lime Tank", "45", "Reagent Tank", {
        "Volume": ("150", "m3"), "Slurry strength": ("20", "% w/w Ca(OH)2"), "pH control": ("AIC-4101, rougher feed pH 10.5", "")},
        "Lime slurry from slaker SL-4521 for pH control and pyrite depression.", ["SL-4521", "TK-4101"]),
    Equip("TH-5101", "Concentrate Thickener", "51", "Thickener", {
        "Type": ("High-rate", ""), "Diameter": ("30", "m"), "Underflow density": ("65", "% solids w/w"),
        "Flocculant dose": ("15 - 25", "g/t")}, "Thickens final concentrate ahead of filtration.", ["FC-4301", "PP-5101A", "FP-5101"]),
    Equip("PP-5101A", "Concentrate Thickener Underflow Pump", "51", "Centrifugal Slurry Pump", {
        "Rated flow": ("210", "m3/h"), "Slurry SG": ("2.0", ""), "Total dynamic head": ("28", "m"), "Motor power": ("75", "kW")},
        "Transfers thickened concentrate to filter feed tank.", ["TH-5101", "FP-5101"]),
    Equip("FP-5101", "Concentrate Filter Press", "51", "Filter", {
        "Type": ("Vertical plate pressure filter", ""), "Filtration area": ("144", "m2"), "Cake moisture": ("8.5", "% w/w"),
        "Transportable moisture limit (TML)": ("9.8", "% w/w")}, "Dewaters concentrate below TML for shipping.", ["PP-5101A"]),
    Equip("TH-6101", "Tailings Thickener", "61", "Thickener", {
        "Type": ("High-rate", ""), "Diameter": ("60", "m"), "Underflow density": ("62", "% solids w/w"),
        "Rake torque (design)": ("12.5", "MNm")}, "Thickens final tailings; water returned to process water tank.", ["FC-4101", "PP-6101A"]),
    Equip("PP-6101A", "Tailings Pumps (3 stages in series, PP-6101A/B/C)", "61", "Centrifugal Slurry Pump", {
        "Rated flow": (f"{MB['S-621']['slurry_m3h']:,}", "m3/h"), "Slurry SG": (f"{MB['S-621']['slurry_sg']}", ""),
        "Stages": ("3 in series to TSF (6.2 km)", ""), "Discharge pressure (stage 3)": ("34", "bar(g)"),
        "Casing design pressure (stage 3)": ("40", "bar(g)"), "Motor power": ("3 x 2,000", "kW")},
        "Pumps thickened tailings to the tailings storage facility (TSF).", ["TH-6101"]),
]
EQ = {e.tag: e for e in EQUIPMENT}

# Instruments and SIS
INSTRUMENTS = [
    # tag, service, range, alarm/trip, sis
    ("TT-3101", "SAG mill drive-end trunnion bearing temperature", "0-150 degC", "TAH 70 degC / TAHH 75 degC", "SIF-3101 (SIL 1) stop SAG mill"),
    ("TT-3102", "SAG mill non-drive-end trunnion bearing temperature", "0-150 degC", "TAH 70 degC / TAHH 75 degC", "SIF-3101 (SIL 1) stop SAG mill"),
    ("PT-3104", "SAG hydrostatic lift oil pressure", "0-250 bar(g)", "PAL 90 bar(g) / PALL 70 bar(g)", "SIF-3102 inhibit mill start / stop"),
    ("PSV-3105", "SAG HP lift pump discharge relief", "-", "Set pressure 160 bar(g) (system design 170 bar(g))", "Mechanical relief"),
    ("PT-3201", "Cyclone feed pressure", "0-250 kPa", "PAL 90 kPa / PAH 140 kPa", "-"),
    ("DT-3201", "Cyclone feed density (nuclear)", "1.0-2.0 SG", "-", "-"),
    ("AIC-4101", "Rougher feed pH", "0-14 pH", "AL 10.0 / AH 11.2", "-"),
    ("PT-6103", "Tailings stage-3 discharge pressure", "0-60 bar(g)", "PAH 36 bar(g) / PAHH 38 bar(g)", "SIF-6101 (SIL 2) trip PP-6101A/B/C"),
    ("LT-6101", "Tailings thickener bed level", "0-10 m", "LAH 6.5 m", "-"),
]

REAGENTS = [
    # name, formula/type, cas, hazard summary, used in
    ("Potassium amyl xanthate (PAX)", "C6H11KOS2", "2720-73-2", "Self-heating solid; decomposes (moisture, heat, acid) releasing carbon disulfide (CS2) - highly flammable, toxic; LEL 1.3 %", "TK-4501 / TK-4502, collector"),
    ("Carbon disulfide (decomposition product)", "CS2", "75-15-0", "Flash point -30 degC, auto-ignition 90 degC, LEL 1.3 %, TWA 1 ppm (ACGIH skin)", "Evolved in TK-4501 room"),
    ("MIBC (methyl isobutyl carbinol)", "C6H14O", "108-11-2", "Flammable liquid Cat 3, flash point 41 degC; STOT SE 3", "TK-4511, frother"),
    ("Polyglycol ether frother (DF-250 type)", "Polypropylene glycol methyl ether", "37286-64-9", "Combustible, flash point >100 degC; eye irritant", "Alternative frother (not specified for TK-4511)"),
    ("Quicklime / hydrated lime", "CaO / Ca(OH)2", "1305-78-8 / 1305-62-0", "Skin corrosion 1B / serious eye damage 1; exothermic with water (slaker)", "SL-4521 / TK-4521, pH modifier"),
    ("Anionic polyacrylamide flocculant", "PAM", "9003-05-8", "Low toxicity; spills extremely slippery", "TH-5101 / TH-6101"),
]

HAZOP_NODES = [
    ("HZ-31-02", "SAG mill hydrostatic lift system", "More pressure", "HP lift pump dead-heads against closed valve", "Oil line rupture, fire at mill", "PSV-3105 set <= system design pressure 170 bar(g)", "Confirm PSV-3105 set pressure on P&ID matches data sheet"),
    ("HZ-31-04", "SAG mill trunnion bearings", "More temperature", "Loss of lube oil flow / cooling", "Bearing wipe, 10-14 day unplanned outage", "TT-3101/3102 TAHH trip via SIF-3101", "Align TAHH setpoint between instrument data sheet and cause & effect"),
    ("HZ-45-03", "PAX xanthate mixing room", "Other than (decomposition)", "Wet/hot PAX, acid contamination", "CS2 accumulation - flash fire / toxic exposure", "Extraction fan FN-4501", "Install CS2 gas detector AT-4501 (alarm 10 % LEL) interlocked to FN-4501 high speed and PAX feeder stop"),
    ("HZ-45-06", "Frother storage TK-4511", "Other than (wrong reagent)", "Frother specification changed", "Hazardous-area classification invalid", "Area classified Zone 2 for MIBC", "Confirm frother identity on P&ID vs data sheet and SDS"),
    ("HZ-61-01", "Tailings pumping to TSF", "More pressure", "Blocked line / valve closure at TSF", "Pipeline rupture, tailings release to environment", "PT-6103 PAHH trip SIF-6101 (SIL 2)", "Confirm stage-3 casing design pressure on P&ID"),
]

# ---------------------------------------------------------------------------
# Seeded discrepancies = eval ground truth.  (doc_id, tag, parameter) -> rendered value.
# ---------------------------------------------------------------------------
SEEDED_CONFLICTS = [
    {"id": "C01", "tag": "ML-3101", "parameter": "Installed power", "true_doc": "DS-ML-3101", "true": "22,000 kW",
     "conflict_doc": "PID-31-001", "conflict": "20,000 kW", "class": "Rating mismatch",
     "why": "Motor/GMD rating drives protection settings and shutdown power studies."},
    {"id": "C02", "tag": "PP-3201A", "parameter": "Rated flow", "true_doc": "PFD-001", "true": f"{MB['S-322']['slurry_m3h']:,} m3/h",
     "conflict_doc": "DS-PP-3201", "conflict": "4,650 m3/h", "class": "Sizing mismatch",
     "why": "Data sheet sized for 250 % circulating load; mass balance is 300 %. Pumps under-rated -> sanding, cyclone roping."},
    {"id": "C03", "tag": "CY-3201", "parameter": "Feed density", "true_doc": "PFD-001", "true": f"{MB['S-321']['solids_w_pct']} % solids w/w",
     "conflict_doc": "OM-RB-001", "conflict": "65 % solids w/w", "class": "Operating basis mismatch",
     "why": "Operating manual target exceeds design; coarser overflow and flotation recovery loss."},
    {"id": "C04", "tag": "TT-3101", "parameter": "TAHH trip setpoint", "true_doc": "DS-INST-TEMP", "true": "75 degC",
     "conflict_doc": "CE-31-001", "conflict": "85 degC", "class": "SIS setpoint mismatch",
     "why": "Trip in logic is 10 degC above the instrument data sheet; bearing wipe risk (HZ-31-04)."},
    {"id": "C05", "tag": "PP-6101A", "parameter": "Casing design pressure (stage 3)", "true_doc": "DS-PP-6101", "true": "40 bar(g)",
     "conflict_doc": "PID-61-001", "conflict": "4.0 bar(g)", "class": "Decimal / unit error",
     "why": "10x error on the drawing; any isolation or re-rating based on the P&ID is unsafe."},
    {"id": "C06", "tag": "TK-4511", "parameter": "Reagent", "true_doc": "DS-TK-4511", "true": "MIBC (methyl isobutyl carbinol)",
     "conflict_doc": "PID-45-001", "conflict": "Polyglycol ether frother (DF-250 type)", "class": "Chemical identity mismatch",
     "why": "Flash point 41 degC vs >100 degC changes hazardous-area classification (HZ-45-06)."},
    {"id": "C07", "tag": "TH-5101", "parameter": "Diameter", "true_doc": "DS-TH-5101", "true": "30 m",
     "conflict_doc": "PID-51-001", "conflict": "25 m", "class": "Dimension mismatch",
     "why": "Thickener area drives flux rating and flocculant dose."},
    {"id": "C08", "tag": "CR-2101", "parameter": "Installed power", "true_doc": "DS-CR-2101", "true": "1,200 kW",
     "conflict_doc": "EL-001", "conflict": "1,000 kW", "class": "Register mismatch",
     "why": "Equipment list feeds the electrical load list and spares catalogue."},
    {"id": "C09", "tag": "TK-4501", "parameter": "CS2 gas detection (AT-4501)", "true_doc": "HAZOP-001", "true": "Required: AT-4501 alarm 10 % LEL, interlock to FN-4501",
     "conflict_doc": "PID-45-001", "conflict": "Not shown on P&ID", "class": "Missing safeguard",
     "why": "HAZOP recommendation HZ-45-03 not carried into the drawing - CS2 flash-fire exposure."},
    {"id": "C10", "tag": "PSV-3105", "parameter": "Set pressure", "true_doc": "DS-INST-PRES", "true": "160 bar(g)",
     "conflict_doc": "PID-31-002", "conflict": "180 bar(g)", "class": "Relief above design pressure",
     "why": "P&ID set pressure exceeds 170 bar(g) system design pressure (HZ-31-02)."},
    {"id": "C11", "tag": "ML-3201", "parameter": "Installed power", "true_doc": "DS-ML-3201 (Sheet 1)", "true": "22,000 kW",
     "conflict_doc": "DS-ML-3201 (Sheet 3)", "conflict": "20,500 kW", "class": "Intra-document sheet mismatch",
     "why": "Cover sheet and motor sheet of the same data sheet disagree."},
]
# Revision supersession decoy: must update in place, NOT be flagged as conflict.
REVISION_DECOY = {"tag": "PP-5101A", "parameter": "Rated flow", "old": ("Rev A", "180 m3/h"), "new": ("Rev B", "210 m3/h")}

_OVERRIDES = {(c["conflict_doc"], c["tag"], c["parameter"]): c["conflict"] for c in SEEDED_CONFLICTS}


def value_in(doc_id: str, tag: str, parameter: str) -> str:
    """Value of (tag, parameter) as rendered in a given document (applies seeded conflicts)."""
    if (doc_id, tag, parameter) in _OVERRIDES:
        return _OVERRIDES[(doc_id, tag, parameter)]
    v, u = EQ[tag].params[parameter]
    return f"{v} {u}".strip()


if __name__ == "__main__":
    import json
    print(json.dumps({k: v for k, v in MB.items()}, indent=1))
    print(len(EQUIPMENT), "equipment;", len(SEEDED_CONFLICTS), "seeded conflicts")
