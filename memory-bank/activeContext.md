# Active Context: openclaw-tools

## Current Status: Cron Management Skill Added (2026-07-20)

### What Just Happened
- **Created `cron-management` skill** — CLI tool for managing OpenClaw cron jobs
- **Script**: `skills/cron-management/scripts/cronctl.sh`
  - `list`, `status`, `pause`, `resume`, `pause-all`, `resume-all`
  - `maintenance on|off` — emergency stop via `/tmp/cron-paused` flag
  - `health <name>` — detailed run history and diagnostics
- **Tested**: All commands verified against live cron jobs (22 jobs)
- **Added to repo**: SKILL.md, _meta.json, skill-card.md, cronctl.sh

### Previous Major Work
- T7 (2026-07-17): K3 Benchmark — LISP interpreter 14/14, subagent tests 4/5
- T5 Phase 5 (2026-07-16): parse.py enhancement — added `--yesterday` flag

### Next Focus
- T2: Benchmark verification (tests moved, not yet verified post-move)

### Open Questions
- Should tests/ have their own memory-bank or use repo-level one?
- GitHub Actions CI — worth it for a tools repo?
