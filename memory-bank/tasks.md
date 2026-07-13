# Tasks: openclaw-tools Reorganization

## T1: Repo Infrastructure ✅ COMPLETE
- [x] Rename `openclaw-tests` → `openclaw-tools`
- [x] Clone to workspace
- [x] Set up memory-bank (v6.12)
- [x] Write README.md for the repo
- [x] Write CONTRIBUTING.md
- [x] Set up `.gitignore` for workspace artifacts

## T2: Reorganize Existing Content
- [x] Move `kimi-benchmarks/` → `tests/kimi-benchmarks/`
- [x] Move `subagent-tests/` → `tests/subagent-tests/`
- [ ] Update any internal references in moved content
- [ ] Verify benchmarks still run after move

## T3: Migrate Skills (Sanitized) ✅ COMPLETE
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
- [x] **Batch 2 — Original skills, needs sanitization:**
  - [x] `bookmarks` — sanitized (removed Telegram-specific refs)
  - [x] `beads` — sanitized (replaced specific projects with generic examples)
  - [x] `pass-secrets` — sanitized (removed store paths, kept generic)
  - [x] `cloakbrowser-stealth` — sanitized (fixed shebang, paths)
  - [x] `mcp-client` — sanitized (replaced example paths)
  - [x] `image-handoff` — sanitized (replaced personal name with "User")
- [x] **Batch 3 — Workspace skills added to repo:**
  - [x] `graph-memory` — knowledge graph queries (sanitized author)
  - [x] `netstatus` — network + gateway status
  - [x] `protonvpn-openvpn` — VPN management
  - [x] `worker-safety` — hard safety limits
- [x] **Skipped:**
  - [x] `kimi-desktop-gateway-policy` — very Kimi-specific → SKIP (user request)
  - [x] `self-improving-agent` — ClawHub origin v3.0.21, modified locally
  - [x] `mulch` — ClawHub origin v1.0.5, modified locally

## T4: Migrate Scripts (Sanitized) ✅ COMPLETE
- [x] `security-update-check.sh` — generic, configurable paths
- [x] `check-disk.sh` — generic, configurable threshold
- [x] `protonvpn.sh` — generic, configurable paths
- [x] `heartbeat-watchdog.sh` — refactored with env vars + CLI args
- [x] `crash-recovery.sh` — refactored with parameterized paths
- [x] `netstatus.sh` — refactored, removed gateway checks
- [x] **Skip**: `sage-setup.sh`, `create-sage-user.sh`, `cloudy-*.sh` (personal)
- [x] **Skip**: `fix-*.sh`/`fix-*.py` (specific to setup)
- [x] **Skip**: `add-kimi-*.py`, `copy-kimi-config.py` (specific)
- [x] **Skip**: `start-gateway*.sh` (specific to setup)
- [x] **Skip**: `beads-executor-check.sh`, `moltbook-*.sh`, `game-center-health-check.sh` (too specific)

## T5: Token Usage Tracking System
- [ ] Enhance `parse.py` with `--save` to SQLite
- [ ] Create `usage.db` schema (daily_totals, cron_jobs, user_sessions)
- [ ] Add session classification (interactive vs cron vs background)
- [ ] Create daily cron job (23:30)
- [ ] Create weekly cron job (Sun 23:30)
- [ ] Create monthly cron job (1st 00:05)
- [ ] Add dashboard/reporting (text or HTML)

## T6: Documentation & Polish ✅ COMPLETE
- [x] Each skill: SKILL.md with usage
- [x] Each skill: skill-card.md (quick reference)
- [x] Each script: header comment with purpose, usage, dependencies
- [x] Top-level README: index of all skills/scripts
- [x] skills-registry.json: machine-readable skill index
- [ ] Add GitHub Actions CI (optional, for tests)

## Blocked / Decisions
- [x] **Decision**: `kimi-desktop-gateway-policy` → SKIP
- [x] **Decision**: `skills-registry.json` → YES, created
- [ ] **Decision**: Should tests/ have their own memory-bank or use repo-level one?
