---
type: Source Document
title: Safety Data Sheet Summary — Potassium Amyl Xanthate (PAX) (CAS 2720-73-2)
description: Safety Data Sheet summary for Potassium Amyl Xanthate (PAX) collector
  reagent used in TK-4501 and TK-4502, detailing CAS 2720-73-2, self-heating solid
  classification, CS2 toxic/flammable off-gas hazards, and handling controls.
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/sources/sds-2720-73-2-potassium-amyl-xanthate.md
tags:
- area 45
- cas 2720-73-2
- collector
- cs2
- cs2-evolution
- hazard profile
- pax
- potassium-amyl-xanthate
- process safety
- reagents
- sds
- self-heating-solid
- standards
- tk-4501
- tk-4502
sources:
- id: src-1
  resource: corpora/copper-concentrator/raw/standards/SDS_2720-73-2_potassium-amyl-xanthate.pdf
  title: SDS_2720-73-2_potassium-amyl-xanthate.pdf
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T22:06:15Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T22:06:15Z'
- by: process:okf-validation-suite
  at: '2026-09-30T22:06:15Z'
status: stable
entity_metadata:
  chemical_name: Potassium amyl xanthate (PAX)
  document_class: Chemical Safety Data Sheet Summary
  first_aid:
    eyes_and_skin: Flush eyes and skin with water for 15 minutes; seek medical attention
    inhalation: Remove to fresh air; seek medical attention
  firefighting_prohibition: Do not use water jet on burning xanthate
  handling_storage: Store cool and dry, away from acids and ignition sources; keep
    containers closed
  lel_pct: 1.3
  exposure_controls:
  - Local exhaust ventilation
  - Chemical goggles
  - Nitrile gloves
  - Respirator where exposure limits may be exceeded
  target_equipment:
  - TK-4501
  - TK-4502
  - FN-4501
  - PP-4501A
  - TK-4101
  - FC-4101
  chemical_formula: C6H11KOS2
  firefighting_media:
  - Dry chemical
  - CO2
  - Foam
  hazards_identification: Self-heating solid; decomposes (moisture, heat, acid) releasing
    carbon disulfide (CS2) - highly flammable, toxic; LEL 1.3 %
  plant_usage: Collector reagent in TK-4501 / TK-4502
  cas_number: 2720-73-2
---

# Safety Data Sheet Summary — Potassium Amyl Xanthate (PAX) (CAS 2720-73-2)

> ⚠️ **CRITICAL PROCESS SAFETY / REAGENT INTEGRITY WARNING:**
> - **SELF-HEATING SOLID & SPONTANEOUS TOXIC/EXPLOSIVE DECOMPOSITION:** Solid potassium amyl xanthate (PAX, CAS 2720-73-2, $C_6H_{11}KOS_2$) is classified as a **Self-heating solid**. When exposed to moisture, ambient heat (>40 °C), or acidic environments, it undergoes spontaneous hydrolysis and decomposition to evolve **carbon disulfide ($CS_2$)**—a volatile, acute neurotoxin and explosive vapor with a Lower Explosive Limit (LEL) of **1.3 %** and an extraordinarily low auto-ignition temperature of **90 °C**.
> - **EQUIPMENT RECONCILIATION (TK-4501 / TK-4502):** SDS Summary `SDS_2720-73-2_potassium-amyl-xanthate.pdf` explicitly designates the plant usage for **TK-4501** (PAX Xanthate Mixing Tank) and **TK-4502** (PAX Dosing Tank) as the primary flotation collector reagent. This directly corroborates Process Data Sheet `RB-4410-PS-TK4501 Rev B`, P&ID `RB-4410-PID-45-001 Rev B`, Concentrator Operating Manual `RB-4410-OM-001 Rev 2` (Sections 3.45 & 8), and HAZOP Study `RB-4410-STD-HAZOP-001 Rev 1` (Node HZ-45-03).
> - **FIREFIGHTING MEDIA & AREA 45 CROSS-REAGENT PROHIBITION:** Extinguish xanthate fires using dry chemical, $CO_2$, or foam. **Do not use water jet on burning xanthate.** Direct water jets violently agitate and scatter burning molten xanthate and accelerate exothermic hydrolysis into dense toxic $CS_2$ vapor clouds. This prohibition is cross-referenced in site SDS summaries for adjacent reagents (MIBC and quicklime).

## Document Overview & Engineering Scope
- **Document Title:** Safety Data Sheet Summary - Potassium amyl xanthate (PAX)
- **Source File:** `corpora/copper-concentrator/raw/standards/SDS_2720-73-2_potassium-amyl-xanthate.pdf`
- **Document Class:** Chemical Safety Data Sheet Summary / Plant Safety Standard
- **Chemical Name:** Potassium amyl xanthate (PAX) / Potassium O-pentyl dithiocarbonate
- **CAS Registry Number:** 2720-73-2
- **Chemical Formula / Type:** $C_6H_{11}KOS_2$ (or $C_5H_{11}OCS_2K$)
- **Target Plant Duty / Service:** Primary sulfide mineral flotation collector prepared as 20% w/v aqueous solution in `TK-4501`, stored in `TK-4502`, and metered via `PP-4501A` to rougher conditioning tank `TK-4101` and flotation cells `FC-4101` through `FC-4107`.
- **Authority Scope:** Site summary for demonstration. Refer to supplier SDS for authoritative transport, handling, and toxicological details.

## SDS Technical Specifications & Parameters
| SDS Section | Parameter / Topic | Value / Specification | Engineering & Operational Implications |
| :--- | :--- | :--- | :--- |
| **Section 1: Identification** | Product / Chemical Name | Potassium amyl xanthate (PAX) | Primary sulfide mineral flotation collector |
| **Section 1: Identification** | Plant Use & Equipment Tags | `TK-4501` / `TK-4502`, collector | Batch mixing in TK-4501 (40 m³ 316L SS), buffer storage in TK-4502 |
| **Section 1: Identification** | CAS Registry Number | 2720-73-2 | Standard numerical chemical identifier |
| **Section 1: Identification** | Chemical Formula / Type | $C_6H_{11}KOS_2$ | Organosulfur potassium salt of amyl xanthic acid |
| **Section 2: Hazards Identification** | Physical / Chemical Hazard | Self-heating solid | Bulk solid pellets generate internal heat if stored damp or unventilated |
| **Section 2: Hazards Identification** | Decomposition Mechanism | Decomposes (moisture, heat, acid) | Hydrolysis releases toxic and flammable carbon disulfide ($CS_2$) gas |
| **Section 2: Hazards Identification** | Off-Gas Hazard Profile | Carbon disulfide ($CS_2$) — highly flammable, toxic | Spontaneous generation of neurotoxic and explosive vapor in vessel headspaces |
| **Section 2: Hazards Identification** | Lower Explosive Limit (LEL) | 1.3 % ($CS_2$ off-gas) | Readily reaches explosive concentrations without adequate room ventilation |
| **Section 4: First Aid Measures** | Inhalation | Remove to fresh air; seek medical attention | Immediate evacuation from $CS_2$ vapor plume; administer oxygen if respiratory distress |
| **Section 4: First Aid Measures** | Eye & Skin Contact | Flush eyes and skin with water for 15 minutes; seek medical attention | Emergency deluge shower / eyewash within 10 seconds in Area 45 |
| **Section 5: Fire Fighting Measures** | Extinguishing Media | Dry chemical, $CO_2$, or foam | Standard extinguishing agents for self-heating and organosulfur solid fires |
| **Section 5: Fire Fighting Measures** | Specific Firefighting Prohibition | Do not use water jet on burning xanthate | Water jets scatter burning pellets and violently generate toxic $CS_2$ vapors |
| **Section 7: Handling & Storage** | Storage Conditions | Store cool and dry, away from acids and ignition sources | Dedicated enclosed ventilated reagent shed; prevent rainwater ingress and acidic contact |
| **Section 7: Handling & Storage** | Container Management | Keep containers closed | Exclude atmospheric moisture and prevent escape of evolved $CS_2$ vapor |
| **Section 8: Exposure Controls & PPE** | Engineering Controls | Local exhaust ventilation | Continuous mechanical extraction fan `FN-4501` operating 24/7 in enclosed mixing room |
| **Section 8: Exposure Controls & PPE** | Eye Protection | Chemical goggles | Splash-proof goggles during dry pellet charging and solution transfer |
| **Section 8: Exposure Controls & PPE** | Hand / Skin Protection | Nitrile gloves | Chemical-resistant nitrile gauntlets preventing dermal absorption |
| **Section 8: Exposure Controls & PPE** | Respiratory Protection | Respirator where exposure limits may be exceeded | Chemical cartridge respirator with organic vapor/particulate filters during hopper loading |

## Cross-Document Reconciliation & Alignment
1. **Reagent Grounding Across Design Basis:**
   - Safety Data Sheet `standards/SDS_2720-73-2_potassium-amyl-xanthate.pdf` grounds the use of PAX in `TK-4501` and `TK-4502`.
   - Process Data Sheet `RB-4410-PS-TK4501 Rev B` specifies batch dissolution of solid PAX to 20% w/v aqueous solution in a 40 m³ 316L vessel, transferring to `TK-4502`.
   - P&ID `RB-4410-PID-45-001 Rev B` specifies `TK-4501` and `TK-4502` in an enclosed room with continuous extraction fan `FN-4501` (Note 1) and dosing governed by `RB-4410-OM-001` (Note 4).
   - Operating Manual `RB-4410-OM-001 Rev 2` (Sec 3.45 & Sec 8) mandates mix water temperature strictly $<40$ °C to prevent thermal decomposition into $CS_2$ (LEL 1.3%, auto-ignition 90 °C) and non-sparking tools.
   - HAZOP Study `RB-4410-STD-HAZOP-001 Rev 1` (Node HZ-45-03) tracks action item `ACT-HAZOP-45-03` to install $CS_2$ gas detector `AT-4501` interlocked to `FN-4501` and feeder stop.
   - *Status:* 100% corroborated across all engineering documents with zero discrepancies.

2. **Self-Heating Solid & Temperature Sensitivity:**
   - The SDS designation of PAX as a "Self-heating solid" reinforces the operating manual requirement that make-up water temperature must never exceed 40 °C. Storage in unventilated bulk containers under solar heating or moisture contamination risks thermal runaway and auto-decomposition.

3. **Firefighting Strategy Integration:**
   - SDS Section 5 mandates "Dry chemical, CO2 or foam. Do not use water jet on burning xanthate."
   - This directive explains why both MIBC SDS (`SDS_108-11-2_mibc.pdf`) and Quicklime SDS (`SDS_1305-78-8_quicklime---hydrated-lime.pdf`) emphasize: *"Do not use water jet on burning xanthate"* due to proximity in Area 45.

## Affected Plant Entities & Cross-References
- **Equipment Concepts:**
  - `equipment/TK-4501` (PAX Xanthate Mixing Tank)
  - `equipment/TK-4502` (PAX Dosing Tank)
  - `equipment/FN-4501` (PAX Mixing Room Extraction Fan)
  - `equipment/PP-4501A` (PAX Dosing Pump)
  - `equipment/TK-4101` (Flotation Conditioning Tank)
  - `equipment/FC-4101` (Rougher Flotation Cells)
- **Hazard Profiles:**
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
[^src-1]: SDS_2720-73-2_potassium-amyl-xanthate.pdf (corpora/copper-concentrator/raw/standards/SDS_2720-73-2_potassium-amyl-xanthate.pdf)
