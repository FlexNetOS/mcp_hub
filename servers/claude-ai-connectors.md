# claude.ai Connectors

Remote, OAuth-backed MCP servers provided through the **claude.ai Connectors directory**.
Unlike the local FlexNetOS servers (`meta-mcp`, `weave`), these are not binaries on your
machine — they are hosted endpoints you authorize once via OAuth.

| | |
|---|---|
| **Kind** | remote |
| **Transport** | HTTP (SSE/streamable) |
| **Auth** | interactive OAuth on first use |
| **Provisioned by** | claude.ai |

> ⚠️ **Headless caveat:** because auth is interactive OAuth, these connectors may be
> unavailable in headless / cron / CI runs. Treat them as interactive-session tools.

## Catalog

| Connector | Tool prefix | Purpose |
|---|---|---|
| Cloudflare Developer Platform | `mcp__claude_ai_Cloudflare_Developer_Platform__` | Workers, KV, R2, and other Cloudflare developer-platform operations |
| Figma | `mcp__claude_ai_Figma__` | Read designs into code and write designs into Figma (Code Connect, screenshots, diagrams, design systems) |
| Gmail | `mcp__claude_ai_Gmail__` | Threads, drafts, labels |
| Google Calendar | `mcp__claude_ai_Google_Calendar__` | Events, availability, scheduling |
| Google Drive | `mcp__claude_ai_Google_Drive__` | File search, read, management |
| Hugging Face | `mcp__claude_ai_Hugging_Face__` | Models, datasets, papers, spaces, docs |
| Microsoft 365 | `mcp__claude_ai_Microsoft_365__` | Outlook mail/calendar, Teams chat, SharePoint search |
| Notion | `mcp__claude_ai_Notion__` | Pages, databases, comments, search |

## Wire it up

**Preferred — claude.ai Connectors directory:** open the claude.ai app → *Settings →
Connectors*, enable the connector, and complete the OAuth flow. This is the source of
truth for the endpoint URL and keeps auth managed for you.

**Manual (`.mcp.json` / `claude mcp add`):** remote servers use the `http` transport.
Template in [`snippets/claude-ai.mcp.json`](../snippets/claude-ai.mcp.json):

```json
{
  "mcpServers": {
    "Notion": { "type": "http", "url": "https://<from-connector-page>/notion/mcp" }
  }
}
```

```bash
claude mcp add --transport http Notion "https://<from-connector-page>/notion/mcp"
```

The URLs in the snippet are **placeholders** — copy the real endpoint from each
connector's page in the claude.ai Connectors directory. Do not invent endpoints.
