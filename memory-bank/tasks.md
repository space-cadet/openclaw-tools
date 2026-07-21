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

## T5: Token Usage Tracking System ✅ COMPLETE (2026-07-15) — Phase 5: parse.py Enhancement (2026-07-16) — v2.1.0 Rolling Windows (2026-07-21)
- [x] **Phase 1: SQLite Database + Incremental Ingestion**
- [x] **Phase 2: Cron Jobs**
- [x] **Phase 3: Rotation & Retention**
- [x] **Phase 4: Dashboard/Reporting**
- [x] **Phase 5: Direct Parser Enhancement**
  - [x] Add `--yesterday` flag to `parse.py` for daily cron reports
  - [x] Update `SKILL.md` — document both direct parser (recommended) and SQLite (optional) approaches
  - [x] Update `skill-card.md` — v1.2.0 with new commands and examples
  - [x] Switch workspace cron jobs to use `parse.py` (accurate, no DB overhead)
  - [x] Keep SQLite tools available for advanced use cases (SQL queries, long-term retention)
- [x] **v2.1.0: Rolling Time Windows & Performance**
  - [x] Add `--hours N` — rolling N-hour window
  - [x] Add `--since` / `--until` — ISO timestamps, dates, or relative (`1d`, `2h`, `30m`)
  - [x] Add `--days N` — last N calendar days
  - [x] Add `--cache` — include cache read/write columns
  - [x] Add `--session-detail` — per-session breakdown with models
  - [x] Mtime filtering — skips files not modified within time window (critical with 7,269 session files)
  - [x] Update `SKILL.md` — v2.1.0 documentation
  - [x] Update `skills-registry.json` — version 2.1.0
  - [x] Commits: `7bc7ede`, `88cc111`

### Design Decisions (Updated 2026-07-16)
- **Direct parser is primary for cron jobs**: `parse.py` reads session JSONL directly, produces accurate numbers without SQLite overhead
- **SQLite remains available**: For advanced querying, dashboards, and long-term retention beyond session files
- **Cost accuracy**: parse.py produces consistent cost estimates ($1.61 vs SQLite's $6.20 for same day — the SQLite approach had classification/aggregation issues)
- **No breaking changes**: Existing `ingest.py`/`report.py` users unaffected; new `--yesterday` flag is additive

### Files Created/Modified
- `skills/token-usage/scripts/parse.py` — Added `--yesterday` flag (+5 lines)
- `skills/token-usage/SKILL.md` — Rewrote to document both approaches
- `skills/token-usage/skill-card.md` — Updated to v1.2.0

### Cron Jobs (Workspace — Updated 2026-07-16)
| Job | Schedule | Tool | Purpose |
|-----|----------|------|---------|
| Token Usage — Daily Report | 04:00 IST daily | `parse.py --yesterday --costs` | Yesterday's usage by model |
| Token Usage — Weekly Report | Monday 09:00 IST | `parse.py --week --costs` | 7-day trend + cost summary |

(Previous SQLite-based cron jobs disabled — see T5 Phase 2 history)

## T6: Documentation & Polish ✅ COMPLETE
- [x] Each skill: SKILL.md with usage
- [x] Each skill: skill-card.md (quick reference)
- [x] Each script: header comment with purpose, usage, dependencies
- [x] Top-level README: index of all skills/scripts
- [x] skills-registry.json: machine-readable skill index
- [ ] Add GitHub Actions CI (optional, for tests)

## T7: K3 Benchmark (2026-07-17) ✅ COMPLETE
- [x] Run LISP interpreter test — 14/14 (100%), perfect score
- [x] Run subagent stress tests — 4/5 PASS, 1 PARTIAL (nested subagents blocked by design)
- [x] Compare with K2.6 (8/11) and K2.7 Code (10/11) results
- [x] Save interpreter.py and results.md to tests/kimi-benchmarks/k3/
- [x] Push to repo

### Results
| Test | K2.6 | K2.7 Code | K3 |
|------|------|-----------|-----|
| LISP Interpreter | 8/11 (72.7%) | 10/11 (90.9%) | **14/14 (100%)** |
| Basic Spawn | — | — | ✅ PASS |
| Tool Access | — | — | ✅ PASS |
| Model Override | — | — | ⚠️ PARTIAL (nested blocked) |
| Parallel Spawn | — | — | ✅ PASS |
| Timeout Stress | — | — | ✅ PASS |

### Key Finding
K3 is a significantly better coder than K2.7 and K2.6. Subagent spawning works reliably at depth 1. Nested subagents (depth > 1) are blocked by the runtime as a safety guardrail.

## T8: Cron Management Skill (2026-07-20) ✅ COMPLETE
- [x] Create `cron-management` skill with SKILL.md, _meta.json, skill-card.md
- [x] Create `scripts/cronctl.sh` — CLI for listing, pausing, resuming, maintenance mode
- [x] Test all commands: list, status, pause, resume, pause-all, resume-all, maintenance, health
- [x] Update skills-registry.json
- [x] Update memory-bank (activeContext, progress, tasks)
- [x] Push to repo

### Features
- `cronctl list` — show all jobs with ✅/❌ status
- `cronctl pause <name>` / `cronctl resume <name>` — single job toggle
- `cronctl pause-all` / `cronctl resume-all` — bulk operations
- `cronctl maintenance on|off` — emergency stop via `/tmp/cron-paused` flag
- `cronctl status` — health dashboard with failing/disabled/overdue counts
- `cronctl health <name>` — detailed run history and diagnostics

### Integration Guide Added
- Shell scripts, Python, Node.js examples for maintenance mode checks
- Rollout strategy for existing jobs
- `memory-bank/implementation-details/cron-management.md` with full architecture

### Why This Exists
OpenClaw has no built-in `enable`/`disable` command for cron jobs. The user had to manually disable 12+ jobs during a billing issue. This skill provides:
1. **Structured CLI** — no more raw JSON patches
2. **Bulk operations** — pause/resume all at once
3. **Maintenance mode** — works even if OpenClaw is down
4. **Health visibility** — see failures without digging through individual job states

