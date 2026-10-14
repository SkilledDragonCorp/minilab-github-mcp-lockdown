"""CLI parses fixture Lockdown docs without a live token."""

from __future__ import annotations

import json
from pathlib import Path

from github_mcp_lockdown.cli import main

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "readme-lockdown-excerpt.md"


def test_cli_json_on_fixture(capsys) -> None:
    code = main([str(FIXTURE), "--json"])
    assert code == 0
    data = json.loads(capsys.readouterr().out)
    assert data["lockdown_cli"] == "--lockdown-mode"
    assert data["read_only_cli"] == "--read-only"
