# playwright (browser extension)

Browser automation against the user's **own running Chrome/Edge** via the "Playwright
MCP Bridge" extension. In `--extension` mode the server drives a real, already-open,
already-authenticated tab — navigate, click, type, snapshot the accessibility tree, read
console/network — instead of launching a separate headless browser.

| | |
|---|---|
| **Repo** | [`microsoft/playwright-mcp`](https://github.com/microsoft/playwright-mcp) (Apache-2.0) |
| **Kind** | external (third-party npm package, unmodified) |
| **Runner** | `bunx` (see note below) |
| **Command** | `bunx @playwright/mcp@latest --extension` |
| **Transport** | stdio |
| **Auth** | none (optional per-profile extension token) |
| **Tool prefix** | `mcp__playwright__` |
| **Status** | stable |

## What it does

`--extension` connects the MCP server to a browser instance the user already has open
(Chrome or Edge only), through the **Playwright MCP Bridge** browser extension. This lets
an agent operate inside the user's real session — logged-in tabs, existing cookies — with
no separate browser to manage. Without `--extension`, `@playwright/mcp` launches its own
headless Playwright browser instead.

## Prerequisites

1. **Install the "Playwright MCP Bridge" extension** in Chrome/Edge (see the
   [extension docs](https://github.com/microsoft/playwright/tree/main/packages/extension#readme)).
2. **Copy the connection token.** Open the extension's status page and copy the
   `PLAYWRIGHT_MCP_EXTENSION_TOKEN` value (unique to your browser profile). Setting it in
   the server's `env` enables automatic connection; without it you must approve each
   connection through a dialog in the browser.

> **Runner note:** the wiring uses `bunx`, not `npx`. The meta-managed JS runtime is Bun;
> the bundled `node`/`npx` is a standalone binary without the npm lib, so `npx` is
> non-functional in this environment. `bunx <pkg>` is the working, meta-native dlx runner.

## Wire it up

Drop-in: [`snippets/playwright.mcp.json`](../snippets/playwright.mcp.json)

```json
{
  "mcpServers": {
    "playwright": {
      "command": "bunx",
      "args": ["@playwright/mcp@latest", "--extension"],
      "env": {
        "PLAYWRIGHT_MCP_EXTENSION_TOKEN": "${PLAYWRIGHT_MCP_EXTENSION_TOKEN}"
      }
    }
  }
}
```

**Never commit the literal token.** Use the `${PLAYWRIGHT_MCP_EXTENSION_TOKEN}` env-ref in
committed config and set the real value in the environment or a gitignored local settings
file (e.g. `.claude/settings.local.json` `env`, or your user `~/.claude.json`).

Or via CLI (per-user, all projects):

```bash
PLAYWRIGHT_MCP_EXTENSION_TOKEN=<token> \
  claude mcp add playwright --scope user -- bunx @playwright/mcp@latest --extension
```

## Tools

Provided by `@playwright/mcp` under the `mcp__playwright__` prefix — browser navigation,
clicking/typing/forms, accessibility-tree snapshots, screenshots, tab management, and
console/network inspection. Run `bunx @playwright/mcp@latest --help` for the full option
set (headless vs extension, allowed-origins, capabilities, etc.).
