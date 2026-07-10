# Tasks: openclaw-tools Reorganization

## T1: Repo Infrastructure
- [x] Rename `openclaw-tests` → `openclaw-tools`
- [x] Clone to workspace
- [x] Set up memory-bank (v6.12)
- [x] Write README.md for the repo (placeholder)
- [ ] Write CONTRIBUTING.md
- [ ] Set up `.gitignore` for workspace artifacts

## T2: Reorganize Existing Content
- [x] Move `kimi-benchmarks/` → `tests/kimi-benchmarks/`
- [x] Move `subagent-tests/` → `tests/subagent-tests/`
- [ ] Update any internal references in moved content
- [ ] Verify benchmarks still run after move

## T3: Migrate Skills (Sanitized)
- [x] **Batch 1 — Original skills (Sage-created), universal:**
  - [x] `token-usage` — universal, already in git
  - [x] `red-team` — universal
  - [x] `mb-init` — generic memory-bank tool
  - [x] `mb-text-workflow` — generic, sanitized paths
  - [x] `mb-db-workflow` — generic, sanitized paths
  - [x] `time-awareness` — generic
  - [x] `timer-build-monitor` — generic
  - [x] `pdf-extract` — utility
  - [x] ~~`openclaw-backup`~~ — REMOVED (ClawHub origin, not modified)
  - [x] ~~`openclaw-backup-optimized`~~ — REMOVED (ClawHub origin, not modified)
  - [x] ~~`self-improving-agent`~~ — REMOVED (ClawHub origin, not modified)
- [ ] **Batch 2 — Original skills, needs sanitization:**
  - [ ] `bookmarks` — remove Telegram-specific chat IDs
  - [ ] `beads` — check for Dolt-specific paths
  - [ ] `pass-secrets` — remove store paths, keep generic
  - [ ] `cloakbrowser-stealth` — check for hardcoded paths
  - [ ] `mcp-client` — check for personal server configs
  - [ ] `kimiim` — check for Kimi-specific group references
  - [ ] `kimi-webbridge-desktop` — check for installation paths
  - [ ] `worker-safety` — check for personal safety rules
- [ ] **Batch 3 — Heavy sanitization or skip:**
  - [ ] `kimi-desktop-gateway-policy` — very Kimi-specific
  - [ ] `image-handoff` — already shared with Cloudy, check for duplicates
- [ ] **ClawHub skills (not migrated, available at clawhub.ai):**
  - [ ] `openclaw-backup` — ClawHub v1.0.0
  - [ ] `openclaw-backup-optimized` — ClawHub v1.0.1
  - [ ] `self-improving-agent` — ClawHub v3.0.21
  - [ ] `mulch` — ClawHub v1.0.5

## T4: Migrate Scripts (Sanitized)
- [ ] `git-guardian.sh` — generic, useful
- [ ] `daily-backup.sh` — generic
- [ ] `heartbeat-*.sh` — generic (but check for hardcoded paths)
- [ ] `config-backup.sh` — generic
- [ ] `security-update-check.sh` — generic
- [ ] `disk-check.sh` — generic
- [ ] **Skip**: `sage-setup.sh`, `create-sage-user.sh`, `cloudy-*.sh` (personal)
- [ ] **Skip**: `fix-*.sh`/`fix-*.py` (specific to your setup)
- [ ] **Skip**: `add-kimi-*.py`, `copy-kimi-config.py` (specific)
- [ ] **Skip**: `start-gateway*.sh` (specific to your setup)

## T5: Token Usage Tracking System
- [ ] Enhance `parse.py` with `--save` to SQLite
- [ ] Create `usage.db` schema (daily_totals, cron_jobs, user_sessions)
- [ ] Add session classification (interactive vs cron vs background)
- [ ] Create daily cron job (23:30)
- [ ] Create weekly cron job (Sun 23:30)
- [ ] Create monthly cron job (1st 00:05)
- [ ] Add dashboard/reporting (text or HTML)

## T6: Documentation & Polish
- [ ] Each skill: README.md or SKILL.md with usage
- [ ] Each script: header comment with purpose, usage, dependencies
- [ ] Top-level README: index of all skills/scripts
- [ ] Update `skill-card.md` files for all skills
- [ ] Add GitHub Actions CI (optional, for tests)

## Blocked / Decisions Needed
- **Decision**: Should `kimi-desktop-gateway-policy` be kept or skipped? (Heavy Kimi-specific setup)
- **Decision**: Should we add a `skills-registry.json` or index file?
- **Decision**: Should tests/ have their own memory-bank or use the repo-level one?
