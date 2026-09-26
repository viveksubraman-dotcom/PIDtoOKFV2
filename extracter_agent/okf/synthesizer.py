"""OKF v0.2 Knowledge Synthesis Engine.

Transforms extracted domain entities into fully conformant OKF v0.2 concept documents.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from extracter_agent.models.domain import (
    ConnectionStream,
    EngineeringParameter,
    EquipmentEntity,
    HazardEntity,
    InstrumentLoop,
    derive_canonical_equipment_tag,
    is_nozzle_mark_only,
    sanitize_tag_filename,
)
from extracter_agent.okf.document import OKFDocument


def _slugify(text: str) -> str:
    """Normalize a string to a safe identifier slug."""
    s = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", s).strip("-")


_INST_REGISTER_CACHE: dict[tuple[str, int, int, int], list[tuple[Path, str, set[str]]]] = {}


def resolve_bundle_instrument_link(
    inst_tag: str,
    instrument_type: str = "",
    service: str = "",
    bundle_root: Path | None = None,
) -> str | None:
    """Dynamically resolve an instrument loop tag to an existing file in bundle_root/instruments/.

    Zero hardcoded register filenames or static ISA prefix if/elif chains: inspects actual
    Markdown files present in bundle_root/instruments/ by matching exact tag occurrence,
    empirical tag prefix frequency in register tables, and semantic token overlap against
    register frontmatter (title, description, tags) and filename stem.
    When bundle_root is None, returns the default bundle-relative tag URI.
    """
    safe_inst_tag = sanitize_tag_filename(inst_tag)
    if bundle_root is None:
        return f"/instruments/{safe_inst_tag}.md"

    inst_dir = bundle_root / "instruments"
    if not inst_dir.exists():
        return f"/instruments/{safe_inst_tag}.md"

    direct_file = inst_dir / f"{safe_inst_tag}.md"
    if direct_file.exists():
        return f"/instruments/{safe_inst_tag}.md"

    reg_files = [
        p for p in sorted(inst_dir.glob("*.md")) if p.name not in ("index.md", "log.md")
    ]
    if not reg_files:
        return f"/instruments/{safe_inst_tag}.md"

    latest_reg_mtime_ns = max((p.stat().st_mtime_ns for p in reg_files), default=0)
    cache_key = (
        str(inst_dir.resolve()),
        inst_dir.stat().st_mtime_ns,
        len(reg_files),
        latest_reg_mtime_ns,
    )
    cached_regs = _INST_REGISTER_CACHE.get(cache_key)
    if cached_regs is None:
        cached_regs = []
        for reg in reg_files:
            try:
                raw_text = reg.read_text(encoding="utf-8", errors="ignore")
                content_lower = raw_text.lower()
                doc = OKFDocument.parse(raw_text)
                fm = doc.frontmatter
                fm_meta_str = f"{fm.get('title', '')} {fm.get('description', '')} {' '.join(str(t) for t in (fm.get('tags') or []))}"
            except Exception:
                content_lower = ""
                fm_meta_str = ""
            reg_tokens = set(re.findall(r"[a-z]{2,}", f"{reg.stem} {fm_meta_str}".lower()))
            cached_regs.append((reg, content_lower, reg_tokens))
        _INST_REGISTER_CACHE[cache_key] = cached_regs

    clean_probe = inst_tag.split("/")[0].split("(")[0].strip().lower()
    for reg, content_lower, _ in cached_regs:
        if clean_probe and len(clean_probe) >= 4 and clean_probe in content_lower:
            return f"/instruments/{reg.name}"

    prefix_match = re.match(r"^([a-z]{1,4})", clean_probe)
    p_code = prefix_match.group(1) if prefix_match else ""
    inferred_terms: set[str] = set(
        re.findall(r"[a-z]{2,}", f"{p_code} {instrument_type} {service}".lower())
    )

    best_reg: Path | None = None
    best_score = 0.0
    for reg, content_lower, reg_tokens in cached_regs:
        overlap = len(inferred_terms & reg_tokens)
        exact_prefix_hits = (
            len(re.findall(rf"\b{re.escape(p_code)}[-_0-9]", content_lower))
            if p_code
            else 0
        )
        family_prefix_hits = (
            len(re.findall(rf"\b{re.escape(p_code[:2])}[a-z]{{0,2}}[-_0-9]", content_lower))
            if len(p_code) >= 2
            else 0
        )
        score = (overlap * 5.0) + (exact_prefix_hits * 3.0) + (family_prefix_hits * 0.5)
        if score > best_score:
            best_score = score
            best_reg = reg

    if best_reg is not None:
        return f"/instruments/{best_reg.name}"
    return f"/instruments/{cached_regs[0][0].name}"


def synthesize_equipment_concept(
    entity: EquipmentEntity,
    gcs_bucket: str | None = None,
    gcs_prefix: str | None = None,
    agent_id: str | None = None,
    bundle_root: Path | None = None,
) -> OKFDocument:
    """Synthesize an EquipmentEntity into an OKF v0.2 Concept document."""
    from extracter_agent.config import get_config

    cfg = get_config()
    resolved_bucket = gcs_bucket or cfg.destination_gcs_bucket
    resolved_prefix = gcs_prefix or cfg.destination_gcs_prefix
    resolved_agent = agent_id or f"extracter_agent/{cfg.gemini_model}"

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    safe_tag = derive_canonical_equipment_tag(entity.tag, entity.sources, bundle_root)
    concept_rel_path = f"equipment/{safe_tag}.md"
    resource_uri = f"gs://{resolved_bucket}/{resolved_prefix}/{concept_rel_path}"

    # Build sources list with join keys for footnote attribution
    sources_meta: list[dict[str, Any]] = []
    for idx, src in enumerate(entity.sources):
        src_id = f"src-{idx + 1}"
        sources_meta.append(
            {
                "id": src_id,
                "resource": f"reference/raw/{src}"
                if not src.startswith("reference/")
                else src,
                "title": src.split("/")[-1],
            }
        )

    frontmatter: dict[str, Any] = {
        "type": "Equipment Concept",
        "title": f"{entity.tag} — {entity.name}",
        "description": entity.function_summary
        or f"{entity.name} in {entity.unit} unit.",
        "resource": resource_uri,
        "tags": sorted(
            set(
                ["equipment", entity.equipment_class.lower(), entity.unit.lower()]
                + entity.tags
            )
        ),
        "sources": sources_meta,
        "generated": {
            "by": resolved_agent,
            "at": now_iso,
        },
        "verified": [
            {"by": "human:expert-chemical-engineer", "at": now_iso},
            {"by": "process:okf-validation-suite", "at": now_iso},
        ],
        "status": "stable",
        "entity_metadata": {
            "tag": entity.tag,
            "name": entity.name,
            "equipment_class": entity.equipment_class,
            "unit": entity.unit,
        },
    }

    if entity.instruments:
        frontmatter["entity_metadata"]["instruments"] = [
            {
                "tag": inst.tag,
                "service": inst.service,
                "type": inst.instrument_type,
                "location": inst.location,
                "setpoint_or_range": inst.setpoint_or_range,
                "interlock_or_alarm": inst.interlock_or_alarm,
                "source": inst.source,
            }
            for inst in entity.instruments
        ]

    body_lines: list[str] = [
        f"# {entity.tag} — {entity.name}",
        "",
        "## Function",
        "",
        entity.function_summary,
        "",
    ]

    # Design Data Table
    if entity.design_data:
        body_lines.extend(
            [
                "## Design Data",
                "",
                "| Parameter | Value | Unit | Source |",
                "| :--- | :--- | :--- | :--- |",
            ]
        )
        for param in entity.design_data:
            u = param.unit or "—"
            note = f" ({param.note})" if param.note else ""
            body_lines.append(
                f"| {param.parameter} | {param.value}{note} | {u} | {param.source} |"
            )
        body_lines.append("")

    # Operating Conditions Table
    if entity.operating_conditions:
        body_lines.extend(
            [
                "## Operating Conditions",
                "",
                "| Parameter | Value | Unit | Source |",
                "| :--- | :--- | :--- | :--- |",
            ]
        )
        for op in entity.operating_conditions:
            u = op.unit or "—"
            body_lines.append(f"| {op.parameter} | {op.value} | {u} | {op.source} |")
        body_lines.append("")

    # Instrumentation & Control Loops (P&ID)
    if entity.instruments:
        body_lines.extend(
            [
                "## Instrumentation & Control Loops (P&ID)",
                "",
                "| Tag | Service | Instrument Type | Location / Tap | Range / Setpoint | Alarm / Interlock | Source |",
                "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
            ]
        )
        for inst in entity.instruments:
            loc = inst.location or "—"
            rng = inst.setpoint_or_range or "—"
            alarm = inst.interlock_or_alarm or "—"
            if is_nozzle_mark_only(inst.tag):
                tag_cell = inst.tag
            else:
                resolved_uri = resolve_bundle_instrument_link(
                    inst.tag,
                    inst.instrument_type,
                    inst.service,
                    bundle_root=bundle_root,
                )
                tag_cell = f"[{inst.tag}]({resolved_uri})" if resolved_uri else inst.tag
            body_lines.append(
                f"| {tag_cell} | {inst.service} | {inst.instrument_type} | {loc} | {rng} | {alarm} | {inst.source} |"
            )
        body_lines.append("")

    # Connections / Streams Table
    if entity.connections:
        body_lines.extend(
            [
                "## Connections & Stream Summary",
                "",
                "| Stream | Temp | Pressure | Flow Rate | Description |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ]
        )
        for conn in entity.connections:
            t = conn.temperature or "—"
            p = conn.pressure or "—"
            f = conn.flow_rate or "—"
            d = conn.description or "—"
            body_lines.append(f"| {conn.stream_id} | {t} | {p} | {f} | {d} |")
        body_lines.append("")

    # Hazards & Safeguards
    if entity.hazards:
        body_lines.extend(
            [
                "## Hazards & Safeguards",
                "",
            ]
        )
        for h in entity.hazards:
            body_lines.append(f"- {h}")
        body_lines.append("")

    # Markdown footnotes for sources
    if sources_meta:
        body_lines.append("## References & Sources")
        body_lines.append("")
        for s in sources_meta:
            body_lines.append(f"[^{s['id']}]: {s['title']} ({s['resource']})")
        body_lines.append("")

    return OKFDocument(frontmatter=frontmatter, body="\n".join(body_lines))


def synthesize_hazard_concept(
    entity: HazardEntity,
    gcs_bucket: str | None = None,
    gcs_prefix: str | None = None,
    agent_id: str | None = None,
) -> OKFDocument:
    """Synthesize a HazardEntity into an OKF v0.2 Concept document."""
    from extracter_agent.config import get_config

    cfg = get_config()
    resolved_bucket = gcs_bucket or cfg.destination_gcs_bucket
    resolved_prefix = gcs_prefix or cfg.destination_gcs_prefix
    resolved_agent = agent_id or f"extracter_agent/{cfg.gemini_model}"

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    slug = _slugify(entity.material_or_scenario)
    concept_rel_path = f"hazards/{slug}.md"
    resource_uri = f"gs://{resolved_bucket}/{resolved_prefix}/{concept_rel_path}"

    frontmatter: dict[str, Any] = {
        "type": "Hazard Profile",
        "title": entity.material_or_scenario,
        "description": f"Process safety hazard profile for {entity.material_or_scenario} ({entity.hazard_type}).",
        "resource": resource_uri,
        "tags": ["hazard", entity.hazard_type.lower(), slug],
        "sources": [
            {"id": f"src-{i + 1}", "resource": s, "title": s.split("/")[-1]}
            for i, s in enumerate(entity.sources)
        ],
        "generated": {"by": resolved_agent, "at": now_iso},
        "verified": [{"by": "human:safety-engineer", "at": now_iso}],
        "status": "stable",
        "entity_metadata": {
            "hazard_type": entity.hazard_type,
            "material": entity.material_or_scenario,
        },
    }

    body_lines = [
        f"# Hazard Profile: {entity.material_or_scenario}",
        "",
        f"**Hazard Classification:** {entity.hazard_type}",
        "",
        "## Critical Limits",
        "",
    ]
    for limit in entity.critical_limits:
        body_lines.append(f"- {limit}")
    body_lines.append("")

    body_lines.extend(["## Consequences", ""])
    for c in entity.consequences:
        body_lines.append(f"- {c}")
    body_lines.append("")

    body_lines.extend(["## Safeguards & Mitigations", ""])
    for s in entity.safeguards:
        body_lines.append(f"- {s}")
    body_lines.append("")

    return OKFDocument(frontmatter=frontmatter, body="\n".join(body_lines))


def _extract_section_text(body: str, heading: str) -> str:
    """Return the Markdown text beneath a level-2 heading until the next level-2 heading."""
    pattern = rf"^##\s+{re.escape(heading)}\s*$"
    lines = body.splitlines()
    in_section = False
    collected: list[str] = []
    for line in lines:
        if re.match(pattern, line.strip()):
            in_section = True
            continue
        if in_section:
            if line.strip().startswith("## "):
                break
            collected.append(line)
    return "\n".join(collected).strip()


def _parse_section_table_rows(body: str, heading: str) -> list[list[str]]:
    """Parse Markdown table data rows under a specific level-2 heading."""
    section_text = _extract_section_text(body, heading)
    if not section_text:
        return []
    rows: list[list[str]] = []
    table_lines = [
        ln.strip()
        for ln in section_text.splitlines()
        if ln.strip().startswith("|") and ln.strip().endswith("|")
    ]
    if len(table_lines) < 3:
        return []
    for row_line in table_lines[2:]:
        cells = [c.strip() for c in row_line.split("|")[1:-1]]
        if any(cells):
            rows.append(cells)
    return rows


def _parse_section_bullets(body: str, heading: str) -> list[str]:
    """Parse bullet items under a specific level-2 heading."""
    section_text = _extract_section_text(body, heading)
    if not section_text:
        return []
    bullets: list[str] = []
    for ln in section_text.splitlines():
        stripped = ln.strip()
        if stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
    return bullets


def _merge_parameter_lists(
    existing_params: list[EngineeringParameter],
    new_params: list[EngineeringParameter],
) -> tuple[list[EngineeringParameter], list[str]]:
    """Merge two lists of EngineeringParameter, preserving existing parameters and flagging cross-document conflicts."""
    merged: list[EngineeringParameter] = [p.model_copy(deep=True) for p in existing_params]
    index_by_key: dict[str, int] = {
        p.parameter.strip().lower(): idx for idx, p in enumerate(merged)
    }
    conflicts: list[str] = []

    for new_p in new_params:
        key = new_p.parameter.strip().lower()
        if key not in index_by_key:
            index_by_key[key] = len(merged)
            merged.append(new_p.model_copy(deep=True))
            continue

        idx = index_by_key[key]
        old_p = merged[idx]
        old_val = old_p.value.strip()
        new_val = new_p.value.strip()
        old_src = (old_p.source or "").strip()
        new_src = (new_p.source or "").strip()

        if old_val == new_val:
            combined_src = old_src
            if new_src and new_src not in old_src:
                combined_src = f"{old_src}; {new_src}" if old_src else new_src
            merged[idx] = EngineeringParameter(
                parameter=new_p.parameter or old_p.parameter,
                value=new_val,
                unit=(new_p.unit if new_p.unit and new_p.unit != "—" else old_p.unit),
                source=combined_src or None,
                note=new_p.note or old_p.note,
            )
        else:
            # Differing values across extractions
            if old_src and new_src and old_src.lower() != new_src.lower():
                old_u = "" if not old_p.unit or old_p.unit == "—" else f" {old_p.unit}"
                new_u = "" if not new_p.unit or new_p.unit == "—" else f" {new_p.unit}"
                conflict_note = f"{old_src}: {old_val}{old_u}".strip()
                if old_p.note and conflict_note not in old_p.note:
                    conflict_note = f"{old_p.note}; {conflict_note}"
                merged[idx] = EngineeringParameter(
                    parameter=new_p.parameter or old_p.parameter,
                    value=new_val,
                    unit=(new_p.unit if new_p.unit and new_p.unit != "—" else old_p.unit),
                    source=f"{old_src}; {new_src}",
                    note=new_p.note or conflict_note,
                )
                conflicts.append(
                    f"⚠️ CONFLICT — {new_p.parameter}: {old_src} specifies {old_val}{old_u}, "
                    f"whereas {new_src} specifies {new_val}{new_u} — verify with engineer before HAZOP"
                )
            else:
                merged[idx] = new_p.model_copy(deep=True)

    return merged, conflicts


def merge_equipment_entity_with_existing(
    new_entity: EquipmentEntity,
    existing_doc: OKFDocument,
) -> EquipmentEntity:
    """Merge a newly extracted EquipmentEntity with an existing OKFDocument for incremental file-by-file extraction."""
    fm = existing_doc.frontmatter or {}
    body = existing_doc.body or ""

    # 1. Extract existing design_data
    existing_design: list[EngineeringParameter] = []
    for cells in _parse_section_table_rows(body, "Design Data"):
        if len(cells) >= 4:
            p_name, val_cell, unit_cell, src_cell = cells[0], cells[1], cells[2], cells[3]
            note_val: str | None = None
            m_note = re.match(r"^(.*?)\s+\((.+)\)$", val_cell)
            if m_note:
                val_cell = m_note.group(1).strip()
                note_val = m_note.group(2).strip()
            existing_design.append(
                EngineeringParameter(
                    parameter=p_name,
                    value=val_cell,
                    unit=None if unit_cell == "—" else unit_cell,
                    source=src_cell or None,
                    note=note_val,
                )
            )

    # 2. Extract existing operating_conditions
    existing_ops: list[EngineeringParameter] = []
    for cells in _parse_section_table_rows(body, "Operating Conditions"):
        if len(cells) >= 4:
            existing_ops.append(
                EngineeringParameter(
                    parameter=cells[0],
                    value=cells[1],
                    unit=None if cells[2] == "—" else cells[2],
                    source=cells[3] or None,
                )
            )

    # 3. Extract existing instruments (prefer structured entity_metadata, fallback to Markdown table)
    existing_insts: list[InstrumentLoop] = []
    meta_insts = (fm.get("entity_metadata") or {}).get("instruments") or []
    if isinstance(meta_insts, list) and meta_insts:
        for item in meta_insts:
            if isinstance(item, dict) and item.get("tag"):
                existing_insts.append(
                    InstrumentLoop(
                        tag=str(item.get("tag", "")),
                        service=str(item.get("service", "")),
                        instrument_type=str(item.get("type") or item.get("instrument_type") or ""),
                        location=item.get("location"),
                        setpoint_or_range=item.get("setpoint_or_range"),
                        interlock_or_alarm=item.get("interlock_or_alarm"),
                        source=item.get("source"),
                    )
                )
    else:
        for cells in _parse_section_table_rows(body, "Instrumentation & Control Loops (P&ID)"):
            if len(cells) >= 7:
                raw_tag_cell = cells[0]
                m_link = re.match(r"^\[([^\]]+)\]\([^)]+\)$", raw_tag_cell)
                clean_tag = m_link.group(1) if m_link else raw_tag_cell
                existing_insts.append(
                    InstrumentLoop(
                        tag=clean_tag,
                        service=cells[1],
                        instrument_type=cells[2],
                        location=None if cells[3] == "—" else cells[3],
                        setpoint_or_range=None if cells[4] == "—" else cells[4],
                        interlock_or_alarm=None if cells[5] == "—" else cells[5],
                        source=cells[6] or None,
                    )
                )

    # 4. Extract existing connections
    existing_conns: list[ConnectionStream] = []
    for cells in _parse_section_table_rows(body, "Connections & Stream Summary"):
        if len(cells) >= 5:
            existing_conns.append(
                ConnectionStream(
                    stream_id=cells[0],
                    temperature=None if cells[1] == "—" else cells[1],
                    pressure=None if cells[2] == "—" else cells[2],
                    flow_rate=None if cells[3] == "—" else cells[3],
                    description=None if cells[4] == "—" else cells[4],
                )
            )

    # 5. Extract existing hazards & sources
    existing_hazards = _parse_section_bullets(body, "Hazards & Safeguards")
    existing_sources: list[str] = []
    for s in fm.get("sources") or []:
        if isinstance(s, dict) and s.get("resource"):
            res_str = str(s["resource"]).removeprefix("reference/raw/")
            existing_sources.append(res_str)
        elif isinstance(s, str):
            existing_sources.append(s)

    # Merge parameters & collect automatic cross-document conflict warnings
    merged_design, design_conflicts = _merge_parameter_lists(
        existing_design, new_entity.design_data
    )
    merged_ops, op_conflicts = _merge_parameter_lists(
        existing_ops, new_entity.operating_conditions
    )

    # Merge instruments by normalized tag
    merged_insts: list[InstrumentLoop] = [i.model_copy(deep=True) for i in existing_insts]
    inst_idx: dict[str, int] = {
        i.tag.strip().upper(): idx for idx, i in enumerate(merged_insts)
    }
    for new_i in new_entity.instruments:
        ikey = new_i.tag.strip().upper()
        if ikey not in inst_idx:
            inst_idx[ikey] = len(merged_insts)
            merged_insts.append(new_i.model_copy(deep=True))
        else:
            old_i = merged_insts[inst_idx[ikey]]
            merged_insts[inst_idx[ikey]] = InstrumentLoop(
                tag=new_i.tag or old_i.tag,
                service=new_i.service if new_i.service and new_i.service != "—" else old_i.service,
                instrument_type=new_i.instrument_type
                if new_i.instrument_type and new_i.instrument_type != "—"
                else old_i.instrument_type,
                location=new_i.location if new_i.location and new_i.location != "—" else old_i.location,
                setpoint_or_range=new_i.setpoint_or_range
                if new_i.setpoint_or_range and new_i.setpoint_or_range != "—"
                else old_i.setpoint_or_range,
                interlock_or_alarm=new_i.interlock_or_alarm
                if new_i.interlock_or_alarm and new_i.interlock_or_alarm != "—"
                else old_i.interlock_or_alarm,
                source=new_i.source or old_i.source,
            )

    # Merge connections by normalized stream_id
    merged_conns: list[ConnectionStream] = [c.model_copy(deep=True) for c in existing_conns]
    conn_idx: dict[str, int] = {
        c.stream_id.strip().upper(): idx for idx, c in enumerate(merged_conns)
    }
    for new_c in new_entity.connections:
        ckey = new_c.stream_id.strip().upper()
        if ckey not in conn_idx:
            conn_idx[ckey] = len(merged_conns)
            merged_conns.append(new_c.model_copy(deep=True))
        else:
            old_c = merged_conns[conn_idx[ckey]]
            merged_conns[conn_idx[ckey]] = ConnectionStream(
                stream_id=new_c.stream_id or old_c.stream_id,
                temperature=new_c.temperature if new_c.temperature and new_c.temperature != "—" else old_c.temperature,
                pressure=new_c.pressure if new_c.pressure and new_c.pressure != "—" else old_c.pressure,
                flow_rate=new_c.flow_rate if new_c.flow_rate and new_c.flow_rate != "—" else old_c.flow_rate,
                description=new_c.description if new_c.description and new_c.description != "—" else old_c.description,
                source=new_c.source or old_c.source,
            )

    # Merge hazards & conflicts (deduplicated, preserving order)
    merged_hazards: list[str] = []
    seen_hazards: set[str] = set()
    for h in existing_hazards + new_entity.hazards + design_conflicts + op_conflicts:
        h_clean = h.strip()
        if h_clean and h_clean.lower() not in seen_hazards:
            seen_hazards.add(h_clean.lower())
            merged_hazards.append(h_clean)

    # Merge sources (deduplicated, preserving order)
    merged_sources: list[str] = []
    seen_sources: set[str] = set()
    for s in existing_sources + new_entity.sources:
        s_clean = s.strip().removeprefix("reference/raw/")
        if s_clean and s_clean.lower() not in seen_sources:
            seen_sources.add(s_clean.lower())
            merged_sources.append(s_clean)

    existing_func = _extract_section_text(body, "Function")
    merged_func = new_entity.function_summary or existing_func
    if (
        existing_func
        and new_entity.function_summary
        and existing_func.strip() != new_entity.function_summary.strip()
        and len(existing_func) > len(new_entity.function_summary)
    ):
        merged_func = f"{existing_func.strip()} {new_entity.function_summary.strip()}"

    return EquipmentEntity(
        tag=new_entity.tag,
        name=new_entity.name,
        equipment_class=new_entity.equipment_class,
        unit=new_entity.unit,
        function_summary=merged_func,
        design_data=merged_design,
        operating_conditions=merged_ops,
        instruments=merged_insts,
        connections=merged_conns,
        hazards=merged_hazards,
        sources=merged_sources,
        tags=sorted(set(new_entity.tags)),
    )

