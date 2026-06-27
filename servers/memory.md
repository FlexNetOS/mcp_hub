# memory

A persistent knowledge-graph the agent reads and writes across a session — entities,
relations, and observations that survive between turns.

| | |
|---|---|
| **Repo** | [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) (`src/memory`, MIT) |
| **Kind** | external (official reference server) |
| **Runner** | `bunx` (see note below) |
| **Command** | `bunx -y @modelcontextprotocol/server-memory` |
| **Transport** | stdio |
| **Auth** | none |
| **Status** | stable |

## What it does

Stores a knowledge graph the model can query and update: create entities, link them with
relations, and attach observations. Useful as a scratch long-term memory within a project.

> **Runner note:** uses `bunx`, not `npx` — the meta-managed JS runtime is Bun and the
> bundled `node`/`npx` is non-functional in this workspace. `bunx <pkg>` is the working
> meta-native dlx runner.

> **Meta variant:** envctl wires a meta-native bash wrapper
> (`envctl/assets/scripts/envctl-mcp-memory-server`) for its own store location. The `bunx`
> form here is the portable canonical.

## Wire it up

Drop-in: [`snippets/memory.mcp.json`](../snippets/memory.mcp.json)

```json
{
  "mcpServers": {
    "memory": {
      "command": "bunx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

Set `MEMORY_FILE_PATH` in `env` to relocate the persisted graph.

## Tools

`create_entities`, `create_relations`, `add_observations`, `read_graph`, `search_nodes`,
and related graph-mutation tools.
