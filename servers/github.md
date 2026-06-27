# github

GitHub operations from an agent — repositories, issues, pull requests, code search, and
Actions — via the official GitHub MCP server, run locally in Docker.

| | |
|---|---|
| **Repo** | [`github/github-mcp-server`](https://github.com/github/github-mcp-server) (Go) |
| **Kind** | external (third-party server, run locally) |
| **Runner** | `docker` |
| **Command** | `docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server` |
| **Transport** | stdio |
| **Auth** | api-key (GitHub PAT) |
| **Status** | stable |

## What it does

Exposes GitHub as MCP tools: read/create issues and PRs, browse and search code, manage
files and branches, and inspect Actions runs. The personal access token scopes what the
agent can see and do.

## Wire it up

Drop-in: [`snippets/github.mcp.json`](../snippets/github.mcp.json)

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    }
  }
}
```

Provide the PAT via the `${GITHUB_TOKEN}` env-ref — **never commit the literal token**.

> **Variants.** The `.github_org` umbrella pins the image by digest
> (`ghcr.io/github/github-mcp-server@sha256:…`) for reproducibility. Two alternatives exist:
> the legacy npm package `@modelcontextprotocol/server-github` via `bunx` (deprecated), and
> the remote OAuth endpoint `https://api.githubcopilot.com/mcp/` (no local runtime).

## Tools

Repository, issue, pull-request, code-search, file, branch, and Actions tools (the exact
set depends on the server version and token scopes).
