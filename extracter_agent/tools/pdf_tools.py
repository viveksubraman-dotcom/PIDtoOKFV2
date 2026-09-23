"""ADK FunctionTools for PDF document processing.

Strictly complies with Rule 11 (FunctionTool docstring contracts, type safety).
"""

from __future__ import annotations

import logging
import re
import tempfile
from pathlib import Path
from typing import Any

from google.cloud import storage

from extracter_agent.config import get_config
from extracter_agent.pdf.processor import (
    extract_equipment_tag_candidates,
    extract_pdf_multimodal_summary,
    extract_pdf_pages,
    get_pdf_metadata,
    is_vector_drawing,
    search_raw_documents,
)

_GCS_RAW_BLOBS_CACHE: list[dict[str, Any]] | None = None
_GCS_RAW_CACHE_DIR = Path(tempfile.gettempdir()) / "extracter_gcs_raw_cache"


def _list_gcs_raw_blobs() -> list[dict[str, Any]]:
    """List and cache raw PDF object metadata from Google Cloud Storage."""
    global _GCS_RAW_BLOBS_CACHE
    if _GCS_RAW_BLOBS_CACHE is not None:
        return _GCS_RAW_BLOBS_CACHE

    cfg = get_config()
    client = storage.Client(project=cfg.google_cloud_project)
    bucket = client.bucket(cfg.destination_gcs_bucket)
    prefix = cfg.source_gcs_raw_prefix.strip("/") + "/"
    items: list[dict[str, Any]] = []
    for blob in bucket.list_blobs(prefix=prefix):
        if blob.name.lower().endswith(".pdf"):
            rel_under_raw = blob.name[len(prefix) :]
            parts = rel_under_raw.split("/")
            sub = parts[0] if len(parts) > 1 else ""
            fname = parts[-1]
            items.append(
                {
                    "file_name": fname,
                    "subfolder": sub,
                    "relative_path": f"reference/raw/{rel_under_raw}",
                    "blob_name": blob.name,
                    "gcs_uri": f"gs://{cfg.destination_gcs_bucket}/{blob.name}",
                    "size_bytes": blob.size or 0,
                }
            )
    if items:
        _GCS_RAW_BLOBS_CACHE = items
    return items


def _download_pdf_from_gcs(pdf_filename: str, subfolder: str) -> tuple[Path | None, str | None]:
    """Download a raw PDF from GCS into the local temporary cache directory."""
    cfg = get_config()
    blobs = _list_gcs_raw_blobs()
    clean_name = Path(pdf_filename).name
    norm_target = re.sub(r"[^a-z0-9]", "", clean_name.lower())

    matched_blob: dict[str, Any] | None = None
    for b in blobs:
        if b["file_name"] == clean_name and (not subfolder or b["subfolder"] == subfolder):
            matched_blob = b
            break
    if not matched_blob:
        for b in blobs:
            if b["file_name"] == clean_name or clean_name.lower() in b["file_name"].lower():
                matched_blob = b
                break
    if not matched_blob:
        for b in blobs:
            if norm_target in re.sub(r"[^a-z0-9]", "", b["file_name"].lower()):
                matched_blob = b
                break

    if not matched_blob:
        return None, None

    dest_path = _GCS_RAW_CACHE_DIR / matched_blob["relative_path"]
    if not dest_path.exists() or dest_path.stat().st_size == 0:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        client = storage.Client(project=cfg.google_cloud_project)
        bucket = client.bucket(cfg.destination_gcs_bucket)
        bucket.blob(matched_blob["blob_name"]).download_to_filename(str(dest_path))

    return dest_path, matched_blob["gcs_uri"]


def find_raw_documents_tool(
    query: str,
    subfolder: str | None = None,
) -> dict[str, Any]:
    """Search and discover raw engineering technical documents in Google Cloud Storage (reference/raw/).

    When to use:
        - When discovering raw PDF files for an equipment tag (e.g. V-2301), drawing number,
          or document category (e.g. data_sheets, pid, pfd) before starting extraction.
        - Example: find_raw_documents_tool(query="V-2301")

    When NOT to use:
        - Do NOT use for already processed Markdown files in reference/wiki/.
        - Do NOT use for general chat inquiries.
        - Do NOT attempt to modify or delete reference files.

    Args:
        query: Equipment tag, document code, or keyword to search (e.g. "V-2301", "Preflash", "0004").
        subfolder: Optional subdirectory to scope search (data_sheets, pid, pfd, operating_manuals, standards).

    Returns:
        A dictionary containing matched files, counts, GCS URIs, and relative paths.
    """
    cfg = get_config()
    if cfg.use_gcs_storage:
        try:
            blobs = _list_gcs_raw_blobs()
            if blobs:
                tokens = [
                    re.sub(r"[^a-z0-9]", "", t.lower())
                    for t in query.split()
                    if len(re.sub(r"[^a-z0-9]", "", t.lower())) >= 2
                ]
                gcs_matches = []
                for b in blobs:
                    if subfolder and b["subfolder"] != subfolder:
                        continue
                    haystack = re.sub(
                        r"[^a-z0-9]", "", f"{b['subfolder']} {b['file_name']}".lower()
                    )
                    if not tokens or any(tok in haystack for tok in tokens):
                        gcs_matches.append(b)
                return {
                    "status": "success",
                    "source_storage": "gcs",
                    "gcs_bucket": f"gs://{cfg.destination_gcs_bucket}/{cfg.source_gcs_raw_prefix}",
                    "query": query,
                    "subfolder": subfolder or "all",
                    "match_count": len(gcs_matches),
                    "matches": gcs_matches,
                }
        except Exception as exc:
            logging.getLogger(__name__).debug("Ignored non-fatal exception: %s", exc)

    raw_dir = cfg.reference_raw_dir
    results = search_raw_documents(query=query, raw_dir=raw_dir, subfolder=subfolder)
    return {
        "status": "success",
        "source_storage": "local",
        "query": query,
        "subfolder": subfolder or "all",
        "match_count": len(results),
        "matches": results,
    }


def process_raw_pdf_tool(
    pdf_filename: str,
    subfolder: str = "data_sheets",
    max_pages: int = 10,
    enable_multimodal: bool = True,
) -> dict[str, Any]:
    """Extract text, tables, and document metadata from a raw engineering PDF in GCS (reference/raw/).

    When to use:
        - When ingesting process data sheets, P&IDs, PFDs, or operating manuals
          from the reference/raw directory in GCS to extract chemical engineering knowledge.
        - Example: process_raw_pdf_tool("14780-8120-PS-V2301_V-2301 PROCESS DATA SHEET_Z1.pdf", "data_sheets")

    When NOT to use:
        - Do NOT use for already processed Markdown files in reference/wiki/.
        - Do NOT use for general conversational queries unrelated to document ingestion.
        - Do NOT attempt to modify or delete the source PDF file.

    Args:
        pdf_filename: The filename or relative path of the PDF.
        subfolder: The subdirectory under reference/raw (e.g. data_sheets, pid, pfd).
        max_pages: Maximum pages to process from the start of the document.
        enable_multimodal: Whether to run Gemini multimodal vision for vector drawings or scanned tables (default: True).

    Returns:
        A dictionary containing metadata, source GCS URI, extracted pages, vector drawing status, and identified equipment tag candidates.
    """
    cfg = get_config()
    raw_dir = cfg.reference_raw_dir
    target_path: Path | None = None
    source_gcs_uri: str | None = None

    if cfg.use_gcs_storage:
        try:
            target_path, source_gcs_uri = _download_pdf_from_gcs(pdf_filename, subfolder)
        except Exception:
            target_path = None

    if target_path is None:
        if (raw_dir / subfolder / pdf_filename).exists():
            target_path = raw_dir / subfolder / pdf_filename
        elif (raw_dir / pdf_filename).exists():
            target_path = raw_dir / pdf_filename
        elif Path(pdf_filename).exists():
            target_path = Path(pdf_filename)
        else:
            matches = list(raw_dir.rglob(f"*{pdf_filename}*"))
            if matches:
                target_path = matches[0]
            else:
                return {
                    "status": "error",
                    "error": f"PDF file not found in GCS or {raw_dir}: {pdf_filename}",
                    "pages": [],
                }

    try:
        meta = get_pdf_metadata(target_path)
        pages = extract_pdf_pages(target_path)
        limited_pages = pages[:max_pages]

        full_text = " ".join(p["text"] for p in limited_pages)
        has_native_text = len(full_text.strip()) > 0
        # Check if drawing is an AutoCAD vector graphic with empty text stream
        is_vector = is_vector_drawing(target_path)

        # Multimodal visual analysis trigger:
        # 1. Vector drawings (P&IDs, PFDs) with no font text stream
        # 2. Or data sheets / drawings where text is completely empty (<100 chars)
        # 3. Or multi-page data sheets where a key specification page has 0 text
        multimodal_text = None
        if enable_multimodal and (is_vector or len(full_text.strip()) < 100):
            multimodal_text = extract_pdf_multimodal_summary(
                target_path,
                prompt_hint=f"Extract complete engineering data for drawing {target_path.stem}",
            )
            limited_pages.append(
                {
                    "page_number": len(limited_pages) + 1,
                    "text": f"[Multimodal Visual Interpretation of {target_path.name}]:\n{multimodal_text}",
                    "char_count": len(multimodal_text),
                    "word_count": len(multimodal_text.split()),
                }
            )
            full_text = f"{full_text}\n{multimodal_text}"
        elif enable_multimodal and any(len(p["text"].strip()) < 50 for p in limited_pages) and subfolder == "data_sheets":
            multimodal_text = extract_pdf_multimodal_summary(
                target_path,
                prompt_hint=f"Focus on mechanical equipment data sheet tables and schedules in {target_path.stem}",
            )
            injected_once = False
            for p in limited_pages:
                if len(p["text"].strip()) < 50:
                    if not injected_once:
                        p["text"] = f"[Multimodal Visual Extraction of {target_path.name} Tables]:\n{multimodal_text}"
                        injected_once = True
                    else:
                        p["text"] = f"[Page {p['page_number']}: Raster table included in Multimodal Visual Extraction above]"
                    p["char_count"] = len(p["text"])
                    p["word_count"] = len(p["text"].split())
            full_text = f"{full_text}\n{multimodal_text}"

        # Extract tag candidates from both text and filename
        combined_text = f"{target_path.stem} {full_text}"
        tag_candidates = extract_equipment_tag_candidates(combined_text)

        rel_path = (
            str(target_path.resolve().relative_to(Path.cwd().resolve()))
            if target_path.resolve().is_relative_to(Path.cwd().resolve())
            else f"{cfg.source_gcs_raw_prefix}/{target_path.parent.name}/{target_path.name}"
        )

        return {
            "status": "success",
            "source_storage": "gcs" if source_gcs_uri else "local",
            "source_gcs_uri": source_gcs_uri
            or f"gs://{cfg.destination_gcs_bucket}/{rel_path}",
            "file_name": target_path.name,
            "subfolder": target_path.parent.name,
            "relative_path": rel_path,
            "metadata": meta,
            "is_vector_drawing": is_vector,
            "has_text_stream": has_native_text,
            "multimodal_ready": True,
            "multimodal_analysis": multimodal_text,
            "pages_processed": len(limited_pages),
            "total_pages": meta["page_count"],
            "tag_candidates": tag_candidates,
            "pages": limited_pages,
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to process PDF {target_path}: {e}",
            "pages": [],
        }

