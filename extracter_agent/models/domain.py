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
    """
    cleaned = tag.strip()
    # Replace ' / ' (paired tags) with '_' and strip direct unit slashes ('A/B/C' -> 'ABC')
    cleaned = re.sub(r"\s+[/\\]\s+", "_", cleaned)
    cleaned = re.sub(r"[/\\]+", "", cleaned)
    cleaned = re.sub(r"\s+", "_", cleaned)
    return cleaned


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
