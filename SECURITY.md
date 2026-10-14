# Security Policy

**Built by [SkilledDragon LLC](https://skilleddragon.com)**

This is a **SkilledDragon educational minilab**, not a production product. We do **not** maintain these repos on a regular schedule and we do **not** operate a vulnerability response program for them.

## Contact

General questions: **hello@skilleddragon.com**  
Do not use a dedicated security mailbox for this repo — none exists.

## If you find an issue

- Prefer reporting **upstream** when the issue is in [github/github-mcp-server](https://github.com/github/github-mcp-server).
- For something specific to this minilab's parsers or CI, you may email hello@skilleddragon.com. There is **no SLA**, and we may not patch or reply quickly.

## Supported versions

Only the commit currently on `main` is considered current for this educational lab.

## Secret handling

- Never commit `.env`, API keys, or tokens.
- Secrets are read from environment variables (local `.env`; GitHub Actions secrets in CI).
- CI is keyless. Optional `GITHUB_PERSONAL_ACCESS_TOKEN` is for live MCP smoke outside required CI only.
- Never paste tokens into prompts, chat logs, or skill copies.
- Set `DISABLE_TELEMETRY=1` and `DO_NOT_TRACK=1` for lab runs.
- Lockdown Mode is a best-effort content filter — not an authorization boundary for the underlying credential.

## Tooling pins

| Control | Pin |
| --- | --- |
| Upstream | `github/github-mcp-server` @ `c59e8c199efbf14467211861de44afaeeb6873e3` (MIT) |
| gitleaks | `v8.30.1` (pre-commit hook + CI binary with SHA256 verify) |
| Dependency audit | `uv export --frozen --format requirements-txt --no-emit-project > /tmp/req.txt` then `uvx pip-audit --strict -r /tmp/req.txt` |

## Upstream license

`github/github-mcp-server` is MIT. Use at your own risk. Pin versions, review the code, and treat this as sample material.
