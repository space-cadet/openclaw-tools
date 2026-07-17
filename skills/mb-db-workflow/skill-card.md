# mb-db-workflow — Skill Card

| Field | Value |
|-------|-------|
| **Name** | mb-db-workflow |
| **Version** | v6.12 |
| **One-liner** | Record and read Memory Bank state via mb-cli (SQLite backend). |

## Trigger
- "db workflow", "record session work", "regenerate memory bank"
- "update tasks" in a project with `memory-bank/database/`

## Key Commands

```bash
# Read state
mb task list
mb task show T25
mb db query "SELECT * FROM task_items" --json
mb session cache

# Record work + regenerate markdown
mb workflow --record --regenerate --task T3 \
  --description "Implemented feature X" \
  --files "Created:src/feature.js,Modified:src/app.js" \
  --status completed

# Task & session management
mb task create "Build quantum simulator" --id T26 --priority high
mb session start --focus T26 --period afternoon
mb session complete --notes "Finished core logic"

# Sync templates
mb db sync --all
```

## Dependencies
- `mb` CLI on PATH
- `memory-bank/database/memory_bank.db`

## Quick Example

```bash
mb workflow --task T1 --description "Setup project" \
  --files "Created:package.json,Modified:README.md" \
  --status in_progress --period morning
```

> Never hand-edit generated markdown (`tasks.md`, `edit_history.md`) — they are overwritten on regeneration.
