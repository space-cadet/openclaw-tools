---
name: bookmarks
description: "Save, list, search, and manage Telegram message bookmarks via /save commands."
---

# Bookmarks Skill

Triggered by `/save ...` messages or bookmark-related requests.

## Commands

All bookmark operations use a single Telegram command with sub-parameters:

| `/save help` | `handler.py help` | Show command usage |
| `/save show #` | `handler.py show <id>` | Display specific bookmark |
| `/save rm #` | `handler.py rm <id>` | Remove a bookmark |

## Commands

All bookmark operations use a single Telegram command with sub-parameters:

| Input | Maps to | Action |
|-------|---------|--------|
| `/save` (as reply) | `bookmark.py save` | Save replied-to message |
| `/save <text>` | `bookmark.py save --content "text"` | Save inline text |
| `/save list [count]` | `bookmark.py list --count N` | List recent bookmarks |
| `/save search <query>` | `bookmark.py search "query"` | Search bookmarks |
| `/save show <#>` | `bookmark.py show <id>` | Show specific bookmark |
| `/save rm <#>` | `bookmark.py rm <id>` | Remove bookmark |
| `/save count` | `bookmark.py json \| jq length` | Count total bookmarks |
| `/save tags` | Parse tags from all entries | List unique tags |
| `/save help` | — | Show usage help |

## Scripts

- `scripts/bookmark.py` — CLI for save/list/search/json (workspace root)
- `scripts/handler.py` — Normalizes `/save ...` into bookmark.py calls

## Workflow

1. Detect `/save` message (standalone or reply).
2. **If replying to assistant message**: fetch full text from session history to avoid truncation, pass via `--full-content`.
3. Parse sub-command and arguments.
4. Run appropriate `bookmark.py` subcommand via exec.
5. Return formatted results to user.

## Save behavior

- **Reply to assistant message**: retrieve full response from session history, save complete text via `--full-content` override
- **Reply to user/other message**: capture the replied-to message text as content (may be truncated if long — recommend inline `/save <text>` for long messages)
- **Inline mode**: use the text after `/save` as content
- **Auto-tags**: extract from content using keyword heuristics
- **Manual tags**: user can append `#tag1 #tag2` to note

## Full-Content Retrieval

When replying `/save` to an assistant message, the skill retrieves the full assistant response from session history instead of using the truncated context snippet. This is done by:
1. Detecting `[reply target] assistant` in the context
2. Fetching session history via `sessions_history`
3. Matching the assistant message by its truncated prefix
4. Passing the full text via `handler.py save-reply --full-content "..."`

This ensures long assistant responses are saved completely, not cut off at the truncation boundary.

## Storage

- `memory/bookmarks.md` — append-only markdown log
- Entry format: `## Bookmark #N — ISO timestamp` with metadata fields
