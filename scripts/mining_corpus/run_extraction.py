"""Run the REAL extracter ADK agent file-by-file over the synthetic mining corpus (Mode B, read-merge-upsert).

Sequential on purpose: each PDF enriches concepts written by the previous ones (merge order matters).
Resumable: completed files are recorded in <bundle>/_run_log.jsonl and skipped on re-run.

Env (set by this script before importing the agent):
  REFERENCE_RAW_DIR=corpora/copper-concentrator/raw
  OUTPUT_BUNDLE_DIR=corpora/copper-concentrator/wiki
  USE_GCS_STORAGE=false
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "corpora/copper-concentrator/raw"
BUNDLE = ROOT / "corpora/copper-concentrator/wiki"
os.environ["REFERENCE_RAW_DIR"] = str(RAW)
os.environ["OUTPUT_BUNDLE_DIR"] = str(BUNDLE)
os.environ["DESTINATION_GCS_PREFIX"] = "okf-bundles/copper-concentrator"
os.environ["USE_GCS_STORAGE"] = "false"
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

import datetime as _dt
import subprocess as _sp

import google.auth
from google.auth import credentials as _gac


class _GcloudCreds(_gac.Credentials):
    """ADC stand-in for local runs when ADC needs an interactive password reauth."""

    def refresh(self, request):
        self.token = _sp.check_output(["gcloud", "auth", "print-access-token", GCLOUD_ACCOUNT], text=True, stdin=_sp.DEVNULL, timeout=60).strip()
        self.expiry = (
            _dt.datetime.now(tz=_dt.timezone.utc).replace(tzinfo=None)
            + _dt.timedelta(minutes=45)
        )


GCLOUD_ACCOUNT = os.getenv("EXTRACT_GCLOUD_ACCOUNT", "")
if GCLOUD_ACCOUNT:
    _proj = os.getenv("GOOGLE_CLOUD_PROJECT")
    google.auth.default = lambda *a, **k: (_GcloudCreds(), _proj)  # type: ignore[assignment]

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from extracter_agent.agent.orchestrator import create_extracter_agent

# Order: design basis first, then data sheets (authoritative design), then drawings, then manual/standards.
ORDER = ["pfd", "data_sheets", "pid", "operating_manuals", "standards"]


def ordered_pdfs() -> list[Path]:
    out = []
    for sub in ORDER:
        files = sorted((RAW / sub).glob("*.pdf"))
        out += files
    return out


async def run_one(pdf: Path, attempt_max: int = 3) -> dict:
    rel = pdf.relative_to(RAW)
    prompt = (f"Process raw engineering file {rel.parent.name}/{pdf.name} and incrementally extract and update all affected "
              "OKF v0.2 concepts (source summary, equipment, instruments, units, hazards, or procedures) in the bundle. "
              "Preserve facts from previously processed documents and flag any cross-document discrepancy as a CONFLICT.")
    last_err = None
    for attempt in range(attempt_max):
        svc = InMemorySessionService()
        sid = f"mining-{int(time.time()*1000)}-{attempt}"
        await svc.create_session(app_name="extracter_agent", user_id="corpus", session_id=sid)
        runner = Runner(agent=create_extracter_agent(), session_service=svc, app_name="extracter_agent")
        tools, final, t0 = [], "", time.time()
        try:
            async for ev in runner.run_async(user_id="corpus", session_id=sid,
                                             new_message=types.Content(role="user", parts=[types.Part.from_text(text=prompt)])):
                for c in ev.get_function_calls() or []:
                    tools.append(c.name)
                if ev.content and ev.content.parts:
                    for p in ev.content.parts:
                        if p.text:
                            final = p.text
            if any(t.startswith("generate_") for t in tools):
                return {"file": str(rel), "ok": True, "tools": tools, "sec": round(time.time() - t0, 1), "summary": final[:600]}
            last_err = f"no generate_* tool call (tools={tools})"
        except Exception as exc:  # transient 429/500 -> backoff
            last_err = f"{type(exc).__name__}: {exc}"[:400]
        await asyncio.sleep(6 * 2 ** attempt)
    return {"file": str(rel), "ok": False, "error": last_err}


async def main_async(limit: int | None) -> None:
    BUNDLE.mkdir(parents=True, exist_ok=True)
    log = BUNDLE / "_run_log.jsonl"
    done = set()
    if log.exists():
        for ln in log.read_text().splitlines():
            r = json.loads(ln)
            if r.get("ok"):
                done.add(r["file"])
    todo = [p for p in ordered_pdfs() if str(p.relative_to(RAW)) not in done]
    if limit:
        todo = todo[:limit]
    print(f"{len(done)} done, {len(todo)} to process", flush=True)
    for i, pdf in enumerate(todo, 1):
        r = await run_one(pdf)
        with log.open("a") as f:
            f.write(json.dumps(r) + "\n")
        print(f"[{i}/{len(todo)}] {'OK ' if r['ok'] else 'ERR'} {r['file']} {r.get('sec','')}s {r.get('tools', r.get('error'))}", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    asyncio.run(main_async(ap.parse_args().limit))
