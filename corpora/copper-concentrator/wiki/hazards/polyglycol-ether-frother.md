---
type: Hazard Profile
title: Polyglycol Ether Frother (DF-250 Type) Chemical Safety & Hazard Profile (CAS
  37286-64-9)
description: Chemical safety data, combustibility hazards, flash point >100 °C, eye
  irritation, storage/handling controls, and discrepancy analysis for polyglycol ether
  frother DF-250 (CAS 37286-64-9).
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/hazards/polyglycol-ether-frother.md
tags:
- area 45
- cas 37286-64-9
- combustible
- conflict
- df-250
- frother
- hazard profile
- polypropylene glycol methyl ether
- process safety
- reagents
- sds
- standards
- tk-4511
sources:
- id: src-1
  resource: corpora/copper-concentrator/raw/standards/SDS_37286-64-9_polyglycol-ether-frother.pdf
  title: SDS_37286-64-9_polyglycol-ether-frother.pdf
- id: src-2
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER
    & LIME_B.pdf
  title: RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf
- id: src-3
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-TK4511_FROTHER STORAGE TANK PROCESS
    DATA SHEET_B.pdf
  title: RB-4410-PS-TK4511_FROTHER STORAGE TANK PROCESS DATA SHEET_B.pdf
- id: src-4
  resource: corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR
    OPERATING MANUAL_R2.pdf
  title: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf
- id: src-5
  resource: corpora/copper-concentrator/raw/standards/RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf
  title: RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T22:12:09Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T22:12:09Z'
- by: process:okf-validation-suite
  at: '2026-09-30T22:12:09Z'
status: stable
entity_metadata:
  chemical_name: Polyglycol ether frother (DF-250 type)
  flash_point_c: '>100'
  first_aid:
    inhalation: Remove to fresh air; seek medical attention
    eyes_and_skin: Flush with water for 15 minutes; seek medical attention
  chemical_family: Polypropylene glycol methyl ether
  alternative_frother: true
  act_hazop_45_06: Confirm frother identity on P&ID vs data sheet and SDS
  handling_storage: Store cool and dry, away from acids and ignition sources; keep
    containers closed
  plant_usage: Alternative frother (not specified for TK-4511)
  exposure_controls:
  - Local exhaust ventilation
  - Chemical goggles
  - Nitrile gloves
  - Respirator where exposure limits may be exceeded
  target_equipment:
  - TK-4511
  - PP-4511A
  - FC-4101
  - FC-4301
  cas_number: 37286-64-9
  firefighting_media:
  - Dry chemical
  - CO2
  - Foam
  ghs_classification:
  - Combustible
  - Eye irritant
  conflict_reagent:
    pid_45_001: Polyglycol ether frother (DF-250 type)
    sds_37286_64_9: Alternative frother (not specified for TK-4511)
    om_and_pds: MIBC (methyl isobutyl carbinol, CAS 108-11-2, flash point 41 °C)
  target_unit: Area 45 - Reagents
---

# Polyglycol Ether Frother (DF-250 Type) Chemical Safety & Hazard Profile (CAS 37286-64-9)

> ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
> - **REAGENT IDENTITY & PLANT SPECIFICATION DISCREPANCY:** Safety Data Sheet Summary `standards/SDS_37286-64-9_polyglycol-ether-frother.pdf` covers **Polyglycol ether frother (DF-250 type)**, CAS No. **37286-64-9**, chemical formula/type **Polypropylene glycol methyl ether**, and specifies its intended plant use explicitly as: *"Alternative frother (not specified for TK-4511)"*.
> - ⚠️ **CONFLICT — P&ID LABELING VS. DESIGN DATA SHEET & SDS:** Piping & Instrumentation Diagram `RB-4410-PID-45-001 Rev B` marks the reagent in Frother Storage Tank `TK-4511` as *"Polyglycol ether frother (DF-250 type)"*. In contrast, Process Data Sheet `RB-4410-PS-TK4511 Rev B`, Concentrator Operating Manual `RB-4410-OM-001 Rev 2` (Sections 3.45 & 8), and SDS `SDS_108-11-2_mibc.pdf` specify **MIBC (methyl isobutyl carbinol, CAS 108-11-2)** as the designated frother reagent. SDS `SDS_37286-64-9_polyglycol-ether-frother.pdf` explicitly records that DF-250 is an alternative frother and is *not specified for TK-4511*. HAZOP Study `RB-4410-STD-HAZOP-001 Rev 1` Node HZ-45-06 issues mandatory recommendation `ACT-HAZOP-45-06` to confirm frother identity across drawings and data sheets.
> - **COMBUSTIBLE LIQUID VS. FLAMMABLE LIQUID CLASSIFICATION:** Polyglycol ether frother DF-250 is a **Combustible** liquid with a closed-cup flash point **>100 °C** and low vapor pressure. By comparison, MIBC has a closed-cup flash point of **41 °C** (GHS Flammable Liquid Category 3), which produces flammable vapor envelopes at ambient summer operating conditions (<35 °C) and mandates Zone 2 electrical equipment per `RB-4410-STD-HAC-001`.
> - **FIREFIGHTING CAUTION & REAGENT SEGREGATION:** Suitable extinguishing media are dry chemical, $CO_2$, or foam. Section 5 of the SDS mandates: *"Do not use water jet on burning xanthate"*, reflecting the co-location of potassium amyl xanthate (`TK-4501`) within the Area 45 reagent storage perimeter.

## Chemical Identification & Physical Properties
| Parameter | Value | Source Citation |
| :--- | :--- | :--- |
| **Chemical Name** | Polyglycol ether frother (DF-250 type) | SDS_37286-64-9_polyglycol-ether-frother.pdf |
| **Chemical Type / Family** | Polypropylene glycol methyl ether | SDS_37286-64-9_polyglycol-ether-frother.pdf |
| **CAS Registry Number** | 37286-64-9 | SDS_37286-64-9_polyglycol-ether-frother.pdf |
| **GHS Hazard Classification** | Combustible; Eye irritant | SDS_37286-64-9_polyglycol-ether-frother.pdf |
| **Closed-Cup Flash Point** | >100 °C | SDS_37286-64-9_polyglycol-ether-frother.pdf |
| **Physical Appearance** | Viscous organic liquid | SDS_37286-64-9_polyglycol-ether-frother.pdf |
| **Plant Service & Scope** | Alternative frother (not specified for TK-4511) | SDS_37286-64-9_polyglycol-ether-frother.pdf |
| **Associated Equipment on P&ID** | Frother Storage Tank `TK-4511` (P&ID label only; ⚠️ CONFLICT) | RB-4410-PID-45-001 Rev B |
| **Design Basis Reagent for TK-4511** | MIBC (flash point 41 °C, Zone 2) | RB-4410-PS-TK4511 Rev B, RB-4410-OM-001 Rev 2 |

## Process Safety Hazards & Failure Modes
| Failure Mode / Hazard Event | Initiating Event | Consequences & Process Severity | Engineered & Procedural Safeguards |
| :--- | :--- | :--- | :--- |
| **Chemical Mismatch & Area Misclassification** | Loading MIBC based on PDS when site mistakenly assumes non-volatile DF-250 frother (⚠️ CONFLICT) | Ignition of flammable MIBC vapors in unrated electrical zones | HAZOP Action ACT-HAZOP-45-06; Zone 2 rated electrical equipment installed around TK-4511 bund per RB-4410-STD-HAC-001 |
| **Eye Irritation & Splash Hazard** | Hose coupling failure, sampling splash, or tank overfilling during offloading | Severe corneal irritation and pain | Chemical goggles, face shield, and nitrile gloves; safety shower and eyewash within 10 s |
| **Thermal Decomposition / Combustion** | Exposure of bulk storage containers to extreme external heat or open flames (>100 °C) | Combustible liquid fire emitting irritating smoke | Dry chemical, CO2, or foam extinguishers; cool containers with water spray from protected location |
| **Multi-Reagent Firefighting Conflict** | Directing water jets toward burning xanthate during reagent storage fire | Scatter of burning chemical; rapid decomposition into toxic, flammable CS2 gas | Strict firefighting rule: Do not use water jet on burning xanthate in Area 45 |
| **Loss of Flotation Selectivity** | Uncontrolled substitution between MIBC and polyglycol frothers without circuit retuning | Change in bubble size distribution, froth stability, and Cu concentrate recovery | Flotation process control via AIC-4101 and manual dosing trim from PP-4511A |

## Emergency Response & First Aid Measures
- **Inhalation:** Immediately remove casualty to fresh air. If irritation or respiratory discomfort develops, obtain medical evaluation.
- **Eye Contact:** Immediately flush eyes with clean running water for at least 15 minutes, holding eyelids wide apart. Remove contact lenses if present. Seek prompt medical attention.
- **Skin Contact:** Wash contaminated areas thoroughly with soap and running water for 15 minutes. Remove and wash contaminated clothing before reuse. If irritation persists, seek medical evaluation.
- **Ingestion:** Rinse mouth thoroughly with water. Do NOT induce vomiting unless directed by medical personnel. Obtain prompt medical advice.
- **Firefighting Protocol:**
  - Approved Agents: Dry chemical, carbon dioxide ($CO_2$), or foam.
  - Critical Multi-Reagent Directive: **Do not use water jet on burning xanthate** located in the adjacent Area 45 storage area (`TK-4501`), as this will cause violent spattering and accelerate toxic carbon disulfide ($CS_2$) formation.

## Safe Handling, Storage & Exposure Controls
- **Engineering Controls:** Provide continuous local exhaust ventilation in chemical handling and pumping areas. Keep tank and transfer line connections tightly sealed.
- **Storage Conditions:** Store in cool, dry, well-ventilated areas away from strong acids and potential ignition sources. Keep drums or storage containers closed when not in use.
- **Personal Protective Equipment (PPE):**
  - **Eye/Face Protection:** Chemical splash goggles; full face shield during transfer, sampling, or hose make/break operations.
  - **Hand/Skin Protection:** Nitrile rubber chemical-resistant gloves; protective chemical apron and safety boots.
  - **Respiratory Protection:** Approved respirator equipped with organic vapor/particulate filters where misting or exposure limits may be exceeded.

## Cross-Document Conflict & Resolution Register
| Parameter / Item | SDS_37286-64-9_polyglycol-ether-frother.pdf | RB-4410-PID-45-001 Rev B | RB-4410-PS-TK4511 Rev B / RB-4410-OM-001 Rev 2 | Reconciliation Status |
| :--- | :--- | :--- | :--- | :--- |
| **Chemical Identification** | Polyglycol ether frother (DF-250 type), CAS 37286-64-9 | Polyglycol ether frother (DF-250 type) | MIBC (methyl isobutyl carbinol, CAS 108-11-2) | ⚠️ CONFLICT: P&ID labels TK-4511 with DF-250; PDS and OM-001 specify MIBC. SDS explicitly confirms DF-250 is an alternative frother not specified for TK-4511. |
| **Flash Point** | >100 °C | Not specified | 41 °C | MIBC is flammable (Zone 2 required); DF-250 is combustible. |
| **Plant Status for TK-4511** | Alternative frother (not specified for TK-4511) | Primary vessel label | Baseline design reagent | SDS confirms DF-250 is not specified for baseline TK-4511. P&ID annotation requires correction per ACT-HAZOP-45-06. |

## References & Sources
[^src-1]: SDS_37286-64-9_polyglycol-ether-frother.pdf (corpora/copper-concentrator/raw/standards/SDS_37286-64-9_polyglycol-ether-frother.pdf)
[^src-2]: RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf (corpora/copper-concentrator/raw/pid/RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf)
[^src-3]: RB-4410-PS-TK4511_FROTHER STORAGE TANK PROCESS DATA SHEET_B.pdf (corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-TK4511_FROTHER STORAGE TANK PROCESS DATA SHEET_B.pdf)
[^src-4]: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf (corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf)
[^src-5]: RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf (corpora/copper-concentrator/raw/standards/RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf)
