# Edit History

*Created: 2026-09-02 18:52 IST*
*Last Updated: 2026-09-18 22:56:00 IST*

### 2026-09-18

#### 22:56:00 IST - T16: mem-update skill merge + ClawHub curation
- Modified `skills/mem-update/SKILL.md` - Merged mb-text-workflow into mem-update (kept project-repo awareness Step 0A + correct §6.5 edit-chunk handling). 91 → 223 lines.
- Modified `skills/mem-format/SKILL.md` - Cleaned Windsurf/`// turbo` residue; TypeScript → pseudocode. 235 → 193 lines.
- Modified `skills/mem-load/SKILL.md` - Removed Windsurf preamble. 91 → 86 lines.
- Modified `skills-registry.json` - Marked mb-text-workflow superseded by mem-update.
- Created `memory-bank/edits/2026-09-18/225600-T16-mem-skills-merge.md` - Canonical edit chunk.
- Modified `memory-bank/tasks.md` - Stamped Last Updated.

### 2026-09-18

#### 21:53:08 IST - T16: Token-usage parser — 9.x version awareness + SQLite migration fix

- Modified `skills/token-usage/scripts/parse.py` - Added `_detect_openclaw_version()`, `detect_storage_backends()`, `_normalise_ts()`, plain `sqlite3.connect()` (macOS fix), mtime pre-filter in `find_sessions()`
- Created `memory-bank/tasks/T16.md` - Full task documentation
- Modified `memory-bank/tasks.md` - Added T16 to registry (normalized to mb-core table format)
- Modified `memory-bank/activeContext.md` - T16 as current focus
- Modified `memory-bank/progress.md` - T16 completion record
- Modified `memory-bank/session_cache.md` - Session handoff
- Created `memory-bank/sessions/2026-09-18-evening.md` - Session record

**Verification:** `--today` returns 855K input / $2.43, `--week` returns 26.3M / $35.82

### 2026-09-16

#### 11:17:45 IST - T14: Token-usage parser — zstd support + Codex/interactive split

- Modified `skills/token-usage/scripts/common.py` - Added `*.jsonl.*.zst` glob, `_zstd_open()` helper, Cloudy's defensive fix for `"info": null`
- Modified `skills/token-usage/scripts/ingest.py` - Added `background:codex` classification, `.zst` opener in `classify_session()`
- Created `skills/token-usage/README.md` - Architecture, data sources, known issues
- Created `memory-bank/tasks/T15.md` - Full task documentation
- Modified `memory-bank/tasks.md` - Added T14 to registry

**Verification:** 17 zstd sessions parsed (all k2.7), 5,598 files ingested, Sept 14–15 now visible, Codex split confirmed in DB

### 2026-09-02

## 2026-09-02

#### 18:50 IST - T14: Update knowledge layer and task-spec after T2 results
- Modified `memory-bank/implementation-details/thinking-benchmarks.md` - Added preliminary findings section with cautious interpretation
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
