"""Load Champion persona system prompts (USB / repo champions/)."""

from __future__ import annotations

from pathlib import Path


def champions_root() -> Path:
    return Path(__file__).resolve().parents[2] / "champions"


def load_system_prompt(champion_id: str) -> str:
    root = champions_root() / champion_id / "system_prompt.txt"
    if root.is_file():
        return root.read_text(encoding="utf-8")
    return f"You are the LYGO Champion {champion_id}. Operate with verify-first ethics."