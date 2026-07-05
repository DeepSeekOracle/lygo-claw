"""Bridge to LYGO Champion USB supervisor (127.0.0.1:9630)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

DEFAULT_URL = os.environ.get("LYGO_USB_SUPERVISOR_URL", "http://127.0.0.1:9630")


def supervise(agent_id: str, tool_name: str, args_preview: str, *, base_url: str | None = None) -> dict[str, Any]:
    url = (base_url or DEFAULT_URL).rstrip("/") + "/Supervise"
    body = json.dumps(
        {"agent_id": agent_id, "tool_call": {"name": tool_name, "args": args_preview[:2048]}}
    ).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as exc:
        return {"approved": True, "skipped": "usb_supervisor_offline", "error": str(exc)}


def health(base_url: str | None = None) -> dict[str, Any]:
    url = (base_url or DEFAULT_URL).rstrip("/") + "/health"
    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as exc:
        return {"ok": False, "error": str(exc)}


def submit_task(
    task_type: str,
    payload: dict | None = None,
    *,
    agent_id: str = "lygo-claw",
    base_url: str | None = None,
) -> dict[str, Any]:
    url = (base_url or DEFAULT_URL).rstrip("/") + "/Task"
    body = json.dumps(
        {"agent_id": agent_id, "type": task_type, "payload": payload or {}}
    ).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as exc:
        return {"ok": False, "error": str(exc)}


def task_status(task_id: str, *, base_url: str | None = None) -> dict[str, Any]:
    url = (base_url or DEFAULT_URL).rstrip("/") + f"/Task?id={task_id}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as exc:
        return {"ok": False, "error": str(exc)}