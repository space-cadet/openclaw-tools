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
- [x] **Batch 4 — Custom skills added to repo (sanitized):**
  - [x] `openclaw-backup` — simple tar-based backup with rotation
  - [x] `openclaw-backup-optimized` — Node.js backup with workspace splitting, change tracking, Discord notifications
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

## T5: Token Usage Tracking System ✅ COMPLETE (2026-07-15)
- [x] **Phase 1: SQLite Database + Incremental Ingestion**
  - [x] Create `usage.db` schema: `daily_totals`, `monthly_totals`, `ingestion_log`
  - [x] Create `ingest.py` — incremental ingestion (only new/modified session files)
  - [x] Session classification: `user` (interactive), `cron:<job_name>`, `background`
  - [x] Update `pricing.json` with `kimi/k2.7` and `kimi/k2.7-code` entries
- [x] **Phase 2: Cron Jobs**
  - [x] Daily ingest (04:00 IST) — job `ff9371fc-ead1-44b1-a30e-b03794bd8512`
  - [x] Daily report (09:05 IST) — job `d39279ae-f544-4b04-8901-6e4059002017`
  - [x] Weekly report (Monday 09:00 IST) — job `ad99af39-465f-4251-beea-8efed9a16f96`
- [x] **Phase 3: Rotation & Retention**
  - [x] Daily granularity: 90 days retention
  - [x] Monthly rollup: forever (aggregated)
  - [x] Vacuum after monthly rotation
  - [x] Monthly rotation cron (1st 00:05) — job `2e2e3337-adce-4848-90f8-1d19992585f0`
- [x] **Phase 4: Dashboard/Reporting**
  - [x] Text-based report for Telegram (`report.py --compact`)
  - [ ] Optional: HTML dashboard (extend later)

### Files Created
- `skills/token-usage/scripts/ingest.py` — incremental ingestion into SQLite
- `skills/token-usage/scripts/report.py` — daily/weekly/monthly reports
- `skills/token-usage/scripts/pricing.json` — model pricing config (updated)
- `skills/token-usage/scripts/usage.db` — SQLite database (initialized, 6589 files ingested)

### Cron Jobs
| Job | Schedule | ID | Purpose |
|-----|----------|-----|---------|
| Token Usage — Daily Ingest | 04:00 IST daily | `ff9371fc-...` | Ingest new session files |
| Token Usage — Daily Report | 09:05 IST daily | `d39279ae-...` | Yesterday's usage report |
| Token Usage — Weekly Report | Monday 09:00 IST | `ad99af39-...` | 7-day trend |
| Token Usage — Monthly Rotation | 1st 00:05 IST | `2e2e3337-...` | Roll up 90+ day data |

### Design Decisions
- **Incremental not full re-parse**: `ingest.py` tracks processed files in `ingestion_log`
- **SQLite over JSONL**: Queryable, fast aggregations, handles gzipped sessions
- **Job type detection**: Regex on first user message (`[cron:...]`) for cron; absence for user; `bg:` in session key for background
- **Pricing**: per-1M-token rates, read from `pricing.json` (overridable)
- **Retention**: Daily data → 90 days, then rolled to monthly. Monthly summaries kept forever.

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
