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

    cfg = get_config()
    root = bundle_root or cfg.output_bundle_dir
    if (
        (not root or not root.exists() or not any(root.rglob("*.md")))
        and bundle_root is None
        and cfg.reference_wiki_dir
        and cfg.reference_wiki_dir.exists()
    ):
        root = cfg.reference_wiki_dir
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


def _extract_equipment_base_id(tag_str: str) -> str:
    """Extract canonical '<PREFIX>-<DIGITS>' base equipment identifier."""
    cleaned = sanitize_tag_filename(tag_str).upper()
    m = re.match(r"^([A-Z]{1,4})[-_]?(\d{3,4})", cleaned)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return cleaned


def derive_canonical_equipment_tag(
    tag: str,
    source_files: list[str] | None = None,
    bundle_root: Path | None = None,
) -> str:
    """Derive the canonical equipment filename tag dynamically from source document metadata and bundle catalog.

    Zero hardcoded equipment tag literals. Enforces strict base equipment ID isolation so shared P&IDs,
    operating manuals, or connected vessel datasheets never cause cross-entity filename collisions.
    """
    safe = sanitize_tag_filename(tag)
    req_base = _extract_equipment_base_id(safe)
    catalog = [c for c in _iter_bundle_catalog(bundle_root) if c["category"] == "equipment"]

    # 1. Extract PS-<TAG> candidates from source_files that share the same base equipment ID
    ps_candidates: list[str] = []
    for src in source_files or []:
        m = re.search(
            r"PS-([A-Z]{1,3})[-_]?(\d{4}[A-Z]*)(?=[_\-\s.]|$)",
            src,
            flags=re.IGNORECASE,
        )
        if m:
            cand = f"{m.group(1).upper()}-{m.group(2).upper()}"
            if _extract_equipment_base_id(cand) == req_base:
                ps_candidates.append(cand)

    for ps_tag in ps_candidates:
        if any(c["stem"].upper() == ps_tag for c in catalog):
            return ps_tag

    # 2. Exact stem match in bundle catalog
    if any(c["stem"].upper() == safe.upper() for c in catalog):
        return next(c["stem"] for c in catalog if c["stem"].upper() == safe.upper())

    # 3. Match existing catalog file only if it shares the same equipment class letter prefix
    #    and explicitly declares this exact equipment tag in its frontmatter or dedicated PS-<TAG>
    ps_code_match = re.match(r"^([A-Z]{1,4})-(\d{3,4})$", req_base)
    dedicated_ps_token = (
        f"ps-{ps_code_match.group(1).lower()}{ps_code_match.group(2)}"
        if ps_code_match
        else ""
    )
    req_prefix = ps_code_match.group(1).upper() if ps_code_match else ""
    raw_tag_lower = tag.strip().lower()
    for c in catalog:
        c_base = _extract_equipment_base_id(str(c["stem"]))
        if req_prefix and not c_base.startswith(f"{req_prefix}-"):
            continue
        head = c["head_lower"]
        if raw_tag_lower and (
            f"tag: {raw_tag_lower}\n" in head
            or f"tag: '{raw_tag_lower}'" in head
            or f'tag: "{raw_tag_lower}"' in head
            or f"title: {raw_tag_lower} " in head
        ):
            return str(c["stem"])
        if dedicated_ps_token and dedicated_ps_token in head and c_base == req_base:
            return str(c["stem"])

    # 4. When no catalog entry exists yet, use matching PS-<TAG> candidate for 2-unit paired tags
    if ps_candidates and re.search(r"\d[A-Z]{2}$", safe):
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

    req_cat = norm_parts[0].lower() if len(norm_parts) > 1 else "root"
    raw_slug = norm_parts[-1].lower() if norm_parts else clean_id.lower()
    core_slug = re.sub(
        r"-(?:process-hazard-profile|chemical-hazard-profile|hazard-profile|process-hazard|hazard|profile|register|specification|procedure|overview|architecture|summary)$",
        "",
        raw_slug,
    ).strip("-")
    if core_slug.startswith(f"{req_cat}-") and len(core_slug) > len(req_cat) + 1:
        core_slug = core_slug.removeprefix(f"{req_cat}-")
    core_id = f"{req_cat}/{core_slug}" if len(norm_parts) > 1 and core_slug else normalized_id

    catalog = _iter_bundle_catalog(bundle_root)
    if not catalog:
        return core_id

    # 1. Exact case-insensitive match against existing bundle concept (clean_id, normalized_id, or core_id)
    candidate_exact_ids = {clean_id.lower(), normalized_id.lower(), core_id.lower()}
    for item in catalog:
        if item["concept_id"].lower() in candidate_exact_ids:
            return str(item["concept_id"])

    # 2. Match by target category + symmetric slug specificity + capped source overlap
    slug_tokens = set(re.findall(r"[a-z0-9]{2,}", core_slug.lower()))
    query_tokens = set(
        re.findall(r"[a-z0-9]{2,}", f"{core_slug} {title} {concept_type}".lower())
    ) - {"md", "okf", "pdf", "extract", "process", "document", "concept", "profile", "register"}
    src_tokens = [Path(s).stem.lower() for s in (sources or []) if s and len(Path(s).stem) >= 4]

    best_id: str | None = None
    best_score = 0.0
    for item in catalog:
        item_cat = str(item["category"]).lower()
        if item_cat != req_cat and not (
            req_cat in ("root", "standards") and item_cat in ("root", "sources", "hazop")
        ):
            continue

        item_stem_tokens = set(re.findall(r"[a-z0-9]{2,}", str(item["stem"]).lower()))
        if not item_stem_tokens:
            continue

        # Direct strict-subset guard between requested slug_tokens and catalog item_stem_tokens:
        # Never collapse a base concept into a multi-word derivative or vice versa (even if only one exists on disk)
        if (
            item_cat == req_cat
            and slug_tokens
            and (slug_tokens < item_stem_tokens or item_stem_tokens < slug_tokens)
        ):
            continue

        overlap = len(query_tokens & item_stem_tokens) / max(1, len(item_stem_tokens))
        slug_jaccard = (
            len(slug_tokens & item_stem_tokens) / max(1, len(slug_tokens | item_stem_tokens))
            if slug_tokens
            else 0.0
        )
        # Require at least one shared stem token (overlap > 0) and shared slug token for non-sources concepts
        has_sds_match = any(
            st.startswith("sds_") and st in item["head_lower"] for st in src_tokens
        )
        if overlap == 0.0 and not has_sds_match:
            continue
        if slug_tokens and req_cat != "sources" and not has_sds_match and slug_jaccard == 0.0:
            continue

        specificity_bonus = 0.15 * len(slug_tokens & item_stem_tokens)
        src_bonus = min(0.35, sum(0.25 for st in src_tokens if st in item["head_lower"]))
        cat_bonus = 0.25 if item_cat == req_cat else 0.0
        score = overlap + (slug_jaccard * 0.5) + specificity_bonus + src_bonus + cat_bonus

        if score > best_score and score >= 0.75:
            best_score = score
            best_id = str(item["concept_id"])

    return best_id or core_id




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
