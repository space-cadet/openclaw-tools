# cloakbrowser-stealth — Skill Card

| Field | Value |
|-------|-------|
| **Name** | cloakbrowser-stealth |
| **Version** | — |
| **One-liner** | Stealth browser automation to bypass bot detection on protected sites. |

## Trigger
- `web_fetch` fails with 403, CAPTCHA, or access denied
- Need to scrape reviews, protected pages, or anti-bot sites
- "This site blocks bots"

## Key Commands

```bash
# Basic fetch
python3 scripts/fetch.py "https://example.com" --wait-ms 3000

# Extract specific elements
python3 fetch.py "URL" --selector "[data-testid='review-title']" --output text

# Full page + screenshot
python3 fetch.py "URL" --wait-ms 4000 --screenshot /tmp/page.png --output json

# Humanize for aggressive detection
python3 fetch.py "URL" --humanize --wait-ms 5000
```

## Dependencies
- Python 3, CloakBrowser (`pip install cloakbrowser`)
- `~/.venv/cloakbrowser` (pre-installed on VPS)

## Quick Example

```bash
cd skills/cloakbrowser-stealth/scripts
python3 fetch.py "https://trustpilot.com/review/example.com" --wait-ms 3000 --output json
```

> ❌ Don't use for: login-required sites, interactive CAPTCHAs, or IP-reputation blocks.
