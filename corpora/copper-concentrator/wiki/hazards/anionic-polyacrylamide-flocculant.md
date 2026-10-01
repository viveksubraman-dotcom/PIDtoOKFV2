---
type: Hazard Profile
title: Anionic Polyacrylamide Flocculant Chemical Safety & Slip Hazard Profile (CAS
  9003-05-8)
description: Chemical safety, extreme wet slip hazard, thickener over-dosing rheology,
  and handling controls for anionic polyacrylamide flocculant (CAS 9003-05-8).
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/hazards/anionic-polyacrylamide-flocculant.md
tags:
- area 45
- area 51
- area 61
- cas 9003-05-8
- flocculant
- hazard profile
- pam
- polyacrylamide
- process safety
- reagents
- sds
- slip-hazard
- standards
- th-5101
- th-6101
- thickener
sources:
- id: src-1
  resource: corpora/copper-concentrator/raw/standards/SDS_9003-05-8_anionic-polyacrylamide-flocculant.pdf
  title: SDS_9003-05-8_anionic-polyacrylamide-flocculant.pdf
- id: src-2
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-TH5101_CONCENTRATE THICKENER PROCESS
    DATA SHEET_B.pdf
  title: RB-4410-PS-TH5101_CONCENTRATE THICKENER PROCESS DATA SHEET_B.pdf
- id: src-3
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-TH6101_TAILINGS THICKENER PROCESS
    DATA SHEET_B.pdf
  title: RB-4410-PS-TH6101_TAILINGS THICKENER PROCESS DATA SHEET_B.pdf
- id: src-4
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-51-001_P&ID CONCENTRATE THICKENING & FILTRATION_B.pdf
  title: RB-4410-PID-51-001_P&ID CONCENTRATE THICKENING & FILTRATION_B.pdf
- id: src-5
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-61-001_P&ID TAILINGS THICKENING & PUMPING
    TO TSF_B.pdf
  title: RB-4410-PID-61-001_P&ID TAILINGS THICKENING & PUMPING TO TSF_B.pdf
- id: src-6
  resource: corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR
    OPERATING MANUAL_R2.pdf
  title: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T22:21:21Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T22:21:21Z'
- by: process:okf-validation-suite
  at: '2026-09-30T22:21:21Z'
status: stable
entity_metadata:
  ghs_classification:
  - Low toxicity
  - Spills extremely slippery
  exposure_controls:
  - Local exhaust ventilation
  - Chemical splash goggles
  - Nitrile gloves
  - Particulate respirator (N95/P2)
  thickener_tailings_torque_limit_mnm: 12.5
  plant_usage: High-rate thickeners TH-5101 and TH-6101 solid-liquid separation
  firefighting_prohibition: Do not use water jet on burning xanthate
  thickener_conc_dose_range_gpt: 15 - 25
  cas_number: 9003-05-8
  handling_storage: Store cool and dry, away from acids and ignition sources; keep
    containers closed
  target_equipment:
  - TH-5101
  - TH-6101
  - FP-5101
  - TK-4531
  firefighting_media:
  - Dry chemical
  - CO2
  - Foam
  chemical_name: Anionic polyacrylamide flocculant
  chemical_formula: PAM
  target_units:
  - Area 45 - Reagents
  - Area 51 - Concentrate Thickening & Filtration
  - Area 61 - Tailings Thickening & Pumping
  first_aid:
    inhalation: Remove to fresh air; seek medical attention
    eyes_and_skin: Flush with water for 15 minutes; seek medical attention
---

# Anionic Polyacrylamide Flocculant Chemical Safety & Slip Hazard Profile (CAS 9003-05-8)

> ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
> - **EXTREME SLIP AND FALL HAZARDS WHEN HYDRATED:** Anionic polyacrylamide flocculant (CAS No. 9003-05-8, chemical type PAM) is classified as having low systemic chemical toxicity, but presents an acute physical safety hazard: **"spills extremely slippery"** per SDS `standards/SDS_9003-05-8_anionic-polyacrylamide-flocculant.pdf`. Contact between dry polymer powder or concentrated liquid polymer and moisture/water creates an exceptionally slick, high-lubricity viscoelastic gel. Spills on access stairs, elevated walkways, rake bridges, and launder platforms around Concentrate Thickener `TH-5101` and Tailings Thickener `TH-6101` represent severe slip, trip, and fall hazards. Dry spills must NEVER be hosed down immediately; dry powder must be swept or vacuumed dry first, followed by application of absorbent sand/grit, before final high-pressure washdown.
> - **THICKENER OVER-DOSING & UNDERFLOW VISCOELASTIC GEL LOCKUP:** Process Data Sheet `RB-4410-PS-TH5101 Rev B` establishes an optimum flocculant dosing window of **15 to 25 g/t dry solids**. Operating Manual `RB-4410-OM-001 Rev 2` (Sections 3.51, 3.61, 10, and 11) warns that over-dosing flocculant (>25 g/t in `TH-5101` or excessive dosage in `TH-6101`) causes hyper-bridging flocculation, resulting in an unpumpable viscoplastic bed structure, extreme yield stress, and rapid rake torque escalation exceeding mechanical ratings (12.5 MNm on `TH-6101`). Furthermore, residual polymer in thickened concentrate blinds filter cloths on filter press `FP-5101`, preventing cake dewatering below the Transportable Moisture Limit (TML 9.8% w/w).
> - **FIREFIGHTING CAUTION & REAGENT SEGREGATION:** Suitable extinguishing media are dry chemical, $\text{CO}_2$, or foam. Section 5 of the SDS mandates: *"Do not use water jet on burning xanthate"*, referencing co-located storage of potassium amyl xanthate (PAX, `TK-4501`) in Area 45. High-pressure water jets striking burning xanthate cause violent spattering of toxic molten chemical and accelerate rapid decomposition into toxic, flammable carbon disulfide ($\text{CS}_2$) vapor.

## Chemical Identification & General Specifications
| Parameter | Value | Source Citation |
| :--- | :--- | :--- |
| **Chemical Name** | Anionic polyacrylamide flocculant | SDS_9003-05-8_anionic-polyacrylamide-flocculant.pdf |
| **Chemical Family / Type** | Polyacrylamide (PAM) anionic polymer | SDS_9003-05-8_anionic-polyacrylamide-flocculant.pdf |
| **CAS Registry Number** | 9003-05-8 | SDS_9003-05-8_anionic-polyacrylamide-flocculant.pdf |
| **GHS Classification** | Low toxicity; Spills extremely slippery | SDS_9003-05-8_anionic-polyacrylamide-flocculant.pdf |
| **Plant Duty & Equipment Use** | High-rate thickeners `TH-5101` (Concentrate) and `TH-6101` (Tailings) | SDS_9003-05-8, PS-TH5101 Rev B, PS-TH6101 Rev B |
| **Reagent Storage / Make-Up System** | Area 45 Reagents Flocculant Dosing System `TK-4531` | RB-4410-PID-51-001 Rev B (Note 1) |
| **Concentrate Thickener Dosage Target** | 15 – 25 g/t dry solids | RB-4410-PS-TH5101 Rev B, RB-4410-OM-001 Rev 2 |
| **Concentrate Underflow Target Density** | 65.0 % solids w/w (SG 1.966) | RB-4410-PFD-003 Rev B, RB-4410-PS-TH5101 Rev B |
| **Tailings Underflow Target Density** | 62.0 % solids w/w (SG 1.652) | RB-4410-PFD-003 Rev B, RB-4410-PS-TH6101 Rev B |
| **Tailings Basin Diameter & Drive Torque** | 60 m diameter; 12.5 MNm design torque rating | RB-4410-PS-TH6101 Rev B, RB-4410-OM-001 Rev 2 |

## Process Safety Hazards & Failure Modes
| Failure Mode / Hazard Event | Initiating Event | Consequences & Process Severity | Engineered & Procedural Safeguards |
| :--- | :--- | :--- | :--- |
| **Personnel Slip, Trip & Fall Injuries** | Powder spillage during bag slitting or line leak contacting wash water | Formation of frictionless hydrogel film on floors, access stairs, and catwalks | Dry sweeping before washing; application of sand/salt/absorbent grit; mandatory anti-slip safety footwear |
| **Concentrate Slime Carryover & Grade Loss** | Flocculant dosing pump trip, line plugging, or under-dosing (<15 g/t) | Incomplete solid-liquid separation; chalcopyrite slimes carry over in 103 m³/h overflow to process water circuit | Continuous turbidity monitoring on overflow launder; automated switchover to standby dosing pump; feed-forward ratio control |
| **Rake Drive Torque Overload & Arm Buckling** | Flocculant over-dosing (>25 g/t) or underflow transfer pump stoppage | Rapid bed consolidation, excessive compaction yield stress exceeding 12.5 MNm mechanical limit on TH-6101 | Automated rake lift on torque high; high bed level alarm (LT-6101 LAH 6.5 m); emergency cone water dilution valves |
| **Filter Cloth Blinding & Cake Liquefaction** | Polymer overdosing carrying unadsorbed high-MW flocculant to FP-5101 | Polymer film blinds filter press cloths; high cake moisture (>9.8% w/w TML), risk of bulk carrier capsize | Strict dosage regulation (15–25 g/t); cloth wash cycles; online cake moisture analyzer before concentrate loadout |
| **Dust Inhalation & Eye Irritation** | Manual charging of dry polymer powder without ventilation | Mechanical irritation of respiratory tract and eyes | Local exhaust ventilation at hopper; chemical splash goggles; N95/P2 particulate respirators |
| **Multi-Reagent Firefighting Conflict** | Use of water jets in Area 45 during fire involving adjacent xanthate (TK-4501) | Scatter of burning xanthate; rapid hydrolysis producing explosive, toxic carbon disulfide ($CS_2$) gas | Dry chemical, CO2, or foam extinguishers; strict directive: do not use water jet on burning xanthate |

## Emergency Response & First Aid Measures
- **Inhalation:** Immediately move casualty to fresh air. If coughing or respiratory irritation develops, seek prompt medical attention.
- **Eye Contact:** Immediately flush eyes thoroughly with clean running water for at least 15 minutes, holding eyelids open. Remove contact lenses if present and easy to do. Obtain medical advice.
- **Skin Contact:** Wash contaminated skin thoroughly with soap and running water for at least 15 minutes. Remove contaminated clothing and wash before reuse.
- **Ingestion:** Rinse mouth thoroughly with water. If conscious, give small sips of water. Do NOT induce vomiting unless instructed by medical professionals.
- **Spill Cleanup Protocol:**
  - **Dry Polymer Spills:** Sweep or vacuum up dry material immediately into suitable waste containers. Do NOT apply water to dry powder spills, as this creates an immediate slip hazard.
  - **Wet / Solution Spills:** Cordon off area immediately. Apply sand, inert absorbent clay, or salt to increase traction and absorb gel. Wash down with high-pressure water only after physical bulk removal of polymer.
- **Firefighting Protocol:**
  - Approved Agents: Dry chemical powder, carbon dioxide ($\text{CO}_2$), or foam.
  - Critical Multi-Reagent Directive: **Do not use water jet on burning xanthate** stored in adjacent Area 45 reagent tanks (`TK-4501`).

## Handling, Storage & Exposure Controls
- **Engineering Controls:** Maintain local mechanical exhaust ventilation in polymer mixing, handling, and feeder areas to minimize airborne dust concentrations. Keep storage containers tightly closed.
- **Storage Conditions:** Store in a cool, dry, well-ventilated storage warehouse away from moisture, strong acids, and direct ignition sources. Maintain containers tightly closed to prevent atmospheric moisture absorption and lump formation.
- **Personal Protective Equipment (PPE):**
  - **Eye Protection:** Chemical splash goggles meeting EN 166 / ANSI Z87.1.
  - **Hand Protection:** Nitrile rubber chemical-resistant gloves.
  - **Skin & Body Protection:** Protective coveralls and safety boots with slip-resistant soles.
  - **Respiratory Protection:** Approved particulate respirator (N95/P2 rating minimum) during dry bag handling, bulk hopper dumping, or where exposure limits may be exceeded.

## References & Sources
[^src-1]: SDS_9003-05-8_anionic-polyacrylamide-flocculant.pdf (corpora/copper-concentrator/raw/standards/SDS_9003-05-8_anionic-polyacrylamide-flocculant.pdf)
[^src-2]: RB-4410-PS-TH5101_CONCENTRATE THICKENER PROCESS DATA SHEET_B.pdf (corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-TH5101_CONCENTRATE THICKENER PROCESS DATA SHEET_B.pdf)
[^src-3]: RB-4410-PS-TH6101_TAILINGS THICKENER PROCESS DATA SHEET_B.pdf (corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-TH6101_TAILINGS THICKENER PROCESS DATA SHEET_B.pdf)
[^src-4]: RB-4410-PID-51-001_P&ID CONCENTRATE THICKENING & FILTRATION_B.pdf (corpora/copper-concentrator/raw/pid/RB-4410-PID-51-001_P&ID CONCENTRATE THICKENING & FILTRATION_B.pdf)
[^src-5]: RB-4410-PID-61-001_P&ID TAILINGS THICKENING & PUMPING TO TSF_B.pdf (corpora/copper-concentrator/raw/pid/RB-4410-PID-61-001_P&ID TAILINGS THICKENING & PUMPING TO TSF_B.pdf)
[^src-6]: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf (corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf)
