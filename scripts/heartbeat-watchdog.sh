#!/bin/bash
# Heartbeat Watchdog Script
# Checks for recent heartbeat failures and alerts if needed
#
# Usage: heartbeat-watchdog.sh [options]
# Options:
#   --memory-file PATH    Path to heartbeat failures JSON state file
#   --sessions-dir PATH   Path to OpenClaw sessions directory
#   --alert-log PATH      Path to alert log file
#
# Environment variables:
#   HEARTBEAT_MEMORY_FILE  Override default memory file path
#   HEARTBEAT_SESSIONS_DIR Override default sessions directory
#   HEARTBEAT_ALERT_LOG    Override default alert log path

set -euo pipefail

# ─── Configuration (override via env vars or CLI) ───────────────────────

MEMORY_FILE="${HEARTBEAT_MEMORY_FILE:-${HOME}/.openclaw/workspace/memory/heartbeat-failures.json}"
SESSIONS_DIR="${HEARTBEAT_SESSIONS_DIR:-${HOME}/.openclaw/agents/main/sessions}"
ALERT_LOG="${HEARTBEAT_ALERT_LOG:-${HOME}/.openclaw/workspace/memory/heartbeat-alerts.log}"

# Parse CLI args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --memory-file)
            MEMORY_FILE="$2"
            shift 2
            ;;
        --sessions-dir)
            SESSIONS_DIR="$2"
            shift 2
            ;;
        --alert-log)
            ALERT_LOG="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--memory-file PATH] [--sessions-dir PATH] [--alert-log PATH]"
            exit 1
            ;;
    esac
done

CURRENT_TIME=$(date -Iseconds)
CURRENT_EPOCH=$(date +%s)

# ─── State Management ───────────────────────────────────────────────────

# Ensure memory file exists
if [[ ! -f "$MEMORY_FILE" ]]; then
    mkdir -p "$(dirname "$MEMORY_FILE")"
    echo '{"consecutiveFailures":0,"lastFailureAt":null,"alertSentAt":null}' > "$MEMORY_FILE"
fi

# Read current state
STATE=$(cat "$MEMORY_FILE")
CONSECUTIVE_FAILURES=$(echo "$STATE" | grep -oP '"consecutiveFailures":\s*\K[0-9]+' || echo "0")
LAST_FAILURE_AT=$(echo "$STATE" | grep -oP '"lastFailureAt":\s*"\K[^"]*' || echo "null")
ALERT_SENT_AT=$(echo "$STATE" | grep -oP '"alertSentAt":\s*"\K[^"]*' || echo "null")

# ─── Session Analysis ───────────────────────────────────────────────────

# Find most recent heartbeat session
HEARTBEAT_SESSION=""
for f in $(ls -t "$SESSIONS_DIR"/*.jsonl 2>/dev/null | head -20); do
    if grep -q '"HEARTBEAT"' "$f" 2>/dev/null; then
        HEARTBEAT_SESSION="$f"
        break
    fi
done

# Check for failure patterns
FAILURE_FOUND=0
if [[ -n "$HEARTBEAT_SESSION" && -f "$HEARTBEAT_SESSION" ]]; then
    if grep -q '"high risk"\|"rejected because it was considered"' "$HEARTBEAT_SESSION" 2>/dev/null; then
        FAILURE_FOUND=1
    fi
fi

# ─── State Update & Alert Logic ─────────────────────────────────────────

if [[ "$FAILURE_FOUND" -eq 1 ]]; then
    CONSECUTIVE_FAILURES=$((CONSECUTIVE_FAILURES + 1))
    LAST_FAILURE_AT="$CURRENT_TIME"
    
    # Check if we should send alert
    SHOULD_ALERT=0
    if [[ "$CONSECUTIVE_FAILURES" -ge 2 ]]; then
        if [[ "$ALERT_SENT_AT" == "null" || -z "$ALERT_SENT_AT" ]]; then
            SHOULD_ALERT=1
        else
            ALERT_EPOCH=$(date -d "$ALERT_SENT_AT" +%s 2>/dev/null || echo "0")
            HOURS_SINCE_ALERT=$(( (CURRENT_EPOCH - ALERT_EPOCH) / 3600 ))
            if [[ "$HOURS_SINCE_ALERT" -ge 4 ]]; then
                SHOULD_ALERT=1
            fi
        fi
    fi
    
    if [[ "$SHOULD_ALERT" -eq 1 ]]; then
        MESSAGE="🚨 Heartbeat failure alert: ${CONSECUTIVE_FAILURES} consecutive heartbeat failures detected. Last: ${LAST_FAILURE_AT}. Provider rejected requests as 'high risk'. Server monitoring may be affected."
        
        # Log to alert file
        echo "$MESSAGE" >> "$ALERT_LOG"
        
        ALERT_SENT_AT="$CURRENT_TIME"
    fi
else
    # Reset on success
    CONSECUTIVE_FAILURES=0
    LAST_FAILURE_AT="null"
    ALERT_SENT_AT="null"
fi

# ─── Save State ─────────────────────────────────────────────────────────

cat > "$MEMORY_FILE" << EOF
{"consecutiveFailures":${CONSECUTIVE_FAILURES},"lastFailureAt":${LAST_FAILURE_AT:+"$LAST_FAILURE_AT"}${LAST_FAILURE_AT:-null},"alertSentAt":${ALERT_SENT_AT:+"$ALERT_SENT_AT"}${ALERT_SENT_AT:-null}}
EOF

echo "Watchdog check complete. Failures: $CONSECUTIVE_FAILURES, Last: ${LAST_FAILURE_AT:-null}, Alert: ${ALERT_SENT_AT:-null}"
