# Project Brief: openclaw-tools

## Vision
A public, shareable repository of OpenClaw skills, scripts, benchmarks, and utilities that any AI agent workspace can adopt.

## Scope
- **Skills**: Sanitized, reusable OpenClaw skills (SKILL.md + scripts)
- **Scripts**: Generic shell/Python scripts for AI agent workspaces
- **Tests**: Benchmarks and test harnesses for OpenClaw capabilities
- **Docs**: Documentation on how to use, contribute, and extend

## What This Is NOT
- NOT a personal workspace (that's `sage-workspace`)
- NOT a place for secrets, API keys, or personal configuration
- NOT a project-specific repo (physics, etc. stay elsewhere)

## Target Audience
- OpenClaw users who want pre-built skills
- AI agent developers building similar workspace tooling
- Contributors who want to share their own skills/scripts

## Current Status
- Renamed from `openclaw-tests` (2026-07-10)
- Contains legacy benchmark content that needs reorganizing
- Memory bank initialized

## Key Principles
1. **Sanitized**: No personal references, no specific paths, no secrets
2. **Documented**: Every skill/script has a README or SKILL.md
3. **Tested**: Scripts work out of the box (with sensible defaults)
4. **Versioned**: Skills have versions, changelogs

## Structure
```
openclaw-tools/
├── skills/           # Shareable skills (sanitized)
├── scripts/          # Generic scripts (sanitized)
├── tests/            # Benchmarks and test harnesses
├── docs/             # Documentation, CONTRIBUTING.md
├── memory-bank/      # Project tracking (this repo's meta)
└── README.md
```
