#!/usr/bin/env bash
# OPTIONAL live MCP smoke — requires GITHUB_PERSONAL_ACCESS_TOKEN.
# Excluded from required CI. Keyless CI never runs this script.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIN="c59e8c199efbf14467211861de44afaeeb6873e3"
BINARY="$ROOT/bin/github-mcp-server"

export DISABLE_TELEMETRY=1
export DO_NOT_TRACK=1

if [[ -z "${GITHUB_PERSONAL_ACCESS_TOKEN:-}" ]]; then
  echo "GITHUB_PERSONAL_ACCESS_TOKEN is unset; live smoke skipped (optional)." >&2
  exit 0
fi

if [[ ! -x "$BINARY" ]]; then
  echo "missing $BINARY; run: bash scripts/upstream-github-mcp.sh first" >&2
  exit 1
fi

if ! "$BINARY" --help 2>&1 | grep -q -- '--lockdown-mode'; then
  echo "binary missing --lockdown-mode flag" >&2
  exit 1
fi
if ! "$BINARY" --help 2>&1 | grep -q -- '--read-only'; then
  echo "binary missing --read-only flag" >&2
  exit 1
fi

OUT="$(mktemp)"
ERR="$(mktemp)"
cleanup() { rm -f "$OUT" "$ERR"; }
trap cleanup EXIT

INIT='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"minilab-live-smoke","version":"0.1.0"}}}'
printf '%s\n' "$INIT" | "$BINARY" stdio --lockdown-mode --read-only >"$OUT" 2>"$ERR" &
PID=$!
sleep 3
kill "$PID" 2>/dev/null || true
wait "$PID" 2>/dev/null || true

if ! grep -qE 'serverInfo|protocolVersion|"result"' "$OUT" 2>/dev/null; then
  echo "live smoke: no MCP initialize result at pin $PIN" >&2
  echo "--- stdout ---" >&2
  cat "$OUT" >&2 || true
  echo "--- stderr ---" >&2
  cat "$ERR" >&2 || true
  exit 1
fi

echo "live MCP smoke OK (lockdown + read-only) at pin $PIN"
