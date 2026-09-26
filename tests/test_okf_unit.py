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


def test_derive_canonical_concept_id_and_equipment_tag():
    """Verify autonomous derivation of canonical OKF concept paths from raw metadata."""
    from extracter_agent.models.domain import (
        derive_canonical_concept_id,
        derive_canonical_equipment_tag,
        sanitize_tag_filename,
    )

    assert sanitize_tag_filename("LT-2201 (Y02)") == "LT-2201"
    assert (
        derive_canonical_equipment_tag(
            "E-2307A/B", ["14780-8120-PS-E2307_E-2307 A_B PROCESS DATA SHEET_Z1.pdf"]
        )
        == "E-2307"
    )
    assert (
        derive_canonical_equipment_tag(
            "P-2302A/B", ["14780-8120-PS-P2302_P-2302 A_B PROCESS DATA SHEET_Z1.pdf"]
        )
        == "P-2302"
    )
    assert (
        derive_canonical_concept_id(
            "hazards/sulfuric-acid-hazard-profile",
            concept_type="Hazard Profile",
            title="Sulfuric Acid (98%) Hazard",
        )
        == "hazards/sulfuric-acid"
    )
    assert (
        derive_canonical_concept_id(
            "instruments/cdn-sis-architecture",
            concept_type="Instrument Specification",
            title="CDN Safety Instrumented System",
        )
        == "instruments/sis-cdn"
    )
    assert (
        derive_canonical_concept_id(
            "standards/hazop-methodology-sg-q-mp-014-r3",
            concept_type="Standard",
            title="HAZOP Methodology SG-Q-MP-014",
        )
        in ("hazop/methodology", "sources/SG-Q-MP-014")
    )


def test_zero_hardcoded_domain_maps_or_tags():
    """Verify that all agent, model, tool, and OKF modules contain zero hardcoded lookup maps, ISA prefix chains, or dataset-specific tags."""
    banned_tokens = [
        "instrument_map",
        "cdn-analyzer-register",
        "diisopropanolamine",
        "E-2307AB",
        "P-2302AB",
        "X-2309AB",
        "Unit 21 (ALKY",
        "LT-0602",
        "HXS-0106",
        '"value": "6600"',
        "UC-2301",
        "UC-2302",
        "p_code.startswith",
        "V-2301",
        "D-2304",
        "D-2204A/B/C",
        "Preflash Column",
        "cumene-hydroperoxide",
        "sis-cdn",
        "2026-06-16T00:00:00Z",
    ]
    target_files = [
        Path("extracter_agent/models/domain.py"),
        Path("extracter_agent/okf/indexer.py"),
        Path("extracter_agent/okf/synthesizer.py"),
        Path("extracter_agent/cli.py"),
        Path("extracter_agent/agent/orchestrator.py"),
        Path("extracter_agent/pdf/processor.py"),
        Path("extracter_agent/tools/okf_tools.py"),
        Path("extracter_agent/tools/pdf_tools.py"),
    ]
    for fpath in target_files:
        src = fpath.read_text(encoding="utf-8")
        for tok in banned_tokens:
            assert tok not in src, f"Hardcoded token '{tok}' found in {fpath}"


def test_bundle_100_percent_golden_parity_and_zero_broken_links():
    """Verify 130/130 Golden Dataset path parity and 0 broken internal Markdown links in build/okf_bundle."""
    import json
    import re

    bundle_dir = Path("build/okf_bundle")
    dataset_path = Path("evals/datasets/wiki_ground_truth_eval.jsonl")
    if not bundle_dir.exists() or not dataset_path.exists():
        return

    grounded = {
        json.loads(line)["relative_wiki_path"]
        for line in dataset_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    bundle_rels = {p.relative_to(bundle_dir).as_posix() for p in bundle_dir.rglob("*.md")}
    missing = grounded - bundle_rels
    assert len(missing) == 0, f"Missing Golden paths in bundle: {sorted(missing)}"

    broken = []
    for md in bundle_dir.rglob("*.md"):
        txt = md.read_text(encoding="utf-8")
        for m in re.finditer(r"\[[^\]]+\]\(([^)#\s]+)(?:#[^)]*)?\)", txt):
            lnk = m.group(1)
            if lnk.startswith(("http://", "https://", "gs://", "mailto:")):
                continue
            t1 = (md.parent / lnk).resolve()
            t2 = (bundle_dir / lnk.lstrip("/")).resolve()
            if not (
                t1.exists()
                or t1.with_suffix(".md").exists()
                or t2.exists()
                or t2.with_suffix(".md").exists()
            ):
                broken.append((md.relative_to(bundle_dir).as_posix(), lnk))

    assert len(broken) == 0, f"Broken internal Markdown links found: {broken[:10]}"


def test_in_place_md_update_invalidates_catalog_and_instrument_caches():
    """Verify in-place edits to child .md files immediately invalidate catalog and instrument caches even when parent dir mtime is unchanged."""
    import os

    from extracter_agent.models.domain import _iter_bundle_catalog
    from extracter_agent.okf.synthesizer import resolve_bundle_instrument_link

    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        inst_dir = root / "instruments"
        inst_dir.mkdir(parents=True)
        reg_a = inst_dir / "pressure-register.md"
        reg_b = inst_dir / "flow-register.md"
        reg_a.write_text(
            "---\ntype: Instrument Specification\ntitle: Pressure Register\n---\n# Pressure\nContains PT-1001.",
            encoding="utf-8",
        )
        reg_b.write_text(
            "---\ntype: Instrument Specification\ntitle: Flow Register\n---\n# Flow\nContains FT-1001.",
            encoding="utf-8",
        )

        # Warm both caches
        cat1 = _iter_bundle_catalog(root)
        assert any("ft-1001" in c["head_lower"] for c in cat1)
        assert not any("zx-9999" in c["head_lower"] for c in cat1)
        assert (
            resolve_bundle_instrument_link("FT-1001", bundle_root=root)
            == "/instruments/flow-register.md"
        )

        # Freeze parent dir mtime, modify reg_b in-place and advance only reg_b's mtime_ns
        dir_stat = inst_dir.stat()
        root_stat = root.stat()
        new_mtime_ns = reg_b.stat().st_mtime_ns + 5_000_000
        reg_b.write_text(
            "---\ntype: Instrument Specification\ntitle: Flow Register\n---\n# Flow\nContains FT-1001 and ZX-9999.",
            encoding="utf-8",
        )
        os.utime(reg_b, ns=(new_mtime_ns, new_mtime_ns))
        os.utime(inst_dir, ns=(dir_stat.st_atime_ns, dir_stat.st_mtime_ns))
        os.utime(root, ns=(root_stat.st_atime_ns, root_stat.st_mtime_ns))

        # Both caches must detect the child file mtime_ns change despite unchanged directory mtime_ns
        cat2 = _iter_bundle_catalog(root)
        assert any("zx-9999" in c["head_lower"] for c in cat2)
        assert (
            resolve_bundle_instrument_link("ZX-9999", bundle_root=root)
            == "/instruments/flow-register.md"
        )


def test_gcs_pdf_cache_redownloads_on_md5_or_size_change(monkeypatch):
    """Verify _download_pdf_from_gcs skips download on matching MD5+size and re-downloads when GCS MD5 changes in-place."""
    from unittest.mock import MagicMock

    from extracter_agent.tools import pdf_tools
    from extracter_agent.tools.pdf_tools import _compute_file_md5_b64

    with tempfile.TemporaryDirectory() as tmpdir:
        cache_dir = Path(tmpdir)
        monkeypatch.setattr(pdf_tools, "_GCS_RAW_CACHE_DIR", cache_dir)

        rel_path = "reference/raw/data_sheets/sample.pdf"
        cached_file = cache_dir / rel_path
        cached_file.parent.mkdir(parents=True, exist_ok=True)
        v1_bytes = b"%PDF-1.4 revision 1 (0.5 kg/cm2g)"
        v2_bytes = b"%PDF-1.4 revision 2 (3.9 kg/cm2g)"  # exact same byte length!
        assert len(v1_bytes) == len(v2_bytes)
        cached_file.write_bytes(v1_bytes)
        v1_md5 = _compute_file_md5_b64(cached_file)

        downloads: list[str] = []

        class DummyBlob:
            def download_to_filename(self, fname: str) -> None:
                downloads.append(fname)
                Path(fname).write_bytes(v2_bytes)

        mock_client = MagicMock()
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = DummyBlob()
        mock_client.bucket.return_value = mock_bucket
        monkeypatch.setattr(pdf_tools.storage, "Client", lambda **kwargs: mock_client)

        # Case 1: Matching size and MD5 -> zero downloads
        monkeypatch.setattr(
            pdf_tools,
            "_GCS_RAW_BLOBS_CACHE",
            [
                {
                    "file_name": "sample.pdf",
                    "subfolder": "data_sheets",
                    "relative_path": rel_path,
                    "blob_name": rel_path,
                    "gcs_uri": f"gs://test-bucket/{rel_path}",
                    "size_bytes": len(v1_bytes),
                    "md5_hash": v1_md5,
                }
            ],
        )
        p1, _ = pdf_tools._download_pdf_from_gcs("sample.pdf", "data_sheets")
        assert p1 == cached_file
        assert len(downloads) == 0

        # Case 2: Same size_bytes, updated md5_hash -> triggers re-download!
        import base64
        import hashlib

        v2_md5 = base64.b64encode(
            hashlib.md5(v2_bytes, usedforsecurity=False).digest()
        ).decode("ascii")
        monkeypatch.setattr(
            pdf_tools,
            "_GCS_RAW_BLOBS_CACHE",
            [
                {
                    "file_name": "sample.pdf",
                    "subfolder": "data_sheets",
                    "relative_path": rel_path,
                    "blob_name": rel_path,
                    "gcs_uri": f"gs://test-bucket/{rel_path}",
                    "size_bytes": len(v2_bytes),
                    "md5_hash": v2_md5,
                }
            ],
        )
        p2, _ = pdf_tools._download_pdf_from_gcs("sample.pdf", "data_sheets")
        assert p2 == cached_file
        assert len(downloads) == 1
        assert cached_file.read_bytes() == v2_bytes



