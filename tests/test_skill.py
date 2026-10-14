"""Skill must teach Lockdown Mode for long-horizon Argon + repo tools."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".claude" / "skills" / "github-mcp-lockdown" / "SKILL.md"


def test_skill_exists_and_frontmatter() -> None:
    assert SKILL.is_file()
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---")
    assert "name: github-mcp-lockdown" in text
    assert "description:" in text


def test_skill_mentions_lockdown_and_argon() -> None:
    text = SKILL.read_text(encoding="utf-8").lower()
    assert "lockdown mode" in text or "lockdown-mode" in text
    assert "argon" in text
    assert "read-only" in text or "--read-only" in text
    assert "never paste" in text
    assert "token" in text
    assert "repo" in text


def test_no_skill_mirrors() -> None:
    assert not (ROOT / ".cursor" / "skills").exists()
    assert not (ROOT / ".agents" / "skills").exists()
