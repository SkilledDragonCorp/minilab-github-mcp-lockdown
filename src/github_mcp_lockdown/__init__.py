"""Parse Lockdown Mode / read-only flags from github/github-mcp-server docs at pin."""

from __future__ import annotations

from github_mcp_lockdown.lockdown import LockdownFlags, parse_lockdown_docs

PIN = "c59e8c199efbf14467211861de44afaeeb6873e3"
UPSTREAM_REPO = "https://github.com/github/github-mcp-server"

__all__ = [
    "PIN",
    "UPSTREAM_REPO",
    "LockdownFlags",
    "parse_lockdown_docs",
]
