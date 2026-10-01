"""Original phenol/cumene (UOP Unit 23) corpus profile - reproduces the pre-profile cockpit exactly."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from corpus_profiles import REPO_ROOT, Profile

_TOKENS = json.loads((Path(__file__).resolve().parent / "phenol_html_tokens.json").read_text(encoding="utf-8"))

UI = {
    "default_node_index": 4,
    "critical_dom_id": "node-d2304",
    "flow_pairs": [
        ["node-r2201", "node-v2301"], ["node-v2301", "node-v2302"], ["node-v2302", "node-d2301"],
        ["node-d2301", "node-d2304"], ["node-d2304", "node-e2307"], ["node-d2304", "node-p2302"],
        ["node-p2302", "node-d2308"], ["node-d2312", "node-d2304"], ["node-d2308", "node-v2401"],
        ["node-sis_cdn", "node-d2304"], ["node-hazop_cdn", "node-sis_cdn"],
    ],
    "persona_flagship_concepts": [
        "troubleshooting/cdn-poor-ams-yield", "troubleshooting/cdn-dehydrator-plugging",
        "procedures/startup-cdn", "equipment/D-2304",
    ],
    "default_concept": "equipment/D-2304",
    "default_graph_node": "troubleshooting/cdn-poor-ams-yield",
    "canvas_caption": "N\u25b2  PROCESS FLOW TOPOLOGY  |  SCALE: 25m ELEVATION",
    "raw_dir_label": "reference/raw/",
}


def build(ctx: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str], dict[str, Any]]:
    return {}, dict(_TOKENS), dict(UI)


_BUNDLE_DIR = REPO_ROOT / "build" / "okf_bundle"

PROFILE = Profile(
    name="phenol-plant",
    raw_dir=REPO_ROOT / "reference" / "raw",
    wiki_dir=_BUNDLE_DIR if _BUNDLE_DIR.exists() else (REPO_ROOT / "reference" / "wiki"),
    gcs_prefix="okf-bundles/phenol-plant",
    build=build,
    harness_required=["PROCESS MANUFACTURING", "BEYOND HAZOP"],
)
