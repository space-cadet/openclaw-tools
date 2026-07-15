# token-usage — Skill Card

| Field | Value |
|-------|-------|
| **Name** | token-usage |
| **Version** | 2.0 |
| **One-liner** | Track, aggregate, and report OpenClaw token usage with SQLite persistence. |

## Trigger
- "How many tokens did I use today/this week?"
- "What's my session cost?"
- Budget monitoring or anomaly detection

## Architecture

**SQLite-based** (incremental ingestion) — not full re-parse every time.

```
usage.db
├── daily_totals       — 90 days of granular data
├── monthly_totals     — Forever (rolled up after 90 days)
└── ingestion_log      — Tracks already-processed files
```

## Key Commands

```bash
# Initialize database (one-time)
cd scripts && python3 ingest.py --init

# Daily incremental ingestion
cd scripts && python3 ingest.py

# Yesterday's report (compact for Telegram)
cd scripts && python3 report.py --yesterday --compact

# Weekly report
cd scripts && python3 report.py --week --compact

# Monthly report
cd scripts && python3 report.py --month --compact

# Legacy direct parser (no DB)
cd scripts && python3 parse.py --today --costs
```

## Cron Jobs (Optional)

| Job | Schedule | Purpose |
|-----|----------|---------|
| Daily Ingest | 04:00 local | Incremental ingestion |
| Daily Report | 09:05 local | Yesterday's usage by job type |
| Weekly Report | Monday 09:00 | 7-day trend |
| Monthly Rotation | 1st 00:05 | Roll up 90+ day data |

## Job Type Classification

- `user` — Interactive sessions
- `cron:<name>` — Cron-triggered sessions (auto-detected)
- `background` — Background tasks

## Dependencies
- Python 3
- SQLite3
- OpenClaw session JSONL files in `~/.openclaw/agents/*/sessions/`
- `scripts/pricing.json` (user-editable)

## Quick Example

```bash
cd skills/token-usage/scripts
python3 report.py --yesterday --compact
```

Output:
```
📊 Token Usage — 2026-07-14
| Type | Msgs | Input | Output | Cost |
| user | 1273 | 3,953,479 | 419,723 | $8.5174 |
| background | 1 | 608 | 1,449 | $0.0047 |
| TOTAL | 1274 | 3,954,087 | 421,172 | $8.5221 |
```

> Important: The system sums `input + output` tokens only. `totalTokens` includes `cacheRead` which would overcount if summed across messages.

## Retention
- Daily: 90 days → rolled to monthly
- Monthly: Kept forever
