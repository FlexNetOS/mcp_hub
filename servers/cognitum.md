# cognitum / cognitum-seed

Two SSE surfaces for the Cognitum platform: the **cloud** control plane and the **local
Seed appliance**. Both are cataloged as separate registry entries but share this doc and
the [`cognitum.mcp.json`](../snippets/cognitum.mcp.json) snippet.

| | cognitum | cognitum-seed |
|---|---|---|
| **Kind** | remote | remote |
| **Runner** | `http` | `http` |
| **URL** | `https://cognitum.one/mcpSse` | `https://cognitum.local:8443/mcp` |
| **Transport** | sse | sse |
| **Auth** | api-key (`${COGNITUM_API_KEY}`) | api-key (`${COGNITUM_SEED_TOKEN}`) |
| **Status** | beta | beta |

## What they do

- **cognitum** — cloud control plane (`api.cognitum.one`): 7 cloud tools (catalog, orders,
  witness chain, etc.). Read access is open; write operations require an API key.
- **cognitum-seed** — the local Seed appliance: 114 on-device tools. Requires a paired
  bearer token; falls back to the USB-gadget endpoint `http://169.254.42.1/mcp` (link-local
  IPv4, physical-cable trust). The Seed activates over link-local + mDNS, not DHCP.

## Wire it up

Drop-in: [`snippets/cognitum.mcp.json`](../snippets/cognitum.mcp.json)

```json
{
  "mcpServers": {
    "cognitum": {
      "type": "sse",
      "url": "https://cognitum.one/mcpSse",
      "env": { "COGNITUM_API_KEY": "${COGNITUM_API_KEY}" }
    },
    "cognitum-seed": {
      "type": "sse",
      "url": "https://cognitum.local:8443/mcp",
      "env": { "COGNITUM_SEED_TOKEN": "${COGNITUM_SEED_TOKEN}" }
    }
  }
}
```

Use env-refs only — **never commit literal keys/tokens**.

## Tools

Cloud: catalog, orders, witness-chain, and related control-plane tools. Seed: the on-device
tool set (114) exposed by the paired appliance.
