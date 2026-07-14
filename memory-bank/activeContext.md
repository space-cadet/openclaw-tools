# Active Context: openclaw-tools

## Current Status: Maintenance & Sync Complete (2026-07-14)

### What Just Happened
- **Workspace → Repo sync**: Added 2 custom skills (openclaw-backup, openclaw-backup-optimized) after sanitization
  - Removed ClawHub metadata (.clawhub/ dirs)
  - Removed personal phrases from backup notifications
  - Changed default timezone from `America/Sao_Paulo` → `UTC`
  - Genericized example repo URLs
- **Repo improvements**: beads skill examples now use `~/.openclaw/workspace` (actual convention)
- **Security-update-check.sh**: Added `SECURITY_TIMEZONE` env var support

### Previous Major Work (2026-07-13)
- Migrated 4 workspace skills → repo (graph-memory, netstatus, protonvpn-openvpn, worker-safety)
- Migrated 6 generic scripts → repo (all with environment-based configuration)
- Created 18 skill-card.md quick reference files
- Created skills-registry.json (machine-readable index)
- Wrote CONTRIBUTING.md and .gitignore
- All committed and pushed to main

### Next Focus
T5: Token usage tracking system — the biggest remaining task.

### Open Questions
- Should tests/ have their own memory-bank or use repo-level one?
- GitHub Actions CI — worth it for a tools repo?
