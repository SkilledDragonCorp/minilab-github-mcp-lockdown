# Fixture excerpt mirroring github/github-mcp-server README Lockdown / read-only sections

## Read-Only Mode

To run the server in read-only mode, you can use the `--read-only` flag.

```bash
./github-mcp-server --read-only
```

```bash
docker run -i --rm \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=<your-token> \
  -e GITHUB_READ_ONLY=1 \
  ghcr.io/github/github-mcp-server
```

## Lockdown Mode

Lockdown mode limits the content that the server will surface from public repositories.

Lockdown mode is a best-effort content filter intended to reduce the risk of prompt injection from untrusted repository content. It is **not** an authorization boundary: it does not change what the underlying GitHub credential can read or write.

As an intentional exception, content authored by a small set of trusted bot accounts (currently `github-actions[bot]` and `copilot`) is always treated as safe.

```bash
./github-mcp-server --lockdown-mode
```

```bash
docker run -i --rm \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=<your-token> \
  -e GITHUB_LOCKDOWN_MODE=1 \
  ghcr.io/github/github-mcp-server
```

In HTTP mode, this flag (or `GITHUB_LOCKDOWN_MODE`) is an upper bound: the `X-MCP-Lockdown` request header can enable lockdown mode when the operator has not, but it cannot disable lockdown mode the operator has already enabled.
