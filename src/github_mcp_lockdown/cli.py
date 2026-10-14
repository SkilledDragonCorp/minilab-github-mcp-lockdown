"""CLI: parse Lockdown Mode docs from vendored upstream README."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from github_mcp_lockdown import PIN, parse_lockdown_docs


def default_readme() -> Path:
    root = Path(__file__).resolve().parents[2]
    return root / "vendor" / "github-mcp-server" / "README.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Parse github-mcp-server Lockdown Mode / read-only flags at the pin."
    )
    parser.add_argument(
        "readme",
        nargs="?",
        type=Path,
        default=None,
        help="Path to upstream README.md (default: vendor/github-mcp-server/README.md)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit LockdownFlags as JSON",
    )
    args = parser.parse_args(argv)
    readme = args.readme or default_readme()
    if not readme.is_file():
        print(
            f"missing {readme}; run: bash scripts/vendor-upstream.sh",
            file=sys.stderr,
        )
        return 1

    flags = parse_lockdown_docs(readme)
    if args.json:
        print(
            json.dumps(
                {
                    "pin": PIN,
                    "lockdown_cli": flags.lockdown_cli,
                    "lockdown_env": flags.lockdown_env,
                    "read_only_cli": flags.read_only_cli,
                    "read_only_env": flags.read_only_env,
                    "http_lockdown_header": flags.http_lockdown_header,
                    "mentions_not_auth_boundary": flags.mentions_not_auth_boundary,
                    "trusted_bots": list(flags.trusted_bots),
                },
                indent=2,
            )
        )
    else:
        print(f"pin={PIN}")
        print(f"lockdown: {flags.lockdown_cli} / {flags.lockdown_env}=1")
        print(f"read-only: {flags.read_only_cli} / {flags.read_only_env}=1")
        print(f"http_header: {flags.http_lockdown_header}")
        print(f"not_auth_boundary={flags.mentions_not_auth_boundary}")
        print(f"trusted_bots={','.join(flags.trusted_bots)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
