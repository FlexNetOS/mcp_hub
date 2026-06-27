# sequential-thinking

A single tool for structured, step-by-step reflective reasoning — break a hard problem
into a sequence of revisable thoughts.

| | |
|---|---|
| **Repo** | [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) (`src/sequentialthinking`, MIT) |
| **Kind** | external (official reference server) |
| **Runner** | `bunx` (see note below) |
| **Command** | `bunx -y @modelcontextprotocol/server-sequential-thinking` |
| **Transport** | stdio |
| **Auth** | none |
| **Status** | stable |

## What it does

Exposes one `sequentialthinking` tool that lets the model lay out a problem as numbered
thoughts, revise earlier steps, branch, and converge — a scaffold for dynamic, reflective
problem-solving.

> **Runner note:** uses `bunx`, not `npx` — the meta-managed JS runtime is Bun and the
> bundled `node`/`npx` is non-functional in this workspace.

## Wire it up

Drop-in: [`snippets/sequential-thinking.mcp.json`](../snippets/sequential-thinking.mcp.json)

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "bunx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

## Tools

`sequentialthinking`.
