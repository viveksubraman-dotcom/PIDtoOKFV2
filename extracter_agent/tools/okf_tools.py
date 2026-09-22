"""ADK FunctionTools for OKF v0.2 Knowledge Synthesis and Validation.

Strictly complies with Rule 11 (FunctionTool docstring contracts, negative constraints).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from extracter_agent.config import get_config
from extracter_agent.models.domain import (
    ConnectionStream,
    EngineeringParameter,
    EquipmentEntity,
    InstrumentLoop,
)
from extracter_agent.okf.indexer import generate_bundle_indexes, update_bundle_log
from extracter_agent.okf.synthesizer import (
    synthesize_equipment_concept,
)
from extracter_agent.okf.validator import validate_okf_bundle


def generate_equipment_okf_tool(
    tag: str,
    name: str,
    equipment_class: str,
    unit: str,
    function_summary: str,
    design_data: list[dict[str, str]],
    operating_conditions: list[dict[str, str]],
    connections: list[dict[str, str]],
    instruments: list[dict[str, str]] | None = None,
    hazards: list[str] | None = None,
    source_files: list[str] | None = None,
    output_bundle_dir: str | None = None,
) -> dict[str, Any]:
    """Construct a validated OKF v0.2 Equipment concept document and save it to the bundle.

    When to use:
        - When synthesizing extracted chemical equipment data into an OKF v0.2 concept.
        - Example: generate_equipment_okf_tool(tag="V-2301", name="Preflash Column", unit="CDN", ...)

    When NOT to use:
        - Do NOT use for raw unstructured PDF documents.
        - Do NOT use for hazard or instrument concepts (use dedicated tools).
        - Do NOT write directly to reference/ directory.

    Args:
        tag: Equipment unique plant identifier, e.g. V-2301, D-2304.
        name: Full equipment title, e.g. Preflash Column.
        equipment_class: Equipment category, e.g. Column, Pump, Heat Exchanger.
        unit: Plant unit code, e.g. CDN, OXI, ALKY, DIST.
        function_summary: Engineering description of the equipment function.
        design_data: List of design parameters with parameter, value, unit, and source.
        operating_conditions: List of operating conditions with parameter, value, unit, and source.
        connections: List of stream connections with stream_id, temperature, pressure, flow_rate.
        instruments: Optional list of P&ID instrument loops associated with this equipment.
        hazards: List of process safety hazard notes and precautions.
        source_files: List of reference source PDF paths.
        output_bundle_dir: Optional destination bundle directory path.

    Returns:
        A dictionary containing generation status, relative path, and document frontmatter.
    """
    cfg = get_config()
    bundle_root = (
        Path(output_bundle_dir) if output_bundle_dir else cfg.output_bundle_dir
    )

    inst_loops = [InstrumentLoop(**i) for i in (instruments or [])]

    entity = EquipmentEntity(
        tag=tag,
        name=name,
        equipment_class=equipment_class,
        unit=unit,
        function_summary=function_summary,
        design_data=[EngineeringParameter(**d) for d in design_data],
        operating_conditions=[
            EngineeringParameter(**op) for op in operating_conditions
        ],
        connections=[ConnectionStream(**c) for c in connections],
        instruments=inst_loops,
        hazards=hazards or [],
        sources=source_files or [],
    )

    doc = synthesize_equipment_concept(
        entity,
        gcs_bucket=cfg.destination_gcs_bucket,
        gcs_prefix=cfg.destination_gcs_prefix,
    )

    # Save to bundle
    equip_dir = bundle_root / "equipment"
    equip_dir.mkdir(parents=True, exist_ok=True)
    output_file = equip_dir / f"{tag}.md"
    output_file.write_text(doc.serialize(), encoding="utf-8")

    # Update log
    update_bundle_log(
        bundle_root,
        "Concept Creation",
        f"Created OKF equipment concept for [{tag} — {name}](/equipment/{tag}.md)",
    )

    return {
        "status": "success",
        "concept_id": f"equipment/{tag}",
        "output_file": str(
            output_file.relative_to(Path.cwd())
            if output_file.is_relative_to(Path.cwd())
            else output_file
        ),
        "title": doc.frontmatter.get("title"),
        "type": doc.frontmatter.get("type"),
        "resource": doc.frontmatter.get("resource"),
        "frontmatter": doc.frontmatter,
    }


def build_okf_indexes_and_validate_tool(
    bundle_dir: str | None = None,
) -> dict[str, Any]:
    """Generate progressive disclosure index.md files and validate the entire OKF bundle.

    When to use:
        - After creating or updating concept documents, to generate index.md files
          and ensure 100% compliance with OKF v0.2 specifications before publishing to GCS.
        - Example: build_okf_indexes_and_validate_tool()

    When NOT to use:
        - Do NOT use before any concepts are written.
        - Do NOT use on arbitrary non-bundle directories.

    Args:
        bundle_dir: Path to the bundle root directory. Defaults to configured output_bundle_dir.

    Returns:
        A dictionary detailing generated index files, total concepts, validation results, and trust tiers.
    """
    cfg = get_config()
    root = Path(bundle_dir) if bundle_dir else cfg.output_bundle_dir
    if not root.exists():
        return {
            "status": "error",
            "error": f"Bundle directory does not exist: {root}",
        }

    written_indexes = generate_bundle_indexes(root)
    validation = validate_okf_bundle(root)

    return {
        "status": "success" if validation["valid"] else "validation_warning",
        "bundle_dir": str(root),
        "indexes_generated": [str(p.name) for p in written_indexes],
        "total_indexes": len(written_indexes),
        "is_valid_okf": validation["valid"],
        "total_documents": validation["total_documents"],
        "trust_tiers": validation["trust_tiers"],
        "errors": validation["errors"],
    }
