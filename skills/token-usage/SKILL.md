---
name: token-usage
description: "Track, aggregate, and report OpenClaw token usage and costs across sessions."
homepage: https://github.com/space-cadet/openclaw-tools/tree/main/skills/token-usage
license: MIT
---

# Token Usage Tracker

Track, aggregate, and report OpenClaw token usage and costs across sessions. Provides both ad-hoc reporting and automated daily/weekly cron-based tracking with SQLite persistence.

## When to Use

- User asks "how many tokens did I use today/this week"
- User wants to know session costs or model breakdown
- Budget monitoring and anomaly detection
- Before/after optimization comparisons

## Architecture

### SQLite Database (Primary)

The system uses incremental ingestion into SQLite for efficient querying:

```
usage.db
├── daily_totals       — Aggregated by date, model, job_type
├── monthly_totals     — Rolled-up summaries (90+ day old data)
└── ingestion_log      — Tracks which session files have been processed
```

**Key design:** Only new or modified session files are parsed on each run. This avoids re-parsing thousands of historical files every day.

### Job Type Classification

Sessions are classified as:
- `user` — Interactive user sessions (no cron marker)
- `cron:<name>` — Sessions triggered by cron jobs (detected via `[cron:...]` marker)
- `background` — Background tasks (spawned without user trigger)

## Commands

### Initialize database (one-time)
```bash
cd skills/token-usage/scripts
python3 ingest.py --init
```

### Incremental ingestion (daily)
```bash
cd skills/token-usage/scripts
python3 ingest.py
```

### Yesterday's report (compact)
```bash
cd skills/token-usage/scripts
python3 report.py --yesterday --compact
```

### Weekly report
```bash
cd skills/token-usage/scripts
python3 report.py --week --compact
```

### Monthly report (includes rolled-up data)
```bash
cd skills/token-usage/scripts
python3 report.py --month --compact
```

### Legacy: Parse sessions directly (no database)
```bash
cd skills/token-usage/scripts
python3 parse.py --today
python3 parse.py --week --costs
python3 parse.py --week --by-cron
```

## Cron Jobs (Optional)

The following cron jobs can be configured for automated tracking:

| Job | Schedule | Purpose |
|-----|----------|---------|
| Daily Ingest | 04:00 local time | Incremental ingestion of new session files |
| Daily Report | 09:05 local time | Yesterday's usage by job type |
| Weekly Report | Monday 09:00 | 7-day trend + cost summary |
| Monthly Rotation | 1st 00:05 | Roll up 90+ day data to monthly totals |

Configure paths to match your `openclaw-tools` installation location.

## Data Format

Sessions are stored as JSONL with lines like:
```json
{"type":"message","message":{"role":"assistant",...},"usage":{"input":1000,"output":500,"totalTokens":1500},...}
```

## Cost Estimation

Uses model pricing from `scripts/pricing.json` (user-editable). Default prices:
- Kimi k2.7: $0.50/1M input, $2.00/1M output
- Kimi k2.7-code: $0.50/1M input, $2.00/1M output
- Claude Sonnet 4.5: $3.00/1M input, $15.00/1M output
- GPT-4o: $2.50/1M input, $10.00/1M output

Costs are approximate. Cache read/write pricing applied when available.

## Important: What "Total" Means

The script reports **input + output tokens** as the usage metric. This is the actual new token consumption per turn.

The `totalTokens` field in session files includes `cacheRead` (cached context window), which gets re-counted at every turn. Summing `totalTokens` across messages would massively overcount — a 10K context used for 100 turns would appear as 1M tokens. The system avoids this by only summing `input` and `output`.

## Retention Policy

- **Daily granularity**: 90 days
- **Monthly summaries**: Kept forever (rolled up from daily after 90 days)
- **Raw session files**: Managed by OpenClaw's session compression (`.jsonl` → `.jsonl.gz` after 3 days)

## Files

| File | Purpose |
|------|---------|
| `scripts/ingest.py` | Incremental ingestion into SQLite |
| `scripts/report.py` | Daily/weekly/monthly report generation |
| `scripts/parse.py` | Legacy direct parser (no database) |
| `scripts/pricing.json` | Model pricing configuration |
| `scripts/usage.db` | SQLite database (created at init) |

## Limitations

- Only parses assistant messages with `usage` fields (OpenClaw 2026.5+ format)
- Historical sessions before JSONL format not supported
- Costs are estimates; actual billing may differ
- Cron job paths must be configured to match your installation directory
