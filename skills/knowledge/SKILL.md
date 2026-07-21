---
name: knowledge
description: "Unified knowledge capture and retrieval for URLs, video/article/paper extracts, social posts, and agent research outputs. Use when saving anything worth re-finding later, summarizing external content, tracking sourced claims, or answering 'where did we store that?' questions."
metadata:
  openclaw:
    emoji: "📚"
    requires:
      bins: []
    install: ["clawhub install knowledge"]
  version: "1.0.0"
  origin: "ClawHub (ianderrington/agent-knowledge)"
  clawhub_url: "https://clawhub.ai/ianderrington/agent-knowledge"
---

# Knowledge Skill

File-based knowledge organization. Capture fast, search later, clean up automatically.

## Purpose

Provides a unified system for capturing and retrieving:
- URLs and bookmarks
- Video/article/paper extracts
- Social posts (tweets, threads)
- Agent-generated research outputs

## Trigger

Use this skill when:
- Saving something worth re-finding later
- Summarizing external content
- Tracking sourced claims
- Answering "where did we store that?"

## Installation

```bash
clawhub install knowledge
```

This installs `scripts/know` — add to PATH or use full path:
```bash
~/.openclaw/skills/knowledge/scripts/know
```

## Storage Location

Default: `~/.soulshare/agent/knowledge/`

Configurable via `~/.config/know/config` or env `KNOWLEDGE_DIR`.

```
knowledge/
├── INDEX.md      # Auto-maintained browsable index
├── urls/         # Bookmarked URLs
├── extracts/     # Video/article/paper summaries
├── posts/        # Social content (tweets, threads)
└── research/     # Agent-generated research
```

## Usage

### Adding Content

```bash
know add url <url> --title "..." --tags "a,b" [--summary "..."]
know add video <url> --title "..." --tags "a,b" [--summary "..."]
know add extract --source <url> --type video|article|paper --title "..." --tags "a,b"
know add post --source <url> --title "..." --tags "a,b"
know add research --title "..." --tags "a,b" [--summary "..."]
```

Each add writes a markdown file with YAML frontmatter and updates `INDEX.md`.

### Searching

```bash
know search "query"           # Grep across all entries
know recent --limit 10        # Recent entries
know list --tags security     # Filter by tag
```

### Cleanup & Maintenance

```bash
know tidy                     # Audit: find issues
know tidy --fix               # Auto-fix: normalize tags, move misplaced files, remove empty
know validate                 # Check frontmatter schema
know reindex                  # Rebuild INDEX.md
know config                   # Show active config paths
```

**Recommended:** Run `know tidy --fix` in heartbeats or nightly cron.

## Data Model (frontmatter)

```yaml
---
type: url|extract|post|research
title: "Entry title"
source_url: "https://..."
source_kind: url|video|article|paper|post|research
tags: ["tag1", "tag2"]
added: "2026-02-26"
added_by: "agent-name"
summary: "One-line summary"
---
```

## QMD Integration

Plain markdown → QMD-indexable.

```bash
qmd collection add ~/.soulshare/agent/knowledge --name knowledge
qmd search "query" --collection knowledge
```

## Discipline

- If it's useful later → `know add` immediately
- Don't leave knowledge only in session memory files
- Every entry needs tags + summary
- Let `know tidy --fix` handle normalization

## References

- [ClawHub skill page](https://clawhub.ai/ianderrington/agent-knowledge)
- [graph-memory](../graph-memory/SKILL.md) — complementary knowledge graph querying
