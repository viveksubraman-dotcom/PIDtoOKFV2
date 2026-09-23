"""Google Cloud Storage (GCS) Knowledge Bundle Exporter.

Uploads and synchronizes OKF v0.2 bundles to enterprise GCS buckets.
"""

from __future__ import annotations

import logging
import mimetypes
from pathlib import Path
from typing import Any

from google.cloud import storage


def get_blob_name(prefix: str, relative_path: str) -> str:
    """Normalize target GCS blob name from prefix and relative path."""
    clean_prefix = prefix.strip("/")
    clean_rel = relative_path.lstrip("/")
    if clean_prefix:
        return f"{clean_prefix}/{clean_rel}"
    return clean_rel


def infer_content_type(file_path: Path | str) -> str:
    """Determine HTTP Content-Type for OKF files."""
    path = Path(file_path)
    if path.suffix == ".md":
        return "text/markdown; charset=utf-8"
    if path.suffix in (".yaml", ".yml"):
        return "text/yaml; charset=utf-8"
    if path.suffix == ".json":
        return "application/json; charset=utf-8"
    guessed, _ = mimetypes.guess_type(str(path))
    return guessed or "application/octet-stream"


class GCSExporter:
    """Manages the upload and synchronization of OKF bundles to Google Cloud Storage."""

    def __init__(self, bucket_name: str, client: storage.Client | None = None) -> None:
        self.bucket_name = bucket_name
        self._client = client

    @property
    def client(self) -> storage.Client:
        if self._client is None:
            self._client = storage.Client()
        return self._client

    def export_bundle(
        self,
        bundle_dir: Path | str,
        prefix: str = "okf-bundles/phenol-plant",
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Upload all bundle files from bundle_dir to gs://<bucket_name>/<prefix>/."""
        root = Path(bundle_dir)
        if not root.exists():
            raise FileNotFoundError(f"Bundle directory does not exist: {root}")

        files_to_upload: list[tuple[Path, str, str]] = []
        total_bytes = 0

        for file_path in root.rglob("*"):
            if file_path.is_file():
                rel_path = str(file_path.relative_to(root))
                blob_name = get_blob_name(prefix, rel_path)
                content_type = infer_content_type(file_path)
                file_size = file_path.stat().st_size
                total_bytes += file_size
                files_to_upload.append((file_path, blob_name, content_type))

        uploaded_uris: list[str] = []

        if not dry_run:
            from concurrent.futures import ThreadPoolExecutor

            bucket = self.client.bucket(self.bucket_name)
            existing_sizes: dict[str, int] = {}
            try:
                if hasattr(bucket, "list_blobs"):
                    for b in bucket.list_blobs(prefix=prefix.strip("/") + "/"):
                        if hasattr(b, "name") and hasattr(b, "size"):
                            existing_sizes[b.name] = b.size or 0
            except Exception as exc:
                logging.getLogger(__name__).debug("Ignored non-fatal exception: %s", exc)

            def _upload_one(item: tuple[Path, str, str]) -> str:
                local_path, blob_name, c_type = item
                uri = f"gs://{self.bucket_name}/{blob_name}"
                f_size = local_path.stat().st_size
                if existing_sizes.get(blob_name) == f_size and f_size > 0 and not blob_name.endswith(("index.md", "log.md")):
                    return uri
                blob = bucket.blob(blob_name)
                blob.upload_from_filename(str(local_path), content_type=c_type)
                return uri

            with ThreadPoolExecutor(max_workers=16) as pool:
                uploaded_uris = list(pool.map(_upload_one, files_to_upload))
        else:
            for _, blob_name, _ in files_to_upload:
                uploaded_uris.append(f"gs://{self.bucket_name}/{blob_name}")

        return {
            "bucket": self.bucket_name,
            "prefix": prefix,
            "dry_run": dry_run,
            "files_count": len(files_to_upload),
            "total_bytes": total_bytes,
            "destination_root_uri": f"gs://{self.bucket_name}/{prefix.strip('/')}",
            "uploaded_uris": uploaded_uris,
        }
