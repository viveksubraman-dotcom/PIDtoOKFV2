"""ADK FunctionTools for PDF document processing.

Strictly complies with Rule 11 (FunctionTool docstring contracts, type safety).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from extracter_agent.config import get_config
from extracter_agent.pdf.processor import (
  extract_equipment_tag_candidates,
  extract_pdf_pages,
  get_pdf_metadata,
)


def process_raw_pdf_tool(
    pdf_filename: str,
    subfolder: str = "data_sheets",
    max_pages: int = 10,
) -> dict[str, Any]:
  """Extract text, tables, and document metadata from a raw engineering PDF.

  When to use:
      - When ingesting process data sheets, P&IDs, PFDs, or operating manuals
        from the reference/raw directory to extract chemical engineering knowledge.
      - Example: process_raw_pdf_tool("14780-8120-PS-V2301_V-2301 PROCESS DATA SHEET_Z1.pdf", "data_sheets")

  When NOT to use:
      - Do NOT use for already processed Markdown files in reference/wiki/.
      - Do NOT use for general conversational queries unrelated to document ingestion.
      - Do NOT attempt to modify or delete the source PDF file.

  Args:
      pdf_filename: The filename or relative path of the PDF.
      subfolder: The subdirectory under reference/raw (e.g. data_sheets, pid, pfd).
      max_pages: Maximum pages to process from the start of the document.

  Returns:
      A dictionary containing metadata, extracted pages, and identified equipment tag candidates.
  """
  cfg = get_config()
  raw_dir = cfg.reference_raw_dir

  if (raw_dir / subfolder / pdf_filename).exists():
    target_path = raw_dir / subfolder / pdf_filename
  elif (raw_dir / pdf_filename).exists():
    target_path = raw_dir / pdf_filename
  elif Path(pdf_filename).exists():
    target_path = Path(pdf_filename)
  else:
    # Try searching by name in raw_dir
    matches = list(raw_dir.rglob(f"*{pdf_filename}*"))
    if matches:
      target_path = matches[0]
    else:
      return {
          "status": "error",
          "error": f"PDF file not found: {pdf_filename} in {raw_dir}",
          "pages": [],
      }

  try:
    meta = get_pdf_metadata(target_path)
    pages = extract_pdf_pages(target_path)
    limited_pages = pages[:max_pages]

    full_text = " ".join(p["text"] for p in limited_pages)
    tag_candidates = extract_equipment_tag_candidates(full_text)

    return {
        "status": "success",
        "file_name": target_path.name,
        "relative_path": str(target_path.resolve().relative_to(Path.cwd().resolve())),
        "metadata": meta,
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
