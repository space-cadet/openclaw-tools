# mcp-client — Skill Card

| Field | Value |
|-------|-------|
| **Name** | mcp-client |
| **Version** | — |
| **One-liner** | Spawn and interact with MCP servers via JSON-RPC stdio. |

## Trigger
- User asks to use an MCP server (desktop-commander, playwright, memory, etc.)
- `openclaw mcp list` returns "unknown command"
- Native MCP tool calling unavailable in current runtime

## Key Commands

```bash
# Read a file via desktop-commander
node scripts/mcp-call.js desktop-commander read_file \
  '{"path":"/path/to/package.json","length":10}'

# Read memory graph
node scripts/mcp-call.js memory read_graph '{}'

# Search memory nodes
node scripts/mcp-call.js memory search_nodes '{"query":"physics"}'
```

## Dependencies
- Node.js
- MCP servers configured in `~/.openclaw/openclaw.json`
- `scripts/mcp-call.js`

## Quick Example

```bash
node scripts/mcp-call.js desktop-commander read_file \
  '{"path":"/home/cloudy/.openclaw/workspace/SOUL.md"}'
```

> Only spawn servers from trusted config. Kill processes after use to avoid zombies.
