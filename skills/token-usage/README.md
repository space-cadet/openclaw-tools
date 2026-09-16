# Token Usage Tracker

Parse OpenClaw and Codex session JSONL files to extract token usage, aggregate by date/model/session type, and generate cost reports across providers.

## When to Use

- User asks "how many tokens did I use today/this week"
- Budget monitoring and anomaly detection
- Before/after optimization comparisons
- Cron job: daily token report to Telegram

## Architecture

```
scripts/
  common.py    — Session discovery, parsing, model normalization, cost estimation
  ingest.py    — Incremental ingestion into SQLite (usage.db)
  report.py    — Report generation from SQLite
  pricing.json — Model pricing table (user-editable)
```

## Data Sources

| Source | Pattern | Classification |
|--------|---------|----------------|
| Interactive sessions | `*.jsonl`, `*.jsonl.gz` | `user` or `cron:<name>` |
| Zstd-compressed (post-9.4 cleanup) | `*.jsonl.deleted.*.zst` | `user` or `cron:<name>` |
| Codex app-server rollouts | `codex-home/sessions/**/*.jsonl` | `background:codex` |

## Key Behaviors

- **Session type separation**: Codex rollout logs (background agent jobs using GPT-5.6-Luna etc.) are classified as `background:codex`, NOT merged into user-facing reports. This prevents false "you used 12M Luna tokens" reports when the user was actually on Kimi.
- **Zstd support**: Post-9.4-upgrade sessions may be zstd-compressed as `.jsonl.deleted.*.zst`. These are discovered and decompressed transparently via the `zstd` CLI.
- **Defensive parsing**: Codex rollout records with `"info": null` are handled gracefully (Cloudy's fix — prevents `AttributeError` crash).
- **Incremental ingestion**: Only new/modified session files are processed. State tracked in `ingestion_log` table.

## Commands

```bash
# Ingest new sessions (run before reporting)
python3 scripts/ingest.py

# Generate reports
python3 scripts/report.py --today
python3 scripts/report.py --yesterday
python3 scripts/report.py --week
python3 scripts/report.py --month
python3 scripts/report.py --yesterday --compact   # Telegram-friendly
```

## Pricing

Edit `scripts/pricing.json` to add/update model pricing. Format:
```json
{
  "kimi/k2.7": {"input": 0.50, "output": 2.00, "cache_read": 0.10, "cache_write": 0.50},
  "openai/gpt-5.6-luna": {"input": 0.20, "output": 1.20, "cache_read": 0.02, "cache_write": 0}
}
```

Costs are estimates in USD per 1M tokens. Unknown models report without cost.

## Known Issues / History

| Date | Issue | Fix |
|------|-------|-----|
| 2026-09-16 | Parser missed zstd-compressed sessions (`.jsonl.deleted.*.zst`) → false "no activity since Aug 16" | Added `*.jsonl.*.zst` glob + `_zstd_open()` in `common.py` |
| 2026-09-16 | Codex rollout usage merged into user reports → false "12M Luna tokens" | Added `background:codex` classification in `ingest.py` |
| 2026-09-16 | `"info": null` in Codex records caused `AttributeError` | Defensive `(payload.get("info") or {})` pattern (Cloudy's fix) |

## Dependencies

- `zstd` CLI (for `.zst` decompression)
- Python 3.10+ (stdlib only — no pip installs needed)
