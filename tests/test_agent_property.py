"""Property-Based Tests (PBT) for ADK agent guardrails using Hypothesis."""

from hypothesis import given
from hypothesis import strategies as st

from extracter_agent.agent.guardrails import check_prompt_security

prohibited_tokens = [
    "ignore previous instructions",
    "disregard all previous instructions",
    "system prompt override",
    "bypass security",
    "delete all files",
    "rm -rf /",
]

safe_chars = st.characters(whitelist_categories=("L", "N", "Z"))


@given(
    prefix=st.text(alphabet=safe_chars, max_size=50),
    bad_token=st.sampled_from(prohibited_tokens),
    suffix=st.text(alphabet=safe_chars, max_size=50),
)
def test_pbt_guardrail_injection_detection_invariant(prefix, bad_token, suffix):
    """Invariant: Any prompt containing a prohibited token is strictly intercepted."""
    prompt = f"{prefix} {bad_token} {suffix}"
    check = check_prompt_security(prompt)
    assert check["filterMatchState"] == "MATCH_FOUND"
    assert check["violation_type"] == "PROMPT_INJECTION"


@given(benign_prompt=st.text(alphabet=safe_chars, min_size=1, max_size=100))
def test_pbt_guardrail_benign_clean_invariant(benign_prompt):
    """Invariant: Clean alphanumeric prompts never trigger false-positive blocks."""
    # Only evaluate if none of the prohibited strings accidentally appear
    if not any(token in benign_prompt.lower() for token in prohibited_tokens):
        check = check_prompt_security(benign_prompt)
        assert check["filterMatchState"] == "NO_MATCH"
        assert check["violation_type"] is None
