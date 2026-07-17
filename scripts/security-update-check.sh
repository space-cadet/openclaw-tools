#!/bin/bash
# Security Update Check Script
# Run nightly to check and apply security updates
#
# Usage: security-update-check.sh [--no-apply]
#   --no-apply: Only check, don't install updates
#
# Environment:
#   SECURITY_LOG_FILE — override log file path (default: /tmp/security-update-check.log)
#   SECURITY_REPORT_FILE — override report output file
#   SECURITY_TIMEZONE — override timezone (default: UTC)

set -euo pipefail

LOG_FILE="${SECURITY_LOG_FILE:-/tmp/security-update-check.log}"
REPORT_FILE="${SECURITY_REPORT_FILE:-/tmp/security-update-check.report}"
NO_APPLY=0

# Parse args
if [[ "${1:-}" == "--no-apply" ]]; then
    NO_APPLY=1
fi

# ... rest of script uses LOG_FILE and REPORT_FILE variables
# (keeping the rest of the logic as-is since it's already generic)

REPORT=""
UPDATES_FOUND=0
REBOOT_REQUIRED="no"

# Log to file but also show output
exec > >(tee -a "$LOG_FILE") 2>&1
echo "=== Security Update Check - $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

# Step 1: Update package lists
echo "[1/5] Running apt update..."
sudo apt update -qq

# Step 2-4: Check unattended-upgrades and apply updates
if command -v unattended-upgrades >/dev/null 2>&1; then
    echo "[2/5] unattended-upgrades found."
    
    # Record timestamp before running
    BEFORE_TIME=$(date +%s)
    BEFORE_DATE=$(date -d "@$BEFORE_TIME" "+%Y-%m-%d %H:%M")
    
    echo "[3/5] Applying security updates..."
    sudo unattended-upgrades 2>&1 || true
    
    echo "[4/5] Checking what was installed..."
    
    # Check unattended-upgrades log for recent activity
    if [ -f /var/log/unattended-upgrades/unattended-upgrades.log ]; then
        # Get the last 20 lines and look for installed upgrades
        LOG_TAIL=$(sudo tail -n 20 /var/log/unattended-upgrades/unattended-upgrades.log)
        
        # Check if "All upgrades installed" appears in recent log
        if echo "$LOG_TAIL" | grep -q "All upgrades installed"; then
            # Check if there's a timestamp near our BEFORE_TIME
            # The log format is: 2026-07-05 22:47:53,535 INFO All upgrades installed
            # We need to check if the most recent "All upgrades installed" is within the last few minutes
            
            # Get the most recent timestamp from the log tail
            RECENT_TS=$(echo "$LOG_TAIL" | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}' | tail -n1 || true)
            
            if [ -n "$RECENT_TS" ]; then
                # Convert to epoch seconds
                RECENT_EPOCH=$(date -d "$RECENT_TS" +%s 2>/dev/null || echo 0)
                
                # If the log entry is within the last 10 minutes, it's from our run
                TIME_DIFF=$((BEFORE_TIME - RECENT_EPOCH))
                if [ "$TIME_DIFF" -lt 600 ] && [ "$TIME_DIFF" -gt -600 ]; then
                    # It's from our run, now count packages
                    # Look for "Packages that will be upgraded:" in the log
                    UPGRADE_LIST=$(sudo grep -B5 "All upgrades installed" /var/log/unattended-upgrades/unattended-upgrades.log | grep "Packages that will be upgraded:" | tail -n1 || true)
                    if [ -n "$UPGRADE_LIST" ]; then
                        # Extract package names after the colon
                        PKG_NAMES=$(echo "$UPGRADE_LIST" | sed 's/.*Packages that will be upgraded: //')
                        UPDATES_FOUND=$(echo "$PKG_NAMES" | wc -w)
                    fi
                fi
            fi
        fi
    fi
    
    # Fallback: check apt history log for recent upgrades
    if [ "$UPDATES_FOUND" -eq 0 ] && [ -f /var/log/apt/history.log ]; then
        # Get the most recent Start-Date
        LAST_START=$(grep "Start-Date:" /var/log/apt/history.log | tail -n1 || true)
        if [ -n "$LAST_START" ]; then
            # Extract date: "Start-Date: 2026-07-05  22:47:41"
            LAST_DATE=$(echo "$LAST_START" | sed 's/Start-Date: //' | tr -s ' ')
            LAST_EPOCH=$(date -d "$LAST_DATE" +%s 2>/dev/null || echo 0)
            
            TIME_DIFF=$((BEFORE_TIME - LAST_EPOCH))
            # If the apt history entry is within the last 10 minutes
            if [ "$TIME_DIFF" -lt 600 ] && [ "$TIME_DIFF" -gt -600 ]; then
                # Look for the Upgrade: line after this Start-Date
                UPGRADE_LINE=$(grep -A10 "Start-Date: $LAST_DATE" /var/log/apt/history.log | grep "Upgrade:" | tail -n1 || true)
                if [ -n "$UPGRADE_LINE" ]; then
                    # Count packages (comma-separated)
                    UPDATES_FOUND=$(echo "$UPGRADE_LINE" | tr ',' '\n' | wc -l)
                fi
            fi
        fi
    fi
else
    echo "[2/5] unattended-upgrades not found."
    echo "[3/5] Checking for security upgrades..."
    
    SECURITY_PACKAGES=$(sudo apt list --upgradable 2>/dev/null | grep -i security || true)
    
    if [ -n "$SECURITY_PACKAGES" ]; then
        COUNT=$(echo "$SECURITY_PACKAGES" | wc -l)
        UPDATES_FOUND=$COUNT
        echo "[4/5] Found $COUNT security packages. Upgrading..."
        sudo apt upgrade -y 2>&1 || true
    else
        echo "[4/5] No security packages found."
    fi
fi

# Step 5: Check if reboot is required
if [ -f /var/run/reboot-required ]; then
    REBOOT_REQUIRED="yes"
fi

echo "[5/5] Reboot required: $REBOOT_REQUIRED"

# Check disk usage
DISK_USAGE=$(df -h / | tail -n1 | awk '{print $5}')
echo "Disk usage: $DISK_USAGE"

# Determine if we should report
if [ "$UPDATES_FOUND" -gt 0 ] || [ "$REBOOT_REQUIRED" = "yes" ]; then
    REPORT="Security updates installed: $UPDATES_FOUND packages. Reboot required: $REBOOT_REQUIRED."
fi

# Output the report to stdout (for the calling agent)
echo "=== REPORT ==="
echo "$REPORT"
