#### 11:02 IST - T5: Multi-source pricing updater + model registry

**Actions:**
- Created `update-pricing.py` — fetches model pricing from OpenRouter API (342 models) and Moonshot direct docs
- Created `registry.json` — model metadata with availability, provider, context windows, alternative pricing
- Fixed `parse.py` None cache pricing bug (TypeError in estimate_cost)
- Updated weekly cron to refresh pricing before report generation
- Updated `pricing.json` with Moonshot-direct rates (CNY→USD conversion at 7.2)

**Key findings:**
| Model | Moonshot Direct | OpenRouter | Diff |
|-------|----------------|------------|------|
| K2.6 | $0.90/M | $0.68/M | OR cheaper |
| K2.7 | $0.90/M | — | — |
| K2.7-code | $0.90/M | $0.82/M | +9% |
| K3 | $2.78/M | $3.00/M | +8% |

**Files modified:**
- `skills/token-usage/scripts/update-pricing.py` (new)
- `skills/token-usage/scripts/registry.json` (new)
- `skills/token-usage/scripts/parse.py` (bugfix)
- `skills/token-usage/scripts/pricing.json` (updated)

**Commit:** `37f65af`
