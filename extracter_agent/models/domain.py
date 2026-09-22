"""Domain entity models for chemical engineering assets and hazard evaluations.

Models align with verified domain extractions in reference/wiki/.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class EngineeringParameter(BaseModel):
  parameter: str
  value: str
  unit: str | None = None
  source: str
  note: str | None = None


class ConnectionStream(BaseModel):
  stream_id: str
  temperature: str | None = None
  pressure: str | None = None
  flow_rate: str | None = None
  description: str | None = None
  source: str


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
