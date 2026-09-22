"""PDF processing pipeline for chemical engineering documents.

Extracts text, metadata, and structural sections from raw engineering PDFs.
"""

from __future__ import annotations

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

    pages.append({
        "page_number": idx + 1,
        "text": text,
        "char_count": len(text),
        "word_count": len(text.split()),
    })

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
      chunks.append({
          "chunk_index": len(chunks) + 1,
          "text": combined,
          "start_page": current_pages[0],
          "end_page": current_pages[-1],
          "char_count": len(combined),
      })
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
    chunks.append({
        "chunk_index": len(chunks) + 1,
        "text": combined,
        "start_page": current_pages[0],
        "end_page": current_pages[-1],
        "char_count": len(combined),
    })

  return chunks


def extract_equipment_tag_candidates(text: str) -> list[str]:
  """Extract likely equipment tag candidates matching standard plant tag patterns.

  Identifies patterns like V-2301, D-2304, E-2301, P-2301AB, OX-2201, X-2301.
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
