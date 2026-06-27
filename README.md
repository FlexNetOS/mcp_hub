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
| **icm** | local | stdio | `icm_*` | [snippet](snippets/icm.mcp.json) | [icm.md](servers/icm.md) |
| **vox** | local | stdio | `vox_*` | [snippet](snippets/vox.mcp.json) | [vox.md](servers/vox.md) |
| **n8n-mcp** | external | stdio (npx) | 7 core + 13 mgmt (`n8n_*`) | [snippet](snippets/n8n-mcp.mcp.json) · [secretd](snippets/n8n-mcp-secretd.mcp.json) | [n8n-mcp.md](servers/n8n-mcp.md) |
| **context7** | external | stdio (bunx) | `resolve-library-id`, `query-docs` | [snippet](snippets/context7.mcp.json) | [context7.md](servers/context7.md) |
| **playwright** (browser extension) | external | stdio (bunx) | `mcp__playwright__*` | [snippet](snippets/playwright.mcp.json) | [playwright.md](servers/playwright.md) |
| **github** | external | stdio (docker) | repo · issues · PRs · Actions | [snippet](snippets/github.mcp.json) | [github.md](servers/github.md) |
| **memory** | external | stdio (bunx) | knowledge-graph (`create_entities`, …) | [snippet](snippets/memory.mcp.json) | [memory.md](servers/memory.md) |
| **sequential-thinking** | external | stdio (bunx) | `sequentialthinking` | [snippet](snippets/sequential-thinking.mcp.json) | [sequential-thinking.md](servers/sequential-thinking.md) |
| **Cloudflare Developer Platform** | remote | http (OAuth) | `mcp__claude_ai_Cloudflare_Developer_Platform__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Figma** | remote | http (OAuth) | `mcp__claude_ai_Figma__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Gmail** | remote | http (OAuth) | `mcp__claude_ai_Gmail__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Google Calendar** | remote | http (OAuth) | `mcp__claude_ai_Google_Calendar__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Google Drive** | remote | http (OAuth) | `mcp__claude_ai_Google_Drive__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Hugging Face** | remote | http (OAuth) | `mcp__claude_ai_Hugging_Face__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Microsoft 365** | remote | http (OAuth) | `mcp__claude_ai_Microsoft_365__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **Notion** | remote | http (OAuth) | `mcp__claude_ai_Notion__*` | [snippet](snippets/claude-ai.mcp.json) | [claude-ai-connectors.md](servers/claude-ai-connectors.md) |
| **exa** | remote | http | `web_search` + content | [snippet](snippets/exa.mcp.json) | [exa.md](servers/exa.md) |
| **n8n-builtin** | remote | http (Bearer) | 1 tool per workflow | [snippet](snippets/n8n-builtin.mcp.json) | [n8n-builtin.md](servers/n8n-builtin.md) |
| **cognitum** | remote | sse | 7 cloud tools | [snippet](snippets/cognitum.mcp.json) | [cognitum.md](servers/cognitum.md) |
| **cognitum-seed** | remote | sse | 114 on-device tools | [snippet](snippets/cognitum.mcp.json) | [cognitum.md](servers/cognitum.md) |

**local** = a FlexNetOS-built binary that must be on `PATH`.
**external** = a third-party server run locally (via `bunx`/Docker). Note: npm-package
servers use **`bunx`**, not `npx` — the meta-managed JS runtime is Bun and the bundled
`npx` is non-functional in this workspace.
**remote** = an OAuth-backed HTTP connector hosted via claude.ai (may be unavailable in headless runs).

Each entry also has a **`hosting`** value — where its *code* lives:
`peer` (top-level meta workspace member, e.g. meta-mcp/weave), `mcp_hub-child` (a forked
external server hosted under mcp_hub via this repo's `.meta.yaml`, e.g. n8n-mcp), or
`registry-only` (no code — unmodified third-party or remote connector). The policy is in
[`docs/server-hosting.md`](docs/server-hosting.md).

### Known, not cataloged

These MCP servers are wired in individual workspace repos but are **intentionally not
cataloged** (see the inventory in [`docs/claude-config-inventory.md`](docs/claude-config-inventory.md)):

- **agentic-flow**, **claude-flow** (`meta-ruvector`) — experimental ruvector R&D,
  `autoStart:false`.
- **qmd** (`obsidian-mind`) — repo-local Node script (`.claude/scripts/qmd-mcp.mjs`), not
  portable.
- **t** (`oh-my-claudecode`) — plugin-local bridge (`${CLAUDE_PLUGIN_ROOT}/bridge/…`).
- **flow-nexus** (`ruflo`) — hardcoded `/workspaces/flow-cloud` devcontainer path; not
  portable outside that container.

They can be promoted to the catalog if/when they become portable and stable.

## Quick start

Register all four local FlexNetOS servers in one go:

```bash
# build the binaries from the meta workspace
cargo build --release -p meta-mcp -p weave -p icm -p vox
# then merge snippets/all-local.mcp.json into your Claude config, or:
claude mcp add meta  --scope user -- meta-mcp
claude mcp add weave --scope user -- weave mcp
claude mcp add icm   --scope user -- icm serve
claude mcp add vox   --scope user -- vox serve
```

For the claude.ai connectors, enable them in the claude.ai Connectors directory
(Settings → Connectors). Full instructions: [`docs/wiring.md`](docs/wiring.md).

## Layout

```
mcp_hub/
├── registry.json                  # machine-readable index of every server (source of truth)
├── registry.schema.json           # JSON Schema for registry entries
├── CONTRIBUTING.md                # how to add a server (the intake process)
├── .meta.yaml                     # nested meta: hosted external servers (mcp_hub-child)
├── n8n-mcp/                        # ← cloned by `meta git update -r` (gitignored)
├── snippets/                      # copy-paste .mcp.json fragments
│   ├── meta.mcp.json
│   ├── weave.mcp.json
│   ├── n8n-mcp.mcp.json
│   ├── n8n-mcp-secretd.mcp.json   # n8n-mcp with the secretd key wrapper (localhost)
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
    ├── wiring.md                  # how to register with Claude Code / Desktop
    ├── server-hosting.md          # policy: peer vs mcp_hub-child vs registry-only
    └── claude-config-inventory.md # census: what's actually wired across ~/ (vs the catalog)
```

A live census of every Claude Code config surface under `/home/drdave` and the MCP servers
+ plugins each wires — i.e. *what is actually wired across the box*, a superset of this
catalog — lives in
[`docs/claude-config-inventory.md`](docs/claude-config-inventory.md).

## Adding a server

`registry.json` is the source of truth; the snippet, doc, and the Catalog table above
mirror it. To add a server: add a registry entry (per
[`registry.schema.json`](registry.schema.json)), a `snippets/<id>.mcp.json`, a
`servers/<id>.md`, and a Catalog row — then run `python3 scripts/validate.py`.

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for the full process and the
`kind`/`hosting`/`runner`/`transport`/`auth` conventions, and
**[docs/server-hosting.md](docs/server-hosting.md)** for *where* a server's code should
live (peer vs mcp_hub-child vs registry-only).

## Scope

This catalogs **MCP servers** (tool providers for AI agents). It does not catalog the
`meta` plugin system or CLI tools — those live in their own repos. The `hosting` field
records where each server's code lives: `peer` servers are top-level workspace members
(`meta_mcp/`, `weave/`); `mcp_hub-child` servers are forks hosted here via `.meta.yaml`
(`n8n-mcp/`); `registry-only` servers (unmodified third-party + remote connectors) are
cataloged for discoverability but live outside the workspace. See
[docs/server-hosting.md](docs/server-hosting.md).
