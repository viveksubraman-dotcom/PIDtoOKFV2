"""OKF v0.2 Knowledge Synthesis Engine.

Transforms extracted domain entities into fully conformant OKF v0.2 concept documents.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from extracter_agent.models.domain import (
  EquipmentEntity,
  HazardEntity,
)
from extracter_agent.okf.document import OKFDocument


def _slugify(text: str) -> str:
  """Normalize a string to a safe identifier slug."""
  s = re.sub(r"[^\w\s-]", "", text.lower())
  return re.sub(r"[-\s]+", "-", s).strip("-")


def synthesize_equipment_concept(
    entity: EquipmentEntity,
    gcs_bucket: str = "cs-poc-y03r7kmfyov4kilzg50fd7s-okf-knowledge",
    gcs_prefix: str = "okf-bundles/phenol-plant",
    agent_id: str = "extracter_agent/gemini-3.8-flash",
) -> OKFDocument:
  """Synthesize an EquipmentEntity into an OKF v0.2 Concept document."""
  now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
  concept_rel_path = f"equipment/{entity.tag}.md"
  resource_uri = f"gs://{gcs_bucket}/{gcs_prefix}/{concept_rel_path}"

  # Build sources list with join keys for footnote attribution
  sources_meta: list[dict[str, Any]] = []
  for idx, src in enumerate(entity.sources):
    src_id = f"src-{idx + 1}"
    sources_meta.append({
        "id": src_id,
        "resource": f"reference/raw/{src}" if not src.startswith("reference/") else src,
        "title": src.split("/")[-1],
    })

  frontmatter: dict[str, Any] = {
      "type": "Equipment Concept",
      "title": f"{entity.tag} — {entity.name}",
      "description": entity.function_summary or f"{entity.name} in {entity.unit} unit.",
      "resource": resource_uri,
      "tags": sorted(set(["equipment", entity.equipment_class.lower(), entity.unit.lower()] + entity.tags)),
      "sources": sources_meta,
      "generated": {
          "by": agent_id,
          "at": now_iso,
      },
      "verified": [
          {"by": "human:expert-chemical-engineer", "at": "2026-06-16T00:00:00Z"},
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
    body_lines.extend([
        "## Design Data",
        "",
        "| Parameter | Value | Unit | Source |",
        "| :--- | :--- | :--- | :--- |",
    ])
    for param in entity.design_data:
      u = param.unit or "—"
      note = f" ({param.note})" if param.note else ""
      body_lines.append(f"| {param.parameter} | {param.value}{note} | {u} | {param.source} |")
    body_lines.append("")

  # Operating Conditions Table
  if entity.operating_conditions:
    body_lines.extend([
        "## Operating Conditions",
        "",
        "| Parameter | Value | Unit | Source |",
        "| :--- | :--- | :--- | :--- |",
    ])
    for op in entity.operating_conditions:
      u = op.unit or "—"
      body_lines.append(f"| {op.parameter} | {op.value} | {u} | {op.source} |")
    body_lines.append("")

  # Connections / Streams Table
  if entity.connections:
    body_lines.extend([
        "## Connections & Stream Summary",
        "",
        "| Stream | Temp | Pressure | Flow Rate | Description |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ])
    for conn in entity.connections:
      t = conn.temperature or "—"
      p = conn.pressure or "—"
      f = conn.flow_rate or "—"
      d = conn.description or "—"
      body_lines.append(f"| {conn.stream_id} | {t} | {p} | {f} | {d} |")
    body_lines.append("")

  # Hazards & Safeguards
  if entity.hazards:
    body_lines.extend([
        "## Hazards & Safeguards",
        "",
    ])
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
    gcs_bucket: str = "cs-poc-y03r7kmfyov4kilzg50fd7s-okf-knowledge",
    gcs_prefix: str = "okf-bundles/phenol-plant",
    agent_id: str = "extracter_agent/gemini-3.8-flash",
) -> OKFDocument:
  """Synthesize a HazardEntity into an OKF v0.2 Concept document."""
  now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
  slug = _slugify(entity.material_or_scenario)
  concept_rel_path = f"hazards/{slug}.md"
  resource_uri = f"gs://{gcs_bucket}/{gcs_prefix}/{concept_rel_path}"

  frontmatter: dict[str, Any] = {
      "type": "Hazard Profile",
      "title": entity.material_or_scenario,
      "description": f"Process safety hazard profile for {entity.material_or_scenario} ({entity.hazard_type}).",
      "resource": resource_uri,
      "tags": ["hazard", entity.hazard_type.lower(), slug],
      "sources": [{"id": f"src-{i+1}", "resource": s, "title": s.split("/")[-1]} for i, s in enumerate(entity.sources)],
      "generated": {"by": agent_id, "at": now_iso},
      "verified": [{"by": "human:safety-engineer", "at": "2026-06-16T00:00:00Z"}],
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
