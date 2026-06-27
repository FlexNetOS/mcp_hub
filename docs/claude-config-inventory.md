# Claude Code config inventory — `/home/drdave`

**Scan date:** 2026-06-26 · **Scope:** Claude Code only, **active** configs.

A census of every Claude Code configuration surface under `/home/drdave` and the MCP
servers + plugins each one wires. Companion to [`../registry.json`](../registry.json) — the
registry is the *canonical catalog* of servers meta ships; this doc is *what is actually
wired across the box right now* (which is a superset, and where drift lives).

> The exhaustive per-config component breakdown (commands / skills / agents / hooks / rules
> / settings / statusline, one row per active `.claude`) is a **deferred follow-up** —
> tracked as KB task `tasks/claude-component-inventory`.

## Methodology

RTK's hook rewrites bare `find` to `rtk find` (different semantics), so the census was run
with `rtk proxy` (raw passthrough):

```bash
# all .claude dirs (135 found)
rtk proxy find /home/drdave \
  -type d \( -name node_modules -o -name target -o -name .git -o -name .rustup \
            -o -name registry -o -name .npm -o -name .cargo \) -prune \
  -o -type d -name .claude -print | sort

# all MCP config files (209 found)
rtk proxy find /home/drdave … -o -type f \
  \( -name '.mcp.json' -o -name 'mcp.json' -o -name '.claude.json' \) -print | sort
```

**Totals:** 135 `.claude` dirs · 209 MCP config files · **~48 active** `.claude` under
`meta` after pruning noise. The rest is noise (see §A) or sibling-tool configs (§D).

## A. Active `.claude` config surfaces

Claude Code loads config from three scopes: **user** (`~/.claude`, `~/.claude.json`),
**project** (`<repo>/.claude`, `<repo>/.mcp.json`), and **plugins** (enabled in user
settings). The user scope is a mirror **into** the meta-tracked source of truth.

| Tier | Path | Role |
|------|------|------|
| User SoT | `meta/envctl/home/.claude` | source of truth (committed in `envctl`) |
| User mirror | `~/.claude` | `settings.json` + `plugins/` are symlinks **into** the SoT (verified via `readlink -f`) |
| Project root | `meta/.claude` | meta-repo project scope |
| Per-repo | meta child repos (below) | each repo's own `.claude` layer |

**Active meta child-repo `.claude` dirs:** `agent`, `atc`, `claude-code`, `ECC`, `envctl`,
`flexnetos_runner`, `handoff` (+`crates/tui`), `harness-agent-rs`, `harness_hub`
(+`handoff-loop`), `icm`, `lane`, `lifeos`, `loop_lib`, `meta_cli`, `meta_dashboard_cli`,
`meta_git_cli`, `meta_git_lib`, `meta_mcp`, `meta-ruvector` (+`crates/ruvector-cli`,
`ui/ruvocal`), `n8n`, `network-control`, `obsidian-mind`, `prompt_hub`, `rtk-tokenkill`,
`ruflo`, `rusty-idd`, `teri`, `vox`, `weave`, `yazelix`, `meta-yard/Archon`,
`vault_hub/kasetto`, `tool_hub/repos/{bun,uv}`.

**Excluded as noise (found, not catalogued):** `.bun/install/cache/*`, `.cache/JetBrains/*`,
`Desktop/_archives/*` (incl. the `claude-move-*` backup), `flexnetos_runner/_work/*` (CI
runner mirrors), `.worktrees/*` (transient git worktrees), `.local/share/Trash`,
`.local-migration-backups`, `.local/share/envctl/repos`, `Downloads/tmp/*`,
`.n8n-claude-bridge/sandbox`, and vendored trees (`rusty-idd/{imports,third_party}`,
`meta-ruvector/{external,examples,.codex}`, `ruflo/v3`, `weave/.handoff/run`,
`oh-my-pi` fixtures).

## B. MCP servers (active Claude scope)

**User scope — live, global** (`~/.claude.json` → `mcpServers`):
`context7`, `icm`, `playwright`, `vox`, `weave`.
The meta project entry (`projects."…/meta".mcpServers`) additionally pins `icm`.

**Plugin-provided** (`meta@gitkb` plugin → `meta/claude-plugin/.mcp.json`):
`meta` (`meta-mcp`).

**Project scope — auto-loaded root `<repo>/.mcp.json`:**

| Repo | Servers |
|------|---------|
| `ECC` | context7, exa, github, memory, playwright, sequential-thinking |
| `envctl` | context7, exa, github, memory, n8n-mcp, playwright, sequential-thinking |
| `.github_org` | github, n8n-mcp |
| `meta-ruvector` | agentic-flow, claude-flow, cognitum, cognitum-seed |
| `n8n` | n8n-builtin, n8n-mcp |
| `obsidian-mind` | qmd |
| `oh-my-claudecode` | t |
| `ruflo` | flow-nexus — **via legacy `.claude/mcp.json`, not root `.mcp.json`** (see §E) |

**Distinct servers seen across the active surface:** agentic-flow, claude-flow, cognitum,
cognitum-seed, context7, exa, flow-nexus, github, icm, memory, meta, n8n-builtin, n8n-mcp,
playwright, qmd, sequential-thinking, t, vox, weave.

## C. Plugins (SoT: `meta/envctl/home/.claude/`)

- **Marketplaces:** `gitkb` (local dir `meta/claude-plugins`), `harness-marketplace` (local
  dir `meta/harness_hub/harness`), `claude-plugins-official` (+ a `.bak` copy).
- **Installed (cache):**
  - `claude-plugins-official` → `claude-code-setup`, `code-review`, `frontend-design`,
    `github`, `hookify`, `playwright`, `ralph-loop`, `rust-analyzer-lsp`, `superpowers`,
    `typescript-lsp`, `ui5-typescript-conversion`
  - `gitkb` → `gitkb`, `meta`
  - `harness-marketplace` → `harness`
- **Enabled** (`settings.json.enabledPlugins`): `gitkb@gitkb`,
  `harness@harness-marketplace`, `meta@gitkb`, `rust-analyzer-lsp@claude-plugins-official`.

## D. Appendix — sibling agent-tool MCP configs (out of scope)

Not Claude Code; listed so they're not mistaken for Claude config:
`.ai/mcp/mcp.json`, `.aws/amazonq/mcp.json`, `.config/Code/User/mcp.json` (VS Code),
`.config/github-copilot/intellij/mcp.json`, `.cursor/mcp.json`, `.junie/mcp/mcp.json`
(JetBrains Junie), `.roo/mcp.json` (Roo) — plus meta-local `.ai`/`.junie`/`.roo` — and
OpenAI Codex plugin caches under `.codex/` and `meta/.local/share/codex/`.

## E. Observed drift (surfaced, not fixed here)

1. **`ruflo` legacy path** — wires `flow-nexus` via `.claude/mcp.json` instead of root
   `.mcp.json`; Claude Code won't auto-load it from that path.
2. **Duplicate `playwright` / `context7` definitions** — user-scope literal/bunx forms vs.
   the catalog/plugin `${ENV}`-ref forms. Resolved by Claude's **user > plugin** precedence,
   so the user-scope form wins on this box; the plugin form is the portable fallback.
3. **Catalog gap** — repos wire servers absent from [`../registry.json`](../registry.json):
   `exa`, `memory`, `sequential-thinking`, `n8n-mcp`, `agentic-flow`, `claude-flow`,
   `cognitum`, `cognitum-seed`, `flow-nexus`, `qmd`, `t`, `n8n-builtin`. The catalog is a
   subset of what's actually wired.
