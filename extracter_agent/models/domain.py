"""Domain entity models for chemical engineering assets and hazard evaluations.

Models align with verified domain extractions in reference/wiki/.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


def sanitize_tag_filename(tag: str) -> str:
    """Sanitize an equipment or instrument tag for safe filesystem markdown filenames.

    Examples:
        'TK-101A/B/C' -> 'TK-101ABC'
        'P-101A/B' -> 'P-101AB'
        'TI-101 / TAH-101' -> 'TI-101_TAH-101'
        'LT-101 (N1)' -> 'LT-101'
    """
    cleaned = tag.strip()
    # Strip parenthetical nozzle/location remarks such as '(Y02)'
    cleaned = re.sub(r"\s*\([^)]*\)", "", cleaned).strip()
    # Replace ' / ' (paired tags) with '_' and strip direct unit slashes ('A/B/C' -> 'ABC')
    cleaned = re.sub(r"\s+[/\\]\s+", "_", cleaned)
    cleaned = re.sub(r"[/\\]+", "", cleaned)
    cleaned = re.sub(r"[^\w\-]+", "_", cleaned)
    return cleaned.strip("_") or "UNTAGGED"


def is_nozzle_mark_only(tag: str) -> bool:
    """Return True if a tag entry represents a datasheet nozzle mark rather than a P&ID instrument tag."""
    t = tag.strip()
    if t.lower().startswith("nozzle "):
        return True
    return bool(re.match(r"^[A-Z]\d{2}\b", t))


_BUNDLE_CATALOG_CACHE: dict[tuple[str, int, int, int], list[dict[str, Any]]] = {}


def _iter_bundle_catalog(bundle_root: Path | None = None) -> list[dict[str, Any]]:
    """Dynamically inspect existing OKF concept files in the bundle directory."""
    from extracter_agent.config import get_config

    root = bundle_root or get_config().output_bundle_dir
    if not root or not root.exists():
        return []

    md_files = sorted(root.rglob("*.md"))
    latest_child_mtime_ns = max((p.stat().st_mtime_ns for p in md_files), default=0)
    cache_key = (
        str(root.resolve()),
        root.stat().st_mtime_ns,
        len(md_files),
        latest_child_mtime_ns,
    )
    cached = _BUNDLE_CATALOG_CACHE.get(cache_key)
    if cached is not None:
        return cached

    catalog: list[dict[str, Any]] = []
    for md_file in md_files:
        rel = md_file.relative_to(root).as_posix()
        if md_file.name == "index.md" and rel != "index.md":
            continue
        stem_id = rel.removesuffix(".md")
        category = stem_id.split("/")[0] if "/" in stem_id else "root"
        try:
            head = md_file.read_text(encoding="utf-8", errors="ignore")[:2500]
        except Exception:
            head = ""
        catalog.append(
            {
                "concept_id": stem_id,
                "category": category,
                "stem": md_file.stem,
                "head_lower": head.lower(),
            }
        )
    _BUNDLE_CATALOG_CACHE[cache_key] = catalog
    return catalog


def derive_canonical_equipment_tag(
    tag: str,
    source_files: list[str] | None = None,
    bundle_root: Path | None = None,
) -> str:
    """Derive the canonical equipment filename tag dynamically from source document metadata and bundle catalog.

    Zero hardcoded equipment tag literals. Resolves against existing bundle equipment concepts
    citing the same Process Data Sheet or parses the generic 'PS-<TAG>' engineering document code.
    """
    safe = sanitize_tag_filename(tag)
    catalog = [c for c in _iter_bundle_catalog(bundle_root) if c["category"] == "equipment"]

    # 1. If exact sanitized tag already exists in bundle catalog, check if a more specific PS-<TAG> file matches
    src_names = [Path(s).name.lower() for s in (source_files or []) if s]
    ps_candidates: list[str] = []
    for src in source_files or []:
        m = re.search(r"PS-([A-Z]{1,3})[-_]?(\d{4}[A-Z]*)(?=[_\-\s.]|$)", src, flags=re.IGNORECASE)
        if m:
            ps_candidates.append(f"{m.group(1).upper()}-{m.group(2).upper()}")

    for ps_tag in ps_candidates:
        if any(c["stem"].upper() == ps_tag for c in catalog):
            return ps_tag

    if any(c["stem"].upper() == safe.upper() for c in catalog):
        return next(c["stem"] for c in catalog if c["stem"].upper() == safe.upper())

    for src_name in src_names:
        for c in catalog:
            if src_name in c["head_lower"]:
                return str(c["stem"])

    if ps_candidates and not re.search(r"[A-Z]{3,}$", safe):
        return ps_candidates[0]

    return safe


def derive_canonical_concept_id(
    concept_id: str,
    concept_type: str = "",
    title: str = "",
    sources: list[str] | None = None,
    entity_metadata: dict[str, Any] | None = None,
    bundle_root: Path | None = None,
) -> str:
    """Dynamically resolve the canonical OKF concept_id path from bundle catalog metadata and structural rules.

    Zero static lookup dictionaries or plant-specific hardcoded strings.
    """
    clean_id = concept_id.removesuffix(".md").strip("/")
    if not clean_id:
        return "index"

    # Normalize parenthetical qualifiers and whitespace in the candidate slug
    parts = [p for p in clean_id.split("/") if p]
    norm_parts: list[str] = []
    for idx, part in enumerate(parts):
        cleaned_part = re.sub(r"\s*\([^)]*\)", "", part).strip()
        if idx == len(parts) - 1 and parts[0].lower() != "sources":
            cleaned_part = re.sub(r"[^\w\-]+", "-", cleaned_part.lower()).strip("-")
        else:
            cleaned_part = re.sub(r"[^\w\-.]+", "-", cleaned_part).strip("-")
        if cleaned_part:
            norm_parts.append(cleaned_part)

    normalized_id = "/".join(norm_parts) if norm_parts else clean_id

    if normalized_id.lower().startswith("equipment/"):
        raw_tag = clean_id.split("/")[-1]
        return f"equipment/{derive_canonical_equipment_tag(raw_tag, sources, bundle_root)}"

    catalog = _iter_bundle_catalog(bundle_root)
    if not catalog:
        return normalized_id

    # 1. Exact case-insensitive match against existing bundle concept
    for item in catalog:
        if item["concept_id"].lower() == clean_id.lower() or item["concept_id"].lower() == normalized_id.lower():
            return str(item["concept_id"])

    # 2. Match by target category + shared authoritative source files / token overlap
    req_cat = parts[0].lower() if len(parts) > 1 else "root"
    query_tokens = set(
        re.findall(r"[a-z0-9]{2,}", f"{clean_id} {title} {concept_type}".lower())
    ) - {"md", "okf", "pdf", "extract", "process", "document", "concept", "profile", "register"}
    src_tokens = [Path(s).stem.lower() for s in (sources or []) if s and len(Path(s).stem) >= 4]

    best_id: str | None = None
    best_score = 0.0
    for item in catalog:
        item_cat = str(item["category"]).lower()
        # Allow matching within the same category, or resolving root/sources/hazop aliases
        if item_cat != req_cat and not (
            req_cat in ("root", "standards") or item_cat in ("root", "sources", "hazop")
        ):
            continue

        item_tokens = set(re.findall(r"[a-z0-9]{2,}", f"{item['concept_id']} {item['stem']}".lower()))
        overlap = len(query_tokens & item_tokens) / max(1, len(item_tokens))
        src_bonus = sum(0.35 for st in src_tokens if st in item["head_lower"])
        cat_bonus = 0.25 if item_cat == req_cat else 0.0
        score = overlap + src_bonus + cat_bonus

        if score > best_score and score >= 0.55:
            best_score = score
            best_id = str(item["concept_id"])

    return best_id or normalized_id




class EngineeringParameter(BaseModel):
    parameter: str
    value: str
    unit: str | None = None
    source: str = Field(default="Engineering Reference Document")
    note: str | None = None


class ConnectionStream(BaseModel):
    stream_id: str
    temperature: str | None = None
    pressure: str | None = None
    flow_rate: str | None = None
    description: str | None = None
    source: str = Field(default="Engineering Reference Document")


class InstrumentLoop(BaseModel):
    tag: str = Field(
        ..., description="Unique instrument loop tag from P&ID or datasheet"
    )
    service: str = Field(
        default="Process Instrumentation",
        description="Process service or functional description",
    )
    instrument_type: str = Field(
        default="Process Instrument",
        description="Physical or functional instrument type (e.g. RTD, DP Transmitter, PSV)",
    )
    location: str | None = Field(
        default=None, description="Physical installation location or nozzle tap point"
    )
    setpoint_or_range: str | None = Field(
        default=None, description="Calibrated range or operational setpoint"
    )
    interlock_or_alarm: str | None = Field(
        default=None, description="Associated DCS alarm or SIS/ESD trip action"
    )
    source: str = Field(
        default="Engineering Reference Document",
        description="Engineering drawing or datasheet citation",
    )


class EquipmentEntity(BaseModel):
    tag: str = Field(..., description="Unique equipment plant identifier tag")
    name: str = Field(..., description="Descriptive equipment title")
    equipment_class: str = Field(
        ..., description="Equipment class (e.g. Column, Heat Exchanger, Pump, Vessel)"
    )
    unit: str = Field(..., description="Plant unit or process section code")
    tags: list[str] = Field(default_factory=list)
    function_summary: str
    design_data: list[EngineeringParameter] = Field(default_factory=list)
    operating_conditions: list[EngineeringParameter] = Field(default_factory=list)
    instruments: list[InstrumentLoop] = Field(
        default_factory=list,
        description="P&ID instrumentation, transmitters, and control/safety loops associated with this equipment",
    )
    connections: list[ConnectionStream] = Field(default_factory=list)
    hazards: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)


class HazardEntity(BaseModel):
    material_or_scenario: str
    hazard_type: str  # Thermal Runaway, Toxicity, Flammability, Overpressure
    critical_limits: list[str] = Field(default_factory=list)
    safeguards: list[str] = Field(default_factory=list)
    consequences: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)


class HazopNode(BaseModel):
    node_id: str
    node_name: str
    unit: str
    deviations: list[dict[str, Any]] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)


class InstrumentEntity(BaseModel):
    tag: str
    service: str
    unit: str
    instrument_type: str
    normal_value: str | None = None
    alarm_high: str | None = None
    alarm_low: str | None = None
    interlock_action: str | None = None
    sources: list[str] = Field(default_factory=list)
