---
type: Source Document
title: Safety Data Sheet Summary — Polyglycol Ether Frother (DF-250 Type) (CAS 37286-64-9)
description: Safety Data Sheet summary for Polyglycol ether frother (DF-250 type),
  CAS 37286-64-9, defining polypropylene glycol methyl ether, flash point >100 °C,
  eye irritant, alternative reagent status, and discrepancy analysis against TK-4511.
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/sources/sds-37286-64-9-polyglycol-ether-frother.md
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
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T22:11:47Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T22:11:47Z'
- by: process:okf-validation-suite
  at: '2026-09-30T22:11:47Z'
status: stable
entity_metadata:
  first_aid:
    eyes_and_skin: Flush eyes and skin with water for 15 minutes; seek medical attention
    inhalation: Remove to fresh air; seek medical attention
  flash_point_c: '>100'
  conflict_reagent:
    pid_45_001: Polyglycol ether frother (DF-250 type)
    sds_37286_64_9: Alternative frother (not specified for TK-4511)
    om_pds_and_sds_mibc: MIBC (methyl isobutyl carbinol, CAS 108-11-2, flash point
      41 °C)
  handling_storage: Store cool and dry, away from acids and ignition sources; keep
    containers closed
  firefighting_media:
  - Dry chemical
  - CO2
  - Foam
  target_equipment:
  - TK-4511
  - PP-4511A
  - FC-4101
  - FC-4301
  ghs_classification:
  - Combustible
  - Eye irritant
  chemical_name: Polyglycol ether frother (DF-250 type)
  cas_number: 37286-64-9
  document_class: Chemical Safety Data Sheet Summary
  plant_usage: Alternative frother (not specified for TK-4511)
  chemical_formula: Polypropylene glycol methyl ether
  exposure_controls:
  - Local exhaust ventilation
  - Chemical goggles
  - Nitrile gloves
  - Respirator where exposure limits may be exceeded
---

# Safety Data Sheet Summary — Polyglycol Ether Frother (DF-250 Type) (CAS 37286-64-9)

> ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
> - **REAGENT IDENTITY & SPECIFICATION CONFLICT (TK-4511):** This Safety Data Sheet Summary (`standards/SDS_37286-64-9_polyglycol-ether-frother.pdf`) defines **Polyglycol ether frother (DF-250 type)**, CAS No. **37286-64-9**, chemical type **Polypropylene glycol methyl ether**, and explicitly designates its plant use as *"Alternative frother (not specified for TK-4511)"*.
> - ⚠️ **CONFLICT — P&ID SPECIFICATION VS. SDS & PROCESS DESIGN:** Piping & Instrumentation Diagram `RB-4410-PID-45-001 Rev B` labels frother storage tank `TK-4511` with *"Reagent: Polyglycol ether frother (DF-250 type)"*. However, Process Data Sheet `RB-4410-PS-TK4511 Rev B`, Concentrator Operating Manual `RB-4410-OM-001 Rev 2` (Sections 3.45 & 8), and SDS `SDS_108-11-2_mibc.pdf` all specify **MIBC (methyl isobutyl carbinol, CAS 108-11-2)** for `TK-4511`. Furthermore, this document explicitly notes that DF-250 is an alternative frother and is *not specified for TK-4511*, confirming a documentation divergence on P&ID `RB-4410-PID-45-001 Rev B`. HAZOP Study `RB-4410-STD-HAZOP-001 Rev 1` Node HZ-45-06 issued mandatory recommendation `ACT-HAZOP-45-06` to confirm frother identity on P&ID vs data sheet and SDS before operation.
> - **COMBUSTIBILITY & HAZARDOUS AREA CLASSIFICATION:** Polyglycol ether frother (DF-250 type) is classified as **Combustible** with a closed-cup flash point **>100 °C**, in contrast to MIBC which has a flash point of **41 °C** (GHS Flammable Liquid Category 3, requiring Zone 2 electrical equipment per `RB-4410-STD-HAC-001`). If polyglycol ether were substituted for MIBC, the fire hazard would decrease; conversely, if MIBC is charged into equipment designed only for high-flash-point combustible liquids, an unmitigated explosive vapor risk arises.
> - **FIREFIGHTING CAUTION & REAGENT SEGREGATION:** Approved extinguishing media are dry chemical, $CO_2$, or foam. The SDS issues the specific warning: *"Do not use water jet on burning xanthate"*, reinforcing cross-reagent safety in Area 45 where potassium amyl xanthate (PAX, `TK-4501`) is located adjacent to frother storage.

## Document Overview & Engineering Scope
- **Document Title:** Safety Data Sheet Summary - Polyglycol ether frother (DF-250 type)
- **Source File:** `corpora/copper-concentrator/raw/standards/SDS_37286-64-9_polyglycol-ether-frother.pdf`
- **Document Class:** Chemical Safety Data Sheet Summary / Site Standard
- **Chemical Name:** Polyglycol ether frother (DF-250 type) / Polypropylene glycol methyl ether
- **CAS Registry Number:** 37286-64-9
- **Formula / Chemical Type:** Polypropylene glycol methyl ether
- **Target Plant Duty / Service:** Alternative flotation frother (not specified for Frother Storage Tank `TK-4511`, Area 45 - Reagents).
- **Authority Scope:** Site demonstration summary. Supplier SDS governs authoritative design and transport compliance.

## SDS Technical Specifications & Parameters
| SDS Section | Parameter / Topic | Value / Specification | Engineering & Operational Implications |
| :--- | :--- | :--- | :--- |
| **Section 1: Identification** | Product / Chemical Name | Polyglycol ether frother (DF-250 type) | Alternative flotation frother |
| **Section 1: Identification** | Plant Use & Equipment Specification | Alternative frother (not specified for TK-4511) | Explicitly excluded from base design for TK-4511 |
| **Section 1: Identification** | CAS Registry Number | 37286-64-9 | Chemical identifier for polypropylene glycol methyl ether |
| **Section 1: Identification** | Formula / Type | Polypropylene glycol methyl ether | High-molecular-weight glycol ether surfactant |
| **Section 2: Hazards Identification** | Hazard Classification | Combustible; Eye irritant | Lower volatility and higher flash point than aliphatic alcohols |
| **Section 2: Hazards Identification** | Closed-Cup Flash Point | >100 °C | Non-flammable under normal ambient conditions; classified combustible |
| **Section 4: First Aid Measures** | Inhalation | Remove to fresh air; seek medical attention | Transfer affected personnel away from vapor or mist |
| **Section 4: First Aid Measures** | Eye & Skin Contact | Flush eyes and skin with water for 15 minutes; seek medical attention | Immediate decontamination at Area 45 emergency safety shower/eyewash |
| **Section 5: Fire Fighting Measures** | Extinguishing Media | Dry chemical, $CO_2$, or foam | Standard extinguishing agents for combustible liquid fires |
| **Section 5: Fire Fighting Measures** | Specific Hazards / Prohibitions | Do not use water jet on burning xanthate | Area 45 multi-reagent safeguard against scattering burning solid xanthate |
| **Section 7: Handling & Storage** | Storage Conditions | Store cool and dry, away from acids and ignition sources | Maintain container integrity; protect from thermal degradation |
| **Section 7: Handling & Storage** | Container Management | Keep containers closed | Prevent moisture absorption and contamination |
| **Section 8: Exposure Controls & PPE** | Ventilation Controls | Local exhaust ventilation | Maintain airborne vapor/mist below occupational thresholds |
| **Section 8: Exposure Controls & PPE** | Eye Protection | Chemical goggles | Mandatory protection against severe eye irritation and splashes |
| **Section 8: Exposure Controls & PPE** | Hand / Skin Protection | Nitrile gloves | Chemical barrier protecting skin from prolonged glycol ether contact |
| **Section 8: Exposure Controls & PPE** | Respiratory Protection | Respirator where exposure limits may be exceeded | Air-purifying respirator required during confined vessel entry or aerosol exposure |

## Cross-Document Reconciliation & Engineering Discrepancies
1. **P&ID Labeling vs. SDS Scope & Design Data Sheet:**
   - Drawing `RB-4410-PID-45-001 Rev B` specifies: `Reagent: Polyglycol ether frother (DF-250 type)` for `TK-4511`.
   - SDS Summary `standards/SDS_37286-64-9_polyglycol-ether-frother.pdf` explicitly specifies: `Alternative frother (not specified for TK-4511)`.
   - Process Data Sheet `RB-4410-PS-TK4511 Rev B`, Operating Manual `RB-4410-OM-001 Rev 2`, and `SDS_108-11-2_mibc.pdf` specify: `MIBC (methyl isobutyl carbinol, CAS 108-11-2)`.
   - *Engineering Reconciliation:* `SDS_37286-64-9_polyglycol-ether-frother.pdf` confirms that polyglycol ether (DF-250 type) is evaluated solely as an alternative reagent and is *not* specified for baseline installation in `TK-4511`. The P&ID annotation represents an unaligned design artifact. HAZOP recommendation `ACT-HAZOP-45-06` mandates reconciling `RB-4410-PID-45-001` before commissioning.

2. **Thermal & Electrical Area Classification Differences:**
   - Polyglycol ether frother (DF-250 type, CAS 37286-64-9) exhibits a high flash point (>100 °C) and low volatility, classifying it as combustible.
   - MIBC (CAS 108-11-2) has a closed-cup flash point of 41 °C, qualifying as GHS Flammable Liquid Category 3 and mandating Zone 2 hazardous area classification around `TK-4511` per `RB-4410-STD-HAC-001`.
   - Electrical equipment in the `TK-4511` containment bund has been engineered for Zone 2 to accommodate MIBC. Substituting DF-250 is safe from an electrical classification standpoint, but reverting to MIBC in an area designed only for high-flash-point combustible liquid would introduce catastrophic ignition risks.

## Affected Plant Entities & Cross-References
- **Equipment Concepts:**
  - `equipment/TK-4511` (Frother Storage Tank)
  - `equipment/PP-4511A` (Frother Dosing Pump)
  - `equipment/FC-4101` (Rougher Flotation Cells)
  - `equipment/FC-4301` (Cleaner Flotation Column)
- **Hazard Profiles:**
  - `hazards/polyglycol-ether-frother` (Polyglycol Ether Frother DF-250 Chemical Safety & Hazard Profile)
  - `hazards/mibc` (MIBC Chemical Safety & Hazard Profile)
  - `hazards/comminution-slurry-hazards` (Comminution, Classification, Flotation, Tailings & Reagents Process Safety Hazards)
- **HAZOP Studies:**
  - `hazop/concentrator-hazop-study` (Node HZ-45-06, Recommendation ACT-HAZOP-45-06)
- **Unit Overviews:**
  - `units/flotation` (Flotation and Regrind Circuit)
  - `units/copper-concentrator` (Overall Concentrator Plant Overview)

## References & Sources
[^src-1]: SDS_37286-64-9_polyglycol-ether-frother.pdf (corpora/copper-concentrator/raw/standards/SDS_37286-64-9_polyglycol-ether-frother.pdf)
