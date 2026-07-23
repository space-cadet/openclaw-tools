# Active Context: openclaw-tools

## Current Status: Token-Usage Multi-Source Pricing (2026-07-23)

### What Just Happened
- **Built `update-pricing.py`**: Multi-source pricing fetcher for model cost tracking
  - Fetches **342 models** from OpenRouter API (`/api/v1/models`)
  - Scrapes **Moonshot direct pricing** from official docs (CNY→USD at ~7.2 rate)
  - Creates `registry.json` with model metadata: availability, provider, context windows, alternative pricing
  - Compares sources: OpenRouter vs direct (e.g., K3: $2.78/M vs $3.00/M — ~8% markup)
- **Fixed `parse.py` bug**: None cache pricing caused TypeError in cost estimation
- **Updated weekly cron**: Token Usage — Weekly Report now refreshes pricing before generating report
- **ClawHub published**: v2.2.4 live (latest tag, 307 downloads) — multi-source pricing with OpenRouter + Moonshot direct
- **Committed**: `37f65af` on main

### Previous Major Work (2026-07-21)
- **Documented `agent-knowledge` ClawHub skill**: Created `skills/knowledge/SKILL.md` with usage docs, data model, and QMD integration
- **Updated README.md**: Added `knowledge` *(ClawHub)* to the skills index under Memory & Knowledge Management

### Previous Major Work (2026-07-20)
- **Created `cron-management` skill** — CLI tool for managing OpenClaw cron jobs

### Next Focus
- T2: Benchmark verification (tests moved, not yet verified post-move)
- T5: Token usage tracking — Phase 6: ClawHub publish with pricing features

### Open Questions
- Should tests/ have their own memory-bank or use repo-level one?
- GitHub Actions CI — worth it for a tools repo?
