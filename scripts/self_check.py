#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    from lygo_claw.gatekeeper import P0Gatekeeper
    from lygo_claw.gateway import SovereignGateway

    p0 = P0Gatekeeper().validate("lygo-claw self check")
    gw = SovereignGateway().ingest("self check", tool_name="self_check")
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "tests", "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    out = {"p0": p0, "gateway_ok": gw.get("ok"), "pytest_exit": r.returncode}
    print(json.dumps(out, indent=2))
    return 0 if r.returncode == 0 and gw.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())