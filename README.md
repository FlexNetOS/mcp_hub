# mcp_hub

**Canonical registry and catalog of MCP servers used across the FlexNetOS meta workspace.**

One place to discover which MCP servers exist, what they do, and how to wire them into
Claude Code / Claude Desktop. Machine-readable index in [`registry.json`](registry.json);
copy-paste configs in [`snippets/`](snippets); per-server docs in [`servers/`](servers).

## Catalog

| Server | Kind | Transport | Tools | Wire-up | Doc |
|---|---|---|---|---|---|
| **meta** (`meta-mcp`) | local | stdio | 29 (`meta_*`) | [snippet](snippets/meta.mcp.json) | [meta_mcp.md](servers/meta_mcp.md) |
| **weave** | local | stdio | 11 (`weave_*`) | [snippet](snippets/weave.mcp.json) | [weave.md](servers/weave.md) |
| **Cloudflare Developer Platform** | remote | http (OAuth) | `mcp__claude_ai_Cloudflare_Developer_Platform__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Figma** | remote | http (OAuth) | `mcp__claude_ai_Figma__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Gmail** | remote | http (OAuth) | `mcp__claude_ai_Gmail__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Google Calendar** | remote | http (OAuth) | `mcp__claude_ai_Google_Calendar__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Google Drive** | remote | http (OAuth) | `mcp__claude_ai_Google_Drive__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Hugging Face** | remote | http (OAuth) | `mcp__claude_ai_Hugging_Face__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Microsoft 365** | remote | http (OAuth) | `mcp__claude_ai_Microsoft_365__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Notion** | remote | http (OAuth) | `mcp__claude_ai_Notion__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |

**local** = a FlexNetOS-built binary that must be on `PATH`.
**remote** = an OAuth-backed HTTP connector hosted via claude.ai (may be unavailable in headless runs).

## Quick start

Register both local FlexNetOS servers in one go:

```bash
# build the binaries from the meta workspace
cargo build --release -p meta-mcp -p weave
# then merge snippets/all-local.mcp.json into your Claude config, or:
claude mcp add meta  --scope user -- meta-mcp
claude mcp add weave --scope user -- weave mcp
```

For the claude.ai connectors, enable them in the claude.ai Connectors directory
(Settings → Connectors). Full instructions: [`docs/wiring.md`](docs/wiring.md).

## Layout

```
mcp_hub/
├── registry.json                  # machine-readable index of every server
├── snippets/                      # copy-paste .mcp.json fragments
│   ├── meta.mcp.json
│   ├── weave.mcp.json
│   ├── claude-ai.mcp.json         # remote connectors (placeholder URLs)
│   └── all-local.mcp.json         # meta + weave in one file
├── servers/                       # per-server reference docs
│   ├── meta_mcp.md
│   ├── weave.md
│   └── claude-ai-connectors.md
└── docs/
    └── wiring.md                  # how to register with Claude Code / Desktop
```

## Adding a server

1. Add an entry to [`registry.json`](registry.json) (`id`, `kind`, `transport`, `command`/`url`, `toolPrefix`, `summary`, `doc`, `snippet`).
2. Add a copy-paste fragment under [`snippets/`](snippets).
3. Add a reference doc under [`servers/`](servers).
4. Add a row to the **Catalog** table above.

Keep `registry.json` as the source of truth — the human-facing tables mirror it.

## Scope

This catalogs **MCP servers** (tool providers for AI agents). It does not catalog the
`meta` plugin system or CLI tools — those live in their own repos. Local servers in this
catalog are workspace members (`meta_mcp/`, `weave/`); see the workspace `.meta.yaml`.
