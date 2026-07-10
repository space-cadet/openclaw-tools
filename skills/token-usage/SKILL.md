---
name: token-usage
description: "Track, aggregate, and report OpenClaw token usage and costs across sessions."
homepage: https://github.com/space-cadet/openclaw-token-usage
license: MIT
---

# Token Usage Tracker

Parse OpenClaw session JSONL files to extract token usage, aggregate by date/model/session, and generate cost reports.

## When to Use

- User asks "how many tokens did I use today/this week"
- User wants to know session costs or model breakdown
- Budget monitoring and anomaly detection
- Before/after optimization comparisons

## Workflow

1. **Locate sessions** — Find `.jsonl` files in `~/.openclaw/agents/*/sessions/`
2. **Parse usage** — Extract `input`, `output`, `cacheRead`, `cacheWrite`, `totalTokens` from each assistant message
3. **Aggregate** — Group by date, model, session ID
4. **Report** — Output summaries, trends, cost estimates

## Commands

### Parse and aggregate current sessions
```bash
python3 ~/.openclaw/skills/token-usage/scripts/parse.py --today
```

### Weekly report with cost estimates
```bash
python3 ~/.openclaw/skills/token-usage/scripts/parse.py --week --costs
```

### Report by cron job (daily breakdown per job)
```bash
python3 ~/.openclaw/skills/token-usage/scripts/parse.py --week --by-cron
```

### Weekly cron report with costs (JSON output)
```bash
python3 ~/.openclaw/skills/token-usage/scripts/parse.py --week --by-cron --costs --json
```

### All-time summary by model
```bash
python3 ~/.openclaw/skills/token-usage/scripts/parse.py --all --by-model
```

### Export to JSON for external dashboards
```bash
python3 ~/.openclaw/skills/token-usage/scripts/parse.py --week --json > /tmp/token-report.json
```

## Data Format

Sessions are stored as JSONL with lines like:
```json
{"type":"message","message":{"role":"assistant",...},"usage":{"input":1000,"output":500,"totalTokens":1500},...}
```

## Cost Estimation

Uses model pricing from `scripts/pricing.json` (user-editable). Default prices:
- Kimi k2.7: $0.50/1M input, $2.00/1M output
- Claude Sonnet 4: $3.00/1M input, $15.00/1M output
- GPT-4o: $2.50/1M input, $10.00/1M output

Costs are approximate. Cache read/write pricing applied when available.

## Important: What "Total" Means

The script reports **input + output tokens** as the usage metric. This is the actual new token consumption per turn.

The `totalTokens` field in session files includes `cacheRead` (cached context window), which gets re-counted at every turn. Summing `totalTokens` across messages would massively overcount — a 10K context used for 100 turns would appear as 1M tokens. The script avoids this by only summing `input` and `output`.

## Output Locations

- Daily summaries: `~/.openclaw/skills/token-usage/logs/YYYY-MM-DD.md`
- Weekly reports: `~/.openclaw/skills/token-usage/logs/week-YYYY-Www.md`
- Raw JSON exports: user-specified or `/tmp/token-usage-*.json`

## Limitations

- Only parses assistant messages with `usage` fields (OpenClaw 2026.5+ format)
- Historical sessions before JSONL format not supported
- Costs are estimates; actual billing may differ
