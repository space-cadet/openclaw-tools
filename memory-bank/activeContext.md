# Active Context: openclaw-tools

## Current Status: Knowledge Skill Documented (2026-07-21)

### What Just Happened
- **Documented `agent-knowledge` ClawHub skill**: Created `skills/knowledge/SKILL.md` with usage docs, data model, and QMD integration
- **Updated README.md**: Added `knowledge` *(ClawHub)* to the skills index under Memory & Knowledge Management
- **Audit of installed ClawHub skills**: Found 5 installed (`mulch`, `self-improving-agent`, `openclaw-backup`, `openclaw-backup-optimized`, `agent-knowledge`); all were already documented except `agent-knowledge`
- **Committed**: `61a8ded` on main

### Previous Major Work (2026-07-20)
- **Created `cron-management` skill** — CLI tool for managing OpenClaw cron jobs
  - Script: `skills/cron-management/scripts/cronctl.sh`
  - Commands: `list`, `status`, `pause`, `resume`, `pause-all`, `resume-all`, `maintenance on|off`, `health <name>`
  - Tested against live cron jobs (22 jobs)

### Previous Major Work (2026-07-17)
- **T7: K3 Benchmark** — LISP interpreter 14/14, subagent tests 4/5

### Previous Major Work (2026-07-16)
- Token Usage `parse.py` — Added `--yesterday` flag for accurate daily cron reports
- SKILL.md updated: Documented both direct parser (recommended) and SQLite (optional) approaches
- skill-card.md updated: v1.2.0 with new commands and cron job examples

### Next Focus
- T2: Benchmark verification (tests moved, not yet verified post-move)
- T5: Token usage tracking — Phase 5: ClawHub publish (in progress)

### Open Questions
- Should tests/ have their own memory-bank or use repo-level one?
- GitHub Actions CI — worth it for a tools repo?
