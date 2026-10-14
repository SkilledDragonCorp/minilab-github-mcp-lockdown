"""Document Lockdown Mode and read-only flags from upstream README at the pin."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LockdownFlags:
    """Flags and env vars for Lockdown Mode + read-only (from upstream README)."""

    lockdown_cli: str
    lockdown_env: str
    read_only_cli: str
    read_only_env: str
    http_lockdown_header: str
    mentions_not_auth_boundary: bool
    trusted_bots: tuple[str, ...]


_LOCKDOWN_CLI = re.compile(r"--lockdown-mode")
_LOCKDOWN_ENV = re.compile(r"GITHUB_LOCKDOWN_MODE")
_READ_ONLY_CLI = re.compile(r"--read-only")
_READ_ONLY_ENV = re.compile(r"GITHUB_READ_ONLY")
_HTTP_HEADER = re.compile(r"X-MCP-Lockdown")
_NOT_AUTH = re.compile(r"not\s+an\s+authorization\s+boundary", re.IGNORECASE)
_BOTS = re.compile(
    r"`(github-actions\[bot\]|copilot)`",
    re.IGNORECASE,
)


def parse_lockdown_docs(readme: Path | str) -> LockdownFlags:
    """Parse Lockdown Mode / read-only documentation from upstream README text or path."""
    text = Path(readme).read_text(encoding="utf-8") if not isinstance(readme, str) else readme
    # Strip markdown emphasis so "**not** an authorization boundary" still matches.
    plain = text.replace("*", "")

    if not _LOCKDOWN_CLI.search(text):
        raise ValueError("upstream README missing --lockdown-mode")
    if not _LOCKDOWN_ENV.search(text):
        raise ValueError("upstream README missing GITHUB_LOCKDOWN_MODE")
    if not _READ_ONLY_CLI.search(text):
        raise ValueError("upstream README missing --read-only")
    if not _READ_ONLY_ENV.search(text):
        raise ValueError("upstream README missing GITHUB_READ_ONLY")
    if not _HTTP_HEADER.search(text):
        raise ValueError("upstream README missing X-MCP-Lockdown")

    bots = tuple(sorted({m.group(1) for m in _BOTS.finditer(text)}))
    if "github-actions[bot]" not in bots or "copilot" not in bots:
        raise ValueError("upstream README missing trusted bot accounts for Lockdown Mode")

    return LockdownFlags(
        lockdown_cli="--lockdown-mode",
        lockdown_env="GITHUB_LOCKDOWN_MODE",
        read_only_cli="--read-only",
        read_only_env="GITHUB_READ_ONLY",
        http_lockdown_header="X-MCP-Lockdown",
        mentions_not_auth_boundary=bool(_NOT_AUTH.search(plain)),
        trusted_bots=bots,
    )
