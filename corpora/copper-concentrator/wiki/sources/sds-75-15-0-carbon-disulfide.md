---
type: Source Document
title: Safety Data Sheet Summary — Carbon Disulfide (Decomposition Product) (CAS 75-15-0)
description: Safety Data Sheet summary for carbon disulfide (CS2) decomposition product
  evolved in TK-4501 room, detailing CAS 75-15-0, flash point -30 °C, auto-ignition
  90 °C, LEL 1.3%, TWA 1 ppm (skin), handling, storage, and firefighting protocols.
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/sources/sds-75-15-0-carbon-disulfide.md
tags:
- area 45
- cas 75-15-0
- chemical safety
- cs2
- cs2-evolution
- decomposition product
- firefighting
- flash point
- hazard profile
- hazards
- lel
- pax
- reagents
- safety data sheet
- sds
- standards
- tk-4501
- twa
sources:
- id: src-1
  resource: corpora/copper-concentrator/raw/standards/SDS_75-15-0_carbon-disulfide.pdf
  title: SDS_75-15-0_carbon-disulfide.pdf
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T22:15:28Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T22:15:28Z'
- by: process:okf-validation-suite
  at: '2026-09-30T22:15:28Z'
status: stable
entity_metadata:
  acgih_twa_ppm: 1
  exposure_controls:
  - Local exhaust ventilation
  - Chemical goggles
  - Nitrile gloves
  - Respirator where exposure limits may be exceeded
  first_aid:
    inhalation: Remove to fresh air; seek medical attention
    eyes_and_skin: Flush eyes and skin with water for 15 minutes; seek medical attention
  plant_usage: Evolved in TK-4501 room
  firefighting_prohibition: Do not use water jet on burning xanthate
  cas_number: 75-15-0
  lel_pct: 1.3
  chemical_name: Carbon disulfide (decomposition product)
  target_equipment:
  - TK-4501
  - TK-4502
  - FN-4501
  chemical_formula: CS2
  hazards_identification: Flash point -30 degC, auto-ignition 90 degC, LEL 1.3 %,
    TWA 1 ppm (ACGIH skin)
  handling_storage: Store cool and dry, away from acids and ignition sources; keep
    containers closed
  skin_notation: true
  flash_point_c: -30
  autoignition_temperature_c: 90
  firefighting_media:
  - Dry chemical
  - CO2
  - Foam
  document_class: Chemical Safety Data Sheet Summary
---

# Safety Data Sheet Summary — Carbon Disulfide (Decomposition Product) (CAS 75-15-0)

> ⚠️ **CRITICAL PROCESS SAFETY / VOLATILE DECOMPOSITION HAZARD WARNING:**
> - **EXTREMELY LOW AUTO-IGNITION TEMPERATURE (90 °C) & WIDE EXPLOSIVE RANGE:** Carbon disulfide ($CS_2$, CAS 75-15-0) is an acute toxic off-gas with a flash point of **-30 °C**, a Lower Explosive Limit (LEL) of **1.3 %**, and an extraordinarily low auto-ignition temperature of **90 °C**. At 90 °C, $CS_2$ vapor can spontaneously ignite upon contact with low-pressure steam pipes, unlagged hot water tracing, or electrical light fixtures.
> - **EQUIPMENT RECONCILIATION (TK-4501 ROOM EVOLUTION):** SDS Summary `SDS_75-15-0_carbon-disulfide.pdf` explicitly documents plant use/service as: *"Evolved in TK-4501 room"*. This directly corroborates Process Data Sheet `RB-4410-PS-TK4501 Rev B`, P&ID `RB-4410-PID-45-001 Rev B` (Note 1), Concentrator Operating Manual `RB-4410-OM-001 Rev 2` (Sec 3.45 & Sec 8), and HAZOP Study `RB-4410-STD-HAZOP-001 Rev 1` (Node HZ-45-03), which identify $CS_2$ as the primary volatile hydrolysis product generated during the dissolution of potassium amyl xanthate (PAX) in mixing tank `TK-4501`.
> - **ACGIH OCCUPATIONAL EXPOSURE LIMIT (1 PPM SKIN):** The 8-hour Time-Weighted Average (TWA) is **1 ppm** with an ACGIH **"Skin"** notation, indicating that lethal/toxic doses can be readily absorbed percutaneously through intact skin as well as via inhalation.
> - **FIREFIGHTING DIRECTIVE & XANTHATE WATER JET PROHIBITION:** Approved extinguishing media are dry chemical, $CO_2$, or foam. SDS Section 5 mandates: **"Do not use water jet on burning xanthate."** Direct high-pressure water streams violently scatter burning molten xanthate and drive accelerated exothermic hydrolysis, releasing dense clouds of toxic and explosive $CS_2$ vapor into Area 45.

## Document Overview & Engineering Scope
- **Document Title:** Safety Data Sheet Summary - Carbon disulfide (decomposition product)
- **Source File:** `corpora/copper-concentrator/raw/standards/SDS_75-15-0_carbon-disulfide.pdf`
- **Document Class:** Chemical Safety Data Sheet Summary / Site Safety Standard
- **Chemical Name:** Carbon disulfide (decomposition product)
- **CAS Registry Number:** 75-15-0
- **Chemical Formula / Type:** $CS_2$
- **Target Plant Duty / Service:** Volatile toxic and explosive off-gas evolved in the enclosed reagent preparation room housing `TK-4501` (PAX Xanthate Mixing Tank) and `TK-4502` (PAX Dosing Tank).
- **Authority Scope:** Site summary for demonstration. Refer to supplier SDS for authoritative transport, toxicological, and industrial hygiene specifications.

## SDS Technical Specifications & Parameters
| SDS Section | Parameter / Topic | Value / Specification | Engineering & Operational Implications |
| :--- | :--- | :--- | :--- |
| **Section 1: Identification** | Product / Chemical Name | Carbon disulfide (decomposition product) | Primary volatile hazardous decomposition product of potassium amyl xanthate (PAX) |
| **Section 1: Identification** | Plant Use & Equipment Tag | Evolved in `TK-4501` room | Generated during batch dissolution of solid PAX pellets in 40 m³ tank `TK-4501` |
| **Section 1: Identification** | CAS Registry Number | 75-15-0 | Chemical Abstracts Service registry identifier |
| **Section 1: Identification** | Formula / Type | $CS_2$ | Linear symmetrical organosulfur molecule with high volatility |
| **Section 2: Hazards Identification** | Flash Point | -30 °C | Highly volatile Class 1 flammable vapor forming explosive mixtures at sub-zero temperatures |
| **Section 2: Hazards Identification** | Auto-Ignition Temperature | 90 °C | Dangerously low auto-ignition threshold; ignites on unlagged steam/hot water tracing or motor casings |
| **Section 2: Hazards Identification** | Lower Explosive Limit (LEL) | 1.3 % by volume in air | Explosive concentrations reached rapidly in unventilated or confined spaces |
| **Section 2: Hazards Identification** | Occupational Exposure Limit | TWA 1 ppm (ACGIH skin notation) | Severe chronic and acute neurotoxin; significant skin absorption route requires total barrier PPE |
| **Section 4: First Aid Measures** | Inhalation | Remove to fresh air; seek medical attention | Evacuate casualty upwind; administer oxygen if respiratory distress occurs |
| **Section 4: First Aid Measures** | Eye & Skin Contact | Flush eyes and skin with water for 15 minutes; seek medical attention | Continuous deluge flushing for 15 minutes; remove contaminated clothes immediately |
| **Section 5: Fire Fighting Measures** | Approved Extinguishing Media | Dry chemical, $CO_2$, or foam | Standard smothering and vapor suppression agents |
| **Section 5: Fire Fighting Measures** | Critical Firefighting Prohibition | Do not use water jet on burning xanthate | Water jets scatter burning solid xanthate and accelerate violent hydrolysis into $CS_2$ gas |
| **Section 7: Handling & Storage** | Storage & Handling Conditions | Store cool and dry, away from acids and ignition sources | Dedicated enclosed ventilated reagent shed; maintain mix water < 40 °C to prevent evolution |
| **Section 7: Handling & Storage** | Container Management | Keep containers closed | Exclude moisture and atmospheric air; prevent escape of evolved vapors into work environment |
| **Section 8: Exposure Controls & PPE** | Engineering Controls | Local exhaust ventilation | Continuous 24/7 mechanical exhaust via extraction fan `FN-4501` maintaining room negative pressure |
| **Section 8: Exposure Controls & PPE** | Eye Protection | Chemical goggles | Splash-tight goggles during PAX charging, mixing, or line breaking |
| **Section 8: Exposure Controls & PPE** | Hand / Skin Protection | Nitrile gloves | Chemical-resistant nitrile gauntlet gloves preventing dermal absorption |
| **Section 8: Exposure Controls & PPE** | Respiratory Protection | Respirator where exposure limits may be exceeded | Air-purifying respirator with organic vapor cartridges (or SCBA in confined spaces) |

## Cross-Document Reconciliation & Alignment
1. **Source Grounding & Reagent Synergy:**
   - Safety Data Sheet `standards/SDS_75-15-0_carbon-disulfide.pdf` establishes the chemical identity and physical hazards of $CS_2$ specifically noting *"use: Evolved in TK-4501 room"*.
   - Process Data Sheet `RB-4410-PS-TK4501 Rev B` specifies under Primary Hazard: *"CS2 evolution on decomposition"*.
   - P&ID `RB-4410-PID-45-001 Rev B` Note 1 mandates that extraction fan `FN-4501` run continuously 24/7 to exhaust $CS_2$ vapors from the enclosed mixing room housing `TK-4501` and `TK-4502`.
   - Concentrator Operating Manual `RB-4410-OM-001 Rev 2` Section 8 explicitly cites $CS_2$ flammability properties (LEL 1.3%, auto-ignition 90 °C) and mandates mix water temperatures strictly $<40$ °C to inhibit hydrolysis.
   - HAZOP Study `RB-4410-STD-HAZOP-001 Rev 1` Node HZ-45-03 mandates recommendation `ACT-HAZOP-45-03`: install continuous $CS_2$ gas detector `AT-4501` with alarm at 10 % LEL interlocked to switch `FN-4501` to high speed and execute an automatic trip of the solid PAX feeder.
   - *Status:* 100% corroborated across all engineering documents with zero discrepancies.

2. **Auto-Ignition Temperature Reconciliation:**
   - `SDS_75-15-0_carbon-disulfide.pdf` lists auto-ignition at **90 °C**, perfectly aligning with `RB-4410-OM-001 Rev 2` Section 8 (90 °C).
   - Some general chemical engineering reference literature cites 100 °C for pure $CS_2$. The governing site standard and operating manual mandate the conservative 90 °C auto-ignition threshold.

3. **Firefighting Strategy Integration across Area 45:**
   - SDS Section 5 states: *"Dry chemical, CO2 or foam. Do not use water jet on burning xanthate."*
   - This directive appears identically across `SDS_2720-73-2_potassium-amyl-xanthate.pdf`, `SDS_108-11-2_mibc.pdf`, and `SDS_1305-78-8_quicklime---hydrated-lime.pdf`, ensuring consistent firefighting tactics throughout the Area 45 reagent precinct.

## Affected Plant Entities & Cross-References
- **Equipment Concepts:**
  - `equipment/TK-4501` (PAX Xanthate Mixing Tank)
  - `equipment/TK-4502` (PAX Dosing Tank)
  - `equipment/FN-4501` (PAX Mixing Room Extraction Fan)
- **Hazard Profiles:**
  - `hazards/carbon-disulfide` (Carbon Disulfide Chemical Safety & Decomposition Hazard Profile)
  - `hazards/potassium-amyl-xanthate` (Potassium Amyl Xanthate Chemical Safety & Hazard Profile)
  - `hazards/comminution-slurry-hazards` (Comminution, Classification, Flotation, Tailings & Reagents Process Safety Hazards)
- **HAZOP Studies:**
  - `hazop/concentrator-hazop-study` (Node HZ-45-03: PAX Mixing Room $CS_2$ Accumulation)
- **Unit Overviews:**
  - `units/flotation` (Flotation and Regrind Circuit)
  - `units/copper-concentrator` (Overall Concentrator Plant Overview)
- **Operating Parameters:**
  - `parameters/concentrator-design-basis` (Overall Process Design Basis)

## References & Sources
[^src-1]: SDS_75-15-0_carbon-disulfide.pdf (corpora/copper-concentrator/raw/standards/SDS_75-15-0_carbon-disulfide.pdf)
