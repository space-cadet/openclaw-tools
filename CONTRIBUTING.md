# Contributing to OpenClaw Tools

Thanks for contributing. This repo is public and shareable — keep it clean.

---

## Quick Start

1. Fork → feature branch → PR
2. Sanitize everything (see checklist below)
3. One skill or script per PR
4. Squash merge on approval

---

## 1. Contributing a New Skill

### Directory Structure

```
skills/<skill-name>/
├── SKILL.md              # Required. Usage, triggers, workflow
├── scripts/              # Optional. Executable helpers
│   └── *.sh, *.py
├── references/           # Optional. Docs, specs, upstream links
│   └── *.md
└── (no nested git repos) # Submodules by exception only
```

### SKILL.md Format

Front matter (YAML) is required:

```yaml
---
name: <skill-name>
description: "One-line trigger description. Use when..."
metadata:
  openclaw:
    emoji: "🔧"           # Optional. Visual hint in indexes
    requires:
      bins: ["python3"]   # Optional. External dependencies
    install: []           # Optional. Setup steps
---
```

Body sections (use what applies):

| Section | Purpose |
|---------|---------|
| `## Purpose` or `## Overview` | What this skill does |
| `## When to Use` / `## Trigger` | How the agent knows to invoke it |
| `## Usage` | Commands, examples, copy-paste snippets |
| `## Architecture` | Flow diagrams or file relationships |
| `## Files` | List of files and their roles |
| `## Dependencies` | What's required to run |
| `## Anti-Patterns` | What NOT to do |
| `## References` | Links to related skills or docs |

Keep it practical. Agents read this under time pressure. Bullet lists > paragraphs. Code blocks > prose.

---

## 2. Contributing a Script

### Header Comment Standards

Every script must start with a descriptive header:

**Shell:**
```bash
#!/bin/bash
# <One-line purpose>
# Usage: script.sh <arg> [options...]
# Dependencies: jq, curl
```

**Python:**
```python
#!/usr/bin/env python3
"""<One-line purpose>

Usage:
    script.py <arg> [--flag]

Dependencies: requests, pydantic
"""
```

### Rules

- **No hardcoded paths** — use `$HOME`, `~`, or accept paths as arguments
- **No hardcoded secrets** — read from env vars or config files
- **Fail fast** — `set -euo pipefail` for bash; explicit error handling for Python
- **Self-documenting** — `--help` flag or usage print on bad args
- **POSIX-friendly** — avoid bashisms if the script might run on macOS/BSD

---

## 3. Contributing to Tests / Benchmarks

```
tests/
├── <suite-name>/
│   ├── README.md           # What this suite tests, how to run it
│   ├── run_test.py         # Entry point (or run.sh)
│   ├── harness.sh          # Optional. Shared test utilities
│   ├── test-*.json         # Test definitions
│   └── results/            # Gitignored. Generated on run
```

### Test Definition (JSON)

```json
{
  "test_id": "sa-01",
  "test_name": "Basic subagent spawn",
  "description": "Verify subagent can be spawned and returns result",
  "timeout_seconds": 60,
  "expected": {
    "status": "completed",
    "output_contains": "done"
  }
}
```

### Benchmarks

- Include a `reference_interpreter.py` or equivalent baseline
- Document model version, date, and hardware in results
- Store raw outputs in `results/` (gitignored), commit summaries only

---

## 4. Sanitization Checklist

**Check every file before committing.** This repo is public.

| Check | What to Remove | Replace With |
|-------|---------------|--------------|
| **Personal names** | "Sage", "Deepak", "Cloudy", "Alice" | Generic: "the user", "the agent", "your-username" |
| **Specific paths** | `/Users/sage/`, `/home/deepak/`, `/Users/cloudy/.openclaw/` | `$HOME`, `~`, `~/.openclaw/`, or placeholders |
| **Secrets** | API keys, tokens, passwords, GPG key IDs | `YOUR_API_KEY_HERE`, env var references |
| **Chat IDs / phone numbers** | Telegram chat IDs, phone numbers | `YOUR_CHAT_ID` or generic description |
| **Domain names** | `quantumofgravity.com`, personal subdomains | `your-domain.com` or omit unless skill-specific |
| **Service references** | "my Telegram bot", "my Kimi gateway" | Generic: "the configured Telegram bot" |

### Quick Scan Commands

```bash
# Find potential personal refs
grep -riE "(sage|deepak|cloudy|quantumofgravity)" skills/ scripts/ tests/

# Find potential secrets
grep -riE "(api.?key|token|password|secret)" skills/ scripts/ tests/ | grep -v "YOUR_"

# Find hardcoded home paths
grep -riE "/(Users|home)/[a-z]+" skills/ scripts/ tests/ | grep -v '\$HOME\|~'
```

> **Golden rule:** If you wouldn't paste it in a public Slack channel, don't commit it.

---

## 5. Git Workflow

### Branch Naming

```
feat/<skill-name>       # New skill
fix/<skill-name>        # Bug fix in existing skill
docs/<skill-name>       # Documentation update
test/<suite-name>       # New test or benchmark
script/<script-name>    # New standalone script
```

### Commits

- Use conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
- One logical change per commit
- Reference issue numbers if applicable: `feat(token-usage): add cost estimation — closes #12`

### PR Process

1. Open PR from feature branch to `main`
2. Fill the PR template (if present) or include:
   - What changed
   - Why it changed
   - Tested how
3. Request review
4. **Squash merge** on approval — keeps history linear

### Semantic Versioning for Skills

Skills are versioned independently. Track in `SKILL.md` front matter or a `CHANGELOG.md` in the skill directory.

| Version | Change Type |
|---------|-------------|
| `x.y.z` | Patch: bug fix, docs tweak |
| `x.y.0` | Minor: new feature, backward compatible |
| `x.0.0` | Major: breaking change, workflow change |

Example:
```yaml
metadata:
  version: "1.2.0"
  changelog:
    - "1.2.0: Added --json output flag"
    - "1.1.0: Added page selection"
    - "1.0.0: Initial release"
```

---

## 6. Skill Template

Copy this to `skills/<your-skill>/SKILL.md`:

```markdown
---
name: <skill-name>
description: "Short trigger description. Use when..."
metadata:
  openclaw:
    emoji: "🔧"
    requires:
      bins: []
    install: []
  version: "1.0.0"
---

# <Skill Name>

## Purpose

What this skill does and why it exists.

## Trigger

When should the agent use this skill? List specific user queries or situations.

## Usage

```bash
# Example command
your-script.sh --flag value
```

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | This file |
| `scripts/your-script.sh` | Main executable |

## Dependencies

- `tool-name` — install via `apt`, `pip`, `npm`, etc.

## Anti-Patterns

- DON'T do X
- DON'T do Y

## References

- [Related Skill](../other-skill/SKILL.md)
- [Upstream Docs](https://example.com/docs)
```

---

## Questions?

Open an issue or PR. This is a community repo — keep it useful, keep it clean.
