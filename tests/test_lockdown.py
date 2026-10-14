"""Parse Lockdown Mode / read-only flags from upstream README at the pin."""

from __future__ import annotations

from pathlib import Path

import pytest

from github_mcp_lockdown import PIN, parse_lockdown_docs

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "vendor" / "github-mcp-server" / "README.md"
FIXTURE = ROOT / "tests" / "fixtures" / "readme-lockdown-excerpt.md"


def test_pin_constant() -> None:
    assert PIN.startswith("c59e8c199efb")
    assert len(PIN) == 40


def test_parse_fixture_excerpt() -> None:
    flags = parse_lockdown_docs(FIXTURE)
    assert flags.lockdown_cli == "--lockdown-mode"
    assert flags.lockdown_env == "GITHUB_LOCKDOWN_MODE"
    assert flags.read_only_cli == "--read-only"
    assert flags.read_only_env == "GITHUB_READ_ONLY"
    assert flags.http_lockdown_header == "X-MCP-Lockdown"
    assert flags.mentions_not_auth_boundary is True
    assert "github-actions[bot]" in flags.trusted_bots
    assert "copilot" in flags.trusted_bots


@pytest.mark.skipif(not README.is_file(), reason="vendor README missing; run vendor-upstream.sh")
def test_parse_vendored_readme_at_pin() -> None:
    flags = parse_lockdown_docs(README)
    assert flags.lockdown_cli == "--lockdown-mode"
    assert flags.lockdown_env == "GITHUB_LOCKDOWN_MODE"
    assert flags.read_only_cli == "--read-only"
    assert flags.mentions_not_auth_boundary is True
