# Wiring MCP servers

How to register the servers in this catalog with Claude Code and Claude Desktop.

## Where config lives

| Client | File |
|---|---|
| Claude Code (project) | `.mcp.json` at the repo root, or `mcpServers` in `.claude/settings.json` |
| Claude Code (user, all projects) | `~/.claude/settings.json` |
| Claude Desktop | `claude_desktop_config.json` |

All use the same `mcpServers` object shape, so the snippets in [`../snippets/`](../snippets)
merge into any of them.

## Local servers (stdio)

`meta-mcp` and `weave` are local binaries. They must be on `PATH`.

```bash
# build both from the meta workspace
cargo build --release -p meta-mcp -p weave
# ...then ensure target/release is on PATH, or `cargo install --path` each.
```

Register everything local at once with [`../snippets/all-local.mcp.json`](../snippets/all-local.mcp.json),
or one at a time:

```bash
claude mcp add meta  --scope user -- meta-mcp
claude mcp add weave --scope user -- weave mcp
```

## Remote connectors (claude.ai)

The claude.ai connectors (Figma, Gmail, Notion, …) are OAuth-backed HTTP servers. Prefer
the **claude.ai Connectors directory** (Settings → Connectors) — it manages the endpoint
URL and auth. See [`../servers/claude-ai-connectors.md`](../servers/claude-ai-connectors.md).

## Verify

```bash
claude mcp list            # shows registered servers + reachability
```

Inside a session, the tools appear namespaced by server (`meta_*`, `weave_*`,
`mcp__claude_ai_*__*`).

## Merging snippets safely

`mcpServers` is a flat map keyed by server name. To combine snippets, copy each entry
into one `mcpServers` object — keys must be unique. Example combining local + Notion:

```json
{
  "mcpServers": {
    "meta":  { "command": "meta-mcp", "args": [] },
    "weave": { "command": "weave", "args": ["mcp"] },
    "Notion": { "type": "http", "url": "https://<from-connector-page>/notion/mcp" }
  }
}
```
