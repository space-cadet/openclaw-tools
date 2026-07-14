# openclaw-backup-optimized — Skill Card

| Field | Value |
|-------|-------|
| **Name** | openclaw-backup-optimized |
| **Version** | 1.0.1 |
| **One-liner** | Full snapshots with workspace splitting, change summaries, and restore instructions. |

## Trigger
- "Set up optimized OpenClaw backups"
- "Backup with change tracking"
- "Split large workspace into parts"
- "Backup with Discord notification"

## Key Commands

```bash
# Install script
cp scripts/backup.js ~/.openclaw/workspace/tools/openclaw-backup.js

# Configure environment
export OPENCLAW_HOME="$HOME/.openclaw"
export OPENCLAW_BACKUP_DIR="$HOME/.openclaw-backup"
export BACKUP_REPO_URL="https://github.com/your/repo.git"
export BACKUP_CHANNEL_ID="1234567890"  # optional, for Discord
export BACKUP_TZ="UTC"
export BACKUP_MAX_HISTORY=7

# Run backup
node ~/.openclaw/workspace/tools/openclaw-backup.js
```

## Dependencies
- Node.js >= 18
- git
- tar

## Quick Example

```bash
# Cron schedule (adjust times as needed)
openclaw cron add --name "openclaw-backup-daily" \
  --cron "0 5,10,15,20 * * *" --tz "UTC" \
  --exec "node ~/.openclaw/workspace/tools/openclaw-backup.js"
```

> Uses workspace hash to skip unchanged archives. Excludes session locks and deleted files for smaller diffs. Force-pushes to backup repo — use a dedicated backup repository.
