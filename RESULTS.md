# Results

Local ship gate recorded **2026-10-14** (keyless lab suite + upstream Go pin).

- Python `3.14.7` · `ruff 0.17.0` · `pytest 9.1.1` · Go `1.26.8`
- Upstream pin `c59e8c199efbf14467211861de44afaeeb6873e3` (`main@c59e8c199efb`)

| Check | Result | Note |
| --- | --- | --- |
| `uv sync --locked --group dev` | **pass** | Lockfile committed |
| `uv run ruff check .` | **pass** | All checks passed |
| `uv run ruff format --check .` | **pass** | Formatted |
| `uv run pytest -q` | **pass** | 10 passed |
| `python3 scripts/check-skills` | **pass** | skills-layout OK |
| `python3 scripts/check-banned-phrases` | **pass** | banned-phrases OK |
| `python3 scripts/check-upstream-parity` | **pass** | upstream-parity OK |
| `bash scripts/upstream-github-mcp.sh` | **pass** | `script/test` + `go build -v ./cmd/github-mcp-server`; `bin/github-mcp-server` present |

Pytest: **10 passed**.

Optional `scripts/live-mcp-smoke.sh` is excluded from required CI.
