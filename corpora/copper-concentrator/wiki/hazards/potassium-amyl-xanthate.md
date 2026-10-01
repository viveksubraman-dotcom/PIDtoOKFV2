---
type: Hazard Profile
title: Potassium Amyl Xanthate (PAX) Chemical Safety & Hazard Profile (CAS 2720-73-2)
description: Chemical safety profile, self-heating solid hazards, spontaneous CS2
  evolution, LEL 1.3%, handling and storage safeguards, firefighting protocols, and
  cross-document reconciliation for potassium amyl xanthate in Area 45.
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/hazards/potassium-amyl-xanthate.md
tags:
- area 45
- cas 2720-73-2
- cas 75-15-0
- collector
- cs2
- cs2-evolution
- firefighting
- first-aid
- flotation
- hazard profile
- hazards
- hazop
- hz-45-03
- pax
- potassium-amyl-xanthate
- process-safety
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
- id: src-2
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-TK4501_PAX XANTHATE MIXING TANK PROCESS
    DATA SHEET_B.pdf
  title: RB-4410-PS-TK4501_PAX XANTHATE MIXING TANK PROCESS DATA SHEET_B.pdf
- id: src-3
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER
    & LIME_B.pdf
  title: RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf
- id: src-4
  resource: corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR
    OPERATING MANUAL_R2.pdf
  title: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf
- id: src-5
  resource: corpora/copper-concentrator/raw/standards/RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf
  title: RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf
- id: src-6
  resource: corpora/copper-concentrator/raw/standards/SDS_75-15-0_carbon-disulfide.pdf
  title: SDS_75-15-0_carbon-disulfide.pdf
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T22:17:48Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T22:17:48Z'
- by: process:okf-validation-suite
  at: '2026-09-30T22:17:48Z'
status: stable
entity_metadata:
  hazop_node: HZ-45-03
  cas_number: 2720-73-2
  target_equipment:
  - TK-4501
  - TK-4502
  - FN-4501
  - PP-4501A
  - TK-4101
  - FC-4101
  ghs_classification:
  - Self-heating solid
  - Acute toxicity
  - Eye/skin irritant
  chemical_formula: C6H11KOS2
  ppe:
  - Chemical splash goggles
  - Nitrile gauntlet gloves
  - Respirator where limits exceeded
  storage_class: Self-heating solid / dry cool storage
  firefighting_prohibition: Do not use water jet on burning xanthate
  act_hazop_45_03: Install CS2 gas detector AT-4501 (alarm 10 % LEL) interlocked to
    FN-4501 high speed and PAX feeder stop
  first_aid:
    eyes_and_skin: Flush eyes and skin with water for 15 minutes; seek medical attention
    inhalation: Remove to fresh air; seek medical attention
  cs2_lel_pct: 1.3
  max_makeup_water_temp_c: 40
  target_unit: Area 45 - Reagents
  cs2_autoignition_c: 90
  firefighting_media:
  - Dry chemical
  - CO2
  - Foam
  chemical_name: Potassium amyl xanthate (PAX)
  cs2_twa_ppm: 1
  cs2_flash_point_c: -30
  cs2_cas: 75-15-0
---

# Potassium Amyl Xanthate (PAX) Chemical Safety & Hazard Profile (CAS 2720-73-2)

> ⚠️ **CRITICAL PROCESS SAFETY / DECOMPOSITION HAZARD WARNING:**
> - **SELF-HEATING SOLID & SPONTANEOUS TOXIC/EXPLOSIVE DECOMPOSITION:** Solid potassium amyl xanthate (PAX, CAS 2720-73-2, chemical formula $C_6H_{11}KOS_2$) is classified as a **Self-heating solid** under GHS. Bulk dry pellets stored in drums or hoppers are subject to internal self-heating if exposed to dampness or elevated temperatures.
> - **CARBON DISULFIDE ($CS_2$) EVOLUTION UPON HYDROLYSIS:** In the presence of moisture, acidic conditions, or make-up water exceeding **40 °C**, PAX undergoes rapid exothermic decomposition to release **carbon disulfide ($CS_2$, CAS 75-15-0)** and carbon oxysulfide ($COS$). Carbon disulfide is an acute neurotoxin (IDLH 500 ppm, ACGIH 8-hour TWA 1 ppm with Skin notation) with a wide flammability range, a Lower Explosive Limit (LEL) of **1.3 %**, a flash point of **-30 °C**, and an extremely low auto-ignition temperature of **90 °C** (which can be ignited by unlagged steam/hot water lines or mechanical friction) per `SDS_75-15-0_carbon-disulfide.pdf`.
> - **CONTINUOUS MECHANICAL VENTILATION MANDATE (FN-4501):** Note 1 of P&ID `RB-4410-PID-45-001 Rev B` and Concentrator Operating Manual `RB-4410-OM-001 Rev 2` mandate that mechanical extraction fan `FN-4501` must operate continuously 24/7 whenever PAX is present in the enclosed reagent mixing room housing `TK-4501` and `TK-4502`. Loss of ventilation triggers an immediate DCS alarm and prohibits operator room entry.
> - **HAZOP RECOMMENDATION ACT-HAZOP-45-03 (NODE HZ-45-03):** HAZOP Study `RB-4410-STD-HAZOP-001 Rev 1` Node HZ-45-03 evaluates xanthate decomposition and issues mandatory recommendation `ACT-HAZOP-45-03` to install continuous ambient $CS_2$ gas detector `AT-4501` (alarm setpoint at **10 % LEL**) interlocked to switch extraction fan `FN-4501` to high speed and execute an automatic trip of the solid PAX feeder.
> - **STRICT FIREFIGHTING MEDIA DIRECTIVE:** Use dry chemical, $CO_2$, or foam. **Do not use water jets on burning xanthate.** Applying high-pressure water streams to burning xanthate scatters the burning molten mass and accelerates violent hydrolysis, generating massive clouds of flammable and toxic $CS_2$ vapor. Non-sparking tools and anti-static PPE are strictly mandatory in Area 45.
> - **CARBON DISULFIDE ($CS_2$) EVOLUTION UPON HYDROLYSIS:** In the presence of moisture, acidic conditions, or make-up water exceeding **40 °C**, PAX undergoes rapid exothermic decomposition to release **carbon disulfide ($CS_2$)** and carbon oxysulfide ($COS$). Carbon disulfide is an extraordinarily toxic neurotoxin (IDLH 500 ppm) with a wide flammability range, a Lower Explosive Limit (LEL) of **1.3 %**, and an extremely low auto-ignition temperature of **90 °C** (which can be ignited by unlagged steam/hot water lines or mechanical friction).

## Chemical Identification & Physical Properties
| Parameter | Value | Source Citation |
| :--- | :--- | :--- |
| **Chemical Name** | Potassium amyl xanthate (PAX) / Potassium O-pentyl dithiocarbonate | SDS_2720-73-2_potassium-amyl-xanthate.pdf |
| **Synonyms** | Potassium pentyl xanthate, Carbonodithioic acid O-pentyl ester potassium salt | SDS_2720-73-2_potassium-amyl-xanthate.pdf |
| **CAS Registry Number** | 2720-73-2 | SDS_2720-73-2_potassium-amyl-xanthate.pdf |
| **Chemical Formula** | $C_6H_{11}KOS_2$ (or $C_5H_{11}OCS_2K$) | SDS_2720-73-2_potassium-amyl-xanthate.pdf, RB-4410-PFD-002 Rev B |
| **Molecular Weight** | 202.38 g/mol | Chemical standard |
| **Physical State / Appearance** | Pale yellow to yellowish-green pellets / solid powder with pungent sulfurous odor | RB-4410-OM-001 Rev 2 |
| **GHS Hazard Classification** | Self-heating solid; Acute Toxicity; Skin/Eye Irritant | SDS_2720-73-2_potassium-amyl-xanthate.pdf |
| **Primary Decomposition Product** | Carbon disulfide ($CS_2$, CAS 75-15-0) and Carbon oxysulfide ($COS$) | SDS_2720-73-2_potassium-amyl-xanthate.pdf, SDS_75-15-0_carbon-disulfide.pdf, RB-4410-PS-TK4501 Rev B |
| **Decomposition Triggers** | Moisture, ambient heat (>40 °C), acidic pH (<7.0) | SDS_2720-73-2_potassium-amyl-xanthate.pdf, RB-4410-OM-001 Rev 2 |
| **Carbon Disulfide ($CS_2$) LEL** | 1.3 % by volume in air | SDS_2720-73-2_potassium-amyl-xanthate.pdf, SDS_75-15-0_carbon-disulfide.pdf, RB-4410-OM-001 Rev 2 |
| **Carbon Disulfide ($CS_2$) Auto-ignition Temp** | 90 °C (spontaneous ignition on hot plant surfaces) | SDS_75-15-0_carbon-disulfide.pdf, RB-4410-OM-001 Rev 2 |
| **Primary Plant Equipment** | `TK-4501` (Mixing Tank, 40 m³) and `TK-4502` (Dosing Tank, 316L SS) | SDS_2720-73-2_potassium-amyl-xanthate.pdf, RB-4410-PS-TK4501 Rev B |
| **Dosing Service & Destination** | Rougher conditioning tank `TK-4101` and rougher cells `FC-4101` to `FC-4107` via pump `PP-4501A` | RB-4410-PID-45-001 Rev B, RB-4410-OM-001 Rev 2 |
| **Prepared Solution Concentration** | 20 % w/v aqueous solution | RB-4410-PS-TK4501 Rev B, RB-4410-OM-001 Rev 2 |
| **Target Circuit Dosing Rate** | 25 g/t dry ore ($67.2\text{ kg/h}$ pure PAX equivalent at 2,688 t/h solids feed) | RB-4410-PFD-002 Rev B, RB-4410-OM-001 Rev 2 |
| **Carbon Disulfide ($CS_2$) Flash Point** | -30 °C | SDS_75-15-0_carbon-disulfide.pdf |
| **Carbon Disulfide ($CS_2$) Exposure Limit** | TWA 1 ppm (ACGIH skin notation) | SDS_75-15-0_carbon-disulfide.pdf |

## Process Safety Hazards & Failure Modes
| Failure Mode / Hazard Event | Initiating Event | Consequences & Process Severity | Engineered & Procedural Safeguards |
| :--- | :--- | :--- | :--- |
| **Bulk Solid Self-Heating & Combustion** | Storage of solid PAX pellets in damp conditions or unventilated warehouse | Exothermic self-heating leading to smoldering, spontaneous ignition, and $CS_2 / SO_2$ generation | GHS Self-heating solid controls; store cool and dry in original sealed containers; moisture exclusion; dry chemical extinguishers |
| **Thermal Decomposition during Dissolution** | Make-up water supplied at >40 °C to mixing tank `TK-4501` | Accelerated hydrolysis into toxic and flammable $CS_2$ gas; rapid pressure/vapor surge | Make-up water temperature strictly interlocked <40 °C per RB-4410-OM-001; 24/7 continuous room extraction via `FN-4501` |
| **Acid Contamination Induced Hydrolysis** | Inadvertent cross-contamination with acid or acidic process water | Violent acidification of xanthate generating immediate high-rate $CS_2$ gas release | Segregated reagent storage; strict isolation from acidic chemicals; milk-of-lime buffering in circuit |
| **Toxic & Explosive Room Atmosphere** | Failure or inadvertent stop of extraction fan `FN-4501` | Rapid accumulation of $CS_2$ (LEL 1.3%, TWA 1 ppm skin) and $COS$ in enclosed room; operator acute neurotoxicity/asphyxiation | DCS interlock on `YS-4501` run status; entry prohibited if fan stopped; installation of `AT-4501` per `ACT-HAZOP-45-03` |
| **Vapor Ignition by Hot Surfaces or Sparks** | $CS_2$ vapor contact with uninsulated piping (>90 °C) or mechanical friction spark | Flash fire or room explosion (autoignition at 90 °C; flash point -30 °C; LEL 1.3%) | Spark-resistant fan wheel on `FN-4501`; mandatory non-sparking beryllium-copper tools; ATEX/IECEx Zone 1/2 rated electrical equipment |
| **Improper Firefighting Water Jet Application** | Responders using high-pressure water hoses on burning xanthate pellets | Spreading molten xanthate, violent chemical reaction, massive toxic plume escalation | Strict firefighting mandate: Do not use water jet on burning xanthate; apply dry chemical, $CO_2$, or foam only |
| **Personnel Dermal / Ocular Exposure** | Bag splitting, dusting during hopper charging, or solution splash | Severe eye irritation, dermal dermatitis, systemic xanthate poisoning | Chemical goggles, nitrile gloves, full faceshield, respiratory protection; emergency safety shower/eyewash within 10 s |

## Emergency Response & First Aid Measures
- **Inhalation:** Immediately remove casualty from exposure into fresh air. If breathing has stopped, trained personnel must administer artificial respiration (avoiding mouth-to-mouth contact if $CS_2$ is present). If breathing is labored, administer oxygen. Seek immediate medical attention.
- **Skin Contact:** Immediately strip contaminated clothing while flushing affected skin with copious running water for at least **15 minutes**. Wash thoroughly with mild soap and water. Seek medical evaluation if chemical irritation or burning persists (note ACGIH skin absorption hazard).
- **Eye Contact:** Immediately hold eyelids apart and flush eyes with a gentle stream of clean water or saline for at least **15 minutes**. Remove contact lenses if present and easy to do. Promptly transfer to ophthalmological care.
- **Ingestion:** Do NOT induce vomiting without medical advice. Rinse mouth thoroughly with water and give small sips of water if conscious. Seek emergency medical treatment immediately.
- **Firefighting Strategy:**
  - **Extinguishing Media:** Dry chemical powder, carbon dioxide ($CO_2$), or alcohol-resistant / universal foam.
  - **Critical Fire Caution:** **DO NOT USE WATER JET ON BURNING XANTHATE.** Water jets cause spattering of molten chemical, spread burning solids, and react exothermically with hot xanthate to accelerate the release of dense, flammable, toxic carbon disulfide ($CS_2$) gas. Cool surrounding unburned containers with water fog from a safe, protected distance.
- **Skin Contact:** Immediately strip contaminated clothing while flushing affected skin with copious running water for at least **15 minutes**. Wash thoroughly with mild soap and water. Seek medical evaluation if chemical irritation or burning persists.

## Safe Handling, Storage & Occupational Exposure Controls
- **Engineering Controls:**
  - Enclosed reagent preparation room must be maintained under negative pressure with dedicated, spark-resistant continuous mechanical extraction ventilation via fan `FN-4501`.
  - Equip reagent mixing room with continuous gas monitoring (`AT-4501`) calibrated for carbon disulfide ($CS_2$) with alarm at 10 % LEL interlocked to fan high-speed boost and dry feeder cutoff per `ACT-HAZOP-45-03`.
  - Batch make-up water temperature must be monitored and strictly maintained below **40 °C**.
  - All tools used in the PAX mixing enclosure must be non-sparking (bronze/beryllium alloy).
- **Safe Storage Practices:**
  - Store bulk solid PAX in original tightly closed containers in a cool, dry, well-ventilated, weather-protected warehouse.
  - Protect from direct sunlight, ambient heat sources, and moisture ingress.
  - Segregate strictly from acids, oxidizing agents, and combustible materials.
  - Area 45 reagent containment bunds must be segregated between xanthate/frother and lime.
- **Personal Protective Equipment (PPE):**
  - **Eye & Face Protection:** Chemical splash goggles and full face shield during solid hopper charging, mixing, or line breaking.
  - **Hand & Body Protection:** Impermeable chemical-resistant nitrile gauntlet gloves, chemical apron, and safety boots.
  - **Respiratory Protection:** Half-mask or full-face air-purifying respirator equipped with organic vapor and particulate (P100/OV) cartridges where dust or $CS_2$ vapor concentrations may approach or exceed occupational exposure standards (TWA 1 ppm). Positive-pressure SCBA or airline respirator required for emergency response or confined space entry.
  - **Respiratory Protection:** Half-mask or full-face air-purifying respirator equipped with organic vapor and particulate (P100/OV) cartridges where dust or $CS_2$ vapor concentrations may approach or exceed occupational exposure standards. Positive-pressure SCBA or airline respirator required for emergency response or confined space entry.

## Cross-Document Engineering Reconciliation
| Parameter / Topic | SDS_2720-73-2_potassium-amyl-xanthate.pdf | SDS_75-15-0_carbon-disulfide.pdf | RB-4410-PS-TK4501 Rev B | RB-4410-PID-45-001 Rev B | RB-4410-OM-001 Rev 2 | Reconciled Status |
| --- | --- | --- | --- | --- | --- | --- |
| **Reagent Identity** | Potassium amyl xanthate (PAX), CAS 2720-73-2 | — | Potassium amyl xanthate (PAX) | Potassium amyl xanthate (PAX) | Potassium amyl xanthate (PAX) | 100% Corroborated across all documents. |
| **Chemical Formula** | $C_6H_{11}KOS_2$ | — | Organosulfur collector | Aqueous PAX solution | $C_5H_{11}OCS_2K$ ($C_6H_{11}KOS_2$) | Chemically identical empirical / structural formulas. |
| **Target Equipment** | `TK-4501` / `TK-4502`, collector | Evolved in `TK-4501` room | `TK-4501` (40 m³ 316L SS) | `TK-4501`, `TK-4502`, `FN-4501` | `TK-4501`, `TK-4502`, `PP-4501A` | 100% Corroborated across plant hierarchy. |
| **Physical Hazard** | Self-heating solid | — | Decomposition off-gas | Enclosed room ventilation req'd | Non-sparking tools required | Corroborated: Self-heating solid behavior. |
| **Off-Gas Product** | $CS_2$ (highly flammable, toxic) | — | $CS_2$ evolution | $CS_2$ extraction via FN-4501 | $CS_2$ (LEL 1.3%, auto-ignition 90 °C) | 100% Corroborated: $CS_2$ primary hazard. |
| **Max Water Temp** | Decomposes with heat | — | Ambient (<35 °C) | Process water feed | $<40$ °C ceiling | Corroborated: Strict 40 °C operational limit. |
| **Firefighting Media** | Dry chemical, $CO_2$, foam; no water jet | Dry chemical, $CO_2$, foam; no water jet | — | Note 1 ventilation | Dry chemical, $CO_2$, foam; no water jet | Corroborated: Water jet strictly prohibited. |
| **Ventilation Control** | Local exhaust ventilation | Local exhaust ventilation | FN-4501 continuous | FN-4501 continuous (Note 1) | FN-4501 continuous 24/7 | 100% Corroborated: Continuous extraction. |
| **HAZOP Action** | — | — | — | — | — | ACT-HAZOP-45-03 mandates AT-4501 interlock. |
| **Decomposition Off-Gas** | $CS_2$ (highly flammable, toxic) | Carbon disulfide ($CS_2$), CAS 75-15-0; evolved in TK-4501 room | $CS_2$ evolution | $CS_2$ extraction via FN-4501 | $CS_2$ (LEL 1.3%, auto-ignition 90 °C) | 100% Corroborated: $CS_2$ is primary off-gas hazard in TK-4501. |
| **$CS_2$ Auto-ignition** | — | 90 °C | — | 90–100 °C | 90 °C | Reconciled: 90 °C is authoritative rating. |
| **$CS_2$ Flash Point** | — | -30 °C | — | — | — | Grounded in SDS 75-15-0. |
| **$CS_2$ Exposure Limit** | — | TWA 1 ppm (ACGIH skin notation) | — | IDLH 500 ppm | — | Grounded in SDS 75-15-0. |

## References & Sources
[^src-1]: SDS_2720-73-2_potassium-amyl-xanthate.pdf (corpora/copper-concentrator/raw/standards/SDS_2720-73-2_potassium-amyl-xanthate.pdf)
[^src-2]: SDS_75-15-0_carbon-disulfide.pdf (corpora/copper-concentrator/raw/standards/SDS_75-15-0_carbon-disulfide.pdf)
[^src-3]: RB-4410-PS-TK4501_PAX XANTHATE MIXING TANK PROCESS DATA SHEET_B.pdf (corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-TK4501_PAX XANTHATE MIXING TANK PROCESS DATA SHEET_B.pdf)
[^src-4]: RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf (corpora/copper-concentrator/raw/pid/RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf)
[^src-5]: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf (corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf)
[^src-6]: RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf (corpora/copper-concentrator/raw/standards/RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf)
