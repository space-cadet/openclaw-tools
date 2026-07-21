---
name: mulch
description: "Memory compaction and indexing. Use mulch prime at session start; mulch record before finishing. Captures learnings so expertise compounds across sessions."
metadata:
  openclaw:
    emoji: "🌱"
    install: ["npm install -g mulch-cli"]
  version: "1.0.0"
  origin: "ClawHub"
---

# Mulch Self Improver — Let your agents grow 🌱

Structured expertise that accumulates over time, lives in git, and works with any agent. Agents start each session from zero; the pattern discovered yesterday is forgotten today. This skill uses [Mulch](https://github.com/jayminwest/mulch): agents call `mulch record` to write learnings and `mulch query` to read them. Expertise compounds across sessions, domains, and teammates.

**Benefits:** Better and more consistent coding · Improved experience · Less hallucination (grounding in project expertise)

**When to use:** Command/tool fails, user corrects you, user wants a missing feature, your knowledge was wrong, or you found a better approach — record with Mulch and promote proven patterns to project memory.

## Installation

```bash
npm install -g mulch-cli
# or: npx mulch-cli <command>
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| Command/operation or API fails | `mulch record <domain> --type failure --description "..." --resolution "..."` |
| User corrects you / knowledge was wrong | `mulch record <domain> --type convention "..."` or `--type pattern --name "..." --description "..."` |
| Found better approach, best practice | `mulch record <domain> --type convention "..."` or `--type guide --name "..." --description "..."` |
| Architectural or tech decision | `mulch record <domain> --type decision --title "..." --rationale "..."` |
| Key file/endpoint to remember | `mulch record <domain> --type reference --name "..." --description "..."` |
| Session start (project has .mulch/) | Run `mulch prime` to load expertise into context |

## Setup

```bash
mulch init
# Quick: add all preset domains at once
mulch add api
mulch add database
mulch add testing
# add domains that match your areas: frontend, backend, infra, docs, config
```

## Record Types

| Type | Required | Use Case |
|------|----------|----------|
| `failure` | description, resolution | What went wrong and how to avoid it |
| `convention` | content | Short rules and best practices |
| `pattern` | name, description | Named patterns |
| `decision` | title, rationale | Architecture, tech choices |
| `reference` | name, description | Key files, endpoints, resources |
| `guide` | name, description | Step-by-step procedures |

## Workflow

1. **Session start:** If `.mulch/` exists, run `mulch prime`
2. **During work:** When something fails or you learn something, run `mulch record`
3. **Before finishing:** Review; record any remaining insights
4. **Promote:** When a pattern is proven, add to project memory files

## Promotion Targets

| Learning Type | Promote To |
|----------------|------------|
| Behavioral patterns | `SOUL.md` |
| Workflow improvements | `AGENTS.md` |
| Tool gotchas | `TOOLS.md` |
| Project facts, conventions | `CLAUDE.md` |

## Periodic Review

- **When:** Before major tasks, after features, weekly
- **Commands:** `mulch status`, `mulch ready --since 7d`, `mulch query --all`
- **Actions:** Promote high-value records; prune stale entries
