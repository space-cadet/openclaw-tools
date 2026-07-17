# mb-text-workflow — Skill Card

| Field | Value |
|-------|-------|
| **Name** | mb-text-workflow |
| **Version** | v6.12 |
| **One-liner** | Manual memory bank update workflow via markdown editing (no database). |

## Trigger
- "update memory bank", "create edit chunk", "update tasks.md"
- "update session cache", "memory bank update workflow"
- Projects without DB-native workflow set up

## Key Commands

No CLI — this is a manual editing workflow:

1. **Step 0 (Discovery):** Check git history, uncommitted changes, recent edit chunks
2. **Step 1:** Update `memory-bank/tasks/Txx.md`
3. **Step 2:** Update `memory-bank/tasks.md` registry
4. **Step 3:** Update `implementation-details/` (knowledge layer — NOT optional)
5. **Step 4:** Update/create `memory-bank/sessions/YYYY-MM-DD-PERIOD.md`
6. **Step 5:** Update `memory-bank/session_cache.md`
7. **Step 6:** Update `activeContext.md`, `errorLog.md`, etc.
8. **Step 7:** Create edit chunk: `memory-bank/edits/YYYY-MM-DD/HHMMSS-Txx-edit-chunk.md`
9. **Step 8:** Regenerate `memory-bank/edit_history.md` from chunks

## Dependencies
- Project with memory-bank directory structure
- Current time and timezone

## Quick Example

```markdown
# memory-bank/edits/2026-07-13/143022-T1-edit-chunk.md
---
kind: edit_chunk
id: abc123
created_at: 2026-07-13 14:30:22 UTC
task_ids: [T1]
---

#### 14:30:22 UTC - T1: Fix auth bug
- Modified `src/auth.js` - Added token validation
```

> NEVER edit `edit_history.md` directly — always create chunk files.
