# vox

Text-to-speech for spoken agent feedback — and voice input via `vox_hear`. Speak short
summaries after significant work, or hold a voice conversation. A FlexNetOS-built local
binary.

| | |
|---|---|
| **Repo** | [`FlexNetOS/vox`](https://github.com/FlexNetOS/vox) |
| **Workspace member** | `vox/` |
| **Binary** | `vox` |
| **Runner** | binary |
| **Command** | `vox serve` |
| **Transport** | stdio |
| **Auth** | none |
| **Tool prefix** | `vox_` |
| **Status** | stable |

## What it does

`vox_speak` renders text to speech (keep summaries short, English by default); `vox_hear`
listens for voice input so the agent can run a listen→think→speak loop. Manage voices,
sound packs, and voice clones, and configure the backend.

## Install

Build from the workspace and ensure `vox` is on `PATH`:

```bash
cargo build --release -p vox
```

## Wire it up

Drop-in: [`snippets/vox.mcp.json`](../snippets/vox.mcp.json)

```json
{
  "mcpServers": {
    "vox": { "command": "vox", "args": ["serve"] }
  }
}
```

Or via CLI (per-user, all projects):

```bash
claude mcp add vox --scope user -- vox serve
```

## Tools

`vox_speak`, `vox_hear`, `vox_list_voices`, `vox_config_show`, `vox_config_set`,
`vox_stats`, plus pack management (`vox_pack_*`) and clones (`vox_clone_*`). See the `vox`
repo for the full set.
