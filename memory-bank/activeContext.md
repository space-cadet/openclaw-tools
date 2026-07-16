# Active Context: openclaw-tools

## Current Status: Token Usage Skill Updated (2026-07-16)

### What Just Happened
- **parse.py — Added `--yesterday` flag**: Direct parser now supports yesterday-only reports (ideal for daily cron jobs)
- **SKILL.md updated**: Documented both direct parser (recommended) and SQLite (optional) approaches
- **skill-card.md updated**: v1.2.0 with new commands and cron job examples

### Background: Why the Switch
The SQLite-based approach (`ingest.py` + `report.py`) produced inflated cost estimates ($6.20 vs $1.61 for the same day) due to how it classified and aggregated sessions. The direct parser (`parse.py`) reads session JSONL directly, avoids the database overhead, and produces accurate, consistent numbers. The workspace switched to `parse.py` for daily/weekly cron reports, keeping the SQLite tools available for advanced use cases.

### Previous Major Work (2026-07-14)
- Workspace → Repo sync: Added 2 custom skills (openclaw-backup, openclaw-backup-optimized)
- Migrated 4 workspace skills → repo (graph-memory, netstatus, protonvpn-openvpn, worker-safety)
- Migrated 6 generic scripts → repo

### Next Focus
- T5: Token usage tracking — Phase 5: ClawHub publish (in progress)

### Open Questions
- Should tests/ have their own memory-bank or use repo-level one?
- GitHub Actions CI — worth it for a tools repo?
