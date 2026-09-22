"""Security guardrails and ADK pre-flight callback hooks.

Implements Rule 11 & Section 1.3: Deterministic interception before agent execution.
"""

from __future__ import annotations

from typing import Any


class SecurityGuardrailError(PermissionError):
  """Raised when a prompt violates enterprise security policies or injection checks."""



def check_prompt_security(prompt: str) -> dict[str, Any]:
  """Evaluate prompt for adversarial jailbreaks, command injections, or policy violations.

  In production, this integrates with Google Cloud Model Armor.
  """
  lowered = prompt.lower()
  prohibited_patterns = [
      "ignore previous instructions",
      "disregard all previous instructions",
      "system prompt override",
      "bypass security",
      "delete all files",
      "rm -rf /",
  ]

  for p in prohibited_patterns:
    if p in lowered:
      return {
          "filterMatchState": "MATCH_FOUND",
          "violation_type": "PROMPT_INJECTION",
          "matched_pattern": p,
      }

  return {
      "filterMatchState": "NO_MATCH",
      "violation_type": None,
  }


def before_agent_callback(callback_context: Any) -> Any:
  """ADK Pre-flight security hook executed before model reasoning.

  Aborts immediately if adversarial prompt injection is detected.
  """
  prompt = ""
  if hasattr(callback_context, "prompt"):
    prompt = callback_context.prompt or ""
  elif isinstance(callback_context, str):
    prompt = callback_context
  elif isinstance(callback_context, dict):
    prompt = callback_context.get("prompt", "")

  check = check_prompt_security(prompt)
  if check["filterMatchState"] == "MATCH_FOUND":
    raise SecurityGuardrailError(
        f"Security violation detected: {check['violation_type']}. Operation aborted."
    )

  return callback_context
