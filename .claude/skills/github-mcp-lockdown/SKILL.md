---
name: github-mcp-lockdown
description: Enable Lockdown Mode and read-only on github/github-mcp-server for long-horizon Gemini 4 Argon agent flows that need repo tools without soaking untrusted public-repo content.
---

# GitHub MCP Lockdown

Use [github/github-mcp-server](https://github.com/github/github-mcp-server) with **Lockdown Mode** and **read-only** when a long-horizon agent (Gemini 4 Argon and peers) needs GitHub repo tools but must not pull the whole untrusted public surface into context.

## When to enable

Enable Lockdown Mode when the agent will read issues, PRs, comments, or commits from **public** repositories that may contain prompt-injection payloads from authors without push access.

Combine with read-only when the agent should not mutate repos, issues, or PRs.

```bash
export DISABLE_TELEMETRY=1
export DO_NOT_TRACK=1
# Fine-grained PAT in the environment only — never paste tokens into prompts.
export GITHUB_PERSONAL_ACCESS_TOKEN=...   # optional live path
./github-mcp-server --lockdown-mode --read-only
# or: GITHUB_LOCKDOWN_MODE=1 GITHUB_READ_ONLY=1 ./github-mcp-server
```

## What Lockdown Mode does

- Filters public-repo content so items from authors **without push access** are withheld or error.
- Private repos and collaborators' own content stay available.
- Trusted bots (`github-actions[bot]`, `copilot`) stay visible so CI noise is not blanked.
- Best-effort content filter — **not** an authorization boundary. The credential's GitHub API scope is unchanged.

## Long-horizon Argon + repo tools

For multi-hour Argon sessions that browse many public issues/PRs:

1. Prefer `--toolsets` allow-lists (repos, issues, pull_requests) over `all`.
2. Always set `--lockdown-mode` for public-repo reads.
3. Prefer `--read-only` unless the session must write.
4. Keep `GITHUB_PERSONAL_ACCESS_TOKEN` in env / secret store — never in the prompt, skill text copies, or chat logs.

## Lab commands (keyless)

```bash
bash scripts/vendor-upstream.sh
uv sync --locked --group dev
uv run github-mcp-lockdown          # parse Lockdown flags from pin README
uv run pytest -q
bash scripts/upstream-github-mcp.sh # script/test + go build at pin
```

Optional live smoke (not CI): `bash scripts/live-mcp-smoke.sh` with `GITHUB_PERSONAL_ACCESS_TOKEN` set.

## Upstream pin

`vendor/github-mcp-server` @ `c59e8c199efbf14467211861de44afaeeb6873e3` (`main@c59e8c199efb`).
