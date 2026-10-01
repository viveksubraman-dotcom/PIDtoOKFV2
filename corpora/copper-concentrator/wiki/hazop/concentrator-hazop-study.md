---
type: HAZOP Study
title: Concentrator Selected Nodes HAZOP Study & Action Item Tracking (RB-4410-STD-HAZOP-001
  Rev 1)
description: HAZOP worksheets, node deviations, root causes, consequences, IPL safeguards,
  mandatory recommendations, and 5x5 risk ranking matrix across comminution, reagents,
  and tailings.
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/hazop/concentrator-hazop-study.md
tags:
- cas 37286-64-9
- deviations
- df-250
- hazop
- hz-31-02
- hz-31-04
- hz-45-03
- hz-45-06
- hz-61-01
- process-safety
- rb-4410
- recommendations
- risk-matrix
- safeguards
sources:
- id: src-1
  resource: corpora/copper-concentrator/raw/standards/RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf
  title: RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf
- id: src-2
  resource: corpora/copper-concentrator/raw/standards/RB-4410-STD-CE-001_SIS CAUSE AND EFFECT MATRIX_B.pdf
  title: RB-4410-STD-CE-001_SIS CAUSE AND EFFECT MATRIX_B.pdf
- id: src-3
  resource: corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR
    OPERATING MANUAL_R2.pdf
  title: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf
- id: src-4
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-31-002_P&ID SAG MILL HYDROSTATIC LIFT &
    LUBE SYSTEM_B.pdf
  title: RB-4410-PID-31-002_P&ID SAG MILL HYDROSTATIC LIFT & LUBE SYSTEM_B.pdf
- id: src-5
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER
    & LIME_B.pdf
  title: RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf
- id: src-6
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-61-001_P&ID TAILINGS THICKENING & PUMPING
    TO TSF_B.pdf
  title: RB-4410-PID-61-001_P&ID TAILINGS THICKENING & PUMPING TO TSF_B.pdf
- id: src-7
  resource: corpora/copper-concentrator/raw/standards/SDS_37286-64-9_polyglycol-ether-frother.pdf
  title: SDS_37286-64-9_polyglycol-ether-frother.pdf
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T22:13:56Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T22:13:56Z'
- by: process:okf-validation-suite
  at: '2026-09-30T22:13:56Z'
status: stable
entity_metadata:
  governing_standard: RB-4410-STD-HAZOP-001 Rev 1
  action_items:
  - action_id: ACT-HAZOP-31-02
    responsible: Lead Mechanical Engineer
    node_ref: HZ-31-02
    tag: PSV-3105
    recommendation: Confirm PSV-3105 set pressure on P&ID matches data sheet
  - responsible: Lead Electrical & C&I Engineer / Process Safety Lead
    node_ref: HZ-31-04
    action_id: ACT-HAZOP-31-04
    recommendation: Align TAHH setpoint between instrument data sheet and cause &
      effect
    tag: SIF-3101
  - recommendation: Install CS2 gas detector AT-4501 (alarm 10 % LEL) interlocked
      to FN-4501 high speed and PAX feeder stop
    tag: AT-4501
    responsible: Lead C&I Engineer
    node_ref: HZ-45-03
    action_id: ACT-HAZOP-45-03
  - tag: TK-4511
    responsible: Chemical Metallurgist / Electrical Engineer
    node_ref: HZ-45-06
    action_id: ACT-HAZOP-45-06
    recommendation: Confirm frother identity on P&ID vs data sheet and SDS
  - responsible: Lead Mechanical Engineer
    action_id: ACT-HAZOP-61-01
    node_ref: HZ-61-01
    recommendation: Confirm stage-3 casing design pressure on P&ID
    tag: PP-6101A/B/C
  nodes_count: 5
  risk_matrix_dimensions: 5x5
  recommendations_mandatory: true
  act_hazop_45_06_clarification: SDS_37286-64-9 confirms DF-250 is alternative frother
    not specified for baseline TK-4511
---

## Mandatory HAZOP Action Item Tracking Register
| Action Item ID | Associated Node | Action Description | Responsible Party | Verification Milestone | Target Asset Tag | Discrepancy Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ACT-HAZOP-31-02** | HZ-31-02 | Issue formal P&ID redline for `RB-4410-PID-31-002 Rev B` correcting `PSV-3105` set pressure from 180 bar(g) to 160 bar(g) to ensure compliance with 170 bar(g) system design pressure. | Lead Mechanical Engineer | P&ID Rev C As-Built Issuance | `PSV-3105` | ⚠️ CONFLICT: P&ID 180 bar vs Data Sheet / OM 160 bar vs Design 170 bar |
| **ACT-HAZOP-31-04** | HZ-31-04 | Reconcile trunnion bearing TAHH trip threshold between `RB-4410-PS-0034 Rev B` (75 °C) and `RB-4410-STD-CE-001 Rev B` (85 °C). Obtain white metal Babbitt vendor certificate. | Lead Electrical & C&I Engineer / Process Safety Lead | LOPA & Bearing Vendor Review | `TT-3101`, `TT-3102`, `SIF-3101` | ⚠️ CONFLICT: Data Sheet / OM 75 °C vs SIS Matrix 85 °C |
| **ACT-HAZOP-45-03** | HZ-45-03 | Detail engineering and procurement of continuous $CS_2$ infrared gas detector `AT-4501` (alarm at 10% LEL) interlocked to switch `FN-4501` to high speed and cut solid PAX feeder. | Lead C&I Engineer | DCS Logic Specification & P&ID Revision | `AT-4501`, `FN-4501`, `TK-4501` | Mandatory New Safeguard Implementation |
| **ACT-HAZOP-45-06** | HZ-45-06 | Verify frother procurement contract and SDS against P&ID `RB-4410-PID-45-001` (DF-250) and Data Sheet `RB-4410-PS-TK4511` (MIBC) to validate Area 45 Zone 2 electrical classification. SDS `SDS_37286-64-9_polyglycol-ether-frother.pdf` confirms DF-250 is an alternative frother and explicitly *not specified for TK-4511*, verifying that P&ID text is an unaligned drawing note. | Chemical Metallurgist / Electrical Engineer | Hazardous Area Dossier Audit & P&ID Revision | `TK-4511`, `PP-4511A` | ⚠️ CONFLICT: P&ID DF-250 vs Data Sheet MIBC (FP 41 °C, Zone 2); SDS 37286-64-9 confirms alternative status |
| **ACT-HAZOP-61-01** | HZ-61-01 | Issue formal P&ID redline for `RB-4410-PID-61-001 Rev B` correcting stage-3 pump casing mechanical design pressure from 4.0 bar(g) to 40 bar(g). | Lead Mechanical Engineer | P&ID Rev C As-Built Issuance | `PP-6101A/B/C`, `PT-6103` | ⚠️ CONFLICT: P&ID 4.0 bar typographical error vs Data Sheet 40 bar |

## References & Sources
- Standard No. SDS_37286-64-9_polyglycol-ether-frother.pdf, *Safety Data Sheet Summary - Polyglycol ether frother (DF-250 type)*, Cymbal Copper Pty Ltd.
- Standard No. RB-4410-STD-HAZOP-001 Rev 1, *HAZOP Study - Concentrator (Selected Nodes)*, Cymbal Copper Pty Ltd.
- Standard No. RB-4410-STD-CE-001 Rev B, *SIS Cause & Effect Matrix*, Cymbal Copper Pty Ltd.
- Operating Manual No. RB-4410-OM-001 Rev 2, *Ridgeback Concentrator - Operating Manual*, Cymbal Copper Pty Ltd.
- Drawing No. RB-4410-PID-31-002 Rev B, *P&ID SAG Mill Hydrostatic Lift & Lube System*, Cymbal Copper Pty Ltd.
- Drawing No. RB-4410-PID-45-001 Rev B, *P&ID Reagents - Xanthate, Frother & Lime*, Cymbal Copper Pty Ltd.
- Drawing No. RB-4410-PID-61-001 Rev B, *P&ID Tailings Thickening & Pumping to TSF*, Cymbal Copper Pty Ltd.

## HAZOP Study Scope & Methodology
This study compiles the process hazard and operability findings codified in Site Engineering Standard `RB-4410-STD-HAZOP-001 Rev 1` (*HAZOP Study - Concentrator (Selected Nodes)*). It evaluates major comminution, chemical reagent preparation, and high-pressure overland slurry pumping systems at the Ridgeback Concentrator (RB-4410).

All recommendations are mandatory unless formally closed through management of change (MOC).

## Master HAZOP Worksheets (Selected Nodes)
| Node Ref | Node Description & Boundaries | Parameter / Guide Word | Deviation | Initiating Cause | Consequences & Severity | Existing Safeguards / IPLs | Mandatory HAZOP Recommendation | Target Asset / Tag |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **HZ-31-02** | SAG mill hydrostatic lift system (PP-3105A/B, TK-3105, lift supply headers to 2 x 2 trunnion pads) | Pressure / More | More pressure | HP lift pump dead-heads against closed valve | High-pressure hydraulic oil line rupture, high-pressure fluid injection, atomized oil spray fire at SAG mill drum | PSV-3105 set <= system design pressure 170 bar(g) | Confirm PSV-3105 set pressure on P&ID matches data sheet (Data Sheet PS-0032 Rev B & OM-001 Sec 12 set 160 bar(g) vs PID-31-002 Rev B set 180 bar(g)) | `PSV-3105`, `PP-3105A/B`, `TK-3105`, `ML-3101` |
| **HZ-31-04** | SAG mill trunnion bearings (Drive-end & Non-drive-end Babbitt shoes) | Temperature / More | More temperature | Loss of lube oil flow / cooling, heat exchanger fouling, bearing friction | Bearing wipe, white metal Babbitt liquefaction under 2,450 t charge load, journal gouging, 10–14 day unplanned concentrator outage | TT-3101/3102 TAHH trip via SIF-3101 (SIL 1) | Align TAHH setpoint between instrument data sheet (75 °C) and cause & effect matrix (85 °C) | `TT-3101`, `TT-3102`, `SIF-3101`, `ML-3101`, `CV-3101` |
| **HZ-45-03** | PAX xanthate mixing room (Enclosed Area 45 mixing bay enclosing TK-4501, TK-4502, and solid PAX charging) | Chemical Reaction / Other than | Other than (decomposition) | Wet/hot PAX (make-up water >40 °C), acid contamination, ambient moisture | Spontaneous decomposition into carbon disulfide ($CS_2$), toxic accumulation in room, flash fire, acute toxic exposure to operators | Extraction fan FN-4501 (24/7 continuous operation per PID Note 1) | Install CS2 gas detector AT-4501 (alarm 10 % LEL) interlocked to FN-4501 high speed and PAX feeder stop | `AT-4501`, `FN-4501`, `TK-4501`, `TK-4502` |
| **HZ-45-06** | Frother storage TK-4511 (Area 45 bulk frother vertical tank, bund, road tanker unloading) | Composition / Other than | Other than (wrong reagent) | Frother specification changed during procurement / operations | Incompatible hazardous-area classification (Zone 2 vs non-hazardous), vapor ignition, unrated electrical apparatus in bund | Area classified Zone 2 for MIBC | Confirm frother identity on P&ID (Polyglycol ether DF-250) vs data sheet (MIBC) and SDS | `TK-4511`, `PP-4511A`, `Area 45` |
| **HZ-61-01** | Tailings pumping to TSF (PP-6101A/B/C series booster train, common discharge header, 6.2 km overland line) | Pressure / More | More pressure | Blocked overland line, downstream valve closure at TSF, sanding | Overland pipeline rupture, stage-3 casing failure, violent high-pressure abrasive slurry spray, major environmental tailings release | PT-6103 PAHH trip SIF-6101 (SIL 2, 2oo3 voting at 38 bar(g)) | Confirm stage-3 casing design pressure on P&ID (Data Sheet PS-PP6101 Rev B states 40 bar(g) vs PID-61-001 Rev B typographical error 4.0 bar(g)) | `PT-6103`, `SIF-6101`, `PP-6101A/B/C` |

## Corporate Risk Matrix Calibration
Per `RB-4410-STD-HAZOP-001 Rev 1`, risks are evaluated on a 5x5 matrix crossing Likelihood (Rare to Almost Certain) with Severity (S1 to S5):

| Likelihood Category | Definition | S1 (Insignificant) | S2 (Minor) | S3 (Moderate) | S4 (Major) | S5 (Catastrophic) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Almost certain** | Occurs repeatedly per year | H | H | H | H | H |
| **Likely** | Occurs several times per facility life | M | H | H | H | H |
| **Possible** | Might occur once per facility life | M | M | H | H | H |
| **Unlikely** | Unlikely but possible | L | M | M | H | H |
| **Rare** | Practically impossible / unprecedented | L | L | M | M | H |

### Node Risk Allocations
- **Node HZ-31-02 (SAG Lift Overpressure):** Likelihood: *Unlikely*, Severity: *S4 (Major fire/equipment damage)* $\rightarrow$ **High Risk (H)** without verified PSV-3105 capacity/setting. Mitigated to **Medium (M)** with PSV set <= 170 bar(g).
- **Node HZ-31-04 (SAG Bearing Overtemperature):** Likelihood: *Possible*, Severity: *S4 (10–14 day plant outage)* $\rightarrow$ **High Risk (H)** if SIF-3101 setting permits Babbitt softening. Mitigated to **Medium (M)** upon setpoint alignment.
- **Node HZ-45-03 (PAX Mixing Room CS2 Accumulation):** Likelihood: *Possible*, Severity: *S4 (Toxic fatality / flash fire)* $\rightarrow$ **High Risk (H)** with ventilation alone. Mitigated to **Medium (M)** upon installing AT-4501 gas detector interlock.
- **Node HZ-45-06 (Frother Reagent Mismatch):** Likelihood: *Unlikely*, Severity: *S3 (Flammable area de-rating)* $\rightarrow$ **Medium Risk (M)**. Mitigated to **Low (L)** upon chemical verification.
- **Node HZ-61-01 (Tailings Overpressure Rupture):** Likelihood: *Unlikely*, Severity: *S5 (Catastrophic environmental dam/corridor release)* $\rightarrow$ **High Risk (H)** if casing is under-rated. Mitigated to **Medium (M)** with SIL 2 trip and 40 bar(g) casing confirmation.
