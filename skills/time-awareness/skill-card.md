# time-awareness — Skill Card

| Field | Value |
|-------|-------|
| **Name** | time-awareness |
| **Version** | — |
| **One-liner** | Always call session_status before queries needing "today" or "now". |

## Trigger
- Any query with relative time ("recently", "last 3 days", "this week")
- Current events without explicit date (news, prices, schedules)
- "What day is it?", "What's happening today?"

## Key Commands

```
1. Call session_status ALONE (never batch with search)
2. WAIT for result
3. Construct query with returned year/month/day
```

## Rules

| Scenario | Action |
|----------|--------|
| Specific date given | Use directly, no session_status |
| Relative time | MUST session_status → compute absolute range |
| Current events (no date) | MUST session_status → include year+month |

## Dependencies
- `session_status` tool available

## Quick Example

```
User: "What happened in the last 3 days?"

WRONG:  web_search("news last 3 days 2025")  ← training-data year
RIGHT:  session_status → "2026-07-13"
        web_search("news July 10-13 2026")
```

> Year self-check: Before submitting any search, verify every year came from session_status. If you see a training-data year — STOP, you skipped step 1.
