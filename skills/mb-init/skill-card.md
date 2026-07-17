# mb-init — Skill Card

| Field | Value |
|-------|-------|
| **Name** | mb-init |
| **Version** | v6.12 |
| **One-liner** | Initialize a memory bank for a new or existing project. |

## Trigger
- Starting a new project that needs task tracking
- Existing project lacks memory-bank documentation
- "Set up memory bank for this project"

## Key Commands

```bash
# Create directory structure
cd <project-root>
mkdir -p memory-bank/{tasks,sessions,edits/$(date +%Y-%m-%d),implementation-details}

# Create core files (tasks.md, session_cache.md, activeContext.md, edit_history.md)
# → See SKILL.md for full templates

# Optional: create first task
cat > memory-bank/tasks/T1.md << 'EOF'
# T1: [Title]
*Created: YYYY-MM-DD HH:MM:SS TZ*
**Status**: 🔄 **IN PROGRESS**
EOF

# Commit
git add memory-bank/
git commit -m "(docs)INIT: Initialize memory bank — v6.12 protocol"
```

## Dependencies
- Project root directory known
- Current time and timezone
- Decision: text-based or DB-native workflow

## Quick Example

```bash
cd /path/to/project
mkdir -p memory-bank/{tasks,sessions,edits/$(date +%Y-%m-%d),implementation-details}
# Copy templates from SKILL.md, then commit
git add memory-bank/ && git commit -m "(docs)INIT: Memory bank v6.12"
```

> After init, use `mb-text-workflow` or `mb-db-workflow` for all updates.
