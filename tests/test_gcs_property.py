"""Property-Based Tests (PBT) for GCS exporter using Hypothesis."""

from pathlib import Path

from hypothesis import given
from hypothesis import strategies as st

from extracter_agent.gcs.exporter import get_blob_name, infer_content_type

safe_path_chars = st.characters(whitelist_categories=("L", "N"))


@given(
    prefix=st.text(alphabet=safe_path_chars, min_size=1, max_size=20),
    part1=st.text(alphabet=safe_path_chars, min_size=1, max_size=20),
    part2=st.text(alphabet=safe_path_chars, min_size=1, max_size=20),
)
def test_pbt_get_blob_name_invariants(prefix, part1, part2):
    """Invariant: get_blob_name combines prefix and parts without double slashes."""
    rel_path = f"{part1}/{part2}.md"
    blob_name = get_blob_name(prefix, rel_path)

    assert "//" not in blob_name
    assert blob_name.startswith(prefix)
    assert blob_name.endswith(f"{part2}.md")


@given(
    ext=st.sampled_from([".md", ".yaml", ".yml", ".json", ".txt", ".bin", ""]),
    filename=st.text(alphabet=safe_path_chars, min_size=1, max_size=15),
)
def test_pbt_infer_content_type_invariants(ext, filename):
    """Invariant: infer_content_type returns a valid non-empty MIME string with a slash."""
    content_type = infer_content_type(Path(f"{filename}{ext}"))
    assert isinstance(content_type, str)
    assert "/" in content_type
    if ext == ".md":
        assert "text/markdown" in content_type
    elif ext in (".yaml", ".yml"):
        assert "text/yaml" in content_type
    elif ext == ".json":
        assert "application/json" in content_type
