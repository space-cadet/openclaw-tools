# token-usage — Skill Card

| Field | Value |
|-------|-------|
| **Name** | token-usage |
| **Version** | v1.2.0 |
| **One-liner** | Track, aggregate, and report OpenClaw token usage and costs across sessions. |

## Trigger
- "How many tokens did I use today/this week?"
- "What's my session cost?"
- Budget monitoring or anomaly detection

## Architecture

**Two approaches:**

1. **Direct Parser (`parse.py`)** — Recommended for cron jobs. No database setup. Reads session JSONL directly.
2. **SQLite Database (`ingest.py` + `report.py`)** — Optional. Incremental ingestion, long-term retention, SQL queries.

## Key Commands

### Direct Parser (Recommended)
```bash
# Yesterday's usage (ideal for daily cron)
cd scripts && python3 parse.py --yesterday --costs

# Today's usage
cd scripts && python3 parse.py --today --costs

# Weekly usage
cd scripts && python3 parse.py --week --costs

# All time by model
cd scripts && python3 parse.py --all --by-model --costs

# By cron job
cd scripts && python3 parse.py --week --by-cron --costs

# JSON output
cd scripts && python3 parse.py --week --json
```

### SQLite Database (Optional)
```bash
# Initialize database (one-time)
cd scripts && python3 ingest.py --init

# Daily incremental ingestion
cd scripts && python3 ingest.py

# Reports
cd scripts && python3 report.py --yesterday --compact
cd scripts && python3 report.py --week --compact
cd scripts && python3 report.py --month --compact
```

## Cron Jobs (Direct Parser — Recommended)

| Job | Schedule | Command | Purpose |
|-----|----------|---------|---------|
| Daily Report | 04:00 local | `parse.py --yesterday --costs` | Yesterday's usage by model |
| Weekly Report | Monday 09:00 | `parse.py --week --costs` | 7-day trend + cost |

## Cron Jobs (SQLite — Optional)

| Job | Schedule | Command | Purpose |
|-----|----------|---------|---------|
| Daily Ingest | 04:00 local | `ingest.py` | Incremental ingestion |
| Daily Report | 09:05 local | `report.py --yesterday --compact` | SQLite report |
| Monthly Rotation | 1st 00:05 | `ingest.py --rotate` | Roll up 90+ day data |

## Job Type Classification

- `user` — Interactive sessions
- `cron:<name>` — Cron-triggered sessions (auto-detected)
- `background` — Background tasks

## Dependencies
- Python 3
- OpenClaw session JSONL files in `~/.openclaw/agents/*/sessions/`
- `scripts/pricing.json` (user-editable)
- SQLite3 (for SQLite database only)

## Quick Example

```bash
cd skills/token-usage/scripts
python3 parse.py --yesterday --costs
```

Output:
```
## 2026-07-15
  k2.7                        in= 2,111,110  out= 251,931  msgs=1062
                              est. $1.5594
  k2.7-code                   in=    93,323  out=   1,693  msgs=  12
                              est. $0.0500
  Day total                   in= 2,204,433  out= 253,624  msgs=1150
                                est. $1.6095

## Grand Total
  input=2,204,433  output=253,624  messages=1,150
  est. cost=$1.6095
```

> Important: The system sums `input + output` tokens only. `totalTokens` includes `cacheRead` which would overcount if summed across messages.

## Retention (SQLite only)
- Daily: 90 days → rolled to monthly
- Monthly: Kept forever
