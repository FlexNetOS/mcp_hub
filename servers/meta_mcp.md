# meta-mcp

MCP server that exposes multi-repo operations for the `meta` workspace to AI agents.

| | |
|---|---|
| **Repo** | [`FlexNetOS/meta_mcp`](https://github.com/FlexNetOS/meta_mcp) |
| **Workspace member** | `meta_mcp/` |
| **Binary** | `meta-mcp` |
| **Transport** | stdio (newline-delimited JSON-RPC 2.0) |
| **Protocol** | `2024-11-05` |
| **Auth** | none |
| **Tool prefix** | `meta_` |
| **Tools** | 29 |
| **Status** | stable |

## What it does

`meta-mcp` is the primary MCP integration for the meta workspace. It shells out to the
`meta` CLI (and to `git`/build tools) and returns structured results, giving an agent
one interface over all repos in `.meta.yaml`.

## Install

The binary ships in the meta release package; or build from the workspace:

```bash
cargo build --release -p meta-mcp   # produces target/release/meta-mcp
```

Ensure `meta-mcp` (and the `meta` CLI it calls) are on `PATH`.

## Wire it up

Drop-in: [`snippets/meta.mcp.json`](../snippets/meta.mcp.json)

```json
{
  "mcpServers": {
    "meta": { "command": "meta-mcp", "args": [] }
  }
}
```

Or via CLI:

```bash
claude mcp add meta --scope user -- meta-mcp
```

`meta-mcp` locates the workspace by walking up from the current directory to find the
`.meta`/`.meta.yaml` config, so run agent sessions from inside the workspace.

## Tools (29)

**Core (4):** `meta_list_projects`, `meta_exec`, `meta_get_config`, `meta_get_project_path`

**Git (10):** `meta_git_status`, `meta_git_pull`, `meta_git_push`, `meta_git_fetch`,
`meta_git_diff`, `meta_git_branch`, `meta_git_add`, `meta_git_commit`,
`meta_git_checkout`, `meta_git_multi_commit`

**Build/test (4):** `meta_detect_build_systems`, `meta_run_tests`, `meta_build`, `meta_clean`

**Discovery (3):** `meta_search_code`, `meta_get_file_tree`, `meta_list_plugins`

**Workspace analysis (8):** `meta_query_repos`, `meta_workspace_state`,
`meta_analyze_impact`, `meta_execution_order`, `meta_snapshot_create`,
`meta_snapshot_list`, `meta_snapshot_restore`, `meta_batch_execute`

Full parameter reference: `meta_mcp` repo and `meta/docs/mcp_server.md`.
