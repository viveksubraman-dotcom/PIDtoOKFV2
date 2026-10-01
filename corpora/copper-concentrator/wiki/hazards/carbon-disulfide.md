---
type: Hazard Profile
title: Carbon Disulfide (CS2) Chemical Safety & Decomposition Hazard Profile (CAS
  75-15-0)
description: Chemical safety profile, auto-ignition at 90 °C, flash point -30 °C,
  LEL 1.3%, ACGIH 1 ppm skin notation, TK-4501 room evolution, FN-4501 continuous
  ventilation, and ACT-HAZOP-45-03 safeguards for carbon disulfide.
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/hazards/carbon-disulfide.md
tags:
- area 45
- autoignition
- cas 75-15-0
- chemical safety
- cs2
- cs2-evolution
- decomposition product
- firefighting
- flash point
- fn-4501
- hazard profile
- hazards
- hazop
- hz-45-03
- idlh
- lel
- pax
- process safety
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
- id: src-2
  resource: corpora/copper-concentrator/raw/standards/SDS_2720-73-2_potassium-amyl-xanthate.pdf
  title: SDS_2720-73-2_potassium-amyl-xanthate.pdf
- id: src-3
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-TK4501_PAX XANTHATE MIXING TANK PROCESS
    DATA SHEET_B.pdf
  title: RB-4410-PS-TK4501_PAX XANTHATE MIXING TANK PROCESS DATA SHEET_B.pdf
- id: src-4
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER
    & LIME_B.pdf
  title: RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf
- id: src-5
  resource: corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR
    OPERATING MANUAL_R2.pdf
  title: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf
- id: src-6
  resource: corpora/copper-concentrator/raw/standards/RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf
  title: RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T22:16:00Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T22:16:00Z'
- by: process:okf-validation-suite
  at: '2026-09-30T22:16:00Z'
status: stable
entity_metadata:
  cas_number: 75-15-0
  target_equipment:
  - TK-4501
  - TK-4502
  - FN-4501
  - AT-4501
  skin_notation: true
  target_unit: Area 45 - Reagents
  chemical_formula: CS2
  hazop_node: HZ-45-03
  max_makeup_water_temp_c: 40
  autoignition_temperature_c: 90
  idlh_ppm: 500
  firefighting_media:
  - Dry chemical
  - CO2
  - Foam
  ppe:
  - Chemical splash goggles
  - Nitrile gauntlet gloves
  - Organic vapor respirator / SCBA
  chemical_name: Carbon disulfide (decomposition product)
  uel_pct: 50
  firefighting_prohibition: Do not use water jet on burning xanthate
  first_aid:
    eyes_and_skin: Flush eyes and skin with water for 15 minutes; seek medical attention
    inhalation: Remove to fresh air; seek medical attention
  lel_pct: 1.3
  act_hazop_45_03: Install CS2 gas detector AT-4501 (alarm 10 % LEL) interlocked to
    FN-4501 high speed and PAX feeder stop
  flash_point_c: -30
  acgih_twa_ppm: 1
---

# Carbon Disulfide ($CS_2$) Chemical Safety & Decomposition Hazard Profile (CAS 75-15-0)

> ⚠️ **CRITICAL PROCESS SAFETY / VOLATILE AUTO-IGNITION WARNING:**
> - **EXTREMELY LOW AUTO-IGNITION TEMPERATURE (90 °C) & WIDE EXPLOSIVE RANGE:** Carbon disulfide ($CS_2$, CAS 75-15-0) is an extraordinarily hazardous, volatile off-gas generated during the handling and dissolution of potassium amyl xanthate (PAX) in Area 45. It possesses a flash point of **-30 °C**, a Lower Explosive Limit (LEL) of **1.3 %**, and an extremely low auto-ignition temperature of **90 °C**. At 90 °C, contact with unlagged low-pressure steam piping, hot water tracing, or unrated electrical lighting can trigger spontaneous vapor cloud ignition without an open flame.
> - **EQUIPMENT RECONCILIATION (TK-4501 / FN-4501):** Safety Data Sheet `SDS_75-15-0_carbon-disulfide.pdf` explicitly identifies its plant occurrence as: *"Evolved in TK-4501 room"*. This directly aligns with Process Data Sheet `RB-4410-PS-TK4501 Rev B`, P&ID `RB-4410-PID-45-001 Rev B` Note 1, Operating Manual `RB-4410-OM-001 Rev 2` (Sec 3.45 & Sec 8), and HAZOP Study `RB-4410-STD-HAZOP-001 Rev 1` Node HZ-45-03.
> - **ACGIH OCCUPATIONAL EXPOSURE LIMIT (1 PPM SKIN):** ACGIH establishes an 8-hour Time-Weighted Average (TWA) of **1 ppm** with a **"Skin"** notation. Percutaneous absorption through skin is a major systemic toxicity route causing severe central and peripheral nervous system degradation.
> - **MANDATORY 24/7 EXTRACTION (FN-4501) & HAZOP INTERLOCK (ACT-HAZOP-45-03):** P&ID `RB-4410-PID-45-001 Rev B` Note 1 mandates that extraction fan `FN-4501` run continuously 24/7 to maintain negative pressure in the enclosed mixing room. HAZOP recommendation `ACT-HAZOP-45-03` requires continuous ambient gas detector `AT-4501` (alarm at **10 % LEL**) interlocked to switch `FN-4501` to high speed and stop the solid PAX dry feeder.
> - **FIREFIGHTING DIRECTIVE & XANTHATE WATER JET PROHIBITION:** Extinguishing agents must be dry chemical, $CO_2$, or foam. **Do not use water jet on burning xanthate.** Applying water jets to burning solid xanthate scatters burning molten pellets and drives accelerated exothermic hydrolysis, generating catastrophic clouds of toxic and explosive $CS_2$ vapor. Non-sparking beryllium-copper tools are strictly mandatory in Area 45.

## Chemical Identification & Physical Properties
| Parameter | Value | Source Citation |
| :--- | :--- | :--- |
| **Chemical Name** | Carbon disulfide (decomposition product) | SDS_75-15-0_carbon-disulfide.pdf |
| **Synonyms** | Carbon bisulfide, Dithiocarbonic anhydride, Methanedithione | Chemical standard |
| **CAS Registry Number** | 75-15-0 | SDS_75-15-0_carbon-disulfide.pdf |
| **Chemical Formula** | $CS_2$ | SDS_75-15-0_carbon-disulfide.pdf |
| **Molecular Weight** | 76.14 g/mol | Chemical standard |
| **Physical State / Appearance** | Clear, colorless to faintly yellow volatile liquid / heavy vapor with sweet ether-like to pungent "rotten cabbage" odor | SDS_75-15-0_carbon-disulfide.pdf, RB-4410-OM-001 Rev 2 |
| **Flash Point (Closed Cup)** | -30 °C | SDS_75-15-0_carbon-disulfide.pdf |
| **Auto-Ignition Temperature** | 90 °C | SDS_75-15-0_carbon-disulfide.pdf, RB-4410-OM-001 Rev 2 |
| **Lower Explosive Limit (LEL)** | 1.3 % by volume in air | SDS_75-15-0_carbon-disulfide.pdf, RB-4410-OM-001 Rev 2 |
| **Upper Explosive Limit (UEL)** | 50.0 % by volume in air | RB-4410-PID-45-001 Rev B (Note 1) |
| **Occupational Exposure Limit (TLV/TWA)**| 1 ppm (8-hour TWA, ACGIH "Skin" notation) | SDS_75-15-0_carbon-disulfide.pdf |
| **Immediately Dangerous to Life or Health (IDLH)** | 500 ppm | RB-4410-PID-45-001 Rev B |
| **Vapor Density (Air = 1)** | 2.63 (vapors sink and accumulate in pits/low spots) | Chemical engineering standard |
| **Boiling Point** | 46.2 °C | Chemical standard |
| **Generation Route / Plant Duty** | Spontaneous decomposition of solid/aqueous PAX in mixing tank `TK-4501` room | SDS_75-15-0_carbon-disulfide.pdf, RB-4410-PS-TK4501 Rev B |

## Process Safety Hazards & Failure Modes
| Failure Mode / Hazard Event | Initiating Cause | Consequences & Process Severity | Engineered & Procedural Safeguards |
| :--- | :--- | :--- | :--- |
| **Thermal Hydrolysis in Mixing Tank** | Make-up process water supplied at >40 °C during batch preparation in `TK-4501` | Rapid, exothermic hydrolysis of PAX generating massive $CS_2$ vapor surge into room atmosphere | Process water supply temperature monitored and strictly held below 40 °C per RB-4410-OM-001 Sec 8; 24/7 exhaust via `FN-4501` |
| **Enclosed Space Vapor Accumulation** | Mechanical failure or inadvertent trip of extraction fan `FN-4501` | $CS_2$ vapor rapidly exceeds 1 ppm TWA and 1.3% LEL, creating lethal IDLH and explosive environment | DCS interlock on `YS-4501` run status; audible/visual door alarms; room entry strictly prohibited if fan is off |
| **Low-Temperature Hot Surface Auto-Ignition** | $CS_2$ vapor contact with hot surfaces > 90 °C (e.g. steam lines, uninsulated piping, hot motor bearings) | Spontaneous vapor cloud ignition without spark or flame; violent flash fire or enclosure explosion | All steam/hot water lines insulated; equipment surface temperature ratings $\le T6$ (85 °C); spark-resistant `FN-4501` wheel |
| **Mechanical / Electrostatic Spark Ignition** | Dropping steel tools, electrical switching, or static buildup during dry PAX pellet charging | Ignition of localized $CS_2$ vapor pockets exceeding 1.3% LEL; fireball and thermal radiation burns | Mandatory non-sparking bronze tools; anti-static footwear and clothing; Zone 1/Zone 2 electrical apparatus |
| **Acid Contamination Induced Hydrolysis** | Inadvertent cross-contamination of PAX with acidic chemicals or acidic wash water | Violent acid-catalyzed decomposition producing high-rate toxic $CS_2$ gas release | Physical segregation of Area 45 reagent bunds; milk-of-lime alkaline buffering; dedicated washdown systems |
| **Percutaneous & Inhalation Toxic Exposure** | Bag splitting, dusting during hopper filling, or sampling without barrier PPE | Acute neurotoxicity, headaches, blurred vision, unconsciousness, severe skin dermatitis (ACGIH Skin notation) | Full-face respirator with OV cartridges, chemical splash goggles, nitrile gauntlets; emergency shower/eyewash within 10 s |
| **Escalation from Water Jet Firefighting** | Responders using high-pressure water hoses on burning xanthate pellets | Splattering of molten solid and rapid exothermic reaction driving runaway $CS_2$ gas generation | Strict firefighting rule: "Do not use water jet on burning xanthate"; apply dry chemical, $CO_2$, or foam only |

## Emergency Response & First Aid Measures
- **Inhalation:** Immediately remove casualty from contaminated atmosphere into fresh air. If breathing has stopped, trained personnel must administer artificial respiration (avoiding direct mouth-to-mouth resuscitation due to secondary $CS_2$ off-gassing). If breathing is difficult, administer medical oxygen. Seek immediate medical attention.
- **Eye Contact:** Immediately flood eyes with copious amounts of clean running water or saline solution for at least **15 minutes**, holding eyelids open. Remove contact lenses if present and easy to remove. Obtain urgent ophthalmological evaluation.
- **Skin Contact:** Promptly remove all contaminated clothing, footwear, and PPE while flushing the skin thoroughly under a deluge safety shower for at least **15 minutes**. Wash with mild soap and water. Seek prompt medical care; observe for signs of systemic percutaneous poisoning.
- **Firefighting Strategy:**
  - **Extinguishing Media:** Dry chemical powder, carbon dioxide ($CO_2$), or alcohol-resistant / standard foam.
  - **Mandatory Firefighting Directive:** **DO NOT USE WATER JET ON BURNING XANTHATE.** Direct water streams scatter burning chemical solids and violently accelerate the hydrolysis of PAX into flammable, toxic $CS_2$ vapor clouds. Cool surrounding unburned containers and structural steel from a safe, sheltered standoff using water fog.

## Safe Handling, Storage & Occupational Exposure Controls
- **Engineering Controls:**
  - **Mechanical Ventilation:** The enclosed PAX preparation room housing `TK-4501` and `TK-4502` must operate under continuous negative pressure with spark-resistant extraction fan `FN-4501` operating 24/7 per Note 1 of P&ID `RB-4410-PID-45-001 Rev B`.
  - **Gas Detection & Interlocks (ACT-HAZOP-45-03):** Equip the room with continuous ambient $CS_2$ infrared/electrochemical detector `AT-4501` calibrated across 0–100 % LEL. Set alarm at **10 % LEL** interlocked to trigger high-speed ventilation boost on `FN-4501` and an immediate emergency stop of the solid PAX dry feeder.
  - **Thermal Management:** Process make-up water temperature must never exceed **40 °C** per `RB-4410-OM-001 Rev 2`.
  - **Hot Surface Protection:** All thermal equipment surfaces within Area 45 must remain below **90 °C** (conservative $T6$ rating of 85 °C).
  - **Tooling:** Only non-sparking beryllium-copper or bronze hand tools are permitted inside the xanthate handling facility.
- **Personal Protective Equipment (PPE):**
  - **Eye & Face Protection:** Chemical splash goggles and full face shield during solid loading, solution mixing, or pipe breaking.
  - **Skin & Hand Protection:** Heavyweight chemical-resistant nitrile gauntlets, chemical apron, and safety gumboots.
  - **Respiratory Protection:** Where vapor concentrations approach or exceed 1 ppm TWA, operators must wear a NIOSH-approved half-face or full-face air-purifying respirator equipped with organic vapor (OV) cartridges. Positive-pressure self-contained breathing apparatus (SCBA) is mandatory for emergency entry or unventilated spaces.

## Cross-Document Engineering Reconciliation
| Parameter / Topic | SDS_75-15-0_carbon-disulfide.pdf | SDS_2720-73-2_potassium-amyl-xanthate.pdf | RB-4410-OM-001 Rev 2 | RB-4410-PID-45-001 Rev B | Reconciled Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Chemical Identity** | Carbon disulfide ($CS_2$), CAS 75-15-0 | $CS_2$ (PAX decomposition off-gas) | $CS_2$ off-gas | $CS_2$ off-gas | 100% Corroborated across all documents. |
| **Flash Point** | -30 °C | — | — | — | Grounded in SDS 75-15-0. |
| **Auto-Ignition Temp** | 90 °C | — | 90 °C (Sec 8) | 90–100 °C (literature) | Reconciled: 90 °C is authoritative conservative design rating. |
| **Lower Explosive Limit (LEL)** | 1.3 % | 1.3 % | 1.3 % | 1.3 % | 100% Corroborated across all engineering documents. |
| **Exposure Limit (TWA)** | 1 ppm (ACGIH skin notation) | — | — | IDLH 500 ppm | Grounded in SDS 75-15-0; 1 ppm skin notation established. |
| **Plant Duty / Equipment** | Evolved in `TK-4501` room | `TK-4501` / `TK-4502` collector | `TK-4501` batch mixing | `TK-4501`, `TK-4502`, `FN-4501` | 100% Corroborated across plant hierarchy. |
| **Firefighting Media** | Dry chemical, $CO_2$, foam; no water jet | Dry chemical, $CO_2$, foam; no water jet | Dry chemical, $CO_2$, foam; no water jet | — | 100% Corroborated: Water jet strictly prohibited. |
| **Safeguards / Actions** | Local exhaust ventilation | Local exhaust ventilation | FN-4501 continuous 24/7 | FN-4501 continuous; Note 1 | ACT-HAZOP-45-03 mandates AT-4501 interlock to FN-4501. |

## References & Sources
[^src-1]: SDS_75-15-0_carbon-disulfide.pdf (corpora/copper-concentrator/raw/standards/SDS_75-15-0_carbon-disulfide.pdf)
[^src-2]: SDS_2720-73-2_potassium-amyl-xanthate.pdf (corpora/copper-concentrator/raw/standards/SDS_2720-73-2_potassium-amyl-xanthate.pdf)
[^src-3]: RB-4410-PS-TK4501_PAX XANTHATE MIXING TANK PROCESS DATA SHEET_B.pdf (corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-TK4501_PAX XANTHATE MIXING TANK PROCESS DATA SHEET_B.pdf)
[^src-4]: RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf (corpora/copper-concentrator/raw/pid/RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf)
[^src-5]: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf (corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf)
[^src-6]: RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf (corpora/copper-concentrator/raw/standards/RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf)
