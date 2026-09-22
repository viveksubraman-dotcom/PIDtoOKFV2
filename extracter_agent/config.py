"""Configuration loader supporting unified multi-environment parameters.

Adheres strictly to Rule 8 of Repository Guidelines.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load local .env if present
load_dotenv(override=False)


class AppConfig(BaseModel):
    """Application configuration parsed from environment variables."""

    service_name: str = Field(
        default_factory=lambda: os.getenv("SERVICE_NAME", "extracter-agent")
    )
    git_repo_url: str = Field(
        default_factory=lambda: os.getenv(
            "GIT_REPO_URL", "https://github.com/pantana-na/extracter-agent.git"
        )
    )
    google_cloud_project: str = Field(
        default_factory=lambda: os.getenv(
            "GOOGLE_CLOUD_PROJECT", "cs-poc-y03r7kmfyov4kilzg50fd7s"
        )
    )
    google_cloud_location: str = Field(
        default_factory=lambda: os.getenv("GOOGLE_CLOUD_LOCATION", "asia-southeast1")
    )
    gemini_model: str = Field(
        default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    )
    deployment_target: str = Field(
        default_factory=lambda: os.getenv("DEPLOYMENT_TARGET", "agent_runtime")
    )

    destination_gcs_bucket: str = Field(
        default_factory=lambda: os.getenv(
            "DESTINATION_GCS_BUCKET",
            "cs-poc-y03r7kmfyov4kilzg50fd7s-okf-knowledge",
        )
    )
    destination_gcs_prefix: str = Field(
        default_factory=lambda: os.getenv(
            "DESTINATION_GCS_PREFIX", "okf-bundles/phenol-plant"
        )
    )
    output_bundle_dir: Path = Field(
        default_factory=lambda: Path(os.getenv("OUTPUT_BUNDLE_DIR", "build/okf_bundle"))
    )

    reference_raw_dir: Path = Field(
        default_factory=lambda: Path(os.getenv("REFERENCE_RAW_DIR", "reference/raw"))
    )
    reference_wiki_dir: Path = Field(
        default_factory=lambda: Path(os.getenv("REFERENCE_WIKI_DIR", "reference/wiki"))
    )


_config: AppConfig | None = None


def get_config() -> AppConfig:
    """Retrieve the singleton AppConfig instance."""
    global _config
    if _config is None:
        _config = AppConfig()
    return _config
