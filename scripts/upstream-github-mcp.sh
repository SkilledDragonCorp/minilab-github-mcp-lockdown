#!/usr/bin/env bash
# Keyless commands from github/github-mcp-server .github/workflows/go.yml
# at pin c59e8c199efbf14467211861de44afaeeb6873e3:
#   1. script/test  (contents: go test -race ./...)
#   2. go build -v ./cmd/github-mcp-server
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIN="c59e8c199efbf14467211861de44afaeeb6873e3"
UPSTREAM="$ROOT/vendor/github-mcp-server"
BIN_DIR="$ROOT/bin"
BINARY="$BIN_DIR/github-mcp-server"

export DISABLE_TELEMETRY=1
export DO_NOT_TRACK=1

if [[ ! -d "$UPSTREAM/.git" ]]; then
  echo "missing vendor/github-mcp-server; run: bash scripts/vendor-upstream.sh" >&2
  exit 1
fi

HEAD="$(git -C "$UPSTREAM" rev-parse HEAD)"
if [[ "$HEAD" != "$PIN" ]]; then
  echo "vendor pin mismatch: expected $PIN got $HEAD" >&2
  exit 1
fi

cd "$UPSTREAM"

# go.yml: run: script/test  →  go test -race ./...
# GitHub Actions (CI=true) uses script/test verbatim.
# Local hosts: raise package timeout — Darwin -race on pkg/github exceeds the default 10m.
if [[ "${CI:-}" == "true" ]]; then
  script/test
else
  go test -race -timeout 90m ./...
fi
go build -v ./cmd/github-mcp-server

mkdir -p "$BIN_DIR"
if [[ ! -f "$UPSTREAM/github-mcp-server" ]]; then
  echo "expected go build to write $UPSTREAM/github-mcp-server" >&2
  exit 1
fi
mv -f "$UPSTREAM/github-mcp-server" "$BINARY"
chmod +x "$BINARY"

if [[ ! -x "$BINARY" ]]; then
  echo "expected executable binary at $BINARY" >&2
  exit 1
fi

echo "upstream OK: binary at $BINARY ($(wc -c < "$BINARY" | tr -d ' ') bytes)"
