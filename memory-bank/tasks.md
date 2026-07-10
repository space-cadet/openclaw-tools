# Tasks: openclaw-tools Reorganization

## T1: Repo Infrastructure
- [x] Rename `openclaw-tests` → `openclaw-tools`
- [x] Clone to workspace
- [x] Set up memory-bank (v6.12)
- [ ] Write README.md for the repo
- [ ] Write CONTRIBUTING.md
- [ ] Set up `.gitignore` for workspace artifacts

## T2: Reorganize Existing Content
- [ ] Move `kimi-benchmarks/` → `tests/kimi-benchmarks/`
- [ ] Move `subagent-tests/` → `tests/subagent-tests/`
- [ ] Update any internal references in moved content
- [ ] Verify benchmarks still run after move

## T3: Migrate Skills (Sanitized)
- [ ] `token-usage` — universal, already in git
- [ ] `bookmarks` — generic, no personal refs
- [ ] `red-team` — universal
- [ ] `mb-init` — useful for anyone
- [ ] `mb-text-workflow` — useful for anyone
- [ ] `mb-db-workflow` — useful for anyone
- [ ] `openclaw-backup` — universal
- [ ] `openclaw-backup-optimized` — universal
- [ ] `pass-secrets` — sanitize store paths, keep generic
- [ ] `self-improving-agent` — universal
- [ ] `time-awareness` — generic
- [ ] `timer-build-monitor` — generic
- [ ] `beads` — needs check for personal references
- [ ] `cloakbrowser-stealth` — needs check for personal refs
- [ ] `mcp-client` — needs check for personal refs
- [ ] `kimiim` — needs check for personal refs
- [ ] `kimi-webbridge-desktop` — needs check for personal refs
- [ ] `kimi-desktop-gateway-policy` — **needs heavy sanitization or skip**
- [ ] `mulch` — needs check for personal refs
- [ ] `pdf-extract` — probably universal
- [ ] `worker-safety` — needs check

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
