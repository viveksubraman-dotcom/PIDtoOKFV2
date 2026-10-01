"""Score the extracted OKF bundle against the seeded-conflict ground truth.

For every seeded conflict (``plant_model.SEEDED_CONFLICTS``) we look for a CONFLICT callout
in the compiled wiki that (a) is attributable to the tag - it mentions the tag or lives in the
tag's concept file - and (b) carries both the governing and the conflicting value.
Numbers are compared as floats (so ``4.0`` and ``40`` stay distinct); non-numeric conflicts
(chemical identity, missing safeguard) use evidence keywords declared below.

The revision decoy (PP-5101A Rev A -> Rev B) must NOT appear as a CONFLICT.
CONFLICT lines that match no seeded item are listed for manual review (they may be genuine
findings, e.g. derived consequences, or false positives) rather than auto-scored.

Usage:  python scripts/mining_corpus/eval_conflicts.py [--wiki DIR] [--json OUT]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plant_model import REVISION_DECOY, SEEDED_CONFLICTS

REPO = Path(__file__).resolve().parents[2]
DEFAULT_WIKI = REPO / "corpora" / "copper-concentrator" / "wiki"

# Non-numeric evidence: every group must match (any alternative within a group).
KEYWORD_EVIDENCE = {
    "C06": [r"MIBC|methyl isobutyl", r"DF-?250|polyglycol"],
    "C09": [r"AT-4501", r"missing|not shown|absent|omitted|not (?:present|depicted|included)|no .*detector"],
}

NUM_RE = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(?![\w])")


def _nums(text: str) -> set[float]:
    return {float(m.replace(",", "")) for m in NUM_RE.findall(text)}


def _first_num(value: str) -> float | None:
    m = NUM_RE.search(value)
    return float(m.group(1).replace(",", "")) if m else None


def _tag_base(tag: str) -> str:
    return re.sub(r"[A-Z]$", "", tag) if re.match(r"^[A-Z]{2}-\d{4}[A-Z]$", tag) else tag


def _conflict_blocks(wiki: Path) -> list[dict]:
    """Every CONFLICT line plus 2 lines of following context, with its file."""
    out = []
    for md in sorted(wiki.rglob("*.md")):
        rel = md.relative_to(wiki).as_posix()
        if rel in ("index.md", "log.md") or rel.endswith("/index.md"):
            continue
        lines = md.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            if "CONFLICT" in line.upper():
                ctx = " ".join(lines[i : i + 3])
                out.append({"file": rel, "line": i + 1, "text": line.strip(), "ctx": ctx})
    return out


def _attributable(block: dict, tag: str) -> bool:
    base = _tag_base(tag)
    return base in block["ctx"] or base.lower() in block["file"].lower()


def _matches(c: dict, block: dict) -> bool:
    if not _attributable(block, c["tag"]):
        return False
    if c["id"] in KEYWORD_EVIDENCE:
        return all(re.search(p, block["ctx"], re.IGNORECASE) for p in KEYWORD_EVIDENCE[c["id"]])
    a, b = _first_num(c["true"]), _first_num(c["conflict"])
    nums = _nums(block["ctx"])
    return a is not None and b is not None and a in nums and b in nums


def evaluate(wiki: Path) -> dict:
    blocks = _conflict_blocks(wiki)
    results, used = [], set()
    for c in SEEDED_CONFLICTS:
        hits = [b for b in blocks if _matches(c, b)]
        for h in hits:
            used.add((h["file"], h["line"]))
        results.append({
            "id": c["id"], "tag": c["tag"], "parameter": c["parameter"], "class": c["class"],
            "true": c["true"], "conflict": c["conflict"], "true_doc": c["true_doc"],
            "conflict_doc": c["conflict_doc"], "detected": bool(hits),
            "evidence": [{"file": h["file"], "line": h["line"], "text": h["text"][:300]} for h in hits[:3]],
        })

    d = REVISION_DECOY
    old_v, new_v = _first_num(d["old"][1]), _first_num(d["new"][1])
    decoy_hits = [
        b for b in blocks
        if _attributable(b, d["tag"])
        and {old_v, new_v} <= _nums(b["text"])
        and not re.search(r"supersedes\s+rev\s*a|increased\s+from\s+180", b["text"], re.IGNORECASE)
    ]
    unmatched = [b for b in blocks if (b["file"], b["line"]) not in used and b not in decoy_hits]

    detected = sum(r["detected"] for r in results)
    return {
        "wiki": str(wiki),
        "seeded_total": len(results),
        "seeded_detected": detected,
        "recall": round(detected / len(results), 3) if results else 0.0,
        "decoy_flagged_as_conflict": bool(decoy_hits),
        "decoy_evidence": [{"file": b["file"], "line": b["line"], "text": b["text"][:300]} for b in decoy_hits[:3]],
        "conflict_lines_total": len(blocks),
        "unmatched_conflict_lines": [{"file": b["file"], "line": b["line"], "text": b["text"][:300]} for b in unmatched],
        "results": results,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki", type=Path, default=DEFAULT_WIKI)
    ap.add_argument("--json", type=Path, default=None)
    args = ap.parse_args()
    rep = evaluate(args.wiki)
    for r in rep["results"]:
        mark = "HIT " if r["detected"] else "MISS"
        where = r["evidence"][0]["file"] if r["evidence"] else "-"
        print(f"{mark} {r['id']} {r['tag']:<9} {r['parameter']:<34} {where}")
    print(f"\nRecall {rep['seeded_detected']}/{rep['seeded_total']} = {rep['recall']:.0%}")
    print(f"Revision decoy flagged as conflict: {rep['decoy_flagged_as_conflict']}")
    print(f"CONFLICT lines total {rep['conflict_lines_total']}, unmatched {len(rep['unmatched_conflict_lines'])}")
    if args.json:
        args.json.write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {args.json}")


if __name__ == "__main__":
    main()
