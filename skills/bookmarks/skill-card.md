# bookmarks — Skill Card

| Field | Value |
|-------|-------|
| **Name** | bookmarks |
| **Version** | — |
| **One-liner** | Save, list, search, and manage Telegram message bookmarks via /save commands. |

## Trigger
- `/save` (as reply or inline)
- `/save list`, `/save search <query>`, `/save show #`, `/save rm #`
- Any bookmark-related request

## Key Commands

```bash
# Save a bookmark
python3 scripts/bookmark.py save --content "..." --tags "physics, qhe"

# List recent
python3 scripts/bookmark.py list --count 10

# Search
python3 scripts/bookmark.py search "black hole"
python3 scripts/bookmark.py search "#physics"

# Handler (normalizes /save commands)
python3 scripts/handler.py save-reply --full-content "..."
```

## Dependencies
- `scripts/bookmark.py` and `scripts/handler.py`
- `memory/bookmarks.md` (append-only markdown log)

## Quick Example

```bash
# Reply to a message with /save → handler fetches full text and appends to memory/bookmarks.md
python3 scripts/bookmark.py save --content "Eureka moment about braids" --tags "math, braids" --note "Check later"
```
