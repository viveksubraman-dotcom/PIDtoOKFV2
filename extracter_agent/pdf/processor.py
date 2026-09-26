"""PDF processing pipeline for chemical engineering documents.

Extracts text, metadata, and structural sections from raw engineering PDFs.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

import pypdf


class PDFProcessingError(Exception):
    """Raised when a PDF cannot be parsed or processed."""


def extract_pdf_pages(file_path: Path | str) -> list[dict[str, Any]]:
    """Extract text and metadata from each page of a PDF document.

    Args:
        file_path: Path to the PDF file.

    Returns:
        A list of dictionaries, each containing page_number (1-indexed), text,
        char_count, and word_count.
    """
    path = Path(file_path)
    if not path.exists():
        raise PDFProcessingError(f"PDF file does not exist: {path}")

    try:
        reader = pypdf.PdfReader(str(path))
    except Exception as e:
        raise PDFProcessingError(f"Failed to read PDF {path}: {e}") from e

    pages: list[dict[str, Any]] = []
    for idx, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception as e:
            text = f"[Extraction error on page {idx + 1}: {e}]"

        pages.append(
            {
                "page_number": idx + 1,
                "text": text,
                "char_count": len(text),
                "word_count": len(text.split()),
            }
        )

    return pages


def get_pdf_metadata(file_path: Path | str) -> dict[str, Any]:
    """Retrieve document-level metadata and summary metrics."""
    path = Path(file_path)
    if not path.exists():
        raise PDFProcessingError(f"PDF file does not exist: {path}")

    try:
        reader = pypdf.PdfReader(str(path))
        meta = reader.metadata or {}
        total_pages = len(reader.pages)
        return {
            "file_name": path.name,
            "file_size_bytes": path.stat().st_size,
            "page_count": total_pages,
            "title": getattr(meta, "title", None) or path.stem,
            "author": getattr(meta, "author", None),
            "creator": getattr(meta, "creator", None),
        }
    except Exception as e:
        raise PDFProcessingError(f"Error extracting metadata from {path}: {e}") from e


def chunk_document_text(
    pages: list[dict[str, Any]],
    max_chunk_size: int = 4000,
    overlap: int = 400,
) -> list[dict[str, Any]]:
    """Chunk page texts into bounded segments preserving page attribution.

    Args:
        pages: List of page dictionaries from extract_pdf_pages.
        max_chunk_size: Maximum characters per chunk.
        overlap: Character overlap between contiguous chunks.

    Returns:
        List of chunks with text, start_page, end_page, and chunk_index.
    """
    if not pages:
        return []

    chunks: list[dict[str, Any]] = []
    current_text: list[str] = []
    current_pages: list[int] = []
    current_len = 0

    for page in pages:
        page_num = page["page_number"]
        page_text = page["text"].strip()
        if not page_text:
            continue

        if current_len + len(page_text) > max_chunk_size and current_text:
            combined = "\n\n".join(current_text)
            chunks.append(
                {
                    "chunk_index": len(chunks) + 1,
                    "text": combined,
                    "start_page": current_pages[0],
                    "end_page": current_pages[-1],
                    "char_count": len(combined),
                }
            )
            # Apply overlap from tail of combined text
            overlap_text = combined[-overlap:] if overlap > 0 else ""
            current_text = [overlap_text, page_text] if overlap_text else [page_text]
            current_pages = [page_num]
            current_len = sum(len(t) for t in current_text)
        else:
            current_text.append(page_text)
            current_pages.append(page_num)
            current_len += len(page_text)

    if current_text:
        combined = "\n\n".join(current_text)
        chunks.append(
            {
                "chunk_index": len(chunks) + 1,
                "text": combined,
                "start_page": current_pages[0],
                "end_page": current_pages[-1],
                "char_count": len(combined),
            }
        )

    return chunks


def extract_equipment_tag_candidates(text: str) -> list[str]:
    """Extract likely equipment tag candidates matching standard plant tag patterns.

    Identifies alphanumeric plant equipment tags matching <PREFIX>-<NUMBER><SUFFIX>.
    Used as candidate hints for model reasoning; does NOT replace cognitive routing.
    """
    pattern = r"\b([A-Z]{1,3}-\d{4}[A-Z]{0,6})\b"
    matches = re.findall(pattern, text)
    # Preserve order, deduplicate
    seen: set[str] = set()
    unique: list[str] = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            unique.append(m)
    return unique


def is_vector_drawing(file_path: Path | str) -> bool:
    """Determine if a PDF is an AutoCAD or vector drawing lacking text streams."""
    path = Path(file_path)
    if not path.exists():
        return False
    try:
        reader = pypdf.PdfReader(str(path))
        if not reader.pages:
            return False
        total_text = "".join(p.extract_text() or "" for p in reader.pages[:3]).strip()
        return len(total_text) == 0
    except Exception:
        return False


def search_raw_documents(
    query: str,
    raw_dir: Path | str,
    subfolder: str | None = None,
) -> list[dict[str, Any]]:
    """Search reference/raw directory for PDF documents matching a query or entity tag."""
    base = Path(raw_dir)
    target = base / subfolder if subfolder else base
    if not target.exists():
        return []

    results: list[dict[str, Any]] = []
    tokens = [t.lower().strip() for t in re.split(r"[\s\-_]+", query) if t.strip()]

    for pdf in target.rglob("*.pdf"):
        name_lower = pdf.name.lower()
        if query.lower() in name_lower or any(tok in name_lower for tok in tokens):
            try:
                rel = pdf.relative_to(base)
            except ValueError:
                rel = pdf
            subf = pdf.parent.name if pdf.parent != base else "root"
            results.append(
                {
                    "file_name": pdf.name,
                    "subfolder": subf,
                    "relative_path": str(rel),
                    "size_bytes": pdf.stat().st_size,
                }
            )

    results.sort(key=lambda x: (x["subfolder"], x["file_name"]))
    return results


def extract_pdf_multimodal_part(file_path: Path | str) -> Any:
    """Create a google.genai types.Part representation for multimodal PDF processing."""
    path = Path(file_path)
    if not path.exists():
        raise PDFProcessingError(f"PDF file does not exist: {path}")

    from google.genai import types

    pdf_bytes = path.read_bytes()
    return types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")


def extract_pdf_multimodal_summary(
    file_path: Path | str,
    prompt_hint: str | None = None,
) -> str:
    """Extract chemical engineering technical content using Gemini multimodal vision.

    Invoked when a document is a vector drawing (P&ID, PFD) lacking font text streams,
    or contains scanned raster data tables. Includes a deterministic SHA-256 local and
    GCS cache so repeated tool calls on the same engineering PDF return in < 50ms.
    """
    path = Path(file_path)
    if not path.exists():
        raise PDFProcessingError(f"PDF file does not exist: {path}")

    import hashlib
    import tempfile
    import time

    from google import genai
    from google.genai import types

    from extracter_agent.config import get_config

    cfg = get_config()
    pdf_bytes = path.read_bytes()
    pdf_sha = hashlib.sha256(pdf_bytes).hexdigest()[:24]
    cache_dir = Path(tempfile.gettempdir()) / "extracter_multimodal_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{path.stem}_{pdf_sha}.md"

    if cache_file.exists() and cache_file.stat().st_size > 100:
        return cache_file.read_text(encoding="utf-8")

    if cfg.use_gcs_storage:
        try:
            from google.cloud import storage

            st_client = storage.Client(project=cfg.google_cloud_project)
            bucket = st_client.bucket(cfg.destination_gcs_bucket)
            cache_blob = bucket.blob(f"cache/multimodal/{path.stem}_{pdf_sha}.md")
            if cache_blob.exists():
                cached_text = cache_blob.download_as_text(encoding="utf-8")
                if len(cached_text) > 100:
                    cache_file.write_text(cached_text, encoding="utf-8")
                    return cached_text
        except Exception as exc:
            logging.getLogger(__name__).debug("Ignored non-fatal exception: %s", exc)

    http_opts = types.HttpOptions(
        retry_options=types.HttpRetryOptions(
            attempts=5,
            initial_delay=2.0,
            exp_base=2.0,
            http_status_codes=[429, 500, 502, 503, 504],
        )
    )
    client = genai.Client(http_options=http_opts)
    part = types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")

    base_prompt = (
        "Extract all chemical engineering technical specifications from this engineering document:\n"
        "- Equipment tag, equipment name/title, unit/section, and document number\n"
        "- Mechanical dimensions (diameter, tangent length, boot ID/length, elevation), supports (saddles/skirt), vessel internals (distributors, partitions, vortex breakers)\n"
        "- Design ratings (internal/external design pressure, design temperature, metallurgy, corrosion allowance)\n"
        "  * CRITICAL OCR DECIMAL CHECK: Carefully inspect decimal points on Design Pressure and Operating Pressure. Cross-check the P&ID equipment banner/title block against the Process Data Sheet AS-BUILT table.\n"
        "- Operating conditions (operating pressure, operating temperature, liquid levels NLL/LLL/VHL, specific gravity)\n"
        "- Nozzles schedule (exact nozzle marks, sizes, ratings, services), stream connections, line tags, origins and destinations\n"
        "- Complete instrumentation loops: NEVER collapse stacked or redundant P&ID instrument bubbles into a single tag; explicitly enumerate every sibling transmitter, controller, hand switch, and suffix\n"
        "- Safety Instrumented Systems (SIS/ESD valves, unit interlocks, trip actions, alarms, PSVs and setpoints)\n"
        "- Engineering notes, minimum static elevation head notes, standard references, and cross-document conflict notes."
    )
    if prompt_hint:
        base_prompt = f"{base_prompt}\nFocus especially on: {prompt_hint}"

    last_err: Exception | None = None
    for attempt in range(3):
        try:
            resp = client.models.generate_content(
                model=cfg.gemini_model,
                contents=[part, base_prompt],
            )
            text_out = resp.text or ""
            if len(text_out) > 100:
                try:
                    cache_file.write_text(text_out, encoding="utf-8")
                    if cfg.use_gcs_storage:
                        from google.cloud import storage

                        st_client = storage.Client(project=cfg.google_cloud_project)
                        bucket = st_client.bucket(cfg.destination_gcs_bucket)
                        bucket.blob(
                            f"cache/multimodal/{path.stem}_{pdf_sha}.md"
                        ).upload_from_string(text_out, content_type="text/markdown")
                except Exception as exc:
                    logging.getLogger(__name__).debug("Ignored non-fatal exception: %s", exc)
            return text_out
        except Exception as e:
            last_err = e
            if attempt < 2:
                time.sleep(2.0 * (2**attempt))
    return f"[Multimodal extraction error: {last_err}]"


