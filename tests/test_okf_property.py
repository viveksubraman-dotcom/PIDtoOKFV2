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
        alphabet=st.sampled_from(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-/_\\ ")),
        min_size=1,
        max_size=40,
    ).filter(lambda s: any(c.isalnum() for c in s))
)
def test_pbt_sanitize_tag_filename_never_contains_slashes(raw_tag):
    """Invariant: sanitize_tag_filename never produces path separators ('/' or '\\') or whitespace."""
    from extracter_agent.models.domain import sanitize_tag_filename

    safe = sanitize_tag_filename(raw_tag)
    assert "/" not in safe
    assert "\\" not in safe
    assert " " not in safe
    assert len(safe) > 0

