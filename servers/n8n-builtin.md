# n8n-builtin

n8n's **own** built-in MCP server (Settings → MCP), which exposes your workflows as tools
over authenticated HTTP. Distinct from [`n8n-mcp`](n8n-mcp.md), the external
node-documentation/validation tool.

| | |
|---|---|
| **Source** | n8n built-in MCP feature (self-hosted n8n) |
| **Kind** | remote (hosted by your local n8n) |
| **Runner** | `http` |
| **URL** | `http://localhost:5678/mcp-server/http` |
| **Transport** | http |
| **Auth** | api-key (Bearer, audience `mcp-server-api`) |
| **Status** | beta |

## What it does

Turns the workflows in your n8n instance into callable MCP tools. Requires n8n running with
MCP access enabled. Pairs with `n8n-mcp`: that one teaches an agent *how to build* n8n
nodes/workflows; this one *runs* the workflows you've already built.

## Wire it up

Drop-in: [`snippets/n8n-builtin.mcp.json`](../snippets/n8n-builtin.mcp.json)

```json
{
  "mcpServers": {
    "n8n-builtin": {
      "type": "http",
      "url": "http://localhost:5678/mcp-server/http",
      "headers": { "Authorization": "Bearer ${N8N_MCP_SERVER_TOKEN}" }
    }
  }
}
```

The token must be an **MCP-server-audience** key (`aud=mcp-server-api`), NOT a public-API
key. Carry it via `${N8N_MCP_SERVER_TOKEN}` from a gitignored `settings.local.json` —
**never commit it** (these repos are public).

## Tools

One MCP tool per exposed workflow (named by the workflow), as configured in n8n's MCP
settings.
