"""Unit tests for GCS bundle exporter."""

from pathlib import Path
import tempfile
import pytest
from extracter_agent.gcs.exporter import GCSExporter, get_blob_name, infer_content_type


def test_get_blob_name():
  """Test blob name normalization."""
  assert get_blob_name("my-prefix", "equipment/V-2301.md") == "my-prefix/equipment/V-2301.md"
  assert get_blob_name("/my-prefix/", "/equipment/V-2301.md") == "my-prefix/equipment/V-2301.md"
  assert get_blob_name("", "index.md") == "index.md"


def test_infer_content_type():
  """Test MIME content type inference for OKF files."""
  assert infer_content_type(Path("index.md")) == "text/markdown; charset=utf-8"
  assert infer_content_type(Path("config.yaml")) == "text/yaml; charset=utf-8"
  assert infer_content_type(Path("data.json")) == "application/json; charset=utf-8"


def test_export_bundle_dry_run():
  """Test dry-run export calculation without calling live GCP APIs."""
  with tempfile.TemporaryDirectory() as tmpdir:
    root = Path(tmpdir)
    (root / "index.md").write_text("# Index", encoding="utf-8")
    (root / "equipment").mkdir()
    (root / "equipment" / "V-2301.md").write_text("---\ntype: Equipment\n---\n# V-2301", encoding="utf-8")

    exporter = GCSExporter(bucket_name="test-bucket")
    res = exporter.export_bundle(root, prefix="bundles/test", dry_run=True)

    assert res["bucket"] == "test-bucket"
    assert res["prefix"] == "bundles/test"
    assert res["dry_run"] is True
    assert res["files_count"] == 2
    assert res["total_bytes"] > 0
    assert "gs://test-bucket/bundles/test/index.md" in res["uploaded_uris"]
    assert "gs://test-bucket/bundles/test/equipment/V-2301.md" in res["uploaded_uris"]


def test_export_bundle_missing_dir_raises():
  """Test error on nonexistent directory."""
  exporter = GCSExporter(bucket_name="test-bucket")
  with pytest.raises(FileNotFoundError):
    exporter.export_bundle("nonexistent/dir/path")
