#!/usr/bin/env python3
"""lygo-claw CLI — sovereign agent gateway."""

from __future__ import annotations

import argparse
import json
import sys

from .framework import LYGOOpenClaw
from .gateway import SovereignGateway
from .gatekeeper import P0Gatekeeper
from .usb_supervisor import health


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="lygo-claw")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_gw = sub.add_parser("gateway", help="Ingest message through P0 + Hermes + USB")
    p_gw.add_argument("text")

    p_run = sub.add_parser("run", help="Run gated limb command")
    p_run.add_argument("command")
    p_run.add_argument("args", nargs="*", default=[])

    sub.add_parser("usb-health", help="Check Champion USB supervisor")

    p_val = sub.add_parser("validate", help="P0 validate text")
    p_val.add_argument("text")

    p_audit = sub.add_parser("audit", help="Hermes chain status")
    p_audit.add_argument("action", choices=["verify"])

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
    if args.cmd == "validate":
        print(json.dumps(P0Gatekeeper().validate(args.text), indent=2))
        return 0
    if args.cmd == "audit":
        from .hermes_audit import validate_audit_chain

        print(json.dumps(validate_audit_chain(), indent=2))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())