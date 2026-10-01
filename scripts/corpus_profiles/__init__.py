"""Corpus profiles for the 4-screen demo cockpit.

A profile decides which engineering corpus the cockpit is built around:

* ``raw_dir`` / ``wiki_dir`` - the raw PDFs and the compiled OKF bundle that feed ``data.js``.
* ``build(ctx)``           - returns ``(static_overrides, html_tokens, ui)``:
    - ``static_overrides``: keys that replace the defaults in ``build_static_data()``;
    - ``html_tokens``: values for every ``{{TOKEN}}`` in ``static/index.template.html``;
    - ``ui``: small runtime hints consumed by ``app.js`` (default node, flow pairs, ...).
* ``harness_required`` / ``harness_forbidden`` - phrases the build harness must / must not find.

Select with ``DEMO_CORPUS`` (default ``copper-concentrator``).
"""

from __future__ import annotations

import importlib
import os
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CORPUS = "copper-concentrator"


@dataclass
class Profile:
    name: str
    raw_dir: Path
    wiki_dir: Path
    gcs_prefix: str
    build: Callable[[dict[str, Any]], tuple[dict[str, Any], dict[str, str], dict[str, Any]]]
    harness_required: list[str] = field(default_factory=list)
    harness_forbidden: list[str] = field(default_factory=list)


_REGISTRY = {
    "phenol-plant": "corpus_profiles.phenol",
    "copper-concentrator": "corpus_profiles.copper_concentrator",
}


def available() -> list[str]:
    return sorted(_REGISTRY)


def load(name: str | None = None) -> Profile:
    name = name or os.getenv("DEMO_CORPUS", DEFAULT_CORPUS)
    if name not in _REGISTRY:
        raise SystemExit(f"Unknown DEMO_CORPUS '{name}'. Available: {', '.join(available())}")
    return importlib.import_module(_REGISTRY[name]).PROFILE
