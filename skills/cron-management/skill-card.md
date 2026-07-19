# cron-management — Skill Card

Quick reference for the cron-management skill.

## Commands

| Command | Description |
|---------|-------------|
| `cronctl list` | List all jobs with status (✅/❌) |
| `cronctl show <name>` | Show detailed job info (JSON) |
| `cronctl pause <name>` | Disable a single job |
| `cronctl resume <name>` | Re-enable a single job |
| `cronctl pause-all` | Disable ALL jobs |
| `cronctl resume-all` | Re-enable ALL jobs |
| `cronctl maintenance on` | Enable maintenance mode (emergency stop) |
| `cronctl maintenance off` | Disable maintenance mode |
| `cronctl status` | Health dashboard |
| `cronctl health <name>` | Show run history and diagnostics |

## Maintenance Mode

Emergency stop that works even if OpenClaw is down:

```bash
cronctl maintenance on   # Creates /tmp/cron-paused
cronctl maintenance off  # Removes it
```

Jobs should check for this flag at startup:

```bash
if [ -f /tmp/cron-paused ]; then
  echo "$(date -Iseconds) — job skipped (maintenance)" >> /tmp/cron-skipped.log
  exit 0
fi
```

## Examples

```bash
# Quick status overview
cronctl status

# Pause one job for debugging
cronctl pause cloudy-blog-writer

# Emergency stop everything
cronctl maintenance on

# Check why a job keeps failing
cronctl health beads-executor
```

## Files

- `skills/cron-management/SKILL.md` — Full documentation
- `skills/cron-management/scripts/cronctl.sh` — Main CLI script
