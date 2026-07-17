# Repo Reorganization Plan

## Background
`openclaw-tests` was originally a benchmark/test repo. It contained:
- `kimi-benchmarks/` — Kimi model benchmarks with memory-bank
- `subagent-tests/` — Subagent test harness and JSON test specs

We want to expand this into a general-purpose toolkit for OpenClaw users.

## Reorganization Steps

### Phase 1: Restructure (Done / In Progress)
1. Rename repo to `openclaw-tools`
2. Move existing benchmark content into `tests/`:
   ```
   tests/
   ├── kimi-benchmarks/       (was kimi-benchmarks/)
   │   └── memory-bank/       (keep as-is, nested)
   └── subagent-tests/        (was subagent-tests/)
   ```
3. Create top-level `skills/`, `scripts/`, `docs/`, `memory-bank/`
4. Write `README.md` with project overview and index

### Phase 2: Migrate Skills (Batch by Batch)
**Batch 1 — Universal, low-risk:**
- `token-usage` (already in git, already public-ready)
- `red-team` (pure protocol, no personal refs)
- `mb-init`, `mb-text-workflow`, `mb-db-workflow` (generic memory-bank tools)
- `openclaw-backup`, `openclaw-backup-optimized` (universal)
- `self-improving-agent` (universal pattern)
- `time-awareness` (generic)
- `timer-build-monitor` (generic)
- `pdf-extract` (utility)

**Batch 2 — Needs sanitization:**
- `bookmarks` (remove Telegram-specific chat IDs, keep generic)
- `beads` (check for Dolt-specific paths, keep generic)
- `pass-secrets` (remove store paths `api/kimi`, `api/gemini`, keep generic)
- `cloakbrowser-stealth` (check for hardcoded paths)
- `mcp-client` (check for personal server configs)
- `kimiim` (check for Kimi-specific group references)
- `kimi-webbridge-desktop` (check for installation paths)
- `mulch` (check for domain config)
- `worker-safety` (check for personal safety rules)

**Batch 3 — Heavy sanitization or skip:**
- `kimi-desktop-gateway-policy` (very Kimi-specific, may not be useful to others)
- `image-handoff` (already shared with Cloudy, check for duplicates)

### Phase 3: Migrate Scripts
**Generic scripts (move as-is):**
- `git-guardian.sh` — scans for uncommitted work
- `daily-backup.sh` — workspace backup
- `heartbeat-run.sh`, `heartbeat-compact.sh`, `heartbeat-watchdog.sh` — heartbeat system
- `config-backup.sh` — config backup
- `security-update-check.sh` — security check
- `disk-check.sh` — disk usage check

**Skip (personal/too specific):**
- `sage-setup.sh`, `sage-setup-clean.sh`, `sage-final.sh`, `sage-resume.sh`
- `create-sage-user.sh`, `create-cloudy-user.sh`
- `cloudy-cmd.sh`, `cloudy-wrapper.sh`, `cloudy-deepak.sh`
- `onboard-cloudy.sh`, `onboard-cloudy-v2.sh`
- `clean-cloudy-workspace.sh`, `update-cloudy-paths.sh`
- `add-kimi-claw.py`, `add-kimi-provider.py`, `copy-kimi-config.py`
- `fix-*.py`, `fix-*.sh` (all fix scripts are specific to your setup)
- `configure-telegram.py`, `check-telegram-config.sh`, `test-telegram.sh` (specific to your Telegram bot)
- `start-gateway.sh`, `start-gateway-manual.sh` (specific to your daemon setup)
- `crash-recovery.sh` (specific to your recovery history)
- `qhe_numerics_cron.sh` (physics-specific)
- `mcp-call.js` (specific to your MCP servers)

### Phase 4: Token Usage System
See memory-bank/tasks.md T5 for full plan.

## Sanitization Checklist for Each Skill
- [ ] Remove personal names ("Sage", "Deepak", "Cloudy")
- [ ] Remove specific paths (`/Users/sage/`, `/Users/deepak/`)
- [ ] Remove chat IDs, phone numbers, API keys
- [ ] Remove specific service references (your Telegram bot, your Kimi gateway)
- [ ] Remove specific domain names (unless they're the skill's purpose)
- [ ] Replace with `$HOME`, `~`, `your-username`, or generic placeholders
- [ ] Add note: "Replace with your own paths/IDs"

## Post-Reorganization Validation
- [ ] All skills have SKILL.md or README.md
- [ ] All scripts have header comments
- [ ] No personal references in any file
- [ ] GitHub secret scanning passes (no accidental keys)
- [ ] Tests still run (benchmarks, harness)
- [ ] README has clear index of all skills and scripts
