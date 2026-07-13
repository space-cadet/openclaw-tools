#!/bin/bash
# Disk usage monitor
# Alerts when disk usage exceeds a threshold
#
# Usage: check-disk.sh [THRESHOLD]
#   THRESHOLD: Percentage threshold (default: 85)
#
# Environment:
#   DISK_THRESHOLD — override default threshold

THRESHOLD="${1:-${DISK_THRESHOLD:-85}}"

USAGE=$(df -h / | awk 'NR==2 {gsub(/%/,""); print $5}')

if [ "$USAGE" -gt "$THRESHOLD" ]; then
    echo "⚠️ DISK WARNING: ${USAGE}% used on root partition (threshold: ${THRESHOLD}%)"
    echo "Run: sudo journalctl --vacuum-size=100M"
    echo "Run: sudo apt autoremove && sudo apt clean"
else
    echo "✅ Disk usage: ${USAGE}% (threshold: ${THRESHOLD}%)"
fi
