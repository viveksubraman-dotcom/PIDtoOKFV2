"""Property-Based Tests (PBT) for OKF documents and bundle operations using Hypothesis."""

import tempfile
from pathlib import Path

from hypothesis import given
from hypothesis import strategies as st

from extracter_agent.okf.document import OKFDocument
from extracter_agent.okf.indexer import generate_bundle_indexes

printable_chars = st.characters(blacklist_categories=("Cc", "Cs", "Zl", "Zp"))


@given(
    doc_type=st.text(alphabet=printable_chars, min_size=1, max_size=50).filter(
        lambda s: bool(s.strip()) and ":" not in s
    ),
    title=st.text(alphabet=printable_chars, min_size=1, max_size=100).filter(
        lambda s: bool(s.strip()) and ":" not in s
    ),
    desc=st.text(alphabet=printable_chars, min_size=1, max_size=200).filter(
        lambda s: bool(s.strip()) and ":" not in s
    ),
    body_text=st.text(alphabet=printable_chars, min_size=1, max_size=1000),
)

def test_pbt_okf_document_roundtrip_invariant(doc_type, title, desc, body_text):
    """Invariant: parse(serialize(doc)) preserves frontmatter type, title, and body."""
    fm = {
        "type": doc_type,
        "title": title,
        "description": desc,
    }
    doc = OKFDocument(frontmatter=fm, body=body_text)
    serialized = doc.serialize()
    reconstructed = OKFDocument.parse(serialized)

    assert reconstructed.frontmatter["type"] == doc_type
    assert reconstructed.frontmatter["title"] == title
    assert reconstructed.frontmatter["description"] == desc
    assert reconstructed.body.strip() == body_text.strip()


@given(
    names=st.lists(
        st.from_regex(r"[a-z0-9_-]{2,20}", fullmatch=True),
        min_size=1,
        max_size=6,
        unique=True,
    )
)
def test_pbt_bundle_index_link_invariants(names):
    """Invariant: Every item listed in generated index.md resolves to an existing file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        sub = root / "items"
        sub.mkdir()

        for name in names:
            doc = OKFDocument(
                frontmatter={
                    "type": "Test Item",
                    "title": name,
                    "description": f"Desc of {name}",
                },
                body=f"# {name}\n\nBody content.",
            )
            (sub / f"{name}.md").write_text(doc.serialize(), encoding="utf-8")

        generate_bundle_indexes(root)

        sub_index = sub / "index.md"
        assert sub_index.exists()
        content = sub_index.read_text(encoding="utf-8")

        # Invariant: Every name generated must be in the index
        for name in names:
            assert f"[{name}]({name}.md)" in content
            # Verify target file actually exists
            target_file = sub / f"{name}.md"
            assert target_file.exists()


@given(
    tags=st.lists(
        st.from_regex(r"[A-Z]{2,4}-[0-9]{3,4}[A-Z]?", fullmatch=True),
        min_size=1,
        max_size=5,
        unique=True,
    ),
    services=st.lists(
        st.text(alphabet=printable_chars, min_size=2, max_size=30).filter(
            lambda s: bool(s.strip()) and "|" not in s and "\n" not in s
        ),
        min_size=5,
        max_size=5,
    ),
)
def test_pbt_instrument_loop_link_invariants(tags, services):
    """Invariant: Synthesized instrument loops produce valid bundle-relative links and round-trip in frontmatter."""
    from extracter_agent.models.domain import EquipmentEntity, InstrumentLoop
    from extracter_agent.okf.synthesizer import synthesize_equipment_concept

    instruments = [
        InstrumentLoop(
            tag=tag,
            service=services[i],
            instrument_type="Transmitter",
            source="P&ID DWG 001",
        )
        for i, tag in enumerate(tags)
    ]

    entity = EquipmentEntity(
        tag="E-101",
        name="Test Exchanger",
        equipment_class="Heat Exchanger",
        unit="TEST",
        function_summary="Test unit",
        instruments=instruments,
    )

    doc = synthesize_equipment_concept(entity)

    # Invariant 1: Every instrument tag has a valid Markdown link in the body
    for inst in instruments:
        expected_link = f"[{inst.tag}](/instruments/{inst.tag}.md)"
        assert expected_link in doc.body

    # Invariant 2: Round-trip via serialization preserves instrument frontmatter metadata
    serialized = doc.serialize()
    reconstructed = OKFDocument.parse(serialized)
    reconstructed_instruments = reconstructed.frontmatter.get(
        "entity_metadata", {}
    ).get("instruments", [])
    assert len(reconstructed_instruments) == len(instruments)
    for original, parsed in zip(instruments, reconstructed_instruments):
        assert parsed["tag"] == original.tag
        assert parsed["service"] == original.service
        assert parsed["source"] == original.source


@given(
    raw_tag=st.text(
        alphabet=st.sampled_from(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-/_\\ ()")),
        min_size=1,
        max_size=40,
    ).filter(lambda s: any(c.isalnum() for c in s))
)
def test_pbt_sanitize_tag_filename_never_contains_slashes(raw_tag):
    """Invariant: sanitize_tag_filename never produces path separators ('/' or '\\'), parentheses, or whitespace."""
    from extracter_agent.models.domain import sanitize_tag_filename

    safe = sanitize_tag_filename(raw_tag)
    assert "/" not in safe
    assert "\\" not in safe
    assert " " not in safe
    assert "(" not in safe
    assert ")" not in safe
    assert len(safe) > 0


@given(
    slug=st.text(
        alphabet=st.sampled_from(list("abcdefghijklmnopqrstuvwxyz0123456789-/")),
        min_size=3,
        max_size=35,
    ).filter(lambda s: s[0].isalnum() and s[-1].isalnum() and "//" not in s)
)
def test_pbt_derive_canonical_concept_id_idempotent(slug):
    """Invariant: derive_canonical_concept_id is idempotent (f(f(x)) == f(x)) and never contains whitespace."""
    from extracter_agent.models.domain import derive_canonical_concept_id

    once = derive_canonical_concept_id(slug)
    twice = derive_canonical_concept_id(once)
    assert once == twice
    assert " " not in once
    assert not once.endswith(".md")


@given(
    prefix=st.sampled_from(["LT", "FT", "TT", "PT", "PSV", "FV", "AT", "HXS", "SC", "XC"]),
    loop_num=st.integers(min_value=100, max_value=9999),
)
def test_pbt_dynamic_instrument_link_never_broken(prefix, loop_num):
    """Invariant: When bundle_root contains instrument register files, resolve_bundle_instrument_link always points to an existing file."""
    from extracter_agent.okf.synthesizer import resolve_bundle_instrument_link

    bundle_dir = Path("build/okf_bundle")
    if not (bundle_dir / "instruments").exists():
        return

    tag = f"{prefix}-{loop_num}"
    resolved = resolve_bundle_instrument_link(tag, "Process Instrument", "Service", bundle_root=bundle_dir)
    assert resolved is not None
    target_file = bundle_dir / resolved.lstrip("/")
    assert target_file.exists(), f"Resolved link {resolved} does not exist in {bundle_dir}"


@given(
    p1_names=st.lists(
        st.from_regex(r"[A-Za-z0-9 ]{3,15}", fullmatch=True).map(str.strip).filter(bool),
        min_size=1,
        max_size=4,
        unique_by=str.lower,
    ),
    p2_names=st.lists(
        st.from_regex(r"[A-Za-z0-9 ]{3,15}", fullmatch=True).map(str.strip).filter(bool),
        min_size=1,
        max_size=4,
        unique_by=str.lower,
    ),
    val1=st.from_regex(r"[0-9]{1,4}", fullmatch=True),
    val2=st.from_regex(r"[0-9]{1,4}", fullmatch=True),
)
def test_pbt_incremental_merge_monotonic_and_idempotent(p1_names, p2_names, val1, val2):
    """Invariant: Incremental Read-Merge-Upsert is monotonically non-decreasing in sources and parameters, and re-applying the same update is idempotent."""
    from extracter_agent.models.domain import EngineeringParameter, EquipmentEntity
    from extracter_agent.okf.synthesizer import (
        merge_equipment_entity_with_existing,
        synthesize_equipment_concept,
    )

    e1 = EquipmentEntity(
        tag="E-900",
        name="Test Cooler",
        equipment_class="Heat Exchanger",
        unit="U90",
        function_summary="Initial function summary.",
        design_data=[
            EngineeringParameter(parameter=p, value=val1, unit="mm", source="DOC-1")
            for p in p1_names
        ],
        hazards=["Initial hazard 1"],
        sources=["data_sheets/DOC_1.pdf"],
    )
    doc1 = OKFDocument.parse(synthesize_equipment_concept(e1).serialize())

    e2 = EquipmentEntity(
        tag="E-900",
        name="Test Cooler",
        equipment_class="Heat Exchanger",
        unit="U90",
        function_summary="Enriched function summary from second PDF.",
        design_data=[
            EngineeringParameter(parameter=p, value=val2, unit="mm", source="DOC-2")
            for p in p2_names
        ],
        hazards=["Secondary hazard 2"],
        sources=["pid/DOC_2.pdf"],
    )

    merged_once = merge_equipment_entity_with_existing(e2, doc1)
    expected_unique_params = len({p.lower() for p in (p1_names + p2_names)})
    assert len(merged_once.design_data) == expected_unique_params
    assert len(merged_once.sources) == 2

    # Re-synthesizing and merging e2 a second time must be idempotent
    doc2 = OKFDocument.parse(synthesize_equipment_concept(merged_once).serialize())
    merged_twice = merge_equipment_entity_with_existing(e2, doc2)
    assert len(merged_twice.design_data) == len(merged_once.design_data)
    assert len(merged_twice.sources) == len(merged_once.sources)
    assert len(merged_twice.hazards) == len(merged_once.hazards)


@given(
    doc_num=st.integers(min_value=1000, max_value=9999),
    rev_old=st.sampled_from(["Rev 0", "Rev A", "Rev Z0", "_Z0", "-R1"]),
    rev_new=st.sampled_from(["Rev 1", "Rev B", "Rev Z1", "_Z1", "-R2"]),
    val_old=st.integers(min_value=1, max_value=50).map(str),
    val_new=st.integers(min_value=51, max_value=100).map(str),
)
def test_pbt_same_document_revision_supersedes_without_conflict(
    doc_num, rev_old, rev_new, val_old, val_new
):
    """Invariant: A newer revision of the same base document updates parameter values in-place without generating a false conflict."""
    from extracter_agent.models.domain import EngineeringParameter, EquipmentEntity
    from extracter_agent.okf.synthesizer import (
        merge_equipment_entity_with_existing,
        synthesize_equipment_concept,
    )

    src_old = f"PS-V{doc_num} {rev_old}" if not rev_old.startswith(("_", "-")) else f"PS-V{doc_num}{rev_old}"
    src_new = f"PS-V{doc_num} {rev_new}" if not rev_new.startswith(("_", "-")) else f"PS-V{doc_num}{rev_new}"

    e_old = EquipmentEntity(
        tag=f"V-{doc_num}",
        name="Test Vessel",
        equipment_class="Vessel",
        unit="U10",
        function_summary="Test vessel function.",
        design_data=[
            EngineeringParameter(
                parameter="Design Pressure",
                value=val_old,
                unit="kg/cm2g",
                source=src_old,
            )
        ],
        sources=[f"data_sheets/{src_old.replace(' ', '_')}.pdf"],
    )
    doc_old = OKFDocument.parse(synthesize_equipment_concept(e_old).serialize())

    e_new = EquipmentEntity(
        tag=f"V-{doc_num}",
        name="Test Vessel",
        equipment_class="Vessel",
        unit="U10",
        function_summary="Test vessel function.",
        design_data=[
            EngineeringParameter(
                parameter="Design Pressure",
                value=val_new,
                unit="kg/cm2g",
                source=src_new,
            )
        ],
        sources=[f"data_sheets/{src_new.replace(' ', '_')}.pdf"],
    )

    merged = merge_equipment_entity_with_existing(e_new, doc_old)
    assert len(merged.design_data) == 1
    assert merged.design_data[0].value == val_new
    assert merged.design_data[0].source == src_new
    assert not any("CONFLICT" in h for h in merged.hazards)
    assert len(merged.sources) == 1


@given(
    tags_doc1=st.lists(
        st.from_regex(r"[A-Z]{2}-[0-9]{4}", fullmatch=True),
        min_size=1,
        max_size=4,
        unique=True,
    ),
    tags_doc2=st.lists(
        st.from_regex(r"[A-Z]{2}-[0-9]{4}", fullmatch=True),
        min_size=1,
        max_size=4,
        unique=True,
    ),
)
def test_pbt_merge_markdown_bodies_preserves_rows_and_idempotent(tags_doc1, tags_doc2):
    """Invariant: merge_markdown_bodies preserves the union of all unique table row keys across documents and is idempotent."""
    from extracter_agent.okf.synthesizer import merge_markdown_bodies

    rows1 = "\n".join(f"| {t} | 0-10 bar | Service A | DWG-001 |" for t in tags_doc1)
    rows2 = "\n".join(f"| {t} | 0-16 bar | Service B | DWG-002 |" for t in tags_doc2)

    md1 = (
        "# Shared Register\n\n"
        "## Instrument Table\n\n"
        "| Tag | Range | Service | Source |\n"
        "| --- | --- | --- | --- |\n"
        f"{rows1}\n\n"
        "## Notes Doc 1\n\n"
        "- Grounded in DWG-001.\n"
    )
    md2 = (
        "# Shared Register\n\n"
        "## Instrument Table\n\n"
        "| Tag | Range | Service | Source |\n"
        "| --- | --- | --- | --- |\n"
        f"{rows2}\n\n"
        "## Notes Doc 2\n\n"
        "- Grounded in DWG-002.\n"
    )

    merged_once = merge_markdown_bodies(md1, md2)
    for t in set(tags_doc1) | set(tags_doc2):
        assert f"| {t} |" in merged_once
    assert "## Notes Doc 1" in merged_once
    assert "## Notes Doc 2" in merged_once

    # Idempotence: merging md2 a second time produces identical output
    merged_twice = merge_markdown_bodies(merged_once, md2)
    assert merged_twice == merged_once




