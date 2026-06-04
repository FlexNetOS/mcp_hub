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
| **n8n-mcp** | external | stdio (npx) | 7 core + 13 mgmt (`n8n_*`) | [snippet](snippets/n8n-mcp.mcp.json) | [n8n-mcp.md](servers/n8n-mcp.md) |
| **Cloudflare Developer Platform** | remote | http (OAuth) | `mcp__claude_ai_Cloudflare_Developer_Platform__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Figma** | remote | http (OAuth) | `mcp__claude_ai_Figma__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Gmail** | remote | http (OAuth) | `mcp__claude_ai_Gmail__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Google Calendar** | remote | http (OAuth) | `mcp__claude_ai_Google_Calendar__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Google Drive** | remote | http (OAuth) | `mcp__claude_ai_Google_Drive__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Hugging Face** | remote | http (OAuth) | `mcp__claude_ai_Hugging_Face__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Microsoft 365** | remote | http (OAuth) | `mcp__claude_ai_Microsoft_365__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Notion** | remote | http (OAuth) | `mcp__claude_ai_Notion__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |

**local** = a FlexNetOS-built binary that must be on `PATH`.
**external** = a third-party server run locally (e.g. via `npx`/Docker).
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
├── registry.json                  # machine-readable index of every server (source of truth)
├── registry.schema.json           # JSON Schema for registry entries
├── CONTRIBUTING.md                # how to add a server (the intake process)
├── snippets/                      # copy-paste .mcp.json fragments
│   ├── meta.mcp.json
│   ├── weave.mcp.json
│   ├── n8n-mcp.mcp.json
│   ├── claude-ai.mcp.json         # remote connectors (placeholder URLs)
│   └── all-local.mcp.json         # meta + weave in one file
├── servers/                       # per-server reference docs
│   ├── meta_mcp.md
│   ├── weave.md
│   ├── n8n-mcp.md
│   └── claude-ai-connectors.md
├── templates/                     # starting points for new entries
│   ├── server.template.md
│   └── server.template.mcp.json
├── scripts/
│   └── validate.py                # registry ↔ snippets ↔ docs ↔ README checker (runs in CI)
└── docs/
    └── wiring.md                  # how to register with Claude Code / Desktop
```

## Adding a server

`registry.json` is the source of truth; the snippet, doc, and the Catalog table above
mirror it. To add a server: add a registry entry (per
[`registry.schema.json`](registry.schema.json)), a `snippets/<id>.mcp.json`, a
`servers/<id>.md`, and a Catalog row — then run `python3 scripts/validate.py`.

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for the full process, the `kind`/`runner`/
`transport`/`auth` conventions, and the templates in [`templates/`](templates).

## Scope

This catalogs **MCP servers** (tool providers for AI agents). It does not catalog the
`meta` plugin system or CLI tools — those live in their own repos. `local` servers are
workspace members (`meta_mcp/`, `weave/`; see the workspace `.meta.yaml`); `external` and
`remote` servers are cataloged for discoverability but live outside the workspace.
