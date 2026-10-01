# Subdirectories

* [equipment](equipment/index.md) - Index of equipment
* [hazards](hazards/index.md) - Index of hazards
* [hazop](hazop/index.md) - Index of hazop
* [instruments](instruments/index.md) - Index of instruments
* [parameters](parameters/index.md) - Index of parameters
* [procedures](procedures/index.md) - Index of procedures
* [sources](sources/index.md) - Index of sources
* [standards](standards/index.md) - Index of standards
* [troubleshooting](troubleshooting/index.md) - Index of troubleshooting
* [units](units/index.md) - Index of units

---

# Master Plant Knowledge Catalog (OKF v0.2)

## 1. Plant Unit Architecture & Scope
- **[Copper Concentrator Plant Overview, Circuit Hierarchy & Reagents](units/copper-concentrator.md)**: High-level concentrator overview covering circuit hierarchy, crushing, SAG milling, secondary ball milling & classification, rougher flot...
- **[Area 2100 / 3100 / 3200: Crushing and Grinding Circuit](units/crushing-and-grinding.md)**: Process unit overview, circuit topology, equipment roster, stream mass balance, primary crushing P&ID (Area 21), SAG Mill P&ID (PID-31-00...
- **[Area 4100 / 4200 / 4300: Flotation and Regrind Circuit](units/flotation.md)**: Process unit overview, circuit topology, equipment roster, stream mass balance, and reagent feed interfaces for Area 4100 / 4200 / 4300 F...

## 2. Master Equipment Specifications & P&ID Loop Matrix

| Tag | Equipment Title | Unit | Class | P&ID Loops | Engineering Function Summary |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [BL-4101A](equipment/BL-4101A.md) | BL-4101A — Rougher Flotation Air Blowers (BL-4101A/B) | Area 41 - Rougher Flotation | Blower | 1 loops | Low-pressure centrifugal air blowers configured in duty/standby service (BL-4101A/B) supplying continuous forced aeration air to the roug... |
| [CR-2101](equipment/CR-2101.md) | CR-2101 — Primary Gyratory Crusher | Area 21 - Primary Crushing | Crusher | 2 loops | Primary 60 x 113 gyratory crusher receiving run-of-mine ore (up to 5,500 t/h peak) via dump pocket/feeder FE-2101 and reducing rock to SA... |
| [CR-3102](equipment/CR-3102.md) | CR-3102 — Pebble Crusher | Area 31 - SAG Milling | Crusher | 1 loops | Cone crusher (extra-coarse) operating in the SAG mill closed circuit. Receives critical-size pebbles (typically 25–65 mm) screened from t... |
| [CV-2101](equipment/CV-2101.md) | CV-2101 — Primary Crusher Discharge Conveyor | Area 21 - Primary Crushing | Conveyor | 2 loops | Primary crusher discharge conveyor and overland transport conveyor transferring primary crushed ore (Stream S-101) from Primary Gyratory ... |
| [CV-3101](equipment/CV-3101.md) | CV-3101 — SAG Mill Feed Conveyor | Area 31 - SAG Milling | Conveyor | 1 loops | SAG mill feed conveyor transferring fresh crushed ore (Stream S-301) from stockpile reclaim feeders FE-3101A/B/C and recycled crushed peb... |
| [CY-3201](equipment/CY-3201.md) | CY-3201 — CY-3201 — Secondary Grinding Hydrocyclone Cluster | Area 32 - Ball Milling & Classification | Hydrocyclone | 3 loops | Closed-circuit classification hydrocyclone cluster separating combined SAG and ball mill slurry into coarse underflow (Stream S-323) recy... |
| [FC-4101](equipment/FC-4101.md) | FC-4101 — Rougher Flotation Tank Cells (FC-4101 to FC-4107) | Area 41 - Rougher Flotation | Flotation Cell | 3 loops | Rougher flotation of cyclone overflow (Stream S-324) across a bank of 7 x 300 m3 forced-air tank cells (tagged FC-4101 to FC-4107) in Are... |
| [FC-4301](equipment/FC-4301.md) | FC-4301 — Cleaner Flotation Column | Area 43 - Regrind & Cleaner Flotation | Flotation Column | 1 loops | Cleaner flotation column performing final upgrading of reground rougher concentrate (Stream S-411 ground in ML-4201 to P80 = 38 µm) into ... |
| [FN-4501](equipment/FN-4501.md) | FN-4501 — PAX Mixing Room Extraction Fan | Area 45 - Reagents | Fan | 2 loops | Extraction Fan FN-4501 provides continuous mechanical exhaust ventilation for the enclosed PAX mixing room housing PAX Xanthate Mixing Ta... |
| [FP-5101](equipment/FP-5101.md) | FP-5101 — Concentrate Filter Press | Area 51 - Concentrate Thickening & Filtration | Filter | 2 loops | Vertical plate pressure filter dewatering thickened copper concentrate underflow (Stream S-511 at 51 t/h solids, 40 m3/h slurry, 65.0 wt%... |
| [ML-3101](equipment/ML-3101.md) | ML-3101 — SAG Mill | Area 31 - SAG Milling | Grinding Mill | 7 loops | Primary autogenous/semi-autogenous grinding (SAG) mill processing primary crushed ore (Stream S-301) and recycled crushed pebbles (Stream... |
| [ML-3201](equipment/ML-3201.md) | ML-3201 — Ball Mill | Area 32 - Ball Milling & Classification | Grinding Mill | 3 loops | Secondary ball mill operating in closed circuit with hydrocyclone cluster CY-3201, receiving classified coarse underflow (Stream S-323) a... |
| [ML-4201](equipment/ML-4201.md) | ML-4201 — ML-4201 — Regrind Mill (vertical stirred) | Area 43 - Regrind & Cleaner Flotation | Grinding Mill | 1 loops | Vertical stirred concentrate regrind mill receiving rougher flotation concentrate slurry (Stream S-411) from rougher cells FC-4101 at 215... |
| [PP-3105A](equipment/PP-3105A.md) | PP-3105A — SAG Mill HP Lift Pump A | Area 31 - SAG Milling | Pump | 2 loops | High-pressure positive-displacement lift pump A operating in 1 duty / 1 standby configuration with PP-3105B. Draws ISO VG 460 lubricating... |
| [PP-3105B](equipment/PP-3105B.md) | PP-3105B — SAG Mill HP Lift Pump B | Area 31 - SAG Milling | Pump | 2 loops | High-pressure positive-displacement lift pump B operating in 1 duty / 1 standby configuration with PP-3105A. Draws ISO VG 460 lubricating... |
| [PP-3201A](equipment/PP-3201A.md) | PP-3201A — PP-3201A — Cyclone Feed Slurry Pump (PP-3201A/B duty, PP-3201C standby) | Area 32 - Ball Milling & Classification | Centrifugal Slurry Pump | 3 loops | Centrifugal heavy-duty slurry pump (PP-3201A, operating in 2 duty + 1 standby configuration PP-3201A/B/C) pumping grinding circuit pulp (... |
| [PP-4501A](equipment/PP-4501A.md) | PP-4501A — PAX Dosing Pump | Area 45 - Reagents | Pump | 1 loops | PAX Dosing Pump PP-4501A is a chemical metering pump in Area 45 drawing 20% w/v aqueous potassium amyl xanthate (PAX) solution from buffe... |
| [PP-4511A](equipment/PP-4511A.md) | PP-4511A — Frother Dosing Pump | Area 45 - Reagents | Pump | 1 loops | Frother Dosing Pump PP-4511A is a chemical metering pump located in the bunded Area 45 reagent area. It draws liquid frother from storage... |
| [PP-5101A](equipment/PP-5101A.md) | PP-5101A — Concentrate Thickener Underflow Pump (PP-5101A/B) | Area 51 - Concentrate Thickening & Filtration | Centrifugal Slurry Pump | 1 loops | Centrifugal heavy-duty slurry pump operating in duty/standby configuration (PP-5101A/B) transferring dense thickened copper concentrate s... |
| [PP-6101A](equipment/PP-6101A.md) | PP-6101A — PP-6101A — Tailings Disposal Slurry Pumps (PP-6101A/B/C - 3 Stages in Series) | Area 61 - Tailings Thickening & Pumping | Centrifugal Slurry Pump | 1 loops | Heavy-duty centrifugal slurry booster pump operating as lead pump in a 3-stage series pumping station (PP-6101A/B/C) to transport 2,576 m... |
| [SC-3101](equipment/SC-3101.md) | SC-3101 — SAG Mill Discharge Screen | Area 31 - SAG Milling | Vibrating Screen | 0 loops | Heavy-duty vibrating pebble scalping screen receiving slurry and pebble discharge from the SAG Mill ML-3101 discharge trommel. Performs c... |
| [ST-2101](equipment/ST-2101.md) | ST-2101 — Coarse Ore Stockpile | Area 21 - Primary Crushing | Stockpile | 0 loops | Coarse ore surge stockpile providing intermediate live buffer storage (60,000 t live capacity, equivalent to ~22.3 hours of concentrator ... |
| [TH-5101](equipment/TH-5101.md) | TH-5101 — Concentrate Thickener | Area 51 - Concentrate Thickening & Filtration | Thickener | 1 loops | Continuous high-rate solid-liquid separation thickener (30 m diameter) receiving final copper concentrate pulp (Stream S-431 at 51 t/h so... |
| [TH-6101](equipment/TH-6101.md) | TH-6101 — Tailings Thickener | Area 61 - Tailings Thickening & Pumping | Thickener | 1 loops | Large-diameter high-rate tailings thickener receiving 6,314 m3/h of final flotation tailings (Stream S-611 at 2,637 t/h dry solids, 33.0 ... |
| [TK-3105](equipment/TK-3105.md) | TK-3105 — SAG Mill Lube Oil Reservoir | Area 31 - SAG Milling | Tank | 2 loops | Lube oil storage and conditioning reservoir supplying high-pressure hydrostatic lift pumps PP-3105A/B and low-pressure hydrodynamic lubri... |
| [TK-4101](equipment/TK-4101.md) | TK-4101 — Flotation Conditioning Tank | Area 4100 - Flotation & Beneficiation | Vessel | 1 loops | Agitated conditioning tank receiving secondary hydrocyclone overflow slurry (Stream S-324) from CY-3201 at 2,688 t/h dry solids and 5,969... |
| [TK-4501](equipment/TK-4501.md) | TK-4501 — PAX Xanthate Mixing Tank | Area 45 - Reagents (Xanthate, Frother, Lime) | Reagent Tank | 3 loops | PAX Xanthate Mixing Tank TK-4501 mixes solid potassium amyl xanthate (PAX) with process water to prepare a 20% w/v aqueous collector solu... |
| [TK-4502](equipment/TK-4502.md) | TK-4502 — PAX Dosing Tank | Area 45 - Reagents | Reagent Tank | 1 loops | PAX Dosing Tank TK-4502 acts as an intermediate storage and buffer tank in Area 45 receiving 20% w/v aqueous potassium amyl xanthate (PAX... |
| [TK-4511](equipment/TK-4511.md) | TK-4511 — Frother Storage Tank | Area 45 - Reagents (Xanthate, Frother, Lime) | Reagent Tank | 1 loops | Frother Storage Tank TK-4511 stores 30 m³ of liquid frother reagent in Area 45 within a dedicated containment bund and feeds frother dosi... |
| [TK-4521](equipment/TK-4521.md) | TK-4521 — Milk-of-Lime Tank | Area 45 - Reagents (Xanthate, Frother, Lime) | Reagent Tank | 1 loops | Milk-of-Lime Tank TK-4521 stores and conditions 150 m³ of 20% w/w Ca(OH)2 hydrated lime slurry received from upstream packaged lime slake... |

## 3. Chemical Process Hazards & Runaway Safeguards Register

| Chemical / Hazard Profile | Canonical Path | Critical Process Safety Summary |
| :--- | :--- | :--- |
| [Anionic Polyacrylamide Flocculant Chemical Safety & Slip Hazard Profile (CAS 9003-05-8)](hazards/anionic-polyacrylamide-flocculant.md) | `hazards/anionic-polyacrylamide-flocculant.md` | Chemical safety, extreme wet slip hazard, thickener over-dosing rheology, and handling controls for anionic polyacrylamide flocculant (CA... |
| [Carbon Disulfide (CS2) Chemical Safety & Decomposition Hazard Profile (CAS 75-15-0)](hazards/carbon-disulfide.md) | `hazards/carbon-disulfide.md` | Chemical safety profile, auto-ignition at 90 °C, flash point -30 °C, LEL 1.3%, ACGIH 1 ppm skin notation, TK-4501 room evolution, FN-4501... |
| [Comminution, Classification, Flotation, Tailings & Reagents Process Safety Hazards](hazards/comminution-slurry-hazards.md) | `hazards/comminution-slurry-hazards.md` | Process safety hazards across concentrator lifecycle including comminution, flotation, tailings, and Area 45 reagent hazards (PAX self-he... |
| [MIBC (Methyl Isobutyl Carbinol) Chemical Safety & Hazard Profile (CAS 108-11-2)](hazards/mibc.md) | `hazards/mibc.md` | Chemical safety data, flammability hazards, flash point 41 °C, STOT SE 3 toxicity, storage/handling controls, and discrepancy analysis fo... |
| [Polyglycol Ether Frother (DF-250 Type) Chemical Safety & Hazard Profile (CAS 37286-64-9)](hazards/polyglycol-ether-frother.md) | `hazards/polyglycol-ether-frother.md` | Chemical safety data, combustibility hazards, flash point >100 °C, eye irritation, storage/handling controls, and discrepancy analysis fo... |
| [Potassium Amyl Xanthate (PAX) Chemical Safety & Hazard Profile (CAS 2720-73-2)](hazards/potassium-amyl-xanthate.md) | `hazards/potassium-amyl-xanthate.md` | Chemical safety profile, self-heating solid hazards, spontaneous CS2 evolution, LEL 1.3%, handling and storage safeguards, firefighting p... |
| [Quicklime and Hydrated Lime Chemical Safety & Hazard Profile (CAS 1305-78-8 / 1305-62-0)](hazards/quicklime-hydrated-lime.md) | `hazards/quicklime-hydrated-lime.md` | Chemical safety data, exothermic slaking reaction hazards, skin corrosion 1B / serious eye damage 1, PPE controls, and cross-reagent fire... |

## 4. Instrumentation, Safety Interlocks (SIS) & Overpressure Protection Register

| Subsystem Register | Canonical Path | Scope & Safety Interlock Summary |
| :--- | :--- | :--- |
| [Plant Instrumentation, Process Analysers, Temperature, Bed Level & Relief Valves (RB-4410)](instruments/pressure-instrumentation-and-relief-valves.md) | `instruments/pressure-instrumentation-and-relief-valves.md` | Consolidated plant instrumentation specification covering temperature protection, pressure transmitters, relief valves, pH analysers, rou... |

## 5. Cross-Document Engineering Discrepancies & Safety Warnings (`⚠️ CONFLICT`)

- **[CR-2101 — Primary Gyratory Crusher](equipment/CR-2101.md)**: | Crusher Mechanical Design Throughput | 5,500 (⚠️ CONFLICT vs PFD S-101 2,688 t/h nominal) (RB-4410-PID-21-001 Rev B and Process Data Sheet RB-4410-PS-CR2101 Rev B specify 5,500 t/h ROM ore max throughput, whereas PFD RB-4410-PFD-001 Rev B
- **[CV-2101 — Primary Crusher Discharge Conveyor](equipment/CV-2101.md)**: - ⚠️ CONFLICT / CAPACITY SURGE NOTE: Conveyor CV-2101 must withstand peak instantaneous surges up to 5,500 t/h from CR-2101 (per RB-4410-PID-21-001 Rev B and RB-4410-PS-CR2101 Rev B) while continuous plant mass balance nominal rate is 2,688
- **[CV-3101 — SAG Mill Feed Conveyor](equipment/CV-3101.md)**: - ⚠️ CONFLICT — SAG Trunnion Bearing Trip Setpoint Tripping CV-3101: RB-4410-STD-CE-001 Rev B specifies CV-3101 trip at TAHH 85 °C (1oo2 voting), whereas RB-4410-PS-0034 Rev B and RB-4410-OM-001 Rev 2 document mill bearing trip at TAHH 75 °
- **[CY-3201 — CY-3201 — Secondary Grinding Hydrocyclone Cluster](equipment/CY-3201.md)**: Closed-circuit classification hydrocyclone cluster separating combined SAG and ball mill slurry into coarse underflow (Stream S-323) recycled to ball mill ML-3201 and fine overflow (Stream S-324) sent by gravity to flotation conditioning ta
- **[FC-4301 — Cleaner Flotation Column](equipment/FC-4301.md)**: | Final Concentrate Solids Mass Rate | 51 (⚠️ CONFLICT: Stream S-431 specifies 51 t/h solids in RB-4410-PFD-002 Rev B and RB-4410-PFD-003 Rev B, whereas Drawing RB-4410-PFD-000 Rev B specifies 50.6 t/h solids (26.0% Cu grade). Sizing of thi
- **[FP-5101 — Concentrate Filter Press](equipment/FP-5101.md)**: | Feed Solids Mass Rate | 51 (⚠️ CONFLICT) (Stream S-511 specifies 51 t/h solids in RB-4410-PFD-003 Rev B, whereas Drawing RB-4410-PFD-000 Rev B specifies 50.6 t/h solids (26.0% Cu grade). Sizing and batch chamber cycle times must accommoda
- **[ML-3101 — SAG Mill](equipment/ML-3101.md)**: Primary autogenous/semi-autogenous grinding (SAG) mill processing primary crushed ore (Stream S-301) and recycled crushed pebbles (Stream S-305) in wet primary comminution; discharges via trommel screen to vibrating screen SC-3101 and cyclo
- **[PP-3105A — SAG Mill HP Lift Pump A](equipment/PP-3105A.md)**: | Discharge Relief Valve (PSV-3105) Set Pressure | 180 (⚠️ CONFLICT vs 160 in PS-0032 and 170 system design) (Drawing Note 1 states set pressure shall not exceed system design pressure (170 bar(g)); drawing marks SET 180 bar(g), whereas PS-
- **[PP-3105B — SAG Mill HP Lift Pump B](equipment/PP-3105B.md)**: | Discharge Relief Valve (PSV-3105) Set Pressure | 180 (⚠️ CONFLICT vs 160 in PS-0032 and 170 system design) (Drawing Note 1 states set pressure shall not exceed system design pressure (170 bar(g)); drawing marks SET 180 bar(g), whereas PS-
- **[PP-3201A — PP-3201A — Cyclone Feed Slurry Pump (PP-3201A/B duty, PP-3201C standby)](equipment/PP-3201A.md)**: | Design Volumetric Flow Rate | 5539 (Volumetric slurry throughput per operating duty pump per RB-4410-PFD-001 Rev B; ⚠️ CONFLICT vs 4,650 m³/h rated flow in RB-4410-PS-PP3201 Rev B) | m3/h | RB-4410-PFD-001 Rev B |
- **[PP-4511A — Frother Dosing Pump](equipment/PP-4511A.md)**: | Fluid Handled | Polyglycol ether frother (DF-250 type) / MIBC (⚠️ CONFLICT) (⚠️ CONFLICT: RB-4410-PID-45-001 Rev B specifies Polyglycol ether frother (DF-250 type), whereas RB-4410-PS-TK4511 Rev B specifies MIBC (methyl isobutyl carbinol)
- **[PP-5101A — Concentrate Thickener Underflow Pump (PP-5101A/B)](equipment/PP-5101A.md)**: - ⚠️ CONFLICT — RATED FLOW / OPERATING FLOW: Process Data Sheet RB-4410-PS-PP5101 Rev B specifies a rated slurry flow of 210 m³/h (increased from 180 m³/h in Rev A after filter trade-off; supersedes Rev A), whereas Process Flow Diagram RB-4
- **[PP-6101A — PP-6101A — Tailings Disposal Slurry Pumps (PP-6101A/B/C - 3 Stages in Series)](equipment/PP-6101A.md)**: Heavy-duty centrifugal slurry booster pump operating as lead pump in a 3-stage series pumping station (PP-6101A/B/C) to transport 2,576 m3/h of thickened tailings underflow (Stream S-621 at 2,637 t/h dry solids, 62.0 wt% solids, SG 1.652) a
- **[TH-5101 — Concentrate Thickener](equipment/TH-5101.md)**: | Feed Solids Mass Rate | 51 (⚠️ CONFLICT) (Stream S-431 specifies 51 t/h solids in RB-4410-PFD-003 Rev B and RB-4410-PFD-002 Rev B, whereas Drawing RB-4410-PFD-000 Rev B specifies 50.6 t/h solids (26.0% Cu grade). The 0.4 t/h variance refl
- **[TH-6101 — Tailings Thickener](equipment/TH-6101.md)**: - ⚠️ CONFLICT — Underflow Solids Concentration: RB-4410-PFD-003 Rev B, RB-4410-PS-TH6101 Rev B; RB-4410-PID-61-001 Rev B, RB-4410-PS-TH6101 Rev B, RB-4410-PFD-003 Rev B specifies 62.0 % w/w, whereas RB-4410-OM-001 Rev 2 specifies 62 % solid
- **[TK-3105 — SAG Mill Lube Oil Reservoir](equipment/TK-3105.md)**: | PSV Relief Return Tie-in | PSV-3105 return line connected to reservoir top (⚠️ CONFLICT: P&ID specifies PSV-3105 set at 180 bar(g) returning to TK-3105, whereas PS-0032 Rev B specifies 160 bar(g) and system design pressure is 170 bar(g)) 
- **[TK-4501 — PAX Xanthate Mixing Tank](equipment/TK-4501.md)**: - ⚠️ CONFLICT — Connected Equipment (Downstream): RB-4410-PS-TK4501 Rev B specifies TK-4502, whereas RB-4410-PID-45-001 Rev B, RB-4410-PS-TK4501 Rev B specifies TK-4502 (Downstream PAX chemical dosing vessel) — verify with engineer before H
- **[TK-4511 — Frother Storage Tank](equipment/TK-4511.md)**: | Reagent Stored | Polyglycol ether frother (DF-250 type) / MIBC (⚠️ CONFLICT) (⚠️ CONFLICT: RB-4410-PID-45-001 Rev B specifies Polyglycol ether frother (DF-250 type), whereas RB-4410-PS-TK4511 Rev B, RB-4410-OM-001 Rev 2, and SDS_108-11-2_
- **[TK-4521 — Milk-of-Lime Tank](equipment/TK-4521.md)**: - ⚠️ CONFLICT — Connected Equipment (Downstream): RB-4410-PS-TK4521 Rev B, RB-4410-PFD-002 Rev B specifies TK-4101, whereas RB-4410-PID-45-001 Rev B, RB-4410-PS-TK4521 Rev B specifies TK-4101 (Flotation conditioning tank receiving lime dosi
- **[Anionic Polyacrylamide Flocculant Chemical Safety & Slip Hazard Profile (CAS 9003-05-8)](hazards/anionic-polyacrylamide-flocculant.md)**: ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
- **[Carbon Disulfide (CS2) Chemical Safety & Decomposition Hazard Profile (CAS 75-15-0)](hazards/carbon-disulfide.md)**: ⚠️ **CRITICAL PROCESS SAFETY / VOLATILE AUTO-IGNITION WARNING:**
- **[Comminution, Classification, Flotation, Tailings & Reagents Process Safety Hazards](hazards/comminution-slurry-hazards.md)**: - **Cross-Document Discrepancy (⚠️ CONFLICT):** Drawing `RB-4410-PID-45-001 Rev B` specifies *"Polyglycol ether frother (DF-250 type)"*, whereas Process Data Sheet `RB-4410-PS-TK4511 Rev B`, Operating Manual `RB-4410-OM-001 Rev 2`, and `SDS
- **[MIBC (Methyl Isobutyl Carbinol) Chemical Safety & Hazard Profile (CAS 108-11-2)](hazards/mibc.md)**: ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
- **[Polyglycol Ether Frother (DF-250 Type) Chemical Safety & Hazard Profile (CAS 37286-64-9)](hazards/polyglycol-ether-frother.md)**: ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
- **[Potassium Amyl Xanthate (PAX) Chemical Safety & Hazard Profile (CAS 2720-73-2)](hazards/potassium-amyl-xanthate.md)**: ⚠️ **CRITICAL PROCESS SAFETY / DECOMPOSITION HAZARD WARNING:**
- **[Quicklime and Hydrated Lime Chemical Safety & Hazard Profile (CAS 1305-78-8 / 1305-62-0)](hazards/quicklime-hydrated-lime.md)**: ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
- **[Concentrator Selected Nodes HAZOP Study & Action Item Tracking (RB-4410-STD-HAZOP-001 Rev 1)](hazop/concentrator-hazop-study.md)**: | **ACT-HAZOP-31-02** | HZ-31-02 | Issue formal P&ID redline for `RB-4410-PID-31-002 Rev B` correcting `PSV-3105` set pressure from 180 bar(g) to 160 bar(g) to ensure compliance with 170 bar(g) system design pressure. | Lead Mechanical Engi
- **[Plant Instrumentation, Process Analysers, Temperature, Bed Level & Relief Valves (RB-4410)](instruments/pressure-instrumentation-and-relief-valves.md)**: ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
- **[Copper Concentrator Overall Process Design Basis & Operating Window](parameters/concentrator-design-basis.md)**: | **Plant Service & Scope** | — | Alternative frother (not specified for TK-4511) | — | Evaluated alternative | ⚠️ CONFLICT: Marked on P&ID RB-4410-PID-45-001 Rev B but excluded from baseline TK-4511 by SDS, PS-TK4511, and OM-001 | SDS_3728
- **[SAG Mill ML-3101 Startup, Feed Ramp, Shutdown, Grind-out & Relining Procedure](procedures/sag-mill-operating-procedures.md)**: ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
- **[HAZOP Study - Concentrator (Selected Nodes) (RB-4410-STD-HAZOP-001 Rev 1)](sources/rb-4410-pfd-000.md)**: ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
- **[Safety Data Sheet Summary — MIBC (Methyl Isobutyl Carbinol) (CAS 108-11-2)](sources/sds-108-11-2-mibc.md)**: ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
- **[Safety Data Sheet Summary — Quicklime / Hydrated Lime (CAS 1305-78-8 / 1305-62-0)](sources/sds-1305-78-8-quicklime-hydrated-lime.md)**: ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
- **[Safety Data Sheet Summary — Potassium Amyl Xanthate (PAX) (CAS 2720-73-2)](sources/sds-2720-73-2-potassium-amyl-xanthate.md)**: ⚠️ **CRITICAL PROCESS SAFETY / REAGENT INTEGRITY WARNING:**
- **[Safety Data Sheet Summary — Polyglycol Ether Frother (DF-250 Type) (CAS 37286-64-9)](sources/sds-37286-64-9-polyglycol-ether-frother.md)**: ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
- **[Safety Data Sheet Summary — Carbon Disulfide (Decomposition Product) (CAS 75-15-0)](sources/sds-75-15-0-carbon-disulfide.md)**: ⚠️ **CRITICAL PROCESS SAFETY / VOLATILE DECOMPOSITION HAZARD WARNING:**
- **[Safety Data Sheet Summary — Anionic Polyacrylamide Flocculant (CAS 9003-05-8)](sources/sds-9003-05-8-anionic-polyacrylamide-flocculant.md)**: ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
- **[Site Standard - Grinding Mill Isolation and Entry (RB-4410-SG-005 Rev 3)](standards/grinding-mill-isolation-standard.md)**: ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
- **[Grinding Circuit Abnormal Situations & Corrective Action Guide](troubleshooting/grinding-circuit-abnormal-situations.md)**: ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
- **[Copper Concentrator Plant Overview, Circuit Hierarchy & Reagents](units/copper-concentrator.md)**: - **Concentrate Thickening (TH-5101):** High-rate 30 m diameter thickener receiving 51 t/h dry solids (Stream S-431 at 149 m³/h slurry, 28.0 wt% solids, SG 1.217) from cleaner flotation column FC-4301. Concentrates slurry via gravity sedime

