"""Parity checks for upstream-github-mcp.sh."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_check_upstream_parity_script() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check-upstream-parity")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_upstream_script_keyless_commands() -> None:
    text = (ROOT / "scripts" / "upstream-github-mcp.sh").read_text(encoding="utf-8")
    assert "script/test" in text
    assert "go build -v ./cmd/github-mcp-server" in text
    assert "go test -race" in text
    assert "./..." in text
    assert "c59e8c199efbf14467211861de44afaeeb6873e3" in text
    # Required upstream path must not demand a live token.
    for line in text.splitlines():
        if line.strip().startswith("#"):
            continue
        assert "GITHUB_PERSONAL_ACCESS_TOKEN" not in line


def test_live_smoke_is_optional_and_separate() -> None:
    live = ROOT / "scripts" / "live-mcp-smoke.sh"
    assert live.is_file()
    text = live.read_text(encoding="utf-8")
    assert "GITHUB_PERSONAL_ACCESS_TOKEN" in text
    assert "OPTIONAL" in text or "optional" in text
    ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "live-mcp-smoke" not in ci
