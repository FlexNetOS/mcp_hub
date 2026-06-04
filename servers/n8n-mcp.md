# n8n-mcp

MCP server for building and managing [n8n](https://n8n.io) workflows from an AI agent —
node documentation, workflow validation, and (with an API key) full workflow/execution
management against a live n8n instance.

| | |
|---|---|
| **Repo** | [`FlexNetOS/n8n-mcp`](https://github.com/FlexNetOS/n8n-mcp) (fork of [`czlonkowski/n8n-mcp`](https://github.com/czlonkowski/n8n-mcp)) |
| **Kind** | external (third-party, run locally) |
| **Runner** | `npx` (or Docker) |
| **Transport** | stdio |
| **Language** | TypeScript / Node.js |
| **Version** | 2.56.0 |
| **License** | MIT |
| **Auth** | API key — required only for the management tools |
| **Status** | stable |
| **Workspace member** | no |

## What it does

Two tiers of tools:

- **Core (7, no credentials):** node documentation, full-text node search, node/workflow
  validation, and template search — everything needed to *author* a workflow JSON.
- **Management (13, requires API config):** create/update/delete/list workflows, run and
  inspect executions, manage credentials, autofix, version history, audit, and health
  checks against a real n8n instance.

## Install & run

Requires Node.js (for `npx`). No install step — `npx` fetches the published package:

```bash
npx n8n-mcp        # stdio server
```

Docker alternative: `ghcr.io/czlonkowski/n8n-mcp`. Self-hosting options (npx, Docker,
Railway, local) are in the upstream [Self-Hosting Guide](https://github.com/czlonkowski/n8n-mcp/blob/main/docs/SELF_HOSTING.md).

## Wire it up

Drop-in: [`snippets/n8n-mcp.mcp.json`](../snippets/n8n-mcp.mcp.json)

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "https://your-n8n-instance.com",
        "N8N_API_KEY": "<your-n8n-api-key>"
      }
    }
  }
}
```

For **docs-only** use, drop `N8N_API_URL` / `N8N_API_KEY` — the 7 core tools still work.
To enable the management tools, point them at your n8n instance and a valid API key.

Or via CLI:

```bash
claude mcp add n8n-mcp --scope user --env N8N_API_URL=https://your-n8n-instance.com --env N8N_API_KEY=<key> -- npx n8n-mcp
```

## Tools

**Core (7):** `tools_documentation`, `search_nodes`, `get_node`, `validate_node`,
`validate_workflow`, `search_templates`, `get_template`

**Management (13, requires `N8N_API_URL` + `N8N_API_KEY`):** `n8n_create_workflow`,
`n8n_get_workflow`, `n8n_update_full_workflow`, `n8n_update_partial_workflow`,
`n8n_delete_workflow`, `n8n_list_workflows`, `n8n_validate_workflow`,
`n8n_autofix_workflow`, `n8n_workflow_versions`, `n8n_deploy_template`,
`n8n_test_workflow`, `n8n_executions`, `n8n_manage_credentials`

Plus system tools `n8n_health_check` and `n8n_audit_instance`. Start with
`tools_documentation` — it self-documents the rest. See the upstream
[README](https://github.com/czlonkowski/n8n-mcp) for full reference.

## Notes

- This is a **fork** in the FlexNetOS org; tool names/counts track upstream as of v2.56.0.
- Unlike `meta-mcp` and `weave`, n8n-mcp is **not** a meta workspace member — it's an
  external server cataloged here for discoverability and one-paste wiring.
- It relates to the workspace `n8n` repo (the automation platform itself) but is a
  separate tool: `n8n-mcp` is the *agent interface*, `n8n` is the *engine*.
