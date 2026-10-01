---
type: Operating Procedure
title: SAG Mill ML-3101 Startup, Feed Ramp, Shutdown, Grind-out & Relining Procedure
description: Operating procedures for SAG Mill ML-3101 startup, feed ramping, locked
  charge inspection, grind-out shutdown, 33 kV and cycloconverter isolation, PT-3104
  bleed-down, shell chocking, and relining safety per RB-4410-OM-001 Rev 2 and RB-4410-SG-005
  Rev 3.
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/procedures/sag-mill-operating-procedures.md
tags:
- 33-kv
- area 31
- chocking
- cycloconverter
- feed-ramp
- gmd
- grind-out
- grinding
- isolation
- liner-handler
- locked-charge
- ml-3101
- operating-procedure
- procedures
- pt-3104
- rb-4410
- rb-4410-om-001
- rb-4410-sg-005
- relining
- sag-mill
- sif-3101
- sif-3102
- spotter
- startup-shutdown
sources:
- id: src-1
  resource: corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR
    OPERATING MANUAL_R2.pdf
  title: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf
- id: src-2
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-ML3101_SAG MILL PROCESS DATA SHEET_B.pdf
  title: RB-4410-PS-ML3101_SAG MILL PROCESS DATA SHEET_B.pdf
- id: src-3
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-31-001_P&ID SAG MILL ML-3101_B.pdf
  title: RB-4410-PID-31-001_P&ID SAG MILL ML-3101_B.pdf
- id: src-4
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-31-002_P&ID SAG MILL HYDROSTATIC LIFT &
    LUBE SYSTEM_B.pdf
  title: RB-4410-PID-31-002_P&ID SAG MILL HYDROSTATIC LIFT & LUBE SYSTEM_B.pdf
- id: src-5
  resource: corpora/copper-concentrator/raw/standards/RB-4410-SG-005_GRINDING MILL ISOLATION AND ENTRY
    STANDARD_R3.pdf
  title: RB-4410-SG-005_GRINDING MILL ISOLATION AND ENTRY STANDARD_R3.pdf
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T18:10:32Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T18:10:32Z'
- by: process:okf-validation-suite
  at: '2026-09-30T18:10:32Z'
status: stable
entity_metadata:
  ramp_duration_min: 15
  voltage_kv: 33
  locked_charge_inspection_hours: 4
  sif_functions:
  - SIF-3101
  - SIF-3102
  tag: ML-3101
  initial_speed_pct_critical: 70
  isolation_standard: RB-4410-SG-005 Rev 3
  grindout_duration_min: 10 - 15
  reline_duration_hours: 72 - 96
  mill_power_target_mw: 18 - 21
  mill_target_solids_pct: 75
  initial_feed_pct: 50
  liner_handler_requirements:
  - dedicated spotter
  - exclusion zone
  pt_3104_bleed_target_barg: 0
  zero_energy_verification: attempted start
  shell_chocking_mandatory: true
---

> ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
> - **LOCKED (FROZEN) CHARGE SAFETY PROTOCOL:** Following any SAG mill stoppage exceeding **4 hours**, fine ore and slurry consolidate into a dense cemented mass ("locked" or "frozen" charge) adhering to the mill shell. **NEVER start the SAG mill at full speed with a frozen charge.** Starting at full rotational speed causes the frozen charge to be carried upward to the top of the 12.2 m diameter shell and drop in a single multi-hundred-tonne catastrophic lump, causing catastrophic shell deformation, liner bolt shearing, trunnion bearing cracking, or severe structural failure. Operators must engage the Gearless Motor Drive (GMD) **inching mode (0.1 rpm)** to gently rotate the shell and visually monitor charge slumping/detachment before attempting main motor startup.
> - **HYDROSTATIC LIFT & LUBE OIL INTERLOCKS (SIF-3101 & SIF-3102):** The 2,450 t mill drum must be hydraulically floated on high-pressure oil before starting. Permissive interlock `SIF-3102` prohibits mill startup if hydrostatic lift pressure transmitter `PT-3104` is below **90 bar(g)** (trips drive on `PALL 70 bar(g)`). Trunnion bearing RTDs `TT-3101` (drive-end) and `TT-3102` (non-drive-end) must indicate below **70 °C** (`TAH 70 °C`), with `TAHH 75 °C` executing an immediate emergency trip via Safety Instrumented Function `SIF-3101` (SIL 1).
> - **33 kV & CYCLOCONVERTER ZERO-ENERGY ISOLATION (RB-4410-SG-005 Rev 3):** During mill entry, liner inspection, or shell relining, the GMD must be positively isolated at both the **33 kV feeder circuit breaker** and the **cycloconverter**, and zero-energy state must be verified by an attempted start per site standard `RB-4410-SG-005 Rev 3`.
> - **LUBE & HYDROSTATIC LIFT DEPRESSURIZATION (PT-3104 BLEED):** Lube and hydrostatic lift systems must be isolated, and pressure transmitter `PT-3104` must be bled down to **0 bar(g)** prior to personnel entry.
> - **SHELL CHOCKING & INCHING DRIVE LOCKOUT:** The mill shell must be mechanically chocked before any person enters the drum to prevent gravitational roll-back or rotation. The inching drive must remain strictly locked out during entry.
> - **CONFINED SPACE ENTRY & ADJACENT FLOTATION CS2 MONITORING:** A Confined Space Entry permit and atmospheric gas testing are mandatory prior to entry. While no internal CS2 source exists in the grinding circuit, the flotation area is adjacent and poses a potential toxic and flammable $CS_2$ gas migration hazard.
> - **LINER HANDLER EXCLUSION ZONE & SPOTTER:** The mechanical liner handler (2.5 t manipulator) must NEVER be operated inside the mill drum while the mill is on inching drive. Operating the liner handler requires a dedicated spotter and an enforced exclusion zone.
> - **CYCLONE FEED PUMP START TIMING & HOPPER OVERFLOW:** Operating personnel must start cyclone feed pumps `PP-3201A` and `PP-3201B` BEFORE SAG and ball mill slurry discharge reaches the common pump hopper. Failure to establish pump flow causes instantaneous hopper overfilling, basement flooding, and severe pump cavitation upon subsequent startup.
> - **33 kV ELECTRICAL ISOLATION & RELINING LOCKOUT (RB-4410-SG-005):** During mill entry, liner inspection, or shell relining, the GMD must be isolated at the **33 kV feeder** and personal safety locks applied per site standard `RB-4410-SG-005`. The mechanical liner handler must NEVER be operated inside the mill drum while the mill is on inching drive.

## Purpose & Scope
This standard operating procedure governs the safe startup, feed ramping, normal shutdown, grind-out, electrical isolation, and relining maintenance sequence for the 12.2 m × 6.7 m Gearless Motor Drive SAG Mill `ML-3101` in Area 31, per Operating Manual `RB-4410-OM-001 Rev 2` and Site Standard `RB-4410-SG-005 Rev 3`.

## Step-by-Step Operating Procedures
### 1. Pre-Start Checks & Permissive Verification
1. Verify lubrication reservoir `TK-3105` oil level (ISO VG 460) and confirm immersion heaters and coolers are operational.
2. Start high-pressure hydrostatic lift pumps `PP-3105A` and `PP-3105B`.
3. Confirm high-pressure lift oil pressure on `PT-3104` rises above **90 bar(g)**. Verify that start permissive `SIF-3102` clears in the DCS.
4. Verify bearing temperature transmitters `TT-3101` (drive-end) and `TT-3102` (non-drive-end) indicate healthy signals and are below `TAH 70 °C`.
5. Verify downstream discharge circuits: vibrating screen `SC-3101`, pebble recycle conveyor `CV-3101`, and pebble crusher `CR-3102` are ready or running.
6. Verify cyclone feed pumps `PP-3201A` and `PP-3201B` are running before slurry enters the common sump.

### 2. Locked Charge Inspection (Stoppages > 4 Hours)
1. If the mill has been stopped for longer than **4 hours**, a locked charge inspection is mandatory.
2. Engage the GMD in **inching mode (0.1 rpm)**.
3. Post an operator at the mill inspection door / feed chute viewing window with a two-way radio to the control room.
4. Slowly rotate the mill drum on inching drive while observing the grinding charge.
5. Confirm that the ore and ball charge slides, slumps, or detaches smoothly from the shell lifters.
6. If the charge remains locked to the shell as it ascends towards top dead center:
   - Immediately STOP inching drive.
   - Do NOT start main drive.
   - Follow site locked charge detachment procedures (controlled reverse inching or hydraulic water soaking).

### 3. SAG Mill Startup & Feed Ramp Sequence
1. Disengage inching mode and secure inching clutch/brake interlocks.
2. Clear the mill perimeter and sound the audible mill startup siren.
3. Start the SAG mill main GMD motor at **70 % critical speed**.
4. Open the feed chute process water valve and initiate mill feed water ratio controller `FIC-3103`, establishing water flow ahead of ore feed.
5. Start stockpile reclaim feeders `FE-3101A/B/C` and feed conveyor `CV-3101`.
6. Introduce fresh ore feed at **50 % of design target** (~1,344 t/h).
7. Ramp ore feed rate smoothly via weight controller `WIC-3101` from 50 % to the 100 % target (**2,688 t/h**) over **15 minutes**.
8. Ensure `FIC-3103` modulates water flow in ratio to ore feed to maintain target belly slurry density of **75 % solids w/w**.
9. Adjust mill rotational speed within 60–80 % critical speed to regulate power draw within the **18 to 21 MW** operating target window.

### 4. Controlled Shutdown & Grind-Out Sequence
1. Stop stockpile reclaim feeders `FE-3101A/B/C` to halt fresh ore feed to conveyor `CV-3101`.
2. Continue running the SAG mill with feed water addition for **10 to 15 minutes** (grind-out cycle).
   - This empties the mill pulp and rock charge, drastically reducing charge weight and preventing charge locking during the outage.
3. Stop process feed water to the feed chute.
4. Stop the SAG mill main GMD motor.
5. Maintain hydrostatic lift and lube pumps `PP-3105A/B` running for 20 minutes post-stoppage to allow trunnion journal cooling.
6. Stop pebble crushing circuit `CR-3102` and screen `SC-3101` once pebble recycle Stream S-305 clears.
7. Flush cyclone feed pump hopper and flush pumps `PP-3201A/B` with clean water before stopping.

### 5. Relining Maintenance & Mill Isolation Sequence (RB-4410-SG-005 Rev 3)
1. **High-Voltage Electrical Lockout & Zero-Energy Verification:**
   - Isolate the GMD at the **33 kV feeder circuit breaker** and the **cycloconverter**.
   - Apply personal safety padlocks and danger tags per site standard `RB-4410-SG-005 Rev 3`.
   - Perform an attempted start (local and remote) to positively verify zero electrical energy.
2. **Hydraulic & Lube System Isolation:**
   - Isolate lube and hydrostatic lift systems (`PP-3105A/B`, `TK-3105`).
   - Bleed hydrostatic lift pressure transmitter `PT-3104` down to **0 bar(g)**.
3. **Mechanical Shell Chocking & Inching Lockout:**
   - Engage mechanical brake caliper clamping system.
   - Physically **chock the mill shell** before any person enters the drum to prevent gravitational roll-back.
   - Inching drive must remain strictly locked out throughout personnel entry.
4. **Confined Space Entry Permit & Atmospheric Gas Testing:**
   - Issue Confined Space Entry (CSE) permit.
   - Perform continuous atmospheric testing for oxygen deficiency and toxic/combustible gases. Note: Although no internal $CS_2$ source is expected in the SAG mill, the flotation area is adjacent and poses potential toxic and flammable $CS_2$ gas migration risk.
5. **Relining Machine Manipulator Safety:**
   - Rig and position the 2.5 t capacity mill relining machine.
   - **CRITICAL SAFETY RULE:** The liner handler / relining machine must NEVER be operated inside the mill drum while the mill is on inching drive.
   - Liner handler operation requires an enforced exclusion zone and a dedicated spotter.
   - Conduct liner replacement (typical SAG reline duration: **72 to 96 hours**).
6. **Re-Commissioning Checks:**
   - Upon relining completion, remove tools, ensure shell chocks are removed and drum is clear of personnel.
   - Remove 33 kV and cycloconverter personal locks, restore lubrication system, and perform locked charge / pre-start checks prior to re-commissioning.

## Procedural Controls & Operating Targets Matrix
| Parameter / Step | Target / Setting | Governing Instrument | Process Safety / Operational Significance |
| :--- | :--- | :--- | :--- |
| **Lift Oil Pressure Permissive** | > 90 bar(g) | PT-3104 | SIF-3102 start permissive; protects trunnion Babbitt |
| **Bearing Temperature Permissive** | < 70 °C | TT-3101 / TT-3102 | Pre-start check; TAHH 75 °C trips SAG mill (SIF-3101 SIL 1) |
| **Locked Charge Check Threshold** | Stop > 4 hours | GMD Inching (0.1 rpm) | Visual verification of charge slumping; prevents shell destruction |
| **Initial Start Speed** | 70 % critical speed | GMD Drive Panel | Smooth acceleration without excessive torque surge |
| **Initial Feed Rate** | 50 % target (~1,344 t/h) | WIC-3101 | Prevents slurry pooling and liner impact |
| **Feed Ramp Duration** | 15 minutes | WIC-3101 | Smooth transition to full 2,688 t/h production |
| **Mill Operating Power** | 18 – 21 MW | JI-3101 / Speed / Feed | Optimal tumbling grinding kinetics |
| **Mill Belly Slurry Density** | 75 % solids w/w | FIC-3103 water ratio | Prevents pooling (<72%) or lifter impact damage (>78%) |
| **Grind-out Duration** | 10 – 15 minutes | Timer / Operations | Evacuates charge, reduces relining weight, avoids locked charge |
| **Isolation Standard** | RB-4410-SG-005 | 33 kV Feeder Breaker | Zero-energy state during confined space relining |
| **Typical Reline Duration** | 72 – 96 hours | Maintenance Schedule | Periodic replacement of 50 mm Cr-Mo shell lifters |
| **Electrical Isolation Points** | 33 kV Feeder & Cycloconverter | 33 kV Feeder Breaker / Drive | Zero-energy state verified by attempted start per RB-4410-SG-005 |
| **Lift Depressurization Target** | 0 bar(g) | PT-3104 | Complete hydraulic depressurization per RB-4410-SG-005 |
| **Mechanical Shell Securing** | Mandatory Chocking | Mechanical Chocks / Inching LOTO | Prevents rotational roll-back; inching locked out during entry |
| **Confined Space Gas Testing** | CSE Permit & Gas Test | Portable Multi-Gas Detector | Checks O2, flammables, toxics (adjacent flotation CS2 risk) |
| **Liner Handler Safeguards** | Dedicated Spotter & Exclusion Zone | Safety Marshall / Exclusion Barrier | Prevents crush/struck-by injuries from 2.5 t manipulator |

## References & Sources
[^1]: Operating Manual No. RB-4410-OM-001 Rev 2, Section 4, 5, 6, 7 & 12, *Ridgeback Concentrator - Operating Manual*, Cymbal Copper Pty Ltd.
[^2]: Process Data Sheet No. RB-4410-PS-ML3101 Rev B, *SAG Mill Process Data Sheet*, Cymbal Copper Pty Ltd.
[^3]: Piping & Instrumentation Diagram RB-4410-PID-31-001 Rev B, *SAG Mill ML-3101*, Cymbal Copper Pty Ltd.
[^4]: Piping & Instrumentation Diagram RB-4410-PID-31-002 Rev B, *SAG Mill Hydrostatic Lift & Lube System*, Cymbal Copper Pty Ltd.
[^5]: Site Standard No. RB-4410-SG-005 Rev 3, *Site Standard - Grinding Mill Isolation and Entry*, Cymbal Copper Pty Ltd.
