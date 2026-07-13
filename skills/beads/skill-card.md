# beads — Skill Card

| Field | Value |
|-------|-------|
| **Name** | beads |
| **Version** | — |
| **One-liner** | Dolt-powered issue tracker for AI coding workflows. |

## Trigger
- "add a todo", "remember to fix", "what's pending"
- User mentions a bug, idea, or feature
- Any task tracking request that should persist across sessions

## Key Commands

```bash
# Add a task
bd create "Title" -p 1 -t task -l project-label

# List ready (unblocked) work
bd ready

# Show all issues
bd list

# Claim / close a task
bd update <id> --claim
bd close <id> --reason "Done"

# Store a persistent insight
bd remember "insight text"

# Get workflow context
bd prime
```

## Dependencies
- `bd` CLI (beads) installed
- Workspace `.beads/` database initialized with `--stealth`

## Quick Example

```bash
cd /path/to/workspace && bd create "Fix login bug" -p 0 -t bug -l my-project,auto -d "OAuth redirect fails on mobile"
```

> Add the `auto` label for executor-eligible tasks (safe to run without human review).
