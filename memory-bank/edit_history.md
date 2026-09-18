# Edit History

*Created: 2026-09-02 18:52 IST*
*Last Updated: 2026-09-18 23:45:00 IST*

### 2026-09-18

#### 22:56:00 IST - T16: mem-update skill merge + ClawHub curation
- Modified `skills/mem-update/SKILL.md` - Merged mb-text-workflow into mem-update (kept project-repo awareness Step 0A + correct §6.5 edit-chunk handling). 91 → 223 lines.
- Modified `skills/mem-format/SKILL.md` - Cleaned Windsurf/`// turbo` residue; TypeScript → pseudocode. 235 → 193 lines.
- Modified `skills/mem-load/SKILL.md` - Removed Windsurf preamble. 91 → 86 lines.
- Modified `skills-registry.json` - Marked mb-text-workflow superseded by mem-update.
- Modified `memory-bank/tasks.md` - Stamped Last Updated.

### 2026-09-02

#### 18:50 IST - T14: Update knowledge layer and task-spec after T2 results
- Modified `memory-bank/implementation-details/thinking-benchmarks.md` - Added preliminary findings section with cautious interpretation ("observation, not evidence")
- Modified `tests/thinking-benchmarks/task-spec.md` - Marked T2 as partially complete; added preliminary results table
- Validated `tests/thinking-benchmarks/results.json` - Confirmed valid JSON via python3 -m json.tool

#### 18:40 IST - T14: T2 pivot force results
- Modified `tests/thinking-benchmarks/results.json` - Added T2 results for low/medium/high
- Modified `memory-bank/tasks/T14.md` - Updated progress with T2 results and key finding
- Modified `memory-bank/progress.md` - Updated T14 entry with T2 results
- Modified `memory-bank/session_cache.md` - Updated progress tracker

#### 17:37 IST - T14: Benchmark suite design
- Created `memory-bank/tasks/T14.md` - T14 task definition with 5-task benchmark suite
- Created `tests/thinking-benchmarks/task-spec.md` - Task prompts, correct answers, scoring rubrics
- Created `tests/thinking-benchmarks/results.json` - Empty results template with schema
- Created `memory-bank/implementation-details/thinking-benchmarks.md` - Methodology, design rationale, limitations
- Created `memory-bank/sessions/2026-09-02-afternoon.md` - Session log
- Modified `memory-bank/tasks.md` - Added T14 to task registry
- Modified `memory-bank/activeContext.md` - Set T14 as current focus
- Modified `memory-bank/progress.md` - Added T14 progress section
- Modified `memory-bank/session_cache.md` - Updated current session info

### 2026-08-23

#### 14:04:00 IST - T13: Record Kimi/OpenClaw context degradation findings
- Created `kimi-benchmarks/context-degradation/README.md` - Added shared report index and public-data restrictions.
- Created `kimi-benchmarks/context-degradation/openclaw-kimi-tool-degradation.md` - Recorded sanitized evidence using Instance A and Instance B labels.
- Created `memory-bank/tasks/T13.md` - Added investigation scope, criteria, dependencies, and open questions.
- Updated `memory-bank/tasks.md` - Registered T13 in the project task index.
- Updated `memory-bank/activeContext.md` - Set T13 as the current focus.
- Updated `memory-bank/progress.md` - Recorded the T13 milestone.
- Created `memory-bank/sessions/2026-08-23-afternoon.md` - Recorded this session's work and next steps.
- Updated `memory-bank/session_cache.md` - Added T13 to active session state.

### 2026-08-16

#### 02:07:36 IST - T8/T11: Record cronctl compatibility fix and diagnostic shutdown
- Updated `memory-bank/tasks.md` - Recorded current CLI compatibility work and diagnostic cron pause
- Updated `memory-bank/activeContext.md` - Recorded disabled availability job and pushed fix
- Updated `memory-bank/session_cache.md` - Recorded session close state
- Updated `memory-bank/sessions/2026-08-15-night.md` - Appended shutdown and compatibility follow-up

#### 01:28:19 IST - T11: Record availability cron and results organization
- Modified `memory-bank/tasks/T11.md` - Recorded raw availability data, existing capability benchmark locations, and planned aggregate results layer
- Modified `memory-bank/tasks.md` - Marked implemented T11 design/deployment work complete and retained aggregate reporting as open
- Modified `memory-bank/activeContext.md` - Documented separation of availability and capability result families
- Modified `memory-bank/progress.md` - Recorded the T11 results-organization milestone
- Modified `memory-bank/session_cache.md` - Added the current repository memory-bank update
- Modified `memory-bank/sessions/2026-08-15-night.md` - Appended the results-organization follow-up

### 2026-08-15

#### 01:32:26 IST - T11: Define provider/model availability study
- Created `memory-bank/tasks/T11.md` - Added planning task and acceptance criteria
- Created `memory-bank/implementation-details/model-availability-study.md` - Documented provider-agnostic direct/OpenClaw harness design, JSONL schema, scheduling, reporting, and cron-control compatibility
- Updated `memory-bank/tasks.md` - Registered T11 as an active planning task

### 2026-08-14

#### 18:36:00 IST - T10: Prepare token-usage v2.4.0
- Modified `tests/token_usage/test_parsers.py` - Added direct-versus-SQLite comparison coverage.
- Modified `skills/token-usage/SKILL.md` - Bumped version to 2.4.0.
- Modified `skills/token-usage/skill-card.md` - Added v2.4.0 changes.
- Modified `skills-registry.json` - Updated token-usage version and description.
- Modified `memory-bank/tasks/T10.md` - Marked code work ready for release review.
- Modified `memory-bank/implementation-details/token-usage.md` - Recorded release status.
- Modified `memory-bank/session_cache.md` - Set ClawHub review as the next step.

#### 18:30:00 IST - T10: Record release completion and ClawHub blocker
- Modified `memory-bank/tasks/T10.md` - Marked code work complete and recorded the publishing blocker.
- Modified `memory-bank/implementation-details/token-usage.md` - Added the v2.4.0 status and next step.
- Modified `memory-bank/activeContext.md` - Recorded the release state.
- Modified `memory-bank/progress.md` - Added the release result.
- Modified `memory-bank/sessions/2026-08-14-evening.md` - Recorded the publish attempt.
- Modified `memory-bank/session_cache.md` - Updated the handoff state.

#### 18:28:00 IST - T10: Use model-aware pricing in cron reports
- Modified `skills/token-usage/scripts/parse.py` - Track model and cache values in cron totals.
- Modified `memory-bank/tasks/T10.md` - Recorded the cron pricing fix.
- Modified `memory-bank/implementation-details/token-usage.md` - Updated remaining work.
- Modified `memory-bank/session_cache.md` - Updated T10 progress.

#### 18:24:33 IST - T10: Clean current release status
- Modified `memory-bank/tasks.md` - Marked completed work and pending ClawHub review.
- Modified `memory-bank/session_cache.md` - Removed stale current-status wording.
- Modified `memory-bank/implementation-details/token-usage.md` - Clarified the publish attempts and current state.
- Modified `memory-bank/activeContext.md` - Recorded that the shared parser and related fixes are complete.
- Modified `memory-bank/sessions/2026-08-14-evening.md` - Recorded the cleanup.

#### 18:24:00 IST - T10: Fix local dates, CLI windows, and report cache totals
- Modified `skills/token-usage/scripts/common.py` - Added local timestamp and date helpers.
- Modified `skills/token-usage/scripts/parse.py` - Added rolling-window flags and local-day grouping.
- Modified `skills/token-usage/scripts/ingest.py` - Store SQLite dates in local time.
- Modified `skills/token-usage/scripts/report.py` - Show cache totals and use local time.
- Modified `tests/token_usage/test_parsers.py` - Added gzip and midnight-boundary coverage.
- Modified `memory-bank/tasks/T10.md` - Recorded completed work.
- Modified `memory-bank/implementation-details/token-usage.md` - Updated remaining work.
- Modified `memory-bank/session_cache.md` - Updated T10 progress.

#### 18:20:00 IST - T10: Record ClawHub pending publication
- Modified `memory-bank/tasks/T10.md` - Recorded that ClawHub accepted v2.4.0 and is reviewing it.
- Modified `memory-bank/implementation-details/token-usage.md` - Added the ClawHub version record and pending state.
- Modified `memory-bank/activeContext.md` - Updated the release state.
- Modified `memory-bank/progress.md` - Recorded the accepted but pending release.
- Modified `memory-bank/sessions/2026-08-14-evening.md` - Recorded the successful retry.
- Modified `memory-bank/session_cache.md` - Updated the handoff state.

#### 18:12:00 IST - T10: Add shared token parser and basic tests
- Created `skills/token-usage/scripts/common.py` - Shared OpenClaw and Codex parsing.
- Modified `skills/token-usage/scripts/parse.py` - Use shared parsing and cache-aware costs.
- Modified `skills/token-usage/scripts/ingest.py` - Use shared parsing and safe model pricing.
- Created `tests/token_usage/test_parsers.py` - Test OpenClaw and Codex records.
- Modified `memory-bank/tasks/T10.md` - Recorded completed work and remaining work.
- Modified `memory-bank/implementation-details/token-usage.md` - Recorded the new parser and tests.
- Modified `memory-bank/session_cache.md` - Updated T10 progress.
- Modified `memory-bank/progress.md` - Recorded the implementation step.
- Modified `memory-bank/sessions/2026-08-14-evening.md` - Recorded the implementation step.

#### 17:35:37 IST - T10: Record token-usage gaps and next steps
- Created `memory-bank/tasks/T10.md` - Recorded the token-usage work plan.
- Created `memory-bank/implementation-details/token-usage.md` - Described the current design and known gaps.
- Created `memory-bank/sessions/2026-08-14-evening.md` - Recorded the audit session.
- Created `memory-bank/session_cache.md` - Set T10 as the active task.
- Modified `memory-bank/tasks.md` - Added T10 to the task list.
- Modified `memory-bank/activeContext.md` - Set the current focus to T10.
- Modified `memory-bank/progress.md` - Added the audit to current progress.

### 2026-07-28

#### 03:45:00 IST - T9: Import mem-* skills from .agents

- Action `skills/mem-update/SKILL.md` - Created: Enhanced v6.12 compliance with project-repo awareness (Step 0)
- Action `skills/mem-scan/SKILL.md` - Created: Multi-repo deep scan for task analysis
- Action `skills/mem-format/SKILL.md` - Created: Template compliance validation
- Action `skills/mem-load/SKILL.md` - Created: Context loading utility
- Action `skills-registry.json` - Updated: Added 4 new mem-* skills (25 total)
- Action `memory-bank/activeContext.md` - Updated: Recorded T9 completion
- Action `memory-bank/tasks.md` - Updated: Added T9 task entry

**Problem**: `mb-text-workflow` defaulted to workspace memory-bank without checking project repos. Caused T35c to be created in wrong location.

**Solution**: Imported `mem-update` from `~/.agents/skills/` with Step 0 (multi-repo scan). Prevents duplicate tasks across workspace and project repos.

### 2026-07-23

#### 11:02 IST - T5: Multi-source pricing updater + model registry

**Actions:**
- Created `update-pricing.py` — fetches model pricing from OpenRouter API (342 models) and Moonshot direct docs
- Created `registry.json` — model metadata with availability, provider, context windows, alternative pricing
- Fixed `parse.py` None cache pricing bug (TypeError in estimate_cost)
- Updated weekly cron to refresh pricing before report generation
- Updated `pricing.json` with Moonshot-direct rates (CNY→USD conversion at 7.2)

**Key findings:**
| Model | Moonshot Direct | OpenRouter | Diff |
|-------|----------------|------------|------|
| K2.6 | $0.90/M | $0.68/M | OR cheaper |
| K2.7 | $0.90/M | — | — |
| K2.7-code | $0.90/M | $0.82/M | +9% |
| K3 | $2.78/M | $3.00/M | +8% |

**Files modified:**
- `skills/token-usage/scripts/update-pricing.py` (new)
- `skills/token-usage/scripts/registry.json` (new)
- `skills/token-usage/scripts/parse.py` (bugfix)
- `skills/token-usage/scripts/pricing.json` (updated)

**Commit:** `37f65af`

### 2026-07-21

#### 12:08:00 IST - Documented agent-knowledge ClawHub skill in repo
- Created `skills/knowledge/SKILL.md` — Documented the `agent-knowledge` skill from ClawHub (ianderrington) with usage, data model, and QMD integration
- Modified `README.md` — Added `knowledge` *(ClawHub)* to Memory & Knowledge Management skills index
- Audit found 5 installed ClawHub skills; all already documented except agent-knowledge

### 2026-07-17

#### 23:55 IST - T7: K3 Benchmark Results

**Actions:**
- Created `tests/kimi-benchmarks/k3/interpreter.py` — K3's LISP interpreter (perfect score)
- Created `tests/kimi-benchmarks/k3/results.md` — full benchmark report
- Updated `memory-bank/tasks.md` — added T7 task
- Updated `memory-bank/progress.md` — logged T7 completion
- Updated `memory-bank/activeContext.md` — current status

**Results:**
- LISP Interpreter: 14/14 (100%) — K3 significantly outperforms K2.7 (10/11) and K2.6 (8/11)
- Subagent tests: 4/5 PASS — all direct spawning works; nested subagents blocked by runtime guardrail

**Key Finding:**
K3 is a better coder than both K2.7 and K2.6. The model override mechanism works (spawn accepted with model parameter), but K2.7 children abort when nested — this is expected runtime behavior preventing runaway subagent chains.

### 2026-07-16

#### 11:56:00 IST - T5: parse.py Enhancement — Added --yesterday flag and updated documentation
- Modified `skills/token-usage/scripts/parse.py` - Added `--yesterday` argument and `until` boundary for yesterday-only reports (+5 lines)
- Modified `skills/token-usage/SKILL.md` - Rewrote to document both direct parser (recommended) and SQLite (optional) approaches
- Modified `skills/token-usage/skill-card.md` - Updated to v1.2.0 with new commands, cron examples, and output format
