"""ADK Root Orchestrator and App definition.

Complies strictly with Google ADK & Agent Runtime Standards (Rule 11).
Deployed to Gemini Enterprise Agent Platform (agent_runtime).
"""

from __future__ import annotations

from google.adk.agents import Agent
from google.adk.apps import App

from extracter_agent.agent.guardrails import before_agent_callback
from extracter_agent.config import get_config
from extracter_agent.tools.gcs_tools import export_bundle_to_gcs_tool
from extracter_agent.tools.okf_tools import (
  build_okf_indexes_and_validate_tool,
  generate_equipment_okf_tool,
)
from extracter_agent.tools.pdf_tools import process_raw_pdf_tool

ORCHESTRATOR_INSTRUCTIONS = """You are the autonomous OKF Extracter Agent running on the Gemini Enterprise Agent Platform.

Your primary mission:
1. Ingest and extract complex chemical engineering technical documents (process data sheets, P&IDs, PFDs, operating manuals, standards) located in `reference/raw/`.
2. Model-driven extraction: Extract equipment design parameters, materials of construction, dimensions, design pressures/temperatures, operating conditions, nozzle schedules, and process safety hazard limits.
3. Structure extracted knowledge strictly according to the Open Knowledge Format (OKF v0.2) specification, with YAML frontmatter and Markdown bodies with footnote citations.
4. Generate progressive disclosure directory indexes (index.md) and update logs (log.md).
5. Publish completed, validated OKF knowledge bundles to Google Cloud Storage (GCS).

Operational Rules:
- Under NO circumstances may you modify, delete, or write into the `reference/` directory. It is strictly read-only.
- All extracted knowledge must be compiled into the destination bundle directory.
- Verify OKF compliance before publishing to GCS.
- Ground all facts in the source engineering documentation.
"""


def create_extracter_agent() -> Agent:
  """Factory to construct the ADK Root Extracter Agent."""
  cfg = get_config()
  return Agent(
      name="extracter_orchestrator",
      description="Autonomous chemical engineering knowledge extraction and OKF bundle publishing agent.",
      model=cfg.gemini_model,
      instruction=ORCHESTRATOR_INSTRUCTIONS,
      tools=[
          process_raw_pdf_tool,
          generate_equipment_okf_tool,
          build_okf_indexes_and_validate_tool,
          export_bundle_to_gcs_tool,
      ],
      before_agent_callback=before_agent_callback,
  )


# Module-level instances for ADK runner and deployment
extracter_agent = create_extracter_agent()
app = App(
    name="extracter-agent",
    root_agent=extracter_agent,
)
