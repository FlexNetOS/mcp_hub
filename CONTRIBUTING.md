# Adding a server to the catalog

This catalog has one source of truth — [`registry.json`](registry.json) — and three
mirrors that must stay consistent with it: a copy-paste **snippet**, a per-server
**doc**, and the **catalog table** in the README. The [`scripts/validate.py`](scripts/validate.py)
checker (run in CI) enforces that consistency.

## The intake model

```
registry.json  ──┬──▶  snippets/<id>.mcp.json   (how to wire it)
   (truth)        ├──▶  servers/<id>.md           (what it is / tools)
                  └──▶  README.md catalog row     (discoverability)
```

Every server is described once in `registry.json`; everything else points back to it.

## Steps

1. **Gather the facts from the source repo** — don't guess. You need: how it's launched
   (binary / `npx` / `docker` / hosted URL), the transport, auth requirements, and the
   tool list/prefix. For forks, read the upstream README/`package.json`.

2. **Add an entry to [`registry.json`](registry.json)** conforming to
   [`registry.schema.json`](registry.schema.json). Bump `version` (semver) and set
   `updated`. Pick the right classification:

   | Field | Meaning | Examples |
   |---|---|---|
   | `kind: local` | FlexNetOS-built binary on `PATH` | meta-mcp, weave |
   | `kind: external` | third-party server run locally | n8n-mcp (`npx`) |
   | `kind: remote` | hosted connector over the network | claude.ai connectors |
   | `runner` | how it starts | `binary` / `npx` / `docker` / `http` |
   | `transport` | MCP transport | `stdio` (needs `command`) / `http` / `sse` (needs `url`) |
   | `auth` | strictest auth needed to use it at all | `none` / `oauth` / `api-key` |

   Use `requiresApi: true` + `env` placeholders when only *some* tools need credentials
   (e.g. n8n-mcp's management tools). Never commit real secrets — use placeholders like
   `<your-api-key>`.

3. **Add a snippet** at `snippets/<id>.mcp.json` — a minimal, ready-to-merge
   `mcpServers` fragment. Put guidance and any "delete these vars for X" notes in a
   leading `_comment` field (JSON has no comments). Start from
   [`templates/server.template.mcp.json`](templates/server.template.mcp.json).

4. **Add a doc** at `servers/<id>.md` — start from
   [`templates/server.template.md`](templates/server.template.md). Cover: what it does,
   install/run, wire-up, and the tool list. Link upstream for forks.

5. **Add a README catalog row** in the table in [`README.md`](README.md), matching the
   entry's `id`, kind, transport, tools, snippet, and doc.

6. **Validate** before committing:

   ```bash
   python3 scripts/validate.py
   ```

   This checks every entry against the schema rules, that referenced `doc`/`snippet`
   files exist, that snippets are valid JSON, that ids are unique, and that the README
   table has a row per server.

7. **Open a PR** with the change. CI runs the validator.

## Conventions

- **`id`** is kebab-case, stable, and unique. It names the snippet (`snippets/<id>.mcp.json`)
  and is the row key in the README. Don't rename it later — other docs may reference it.
- **One server per entry.** A server that exposes two tiers of tools (like n8n-mcp) is
  still one entry; describe the tiers in `summary`/doc.
- **Status** reflects readiness: `stable` / `beta` / `experimental` / `deprecated`.
- **Forks** record both the FlexNetOS `repo` and the upstream source (in `notes` and the
  doc).
