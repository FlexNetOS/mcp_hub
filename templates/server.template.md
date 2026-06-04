# <display-name>

One-sentence description of what the server does and who it's for.

| | |
|---|---|
| **Repo** | [`owner/repo`](https://github.com/owner/repo) (note upstream if a fork) |
| **Kind** | local / external / remote |
| **Runner** | binary / npx / docker / http |
| **Transport** | stdio / http / sse |
| **Language** | … |
| **Auth** | none / oauth / api-key |
| **Status** | stable / beta / experimental / deprecated |
| **Workspace member** | yes (`<dir>`) / no |

## What it does

A short paragraph. If the server has tool tiers (e.g. some tools need credentials), say
so here.

## Install & run

How to obtain and start it (build command, `npx`, Docker image, or "hosted — no install").

## Wire it up

Drop-in: [`snippets/<id>.mcp.json`](../snippets/<id>.mcp.json)

```json
{
  "mcpServers": {
    "<id>": { "command": "…", "args": [] }
  }
}
```

Or via CLI:

```bash
claude mcp add <id> --scope user -- <command> <args>
```

## Tools

List the tools (or tool prefix + count). For large/forked servers, link upstream for the
full reference.

## Notes

Anything non-obvious: fork provenance, credential scope, relationship to other repos.
