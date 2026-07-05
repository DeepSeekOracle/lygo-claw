"""LYGO-hardened message gateway (localhost-only sovereign defaults)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .gatekeeper import P0Gatekeeper
from .hermes_audit import log_event, post_tool_call, pre_tool_call, set_log_path
from .usb_supervisor import supervise


class SovereignGateway:
    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or self._default_config()
        self.gatekeeper = P0Gatekeeper()
        audit = Path(self.config.get("hermes_log", "data/hermes_audit/audit_trail.log"))
        audit.parent.mkdir(parents=True, exist_ok=True)
        set_log_path(audit)

    @staticmethod
    def _default_config() -> dict[str, Any]:
        cfg_path = Path(__file__).resolve().parents[2] / "config" / "sovereign_defaults.json"
        if cfg_path.is_file():
            return json.loads(cfg_path.read_text(encoding="utf-8"))
        return {
            "bind_host": "127.0.0.1",
            "p0_enforced": True,
            "usb_supervisor": True,
            "hermes_log": "data/hermes_audit/audit_trail.log",
        }

    def ingest(self, text: str, *, agent_id: str = "lygo-claw", tool_name: str = "message") -> dict[str, Any]:
        pre_tool_call(tool_name, {"agent_id": agent_id, "preview": text[:512]})
        v = self.gatekeeper.validate(text)
        if self.config.get("p0_enforced") and v.get("verdict") == "QUARANTINE":
            post_tool_call(tool_name, False, {"p0": v})
            log_event("gateway_quarantine", detail=v)
            return {"ok": False, "verdict": "QUARANTINE", "p0": v}

        usb = {"approved": True, "skipped": True}
        if self.config.get("usb_supervisor"):
            usb = supervise(agent_id, tool_name, text)

        approved = usb.get("approved", True) and v.get("verdict") != "QUARANTINE"
        post_tool_call(tool_name, approved, {"p0": v, "usb": usb})
        return {
            "ok": approved,
            "verdict": v.get("verdict"),
            "p0": v,
            "usb_supervisor": usb,
            "persona_hint": self.config.get("default_champion", "Lightfather"),
        }