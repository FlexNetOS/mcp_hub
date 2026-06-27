# exa

Web search and page-content retrieval via Exa's hosted MCP endpoint — nothing runs locally.

| | |
|---|---|
| **Repo** | [`exa-labs/exa-mcp-server`](https://github.com/exa-labs/exa-mcp-server) (hosted) |
| **Kind** | remote (hosted HTTP endpoint) |
| **Runner** | `http` |
| **URL** | `https://mcp.exa.ai/mcp` |
| **Transport** | http |
| **Auth** | none for core search; API key for more |
| **Status** | stable |

## What it does

Live web search plus full-content retrieval, so the agent can ground answers in current
pages. The core search works against the hosted endpoint with no credentials; an Exa API
key raises rate limits and unlocks additional tools.

## Wire it up

Drop-in: [`snippets/exa.mcp.json`](../snippets/exa.mcp.json)

```json
{
  "mcpServers": {
    "exa": {
      "type": "http",
      "url": "https://mcp.exa.ai/mcp"
    }
  }
}
```

For authenticated use, append the key as a query param
(`https://mcp.exa.ai/mcp?exaApiKey=${EXA_API_KEY}`) via an env-ref — **never commit the
literal key**. Get a key at [exa.ai](https://exa.ai).

## Tools

`web_search` and content-retrieval tools (the exact set is defined by the hosted endpoint).
