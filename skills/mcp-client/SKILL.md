---
name: mcp-client
description: |
  Spawn and interact with MCP (Model Context Protocol) servers via JSON-RPC stdio.
  Use when the user wants to call tools from MCP servers that are configured in
  OpenClaw config (~/.openclaw/openclaw.json or ~/.openclaw/config.yaml) but the
  runtime does not natively expose them. Covers stdio, SSE, and streamable-http
  transports. Use for: file operations via desktop-commander, browser automation
  via playwright-mcp, memory storage via server-memory, database queries via
  supabase-mcp, or any other MCP server the user has installed.
---

# MCP Client Skill

## Purpose

OpenClaw versions before native MCP client support (e.g. 2026.3.13) do not
expose configured MCP servers as agent tools. This skill bridges that gap by
spawning MCP server processes directly and speaking JSON-RPC over stdio.

## When to use

- User asks to use an MCP server (desktop-commander, playwright, memory, etc.)
- `openclaw mcp list` returns "unknown command" or config path not found
- Native MCP tool calling is unavailable in the current runtime

## When NOT to use

- Native MCP support is already working (`openclaw mcp list` shows servers)
- The task can be done with existing agent tools (exec, read, edit, browser)

## Workflow

### 1. Discover configured servers

Read `~/.openclaw/openclaw.json` (JSON) or `~/.openclaw/config.yaml` (YAML)
and extract `mcp.servers`:

```json
{
  "mcp": {
    "servers": {
      "desktop-commander": {
        "command": "node",
        "args": ["/path/to/mcps/desktop-commander/dist/index.js"]
      },
      "memory": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-memory"],
        "env": { "MEMORY_FILE_PATH": "/path/to/.memory/memory.json" }
      }
    }
  }
}
```

### 2. Spawn the server process

Use `scripts/mcp-call.js` (see below) or inline Node.js to:

1. Spawn the process with `command` + `args`
2. Set any `env` variables
3. Send `initialize` request (JSON-RPC)
4. Send `tools/list` to discover available tools
5. Send `tools/call` to invoke the desired tool
6. Parse the result and return to user
7. Kill the process

### 3. Handle responses

MCP servers return results as JSON-RPC responses. Tool results are in:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [{"type": "text", "text": "..."}],
    "isError": false
  }
}
```

Extract `result.content[0].text` for text output, or handle `isError: true`.

## Helper Script

Use `scripts/mcp-call.js` for reliable MCP communication:

```bash
node scripts/mcp-call.js <server-name> <tool-name> '<json-args>'
```

Examples:

```bash
# Read a file via desktop-commander
node scripts/mcp-call.js desktop-commander read_file '{"path":"/path/to/project/package.json","length":10}'

# Read memory graph
node scripts/mcp-call.js memory read_graph '{}'

# Search memory nodes
node scripts/mcp-call.js memory search_nodes '{"query":"physics"}'
```

The script:
- Reads server config from `~/.openclaw/openclaw.json`
- Spawns the process, sends initialize + tools/call
- Outputs clean result text (or JSON if `--json`)
- Exits with code 1 on error

### Memory MCP Server Tools

The `@modelcontextprotocol/server-memory` exposes a knowledge graph:

| Tool | Purpose |
|------|---------|
| `create_entities` | Add entities with type + observations |
| `create_relations` | Link entities with relation types |
| `add_observations` | Append observations to existing entities |
| `read_graph` | Dump the full graph |
| `search_nodes` | Search entities by name/observation |
| `open_nodes` | Get specific entities by name |
| `delete_entities` | Remove entities |
| `delete_observations` | Remove specific observations |
| `delete_relations` | Remove relations |

## Security Notes

- Only spawn servers from trusted config (user-owned `~/.openclaw/`)
- Respect `allowedDirectories` in desktop-commander — it will reject paths
- Do not log or echo MCP server env vars (may contain tokens)
- Kill processes after use to avoid zombie MCP servers

## Current Limitations

- Stdio transport only (no SSE/streamable-http support in workaround)
- One-shot calls (no persistent MCP connection across agent turns)
- Process spawn overhead per call (~1-2s for feature flag fetch)
- Tool schemas are discovered dynamically, not cached

## Future

When OpenClaw natively supports MCP clients (`openclaw mcp list` works),
this skill becomes obsolete. Transition path: remove skill, rely on native
`bundle-mcp` tool profile.
