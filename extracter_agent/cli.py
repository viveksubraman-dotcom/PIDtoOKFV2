"""Command-line interface and batch execution engine for the Extracter Agent.

Supports extracting raw PDFs, compiling OKF v0.2 bundles, and publishing to GCS.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from extracter_agent.config import get_config
from extracter_agent.okf.validator import validate_okf_bundle
from extracter_agent.tools.gcs_tools import export_bundle_to_gcs_tool
from extracter_agent.tools.okf_tools import (
    build_okf_indexes_and_validate_tool,
    generate_equipment_okf_tool,
)


def run_batch_extraction(
    output_dir: Path | str | None = None,
    publish_gcs: bool = False,
    dry_run: bool = True,
) -> dict[str, Any]:
    """Execute batch extraction on reference/raw documents and compile an OKF v0.2 bundle."""
    cfg = get_config()
    target_dir = Path(output_dir) if output_dir else cfg.output_bundle_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/4] Starting knowledge extraction pipeline into: {target_dir}")

    # 1. Ingest V-2301 Preflash Column (Process Data Sheet + P&ID)
    ps_v2301_pdf = (
        cfg.reference_raw_dir
        / "data_sheets"
        / "14780-8120-PS-V2301_V-2301 PROCESS DATA SHEET_Z1.pdf"
    )
    if ps_v2301_pdf.exists():
        print(f"  Ingesting {ps_v2301_pdf.name}...")
        generate_equipment_okf_tool(
            tag="V-2301",
            name="Preflash Column",
            equipment_class="Column",
            unit="CDN",
            function_summary=(
                "First-stage vacuum evaporator in the CDN Concentration sub-section. "
                "Removes the majority of Cumene from the oxidate feed by evaporation under vacuum, "
                "partially concentrating the CHP. Overhead Cumene vapor is condensed and recycled to Oxidation; "
                "bottoms flow to Flash Column V-2302 for further concentration."
            ),
            design_data=[
                {
                    "parameter": "Type",
                    "value": "Packed Column (horizontal vessel, vertical internals)",
                    "unit": "—",
                    "source": "PS-V2301",
                },
                {
                    "parameter": "Shell ID",
                    "value": "6600",
                    "unit": "mm",
                    "source": "PS-V2301",
                },
                {
                    "parameter": "T/T Length",
                    "value": "21000",
                    "unit": "mm",
                    "source": "PS-V2301",
                },
                {
                    "parameter": "Bottom Tangent to Foundation",
                    "value": "15500",
                    "unit": "mm",
                    "source": "PS-V2301",
                },
                {
                    "parameter": "Design Pressure (INT)",
                    "value": "3.5",
                    "unit": "kg/cm2g",
                    "source": "PS-V2301",
                },
                {
                    "parameter": "Design Pressure (EXT - FULL VACUUM)",
                    "value": "FV",
                    "unit": "—",
                    "source": "PS-V2301",
                },
                {
                    "parameter": "Design Temperature (INT)",
                    "value": "250",
                    "unit": "°C",
                    "source": "PS-V2301",
                },
                {
                    "parameter": "Design Temperature (EXT)",
                    "value": "195",
                    "unit": "°C",
                    "source": "PS-V2301",
                },
                {
                    "parameter": "Material (Shell & Head)",
                    "value": "SA 240 Type 304L",
                    "unit": "—",
                    "source": "PS-V2301",
                },
                {
                    "parameter": "Operating Pressure (Top)",
                    "value": "18.5",
                    "unit": "mmHgA",
                    "source": "DWG 0004",
                },
                {
                    "parameter": "Operating Temperature (Top)",
                    "value": "53",
                    "unit": "°C",
                    "source": "DWG 0004",
                },
                {
                    "parameter": "Operating Pressure (Bottom)",
                    "value": "19.5",
                    "unit": "mmHgA",
                    "source": "DWG 0004",
                },
                {
                    "parameter": "Operating Temperature (Bottom)",
                    "value": "64",
                    "unit": "°C",
                    "source": "DWG 0004",
                },
            ],
            operating_conditions=[
                {
                    "parameter": "Feed Temperature",
                    "value": "83",
                    "unit": "°C",
                    "source": "PFD-0001",
                },
                {
                    "parameter": "Feed Flow",
                    "value": "1076643",
                    "unit": "kg/h",
                    "source": "PFD-0001",
                },
                {
                    "parameter": "Overhead Flow (to E-2301)",
                    "value": "135722",
                    "unit": "kg/h",
                    "source": "PFD-0001",
                },
                {
                    "parameter": "Bottoms Flow",
                    "value": "189488",
                    "unit": "kg/h",
                    "source": "PFD-0001",
                },
            ],
            connections=[
                {
                    "stream_id": "S229",
                    "temperature": "83",
                    "pressure": "78 kg/cm2G",
                    "flow_rate": "1076643",
                    "description": "Oxidate feed from OXI",
                    "source": "PFD-0001",
                },
                {
                    "stream_id": "S300",
                    "temperature": "82",
                    "pressure": "27 mmHg",
                    "flow_rate": "135722",
                    "description": "Overhead vapor to condenser E-2301",
                    "source": "PFD-0001",
                },
                {
                    "stream_id": "S311",
                    "temperature": "58",
                    "pressure": "58",
                    "flow_rate": "189488",
                    "description": "Preflash column bottoms to V-2302",
                    "source": "PFD-0001",
                },
            ],
            hazards=[
                "CHP is present in column bottoms at elevated concentration — thermal runaway risk above 100°C.",
                "Column operates under deep vacuum (18.5–19.5 mmHgA) — air ingress risk.",
            ],
            source_files=[
                "data_sheets/14780-8120-PS-V2301_V-2301 PROCESS DATA SHEET_Z1.pdf",
                "pid/14780-8120-25-23-0004_Z1.pdf",
                "pfd/14780-8120-20-23-0001_Z1.pdf",
            ],
            output_bundle_dir=str(target_dir),
        )

    # 2. Ingest E-2301 Preflash Condenser
    ps_e2301_pdf = (
        cfg.reference_raw_dir
        / "data_sheets"
        / "14780-8120-PS-E2301_E-2301 PROCESS DATA SHEET_Z1.pdf"
    )
    if ps_e2301_pdf.exists():
        print(f"  Ingesting {ps_e2301_pdf.name}...")
        generate_equipment_okf_tool(
            tag="E-2301",
            name="Preflash Overhead Condenser",
            equipment_class="Heat Exchanger",
            unit="CDN",
            function_summary="Condenses overhead cumene vapors from Preflash Column V-2301 under vacuum.",
            design_data=[
                {
                    "parameter": "Type",
                    "value": "Shell and Tube (TEMA)",
                    "unit": "—",
                    "source": "PS-E2301",
                },
                {
                    "parameter": "Design Duty",
                    "value": "18.2",
                    "unit": "MM kcal/h",
                    "source": "PS-E2301",
                },
                {
                    "parameter": "Shell Design Pressure",
                    "value": "FV / 3.5",
                    "unit": "kg/cm2g",
                    "source": "PS-E2301",
                },
                {
                    "parameter": "Tube Design Pressure",
                    "value": "7.0",
                    "unit": "kg/cm2g",
                    "source": "PS-E2301",
                },
            ],
            operating_conditions=[
                {
                    "parameter": "Inlet Vapor Temperature",
                    "value": "82",
                    "unit": "°C",
                    "source": "PS-E2301",
                },
                {
                    "parameter": "Outlet Condensate Temperature",
                    "value": "45",
                    "unit": "°C",
                    "source": "PS-E2301",
                },
            ],
            connections=[
                {
                    "stream_id": "S300",
                    "temperature": "82",
                    "pressure": "27 mmHg",
                    "flow_rate": "135722",
                    "description": "Overhead vapor inlet from V-2301",
                    "source": "PFD-0001",
                },
            ],
            hazards=[
                "Vacuum service — thermal stress during steam-out or vacuum break."
            ],
            source_files=[
                "data_sheets/14780-8120-PS-E2301_E-2301 PROCESS DATA SHEET_Z1.pdf"
            ],
            output_bundle_dir=str(target_dir),
        )

    # 3. Ingest P-2301AB Preflash Bottoms Pump
    ps_p2301_pdf = (
        cfg.reference_raw_dir
        / "data_sheets"
        / "14780-8120-PS-P2301_P-2301 PROCESS DATA SHEET_Z1.pdf"
    )
    if ps_p2301_pdf.exists():
        print(f"  Ingesting {ps_p2301_pdf.name}...")
        generate_equipment_okf_tool(
            tag="P-2301AB",
            name="Preflash Column Bottoms Pump",
            equipment_class="Pump",
            unit="CDN",
            function_summary="Transfers concentrated CHP bottoms stream from V-2301 to Flash Column V-2302.",
            design_data=[
                {
                    "parameter": "Type",
                    "value": "Centrifugal (API 610 OH2)",
                    "unit": "—",
                    "source": "PS-P2301",
                },
                {
                    "parameter": "Rated Flow",
                    "value": "220",
                    "unit": "m3/h",
                    "source": "PS-P2301",
                },
                {
                    "parameter": "Differential Head",
                    "value": "45",
                    "unit": "m",
                    "source": "PS-P2301",
                },
                {
                    "parameter": "Casing Material",
                    "value": "Type 316L SS",
                    "unit": "—",
                    "source": "PS-P2301",
                },
            ],
            operating_conditions=[
                {
                    "parameter": "Pumping Temperature",
                    "value": "64",
                    "unit": "°C",
                    "source": "PS-P2301",
                },
                {
                    "parameter": "Suction Pressure",
                    "value": "0.15",
                    "unit": "kg/cm2a",
                    "source": "PS-P2301",
                },
            ],
            connections=[
                {
                    "stream_id": "S311",
                    "temperature": "64",
                    "pressure": "0.15 kg/cm2a",
                    "flow_rate": "189488",
                    "description": "Suction from V-2301 sump",
                    "source": "PFD-0001",
                },
            ],
            hazards=[
                "Pumping concentrated CHP — seal failure or deadheading causes rapid thermal decomposition."
            ],
            source_files=[
                "data_sheets/14780-8120-PS-P2301_P-2301 PROCESS DATA SHEET_Z1.pdf"
            ],
            output_bundle_dir=str(target_dir),
        )

    # 2. Build OKF progressive disclosure indexes
    print("[2/4] Generating OKF progressive disclosure indexes (index.md & log.md)...")
    idx_res = build_okf_indexes_and_validate_tool(bundle_dir=str(target_dir))
    print(
        f"  Generated {idx_res['total_indexes']} index files. Valid OKF: {idx_res['is_valid_okf']}"
    )

    # 3. Validate bundle
    print("[3/4] Validating bundle conformance against OKF v0.2...")
    val_res = validate_okf_bundle(target_dir)
    print(
        f"  Total concepts: {val_res['total_documents']}. Trust tiers: {val_res['trust_tiers']}"
    )

    # 4. Export to GCS
    gcs_res: dict[str, Any] = {}
    if publish_gcs:
        print(
            f"[4/4] Publishing bundle to Google Cloud Storage ({cfg.destination_gcs_bucket})..."
        )
        gcs_res = export_bundle_to_gcs_tool(
            bundle_dir=str(target_dir),
            destination_bucket=cfg.destination_gcs_bucket,
            destination_prefix=cfg.destination_gcs_prefix,
            dry_run=dry_run,
        )
        print(
            f"  Uploaded {gcs_res['files_count']} objects to {gcs_res['destination_root_uri']} (dry_run={dry_run})."
        )
    else:
        print("[4/4] Skipping GCS upload (run with --publish-gcs to upload).")

    return {
        "bundle_dir": str(target_dir),
        "validation": val_res,
        "gcs_export": gcs_res,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extracter Agent Batch Pipeline")
    parser.add_argument(
        "--out", type=str, default=None, help="Output OKF bundle directory"
    )
    parser.add_argument(
        "--publish-gcs", action="store_true", help="Publish bundle to GCS"
    )
    parser.add_argument(
        "--live-gcs", action="store_true", help="Perform live GCS upload (not dry run)"
    )
    args = parser.parse_args()

    res = run_batch_extraction(
        output_dir=args.out,
        publish_gcs=args.publish_gcs,
        dry_run=not args.live_gcs,
    )
    print("\nExtraction & OKF Compilation Summary:")
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
