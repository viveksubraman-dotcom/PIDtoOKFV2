---
type: Unit Overview
title: 'Area 2100 / 3100 / 3200: Crushing and Grinding Circuit'
description: Process unit overview, circuit topology, equipment roster, stream mass
  balance, primary crushing P&ID (Area 21), SAG Mill P&ID (PID-31-001), SAG Mill lift
  & lube system (PID-31-002, SIF-3102, PSV-3105 conflict), and Ball Mill & Cyclone
  Cluster P&ID (PID-32-001, ML-3201, CY-3201, PP-3201A/B/C, LIC-3201, DT-3201 nuclear
  permit).
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/units/crushing-and-grinding.md
tags:
- abnormal-situations
- area 21
- area 2100
- area 31
- area 3100
- area 3200
- ball-mill
- coarse-ore-stockpile
- comminution
- cone-crusher
- copper-concentrator
- cr-2101
- cr-3102
- crusher
- crushing
- cv-2101
- cv-3101
- cy-3201
- cyclone-cluster
- dt-3201
- fe-3101a
- fic-3103
- grind-out
- grinding
- ji-3101
- lic-3201
- locked-charge
- mass-balance
- ml-3101
- ml-3201
- operating-manual
- operating-targets
- pebble-crusher
- pp-3105a
- pp-3105b
- pp-3201a
- pp-3201b
- pp-3201c
- primary-crushing
- psv-3105
- pt-3104
- pt-3201
- radiation-permit
- rb-4410
- rb-4410-om-001
- rb-4410-sg-005
- relining
- sag-mill
- sc-3101
- sif-3101
- sif-3102
- slurry-pump
- st-2101
- tk-3105
- tt-3101
- tt-3102
- tt-3201
- tt-3202
- unit
- vd-2101
- wic-3101
- wit-2102
- wt-2101
sources:
- id: src-1
  resource: corpora/copper-concentrator/raw/pfd/RB-4410-PFD-001_PROCESS FLOW DIAGRAM CRUSHING AND GRINDING_B.pdf
  title: RB-4410-PFD-001_PROCESS FLOW DIAGRAM CRUSHING AND GRINDING_B.pdf
- id: src-2
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-0032_PRESSURE INSTRUMENT & RELIEF
    VALVE PROCESS DATA SHEET_B.pdf
  title: RB-4410-PS-0032_PRESSURE INSTRUMENT & RELIEF VALVE PROCESS DATA SHEET_B.pdf
- id: src-3
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-0033_ANALYSER, DENSITY & LEVEL INSTRUMENT
    DATA SHEET_B.pdf
  title: RB-4410-PS-0033_ANALYSER, DENSITY & LEVEL INSTRUMENT DATA SHEET_B.pdf
- id: src-4
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-0034_TEMPERATURE INSTRUMENT PROCESS
    DATA SHEET_B.pdf
  title: RB-4410-PS-0034_TEMPERATURE INSTRUMENT PROCESS DATA SHEET_B.pdf
- id: src-5
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-CR2101_PRIMARY GYRATORY CRUSHER PROCESS
    DATA SHEET_B.pdf
  title: RB-4410-PS-CR2101_PRIMARY GYRATORY CRUSHER PROCESS DATA SHEET_B.pdf
- id: src-6
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-CR3102_PEBBLE CRUSHER PROCESS DATA
    SHEET_B.pdf
  title: RB-4410-PS-CR3102_PEBBLE CRUSHER PROCESS DATA SHEET_B.pdf
- id: src-7
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-CY3201_CYCLONE CLUSTER PROCESS DATA
    SHEET_B.pdf
  title: RB-4410-PS-CY3201_CYCLONE CLUSTER PROCESS DATA SHEET_B.pdf
- id: src-8
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-ML3101_SAG MILL PROCESS DATA SHEET_B.pdf
  title: RB-4410-PS-ML3101_SAG MILL PROCESS DATA SHEET_B.pdf
- id: src-9
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-ML3201_BALL MILL PROCESS DATA SHEET_B.pdf
  title: RB-4410-PS-ML3201_BALL MILL PROCESS DATA SHEET_B.pdf
- id: src-10
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-PP3201_CYCLONE FEED PUMP PROCESS
    DATA SHEET_B.pdf
  title: RB-4410-PS-PP3201_CYCLONE FEED PUMP PROCESS DATA SHEET_B.pdf
- id: src-11
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-21-001_P&ID PRIMARY CRUSHING_B.pdf
  title: RB-4410-PID-21-001_P&ID PRIMARY CRUSHING_B.pdf
- id: src-12
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-31-001_P&ID SAG MILL ML-3101_B.pdf
  title: RB-4410-PID-31-001_P&ID SAG MILL ML-3101_B.pdf
- id: src-13
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-31-002_P&ID SAG MILL HYDROSTATIC LIFT &
    LUBE SYSTEM_B.pdf
  title: RB-4410-PID-31-002_P&ID SAG MILL HYDROSTATIC LIFT & LUBE SYSTEM_B.pdf
- id: src-14
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-32-001_P&ID BALL MILL ML-3201 & CYCLONE
    CLUSTER CY-3201_B.pdf
  title: RB-4410-PID-32-001_P&ID BALL MILL ML-3201 & CYCLONE CLUSTER CY-3201_B.pdf
- id: src-15
  resource: corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR
    OPERATING MANUAL_R2.pdf
  title: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T18:04:18Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T18:04:18Z'
- by: process:okf-validation-suite
  at: '2026-09-30T18:04:18Z'
status: stable
entity_metadata:
  crusher_installed_power_kw: 1200
  feed_solids_tph: 2688
  sag_feed_f80_mm: 150
  crusher_p80_mm: 150
  cyclone_of_solids_pct: 35
  pumps_standby: 1
  pebble_recycle_tph: 484
  sif_functions:
  - SIF-3101
  - SIF-3102
  crusher_type: Gyratory 60 x 113
  pumps_duty: 2
  cyclone_of_p80_um: 150
  fresh_feed_tph: 2688
  plant_code: RB-4410
  cyclone_uf_tph: 8064
  circulating_load: 3
  crusher_tag: CR-2101
  crusher_feed_opening_mm: 1525
  crusher_css_mm: 165
  crusher_peak_tph: 5500
  cyclone_feed_tph: 10752
  cyclone_uf_solids_pct: 75
  cyclone_feed_solids_pct: 60
  unit_codes:
  - Area 2100
  - Area 3100
  - Area 3200
  throughput_tpd: 60000
  cyclone_of_tph: 2688
  instruments:
  - WT-2101
  - WIT-2102
  - PT-3201
  - DT-3201
  - LIC-3201
  - TT-3101
  - TT-3102
  - TT-3201
  - TT-3202
  - PT-3104
  - PSV-3105
  - WIC-3101
  - FIC-3103
  - JI-3101
  cyclone_feed_m3h: 11078
  pebble_crusher_tag: CR-3102
  pebble_crusher_type: Cone crusher, extra-coarse
  pebble_crusher_power_kw: 750
  pebble_crusher_throughput_tph: 484
  pebble_crusher_css_mm: 12
  cyclone_feed_pressure_max_kpa: 130
  cyclone_cluster_config: 16 x 660 mm (13 operating / 3 standby)
  cyclone_feed_pressure_min_kpa: 100
  sag_inching_rpm: 0.1
  sag_lube_oil_grade: ISO VG 460
  sag_charge_weight_max_t: 2450
  sag_specific_energy_kwh_t: 8.2
  sag_lube_design_barg: 170
  sag_shell_material: ASTM A516 Gr 70, 90 mm
  sag_ball_charge_pct: 12-15
  sag_dimensions: 12.2 x 6.7 m (40 x 22 ft)
  sag_reline_capacity_t: 2.5
  sag_max_filling_pct: 30
  sag_gmd_power_kw: 22000
  sag_hp_lift_normal_barg: 120
  sag_speed_range_pct_critical: 60-80
  ball_mill_speed_pct_critical: 75
  ball_mill_lube_oil_grade: ISO VG 460
  ball_mill_dimensions: 8.2 x 13.4 m (27 x 44 ft)
  ball_mill_charge_weight_max_t: 1980
  ball_mill_installed_power_kw: 22000
  ball_mill_lube_design_barg: 170
  ball_mill_reline_capacity_t: 2.5
  ball_mill_inching_rpm: 0.1
  ball_mill_voltage: 33 kV feed / cycloconverter
  ball_mill_media_size_mm: 65
  ball_mill_tag: ML-3201
  ball_mill_shell_material: ASTM A516 Gr 70, 80 mm
  ball_mill_hp_lift_barg: 110
  ball_mill_specific_energy_kwh_t: 8
  ball_mill_ball_charge_pct: 32 - 35
  ball_mill_rated_power_kw: 20500
  cyclone_feed_pump_rated_flow_m3h: 4650
  cyclone_feed_pump_liner: High-chrome white iron
  cyclone_feed_pump_casing_barg: 10
  cyclone_feed_pump_tdh_m: 32
  cyclone_feed_pump_power_kw: 1600
  cyclone_feed_pump_tag: PP-3201A/B/C
  crusher_vendor_drawing: VD-2101
  stockpile_live_capacity_t: 60000
  stockpile_tag: ST-2101
  conveyor_reconciliation_tag: WIT-2102
  conveyor_tag: CV-2101
  conveyor_wt_tag: WT-2101
  stockpile_reclaim_feeders:
  - FE-3101A
  - FE-3101B
  - FE-3101C
  sag_gmd_power_kw_conflict:
    pid_31_001_kw: 20000
    pds_and_equip_list_kw: 22000
  target_sag_mill_solids_pct: 75
  discrepancy_psv_3105:
    om_001_barg: 160
    corroborated_by_om001: true
    pid_31_002_barg: 180
    system_design_barg: 170
    pds_ps_0032_barg: 160
    conflict: false
  psv_3105_conflict:
    pds_set_barg: 160
    pid_set_barg: 180
    system_design_barg: 170
  lift_pumps:
  - PP-3105A
  - PP-3105B
  lube_reservoir: TK-3105
  standby_pump_pp3201c_identical: true
  radiation_permit_required: true
  cyclone_feed_pump_rated_flow_conflict:
    pfd_and_pid_rated_m3h: 5539
    pds_rated_m3h: 4650
  nuclear_gauge_tag: DT-3201
  locked_charge_limit_hours: 4
  conflict_cyclone_density:
    pds_and_pid_pct: 60
    om_001_pct: 65
  isolation_standard: RB-4410-SG-005
  circulating_load_range_pct: 250 - 300
  psv_3105_set_pressure_barg: 160
  sag_operating_power_mw: 18 - 21
  reline_duration_hours: 72 - 96
  ball_mill_operating_power_mw: 19 - 21
  grindout_duration_min: 10 - 15
---

> ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
> - **⚠️ CONFLICT — CYCLONE FEED SLURRY DENSITY (CY-3201):** Operating Manual `RB-4410-OM-001 Rev 2` (Table 3.32 and Section 4) explicitly specifies the design cyclone feed density as **65 % solids w/w** (regulated via `DT-3201` and sump dilution water). In contrast, Process Data Sheet `RB-4410-PS-CY3201 Rev B`, Process Flow Diagram `RB-4410-PFD-001 Rev B` (Stream S-321), and P&ID `RB-4410-PID-32-001 Rev B` specify a design cyclone feed density of **60.0 % solids w/w** (SG 1.618). Section 4 of `RB-4410-OM-001 Rev 2` warns: *"Operating the cyclones above the design feed density coarsens the overflow and reduces rougher recovery. Operators should reduce feed rate before exceeding the target."* Reconcile this operating setpoint with lead process metallurgist prior to HAZOP closure.
> - **LOCKED (FROZEN) CHARGE HAZARD ON SAG MILL START-UP:** Following any stoppage longer than **4 hours**, fine ore and slurry consolidate into a dense cemented mass ("locked" charge) adhering to the mill shell. Starting at full rotational speed causes the frozen charge to be carried upward and drop from top dead center (12.2 m drop), causing catastrophic shell deformation, liner bolt shearing, or trunnion bearing cracking. Operators must engage the Gearless Motor Drive (GMD) inching mode (0.1 rpm) to gently rotate the shell and visually verify charge detachment before starting main drive per `RB-4410-OM-001 Rev 2` Section 5 & 7.
> - **MILL RELINING SAFETY & 33 kV ISOLATION (RB-4410-SG-005):** During planned stops the SAG mill must be run empty (grind-out) for **10 to 15 minutes** to reduce charge weight. The GMD must be isolated at the **33 kV feeder** and personal locks applied per site standard `RB-4410-SG-005`. The mechanical liner handler must NEVER be operated inside the mill drum while the mill is on inching drive. Typical relining duration is **72 to 96 hours** per `RB-4410-OM-001 Rev 2` Section 6.
> - **CORROBORATION OF PSV-3105 SET PRESSURE (160 bar(g)):** Section 12 of `RB-4410-OM-001 Rev 2` explicitly corroborates that SAG HP lift pump discharge relief valve `PSV-3105` has a set pressure of **160 bar(g)** (against 170 bar(g) system design), confirming Process Data Sheet `RB-4410-PS-0032 Rev B` and resolving the conflict against P&ID drawing `RB-4410-PID-31-002 Rev B`'s erroneous notation of 180 bar(g).
> - **⚠️ CONFLICT — CYCLONE FEED PUMP RATED FLOW:** Process Data Sheet `RB-4410-PS-PP3201 Rev B` specifies a rated slurry flow rate of **4,650 m³/h** per pump, whereas Process Flow Diagram `RB-4410-PFD-001 Rev B` (Stream S-322), Operating Manual `RB-4410-OM-001 Rev 2` (Sec 3.32), and Piping & Instrumentation Diagram `RB-4410-PID-32-001 Rev B` specify a rated slurry flow rate of **5,539 m³/h** each @ SG 1.618 (total feed 11,078 m³/h split across 2 duty pumps `PP-3201A/B`) — verify pump hydraulic capacity, impeller sizing curve, and operating point with lead process engineer before HAZOP.
> - **⚠️ CONFLICT — CYCLONE FEED PUMP RATED FLOW:** Process Data Sheet `RB-4410-PS-PP3201 Rev B` specifies a rated slurry flow rate of **4,650 m³/h** per pump, whereas Process Flow Diagram `RB-4410-PFD-001 Rev B` (Stream S-322) and Piping & Instrumentation Diagram `RB-4410-PID-32-001 Rev B` specify a rated slurry flow rate of **5,539 m³/h** each @ SG 1.618 (total feed 11,078 m³/h split across 2 duty pumps `PP-3201A/B`) — verify pump hydraulic capacity, impeller sizing curve, and operating point with lead process engineer before HAZOP.
> - **CYCLONE FEED HOPPER LEVEL & PUMP SPEED CONTROL (LIC-3201):** Per Note 1 of `RB-4410-PID-32-001 Rev B`, cyclone feed hopper level controller `LIC-3201` modulates the variable speed drive (VFD) of cyclone feed pumps `PP-3201A/B` to maintain stable sump inventory. Signal failure or control loop instability can cause sump slurry overflow onto the grinding floor or pump cavitation.
> - **NUCLEAR GAUGE RADIATION SAFETY (DT-3201):** Per Note 3 of `RB-4410-PID-32-001 Rev B`, density transmitter `DT-3201` on the cyclone feed vertical column is a nuclear gauge; statutory radiation safety permits, shutter padlock lockouts, and wipe testing protocols apply.
> - **STANDBY PUMP REDUNDANCY (PP-3201C):** Per Note 2 of `RB-4410-PID-32-001 Rev B`, standby pump `PP-3201C` is identical to duty pumps `PP-3201A/B` (C not shown on drawing). Automated valve sequencing and seal water priming are mandatory during online pump transfer.
> - **⚠️ CONFLICT — RELIEF VALVE SET PRESSURE VS SYSTEM DESIGN PRESSURE & PROCESS DATA SHEET (PSV-3105):** Drawing `RB-4410-PID-31-002 Rev B` explicitly specifies `PSV-3105 SET 180 bar(g)`. However, Note 1 on the drawing mandates: *"PSV-3105 protects HP lift pump discharge; set pressure shall not exceed system design pressure."* The HP lift pump circuit system design pressure on this drawing is specified as **170 bar(g)** (normal operating discharge 120 bar(g)). In contrast, Process Data Sheet `RB-4410-PS-0032 Rev B` specifies the set pressure of `PSV-3105` as **160 bar(g)**. Setting PSV-3105 at 180 bar(g) exceeds the 170 bar(g) system design pressure rating by 10 bar and directly violates drawing Note 1. This overpressure discrepancy must be verified with piping/mechanical engineering and corrected prior to HAZOP closure.
> - **SAG MILL START INHIBIT INTERLOCK (SIF-3102 / PT-3104):** Per Note 2 of `RB-4410-PID-31-002 Rev B`, pressure transmitter `PT-3104` Low-Low Pressure Alarm (`PALL 70 bar(g)`) executes Safety Instrumented Function `SIF-3102` to inhibit SAG Mill start. Hydrostatic lift oil pressure (normal operating 120 bar(g)) supplied by pumps `PP-3105A/B` from 12 m³ reservoir `TK-3105` must be confirmed before drum rotation to prevent white metal Babbitt bearing wipe under the 2,450 t total charge weight.
> - **SAG MILL MOTOR POWER DISCREPANCY (⚠️ CONFLICT):** Piping & Instrumentation Diagram `RB-4410-PID-31-001 Rev B` specifies the SAG Mill `ML-3101` motor rating as **20,000 kW GMD** (Gearless Motor Drive). In contrast, Process Data Sheet `RB-4410-PS-ML3101 Rev B` and Mechanical Equipment List `RB-4410-PID-00-002 Rev B` specify an installed power of **22,000 kW** (22 MW GMD). This 2,000 kW discrepancy represents an unaligned drive sizing or de-rated motor allocation that must be formally reconciled with electrical engineering and vendor drive documentation prior to HAZOP closure.
> - **AUXILIARY LUBRICATION EQUIPMENT OMISSION (NOTE 3):** Per Note 3 of `RB-4410-PID-31-002 Rev B`, coolers, filters, and heaters are not shown on the P&ID and reside in vendor packages.
> - **SAG MILL PULP DENSITY RATIO CONTROL (FIC-3103):** Per Note 3 of `RB-4410-PID-31-001 Rev B`, mill feed water ratio controller `FIC-3103` targets **75 % solids** in the SAG mill belly. Ratio controller failure causes slurry pooling (excess dilution water dampening grinding kinetics) or viscoplastic slurry cushioning and severe liner damage (insufficient water).
> - **SAG BEARING TRIP VIA SIF-3101 (SIL 1):** Per Note 2 of `RB-4410-PID-31-001 Rev B`, duplex RTD temperature transmitters `TT-3101` (drive-end) and `TT-3102` (non-drive-end) initiate an emergency stop of the SAG mill main drive via Safety Instrumented Function `SIF-3101` (SIL 1) governed by standard `RB-4410-STD-CE-001` at `TAHH 75 °C` (warning alarm `TAH 70 °C`) to protect white metal Babbitt bearings from catastrophic wipe under the 2,450 t total charge weight.
> - **PEBBLE CRUSHER BYPASS CHUTE OMISSION:** Per Note 4 of `RB-4410-PID-31-001 Rev B`, the pebble crusher bypass chute is not shown on the drawing. Bypass line routing and diversion interlocks during cone crusher `CR-3102` maintenance must be strictly verified before HAZOP.
> - **PRIMARY CRUSHER MOTOR POWER CONFLICT (⚠️ CONFLICT):** Piping & Instrumentation Diagram `RB-4410-PID-21-001 Rev B` and Process Data Sheet `RB-4410-PS-CR2101 Rev B` specify Primary Gyratory Crusher `CR-2101` installed power as **1,200 kW**. In contrast, Mechanical Equipment List `RB-4410-PID-00-002 Rev B` specifies **1,000 kW** installed/motor power. Drive sizing and electrical load lists must be reconciled prior to HAZOP closure.
> - **PRIMARY CRUSHER THROUGHPUT CONFLICT (⚠️ CONFLICT):** Process Data Sheet `RB-4410-PS-CR2101 Rev B` and P&ID `RB-4410-PID-21-001 Rev B` specify a primary crusher mechanical design throughput / ROM ore maximum feed rate of **5,500 t/h** (Gyratory 60 x 113, 1,200 kW, CSS 165 mm), whereas `RB-4410-PFD-001 Rev B` (Stream S-101) specifies a nominal continuous operating solids throughput of **2,688 t/h** (corresponding to 60,000 tpd at 93% plant availability). Overland conveyor `CV-2101`, apron feeder `FE-2101`, transfer chutes, and coarse ore stockpile `ST-2101` must be engineered to absorb this peak instantaneous surge envelope prior to HAZOP closure.
> - **PLANT FEED RECONCILIATION METER INTEGRITY (WIT-2102):** Per Note 3 of `RB-4410-PID-21-001 Rev B`, weightometer `WIT-2102` on conveyor `CV-2101` is the official plant feed reconciliation meter governing daily concentrator metallurgical balance and mine reconciliation. Dynamic calibration chains and belt tare zeroing must be maintained under strict QA protocol.
> - **CRUSHER LUBRICATION & HYDROSET INTEGRITY (VD-2101):** Primary crusher lubrication and hydraulic hydroset mantle positioning are governed by vendor drawing `VD-2101` (PID Note 1). Lube pressure, flow, and temperature trips must be interlocked with the 1,200 kW drive motor to prevent eccentric bushing seizure.
> - **CYCLONE FEED PUMP RATED FLOW DISCREPANCY (⚠️ CONFLICT):** Process Data Sheet `RB-4410-PS-PP3201 Rev B` specifies a rated slurry flow rate of **4,650 m³/h** per pump (1,600 kW motor, 32 m TDH, 10 bar(g) casing design pressure). In contrast, Process Flow Diagram `RB-4410-PFD-001 Rev B` (Stream S-322) specifies an operating flow rate of **5,539 m³/h** per operating duty pump (total cluster feed Stream S-321 of 11,078 m³/h at 60.0 wt% solids and SG 1.618 across 2 operating pumps `PP-3201A/B`). The 889 m³/h per pump deficit (16.0% below PFD nominal operating flow) represents an unresolved sizing conflict that could restrict concentrator throughput or induce severe pump cavitation and motor overload if operated at PFD throughput. Verified engineering hydraulic runout curves and impeller trim must be confirmed with the lead mechanical/process engineer before HAZOP closure.
> - **BALL MILL BEARING THERMAL & LUBE PROTECTION (ML-3201):** Per `RB-4410-PS-ML3201 Rev B`, Secondary Ball Mill `ML-3201` operates with a combined hydrostatic lift and hydrodynamic lubrication unit (ISO VG 460 oil) at a normal HP lift pump discharge of **110 bar(g)** into a **170 bar(g)** design system. White metal Babbitt bearing temperatures are monitored by `TT-3201` and `TT-3202` across 0–150 °C. The mill carries up to **1,980 tonnes** total charge weight at 32–35% vol ball filling; confined space liner relining using a **2.5 t** relining machine and **0.1 rpm** inching mode requires mandatory 33 kV breaker LOTO and mechanical brake locking.
> - **SAG MILL BEARING LUBRICATION COLLAPSE PROTECTION (SIF-3102):** Per `RB-4410-PS-ML3101 Rev B` and `RB-4410-PS-0032 Rev B`, SAG Mill `ML-3101` trunnion bearings operate on a combined hydrostatic lift and hydrodynamic lube unit (ISO VG 460 oil) with normal high-pressure lift pump discharge of **120 bar(g)** into a **170 bar(g)** design pressure system. Transmitter `PT-3104` triggers safety function `SIF-3102` to inhibit mill starting or trip running mill drive on low-low pressure `PALL 70 bar(g)` (warning alarm `PAL 90 bar(g)`). PSV-3105 provides mechanical overpressure relief at 160 bar(g).
> - **SIF-3101 (SIL 1) SAG MILL TRUNNION BEARING OVERTEMPERATURE TRIP:** White metal Babbitt linings of the 2 x 2 pad trunnion bearings are monitored by duplex RTD transmitters `TT-3101` (drive-end) and `TT-3102` (non-drive-end) across 0–150 °C per `RB-4410-PS-ML3101 Rev B` and `RB-4410-PS-0034 Rev B`. Warning alarm activates at `TAH 70 °C`; emergency trip executes at `TAHH 75 °C` via `SIF-3101` (SIL 1) to prevent catastrophic bearing wipe, Babbitt liquefaction, and journal gouging under the 2,450 t total charge load.
> - **PRIMARY CRUSHER THROUGHPUT CONFLICT (⚠️ CONFLICT):** Process Data Sheet `RB-4410-PS-CR2101 Rev B` specifies a primary crusher mechanical design throughput of **5,500 t/h** (Gyratory 60 x 113, 1,200 kW), whereas `RB-4410-PFD-001 Rev B` (Stream S-101) specifies a nominal continuous operating solids throughput of **2,688 t/h** (corresponding to 60,000 tpd at 93% plant availability). Overland conveyor `CV-2101`, apron feeder `FE-2101`, and transfer chutes must be engineered to absorb this peak instantaneous surge envelope prior to HAZOP closure.
> - **PEBBLE RECYCLE THROUGHPUT CONGRUENCE:** Process Data Sheet `RB-4410-PS-CR3102 Rev B` specifies a design throughput of **484 t/h** (Cone crusher, extra-coarse, 750 kW, CSS 12 mm) for Pebble Crusher `CR-3102`, which is fully congruent with the continuous mass balance pebble recycle rate on Stream S-305 (484 t/h dry solids, 191 $m^3/h$, 97.0 wt% solids) specified on Drawing `RB-4410-PFD-001 Rev B`.
> - **CYCLONE CLUSTER OPERATING PRESSURE & CONFIGURATION:** Hydrocyclone cluster `CY-3201` comprises **16 x 660 mm** cyclones (13 operating / 3 standby) operating at **100–130 kPa** feed pressure per `RB-4410-PS-CY3201 Rev B`, bounded by DCS alarms PAL 90 kPa and PAH 140 kPa (PT-3201 per `RB-4410-PS-0032 Rev B`). Slurry feed density is regulated at 60.0% w/w (SG 1.618 monitored by DT-3201). Density exceeding 60.0% w/w induces hydrocyclone roping, injecting coarse oversize into the flotation feed (Stream S-324) and triggering severe slurry pump cavitation or line sanding.
> - **SAG MILL BEARING PROTECTION (SIF-3101 & SIF-3102):** SAG Mill `ML-3101` trunnion bearings are protected by two independent Safety Instrumented Functions:
>   - **Thermal Protection (SIF-3101, SIL 1):** Dual temperature transmitters `TT-3101` (drive-end) and `TT-3102` (non-drive-end) monitor white metal Babbitt bearing temperatures across 0–150 °C per `RB-4410-PS-0034 Rev B`. Warning alarm activates at `TAH 70 °C`; emergency trip executes at `TAHH 75 °C` to prevent catastrophic bearing wipe and shaft seizure.
>   - **Lubrication Lift Oil Protection (SIF-3102):** Pressure transmitter `PT-3104` monitors hydrostatic lift oil pressure (0–250 bar(g)) per `RB-4410-PS-0032 Rev B`. Low alarm at `PAL 90 bar(g)`; start inhibit and trip execute at `PALL 70 bar(g)`.
> - **CYCLONE INSTRUMENTATION CONTROL (PT-3201 & DT-3201):** Operating manifold pressure is monitored by `PT-3201` (span 0–250 kPa, normal window 100–130 kPa, alarms 90–140 kPa). Feed pulp density is monitored on the vertical delivery riser by nuclear gamma transmitter `DT-3201` (span 1.0–2.0 SG, nominal design 1.618 SG per `RB-4410-PS-0033 Rev B`), providing feedback to sump dilution water valves.
> - The comminution circuit operates with a high-density classification closed loop (60.0% w/w hydrocyclone feed, 75.0% w/w underflow) and a 300% circulating load (8,064 t/h ball mill recycle). Dilution water addition to the cyclone feed pump sump must be strictly interlocked with pulp density sensors. Slurry density exceeding 60.0% w/w induces hydrocyclone roping, injecting coarse oversize into the flotation feed (Stream S-324) and triggering severe slurry pump cavitation or line sanding.
> - **CYCLONE INSTRUMENTATION CONTROL (PT-3201 & DT-3201):** Operating manifold pressure is monitored by `PT-3201` (span 0–250 kPa, window 90–140 kPa). Feed pulp density is monitored on the vertical delivery riser by nuclear gamma transmitter `DT-3201` (span 1.0–2.0 SG, nominal design 1.618 SG per `RB-4410-PS-0033 Rev B`), providing feedback to sump dilution water valves.

## Grinding Circuit Operations & Operating Philosophy (RB-4410-OM-001)
Operating Manual `RB-4410-OM-001 Rev 2` defines the operational requirements for the comminution circuit (Areas 21, 31, and 32):

### 1. Grinding Operating Envelopes & Target Matrix
- **SAG Mill Feed Rate (WIC-3101):** 2,688 t/h dry solids.
- **SAG Mill Belly Slurry Density (FIC-3103):** 75 % solids w/w maintained by feed water ratio controller.
- **SAG Mill Power Draw Target:** 18 to 21 MW regulated by speed (60–80% critical) and feed rate.
- **Ball Mill Power Draw Target:** 19 to 21 MW on fixed-speed GMD ring motor (75% critical).
- **Cyclone Feed Density Target:** 65 % solids w/w monitored by `DT-3201` via sump dilution water (⚠️ CONFLICT vs 60.0% in datasheets).
- **Cyclone Feed Pressure Window (PT-3201):** 100 to 130 kPa across 13 operating cyclones (3 standby).
- **Cyclone Overflow Liberation Size:** $P_{80} = 150\ \mu\text{m}$ monitored by online PSI particle size analyser.
- **Grinding Circulating Load:** 250 to 300 % calculated ratio.

### 2. SAG Mill Start-Up & Feed Ramp Sequence
1. Confirm lube and hydrostatic lift system running, `PT-3104` above 90 bar(g) (start permissive `SIF-3102`).
2. Confirm `TT-3101`/`TT-3102` healthy and below alarm (`TAH 70 °C`).
3. Check for frozen (locked) charge after a stop longer than 4 hours: inch the mill using GMD inching mode (0.1 rpm) and observe charge detachment.
4. Start the mill at 70 % critical speed, then introduce feed at 50 % of target over 15 minutes via `WIC-3101`.
5. Start cyclone feed pumps `PP-3201A` and `B` before mill discharge reaches the hopper.

### 3. SAG Mill Shutdown, Grind-out & Relining Sequence
1. For a planned stop, run the mill empty (grind-out) for 10 to 15 minutes to reduce charge weight.
2. Isolate the GMD at the 33 kV feeder and apply personal locks per site standard `RB-4410-SG-005` (mill isolation).
3. Relining uses the 2.5 t mill relining machine; the liner handler must not be used while the mill is on inching drive.
4. Typical SAG reline duration is 72 to 96 hours.

### 4. Grinding Circuit Abnormal Situations & Responses
- **SAG Bearing Temperature High:** Lube oil cooling loss or filter blockage triggers `TAH 70 °C` alarm; `SIF-3101` trips mill at `TAHH 75 °C`.
- **Locked Charge:** Stopped > 4 h with fine ore; inch mill; never start at full speed with frozen charge.
- **Cyclone Roping:** Feed density too high (> 65%) or pump under capacity; add dilution water, check pump speed.
- **Hopper Overflow / Sanding:** Cyclone feed pump under capacity; reduce fresh feed on `CV-3101`, start standby pump `PP-3201C`.

## References & Sources
- Operating Manual No. RB-4410-OM-001 Rev 2, *Ridgeback Concentrator - Operating Manual*, Cymbal Copper Pty Ltd.
- Drawing No. RB-4410-PFD-001 Rev B, *Process Flow Diagram Crushing and Grinding*, Cymbal Copper Pty Ltd.
- Process Data Sheet No. RB-4410-PS-0032 Rev B, *Pressure Instrument & Relief Valve Process Data Sheet*, Cymbal Copper Pty Ltd.
- Process Data Sheet No. RB-4410-PS-0033 Rev B, *Analyser, Density & Level Instrument Process Data Sheet*, Cymbal Copper Pty Ltd.
- Process Data Sheet No. RB-4410-PS-0034 Rev B, *Temperature Instrument Process Data Sheet*, Cymbal Copper Pty Ltd.
- Process Data Sheet No. RB-4410-PS-CR2101 Rev B, *Primary Gyratory Crusher Process Data Sheet*, Cymbal Copper Pty Ltd.
- Process Data Sheet No. RB-4410-PS-CR3102 Rev B, *Pebble Crusher Process Data Sheet*, Cymbal Copper Pty Ltd.
- Process Data Sheet No. RB-4410-PS-CY3201 Rev B, *Cyclone Cluster Process Data Sheet*, Cymbal Copper Pty Ltd.
- Process Data Sheet No. RB-4410-PS-ML3101 Rev B, *SAG Mill Process Data Sheet*, Cymbal Copper Pty Ltd.
- Process Data Sheet No. RB-4410-PS-ML3201 Rev B, *Ball Mill Process Data Sheet*, Cymbal Copper Pty Ltd.
- Process Data Sheet No. RB-4410-PS-PP3201 Rev B, *Cyclone Feed Pump Process Data Sheet*, Cymbal Copper Pty Ltd.
- Drawing No. RB-4410-PID-21-001 Rev B, *Piping & Instrumentation Diagram - Primary Crushing*, Cymbal Copper Pty Ltd.
- Drawing No. RB-4410-PID-31-001 Rev B, *Piping & Instrumentation Diagram - SAG Mill ML-3101*, Cymbal Copper Pty Ltd.
- Drawing No. RB-4410-PID-31-002 Rev B, *Piping & Instrumentation Diagram - SAG Mill Hydrostatic Lift & Lube System*, Cymbal Copper Pty Ltd.
- Drawing No. RB-4410-PID-32-001 Rev B, *Piping & Instrumentation Diagram - Ball Mill ML-3201 & Cyclone Cluster CY-3201*, Cymbal Copper Pty Ltd.
- Standard No. RB-4410-SG-005, *Mill Isolation and LOTO Standard*, Cymbal Copper Pty Ltd.

## Area 3200 Ball Milling & Cyclone Classification Control Philosophy (RB-4410-PID-32-001)
- **Cyclone Feed Sump Inventory Regulation (LIC-3201):** Sump level controller `LIC-3201` regulates the slurry level in the common cyclone feed hopper by modulating the variable speed drive (VFD) of duty pumps `PP-3201A/B` (Note 1). This prevents sump overflowing under circulating load surges and protects against pump air entrainment.
- **Standby Slurry Pump Equivalence (PP-3201C):** As codified in Note 2 of `RB-4410-PID-32-001 Rev B`, installed standby pump `PP-3201C` (not shown on drawing) is identical in hydraulic design, metallurgy (high-chrome white iron), and drive power (1,600 kW) to duty pumps `PP-3201A` and `PP-3201B`.
- **Slurry Density Optimization & Radiation Permitting (DT-3201):** Vertical cyclone feed riser density is monitored by nuclear density transmitter `DT-3201` targeting 60.0 wt% solids (SG 1.618). Note 3 mandates that statutory radiation safety permits apply for nuclear gauge `DT-3201`. Feedback controls sump dilution water trim to maintain cyclone separation efficiency ($P_{80} = 150\text{ µm}$) and prevent cyclone roping.
- **Feed Pressure Monitoring (PT-3201):** Operating pressure on the radial distributor manifold is monitored by `PT-3201` (normal operating window 100–130 kPa, PAL 90 kPa, PAH 140 kPa).

## Equipment Roster
| Equipment Tag | Equipment Name | Class | Design Duty / Capacity | PFD Stream Ties |
| :--- | :--- | :--- | :--- | :--- |
| **CR-2101** | Primary Gyratory Crusher | Crusher | Gyratory 60 x 113, 1,200 kW (PS-CR2101 / PID-21-001) / 1,000 kW (PID-00-002), 5,500 t/h peak mechanical design capacity (2,688 t/h nominal operating rate), CSS 165 mm, feed opening 1,525 mm, product $P_{80} = 150\text{ mm}$; lube/hydroset per VD-2101 [^5] [^11] | Discharges S-101 via CV-2101; fed via FE-2101 [^1] [^5] [^11] |
| **ML-3101** | SAG Mill | Grinding Mill | 12.2 x 6.7 m (40 x 22 ft), 20,000 kW GMD (PID-31-001) / 22,000 kW GMD (PS-ML3101 / PID-00-002), 2,688 t/h fresh feed + 484 t/h pebble recycle (3,172 t/h total), 8.2 kWh/t, 60–80% critical speed, 12–15% ball charge, 30% max filling, 2,450 t max charge, ASTM A516 Gr 70 90 mm shell, 2 x 2 pad trunnion bearings (120 bar(g) normal lift oil, ISO VG 460); SIF-3101 (SIL 1) TT-3101/3102 per RB-4410-STD-CE-001; SIF-3102 PT-3104; FIC-3103 targets 75% solids; WIC-3101; JI-3101 | Receives S-301, S-305; Discharges via trommel to SC-3101 |
| **ML-3201** | Secondary Ball Mill | Grinding Mill | 8.2 x 13.4 m (27 x 44 ft), 22,000 kW installed GMD ring motor, 75% critical speed, 32–35% vol ball charge (65 mm media), 8.0 kWh/t, 1,980 t max charge, ASTM A516 Gr 70 80 mm shell, cast steel head/trunnions, 110 bar(g) normal lift oil (170 bar(g) design, ISO VG 460), TT-3201/3202; 8,064 t/h solids (300% circulating load); discharges overflow to PP-3201 hopper | Receives S-323; Discharges overflow to PP-3201 hopper |
| **CY-3201** | Hydrocyclone Cluster | Classifier | 11,078 $m^3/h$ slurry @ 60% solids w/w; 16 x 660 mm (13 operating / 3 standby); 100–130 kPa feed pressure; overflow $P_{80} = 150\text{ µm}$; PT-3201, DT-3201 (nuclear gauge radiation permit per Note 3) | Receives S-321; Discharges S-323, S-324 |
| **PP-3201A/B/C** | Cyclone Feed Slurry Pumps | Centrifugal Slurry Pump | 2 Duty + 1 Standby (PP-3201C identical to A/B per PID Note 2); Rated flow 5,539 m³/h each @ SG 1.618 (PID-32-001 & PFD-001) / 4,650 m³/h rated (PS-PP3201); TDH 32 m, 1,600 kW motor, 10 bar(g) casing, high-chrome white iron liners; LIC-3201 speed control | Discharges S-322 per duty pump to common S-321 |
| **CR-3102** | Pebble Crusher | Crusher | Cone crusher extra-coarse, 750 kW, 484 t/h design throughput, CSS 12 mm | Discharges S-305 (484 t/h dry solids) to CV-3101; fed from SC-3101 [^1] [^6] |
| **CV-2101** | Primary Crusher Discharge Conveyor | Conveyor | Overland conveyor transferring crushed ore (Stream S-101) from CR-2101 to stockpile ST-2101; up to 5,500 t/h peak surge, nominal 2,688 t/h solids; WT-2101 and WIT-2102 reconciliation meter [^11] | Conveys S-101 from CR-2101 to ST-2101 [^1] [^11] |
| **ST-2101** | Coarse Ore Stockpile | Stockpile | Live storage capacity: 60,000 t (~22.3 hours buffer at nominal 2,688 t/h); reclaimed via 3 apron feeders FE-3101A/B/C in reclaim tunnel [^11] | Receives S-101; discharges S-301 via FE-3101A/B/C to CV-3101 [^1] [^11] |
| **CV-3101** | SAG Mill Feed Conveyor | Conveyor | Transfers fresh ore (Stream S-301) and crushed pebbles return into SAG feed chute; 3,172 t/h nominal solids; WIC-3101 weight controller | Feeds S-301 and crushed pebbles return to ML-3101 feed chute |
| **SC-3101** | SAG Mill Discharge Screen | Vibrating Screen | Heavy-duty vibrating pebble scalping screen (12 mm cut); scalps 484 t/h pebbles (Stream S-305) to CR-3102; screen undersize (-12 mm) gravity drains to cyclone feed hopper | Receives ML-3101 trommel discharge; discharges S-305 to CR-3102; U/S to cyclone feed hopper |
| **TK-3105** | SAG Mill Lube Oil Reservoir | Tank | Capacity: 12 m³; Oil Grade: ISO VG 460; supplies PP-3105A/B; receives PSV-3105 relief return; temperature TT-3101 | Lube oil inventory loop for ML-3101 |
| **PP-3105A** | SAG Mill HP Lift Pump A | Pump | Duty positive-displacement lift pump; Normal discharge 120 bar(g); System design pressure 170 bar(g); protected by PSV-3105 | Suction from TK-3105; discharge to ML-3101 trunnion pads |
| **PP-3105B** | SAG Mill HP Lift Pump B | Pump | Standby positive-displacement lift pump; Normal discharge 120 bar(g); System design pressure 170 bar(g); protected by PSV-3105 | Suction from TK-3105; discharge to ML-3101 trunnion pads |

## Citations
[^13]: Drawing No. RB-4410-PID-32-001 Rev B, *Piping & Instrumentation Diagram - Ball Mill ML-3201 & Cyclone Cluster CY-3201*, Ridgeback Concentrator.

## Area 3100 SAG Milling Control Philosophy (RB-4410-PID-31-001 & PID-31-002)
- **Mill Feed Rate Regulation (WIC-3101):** Weight indicating controller `WIC-3101` on feed conveyor `CV-3101` regulates total ore feed (nominal 2,688 t/h fresh ore) by modulating the speed of stockpile reclaim apron feeders `FE-3101A/B/C`.
- **Feed Water Ratio Control (FIC-3103):** Process water is injected into the SAG mill feed chute under ratio control via `FIC-3103`, which continuously tracks ore mass flow from `WIC-3101` to target **75 % solids** inside the grinding drum (Note 3). Correct slurry rheology ensures efficient autogenous impact grinding without slurry pooling or ball-on-liner damage.
- **Drive Load & Power Monitoring (JI-3101):** Motor load indicator `JI-3101` continuously tracks power draw of the GMD ring motor (0–25,000 kW) to detect mill overload, slurry pooling, or charge volume variations.
- **Pebble Scalping & Classification (SC-3101 & CR-3102):** Mill slurry discharges through a trunnion trommel onto vibrating screen `SC-3101`. Screen oversize (+12 mm pebbles, Stream S-305 at 484 t/h) is conveyed to Pebble Crusher `CR-3102`. Screen undersize (-12 mm slurry) gravity drains into the common cyclone feed hopper feeding slurry pumps `PP-3201A/B/C`.
- **SIF-3101 (SIL 1) Bearing Overtemperature Trip:** Embedded duplex RTDs `TT-3101` (drive-end) and `TT-3102` (non-drive-end) monitor trunnion Babbitt temperatures (0–150 °C span). Pre-trip alarm initiates at `TAH 70 °C`; `SIF-3101` executes an emergency trip of the SAG mill drive at `TAHH 75 °C` per `RB-4410-STD-CE-001` (Note 2).
- **Hydrostatic Lift & Lube System Protection (RB-4410-PID-31-002):**
  - High-pressure lift pumps `PP-3105A/B` draw ISO VG 460 lube oil from 12 m³ reservoir `TK-3105` and deliver it at 120 bar(g) normal operating pressure (170 bar(g) system design pressure) to the SAG mill trunnion bearing pads.
  - Pressure transmitter `PT-3104` monitors lift oil header pressure. Per Drawing Note 2, `PT-3104` Low-Low Pressure Alarm (`PALL 70 bar(g)`) executes Safety Instrumented Function `SIF-3102` to inhibit mill starting and protect against bearing wipe.
  - Overpressure protection is provided by safety relief valve `PSV-3105` relieving back to reservoir `TK-3105`. ⚠️ **CONFLICT:** Drawing RB-4410-PID-31-002 Rev B specifies `SET 180 bar(g)`, which exceeds the 170 bar(g) system design pressure and contradicts Drawing Note 1, whereas Process Data Sheet `RB-4410-PS-0032 Rev B` specifies `160 bar(g)`. Field setting must be verified before HAZOP.
  - Note 3 indicates coolers, filters, and heaters are omitted from the P&ID and covered under vendor packages.
- **Pebble Crusher Bypass Routing:** Note 4 indicates the pebble crusher bypass chute is not shown on the P&ID. Operational diversion during pebble crusher maintenance must be coordinated to prevent circuit bottlenecks.

## Circuit Summary
The Crushing and Grinding Circuit encompasses primary ore reduction and overland surge storage (Area 2100 / Area 21), primary SAG milling and pebble crushing (Area 3100), and secondary ball mill grinding with closed-circuit hydrocyclone classification (Area 3200). It processes 60,000 tpd (2,688 t/h at 93% availability) of run-of-mine ore down to a target product grind of $P_{80} = 150\text{ µm}$ in hydrocyclone overflow (Stream S-324) feeding the flotation plant [^1] [^5] [^6] [^7] [^8] [^9] [^10] [^11].

## Area 2100 Primary Crushing & Surge Storage Control Philosophy (RB-4410-PID-21-001)
- **Crusher Operation (CR-2101):** Run-of-mine ore is dumped by haul trucks into the dump pocket and fed to the 60 x 113 gyratory crusher cavity via apron feeder FE-2101. The crusher reduces ore to a nominal $P_{80} = 150\text{ mm}$ at a Closed Side Setting of 165 mm, driven by a 1,200 kW motor [^5] [^11].
- **Crusher Lubrication & Hydraulic Hydroset System (VD-2101):** Spider bushing lubrication, eccentric bushing cooling, and mainshaft hydraulic vertical position adjustment (Hydroset) are provided by the vendor lube/hydraulic power package detailed on vendor drawing `VD-2101` (PID Note 1) [^11].
- **Overland Conveying & Feed Reconciliation (CV-2101):** Crushed ore discharges onto conveyor `CV-2101` (Stream S-101). Belt weight transmitter `WT-2101` monitors instantaneous flow and conveyor load. Downstream weightometer `WIT-2102` is certified as the official plant feed reconciliation meter (PID Note 3), providing cumulative dry tonnage logging for plant metallurgical accounting [^11].
- **Environmental Silica Dust Suppression:** Water sprays are positioned at the crusher discharge chamber and conveyor transfer chutes to suppress respirable crystalline silica dust (PID Note 2) [^11].
- **Stockpile Live Surge Buffer (ST-2101):** Conveyor CV-2101 discharges onto the 60,000 t live capacity coarse ore stockpile `ST-2101`. Reclaim apron feeders `FE-3101A/B/C` inside the underground reclaim vault draw coarse ore onto SAG feed conveyor `CV-3101` (Stream S-301), providing 22.3 hours of buffer capacity to ensure continuous grinding operations during mine or crusher downtime [^1] [^11].

## Area 3100 SAG Milling Control Philosophy (RB-4410-PID-31-001)
- **Mill Feed Rate Regulation (WIC-3101):** Weight indicating controller `WIC-3101` on feed conveyor `CV-3101` regulates total ore feed (nominal 2,688 t/h fresh ore) by modulating the speed of stockpile reclaim apron feeders `FE-3101A/B/C`.
- **Feed Water Ratio Control (FIC-3103):** Process water is injected into the SAG mill feed chute under ratio control via `FIC-3103`, which continuously tracks ore mass flow from `WIC-3101` to target **75 % solids** inside the grinding drum (Note 3). Correct slurry rheology ensures efficient autogenous impact grinding without slurry pooling or ball-on-liner damage.
- **Drive Load & Power Monitoring (JI-3101):** Motor load indicator `JI-3101` continuously tracks power draw of the GMD ring motor (0–25,000 kW) to detect mill overload, slurry pooling, or charge volume variations.
- **Pebble Scalping & Classification (SC-3101 & CR-3102):** Mill slurry discharges through a trunnion trommel onto vibrating screen `SC-3101`. Screen oversize (+12 mm pebbles, Stream S-305 at 484 t/h) is conveyed to Pebble Crusher `CR-3102`. Screen undersize (-12 mm slurry) gravity drains into the common cyclone feed hopper feeding slurry pumps `PP-3201A/B/C`.
- **SIF-3101 (SIL 1) Bearing Overtemperature Trip:** Embedded duplex RTDs `TT-3101` (drive-end) and `TT-3102` (non-drive-end) monitor trunnion Babbitt temperatures (0–150 °C span). Pre-trip alarm initiates at `TAH 70 °C`; `SIF-3101` executes an emergency trip of the SAG mill drive at `TAHH 75 °C` per `RB-4410-STD-CE-001` (Note 2).
- **Auxiliary Lube Interface (RB-4410-PID-31-002):** Hydrostatic lift and hydrodynamic lube systems are detailed on interface drawing `RB-4410-PID-31-002` (Note 1).
- **Pebble Crusher Bypass Routing:** Note 4 indicates the pebble crusher bypass chute is not shown on the P&ID. Operational diversion during pebble crusher maintenance must be coordinated to prevent circuit bottlenecks.

## Process Flowsheet & Equipment Interconnection
The comminution flowsheet is configured in a SABC-like (Semi-Autogenous Ball mill Crusher) closed-circuit arrangement depicted on Drawing RB-4410-PFD-001 Rev B, Process Data Sheet RB-4410-PS-CR2101 Rev B, Process Data Sheet RB-4410-PS-CR3102 Rev B, Process Data Sheet RB-4410-PS-CY3201 Rev B, Process Data Sheet RB-4410-PS-ML3101 Rev B, Process Data Sheet RB-4410-PS-ML3201 Rev B, and Process Data Sheet RB-4410-PS-PP3201 Rev B:

```
[ ROM Ore (Dump Pocket) ]
     │
     ▼ (Apron Feeder FE-2101, Feed Opening 1,525 mm)
[ Primary Gyratory Crusher CR-2101 (60 x 113, 1,200 kW, CSS 165 mm) ]
     │
     ▼ Stream S-101 (Overland Conveyor CV-2101, 2,688 t/h nom / 5,500 t/h peak solids @ 97% solids)
[ Coarse Ore Stockpile ]
     │
     ▼ Stream S-301 (2,688 t/h solids @ 97% solids)
[ SAG Mill ML-3101 (12.2 x 6.7 m, 22,000 kW GMD, 2,450 t max charge) ] ◄── [ Pebble Recycle Stream S-305: 484 t/h via CV-3101 ]
     │                                                                           ▲
     ▼ (Discharge Trommel to Screen SC-3101)                                      │
[ Pebble Screen SC-3101 ] ──(Oversize +12 mm)──────────────────────────► [ Pebble Crusher CR-3102 (Cone, 750 kW, CSS 12 mm, 484 t/h) ]
     │ (Undersize -12 mm)
     ▼
[ Common Cyclone Feed Sump ] ◄──── [ Ball Mill ML-3201 Discharge (Overflow to PP-3201 hopper) ]
     │
     ├─────────────────────────────────┐
     ▼                                 ▼
[ Cyclone Feed Pump PP-3201A ]    [ Cyclone Feed Pump PP-3201B ] (PP-3201C Standby)
  (4,650 m3/h rated, 1,600 kW)       (4,650 m3/h rated, 1,600 kW)
     │ (Stream S-322: 5,539 m3/h)      │ (Stream S-322: 5,539 m3/h)
     └────────────────┬────────────────┘
                      ▼ Stream S-321 (Total: 11,078 m3/h @ 60% solids, 1.618 SG monitored by DT-3201)
           [ Hydrocyclone Cluster CY-3201 (16 x 660 mm, 13 op / 3 stby, 100–130 kPa) ]
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
   (Underflow Stream S-323)   (Overflow Stream S-324)
   8,064 t/h solids           2,688 t/h solids @ 35% solids (P80 150 µm)
   @ 75% solids               5,969 m3/h slurry
         │                         │
         ▼                         ▼
   [ Ball Mill ML-3201 ]      [ To Rougher Flotation (RB-4410-PFD-002) ]
```

## Design Stream Mass Balance (RB-4410-PFD-001)
Operating parameters governing each process stream in the circuit:

| Stream ID | Description | Solids (t/h) | Water (t/h) | % Solids (w/w) | Slurry Flow ($m^3/h$) | Slurry SG | Source Reference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **S-101** | Primary crusher product to stockpile | 2,688 | 83 | 97.0 | 1,061 | 2.613 | RB-4410-PFD-001 Rev B [^1] |
| **S-301** | SAG mill fresh feed | 2,688 | 83 | 97.0 | 1,061 | 2.613 | RB-4410-PFD-001 Rev B [^1] |
| **S-305** | Pebble crusher recycle | 484 | 15 | 97.0 | 191 | 2.613 | RB-4410-PFD-001 Rev B [^1] |
| **S-321** | Cyclone feed (total, 2 duty pumps) | 10,752 | 7,168 | 60.0 | 11,078 | 1.618 | RB-4410-PFD-001 Rev B [^1] |
| **S-322** | Cyclone feed per duty pump (PP-3201A/B) | 5,376 | 3,584 | 60.0 | 5,539 | 1.618 | RB-4410-PFD-001 Rev B [^1] |
| **S-323** | Cyclone underflow to ball mill | 8,064 | 2,688 | 75.0 | 5,620 | 1.913 | RB-4410-PFD-001 Rev B [^1] |
| **S-324** | Cyclone overflow to flotation | 2,688 | 4,992 | 35.0 | 5,969 | 1.287 | RB-4410-PFD-001 Rev B [^1] |

## Operating Windows & Safety Interlocks
1. **Circulating Load Regulation:** Maintained at 300% ($8,064 / 2,688 = 3.00$). Deviations indicate either over-grinding ($CL < 250\%$) or excessive coarse ore buildup ($CL > 350\%$), which overloads the ball mill motor and risks sump slurry overflow [^1].
2. **Pebble Crushing Circuit Control (CR-3102):** Pebble Crusher `CR-3102` reduces critical-size pebbles (484 t/h design capacity) with a Closed Side Setting of 12 mm. Feed rate must be regulated by cavity level transmitters and 750 kW drive motor power draw to prevent cavity choking. Upstream cross-belt tramp magnets and metal detectors protect against broken SAG mill grinding balls [^6].
3. **SAG Mill Drive, Inching & Relining (ML-3101):** The SAG mill is powered by a 22,000 kW gearless synchronous ring motor fed by a 33 kV cycloconverter. Rotational speed operates within 60–80% of critical speed during normal grinding. A dedicated auxiliary GMD inching mode at 0.1 rpm permits controlled rotational positioning during relining and shell inspection. Relining operations utilize a 2.5 t capacity mill relining machine handling 50 mm Cr-Mo lifter bars [^8].
4. **SAG Mill Trunnion Bearing Protection (SIF-3101 & SIF-3102):**
   - **Thermal Protection (SIF-3101, SIL 1):** Dual duplex RTD sensors on drive-end (TT-3101) and non-drive-end (TT-3102) continuously monitor Babbitt white metal temperatures (0–150 °C span). Warning alarm activates at TAH 70 °C; automatic emergency drive shutdown trips at TAHH 75 °C to avert catastrophic bearing wipe under the 2,450 t total charge weight [^3] [^8].
   - **Hydrostatic Lift Pressure (SIF-3102):** The bearing package utilizes a combined hydrostatic lift and hydrodynamic lubrication unit (ISO VG 460 oil) with normal lift pump discharge at 120 bar(g). Pressure transmitter PT-3104 inhibits startup or trips running mill at PALL 70 bar(g) (warning alarm PAL 90 bar(g)) to prevent oil film collapse. PSV-3105 provides mechanical relief at 160 bar(g) against 170 bar(g) system design pressure [^4] [^8].
5. **Secondary Ball Mill Operation & Lubrication Protection (ML-3201):**
   - Secondary ball mill `ML-3201` is powered by a 22,000 kW installed GMD (20,500 kW rated ring motor) operating at fixed speed of 75% critical speed. Ball charge is 32–35% by volume with 65 mm media, achieving an 8.0 kWh/t specific grinding energy [^9].
   - The trunnion bearing package features a combined hydrostatic lift and hydrodynamic lube unit with ISO VG 460 oil. The high-pressure lift pump delivers normal discharge pressure of **110 bar(g)** into a **170 bar(g)** design system [^9].
   - Trunnion bearing white metal temperatures are monitored by `TT-3201` (drive-end) and `TT-3202` (non-drive-end) across 0–150 °C to prevent bearing wipe under the 1,980 t maximum charge weight [^9].
   - Maintenance inching is provided by a dedicated GMD mode at 0.1 rpm; liner replacement uses a 2.5 t capacity relining machine and requires positive 33 kV breaker LOTO [^9].
6. **Cyclone Feed Slurry Dilution & Density (DT-3201):** Dilution water is injected into the pump sump to preserve feed density at 60.0% w/w (SG 1.618), actively measured by nuclear gauge DT-3201 (1.0–2.0 SG). If density climbs towards 65%, cyclone roping occurs, causing coarse oversize ($+150\text{ µm}$) to contaminate the flotation feed [^1] [^2].
7. **Cyclone Feed Operating Pressure & Cluster Control (CY-3201):** Cyclone inlet manifold pressure is maintained between 100 and 130 kPa across 13 operating cyclones (3 standby). Monitored by PT-3201 with operational alarms at PAL 90 kPa and PAH 140 kPa [^4] [^7].
8. **Slurry Pump Protection & Anti-Sanding (PP-3201A/B/C):** PP-3201A/B/C operate in 2 duty + 1 standby configuration (1,600 kW motors, 32 m TDH, 10 bar(g) casing design pressure, high-chrome white iron liners per `RB-4410-PS-PP3201 Rev B`). Automatic flush water sequencing is mandatory upon pump trip to prevent coarse settling and line sanding in the cyclone feed vertical column [^1] [^10].
9. **Primary Crusher Cavity Level & Choke Protection:** Apron feeder `FE-2101` speed is modulated based on crusher cavity level to maintain optimal choke feeding without exceeding mantle motor load (1,200 kW) or causing feed pocket bridging [^5].
   - **Thermal Protection (SIF-3101, SIL 1):** White metal temperatures on drive-end (TT-3101) and non-drive-end (TT-3102) are continuously monitored across 0–150 °C. At TAH 70 °C, an alarm alerts the operator. At TAHH 75 °C, SIF-3101 automatically trips the SAG mill drive to prevent bearing wipe [^3].
   - **Hydrostatic Lift Pressure (SIF-3102):** PT-3104 inhibits startup or trips running mill at PALL 70 bar(g) (warning alarm PAL 90 bar(g)) [^4].
