#!/usr/bin/env python3
"""Verify a public LYGO CLAW USB tree is boot-ready and secret-free."""

from __future__ import annotations

import argparse
import json
import re
import socket
import sys
from pathlib import Path

FORBIDDEN_PARTS = (
    "boot/",
    "_builder_vault/",
    ".git/",
    "CLAWNCH_TOKEN",
)
FORBIDDEN_NAMES = {
    ".env",
    "credentials.json",
    "core_signing.key",
    "id_rsa",
    "wallet.json",
    "token_config.json",
}
SECRET_PATTERNS = (
    re.compile(r"sk-[a-zA-Z0-9]{20,}"),
    re.compile(r"ghp_[a-zA-Z0-9]{20,}"),
    re.compile(r"xai-[a-zA-Z0-9]{20,}"),
    re.compile(r"nvapi-[a-zA-Z0-9]{20,}"),
)
REQUIRED = (
    "LYGO_CLAW_Launch.bat",
    "LYGO_Gateway.ps1",
    "LYGO_Ollama_USB_Boot.ps1",
    "lygo-claw/lygo.json",
    "dashboard/lygo-claw.html",
    "tools/node/node.exe",
    "tools/lygo-gateway/dist/entry.js",
    "README.txt",
    "START_HERE_USB.txt",
)


def port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


SKIP_TEXT_SCAN_PREFIXES = (
    "models/ollama/blobs/",
    "product/runtime/ollama/",
    "tools/lygo-gateway/node_modules/",
)
TEXT_SUFFIXES = {
    ".html", ".htm", ".md", ".txt", ".json", ".js", ".mjs", ".cjs", ".ts",
    ".bat", ".cmd", ".ps1", ".py", ".css", ".xml", ".yml", ".yaml", ".env",
}


def scan_secrets(root: Path) -> list[str]:
    hits: list[str] = []
    for f in root.rglob("*"):
        if not f.is_file():
            continue
        rel = f.relative_to(root).as_posix()
        if any(p in rel for p in FORBIDDEN_PARTS):
            hits.append(f"forbidden_path:{rel}")
        if f.name in FORBIDDEN_NAMES and "node_modules/" not in rel:
            hits.append(f"forbidden_name:{rel}")
        if f.suffix.lower() in {".log", ".err"} and "logs" not in rel:
            if rel.startswith(("gw_", "gateway_", "restore_")):
                hits.append(f"runtime_log:{rel}")
        if any(rel.startswith(p) for p in SKIP_TEXT_SCAN_PREFIXES):
            continue
        if f.suffix.lower() not in TEXT_SUFFIXES and f.name not in FORBIDDEN_NAMES:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")[:80000]
        except OSError:
            continue
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                hits.append(f"secret_pattern:{rel}")
                break
    return hits


def check_models(root: Path) -> dict:
    models_dir = root / "models" / "ollama"
    blobs = list(models_dir.glob("blobs/*")) if models_dir.exists() else []
    manifests = list(models_dir.glob("manifests/**/*")) if models_dir.exists() else []
    return {
        "models_dir": str(models_dir),
        "blob_count": len(blobs),
        "manifest_count": len([m for m in manifests if m.is_file()]),
        "weights_on_usb": len(blobs) > 0 and len(manifests) > 0,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("usb_root", nargs="?", default=str(Path(__file__).resolve().parents[1] / "usb"))
    ap.add_argument("--require-weights", action="store_true", help="Fail if model blobs missing")
    ap.add_argument("--check-ports", action="store_true", help="Require Ollama :11434 and Gateway :18789")
    args = ap.parse_args()
    root = Path(args.usb_root).resolve()
    if not root.is_dir():
        print(json.dumps({"ok": False, "error": f"missing root {root}"}, indent=2))
        return 1

    missing = [p for p in REQUIRED if not (root / p).exists()]
    hits = scan_secrets(root)
    models = check_models(root)
    ports = {
        "ollama_11434": port_open("127.0.0.1", 11434),
        "gateway_18789": port_open("127.0.0.1", 18789),
    }

    ok = not missing and not hits
    if args.require_weights and not models["weights_on_usb"]:
        ok = False
    if args.check_ports and not all(ports.values()):
        ok = False

    report = {
        "ok": ok,
        "root": str(root),
        "missing": missing,
        "secret_hits": hits[:30],
        "models": models,
        "ports": ports,
    }
    print(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())