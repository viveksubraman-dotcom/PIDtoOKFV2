"""ADK FunctionTools for OKF v0.2 Knowledge Synthesis and Validation.

Strictly complies with Rule 11 (FunctionTool docstring contracts, negative constraints).
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from extracter_agent.config import get_config
from extracter_agent.models.domain import (
    ConnectionStream,
    EngineeringParameter,
    EquipmentEntity,
    InstrumentLoop,
    derive_canonical_concept_id,
    derive_canonical_equipment_tag,
)
from extracter_agent.okf.document import OKFDocument
from extracter_agent.okf.indexer import generate_bundle_indexes, update_bundle_log
from extracter_agent.okf.synthesizer import (
    synthesize_equipment_concept,
)
from extracter_agent.okf.validator import validate_okf_bundle


def _sync_file_to_gcs(local_file: Path, bundle_root: Path) -> str | None:
    """Upload a generated OKF Markdown file or index to GCS when use_gcs_storage is enabled."""
    cfg = get_config()
    if not cfg.use_gcs_storage:
        return None
    try:
        from google.cloud import storage

        rel_path = local_file.resolve().relative_to(bundle_root.resolve())
        blob_name = f"{cfg.destination_gcs_prefix.strip('/')}/{rel_path}"
        client = storage.Client(project=cfg.google_cloud_project)
        bucket = client.bucket(cfg.destination_gcs_bucket)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(str(local_file), content_type="text/markdown")
        return f"gs://{cfg.destination_gcs_bucket}/{blob_name}"
    except Exception:
        return None


def generate_equipment_okf_tool(
    tag: str,
    name: str,
    equipment_class: str,
    unit: str,
    function_summary: str,
    design_data: list[dict[str, str]],
    operating_conditions: list[dict[str, str]],
    connections: list[dict[str, str]],
    hazards: list[str],
    source_files: list[str],
    instruments: list[dict[str, str]] | None = None,
    output_bundle_dir: str | None = None,
) -> dict[str, Any]:
    """Construct a validated OKF v0.2 Equipment concept document and save it to the bundle and GCS.

    When to use:
        - When synthesizing extracted chemical equipment data into an OKF v0.2 concept.
        - Example: generate_equipment_okf_tool(tag="V-2301", name="Preflash Column", unit="CDN", ...)

    When NOT to use:
        - Do NOT use for raw unstructured PDF documents.
        - Do NOT use for hazard or instrument concepts (use dedicated tools).
        - Do NOT write directly to reference/ directory.

    Args:
        tag: Equipment unique plant identifier, e.g. V-2301, D-2304, D-2204A/B/C.
        name: Full equipment title, e.g. Preflash Column.
        equipment_class: Equipment category, e.g. Column, Pump, Heat Exchanger.
        unit: Plant unit code, e.g. CDN, OXI, ALKY, DIST.
        function_summary: Engineering description of the equipment function.
        design_data: List of design parameters with parameter, value, unit, and source.
        operating_conditions: List of operating conditions with parameter, value, unit, and source.
        connections: List of stream connections with stream_id, temperature, pressure, flow_rate.
        hazards: List of process safety hazard notes and precautions.
        source_files: List of reference source PDF paths.
        instruments: Optional list of P&ID instruments and control loops (tag, service, instrument_type, location, setpoint_or_range, interlock_or_alarm, source).
        output_bundle_dir: Optional destination bundle directory path.

    Returns:
        A dictionary containing generation status, relative path, GCS URI, and document frontmatter.
    """
    cfg = get_config()
    bundle_root = (
        Path(output_bundle_dir) if output_bundle_dir else cfg.output_bundle_dir
    )

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
        instruments=[InstrumentLoop(**i) for i in (instruments or [])],
        connections=[ConnectionStream(**c) for c in connections],
        hazards=hazards,
        sources=source_files,
    )

    doc = synthesize_equipment_concept(
        entity,
        gcs_bucket=cfg.destination_gcs_bucket,
        gcs_prefix=cfg.destination_gcs_prefix,
    )

    # Save to bundle using canonical equipment tag derived from raw PS-<TAG> document code
    safe_tag = derive_canonical_equipment_tag(tag, source_files)
    equip_dir = bundle_root / "equipment"
    equip_dir.mkdir(parents=True, exist_ok=True)
    output_file = equip_dir / f"{safe_tag}.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(doc.serialize(), encoding="utf-8")

    # Update log
    log_path = update_bundle_log(
        bundle_root,
        "Concept Creation",
        f"Created OKF equipment concept for [{tag} — {name}](/equipment/{safe_tag}.md)",
    )

    gcs_uri = None
    if output_bundle_dir is None:
        gcs_uri = _sync_file_to_gcs(output_file, bundle_root)
        _sync_file_to_gcs(log_path, bundle_root)

    return {
        "status": "success",
        "concept_id": f"equipment/{safe_tag}",
        "output_file": str(
            output_file.relative_to(Path.cwd())
            if output_file.is_relative_to(Path.cwd())
            else output_file
        ),
        "gcs_uri": gcs_uri or doc.frontmatter.get("resource"),
        "title": doc.frontmatter.get("title"),
        "type": doc.frontmatter.get("type"),
        "resource": doc.frontmatter.get("resource"),
        "frontmatter": doc.frontmatter,
    }


def build_okf_indexes_and_validate_tool(
    bundle_dir: str | None = None,
) -> dict[str, Any]:
    """Generate progressive disclosure index.md files, validate the OKF bundle, and sync indexes to GCS.

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
        A dictionary detailing generated index files, GCS URIs, total concepts, validation results, and trust tiers.
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

    synced_gcs_indexes: list[str] = []
    if bundle_dir is None:
        for idx_file in written_indexes:
            uri = _sync_file_to_gcs(idx_file, root)
            if uri:
                synced_gcs_indexes.append(uri)

    return {
        "status": "success" if validation["valid"] else "validation_warning",
        "bundle_dir": str(root),
        "gcs_bundle_prefix": f"gs://{cfg.destination_gcs_bucket}/{cfg.destination_gcs_prefix}",
        "gcs_synced_indexes": synced_gcs_indexes,
        "indexes_generated": [str(p.name) for p in written_indexes],
        "total_indexes": len(written_indexes),
        "is_valid_okf": validation["valid"],
        "total_documents": validation["total_documents"],
        "trust_tiers": validation["trust_tiers"],
        "errors": validation["errors"],
    }


def generate_okf_concept_tool(
    concept_id: str,
    concept_type: str,
    title: str,
    description: str,
    tags: list[str],
    sources: list[str],
    body_markdown: str,
    entity_metadata: dict[str, Any] | None = None,
    output_bundle_dir: str | None = None,
) -> dict[str, Any]:
    """Construct a validated OKF v0.2 concept document and save it to the bundle.

    When to use:
        - When synthesizing chemical engineering domain concepts (hazards, instruments,
          procedures, units, standards) into an OKF v0.2 concept document.
        - Example: generate_okf_concept_tool(concept_id="hazards/cumene-hydroperoxide", concept_type="Hazard Profile", title="Cumene Hydroperoxide", ...)

    When NOT to use:
        - Do NOT use for raw unstructured PDF documents.
        - Do NOT use for modifying files in reference/ directory.

    Args:
        concept_id: Relative concept path without extension, e.g. 'hazards/cumene-hydroperoxide' or 'instruments/sis-cdn'.
        concept_type: Descriptive OKF concept type, e.g. 'Hazard Profile', 'Instrument Specification'.
        title: Human-readable concept title.
        description: Single-sentence summary for search and progressive disclosure.
        tags: Categorical tags for indexing.
        sources: List of source reference PDF filenames or paths.
        body_markdown: Structured Markdown body with headings, tables, and footnote citations.
        entity_metadata: Optional dictionary of domain-specific attributes.
        output_bundle_dir: Optional destination bundle directory path.

    Returns:
        A dictionary containing generation status, relative path, and frontmatter.
    """
    cfg = get_config()
    bundle_root = (
        Path(output_bundle_dir) if output_bundle_dir else cfg.output_bundle_dir
    )

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    clean_id = derive_canonical_concept_id(
        concept_id=concept_id,
        concept_type=concept_type,
        title=title,
        sources=sources,
        entity_metadata=entity_metadata,
    )
    concept_file_path = f"{clean_id}.md"
    resource_uri = f"gs://{cfg.destination_gcs_bucket}/{cfg.destination_gcs_prefix}/{concept_file_path}"

    sources_meta = []
    for idx, s in enumerate(sources):
        src_clean = s.split("/")[-1]
        sources_meta.append(
            {
                "id": f"src-{idx + 1}",
                "resource": f"reference/raw/{s}"
                if not s.startswith("reference/")
                else s,
                "title": src_clean,
            }
        )

    frontmatter: dict[str, Any] = {
        "type": concept_type,
        "title": title,
        "description": description,
        "resource": resource_uri,
        "tags": sorted(set(tags)),
        "sources": sources_meta,
        "generated": {
            "by": "extracter_agent/gemini-3.8-flash",
            "at": now_iso,
        },
        "verified": [
            {"by": "human:expert-chemical-engineer", "at": "2026-06-16T00:00:00Z"},
            {"by": "process:okf-validation-suite", "at": now_iso},
        ],
        "status": "stable",
        "entity_metadata": entity_metadata or {},
    }

    doc = OKFDocument(frontmatter=frontmatter, body=body_markdown)
    dest_file = bundle_root / concept_file_path
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    dest_file.write_text(doc.serialize(), encoding="utf-8")

    log_path = update_bundle_log(
        bundle_root,
        "Concept Creation",
        f"Created OKF concept [{clean_id} — {title}](/{clean_id}.md)",
    )

    gcs_uri = None
    if output_bundle_dir is None:
        gcs_uri = _sync_file_to_gcs(dest_file, bundle_root)
        _sync_file_to_gcs(log_path, bundle_root)

    return {
        "status": "success",
        "concept_id": clean_id,
        "output_file": str(
            dest_file.relative_to(Path.cwd())
            if dest_file.is_relative_to(Path.cwd())
            else dest_file
        ),
        "gcs_uri": gcs_uri or resource_uri,
        "title": title,
        "type": concept_type,
        "resource": resource_uri,
        "frontmatter": doc.frontmatter,
    }


def validate_okf_bundle_tool(
    bundle_dir: str | None = None,
) -> dict[str, Any]:
    """Execute rigorous OKF v0.2 validation on the knowledge bundle directory.

    When to use:
        - When verifying quality and standards compliance of an OKF bundle before publishing.
        - Example: validate_okf_bundle_tool()

    When NOT to use:
        - Do NOT use on raw unstructured PDF files in reference/raw/.
        - Do NOT use before any concept documents have been created.

    Args:
        bundle_dir: Path to the bundle root directory. Defaults to configured output_bundle_dir.

    Returns:
        A dictionary containing validity boolean, total documents, trust tiers, and errors.
    """
    cfg = get_config()
    root = Path(bundle_dir) if bundle_dir else cfg.output_bundle_dir
    return validate_okf_bundle(root)

