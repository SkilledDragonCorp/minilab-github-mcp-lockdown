#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIN="c59e8c199efbf14467211861de44afaeeb6873e3"
DEST="$ROOT/vendor/github-mcp-server"

mkdir -p "$ROOT/vendor"

if [[ -d "$DEST/.git" ]]; then
  git -C "$DEST" fetch --depth 1 origin "$PIN" || git -C "$DEST" fetch origin "$PIN"
  git -C "$DEST" checkout --force "$PIN"
else
  rm -rf "$DEST"
  git clone https://github.com/github/github-mcp-server.git "$DEST"
  git -C "$DEST" checkout "$PIN"
fi

HEAD="$(git -C "$DEST" rev-parse HEAD)"
if [[ "$HEAD" != "$PIN" ]]; then
  echo "vendor pin mismatch: expected $PIN got $HEAD" >&2
  exit 1
fi

echo "vendor/github-mcp-server @ $HEAD"
