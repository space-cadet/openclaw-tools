# pass-secrets — Skill Card

| Field | Value |
|-------|-------|
| **Name** | pass-secrets |
| **Version** | — |
| **One-liner** | Store and retrieve secrets using pass (password-store) with GPG encryption. |

## Trigger
- "Store this API key securely"
- "What's my API key for X?"
- Any secret storage/retrieval request

## Key Commands

```bash
# Store a secret
pass insert -m path/to/secret
# Type value, press Ctrl+D

# Retrieve
pass show path/to/secret

# List all secrets
pass ls

# Remove
pass rm path/to/secret
```

## Dependencies
- `pass` (password-store)
- GPG key initialized
- Store at `~/.password-store/`

## Quick Example

```bash
# Store Kimi API key
pass insert -m api/kimi
# → paste key, Ctrl+D

# Retrieve
pass show api/kimi
```

> Secrets are GPG-encrypted at rest. Back up `~/.password-store/` and `~/.gnupg/` separately.
