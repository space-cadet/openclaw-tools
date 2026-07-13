#!/bin/bash
# crash-recovery.sh — Detect recent crashes and prepare context recovery
# Usage: bash crash-recovery.sh [OPTIONS]
#
# Options:
#   --sessions-dir PATH   Path to OpenClaw sessions directory
#   --crash-log PATH      Path to crash log file
#   --recovery-file PATH  Path to write recovery context
#
# Environment variables:
#   CRASH_SESSIONS_DIR    Override default sessions directory
#   CRASH_LOG_FILE        Override default crash log path
#   CRASH_RECOVERY_FILE   Override default recovery file path

set -euo pipefail

# ─── Configuration ──────────────────────────────────────────────────────

SESSIONS_DIR="${CRASH_SESSIONS_DIR:-${HOME}/.openclaw/agents/main/sessions}"
CRASH_LOG="${CRASH_LOG_FILE:-${HOME}/.openclaw/workspace/memory/crash-log.md}"
RECOVERY_FILE="${CRASH_RECOVERY_FILE:-/tmp/crash-recovery-context.txt}"

# Parse CLI args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --sessions-dir)
            SESSIONS_DIR="$2"
            shift 2
            ;;
        --crash-log)
            CRASH_LOG="$2"
            shift 2
            ;;
        --recovery-file)
            RECOVERY_FILE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--sessions-dir PATH] [--crash-log PATH] [--recovery-file PATH]"
            exit 1
            ;;
    esac
done

# ─── Detect recent crashes ─────────────────────────────────────────────

echo "=== Crash Recovery Check ==="
echo "Time: $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "Sessions dir: $SESSIONS_DIR"
echo ""

# 1. Check for .reset files in the last hour
RECENT_RESETS=$(find "$SESSIONS_DIR" -maxdepth 1 -name "*.reset*" -mmin -60 2>/dev/null | wc -l)

# 2. Check if the most recent session file is very short (indicates abrupt end)
LATEST_SESSION=""
SESSION_LINE_COUNT=0
TMP_LIST=$(mktemp)
find "$SESSIONS_DIR" -maxdepth 1 -name "*.jsonl" ! -name "*trajectory*" -printf '%T@ %p\n' 2>/dev/null | sort -rn > "$TMP_LIST"
if [ -s "$TMP_LIST" ]; then
    LATEST_SESSION=$(head -1 "$TMP_LIST" | cut -d' ' -f2-)
    if [ -n "$LATEST_SESSION" ] && [ -f "$LATEST_SESSION" ]; then
        SESSION_LINE_COUNT=$(wc -l < "$LATEST_SESSION" || echo 0)
    fi
fi
rm -f "$TMP_LIST"

# 3. Check crash log for recent entries
RECENT_CRASHES=0
if [ -f "$CRASH_LOG" ]; then
    CURRENT_HOUR=$(date -u '+%Y-%m-%d %H')
    RECENT_CRASHES=$(grep -c "^## ${CURRENT_HOUR}" "$CRASH_LOG" 2>/dev/null || echo 0)
fi

echo "Recent .reset files (last 60 min): $RECENT_RESETS"
echo "Latest session line count: $SESSION_LINE_COUNT"
echo "Recent crash log entries (this hour): $RECENT_CRASHES"
echo ""

# ─── Determine if recovery is needed ────────────────────────────────────

NEEDS_RECOVERY=false
if [ "$RECENT_RESETS" -gt 0 ]; then
    echo "⚠️  Session reset detected in last hour."
    NEEDS_RECOVERY=true
fi

if [ "$SESSION_LINE_COUNT" -lt 5 ] && [ "$SESSION_LINE_COUNT" -gt 0 ]; then
    echo "⚠️  Latest session is very short ($SESSION_LINE_COUNT lines) — possible crash."
    NEEDS_RECOVERY=true
fi

if [ "$RECENT_CRASHES" -ge 2 ]; then
    echo "🚨 Multiple crashes logged this hour ($RECENT_CRASHES)."
    NEEDS_RECOVERY=true
fi

if [ "$NEEDS_RECOVERY" = false ]; then
    echo "✅ No recent crashes detected. Session appears healthy."
    rm -f "$RECOVERY_FILE"
    exit 0
fi

# ─── Recover context from previous session ──────────────────────────────

echo ""
echo "=== Recovering Context ==="

# Find the second-most-recent session (the one that crashed)
PREV_SESSION=""
TMP_LIST2=$(mktemp)
find "$SESSIONS_DIR" -maxdepth 1 -name "*.jsonl" ! -name "*trajectory*" -printf '%T@ %p\n' 2>/dev/null | sort -rn > "$TMP_LIST2"
if [ -s "$TMP_LIST2" ]; then
    PREV_SESSION=$(sed -n '2p' "$TMP_LIST2" | cut -d' ' -f2-)
fi
rm -f "$TMP_LIST2"

if [ -z "$PREV_SESSION" ] || [ ! -f "$PREV_SESSION" ]; then
    echo "❌ No previous session file found for recovery."
    exit 1
fi

echo "Reading from: $(basename "$PREV_SESSION")"

# Extract last 20 user and assistant messages using Python
python3 << PYEOF
import json, os, sys

session_file = os.environ.get("PREV_SESSION", "")
if not session_file or not os.path.exists(session_file):
    sys.exit(1)

messages = []
with open(session_file, 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            if data.get('type') == 'message':
                msg = data.get('message', {})
                role = msg.get('role', '')
                content = msg.get('content', [])
                text = ''
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get('type') == 'text':
                            text += c.get('text', '')
                elif isinstance(content, str):
                    text = content
                
                if role in ('user', 'assistant') and text:
                    if len(text) > 500:
                        text = text[:500] + '... [truncated]'
                    messages.append((role, text))
        except json.JSONDecodeError:
            continue

messages = messages[-20:]
recovery_file = os.environ.get("RECOVERY_FILE", "/tmp/crash-recovery-context.txt")
with open(recovery_file, 'w') as f:
    f.write("=== CRASH RECOVERY CONTEXT ===\n")
    f.write(f"Source: {session_file}\n")
    f.write(f"Recovered at: {os.popen('date -u +\"%Y-%m-%d %H:%M UTC\"').read().strip()}\n")
    f.write(f"Messages recovered: {len(messages)}\n")
    f.write("=" * 50 + "\n\n")
    
    for role, text in messages:
        prefix = "USER" if role == "user" else "ASSISTANT"
        f.write(f"[{prefix}]\n{text}\n\n")

print(f"✅ Recovered {len(messages)} messages to {recovery_file}")
PYEOF

if [ -f "$RECOVERY_FILE" ]; then
    echo ""
    echo "=== Recovered Context Preview ==="
    head -50 "$RECOVERY_FILE"
    echo ""
    echo "Full recovery context saved to: $RECOVERY_FILE"
    echo ""
    echo "Next steps:"
    echo "1. Read $RECOVERY_FILE for full context"
    echo "2. Summarize what was being done before the crash"
    echo "3. Continue from where you left off"
    echo "4. Log this crash in $CRASH_LOG"
fi
