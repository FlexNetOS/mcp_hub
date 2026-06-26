# context7

Up-to-date, version-specific library/framework documentation and code examples on demand.
Resolves a library name to an ID, then fetches current docs — so answers about SDKs, CLIs,
and APIs reflect recent releases instead of stale training data.

| | |
|---|---|
| **Repo** | [`upstash/context7`](https://github.com/upstash/context7) (MIT) |
| **Kind** | external (third-party npm package, unmodified) |
| **Runner** | `bunx` (see note below) |
| **Command** | `bunx -y @upstash/context7-mcp --api-key ${CONTEXT7_API_KEY}` |
| **Transport** | stdio |
| **Auth** | api-key |
| **Status** | stable |

## What it does

Two tools: `resolve-library-id` (name → Context7 library ID) and `query-docs` (ID + question
→ current documentation and snippets). Use it whenever working with a library, framework,
SDK, API, or CLI tool — even well-known ones — to avoid out-of-date answers.

> **Runner note:** the wiring uses `bunx`, not `npx`. The meta-managed JS runtime is Bun;
> the bundled `node`/`npx` is a standalone binary without the npm lib, so `npx` is
> non-functional in this environment. `bunx <pkg>` is the working, meta-native dlx runner.

## Wire it up

Drop-in: [`snippets/context7.mcp.json`](../snippets/context7.mcp.json)

```json
{
  "mcpServers": {
    "context7": {
      "command": "bunx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "${CONTEXT7_API_KEY}"]
    }
  }
}
```

Get a key at [context7.com](https://context7.com). **Never commit the literal key** — set it
via the `${CONTEXT7_API_KEY}` env-ref in committed config and provide the value in the
environment or a gitignored local settings file.

## Tools

`resolve-library-id`, `query-docs`.
