"""P0 gatekeeper for agent commands (standalone lygo-claw package)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_VENDOR_P0 = Path(__file__).resolve().parents[2] / "vendor" / "p0"
if str(_VENDOR_P0) not in sys.path:
    sys.path.insert(0, str(_VENDOR_P0))

try:
    from byte_entropy_filter import validate_bytes as _validate_bytes  # type: ignore

    P0_AVAILABLE = True
except ImportError:
    P0_AVAILABLE = False
    _validate_bytes = None  # type: ignore


class P0Gatekeeper:
    def __init__(self, max_bytes: int = 32768):
        self.max_bytes = max_bytes

    def validate(self, command: str) -> dict[str, Any]:
        data = command.encode("utf-8")
        if len(data) > self.max_bytes:
            return {
                "verdict": "QUARANTINE",
                "reason": "size_exceeded",
                "reasoning": f"Command {len(data)} > {self.max_bytes}",
            }
        if P0_AVAILABLE and _validate_bytes:
            out = _validate_bytes(data)
            return {
                "verdict": out.get("verdict", out.get("decision", "SOFTEN")),
                "reasoning": out.get("reasoning", ""),
            }
        return {"verdict": "SOFTEN", "reasoning": "P0 shim: size OK"}