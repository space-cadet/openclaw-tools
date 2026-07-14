# openclaw-backup — Skill Card

| Field | Value |
|-------|-------|
| **Name** | openclaw-backup |
| **Version** | 1.0.0 |
| **One-liner** | Backup and restore OpenClaw data with automatic rotation. |

## Trigger
- "Create a backup"
- "Restore my OpenClaw data"
- "Set up automatic backups"
- "How do I backup my workspace?"

## Key Commands

```bash
# Create backup (default: ~/openclaw-backups/)
./scripts/backup.sh

# Create backup to custom directory
./scripts/backup.sh /path/to/backups

# Restore from backup
openclaw gateway stop
mv ~/.openclaw ~/.openclaw-old
tar -xzf ~/openclaw-backups/openclaw-YYYY-MM-DD_HHMM.tar.gz -C ~
openclaw gateway start
```

## Dependencies
- bash
- tar

## Quick Example

```bash
# Daily backup via cron
0 3 * * * /path/to/scripts/backup.sh ~/openclaw-backups
```

> Backup archives may contain credentials and session data. Store securely and avoid sharing.
