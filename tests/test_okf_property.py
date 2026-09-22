"""Property-Based Tests (PBT) for OKF documents and bundle operations using Hypothesis."""

import tempfile
from pathlib import Path
from hypothesis import given, strategies as st
from extracter_agent.okf.document import OKFDocument
from extracter_agent.okf.indexer import generate_bundle_indexes


printable_chars = st.characters(blacklist_categories=("Cc", "Cs", "Zl", "Zp"))

@given(
    doc_type=st.text(alphabet=printable_chars, min_size=1, max_size=50).filter(lambda s: bool(s.strip()) and ":" not in s),
    title=st.text(alphabet=printable_chars, min_size=1, max_size=100),
    desc=st.text(alphabet=printable_chars, min_size=1, max_size=200),
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
          frontmatter={"type": "Test Item", "title": name, "description": f"Desc of {name}"},
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
