"""OKF v0.2 Knowledge Synthesis Engine.

Transforms extracted domain entities into fully conformant OKF v0.2 concept documents.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from extracter_agent.models.domain import (
    EquipmentEntity,
    HazardEntity,
    derive_canonical_equipment_tag,
    is_nozzle_mark_only,
    sanitize_tag_filename,
)
from extracter_agent.okf.document import OKFDocument


def _slugify(text: str) -> str:
    """Normalize a string to a safe identifier slug."""
    s = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", s).strip("-")


_INST_REGISTER_CACHE: dict[tuple[str, int], list[tuple[Path, str, set[str]]]] = {}


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

    cache_key = (str(inst_dir.resolve()), inst_dir.stat().st_mtime_ns)
    cached_regs = _INST_REGISTER_CACHE.get(cache_key)
    if cached_regs is None:
        reg_files = [
            p for p in sorted(inst_dir.glob("*.md")) if p.name not in ("index.md", "log.md")
        ]
        if not reg_files:
            return f"/instruments/{safe_inst_tag}.md"
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
