---
name: token-usage
description: "Track, aggregate, and report OpenClaw token usage and costs across sessions."
homepage: https://github.com/space-cadet/openclaw-tools/tree/main/skills/token-usage
license: MIT
---

# Token Usage Tracker

Track, aggregate, and report OpenClaw token usage and costs across sessions. Provides both ad-hoc reporting and automated daily/weekly cron-based tracking.

## When to Use

- User asks "how many tokens did I use today/this week"
- User wants to know session costs or model breakdown
- Budget monitoring and anomaly detection
- Before/after optimization comparisons

## Architecture

The system provides two reporting approaches:

### Direct Parser (Primary — `parse.py`)

Parses session JSONL files directly with no database required. This is the recommended approach for cron jobs and ad-hoc reporting.

**Key features:**
- No database setup — reads session files directly
- Supports `--today`, `--yesterday`, `--week`, `--all`
- Cost estimation with `--costs`
- Cron job detection with `--by-cron`
- JSON output with `--json`
- Specific session files via `--sessions`

### SQLite Database (`ingest.py` + `report.py`)

Optional incremental ingestion into SQLite for advanced querying and long-term retention:

```
usage.db
├── daily_totals       — Aggregated by date, model, job_type
├── monthly_totals     — Rolled-up summaries (90+ day old data)
└── ingestion_log      — Tracks which session files have been processed
```

**Use when:** you need SQL queries, long-term retention beyond session files, or custom dashboards.

## Commands

### Direct Parser (Recommended)

```bash
cd skills/token-usage/scripts

# Today's usage
python3 parse.py --today --costs

# Yesterday's usage (ideal for daily cron reports)
python3 parse.py --yesterday --costs

# Weekly usage
python3 parse.py --week --costs

# All time, grouped by model
python3 parse.py --all --by-model --costs

# Weekly usage broken down by cron job
python3 parse.py --week --by-cron --costs

# JSON output for external dashboards
python3 parse.py --week --json

# Specific session files
python3 parse.py --sessions /path/to/session1.jsonl /path/to/session2.jsonl --costs
```

### SQLite Database (Optional)

```bash
cd skills/token-usage/scripts

# Initialize database (one-time)
python3 ingest.py --init

# Incremental ingestion (daily)
python3 ingest.py

# Yesterday's report (compact)
python3 report.py --yesterday --compact

# Weekly report
python3 report.py --week --compact

# Monthly report (includes rolled-up data)
python3 report.py --month --compact
```

## Cron Jobs (Optional)

The following cron jobs can be configured for automated tracking. These examples use the direct parser approach:

| Job | Schedule | Command | Purpose |
|-----|----------|---------|---------|
| Daily Report | 04:00 local time | `parse.py --yesterday --costs` | Yesterday's usage by model |
| Weekly Report | Monday 09:00 | `parse.py --week --costs` | 7-day trend + cost summary |

For SQLite-based tracking, configure:
| Job | Schedule | Command | Purpose |
|-----|----------|---------|---------|
| Daily Ingest | 04:00 local time | `ingest.py` | Incremental ingestion |
| Daily Report | 09:05 local time | `report.py --yesterday --compact` | SQLite-based report |
| Monthly Rotation | 1st 00:05 | `ingest.py --rotate` | Roll up 90+ day data |

Configure paths to match your `openclaw-tools` installation location.

## Data Format

Sessions are stored as JSONL with lines like:
```json
{"type":"message","message":{"role":"assistant",...},"usage":{"input":1000,"output":500,"totalTokens":1500},...}
```

## Job Type Classification

Sessions are classified as:
- `user` — Interactive user sessions (no cron marker)
- `cron:<name>` — Sessions triggered by cron jobs (detected via `[cron:...]` marker)
- `background` — Background tasks (spawned without user trigger)

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

## Retention Policy (SQLite only)

- **Daily granularity**: 90 days
- **Monthly summaries**: Kept forever (rolled up from daily after 90 days)
- **Raw session files**: Managed by OpenClaw's session compression (`.jsonl` → `.jsonl.gz` after 3 days)

## Files

| File | Purpose |
|------|---------|
| `scripts/parse.py` | Direct parser (no database) — recommended for cron jobs |
| `scripts/ingest.py` | Incremental ingestion into SQLite |
| `scripts/report.py` | SQLite-based daily/weekly/monthly reports |
| `scripts/pricing.json` | Model pricing configuration |
| `scripts/usage.db` | SQLite database (created at init) |

## Limitations

- Only parses assistant messages with `usage` fields (OpenClaw 2026.5+ format)
- Historical sessions before JSONL format not supported
- Costs are estimates; actual billing may differ
- Cron job paths must be configured to match your installation directory
