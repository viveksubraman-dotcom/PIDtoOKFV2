---
type: Hazard Profile
title: MIBC (Methyl Isobutyl Carbinol) Chemical Safety & Hazard Profile (CAS 108-11-2)
description: Chemical safety data, flammability hazards, flash point 41 °C, STOT SE
  3 toxicity, storage/handling controls, and discrepancy analysis for methyl isobutyl
  carbinol frother in TK-4511.
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/hazards/mibc.md
tags:
- area 45
- cas 108-11-2
- cas 37286-64-9
- conflict
- flammable liquid
- frother
- hazard profile
- hazop
- mibc
- process safety
- reagents
- sds
- stot se 3
- tk-4511
- zone 2
sources:
- id: src-1
  resource: corpora/copper-concentrator/raw/standards/SDS_108-11-2_mibc.pdf
  title: SDS_108-11-2_mibc.pdf
- id: src-2
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-TK4511_FROTHER STORAGE TANK PROCESS
    DATA SHEET_B.pdf
  title: RB-4410-PS-TK4511_FROTHER STORAGE TANK PROCESS DATA SHEET_B.pdf
- id: src-3
  resource: corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR
    OPERATING MANUAL_R2.pdf
  title: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf
- id: src-4
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER
    & LIME_B.pdf
  title: RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf
- id: src-5
  resource: corpora/copper-concentrator/raw/standards/RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf
  title: RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf
- id: src-6
  resource: corpora/copper-concentrator/raw/standards/SDS_37286-64-9_polyglycol-ether-frother.pdf
  title: SDS_37286-64-9_polyglycol-ether-frother.pdf
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T22:12:32Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T22:12:32Z'
- by: process:okf-validation-suite
  at: '2026-09-30T22:12:32Z'
status: stable
entity_metadata:
  storage_class: Zone 2 flammable liquid
  first_aid:
    inhalation: Remove to fresh air; seek medical attention
    eyes_and_skin: Flush with water for 15 minutes; seek medical attention
  conflict_reagent:
    om_pds_and_sds_mibc: MIBC (methyl isobutyl carbinol, flash point 41 °C)
    sds_37286_64_9: Alternative frother (not specified for TK-4511, flash point >100
      °C)
    pid_45_001: Polyglycol ether frother (DF-250 type)
  chemical_name: Methyl isobutyl carbinol (MIBC)
  ppe:
  - Chemical goggles
  - Nitrile gloves
  - Organic vapor respirator
  flash_point_c: 41
  chemical_formula: C6H14O
  ghs_classification:
  - Flammable liquid Cat 3
  - STOT SE 3
  hazop_node: HZ-45-06
  cas_number: 108-11-2
  target_unit: Area 45 - Reagents
  act_hazop_45_06: Confirm frother identity on P&ID vs data sheet and SDS
  target_equipment:
  - TK-4511
  - PP-4511A
  - FC-4101
  - FC-4301
---

# MIBC (Methyl Isobutyl Carbinol) Chemical Safety & Hazard Profile (CAS 108-11-2)

> ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
> - **FLAMMABLE LIQUID CATEGORY 3 (FLASH POINT 41 °C):** MIBC is a flammable liquid (GHS Flammable Liquid Category 3) with a closed-cup flash point of **41 °C**. In warm ambient climates or under solar heating of tank `TK-4511`, liquid temperatures approach or exceed the flash point, establishing an explosive vapor-air mixture in the vessel ullage space. Area 45 electrical equipment must comply with Zone 2 hazardous area classification.
> - ⚠️ **CONFLICT — REAGENT CHEMISTRY & HAZARDOUS AREA CLASSIFICATION (TK-4511):** Drawing `RB-4410-PID-45-001 Rev B` specifies Reagent: **Polyglycol ether frother (DF-250 type)** with Note 2 referencing general area classification per `RB-4410-STD-HAC-001`. In sharp contrast, Safety Data Sheet Summary `standards/SDS_108-11-2_mibc.pdf`, Process Data Sheet `RB-4410-PS-TK4511 Rev B`, and Concentrator Operating Manual `RB-4410-OM-001 Rev 2` (Sections 3.45 & 8) specify Reagent Stored: **MIBC (methyl isobutyl carbinol)**, an aliphatic alcohol with a flash point of 41 °C classified as Class 3 flammable liquid requiring **Zone 2** electrical equipment. Polyglycol ethers (DF-250 type, CAS 37286-64-9 per `standards/SDS_37286-64-9_polyglycol-ether-frother.pdf`) are non-volatile polyglycol liquids with high flash points (>100 °C) and negligible vapor pressure, explicitly documented as an *"Alternative frother (not specified for TK-4511)"*, confirming that the P&ID text is an unaligned drawing note.
> - **HAZOP STUDY ACTION ITEM ACT-HAZOP-45-06 (NODE HZ-45-06):** In HAZOP Study `RB-4410-STD-HAZOP-001 Rev 1` Node HZ-45-06 ("Other than (wrong reagent)"), the team identified that changing frother specification invalidates the hazardous area classification. The safeguard is: *"Area classified Zone 2 for MIBC"*. Mandatory HAZOP recommendation `ACT-HAZOP-45-06` mandates: *"Confirm frother identity on P&ID vs data sheet and SDS"*.
> - **STOT SE 3 (SPECIFIC TARGET ORGAN TOXICITY - SINGLE EXPOSURE):** Vapors irritate respiratory passages and mucous membranes, causing dizziness, headaches, and narcotic central nervous system (CNS) depression. Continuous ventilation and PPE compliance are mandatory during tanker offloading and tank maintenance.
> - **FIREFIGHTING EXTINGUISHING MEDIA:** Use dry chemical, $CO_2$, or alcohol-resistant foam. Note: Reagent summary cautions *"Do not use water jet on burning xanthate"*, indicating that water jets applied to adjacent xanthate storage (`TK-4501`) will cause violent dispersion and toxic $CS_2$ combustion.
> - ⚠️ **CONFLICT — REAGENT CHEMISTRY & HAZARDOUS AREA CLASSIFICATION (TK-4511):** Drawing `RB-4410-PID-45-001 Rev B` specifies Reagent: **Polyglycol ether frother (DF-250 type)** with Note 2 referencing general area classification per `RB-4410-STD-HAC-001`. In sharp contrast, Safety Data Sheet Summary `standards/SDS_108-11-2_mibc.pdf`, Process Data Sheet `RB-4410-PS-TK4511 Rev B`, and Concentrator Operating Manual `RB-4410-OM-001 Rev 2` (Sections 3.45 & 8) specify Reagent Stored: **MIBC (methyl isobutyl carbinol)**, an aliphatic alcohol with a flash point of 41 °C classified as Class 3 flammable liquid requiring **Zone 2** electrical equipment. Polyglycol ethers (DF-250 type) are non-volatile polyglycol liquids with high flash points (>100 °C) and negligible vapor pressure, whereas MIBC readily generates flammable vapors.

## Chemical Identification & Physical Properties
| Parameter | Value | Source Citation |
| :--- | :--- | :--- |
| **Chemical Name** | Methyl isobutyl carbinol (MIBC) / 4-Methylpentan-2-ol | SDS_108-11-2_mibc.pdf, RB-4410-PS-TK4511 Rev B |
| **Synonyms** | 4-Methyl-2-pentanol, Isobutyl methyl carbinol, Methyl amyl alcohol | SDS_108-11-2_mibc.pdf |
| **CAS Registry Number** | 108-11-2 | SDS_108-11-2_mibc.pdf |
| **Chemical Formula** | $C_6H_{14}O$ / $(CH_3)_2CHCH_2CH(OH)CH_3$ | SDS_108-11-2_mibc.pdf, RB-4410-PFD-002 Rev B |
| **Molecular Weight** | 102.17 g/mol | Chemical standard |
| **Physical State / Appearance** | Clear, colorless liquid with mild aliphatic odor | RB-4410-PS-TK4511 Rev B |
| **Closed-Cup Flash Point** | 41 °C | SDS_108-11-2_mibc.pdf, RB-4410-PS-TK4511 Rev B, RB-4410-OM-001 Rev 2 |
| **GHS Flammability Class** | Flammable liquid Category 3 | SDS_108-11-2_mibc.pdf |
| **Health Hazard Rating** | STOT SE 3 (Respiratory tract irritation, narcotic effects) | SDS_108-11-2_mibc.pdf |
| **Target Plant Equipment** | `TK-4511` (Frother Storage Tank, 30 m³ vertical tank) | SDS_108-11-2_mibc.pdf, RB-4410-PS-TK4511 Rev B |
| **Dosing Service & Destination** | Rougher cells `FC-4101` and Cleaner Column `FC-4301` via pump `PP-4511A` | RB-4410-PID-45-001 Rev B, RB-4410-OM-001 Rev 2 |
| **Nominal Dosing Rate** | 20 g/t dry ore (53.8 kg/h at 2,688 t/h ore feed) | RB-4410-PFD-002 Rev B, RB-4410-OM-001 Rev 2 |

## Process Safety Hazards & Failure Modes
| Failure Mode / Hazard Event | Initiating Event | Consequences & Process Severity | Engineered & Procedural Safeguards |
| :--- | :--- | :--- | :--- |
| **Vapor Ignition & Tank Explosion** | Hot work near tank ullage, lightning strike, or ungrounded tanker discharge (FP 41 °C) | Flash fire, tank structural failure, personnel severe burns | Zone 2 certified electrical equipment; tank breather flame arrestor; mandatory tanker grounding/bonding interlock; hot work permit system |
| **Reagent Mismatch & Unrated Equipment** | Procuring/loading MIBC when P&ID specifies polyglycol ether (DF-250) (⚠️ CONFLICT) | Electrical apparatus in bund not rated for Class 3 flammable vapor, resulting in spark ignition | Reconcile P&ID RB-4410-PID-45-001 with SDS and PS-TK4511 per HAZOP recommendation ACT-HAZOP-45-06; Zone 2 bund certification |
| **Vapor Exposure & CNS Depression** | Breather vent discharge into walkway or offloading hose leak | Respiratory irritation, dizziness, operator unconsciousness | Atmospheric breather vent discharge oriented away from walkways; local exhaust ventilation; organic vapor respirators |
| **Secondary Xanthate Fire Escalation** | Water jet applied to burning xanthate in adjacent Area 45 bund during MIBC emergency | Violent splashing of burning xanthate, massive toxic $CS_2$ evolution | Strict firefighting directive: Do not use water jet on burning xanthate; use dry chemical, $CO_2$, or alcohol foam |
| **Tank Overflow & Environmental Spill** | Tanker unloading overfill without monitoring LI-4511 | 30 m³ flammable liquid spill into bund, vapor cloud generation | 110% capacity concrete containment bund per P&ID Note 2; tank level indicator LI-4511; tanker overfill prevention probe |

## Emergency Response & First Aid Measures
- **Inhalation:** Immediately remove casualty from the contaminated vapor plume to fresh air. If breathing is difficult, administer oxygen by qualified personnel. Seek immediate medical attention.
- **Eye Contact:** Immediately flush eyes with copious clean water for at least 15 minutes, holding eyelids apart. Remove contact lenses if present and easy to do. Seek immediate ophthalmological/medical attention.
- **Skin Contact:** Promptly wash contaminated skin with copious running water and non-abrasive soap for 15 minutes. Remove and decontaminate all soaked clothing and footwear before reuse. If irritation persists, seek medical evaluation.
- **Ingestion:** Do NOT induce vomiting without medical instruction. Rinse mouth thoroughly with water and seek urgent medical treatment.
- **Firefighting Strategy:**
  - Extinguishing Media: Dry chemical powder, carbon dioxide ($CO_2$), or alcohol-resistant foam.
  - Critical Fire Caution: **Do not use high-pressure water jets on burning xanthate** located in the adjacent Area 45 reagent facility, as this spreads burning liquid/powder and accelerates hazardous $CS_2$ formation. Cool un-ignited tanks with water fog/spray from a protected distance.

## Safe Handling, Storage & Occupational Exposure Controls
- **Engineering Controls:**
  - Provide continuous local exhaust ventilation or ensure storage is in an open-air, naturally ventilated bunded facility.
  - Equip storage tank `TK-4511` with an approved pressure/vacuum breather valve fitted with an explosion-proof flame arrestor.
  - Maintain verified electrical continuity and bonding jumpers between the delivery road tanker, unloading pump `PP-4511A`, and tank `TK-4511` during all transfers to dissipate electrostatic charge.
- **Safe Handling Practices:**
  - Keep containers tightly closed when not in use.
  - Prohibit all open flames, smoking, and non-certified electrical equipment within the Zone 2 hazardous perimeter (governed by `RB-4410-STD-HAC-001`).
  - Store cool and dry, strictly segregated from strong oxidizing agents, strong acids, and direct thermal/ignition sources.
- **Personal Protective Equipment (PPE):**
  - **Eyes/Face:** Chemical splash goggles and full face shield during sampling or hose connection.
  - **Hands/Skin:** Nitrile rubber chemical-resistant gloves; chemical-resistant apron and boots for transfer operations.
  - **Respiratory:** Half-mask or full-face air-purifying respirator equipped with organic vapor (OV) cartridges where atmospheric monitoring indicates exposure limits may be exceeded or during confined space entry.

## Cross-Document Conflict Register
| Topic / Parameter | SDS_108-11-2_mibc.pdf | RB-4410-PS-TK4511 Rev B | RB-4410-OM-001 Rev 2 | RB-4410-PID-45-001 Rev B | SDS_37286-64-9_polyglycol-ether-frother.pdf | Reconciled Status |
| --- | --- | --- | --- | --- | --- | --- |
| **Reagent Chemical Identity** | MIBC (methyl isobutyl carbinol), CAS 108-11-2 | MIBC (methyl isobutyl carbinol) | MIBC (methyl isobutyl carbinol) | Polyglycol ether frother (DF-250 type) | Polyglycol ether frother (DF-250 type, CAS 37286-64-9); Alternative frother (not specified for TK-4511) | ⚠️ CONFLICT: 3 documents specify MIBC; P&ID specifies DF-250. SDS for DF-250 confirms it is an alternative frother *not specified for TK-4511*. HAZOP recommendation ACT-HAZOP-45-06 mandates formal confirmation. |
| **Closed-Cup Flash Point** | 41 °C | 41 °C | 41 °C | Not specified (>100 °C typical for glycol ethers) | >100 °C (combustible) | Corroborated at 41 °C for MIBC; DF-250 is >100 °C. |
| **Hazardous Area Classification** | Flammable liquid Cat 3 | Zone 2 | Zone 2 | Note 2 per RB-4410-STD-HAC-001 | Non-hazardous / combustible | Zone 2 mandatory if MIBC is stored. |

## References & Sources
[^src-1]: SDS_108-11-2_mibc.pdf (corpora/copper-concentrator/raw/standards/SDS_108-11-2_mibc.pdf)
[^src-2]: RB-4410-PS-TK4511_FROTHER STORAGE TANK PROCESS DATA SHEET_B.pdf (corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-TK4511_FROTHER STORAGE TANK PROCESS DATA SHEET_B.pdf)
[^src-3]: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf (corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf)
[^src-4]: RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf (corpora/copper-concentrator/raw/pid/RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf)
[^src-5]: RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf (corpora/copper-concentrator/raw/standards/RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf)
[^src-6]: SDS_37286-64-9_polyglycol-ether-frother.pdf (corpora/copper-concentrator/raw/standards/SDS_37286-64-9_polyglycol-ether-frother.pdf)
