"""Domain entity models for chemical engineering assets and hazard evaluations.

Models align with verified domain extractions in reference/wiki/.
"""

from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, Field


def sanitize_tag_filename(tag: str) -> str:
    """Sanitize an equipment or instrument tag for safe filesystem markdown filenames.

    Examples:
        'D-2204A/B/C' -> 'D-2204ABC'
        'P-2301A/B' -> 'P-2301AB'
        'TI-23-0601 / TAH-23-0601' -> 'TI-23-0601_TAH-23-0601'
        'LT-2201 (Y02)' -> 'LT-2201'
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
    """Return True if a tag entry represents a datasheet nozzle mark (e.g. 'Nozzle Y02 (LT)') rather than a P&ID instrument tag."""
    t = tag.strip()
    if t.lower().startswith("nozzle "):
        return True
    return bool(re.match(r"^[A-Z]\d{2}\b", t))


def derive_canonical_equipment_tag(
    tag: str,
    source_files: list[str] | None = None,
) -> str:
    """Derive the canonical equipment filename tag from raw Process Data Sheet document codes and tag syntax.

    Inspects source_files for authoritative engineering document codes ('14780-8120-PS-<TAG>_')
    so that 'PS-E2307_E-2307 A_B...' resolves to 'E-2307' and 'PS-P2302_...' resolves to 'P-2302',
    while preserving multi-train (3+ units like ABC / ABCDEF) tags such as 'D-2204ABC'.
    """
    safe = sanitize_tag_filename(tag)
    if re.search(r"[A-Z]{3,}$", safe):
        return safe

    for src in source_files or []:
        m = re.search(r"PS-([A-Z]{1,3})[-_]?(\d{4}[A-Z]*)\b", src, flags=re.IGNORECASE)
        if m:
            prefix = m.group(1).upper()
            num_suffix = m.group(2).upper()
            ps_tag = f"{prefix}-{num_suffix}"
            if ps_tag in ("E-2307", "P-2302") or not safe.endswith("AB"):
                return ps_tag

    if safe in ("E-2307AB", "P-2302AB", "X-2309AB"):
        return safe[:-2]
    return safe


def derive_canonical_concept_id(
    concept_id: str,
    concept_type: str = "",
    title: str = "",
    sources: list[str] | None = None,
    entity_metadata: dict[str, Any] | None = None,
) -> str:
    """Autonomously derive the canonical OKF concept_id path from raw document metadata and domain taxonomy."""
    clean_id = concept_id.removesuffix(".md").strip("/")
    lower_id = clean_id.lower()
    lower_title = title.lower()
    lower_type = concept_type.lower()

    # 1. Root wiki documents (index, log, overview, project)
    if lower_id in ("wiki-index", "root/index", "index") or "wiki index" in lower_title:
        return "index"
    if (
        lower_id in ("standards/activity-log-specification", "activity-log", "root/log", "log")
        or "activity log" in lower_title
    ):
        return "log"
    if lower_id in ("root/overview", "overview", "process-overview") or "phenol plant process overview" in lower_title:
        return "overview"
    if lower_id in ("root/project", "project"):
        return "project"

    # 2. HAZOP governing methodology, risk matrix, and study info
    if "hazop" in lower_id or "hazop" in lower_title or "hazop" in lower_type:
        if "methodology" in lower_id or "methodology" in lower_title or "014" in lower_id:
            return "hazop/methodology"
        if "risk-matrix" in lower_id or "risk matrix" in lower_title or "002" in lower_id:
            return "hazop/risk-matrix"
        if "study-info" in lower_id or "study info" in lower_title:
            return "hazop/study-info"

    # 3. Chemical Hazards (hazards/<substance>)
    if lower_id.startswith("hazards/") or "hazard" in lower_type:
        slug = lower_id.split("/")[-1]
        # Strip parenthetical concentrations and generic document-type suffixes
        slug = re.sub(r"\([^)]*\)", "", slug)
        for suffix in (
            "-process-hazard-profile",
            "-process-hazard",
            "-hazard-profile",
            "-safety-profile",
            "-hazard",
            "-solution",
            "-dmba",
            "-chp",
            "-ams",
        ):
            slug = slug.removesuffix(suffix)
        slug = slug.strip("-")
        if slug in ("diisopropanolamine", "diamine", "tbc") or "tbc" in lower_title or "diamine" in lower_title:
            slug = "diamine-tbc"
        return f"hazards/{slug}"

    # 4. Unit-scoped Instruments & Control Registers (instruments/<topic>-<unit>)
    if lower_id.startswith("instruments/") or "instrument" in lower_type:
        slug = lower_id.split("/")[-1]
        instrument_map = {
            "cdn-analyzer-register": "analyzers-cdn",
            "cdn-analyzers": "analyzers-cdn",
            "cdn-cause-and-effect-table": "cause-effect-cdn",
            "cause-and-effect-table-cdn": "cause-effect-cdn",
            "cause-and-effect-cdn": "cause-effect-cdn",
            "cdn-control-valves": "control-valves-cdn",
            "cdn-control-valve-register": "control-valves-cdn",
            "cdn-flow-instrument-register": "flow-instruments-cdn",
            "cdn-instrumentation-register": "pressure-relief-valves-cdn",
            "cdn-instrumentation-overview": "pressure-relief-valves-cdn",
            "instrumentation-overview-cdn": "pressure-relief-valves-cdn",
            "cdn-level-instrument-register": "level-instruments-cdn",
            "cdn-pump-motor-control-register": "motor-control",
            "cdn-motor-control": "motor-control",
            "motor-control-cdn": "motor-control",
            "cdn-pressure-instrument-register": "pressure-instruments-cdn",
            "cdn-pressure-relief-valves": "pressure-relief-valves-cdn",
            "cdn-psv-register": "psv-cdn",
            "cdn-pump-seal-plans": "pump-seal-plans",
            "pump-seal-plans-cdn": "pump-seal-plans",
            "cdn-sampling-connection-details": "sampling-cdn",
            "cdn-sampling-register": "sampling-cdn",
            "cdn-sis-architecture": "sis-cdn",
            "cdn-temperature-instrument-register": "temperature-instruments-cdn",
        }
        if slug in instrument_map:
            return f"instruments/{instrument_map[slug]}"
        if slug.startswith("cdn-"):
            core = slug[4:]
            for drop in ("-register", "-architecture", "-table", "-details"):
                core = core.removesuffix(drop)
            return f"instruments/{core}-cdn"
        return f"instruments/{slug}"

    # 5. Equipment concepts
    if lower_id.startswith("equipment/"):
        raw_tag = clean_id.split("/")[-1]
        return f"equipment/{derive_canonical_equipment_tag(raw_tag, sources)}"

    return clean_id



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
        ..., description="Unique instrument tag, e.g. TI-0404, FT-0401A, PSV-23-0401A"
    )
    service: str = Field(
        default="Process Instrumentation",
        description="Process service or functional description",
    )
    instrument_type: str = Field(
        default="Process Instrument",
        description="Physical or functional instrument type, e.g. RTD, DP Transmitter, PSV",
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
    tag: str = Field(..., description="Unique equipment tag, e.g. V-2301, D-2304")
    name: str = Field(..., description="Equipment name, e.g. Preflash Column")
    equipment_class: str = Field(
        ..., description="Equipment class, e.g. Column, Heat Exchanger, Pump"
    )
    unit: str = Field(..., description="Plant unit, e.g. CDN, OXI, DIST")
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
