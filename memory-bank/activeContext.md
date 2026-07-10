# Active Context: openclaw-tools

## What We're Doing
Reorganizing `openclaw-tests` into `openclaw-tools`: a public repo for shareable OpenClaw skills, scripts, and utilities.

## Current Focus
Repo infrastructure: memory-bank setup, README, and reorganization plan.

## Immediate Next Steps
1. Write top-level README.md
2. Move existing content into `tests/` directory
3. Start migrating sanitized skills (batch by batch)
4. Start migrating sanitized scripts

## Open Questions
- Should we keep `kimi-desktop-gateway-policy`? (Very Kimi-specific)
- Should we create a `skills-registry.json` for discoverability?
- Should benchmarks keep their own memory-bank or use the repo-level one?

## Decisions Made
- ✅ Repo renamed from `openclaw-tests` → `openclaw-tools`
- ✅ Public visibility (for sharing)
- ✅ Memory-bank v6.12 initialized for project tracking
- ✅ Skills will be sanitized before migration (no personal refs, no secrets)
- ✅ `pass-secrets` will be included (sanitized) — low security risk
- ✅ Scripts with personal refs (`sage-`, `cloudy-`, `fix-*`) stay in private workspace
