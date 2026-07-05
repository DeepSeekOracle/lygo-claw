#!/usr/bin/env python3
"""lygo-claw CLI — sovereign agent gateway."""

from __future__ import annotations

import argparse
import json
import sys

from .framework import LYGOOpenClaw
from .gateway import SovereignGateway
from .gatekeeper import P0Gatekeeper
from .godmode_brain import brain_brief, brain_dream, brain_init, brain_query
from .sovereign_loop import run_sovereign_loop
from .usb_supervisor import health, submit_task, task_status


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="lygo-claw")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_gw = sub.add_parser("gateway", help="Ingest message through P0 + Hermes + USB")
    p_gw.add_argument("text")

    p_run = sub.add_parser("run", help="Run gated limb command")
    p_run.add_argument("command")
    p_run.add_argument("args", nargs="*", default=[])

    sub.add_parser("usb-health", help="Check Champion USB supervisor")

    p_bt = sub.add_parser("buildr-task", help="Queue a BUILDR USB daemon task (daemon must be running)")
    p_bt.add_argument(
        "type",
        choices=["verify_standalone", "verify_bootstrap", "chat_once", "anchor_audit", "second_brain_loop"],
    )
    p_bt.add_argument("--prompt", default="", help="For chat_once")
    p_bt.add_argument("--wait", action="store_true", help="Poll until done")

    p_val = sub.add_parser("validate", help="P0 validate text")
    p_val.add_argument("text")

    p_audit = sub.add_parser("audit", help="Hermes chain status")
    p_audit.add_argument("action", choices=["verify"])

    sub.add_parser("brain-init", help="Initialize God-Mode vault on USB mycelium")
    sub.add_parser("brain-dream", help="Run dream cycle (gap filler on USB when present)")
    sub.add_parser("brain-brief", help="Print morning brief.md")
    p_bq = sub.add_parser("brain-query", help="Grounded vault search")
    p_bq.add_argument("question")
    p_sl = sub.add_parser("sovereign-loop", help="Desktop + USB + lattice balanced loop")
    p_sl.add_argument("--no-lattice", action="store_true")
    p_sl.add_argument("--no-dream", action="store_true")

    args = ap.parse_args(argv)

    if args.cmd == "gateway":
        print(json.dumps(SovereignGateway().ingest(args.text), indent=2))
        return 0
    if args.cmd == "run":
        out = LYGOOpenClaw().run(args.command, list(args.args))
        print(json.dumps(out, indent=2))
        return 0 if out.get("ok") else 2
    if args.cmd == "usb-health":
        print(json.dumps(health(), indent=2))
        return 0
    if args.cmd == "buildr-task":
        payload: dict = {}
        if args.type == "chat_once":
            payload["prompt"] = args.prompt or "Say OK in one word."
        if args.type == "verify_bootstrap":
            payload = {"edition": "GROK_BUILDR", "phase2": True}
        queued = submit_task(args.type, payload)
        print(json.dumps(queued, indent=2))
        if not args.wait or not queued.get("task_id"):
            return 0 if queued.get("task_id") else 2
        import time

        tid = queued["task_id"]
        for _ in range(90):
            time.sleep(2)
            st = task_status(tid)
            print(json.dumps(st, indent=2))
            if st.get("status") in ("done", "failed"):
                return 0 if st.get("status") == "done" and (st.get("result") or {}).get("ok") else 2
        return 2
    if args.cmd == "validate":
        print(json.dumps(P0Gatekeeper().validate(args.text), indent=2))
        return 0
    if args.cmd == "audit":
        from .hermes_audit import validate_audit_chain

        print(json.dumps(validate_audit_chain(), indent=2))
        return 0
    if args.cmd == "brain-init":
        print(json.dumps(brain_init(), indent=2))
        return 0
    if args.cmd == "brain-dream":
        print(json.dumps(brain_dream(), indent=2))
        return 0
    if args.cmd == "brain-brief":
        print(json.dumps(brain_brief(), indent=2))
        return 0
    if args.cmd == "brain-query":
        print(json.dumps(brain_query(args.question), indent=2))
        return 0
    if args.cmd == "sovereign-loop":
        rep = run_sovereign_loop(dream=not args.no_dream, lattice=not args.no_lattice)
        print(json.dumps(rep, indent=2))
        return 0 if rep.get("balanced") else 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())