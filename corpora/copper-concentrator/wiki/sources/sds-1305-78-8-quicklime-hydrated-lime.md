---
type: Source Document
title: Safety Data Sheet Summary — Quicklime / Hydrated Lime (CAS 1305-78-8 / 1305-62-0)
description: Safety Data Sheet summary for quicklime and hydrated lime (CAS 1305-78-8
  / 1305-62-0) used as pH modifier in slaker SL-4521 and storage tank TK-4521, defining
  Skin Corr 1B, Eye Dam 1, exothermic slaking, and Area 45 firefighting controls.
resource: gs://ut-interaction-demo-okf-knowledge/okf-bundles/copper-concentrator/sources/sds-1305-78-8-quicklime-hydrated-lime.md
tags:
- area 45
- cas 1305-62-0
- cas 1305-78-8
- chemical-burns
- exothermic
- eye damage 1
- hazard profile
- hydrated-lime
- lime
- milk-of-lime
- process safety
- quicklime
- reagents
- sds
- skin corrosion 1b
- sl-4521
- standards
- tk-4521
sources:
- id: src-1
  resource: corpora/copper-concentrator/raw/standards/SDS_1305-78-8_quicklime---hydrated-lime.pdf
  title: SDS_1305-78-8_quicklime---hydrated-lime.pdf
generated:
  by: extracter_agent/gemini-3.8-flash
  at: '2026-09-30T18:32:07Z'
verified:
- by: human:expert-chemical-engineer
  at: '2026-09-30T18:32:07Z'
- by: process:okf-validation-suite
  at: '2026-09-30T18:32:07Z'
status: stable
entity_metadata:
  firefighting_restriction: Do not use water jet on burning xanthate
  document_class: Chemical Safety Data Sheet Summary
  handling_storage: Store cool and dry, away from acids and ignition sources; keep
    containers closed
  plant_usage: pH modifier in SL-4521 / TK-4521
  chemical_formulas:
  - CaO
  - Ca(OH)2
  target_equipment:
  - SL-4521
  - TK-4521
  - TK-4101
  - FC-4101
  target_unit: Area 45 - Reagents
  firefighting_media:
  - Dry chemical
  - CO2
  - Foam
  exposure_controls:
  - Local exhaust ventilation
  - Chemical goggles
  - Nitrile gloves
  - Respirator where exposure limits exceeded
  ghs_classification:
  - Skin corrosion 1B
  - Serious eye damage 1
  physical_hazard: Exothermic with water (slaker)
  cas_numbers:
  - 1305-78-8
  - 1305-62-0
  chemical_names:
  - Quicklime
  - Hydrated lime
  first_aid:
    inhalation: Remove to fresh air; seek medical attention
    eyes_and_skin: Flush with water for 15 minutes; seek medical attention
---

# Safety Data Sheet Summary — Quicklime / Hydrated Lime (CAS 1305-78-8 / 1305-62-0)

> ⚠️ **CRITICAL PROCESS SAFETY / DISCREPANCY WARNING:**
> - **EXOTHERMIC SLAKING REACTION & THERMAL BOILING HAZARD (SL-4521):** Quicklime (calcium oxide, $\text{CaO}$) undergoes an intensely exothermic slaking reaction with water ($\text{CaO} + \text{H}_2\text{O} \rightarrow \text{Ca(OH)}_2 + \Delta H_{\text{rxn}} = -65.2\text{ kJ/mol}$) inside packaged lime slaker `SL-4521`. Inadequate slaking water flow or high lime-to-water ratios can cause local boiling, steam generation, and violent ejection/splattering of boiling alkaline slurry ($\text{pH} > 12.5$, temperature $> 90\ ^\circ\text{C}$), presenting catastrophic thermal and chemical burn risks to personnel.
> - **GHS HEALTH CLASSIFICATION (SKIN CORROSION 1B / SERIOUS EYE DAMAGE 1):** Both quicklime ($\text{CaO}$) and hydrated lime ($\text{Ca(OH)}_2$) are classified as **Skin Corrosion Category 1B** and **Serious Eye Damage Category 1**. Contact with dust, dry powder, or slurry causes severe, irreversible corneal burns, blindness, and deep chemical necrotic skin ulceration. Continuous personal protective equipment (chemical splash goggles, full face shield, nitrile/neoprene gauntlets, and respirators) and verified safety shower / eyewash stations within 10 seconds of travel are mandatory.
> - **CROSS-REAGENT FIREFIGHTING RESTRICTION IN AREA 45:** SDS Section 5 mandates: *"Dry chemical, CO2 or foam. Do not use water jet on burning xanthate."* Area 45 houses potassium amyl xanthate (`TK-4501`) and frother (`TK-4511`) adjacent to milk-of-lime storage (`TK-4521`). High-pressure water jets must never be directed toward burning xanthate due to explosive scattering and toxic $\text{CS}_2$ gas generation.
> - **DOWNSTREAM PROCESS BUFFERING & PH CONTROL (TK-4521 / AIC-4101):** Hydrated lime prepared in `SL-4521` is transferred to 150 m³ storage tank `TK-4521` as a 20% w/w $\text{Ca(OH)}_2$ suspension. Dosing is regulated via closed-loop controller `AIC-4101` to maintain flotation feed conditioning tank `TK-4101` at target pH 10.5 (AL 10.0 / AH 11.2) for pyrite depression.

## Document Overview & Engineering Scope
- **Document Title:** Safety Data Sheet Summary - Quicklime / hydrated lime
- **Source File:** `corpora/copper-concentrator/raw/standards/SDS_1305-78-8_quicklime---hydrated-lime.pdf`
- **Document Class:** Chemical Safety Data Sheet Summary / Site Standard
- **Chemical Names:** Quicklime (Calcium Oxide) / Hydrated Lime (Calcium Hydroxide)
- **CAS Registry Numbers:** 
  - Quicklime: **1305-78-8**
  - Hydrated Lime: **1305-62-0**
- **Chemical Formulas:** $\text{CaO}$ / $\text{Ca(OH)}_2$
- **Target Plant Duty / Service:** Slurry pH modifier and pyrite depressant in Area 45 (Reagents), prepared in Lime Slaker `SL-4521`, stored in Milk-of-Lime Tank `TK-4521`, and dosed to Rougher Conditioning Tank `TK-4101` and Rougher Cells `FC-4101`.
- **Authority Scope:** Site demonstration summary. Supplier SDS governs authoritative design and statutory transport compliance.

## SDS Technical Specifications & Parameters
| SDS Section | Parameter / Topic | Value / Specification | Engineering & Operational Implications |
| :--- | :--- | :--- | :--- |
| **Section 1: Identification** | Product / Chemical Name | Quicklime / hydrated lime | Primary inorganic alkaline reagent and pH modifier |
| **Section 1: Identification** | Plant Use & Equipment Tag | `SL-4521` / `TK-4521`, pH modifier | Slaker `SL-4521` hydrates quicklime; 150 m³ tank `TK-4521` stores 20% w/w slurry |
| **Section 1: Identification** | CAS Numbers | 1305-78-8 ($\text{CaO}$) / 1305-62-0 ($\text{Ca(OH)}_2$) | Chemical Abstract Service identifiers for unslaked and slaked lime |
| **Section 1: Identification** | Formula / Type | $\text{CaO}$ / $\text{Ca(OH)}_2$ | Alkaline earth oxide and hydroxide |
| **Section 2: Hazards Identification** | GHS Health Hazards | Skin corrosion 1B / serious eye damage 1 | Causes irreversible ocular burns and tissue necrosis upon moisture contact |
| **Section 2: Hazards Identification** | Physical / Reaction Hazards | Exothermic with water (slaker) | Severe heat generation during hydration ($\Delta H = -65.2\text{ kJ/mol}$) |
| **Section 4: First Aid Measures** | Inhalation | Remove to fresh air; seek medical attention | Prevent pulmonary edema and severe respiratory mucosal ulceration |
| **Section 4: First Aid Measures** | Eye & Skin Contact | Flush eyes and skin with water for 15 minutes; seek medical attention | Emergency deluge within 10 seconds; prolonged irrigation critical for bases |
| **Section 5: Fire Fighting Measures** | Extinguishing Media | Dry chemical, $\text{CO}_2$ or foam | Standard extinguishing agents; avoid excess uncontained runoff |
| **Section 5: Fire Fighting Measures** | Cross-Reagent Precaution | Do not use water jet on burning xanthate | Area 45 multi-reagent directive to prevent molten xanthate and $\text{CS}_2$ dispersion |
| **Section 7: Handling & Storage** | Environmental Conditions | Store cool and dry, away from acids and ignition sources | Moisture triggers spontaneous hydration; acids cause violent neutralization |
| **Section 7: Handling & Storage** | Containment Management | Keep containers closed | Prevent atmospheric moisture absorption and airborne dust dispersion |
| **Section 8: Exposure Controls & PPE** | Ventilation Controls | Local exhaust ventilation | Mandatory dust extraction on lime bag break / slaker hopper feed |
| **Section 8: Exposure Controls & PPE** | Eye Protection | Chemical goggles | Tight-fitting chemical splash goggles preventing dust and liquid ingress |
| **Section 8: Exposure Controls & PPE** | Hand / Dermal Protection | Nitrile gloves | Impermeable chemical barrier against corrosive alkaline slurries |
| **Section 8: Exposure Controls & PPE** | Respiratory Protection | Respirator where exposure limits may be exceeded | Particulate / alkaline mist filtering respirator for dry powder transfer |

## Cross-Document Reconciliation & Plant Integration
1. **Equipment Association & Service Scope:**
   - SDS explicitly references use in: **`SL-4521` / `TK-4521`, pH modifier**.
   - P&ID `RB-4410-PID-45-001 Rev B` depicts `TK-4521` (Milk-of-Lime Tank) and references Lime Slaker `SL-4521` in Note 3 (*"Lime slaker SL-4521 is defined on vendor package drawing"*).
   - Process Data Sheet `RB-4410-PS-TK4521 Rev B` specifies a 150 m³ atmospheric vertical tank holding 20% w/w $\text{Ca(OH)}_2$ slurry with continuous mechanical agitation to prevent settling and scaling.
   - Operating Manual `RB-4410-OM-001 Rev 2` Section 8 explicitly details the violent exothermic hazard of lime slaking in `SL-4521` and the dosing control via `AIC-4101` to maintain rougher feed alkalinity at target pH 10.5.

2. **Reactivity & Heat of Slaking in SL-4521:**
   - Quicklime ($\text{CaO}$, CAS 1305-78-8) fed into slaker `SL-4521` reacts rapidly with process water. If the water ratio drops, the slaking temperature escalates above 90 °C, generating steam pockets that can eject caustic lime slurry out of slaker inspection ports.
   - The slurry is quenched and diluted to 20% w/w $\text{Ca(OH)}_2$ before gravity overflowing into `TK-4521`.

3. **Multi-Reagent Fire & Hazard Precaution in Area 45:**
   - Section 5 of the SDS includes the specific caution: *"Do not use water jet on burning xanthate."* This directly reinforces Area 45 segregation between the lime slaking area and potassium amyl xanthate (PAX) mixing tank `TK-4501`. Water jets on burning PAX cause violent splattering and accelerate hydrolysis into toxic, flammable carbon disulfide ($\text{CS}_2$, auto-ignition temperature 90 °C).

## Affected Plant Entities & Cross-References
- **Equipment Concepts:**
  - `equipment/TK-4521` (Milk-of-Lime Tank)
  - `equipment/SL-4521` (Packaged Lime Slaker)
  - `equipment/TK-4101` (Flotation Conditioning Tank)
  - `equipment/FC-4101` (Rougher Flotation Tank Cells)
- **Hazard Profiles:**
  - `hazards/quicklime-hydrated-lime` (Quicklime & Hydrated Lime Chemical Safety & Hazard Profile)
  - `hazards/comminution-slurry-hazards` (Comminution, Classification, Flotation, Tailings & Reagents Process Safety Hazards)
- **Unit Overviews:**
  - `units/flotation` (Flotation and Regrind Circuit)
  - `units/copper-concentrator` (Overall Concentrator Plant Overview)

## References & Sources
[^src-1]: SDS_1305-78-8_quicklime---hydrated-lime.pdf (corpora/copper-concentrator/raw/standards/SDS_1305-78-8_quicklime---hydrated-lime.pdf)
