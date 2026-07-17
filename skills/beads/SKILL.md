---
name: beads
user-invocable: true
description: "Track tasks and ideas with beads (bd) - Dolt-powered issue tracker for AI coding workflows."
---

# Beads Task Tracker

Use beads to quickly capture tasks, ideas, and bugs without losing context across sessions.

## When to Use

- User says "add a todo" or "remember to fix"
- User wants to see open tasks or what's ready to work on
- User mentions a bug, idea, or feature during conversation
- Any task tracking request that should persist across sessions

## Project Labels

When creating tasks, always include a **project label** using `-l <project>`.

Project labels map to directories via `.beads/project-dirs.json`:
- `my-project` → `code/my-project`
- `another-project` → `apps/another-project`
- `docs` → `documentation`
- `workspace` → root (for general tasks)

**Task naming convention:**
- Title should be descriptive and standalone
- Description should include context about what needs to happen
- Labels should include the project and optionally `auto` (for executor-eligible tasks)

Example:
```bash
cd ~/.openclaw/workspace && bd create "Integrate language translator" -p 1 -t feature -l my-project,auto -d "Allow users to view pages in regional Indian languages. Use Google Translate or similar widget."
```

**Executor-eligible tasks:** Add the `auto` label if the task can be safely executed by the cron executor without human review. Tasks requiring design decisions or major architecture changes should NOT have the `auto` label.

## Commands

Always use `bd` with the workspace `.beads/` database. The workspace root is initialized with `--stealth` so `.beads/` is gitignored.

### Add a task
```bash
cd ~/.openclaw/workspace && bd create "Title" -p 1 -t task -l project-label
```

Priority levels: 0=critical, 1=high, 2=normal, 3=low
Types: task, bug, idea, feature, refactor, docs

### Add an idea or bug
```bash
cd ~/.openclaw/workspace && bd create "Idea: something" -p 2 -t idea -l project-label
cd ~/.openclaw/workspace && bd create "Bug: something broken" -p 0 -t bug -l project-label
```

### List ready (unblocked) work
```bash
cd ~/.openclaw/workspace && bd ready
```

### Show all issues
```bash
cd ~/.openclaw/workspace && bd list
```

### Show specific issue
```bash
cd ~/.openclaw/workspace && bd show <id>
```

### Claim a task (mark in-progress)
```bash
cd ~/.openclaw/workspace && bd update <id> --claim
```

### Close a task
```bash
cd ~/.openclaw/workspace && bd close <id> --reason "Done"
```

### Add dependency
```bash
cd ~/.openclaw/workspace && bd dep add <child> <parent>
```

### Store a persistent memory/insight
```bash
cd ~/.openclaw/workspace && bd remember "insight text"
```

### Get workflow context
```bash
cd ~/.openclaw/workspace && bd prime
```

## Workflow

1. When user mentions a task/idea/bug → capture it immediately with `bd create`
2. When user asks what's pending → run `bd ready` or `bd list`
3. When user completes something → run `bd close` on the relevant item
4. Use `bd prime` to inject context when starting a new work session

## Integration with Memory Bank

- **Beads**: Granular, actionable tasks for the current project/workspace. What's the next thing to do?
- **Memory Bank**: Long-term context, design decisions, session history, identity. Why did we do it this way?

Both systems complement each other. Beads tracks what needs to happen; memory bank tracks what happened and why.
