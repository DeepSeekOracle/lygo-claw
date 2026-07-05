"""Balanced loop: Desktop LYGO-Claw <-> USB BUILDR <-> lattice verify."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .godmode_brain import brain_dream, brain_init, resolve_vault_root, resolve_key_root
from .gateway import SovereignGateway
from .usb_supervisor import health as usb_health, submit_task, task_status

SIGNATURE = "D9Phi963-SOVEREIGN-LOOP-v1"


def _lattice_verify(stack: Path) -> dict[str, Any]:
    tool = stack / "tools" / "verify_lattice_alignment.py"
    if not tool.is_file():
        return {"ok": None, "skipped": "no verify script"}
    proc = subprocess.run(
        [sys.executable, str(tool)],
        cwd=str(stack),
        capture_output=True,
        text=True,
        timeout=180,
    )
    aligned = proc.returncode == 0 and "ALIGNED" in (proc.stdout or "")
    return {"ok": aligned, "exit_code": proc.returncode, "summary": "ALIGNED" if aligned else "NEEDS_FIX"}


def run_sovereign_loop(
    *,
    init_vault: bool = False,
    dream: bool = True,
    lattice: bool = True,
    usb_tasks: bool = True,
) -> dict[str, Any]:
    ts = datetime.now(timezone.utc).isoformat()
    stack = Path(os.environ.get("LYGO_STACK_ROOT", r"I:\E Drive\lygo-protocol-stack"))
    vault = resolve_vault_root()
    key = resolve_key_root(vault) or Path(os.environ.get("LYGO_BUILDER_KEY_ROOT", r"E:\LYGO_BUILDER_KEY"))

    steps: dict[str, Any] = {}

    if init_vault or not (vault / "memory.md").is_file():
        steps["brain_init"] = brain_init(vault)

    steps["usb_health"] = usb_health()
    if dream:
        steps["brain_dream"] = brain_dream(vault)

    if usb_tasks and steps["usb_health"].get("ok"):
        queued = submit_task("verify_standalone", {}, agent_id="sovereign-loop")
        steps["usb_task_verify"] = queued
        tid = queued.get("task_id")
        if tid:
            import time

            for _ in range(30):
                st = task_status(tid)
                if st.get("status") in ("done", "failed"):
                    steps["usb_task_result"] = st
                    break
                time.sleep(1)

    gw = SovereignGateway().ingest("Sovereign loop tick — lattice USB brain balance check.")
    steps["gateway"] = {"ok": gw.get("ok"), "verdict": gw.get("verdict")}

    if lattice:
        steps["lattice"] = _lattice_verify(stack)

    balanced = bool(
        steps.get("usb_health", {}).get("ok")
        and steps.get("gateway", {}).get("ok")
        and (steps.get("lattice", {}).get("ok") is not False)
    )
    report = {
        "signature": SIGNATURE,
        "ts": ts,
        "balanced": balanced,
        "vault": str(vault),
        "key_root": str(key) if key.exists() else None,
        "stack_root": str(stack),
        "steps": steps,
    }
    out = vault / "lygo" / "sovereign_loop_last_run.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report