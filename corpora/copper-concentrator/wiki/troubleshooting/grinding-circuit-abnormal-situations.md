---
type: Troubleshooting Guide
title: Grinding Circuit Abnormal Situations & Corrective Action Guide
description: Abnormal situation handling and diagnostic pathways for SAG bearing overtemperature,
  locked charge, cyclone roping, hopper sanding, and tailings line overpressure per
  RB-4410-OM-001 Rev 2.
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/troubleshooting/grinding-circuit-abnormal-situations.md
tags:
- abnormal-situations
- bearing-temperature
- cyclone-roping
- diagnostics
- grinding
- hopper-overflow
- locked-charge
- operating-manual
- pipeline-flushing
- rb-4410
- rb-4410-om-001
- sif-3101
- sif-6101
- tailings-pumping
- troubleshooting
sources:
- id: src-1
  resource: corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR
    OPERATING MANUAL_R2.pdf
  title: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf
- id: src-2
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-0032_PRESSURE INSTRUMENT & RELIEF
    VALVE PROCESS DATA SHEET_B.pdf
  title: RB-4410-PS-0032_PRESSURE INSTRUMENT & RELIEF VALVE PROCESS DATA SHEET_B.pdf
- id: src-3
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-CY3201_CYCLONE CLUSTER PROCESS DATA
    SHEET_B.pdf
  title: RB-4410-PS-CY3201_CYCLONE CLUSTER PROCESS DATA SHEET_B.pdf
- id: src-4
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-PP6101_TAILINGS PUMPS PROCESS DATA
    SHEET_B.pdf
  title: RB-4410-PS-PP6101_TAILINGS PUMPS PROCESS DATA SHEET_B.pdf
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T17:55:49Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T17:55:49Z'
- by: process:okf-validation-suite
  at: '2026-09-30T17:55:49Z'
status: stable
entity_metadata:
  tailings_pahh_barg: 38
  cyclone_feed_density_pds_pct: 60
  locked_charge_limit_hours: 4
  sif_functions:
  - SIF-3101
  - SIF-3102
  - SIF-6101
  bearing_tah_c: 70
  plant_areas:
  - Area 31
  - Area 32
  - Area 61
  tailings_pah_barg: 36
  discrepancy_feed_density: true
  cyclone_feed_density_om_pct: 65
  bearing_tahh_c: 75
---

> ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
> - **FROZEN / LOCKED CHARGE IMMEDIATE RESPONSE:** Never attempt to restart a tripped or shut down SAG mill at full speed if the stoppage has exceeded 4 hours. Fine ore compaction can cement the ball and ore charge to the shell liners. Full-speed startup causes the charge to detach near top dead center (12 o'clock position), dropping 2,450 tonnes dynamically onto the bottom liners, destroying shell liners, cracking trunnion journals, or catastrophically shearing shell bolts.
> - **TRUNNION OVERTEMPERATURE TRIP (SIF-3101 SIL 1):** If `TT-3101` or `TT-3102` reaches `TAH 70 °C`, inspect lube oil cooling water and oil flow immediately. At `TAHH 75 °C`, `SIF-3101` (SIL 1) initiates an unbypassable hard trip of the 22,000 kW GMD ring motor to avert Babbitt wiping.
> - **CYCLONE ROPING & DOWNSTREAM RECOVERY LOSS:** Operating cyclone cluster `CY-3201` at feed densities above the design target (⚠️ CONFLICT: 65 % solids w/w in OM-001 vs 60.0 % solids in PS-CY3201 / PFD-001) or with choked apex nozzles forces coarse unclassified ore (+150 µm) into overflow Stream S-324, sanding rougher flotation cells and drastically lowering chalcopyrite recovery.
> - **MANDATORY POST-TRIP TAILINGS PIPELINE FLUSHING:** If 3-stage tailings pumps `PP-6101A/B/C` trip on stage-3 overpressure `PAHH 38 bar(g)` (`SIF-6101 SIL 2`), operations must immediately inject clean flush water into the 6.2 km overland pipeline before attempting a restart. Unflushed dense slurry (62 % solids w/w, SG 1.652) will consolidate and permanently sand the pipeline corridor.

## Scope & Diagnostic Overview
This troubleshooting procedure defines the diagnostic pathways, root cause analyses, and immediate operational mitigations for primary grinding, classification, slurry pumping, and tailings transport abnormal situations across Areas 31, 32, and 61, per Section 7 and Section 11 of Operating Manual `RB-4410-OM-001 Rev 2`.

## Grinding & Pumping Abnormal Situation Response Matrix
| Symptom / Alarm | Direct Operational Indicator | Root Cause Analysis | Immediate Operator Response | Secondary Escalation / Engineering Check |
| :--- | :--- | :--- | :--- | :--- |
| **SAG bearing temperature high** | `TT-3101` or `TT-3102` alarms at `TAH 70 °C` (trip threshold: `TAHH 75 °C`) | 1. Lube oil cooler water supply failure or plate fouling.<br>2. HP lift pump failure or low lube flow.<br>3. Severe trunnion pad misalignment or oil viscosity degradation. | 1. Check lube skid oil pressure and flow indicators.<br>2. Switch to standby oil cooler and check cooling water valve position.<br>3. Verify lube oil reservoir `TK-3105` temperature.<br>4. If temperature continues rising towards 75 °C, prepare for executive trip via `SIF-3101` (SIL 1). | If tripped on `TAHH 75 °C`, engage 33 kV LOTO, remove bearing housing inspection covers, and inspect white metal Babbitt for wiping or journal scoring before restart. |
| **Locked (frozen) charge** | High starting torque, abnormal GMD power spike `JI-3101`, no cascading sound | Mill stopped longer than 4 hours with fine ore slurry and grinding balls settling into compacted solid mass. | 1. **NEVER start at full rotational speed.**<br>2. Switch GMD to inching mode (0.1 rpm).<br>3. Inch mill drum in small increments while watching charge through feed inspection port.<br>4. If charge does not detach, stop inching. | Apply controlled reverse inching or introduce low-pressure water soak to soften compacted fines before re-attempting inching. |
| **Cyclone roping** | Dense rope-like underflow discharge, feed pressure surging on `PT-3201`, coarse spillage in flotation feed | 1. Feed slurry density too high (> 65 % solids w/w on `DT-3201`).<br>2. Apex nozzle diameter worn or obstructed by foreign debris.<br>3. Pump delivery rate insufficient or feed pressure < 100 kPa. | 1. Add dilution water immediately to cyclone feed sump.<br>2. Check feed pump `PP-3201A/B` speed and manifold pressure `PT-3201`.<br>3. Reduce SAG mill fresh ore feed rate `WIC-3101` until cyclone feed density returns to target.<br>4. Switch to standby hydrocyclones in cluster `CY-3201`. | Inspect apex liners and vortex finders for wear; re-calibrate nuclear density transmitter `DT-3201`. |
| **Hopper overflow / sanding** | Sump level rising rapidly on `LIC-3201`, slurry spilling over sump lip onto basement floor | 1. Duty cyclone feed pumps (`PP-3201A/B`) under capacity or impeller severely worn.<br>2. VFD speed limitation or drive trip.<br>3. Circulating load spike exceeding 300 %. | 1. Immediately reduce fresh ore feed rate on SAG feed conveyor `CV-3101`.<br>2. Start standby cyclone feed pump `PP-3201C`.<br>3. Increase pump speed on running duty pumps via `LIC-3201` manual trim.<br>4. Cut sump dilution water if level is nearing overflow lip. | Clear floor spillage via sump evacuation pumps; inspect wet-end pump liners for excessive cavitation wear. |
| **Tailings overland pipeline overpressure / trip** | `PT-6103` alarms at `PAH 36 bar(g)` and trips pumps at `PAHH 38 bar(g)` via `SIF-6101` | 1. Slurry compaction / scaling restriction along 6.2 km pipeline.<br>2. High tailings underflow density (> 62 % solids w/w).<br>3. Downstream valve at TSF closed or partially throttled. | 1. Confirm simultaneous executive trip of `PP-6101A/B/C` by `SIF-6101` (SIL 2).<br>2. **MANDATORY:** Initiate automated emergency flush water sequence immediately to flush the 6.2 km pipeline to the TSF before solids settle.<br>3. Do NOT restart slurry pumps until pipeline is fully water-flushed. | 1. Report pipeline pressure excursion to Engineer of Record for the TSF.<br>2. Inspect pressure trend and line wall thickness per `RB-4410-STD-TSF-002`. |
| **PAX mixing room toxic gas / ventilation failure** | Extraction fan `FN-4501` run signal lost; $CS_2$ infrared detector alarm | 1. Fan motor trip or drive belt failure.<br>2. Accelerated thermal decomposition of PAX due to mix water temperature > 40 °C. | 1. Immediately evacuate PAX mixing room.<br>2. Prohibit personnel entry; barricade room.<br>3. Halt PAX pellet charging into `TK-4501`.<br>4. Restart standby extraction fan or reset `FN-4501` breaker from outside enclosure. | Confirm zero flammable/toxic atmosphere with calibrated multi-gas detector before re-entering mixing room. |

## References & Sources
[^1]: Operating Manual No. RB-4410-OM-001 Rev 2, Section 7, 8 & 11, *Ridgeback Concentrator - Operating Manual*, Cymbal Copper Pty Ltd.
[^2]: Process Data Sheet No. RB-4410-PS-0032 Rev B, *Pressure Instrument & Relief Valve Process Data Sheet*, Cymbal Copper Pty Ltd.
[^3]: Process Data Sheet No. RB-4410-PS-CY3201 Rev B, *Cyclone Cluster Process Data Sheet*, Cymbal Copper Pty Ltd.
[^4]: Process Data Sheet No. RB-4410-PS-PP6101 Rev B, *Tailings Pumps Process Data Sheet*, Cymbal Copper Pty Ltd.
