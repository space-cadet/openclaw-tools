# token-usage — Skill Card

| Field | Value |
|-------|-------|
| **Name** | token-usage |
| **Version** | — |
| **One-liner** | Track, aggregate, and report OpenClaw token usage and costs across sessions. |

## Trigger
- "How many tokens did I use today/this week?"
- "What's my session cost?"
- Budget monitoring or anomaly detection

## Key Commands

```bash
# Today's usage
python3 scripts/parse.py --today

# Weekly report with costs
python3 scripts/parse.py --week --costs

# Weekly cron report (JSON)
python3 scripts/parse.py --week --by-cron --costs --json

# All-time by model
python3 scripts/parse.py --all --by-model

# Export to JSON
python3 scripts/parse.py --week --json > /tmp/token-report.json
```

## Dependencies
- Python 3
- OpenClaw session JSONL files in `~/.openclaw/agents/*/sessions/`
- `scripts/pricing.json` (user-editable)

## Quick Example

```bash
python3 ~/.openclaw/skills/token-usage/scripts/parse.py --week --costs
```

> Important: The script sums `input + output` tokens only. `totalTokens` includes `cacheRead` which would overcount if summed across messages.
