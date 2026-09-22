"""OKF v0.2 Progressive Disclosure Indexer and Log Generator.

Implements Open Knowledge Format v0.2 §8 (Index files) and §9 (Log files).
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from extracter_agent.okf.document import OKFDocument

_INDEX_FILENAME = "index.md"
_LOG_FILENAME = "log.md"


def _build_index_body(entries: list[tuple[str, str, str, str]]) -> str:
  """Group concepts by type and format markdown listing."""
  # entries: (type, title, relative_link, description)
  grouped: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
  for typ, title, link, desc in entries:
    grouped[typ or "Other Concepts"].append((title, link, desc))

  sections: list[str] = []
  for typ in sorted(grouped):
    lines = [f"# {typ}", ""]
    for title, link, desc in sorted(grouped[typ], key=lambda e: e[0].lower()):
      suffix = f" - {desc}" if desc else ""
      lines.append(f"* [{title}]({link}){suffix}")
    sections.append("\n".join(lines))

  return "\n\n".join(sections) + "\n"


def generate_bundle_indexes(bundle_root: Path | str) -> list[Path]:
  """Generate index.md files for all directories within the bundle tree."""
  root = Path(bundle_root)
  if not root.exists():
    return []

  written_indexes: list[Path] = []

  # Find all directories that contain markdown documents
  directories: set[Path] = set()
  for md_file in root.rglob("*.md"):
    if md_file.name in (_INDEX_FILENAME, _LOG_FILENAME):
      continue
    cur = md_file.parent
    while cur != root.parent:
      directories.add(cur)
      if cur == root:
        break
      cur = cur.parent

  # Process bottom-up
  sorted_dirs = sorted(directories, key=lambda p: -len(p.parts))

  for directory in sorted_dirs:
    entries: list[tuple[str, str, str, str]] = []

    for child in sorted(directory.iterdir()):
      if child.name in (_INDEX_FILENAME, _LOG_FILENAME):
        continue

      if child.is_file() and child.suffix == ".md":
        try:
          doc = OKFDocument.parse(child.read_text(encoding="utf-8"))
          fm = doc.frontmatter
          title = str(fm.get("title") or child.stem)
          desc = str(fm.get("description") or "")
          typ = str(fm.get("type") or "Document")
          entries.append((typ, title, child.name, desc))
        except Exception:
          entries.append(("Document", child.stem, child.name, ""))
      elif child.is_dir():
        entries.append(("Subdirectories", child.name, f"{child.name}/{_INDEX_FILENAME}", f"Index of {child.name}"))

    if entries:
      index_file = directory / _INDEX_FILENAME
      index_content = _build_index_body(entries)
      index_file.write_text(index_content, encoding="utf-8")
      written_indexes.append(index_file)

  return written_indexes


def update_bundle_log(
    bundle_root: Path | str,
    action: str,
    details: str,
    date_str: str | None = None,
) -> Path:
  """Append a structured entry to the bundle root log.md."""
  root = Path(bundle_root)
  root.mkdir(parents=True, exist_ok=True)
  log_path = root / _LOG_FILENAME

  today = date_str or datetime.now(timezone.utc).strftime("%Y-%m-%d")

  existing_content = ""
  if log_path.exists():
    existing_content = log_path.read_text(encoding="utf-8")

  new_entry = f"* **{action}**: {details}\n"

  if not existing_content:
    content = f"# Directory Update Log\n\n## {today}\n{new_entry}"
  elif f"## {today}" in existing_content:
    # Insert under today's heading
    content = existing_content.replace(f"## {today}\n", f"## {today}\n{new_entry}")
  else:
    # Prepend new date section after the title
    title_marker = "# Directory Update Log\n\n"
    if existing_content.startswith(title_marker):
      content = title_marker + f"## {today}\n{new_entry}\n" + existing_content[len(title_marker):]
    else:
      content = f"# Directory Update Log\n\n## {today}\n{new_entry}\n\n" + existing_content

  log_path.write_text(content, encoding="utf-8")
  return log_path
