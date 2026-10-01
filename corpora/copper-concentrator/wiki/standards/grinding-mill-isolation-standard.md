---
type: Site Standard
title: Site Standard - Grinding Mill Isolation and Entry (RB-4410-SG-005 Rev 3)
description: Site Standard RB-4410-SG-005 Rev 3 defining mandatory protocols for grinding
  mill 33 kV and cycloconverter isolation, PT-3104 bleed-down, shell chocking, confined
  space entry, and liner handler spotter safety.
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/standards/grinding-mill-isolation-standard.md
tags:
- 33-kv
- ball-mill
- chocking
- confined-space
- cs2
- cycloconverter
- entry
- gmd
- isolation
- liner-handler
- loto
- ml-3101
- ml-3201
- pt-3104
- rb-4410
- rb-4410-sg-005
- relining
- sag-mill
- site-standard
- standard
sources:
- id: src-1
  resource: corpora/copper-concentrator/raw/standards/RB-4410-SG-005_GRINDING MILL ISOLATION AND ENTRY
    STANDARD_R3.pdf
  title: RB-4410-SG-005_GRINDING MILL ISOLATION AND ENTRY STANDARD_R3.pdf
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T18:07:47Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T18:07:47Z'
- by: process:okf-validation-suite
  at: '2026-09-30T18:07:47Z'
status: stable
entity_metadata:
  gas_test_hazard: CS2 migration from adjacent flotation area
  zero_energy_verification: attempted start
  title: Site Standard - Grinding Mill Isolation and Entry
  pressure_bleed_tag: PT-3104
  plant_code: RB-4410
  liner_handler_requirements:
  - dedicated spotter
  - exclusion zone
  isolation_points:
  - 33 kV feeder
  - cycloconverter
  - lube and hydrostatic lift systems
  pressure_bleed_target_barg: 0
  equipment_tags:
  - ML-3101
  - ML-3201
  - PP-3105A
  - PP-3105B
  - TK-3105
  revision: Rev 3
  inching_lockout_during_entry: true
  shell_chocking_mandatory: true
  document_number: RB-4410-SG-005
  document_type: Site Standard
---

> ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
> - **MANDATORY ZERO-ENERGY VERIFICATION (33 kV & CYCLOCONVERTER):** Prior to any mill entry or relining maintenance, the Gearless Motor Drive (GMD) must be isolated at both the **33 kV feeder circuit breaker** and the **cycloconverter drive**. Zero-energy state must be positively verified via an attempted local and remote start test before personnel approach the machine.
> - **HYDROSTATIC LIFT SYSTEM DEPRESSURIZATION & BLEEDING (PT-3104):** Both the lubrication and high-pressure hydrostatic lift systems must be positively isolated, and pressure transmitter `PT-3104` must be manually and instrumentally bled down to **0 bar(g)**. Unrelieved hydraulic pressure can cause residual jacking forces or unexpected oil injection hazards.
> - **MECHANICAL SHELL CHOCKING & INCHING DRIVE LOCKOUT:** The mill shell must be physically chocked with engineered mechanical chocks before any person enters the drum to prevent accidental gravitational rotation due to asymmetric charge or liner mass. The auxiliary inching drive must remain strictly locked out (LOTO) throughout the entire duration of personnel entry.
> - **CONFINED SPACE ENTRY & ADJACENT FLOTATION CS2 INGRESS HAZARD:** A formal Confined Space Entry (CSE) permit and continuous atmospheric gas testing are mandatory prior to and during mill entry. Although no internal carbon disulfide ($CS_2$) source is expected within the grinding mill, the flotation area is adjacent to Area 31 and poses a serious toxic and explosive vapor migration risk from potassium amyl xanthate (PAX) decomposition.
> - **LINER HANDLER EXCLUSION ZONE & DEDICATED SPOTTER:** Operation of the mechanical liner handler (2.5 t manipulator) inside the mill drum requires an enforced exclusion zone and a dedicated, competent spotter in continuous communication with the machine operator.

## Standard Metadata
- **Standard Title:** Site Standard - Grinding Mill Isolation and Entry
- **Standard Document Number:** RB-4410-SG-005
- **Revision:** Rev 3
- **Plant / Project:** Ridgeback Concentrator - Project RB-4410
- **Governing Entity:** Cymbal Copper Pty Ltd
- **Source Document:** `corpora/copper-concentrator/raw/standards/RB-4410-SG-005_GRINDING MILL ISOLATION AND ENTRY STANDARD_R3.pdf`
- **Applicable Units & Equipment:** Area 31 (SAG Mill `ML-3101`), Area 32 (Ball Mill `ML-3201`), Area 43 (Regrind Mill `ML-4201`), HP Lift Pumps `PP-3105A/B`, Lube Reservoir `TK-3105`

## Mandatory Isolation & Entry Requirements
| Step / Safeguard | System / Equipment | Requirement & Mandatory Action | Process Safety / Engineering Significance |
| :--- | :--- | :--- | :--- |
| **1. High-Voltage Electrical Isolation** | GMD 33 kV Feeder & Cycloconverter | Isolate GMD at 33 kV feeder breaker and cycloconverter; verify zero energy by attempted start | Prevents inadvertent motor energization; eliminates arc flash and rotational hazards |
| **2. Hydraulic & Lube System Isolation** | Hydrostatic Lift & Lube Units (PP-3105A/B, TK-3105) | Isolate lube and hydrostatic lift systems; bleed lift pressure `PT-3104` to 0 bar(g) | Eliminates trapped hydraulic energy and unwanted journal jacking during entry |
| **3. Mechanical Shell Chocking** | SAG Mill `ML-3101` / Ball Mill Shell | Chock the mill shell before any person enters; auxiliary inching drive locked out during entry | Prevents catastrophic gravitational roll-back/rotation caused by unbalanced charge or liners |
| **4. Confined-Space Entry & Gas Testing** | Internal Drum Atmosphere | Issue Confined-Space Entry (CSE) permit; perform continuous atmospheric gas testing | Monitors oxygen levels, toxic gases, and potential $CS_2$ vapor migration from adjacent flotation area |
| **5. Liner Handler Safe Operation** | Relining Machine Manipulator (2.5 t) | Enforce dedicated spotter and exclusion zone around liner handler during all relining movements | Prevents crush, pinch, and struck-by injuries from suspended 50 mm Cr-Mo liner lifters |

## Operational & Maintenance Interfaces
- **SAG Mill Relining Procedure (`procedures/sag-mill-operating-procedures.md`):** Relining maintenance requires mill drum isolation adhering strictly to this standard during the 72 to 96-hour reline outage.
- **Grinding Circuit Hazard Profile (`hazards/comminution-slurry-hazards.md`):** Identifies trapped rotational inertia, high-pressure oil injection, and confined space gas hazards governed by this standard.

## References & Sources
[^1]: Site Standard No. RB-4410-SG-005 Rev 3, *Site Standard - Grinding Mill Isolation and Entry*, Cymbal Copper Pty Ltd.
