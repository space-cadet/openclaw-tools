# Active Context: openclaw-tools

## What We're Doing
Reorganizing `openclaw-tests` into `openclaw-tools`: a public repo for shareable OpenClaw skills, scripts, and utilities.

## Current Focus
All Batch 1 and Batch 2 skills migrated to openclaw-tools. Ready for scripts migration and README.

## Immediate Next Steps (Next Session)
1. Migrate generic scripts (git-guardian.sh, daily-backup.sh, heartbeat-*.sh)
2. Write top-level README.md with skill index
3. Set up token usage tracking system (T5)

## Open Questions
- Should we create a `skills-registry.json` for discoverability? → **Decide next session**
- Should benchmarks keep their own memory-bank or use repo-level one? → **Decide next session**

## Decisions Made (This Session)
- ✅ Repo renamed from `openclaw-tests` → `openclaw-tools`
- ✅ Public visibility (for sharing)
- ✅ Memory-bank v6.12 initialized for project tracking
- ✅ 14 original skills migrated, 3 ClawHub skills removed, 4 Kimi-specific skipped
- ✅ Telegram rich messages enabled
- ✅ Sanitization approach: replace personal names with "User", specific paths with `/path/to/...` or generic examples

## Decisions Made
- ✅ Repo renamed from `openclaw-tests` → `openclaw-tools`
- ✅ Public visibility (for sharing)
- ✅ Memory-bank v6.12 initialized for project tracking
- ✅ Skills will be sanitized before migration (no personal refs, no secrets)
- ✅ `pass-secrets` will be included (sanitized) — low security risk
- ✅ Scripts with personal refs (`sage-`, `cloudy-`, `fix-*`) stay in private workspace
