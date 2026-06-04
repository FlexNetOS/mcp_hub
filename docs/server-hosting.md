# Server hosting policy

How an MCP server is physically hosted in the FlexNetOS workspace — decided once here so
the catalog stays coherent as it grows.

## The problem

MCP servers in the catalog have different **citizenship**. Treating them uniformly (e.g.
making every server a top-level meta peer) dilutes "what the meta workspace *is*" and
mixes first-party components with third-party dependencies. n8n-mcp surfaced this: it's a
forked external tool, not a component of meta — it shouldn't sit beside `meta_cli` and
`weave` in the root `.meta.yaml`.

## The rule

Each registry entry declares a `hosting` value. It follows from what the server *is*:

| `hosting` | What it is | Where the code lives | Examples |
|---|---|---|---|
| `peer` | First-party component of the meta system, built in-workspace | top-level `.meta.yaml` peer | meta-mcp, weave |
| `mcp_hub-child` | An external server FlexNetOS **forks and maintains** | nested under mcp_hub (see below) | n8n-mcp |
| `registry-only` | A server we **don't** host: an unmodified third-party server we just point at, or a hosted remote connector with no code | nowhere — snippet + doc only | claude.ai connectors |

Decision flow for a new server:

```
Is it part of the meta system itself?        ── yes ─▶ peer
        │ no
Do we fork & maintain its source?            ── yes ─▶ mcp_hub-child
        │ no
                                                  └──▶ registry-only
```

## How `mcp_hub-child` works (nested meta)

mcp_hub is a **nested meta repo**. It carries its own `.meta.yaml` listing the external
servers it hosts, and the parent workspace marks it `meta: true`:

```yaml
# root .meta.yaml
mcp_hub:
  repo: git@github.com:FlexNetOS/mcp_hub.git
  tags: [hub, mcp]
  meta: true            # ← recurse into mcp_hub/.meta.yaml

# mcp_hub/.meta.yaml
projects:
  n8n-mcp:
    repo: git@github.com:FlexNetOS/n8n-mcp.git
    tags: [mcp, external]
```

Consequences:

- `meta git update -r` clones mcp_hub **and** its hosted servers (into `mcp_hub/<id>/`).
- `meta exec -r -- <cmd>` and `meta project list -r` span both levels.
- Hosted server clones are independent repos, ignored by mcp_hub's `.gitignore` — they
  are **not** part of mcp_hub's own history (no submodule, no vendored code).
- The registry entry records `subPath` (the dir under mcp_hub) so tools can locate it.

### Why nested-meta and not git submodules

Both give a "child repo under mcp_hub" identity. Nested-meta was chosen because it is
**native to this workspace** — the same `meta` commands that drive every other repo also
drive these, with no submodule friction (detached HEADs, manual `submodule update`, a
mechanism the `meta` CLI doesn't manage). Trade-off: nested-meta tracks a branch rather
than pinning an exact commit. If a hosted fork needs a pinned, reviewed commit for
provenance, record it in the registry entry (add a `pin` field) — the clone still comes
from `.meta.yaml`.

## Lifecycle of an `mcp_hub-child`

1. **Fork** the upstream server into `FlexNetOS/<id>`.
2. **Host it**: add it to `mcp_hub/.meta.yaml` (`projects:`) and to `mcp_hub/.gitignore`
   (`/<id>/`).
3. **Register it**: add the registry entry with `kind: external`, `hosting: mcp_hub-child`,
   `subPath: <id>`, plus snippet + doc (see [CONTRIBUTING.md](../CONTRIBUTING.md)).
4. **Materialize**: `meta git update -r` clones it into `mcp_hub/<id>/`.
5. **Update from upstream**: pull upstream into the fork; `meta git -r` keeps clones current.
6. **Remove**: delete from `.meta.yaml`, `.gitignore`, and the registry; optionally archive
   the fork.

## What did *not* change

- First-party servers stay top-level peers. This policy does not move meta-mcp or weave.
- registry.json remains the single source of truth; `hosting` is just a new field on it,
  enforced by `scripts/validate.py`.
