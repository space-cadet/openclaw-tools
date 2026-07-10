# Token Usage Tracker

Track, aggregate, and report OpenClaw token usage and costs across sessions.

## Features

- Parse session JSONL files to extract per-message token usage
- Aggregate by date, model, or cron job
- Cost estimation with configurable pricing
- JSON export for dashboards
- Handles cacheRead correctly (excludes from totals)

## Usage

```bash
# Daily report
python3 scripts/parse.py --today

# Weekly report with costs
python3 scripts/parse.py --week --costs

# Per-cron-job breakdown
python3 scripts/parse.py --week --by-cron

# All-time by model
python3 scripts/parse.py --all --by-model

# JSON export
python3 scripts/parse.py --week --json
```

## Files

- `SKILL.md` — Skill definition
- `scripts/parse.py` — Python parser
- `scripts/pricing.json` — Model pricing (user-editable)
