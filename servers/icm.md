# icm

Infinite Context Memory — persistent, cross-session memory for agents. Recall prior
decisions, resolved errors, and user preferences before work; store durable memory when
something worth remembering happens. A FlexNetOS-built local binary.

| | |
|---|---|
| **Repo** | [`FlexNetOS/icm`](https://github.com/FlexNetOS/icm) |
| **Workspace member** | `icm/` |
| **Binary** | `icm` |
| **Runner** | binary |
| **Command** | `icm serve` |
| **Transport** | stdio |
| **Auth** | none |
| **Tool prefix** | `icm_` |
| **Status** | stable |

## What it does

Topic-organized memories with importance/decay, recall (search) and store (persist),
in-place updates, topic hygiene, plus memoirs, feedback capture, and transcripts. Used
proactively: recall relevant context at task start; store on the trigger events (decision
made, error resolved, significant task done, preference learned).

## Install

Build from the workspace and ensure `icm` is on `PATH`:

```bash
cargo build --release -p icm
```

## Wire it up

Drop-in: [`snippets/icm.mcp.json`](../snippets/icm.mcp.json)

```json
{
  "mcpServers": {
    "icm": { "command": "icm", "args": ["serve"] }
  }
}
```

Or via CLI (per-user, all projects):

```bash
claude mcp add icm --scope user -- icm serve
```

## Tools

Memory: `icm_memory_recall`, `icm_memory_store`, `icm_memory_update`, `icm_memory_forget`,
`icm_memory_health`, `icm_memory_list_topics`, `icm_memory_stats`, and consolidation/embed
helpers. Plus memoir (`icm_memoir_*`), feedback (`icm_feedback_*`), transcript
(`icm_transcript_*`), `icm_learn`, and `icm_wake_up`. See the `icm` repo for the full set.
