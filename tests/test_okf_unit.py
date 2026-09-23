"""Unit tests for OKF document model, synthesizer, indexer, and validator."""

import tempfile
from pathlib import Path

from extracter_agent.models.domain import (
    ConnectionStream,
    EngineeringParameter,
    EquipmentEntity,
    InstrumentLoop,
)
from extracter_agent.okf.document import OKFDocument
from extracter_agent.okf.indexer import generate_bundle_indexes, update_bundle_log
from extracter_agent.okf.synthesizer import (
    synthesize_equipment_concept,
)
from extracter_agent.okf.validator import validate_okf_bundle


def test_okf_document_parse_and_serialize():
    """Test basic document parsing and serialization."""
    raw = """---
type: Equipment Concept
title: V-2301 — Preflash Column
tags: [equipment, column, cdn]
---

# V-2301 — Preflash Column

## Function
Primary vacuum flash evaporator.
"""
    doc = OKFDocument.parse(raw)
    assert doc.frontmatter["type"] == "Equipment Concept"
    assert doc.frontmatter["title"] == "V-2301 — Preflash Column"
    assert "Primary vacuum flash evaporator." in doc.body

    serialized = doc.serialize()
    assert serialized.startswith("---\n")
    assert "type: Equipment Concept" in serialized

    # Re-parse
    doc2 = OKFDocument.parse(serialized)
    assert doc2.frontmatter == doc.frontmatter
    assert doc2.body.strip() == doc.body.strip()


def test_synthesize_equipment_concept():
    """Test synthesizing an EquipmentEntity into OKF v0.2."""
    entity = EquipmentEntity(
        tag="V-2301",
        name="Preflash Column",
        equipment_class="Column",
        unit="CDN",
        function_summary="First-stage vacuum evaporator in CDN.",
        design_data=[
            EngineeringParameter(
                parameter="Shell ID", value="6600", unit="mm", source="PS-V2301"
            ),
            EngineeringParameter(
                parameter="T/T Length", value="21000", unit="mm", source="PS-V2301"
            ),
        ],
        operating_conditions=[
            EngineeringParameter(
                parameter="Top Pressure", value="18.5", unit="mmHgA", source="DWG 0004"
            ),
            EngineeringParameter(
                parameter="Top Temp", value="53", unit="°C", source="DWG 0004"
            ),
        ],
        instruments=[
            InstrumentLoop(
                tag="TI-0404",
                service="Column Bottom Temp",
                instrument_type="RTD",
                location="Column Bottom Sump",
                setpoint_or_range="0–200 °C",
                interlock_or_alarm="TXSHH-0404 (UC-2301 ESD)",
                source="DWG 0004",
            ),
            InstrumentLoop(
                tag="FT-0401A",
                service="Feed Flow",
                instrument_type="Flow Transmitter",
                location="Feed Line",
                setpoint_or_range="0–200 t/h",
                interlock_or_alarm="FXSLL-0401A (2oo3)",
                source="DWG 0004",
            ),
        ],
        connections=[
            ConnectionStream(
                stream_id="S229",
                temperature="83",
                description="Oxidate feed",
                source="PFD-0001",
            ),
        ],
        hazards=["CHP thermal runaway risk under elevated temperature."],
        sources=[
            "data_sheets/14780-8120-PS-V2301_V-2301.pdf",
            "pid/14780-8120-25-23-0004.pdf",
        ],
    )

    doc = synthesize_equipment_concept(entity)
    assert doc.frontmatter["type"] == "Equipment Concept"
    assert doc.frontmatter["title"] == "V-2301 — Preflash Column"
    assert "gs://" in doc.frontmatter["resource"]
    assert len(doc.frontmatter["sources"]) == 2
    assert doc.frontmatter["verified"][0]["by"] == "human:expert-chemical-engineer"
    assert doc.frontmatter["status"] == "stable"

    # Verify instrument metadata in frontmatter
    assert len(doc.frontmatter["entity_metadata"]["instruments"]) == 2
    assert doc.frontmatter["entity_metadata"]["instruments"][0]["tag"] == "TI-0404"
    assert doc.frontmatter["entity_metadata"]["instruments"][1]["tag"] == "FT-0401A"

    # Verify Markdown body tables & footnotes
    assert "## Design Data" in doc.body
    assert "| Shell ID | 6600 | mm | PS-V2301 |" in doc.body
    assert "## Operating Conditions" in doc.body
    assert "## Instrumentation & Control Loops (P&ID)" in doc.body
    assert (
        "| [TI-0404](/instruments/TI-0404.md) | Column Bottom Temp | RTD | Column Bottom Sump | 0–200 °C | TXSHH-0404 (UC-2301 ESD) | DWG 0004 |"
        in doc.body
    )
    assert (
        "| [FT-0401A](/instruments/FT-0401A.md) | Feed Flow | Flow Transmitter | Feed Line | 0–200 t/h | FXSLL-0401A (2oo3) | DWG 0004 |"
        in doc.body
    )
    assert "[^src-1]:" in doc.body


def test_bundle_indexes_and_validation():
    """Test bundle directory indexing and validation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        bundle_root = Path(tmpdir)

        # Create subdirectories
        equip_dir = bundle_root / "equipment"
        hazards_dir = bundle_root / "hazards"
        equip_dir.mkdir()
        hazards_dir.mkdir()

        # Write concepts
        doc1 = OKFDocument(
            frontmatter={
                "type": "Equipment Concept",
                "title": "V-2301",
                "description": "Preflash column",
            },
            body="# V-2301\n\nContent here.",
        )
        (equip_dir / "V-2301.md").write_text(doc1.serialize(), encoding="utf-8")

        doc2 = OKFDocument(
            frontmatter={
                "type": "Hazard Profile",
                "title": "CHP",
                "description": "Peroxide hazard",
            },
            body="# CHP\n\nContent here.",
        )
        (hazards_dir / "chp.md").write_text(doc2.serialize(), encoding="utf-8")

        # Generate indexes
        written = generate_bundle_indexes(bundle_root)
        assert len(written) >= 2  # equipment/index.md, hazards/index.md, index.md

        root_index = bundle_root / "index.md"
        assert root_index.exists()
        assert "Subdirectories" in root_index.read_text(encoding="utf-8")

        # Write log.md
        log_path = update_bundle_log(
            bundle_root, "Initialization", "Created test bundle"
        )
        assert log_path.exists()

        # Validate bundle
        val_res = validate_okf_bundle(bundle_root)
        assert val_res["valid"] is True
        assert val_res["total_documents"] == 2
        assert val_res["has_root_index"] is True
        assert val_res["has_root_log"] is True


def test_generate_equipment_okf_tool_multi_unit_slash_tag():
    """Verify multi-unit tags containing slashes (e.g. D-2204A/B/C) write to sanitized filenames without FileNotFoundError."""
    from extracter_agent.tools.okf_tools import generate_equipment_okf_tool

    with tempfile.TemporaryDirectory() as tmpdir:
        res = generate_equipment_okf_tool(
            tag="D-2204A/B/C",
            name="Charcoal Adsorbers",
            equipment_class="Vessel",
            unit="OXI",
            function_summary="Three parallel activated carbon bed adsorbers for vent gas treatment.",
            design_data=[
                {"parameter": "Design Pressure", "value": "3.5", "unit": "kg/cm²g"}
            ],
            operating_conditions=[
                {"parameter": "Operating Temperature", "value": "40", "unit": "°C"}
            ],
            connections=[
                {"stream_id": "N1", "description": "Vent gas inlet"}
            ],
            hazards=["⚠️ CONFLICT — Verify bed regeneration temperature limits."],
            source_files=["14780-8120-PS-D2204_D-2204 PROCESS DATA SHEET_Z1.pdf"],
            instruments=[
                {"tag": "TI-2204A / TAH-2204A", "service": "Bed Temp"}
            ],
            output_bundle_dir=tmpdir,
        )
        assert res["status"] == "success"
        assert res["concept_id"] == "equipment/D-2204ABC"
        expected_file = Path(tmpdir) / "equipment" / "D-2204ABC.md"
        assert expected_file.exists()
        content = expected_file.read_text(encoding="utf-8")
        assert "D-2204A/B/C — Charcoal Adsorbers" in content
        assert "/instruments/TI-2204A_TAH-2204A.md" in content

