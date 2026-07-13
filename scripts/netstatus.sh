#!/bin/bash
# netstatus.sh — Network + VPN Status
# Shows VPN state, public IP location, and system uptime.
# Does NOT include OpenClaw gateway checks (those are runtime-specific).
#
# Usage: netstatus.sh [full|compact]
# Environment variables:
#   NETSTATUS_CACHE_FILE  Override default cache file path
#   NETSTATUS_CACHE_TTL   Override cache TTL (default: 30 seconds)
#   NETSTATUS_CURL_TIMEOUT  Override curl timeout (default: 10 seconds)
#   NETSTATUS_VPN_INTERFACE  Override VPN interface name (default: tun0)

set -euo pipefail

# ─── Configuration ──────────────────────────────────────────────────────

CACHE_FILE="${NETSTATUS_CACHE_FILE:-/tmp/netstatus-cache}"
CACHE_TTL="${NETSTATUS_CACHE_TTL:-30}"
CURL_TIMEOUT="${NETSTATUS_CURL_TIMEOUT:-10}"
VPN_INTERFACE="${NETSTATUS_VPN_INTERFACE:-tun0}"

MODE="${1:-full}"

# ─── Cache Check ────────────────────────────────────────────────────────

if [ -f "$CACHE_FILE" ]; then
    CACHE_AGE=$(($(date +%s) - $(stat -c %Y "$CACHE_FILE" 2>/dev/null || echo 0)))
    if [ "$CACHE_AGE" -lt "$CACHE_TTL" ]; then
        cat "$CACHE_FILE"
        exit 0
    fi
fi

# ─── VPN Check ──────────────────────────────────────────────────────────

VPN_STATE="DOWN"
VPN_IP=""
VPN_COUNTRY=""
VPN_CITY=""
VPN_ORG=""

if ip addr show "$VPN_INTERFACE" >/dev/null 2>&1; then
    VPN_STATE="UP"
fi

# ─── Public IP / Location ───────────────────────────────────────────────

IPINFO=$(curl -s --max-time "$CURL_TIMEOUT" https://ipinfo.io/json 2>/dev/null)

if [ -n "$IPINFO" ]; then
    VPN_IP=$(echo "$IPINFO" | jq -r '.ip // "unknown"' 2>/dev/null)
    VPN_COUNTRY=$(echo "$IPINFO" | jq -r '.country // "unknown"' 2>/dev/null)
    VPN_CITY=$(echo "$IPINFO" | jq -r '.city // "unknown"' 2>/dev/null)
    VPN_REGION=$(echo "$IPINFO" | jq -r '.region // ""' 2>/dev/null)
    VPN_ORG=$(echo "$IPINFO" | jq -r '.org // "unknown"' 2>/dev/null)
fi

# ─── System Uptime ──────────────────────────────────────────────────────

SYS_UPTIME=$(uptime -p 2>/dev/null || echo "unknown")

# ─── Build Output ─────────────────────────────────────────────────────────

if [ "$MODE" = "compact" ]; then
    if [ "$VPN_STATE" = "UP" ]; then
        OUTPUT="🌐 ${VPN_COUNTRY} ${VPN_IP} | ⏱️ ${SYS_UPTIME}"
    else
        OUTPUT="🌐 NO VPN | ⏱️ ${SYS_UPTIME}"
    fi
else
    OUTPUT="🌐 Network Status
━━━━━━━━━━━━━━━━━━━━━"

    if [ "$VPN_STATE" = "UP" ]; then
        OUTPUT="${OUTPUT}
🛡️ VPN: ${VPN_COUNTRY} (${VPN_CITY}${VPN_REGION:+, $VPN_REGION})
    IP: ${VPN_IP}
    Provider: ${VPN_ORG}
    Interface: ${VPN_INTERFACE} UP"
    else
        OUTPUT="${OUTPUT}
🛡️ VPN: DISCONNECTED
    Interface: ${VPN_INTERFACE} DOWN"
    fi

    OUTPUT="${OUTPUT}

🌍 Public IP: ${VPN_IP:-unreachable}

⏱️ System uptime: ${SYS_UPTIME}"
fi

# ─── Cache and Output ───────────────────────────────────────────────────

echo "$OUTPUT" > "$CACHE_FILE"
cat "$CACHE_FILE"
