---
type: Source Document
title: Safety Data Sheet Summary — MIBC (Methyl Isobutyl Carbinol) (CAS 108-11-2)
description: Safety Data Sheet summary for MIBC (methyl isobutyl carbinol) frother
  reagent used in TK-4511, defining CAS 108-11-2, flammability Cat 3, flash point
  41 °C, STOT SE 3, and cross-document discrepancy analysis.
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/sources/sds-108-11-2-mibc.md
tags:
- area 45
- cas 108-11-2
- conflict
- flammable liquid
- frother
- hazard profile
- mibc
- process safety
- reagents
- sds
- standards
- tk-4511
sources:
- id: src-1
  resource: corpora/copper-concentrator/raw/standards/SDS_108-11-2_mibc.pdf
  title: SDS_108-11-2_mibc.pdf
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T18:28:40Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T18:28:40Z'
- by: process:okf-validation-suite
  at: '2026-09-30T18:28:40Z'
status: stable
entity_metadata:
  firefighting_media:
  - Dry chemical
  - CO2
  - Foam
  plant_usage: Frother reagent in TK-4511
  flash_point_c: 41
  ghs_classification:
  - Flammable liquid Cat 3
  - STOT SE 3
  conflict_reagent:
    pid_45_001: Polyglycol ether frother (DF-250 type)
    pds_and_sds: MIBC (methyl isobutyl carbinol)
  chemical_name: MIBC (methyl isobutyl carbinol)
  exposure_controls:
  - Local exhaust ventilation
  - Chemical goggles
  - Nitrile gloves
  - Organic vapor respirator where limits exceeded
  document_class: Chemical Safety Data Sheet Summary
  cas_number: 108-11-2
  first_aid:
    eyes_and_skin: Flush with water for 15 minutes; seek medical attention
    inhalation: Remove to fresh air; seek medical attention
  target_equipment:
  - TK-4511
  - PP-4511A
  - FC-4101
  - FC-4301
  chemical_formula: C6H14O
  handling_storage: Store cool and dry, away from acids and ignition sources; keep
    containers closed
---

# Safety Data Sheet Summary — MIBC (Methyl Isobutyl Carbinol) (CAS 108-11-2)

> ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
> - **REAGENT IDENTITY & HAZARDOUS AREA RECONCILIATION (TK-4511):** SDS Summary `SDS_108-11-2_mibc.pdf` explicitly identifies the chemical reagent used in frother storage tank `TK-4511` as **MIBC (methyl isobutyl carbinol)**, CAS No. **108-11-2**, chemical formula **$C_6H_{14}O$**, classified as **Flammable liquid Category 3** with a closed-cup flash point of **41 °C** and **STOT SE 3** (Specific Target Organ Toxicity — Single Exposure Category 3). This corroborates Process Data Sheet `RB-4410-PS-TK4511 Rev B`, Concentrator Operating Manual `RB-4410-OM-001 Rev 2` (Sections 3.45 & 8), and HAZOP Study `RB-4410-STD-HAZOP-001 Rev 1` (Node HZ-45-06).
> - ⚠️ **CONFLICT — REAGENT CHEMISTRY & HAZARDOUS AREA CLASSIFICATION:** Piping & Instrumentation Diagram `RB-4410-PID-45-001 Rev B` explicitly marks the reagent for `TK-4511` as **Polyglycol ether frother (DF-250 type)** with general area classification per `RB-4410-STD-HAC-001`. Polyglycol ethers (DF-250) are high-molecular-weight glycol liquids with flash points >100 °C. Storing MIBC (flash point 41 °C, Category 3 flammable liquid) creates flammable vapor spaces and requires Zone 2 certified electrical equipment, tank breather flame arrestors, and strict tanker bonding. HAZOP Node HZ-45-06 issues mandatory recommendation `ACT-HAZOP-45-06` to confirm frother identity on P&ID vs data sheet and SDS.
> - **FIREFIGHTING EXTINGUISHING MEDIA:** Use dry chemical, $CO_2$, or foam. Note that the document summary contains the instruction *"Do not use water jet on burning xanthate"*, highlighting cross-reagent safety protocols in Area 45 where potassium amyl xanthate (PAX) is stored and handled in adjacent tankage (`TK-4501`).

## Document Overview & Engineering Scope
- **Document Title:** Safety Data Sheet Summary - MIBC (methyl isobutyl carbinol)
- **Source File:** `corpora/copper-concentrator/raw/standards/SDS_108-11-2_mibc.pdf`
- **Document Class:** Chemical Safety Data Sheet Summary / Site Standard
- **Chemical Name:** MIBC (methyl isobutyl carbinol) / 4-Methyl-2-pentanol
- **CAS Registry Number:** 108-11-2
- **Chemical Formula:** $C_6H_{14}O$
- **Target Plant Duty / Service:** Frother reagent bulk storage in `TK-4511` (Area 45 - Reagents), dosing flotation rougher cells `FC-4101` and cleaner column `FC-4301`.
- **Authority Scope:** Site demonstration summary. Supplier SDS governs authoritative design and transport compliance.

## SDS Technical Specifications & Parameters
| SDS Section | Parameter / Topic | Value / Specification | Engineering & Operational Implications |
| :--- | :--- | :--- | :--- |
| **Section 1: Identification** | Product / Chemical Name | MIBC (methyl isobutyl carbinol) | Primary aliphatic alcohol flotation frother |
| **Section 1: Identification** | Plant Use & Equipment Tag | `TK-4511`, frother | Stored in 30 m³ atmospheric vertical tank TK-4511 |
| **Section 1: Identification** | CAS Number | 108-11-2 | Unique global chemical identifier |
| **Section 1: Identification** | Chemical Formula / Type | $C_6H_{14}O$ | Low-molecular-weight branched hexyl alcohol |
| **Section 2: Hazards Identification** | GHS Flammability Category | Flammable liquid Cat 3 | Requires Zone 2 hazardous area classification |
| **Section 2: Hazards Identification** | Closed-Cup Flash Point | 41 °C | Flammable vapor develops under direct summer sun/ambient |
| **Section 2: Hazards Identification** | Target Organ Toxicity | STOT SE 3 | Respiratory tract irritation and CNS depression (narcotic effects) |
| **Section 4: First Aid Measures** | Inhalation | Remove to fresh air; seek medical attention | Relocate victim from vapor plume; administer oxygen if needed |
| **Section 4: First Aid Measures** | Eye & Skin Contact | Flush eyes and skin with water for 15 minutes; seek medical attention | Immediate eyewash/deluge shower actuation in Area 45 |
| **Section 5: Fire Fighting Measures** | Extinguishing Media | Dry chemical, $CO_2$, or foam | Standard flammable liquid firefighting agents |
| **Section 5: Fire Fighting Measures** | Specific Hazards / Prohibitions | Do not use water jet on burning xanthate | Area 45 segregation warning; water jet on xanthate spreads molten/toxic mass |
| **Section 7: Handling & Storage** | Storage Conditions | Store cool and dry, away from acids and ignition sources | Bunded shaded storage, strict elimination of open flames/hot work |
| **Section 7: Handling & Storage** | Container Management | Keep containers closed | Prevent vapor escape and evaporative concentration loss |
| **Section 8: Exposure Controls & PPE** | Ventilation Controls | Local exhaust ventilation | Enclosed ventilation or open-air naturally ventilated bunds |
| **Section 8: Exposure Controls & PPE** | Eye Protection | Chemical goggles | Mandatory eye protection against splash/vapor irritation |
| **Section 8: Exposure Controls & PPE** | Hand / Skin Protection | Nitrile gloves | Chemical-resistant barrier against aliphatic alcohol dermal penetration |
| **Section 8: Exposure Controls & PPE** | Respiratory Protection | Respirator where exposure limits may be exceeded | Organic vapor cartridge respirator for confined space or tank top entry |

## Cross-Document Reconciliation & Engineering Discrepancies
1. **Reagent Chemistry Conflict (MIBC vs DF-250 Polyglycol Ether):**
   - SDS `standards/SDS_108-11-2_mibc.pdf` specifies: **MIBC (methyl isobutyl carbinol)**, CAS 108-11-2, for `TK-4511`.
   - Process Data Sheet `RB-4410-PS-TK4511 Rev B` specifies: **MIBC (methyl isobutyl carbinol)**, flash point 41 °C, Zone 2.
   - Operating Manual `RB-4410-OM-001 Rev 2` (Sec 3.45 & 8) specifies: **MIBC (methyl isobutyl carbinol)**, flash point 41 °C, Zone 2.
   - HAZOP Study `RB-4410-STD-HAZOP-001 Rev 1` (Node HZ-45-06) evaluates: **MIBC frother specification** and issues recommendation `ACT-HAZOP-45-06`.
   - Piping & Instrumentation Diagram `RB-4410-PID-45-001 Rev B` specifies: **Polyglycol ether frother (DF-250 type)**.
   - *Resolution Action:* Update P&ID `RB-4410-PID-45-001` to reflect MIBC and verify that the electrical apparatus installed in the `TK-4511` bund satisfies Zone 2 hazardous area classification per `RB-4410-STD-HAC-001`.

2. **Electrical Hazardous Area Classification:**
   - MIBC has a flash point of 41 °C (Flammable Liquid Cat 3). In ambient conditions exceeding 30–35 °C or under solar heating, the vapor space inside `TK-4511` is within the flammable range (LEL ~1.0% to UEL ~5.5%).
   - Tank `TK-4511` breather vent must be equipped with an approved flame arrestor, and electrical equipment within the bund must be certified ATEX / IECEx Zone 2 (Group IIA, Temperature Class T3 minimum).

3. **Multi-Reagent Segregation in Area 45:**
   - Section 5 explicitly references xanthate ("Do not use water jet on burning xanthate").
   - Potassium amyl xanthate (`TK-4501`) decomposes into $CS_2$ (carbon disulfide, auto-ignition temperature 90 °C). Acids catalyze this decomposition. MIBC must be stored away from strong acids and separate from oxidizers.

## Affected Plant Entities & Cross-References
- **Equipment Concepts:**
  - `equipment/TK-4511` (Frother Storage Tank)
  - `equipment/PP-4511A` (Frother Dosing Pump)
  - `equipment/FC-4101` (Rougher Flotation Cells)
  - `equipment/FC-4301` (Cleaner Flotation Column)
- **Hazard Profiles:**
  - `hazards/mibc` (MIBC Chemical Safety & Hazard Profile)
  - `hazards/comminution-slurry-hazards` (Comminution, Classification, Flotation, Tailings & Reagents Process Safety Hazards)
- **HAZOP Studies:**
  - `hazop/concentrator-hazop-study` (Node HZ-45-06)
- **Unit Overviews:**
  - `units/flotation` (Flotation and Regrind Circuit)
  - `units/copper-concentrator` (Overall Concentrator Plant Overview)

## References & Sources
[^src-1]: SDS_108-11-2_mibc.pdf (corpora/copper-concentrator/raw/standards/SDS_108-11-2_mibc.pdf)
