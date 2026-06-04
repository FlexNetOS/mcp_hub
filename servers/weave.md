# weave

Rust-native agent-to-agent session mesh with a native terminal injector. Lets
coding-agent sessions (Claude Code, etc.) message each other and pushes a live nudge
into a peer's tmux/zellij pane the moment a message arrives.

| | |
|---|---|
| **Repo** | [`FlexNetOS/weave`](https://github.com/FlexNetOS/weave) |
| **Workspace member** | `weave/` |
| **Binary** | `weave` |
| **Transport** | stdio (newline-delimited JSON-RPC 2.0) |
| **Protocol** | `2025-06-18` (also supports `2024-11-05`, `2025-03-26`) |
| **Auth** | none |
| **Tool prefix** | `weave_` |
| **Tools** | 11 |
| **Status** | stable |

## What it does

One static Rust binary — no Python, no daemon, no dependency on repowire. Sessions send
and read messages; when the recipient is a registered injectable peer, weave pushes a
live nudge into their pane. Degrades to hook-delivery-on-next-turn when no multiplexer is
present. libSQL backend.

## Install

Build from the workspace:

```bash
cargo build --release -p weave   # produces target/release/weave
```

Ensure `weave` is on `PATH`.

## Wire it up

Drop-in: [`snippets/weave.mcp.json`](../snippets/weave.mcp.json)

```json
{
  "mcpServers": {
    "weave": { "command": "weave", "args": ["mcp"] }
  }
}
```

Or via CLI (per-user, all projects):

```bash
claude mcp add weave --scope user -- weave mcp
```

To pin a session identity, append `--session <name>` to the args
(e.g. `"args": ["mcp", "--session", "desktop"]`). `weave setup` can also wire the MCP
server **and** lifecycle hooks in one step.

## Tools (11)

`weave_send`, `weave_inbox`, `weave_reply`, `weave_thread`, `weave_peers`,
`weave_sessions`, `weave_whoami`, `weave_history`, `weave_receipts`, `weave_clear`,
`weave_doctor`

See the `weave` repo `README.md`, `PRD.md`, and `docs/` for the full protocol and
injector design.
