---
type: Hazard Profile
title: Quicklime and Hydrated Lime Chemical Safety & Hazard Profile (CAS 1305-78-8
  / 1305-62-0)
description: Chemical safety data, exothermic slaking reaction hazards, skin corrosion
  1B / serious eye damage 1, PPE controls, and cross-reagent firefighting protocols
  for quicklime and hydrated lime in SL-4521 and TK-4521.
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/hazards/quicklime-hydrated-lime.md
tags:
- area 45
- cas 1305-62-0
- cas 1305-78-8
- chemical-burns
- chemical-safety
- exothermic-reaction
- eye-damage
- first-aid
- hazard profile
- hydrated-lime
- lime
- lime-slaker
- milk-of-lime
- process safety
- quicklime
- reagents
- sds
- skin-corrosion
- sl-4521
- standards
- tk-4521
sources:
- id: src-1
  resource: corpora/copper-concentrator/raw/standards/SDS_1305-78-8_quicklime---hydrated-lime.pdf
  title: SDS_1305-78-8_quicklime---hydrated-lime.pdf
- id: src-2
  resource: corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-TK4521_MILK-OF-LIME TANK PROCESS
    DATA SHEET_B.pdf
  title: RB-4410-PS-TK4521_MILK-OF-LIME TANK PROCESS DATA SHEET_B.pdf
- id: src-3
  resource: corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR
    OPERATING MANUAL_R2.pdf
  title: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf
- id: src-4
  resource: corpora/copper-concentrator/raw/pid/RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER
    & LIME_B.pdf
  title: RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T18:32:41Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T18:32:41Z'
- by: process:okf-validation-suite
  at: '2026-09-30T18:32:41Z'
status: stable
entity_metadata:
  ppe:
  - Chemical splash goggles
  - Full face shield
  - Nitrile gauntlets
  - Particulate respirator
  target_unit: Area 45 - Reagents
  chemical_formulas:
  - CaO
  - Ca(OH)2
  ghs_classification:
  - Skin corrosion 1B
  - Serious eye damage 1
  dosing_target_ph: 10.5
  exothermic_reaction:
    heat_generation: Strongly exothermic with water in slaker SL-4521
    delta_h_kj_mol: -65.2
  cas_numbers:
  - 1305-78-8
  - 1305-62-0
  storage_tank_tag: TK-4521
  slurry_concentration_pct_ww: 20
  ph_alarms:
    ah: 11.2
    al: 10
  storage_volume_m3: 150
  target_equipment:
  - SL-4521
  - TK-4521
  - TK-4101
  - FC-4101
  chemical_names:
  - Quicklime
  - Hydrated lime
  first_aid:
    inhalation: Remove to fresh air; seek medical attention
    eyes_and_skin: Flush with water for 15 minutes; seek medical attention
  dosing_controller: AIC-4101
---

# Quicklime and Hydrated Lime Chemical Safety & Hazard Profile (CAS 1305-78-8 / 1305-62-0)

> ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
> - **EXOTHERMIC SLAKING REACTION & ERUPTION HAZARD (SL-4521):** Quicklime (calcium oxide, $\text{CaO}$) hydration with water in lime slaker `SL-4521` is intensely exothermic:
>   $$\text{CaO} + \text{H}_2\text{O} \rightarrow \text{Ca(OH)}_2 \quad (\Delta H = -65.2\text{ kJ/mol})$$
>   If the water-to-lime ratio falls below design specifications, local boiling occurs rapidly, leading to steam generation, pressure buildup, and violent eruption of scalding caustic slurry ($\text{pH} > 12.5$, temperature $> 90\ ^\circ\text{C}$). Personnel must observe vendor operating envelopes, automated water flow permissives, and wear full face shields and chemical gauntlets.
> - **GHS HEALTH HAZARD — SEVERE CHEMICAL BURNS & CORNEAL OPACITY:** Both quicklime and hydrated lime are categorized as **Skin Corrosion Category 1B** and **Serious Eye Damage Category 1**. Contact with calcium hydroxide slurry or unslaked calcium oxide dust causes saponification of dermal lipids, deep tissue necrosis, and irreversible corneal liquefactive necrosis leading to permanent blindness. Deluge safety showers and eyewash stations must be reachable within 10 seconds of travel time from all points in `SL-4521` and `TK-4521`.
> - **MULTI-REAGENT FIREFIGHTING PRECAUTION (AREA 45):** In accordance with SDS Section 5, standard extinguishing media include dry chemical powder, $\text{CO}_2$, or foam. A critical negative directive applies in Area 45: **"Do not use water jet on burning xanthate."** Directing solid water streams onto potassium amyl xanthate (`TK-4501`) causes dynamic splashing of molten xanthate and accelerates hydrolysis into toxic, explosive carbon disulfide ($\text{CS}_2$) vapor (auto-ignition temperature 90 °C).
> - **SLURRY SANDING & SCALE DEPOSITION (TK-4521):** Milk-of-lime slurry at 20% w/w $\text{Ca(OH)}_2$ has a high settling velocity. Loss of mechanical agitation in `TK-4521` or stagnation in dosing headers to `TK-4101` causes rapid settling, irreversible compaction, and calcium carbonate scaling. Recirculating ring mains and automated clean water flush systems are mandatory.

## Chemical Identification & Physical Properties
| Parameter | Quicklime ($\text{CaO}$) | Hydrated Lime ($\text{Ca(OH)}_2$) | Source Citation |
| :--- | :--- | :--- | :--- |
| **Chemical Name** | Calcium Oxide | Calcium Hydroxide | SDS_1305-78-8_quicklime---hydrated-lime.pdf |
| **Common Synonyms** | Burnt lime, unslaked lime, pebble lime | Slaked lime, milk-of-lime (slurry), pickling lime | SDS_1305-78-8_quicklime---hydrated-lime.pdf, RB-4410-PS-TK4521 Rev B |
| **CAS Registry Number** | **1305-78-8** | **1305-62-0** | SDS_1305-78-8_quicklime---hydrated-lime.pdf |
| **Chemical Formula** | $\text{CaO}$ | $\text{Ca(OH)}_2$ | SDS_1305-78-8_quicklime---hydrated-lime.pdf |
| **Molecular Weight** | 56.08 g/mol | 74.09 g/mol | Chemical standard |
| **Physical Appearance** | White to grey-white pebble / granules | Fine white powder or 20% w/w aqueous slurry | RB-4410-PS-TK4521 Rev B, SDS |
| **Aqueous Slurry pH** | Strongly alkaline ($\approx 12.5$ in sat. soln) | Strongly alkaline ($\approx 12.5$ in sat. soln) | RB-4410-OM-001 Rev 2, RB-4410-PS-TK4521 Rev B |
| **GHS Classification** | Skin Corr. 1B / Eye Dam. 1 | Skin Corr. 1B / Eye Dam. 1 | SDS_1305-78-8_quicklime---hydrated-lime.pdf |
| **Heat of Hydration** | $-65.2\text{ kJ/mol}$ ($-1,164\text{ kJ/kg CaO}$) | Exothermic dissolution heat | SDS, RB-4410-OM-001 Rev 2 Sec 8 |
| **Target Plant Equipment** | Packaged Lime Slaker `SL-4521` | Milk-of-Lime Tank `TK-4521` (150 m³ storage) | SDS, RB-4410-PID-45-001 Rev B |
| **Dosing Role & Destination** | Raw material feed to slaker `SL-4521` | Dosed to `TK-4101` on `AIC-4101` (target 10.5 pH) | RB-4410-PFD-002 Rev B, RB-4410-OM-001 Rev 2 |

## Process Safety Hazards, Failure Modes & Safeguards
| Failure Mode / Hazard Event | Initiating Event | Consequences & Severity | Engineered Safeguards & Operational Controls |
| :--- | :--- | :--- | :--- |
| **Slaker Thermal Runaway & Boiling Eruption** | Low water flow to `SL-4521` or quicklime overfeed during slaking | Violent boiling of slurry, steam expulsion, caustic slurry eruptions ($>90\ ^\circ\text{C}$, $\text{pH} > 12$) spraying operators | Water-to-lime ratio control; slaker feed shutoff interlock on low dilution water; vented slaker hood with scrubbed exhaust; mandatory full-face shields and gauntlets |
| **Ocular Destruction & Chemical Skin Burns** | Pipe flange rupture, sampling splash, or dust inhalation during lime handling | Irreversible blindness from corneal burn; severe chemical necrotic ulceration of skin | Safety shower and eyewash stations within 10 seconds of travel; chemical splash goggles; full face shield; nitrile/neoprene gauntlets; long apron |
| **Cross-Reagent Fire Escalation (Area 45)** | High-pressure water jet applied to xanthate fire during adjacent emergency | Violent dispersion of burning xanthate, flash vaporization, massive toxic $\text{CS}_2$ gas generation | Strict SDS firefighting directive: Do not use water jet on burning xanthate; deploy dry chemical, $\text{CO}_2$, or foam; water spray only for cooling vessels |
| **Milk-of-Lime Sanding & Line Plugging** | Agitator mechanical trip in `TK-4521` or low slurry flow in distribution header | Dense 20% w/w slurry consolidates at tank bottom or plugs lines, starving flotation circuit of lime | Continuous mechanical agitation in 150 m³ vessel `TK-4521`; recirculating ring main loop; automated clean water flushing on pump shutdown |
| **Rougher Alkalinity Excursion & Pyrite Activation** | Dosing pump failure or lime line plugging allowing feed pH to drop below 10.0 | Pyrite floats into rougher concentrate, diluting copper grade; accelerates PAX hydrolysis into toxic $\text{CS}_2$ | Closed-loop pH controller `AIC-4101` (setpoint 10.5 pH, low alarm `AL 10.0`, high alarm `AH 11.2`); automatic standby dosing pump cut-in |
| **Inadvertent Acid-Base Neutralization** | Spill of acidic reagent into lime bund or accidental cross-connection | Highly exothermic neutralization reaction, acid mist evolution, boiling acid/base spray | Strict physical segregation of lime storage from acid storage; independent containment bunding; keyed hose connections |

## Emergency Response & First Aid Measures
- **Inhalation:** Immediately move casualty to fresh air. If breathing is labored or has stopped, administer artificial respiration or oxygen by trained medical personnel. Seek immediate medical attention.
- **Skin Contact:** Immediately remove all contaminated clothing, shoes, and equipment under a deluge safety shower. Flush affected skin surfaces with copious volumes of running water for at least 15 minutes. Decontaminate or properly discard contaminated articles. Seek prompt medical evaluation.
- **Eye Contact:** Instantly flood open eyes with clean water from an emergency eyewash station for at least 15 minutes, holding eyelids apart. Do not apply chemical neutralizing agents. Arrange immediate ophthalmological evaluation and transport to a hospital.
- **Ingestion:** If victim is conscious, rinse mouth thoroughly with water and give copious water to drink. Do NOT induce vomiting. Never give anything by mouth to an unconscious person. Obtain urgent hospital medical care.
- **Firefighting Protocol:**
  - **Permitted Extinguishing Agents:** Dry chemical powder, carbon dioxide ($\text{CO}_2$), or alcohol-resistant foam.
  - **Water Application Rules:** Quicklime reacts exothermically with water; apply water fog or spray only to cool un-ignited exposed containers from a protected distance if adequate water volume is available.
  - **Critical Warning:** **Do not use water jet on burning xanthate.** In Area 45, avoid spraying high-pressure water streams into the PAX mixing room (`TK-4501`) where molten xanthate and flammable $\text{CS}_2$ vapors will be dispersed.

## Safe Handling, Storage & Occupational Exposure Controls
- **Engineering Controls:**
  - Provide continuous local exhaust ventilation at all lime powder charging points, bag splitters, and slaker feed hoppers.
  - Enclose lime conveying and transfer spools to eliminate fugitive alkaline dust emission.
  - Maintain functional eyewash and safety shower stations within 10 seconds of all quicklime and hydrated lime handling units (`SL-4521`, `TK-4521`, `TK-4101`).
- **Handling Practices:**
  - Avoid all direct physical contact with eyes, skin, and work clothing.
  - Keep chemical storage containers and bags tightly closed and protected against moisture and relative humidity.
  - Prohibit storage near strong acids, oxidizers, and unsealed organic chemicals.
- **Personal Protective Equipment (PPE):**
  - **Eye & Face Protection:** Tight-fitting chemical splash goggles combined with an approved full-face shield (ANSI/ISEA Z87.1 approved).
  - **Hand Protection:** Heavy-duty chemical-resistant nitrile or neoprene gauntlet-style gloves.
  - **Skin & Body Protection:** Chemical-resistant overalls, impermeable rubber apron, and chemical-resistant safety boots.
  - **Respiratory Protection:** Approved particulate air-purifying respirator (N95 or P100 filter) during dry lime handling; powered air-purifying respirator (PAPR) where dust levels exceed occupational exposure limits.

## Cross-Document Alignment & Equipment Traceability
| Topic / Parameter | SDS_1305-78-8_quicklime---hydrated-lime.pdf | RB-4410-PS-TK4521 Rev B | RB-4410-PID-45-001 Rev B | RB-4410-OM-001 Rev 2 | Reconciled Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Chemical Identity** | Quicklime ($\text{CaO}$, CAS 1305-78-8) / Hydrated lime ($\text{Ca(OH)}_2$, CAS 1305-62-0) | Hydrated lime slurry ($Ca(OH)_2$) | Hydrated lime / Milk-of-lime | Hydrated lime ($Ca(OH)_2$) prepared from quicklime | Fully aligned across all documents |
| **Slaker Package Tag** | `SL-4521`, pH modifier | `SL-4521` (Lime Slaker) | `SL-4521` (vendor package per Note 3) | `SL-4521` (Sec 8, exothermic slaker) | Fully aligned: vendor package supplying `TK-4521` |
| **Storage Tank Tag** | `TK-4521` | `TK-4521` (150 m³ storage tank) | `TK-4521` (Area 45 Reagent tank) | `TK-4521` (Sec 3.45 & Sec 8) | Fully aligned across all documents |
| **Slurry Concentration** | pH modifier | 20% w/w $\text{Ca(OH)}_2$ suspension | 20% w/w slurry | 20% w/w $\text{Ca(OH)}_2$ slurry | Fully aligned at 20% w/w |
| **Downstream Destination** | pH modifier | `TK-4101` (Flotation Conditioning Tank) | Dosing line to `TK-4101` | `TK-4101` rougher feed | Fully aligned |
| **pH Target & Control** | pH modifier | Target 10.5 pH via `AIC-4101` | Closed-loop `AIC-4101` (Note 4 per OM-001) | Target 10.5 pH (AL 10.0 / AH 11.2) | Fully aligned |
| **Exothermic Hazard** | Exothermic with water (slaker) | Operating Temp: Ambient (tank) | Note 3 (vendor package) | Sec 8: Strongly exothermic slaking reaction | Fully aligned; slaker manages hydration heat |

## References & Sources
[^src-1]: SDS_1305-78-8_quicklime---hydrated-lime.pdf (corpora/copper-concentrator/raw/standards/SDS_1305-78-8_quicklime---hydrated-lime.pdf)
[^src-2]: RB-4410-PS-TK4521_MILK-OF-LIME TANK PROCESS DATA SHEET_B.pdf (corpora/copper-concentrator/raw/data_sheets/RB-4410-PS-TK4521_MILK-OF-LIME TANK PROCESS DATA SHEET_B.pdf)
[^src-3]: RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf (corpora/copper-concentrator/raw/operating_manuals/RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf)
[^src-4]: RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf (corpora/copper-concentrator/raw/pid/RB-4410-PID-45-001_P&ID REAGENTS - XANTHATE, FROTHER & LIME_B.pdf)
