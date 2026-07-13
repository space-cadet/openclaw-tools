# graph-memory — Skill Card

| Field | Value |
|-------|-------|
| **Name** | graph-memory |
| **Version** | 1.0.0 |
| **One-liner** | Query the agent's knowledge graph for entities, relationships, and statistics. |

## Trigger
- "What do you know about X?"
- "How is X connected to Y?"
- Need context about past work, people, projects

## Key Commands (JS functions)

```js
// Search entities
graph_search("chimera", { type: "project", deep: true })

// Graph statistics
graph_stats()

// Traverse relationships
graph_related("deepak", 2)
```

## Dependencies
- `better-sqlite3` (npm)
- Graph DB at `~/.openclaw/workspace/.openclaw_memory/graph.db`

## Quick Example

```js
graph_search("quantum", { type: "project", deep: true, limit: 10 })
```

> Returns matching entities, types, mention counts, and neighbor lists.
