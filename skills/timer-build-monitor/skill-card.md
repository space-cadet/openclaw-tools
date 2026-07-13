# timer-build-monitor — Skill Card

| Field | Value |
|-------|-------|
| **Name** | timer-build-monitor |
| **Version** | — |
| **One-liner** | One-shot async timers for build monitoring and long-running tasks. |

## Trigger
- "Check build status in 20 minutes"
- "Remind me when X finishes"
- Any one-shot delayed check

## Key Commands

```bash
# Set a timer
$timer "check eas build in 20 minutes" --name eas-build-v018

# List active timers
$timer list

# Cancel a timer
$timer cancel eas-build-v018
```

## Architecture

```
User sets timer → Parse intent → Spawn subagent (isolated, timeout)
  → Subagent sleeps → Checks status → Reports back
  → Success: update state, notify user
  → Timeout: notify user "timer expired"
```

## Dependencies
- `scripts/timer.sh` (CLI wrapper)
- `scripts/state.sh` (JSON state in `~/.openclaw/timers/`)
- `sessions_spawn` with `mode="run"`

## Quick Example

```bash
$timer "check CI build in 15 minutes" --name ci-check-001
# Subagent sleeps 15 min, checks build, reports back
```

> Trade-off: Subagent pattern is simple but doesn't survive session restarts. For persistent timers, use OpenClaw native `cron` tool.
