#!/bin/bash
# netstatus.sh — Network + VPN + Local + Tailscale Status
# Shows all network interfaces: local, VPN, Tailscale, public IP, and system uptime.
#
# Usage: netstatus.sh [full|compact]
# Environment variables:
#   NETSTATUS_CACHE_FILE      Override default cache file path
#   NETSTATUS_CACHE_TTL       Override cache TTL (default: 30 seconds)
#   NETSTATUS_CURL_TIMEOUT    Override curl timeout (default: 10 seconds)

set -euo pipefail

# ─── Configuration ──────────────────────────────────────────────────────

CACHE_FILE="${NETSTATUS_CACHE_FILE:-/tmp/netstatus-cache}"
CACHE_TTL="${NETSTATUS_CACHE_TTL:-30}"
CURL_TIMEOUT="${NETSTATUS_CURL_TIMEOUT:-10}"

MODE="${1:-full}"

# Detect OS
OS="linux"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
fi

# ─── Cache Check ────────────────────────────────────────────────────────

if [ -f "$CACHE_FILE" ]; then
    if [ "$OS" = "macos" ]; then
        CACHE_AGE=$(($(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || echo 0)))
    else
        CACHE_AGE=$(($(date +%s) - $(stat -c %Y "$CACHE_FILE" 2>/dev/null || echo 0)))
    fi
    if [ "$CACHE_AGE" -lt "$CACHE_TTL" ]; then
        cat "$CACHE_FILE"
        exit 0
    fi
fi

# ─── Helpers ────────────────────────────────────────────────────────────

get_interface_ips() {
    local iface="$1"
    if [ "$OS" = "macos" ]; then
        ifconfig "$iface" 2>/dev/null | awk '/inet / {print $2}' | grep -v "127.0.0.1"
    else
        ip addr show "$iface" 2>/dev/null | awk '/inet / {print $2}' | cut -d/ -f1 | grep -v "127.0.0.1"
    fi
}

country_emoji() {
    case "${1:-}" in
        US) echo "🇺🇸" ;;
        GB|UK) echo "🇬🇧" ;;
        DE) echo "🇩🇪" ;;
        FR) echo "🇫🇷" ;;
        NL) echo "🇳🇱" ;;
        SE) echo "🇸🇪" ;;
        CH) echo "🇨🇭" ;;
        CA) echo "🇨🇦" ;;
        JP) echo "🇯🇵" ;;
        SG) echo "🇸🇬" ;;
        IN) echo "🇮🇳" ;;
        *) echo "🌍" ;;
    esac
}

# ─── Interface Discovery ────────────────────────────────────────────────

# Build lists of interfaces by category
LOCAL_IFACES=""
VPN_IFACES=""
TAILSCALE_IFACES=""
LOOPBACK_IFACES=""
OTHER_IFACES=""

if [ "$OS" = "macos" ]; then
    ALL_IFACES=$(ifconfig -l 2>/dev/null || echo "")
    for iface in $ALL_IFACES; do
        # Skip loopback
        if [[ "$iface" == lo* ]]; then
            LOOPBACK_IFACES="$LOOPBACK_IFACES $iface"
            continue
        fi

        IPS=$(get_interface_ips "$iface" 2>/dev/null || true)
        [ -z "$IPS" ] && continue

        # Check if Tailscale (100.x range)
        if echo "$IPS" | grep -qE "^100\.([6-9][0-9]|1[0-2][0-7])\."; then
            TAILSCALE_IFACES="$TAILSCALE_IFACES $iface"
            continue
        fi

        # Check if VPN tunnel (utun/tun/ppp with non-local IP)
        if [[ "$iface" == utun* ]] || [[ "$iface" == tun* ]] || [[ "$iface" == ppp* ]]; then
            VPN_IFACES="$VPN_IFACES $iface"
            continue
        fi

        # Check if physical interface (en/eth/wlan)
        if [[ "$iface" == en* ]] || [[ "$iface" == eth* ]] || [[ "$iface" == wlan* ]]; then
            LOCAL_IFACES="$LOCAL_IFACES $iface"
            continue
        fi

        OTHER_IFACES="$OTHER_IFACES $iface"
    done
else
    # Linux
    ALL_IFACES=$(ip -o link show 2>/dev/null | awk -F': ' '{print $2}' || true)
    for iface in $ALL_IFACES; do
        # Skip loopback
        if [[ "$iface" == lo* ]]; then
            LOOPBACK_IFACES="$LOOPBACK_IFACES $iface"
            continue
        fi

        IPS=$(get_interface_ips "$iface" 2>/dev/null || true)
        [ -z "$IPS" ] && continue

        # Check if Tailscale (100.x range)
        if echo "$IPS" | grep -qE "^100\.([6-9][0-9]|1[0-2][0-7])\."; then
            TAILSCALE_IFACES="$TAILSCALE_IFACES $iface"
            continue
        fi

        # Check if VPN tunnel
        if [[ "$iface" == tun* ]] || [[ "$iface" == ppp* ]]; then
            VPN_IFACES="$VPN_IFACES $iface"
            continue
        fi

        # Check if physical interface
        if [[ "$iface" == eth* ]] || [[ "$iface" == wlan* ]] || [[ "$iface" == en* ]]; then
            LOCAL_IFACES="$LOCAL_IFACES $iface"
            continue
        fi

        OTHER_IFACES="$OTHER_IFACES $iface"
    done
fi

# ─── VPN / Public IP ────────────────────────────────────────────────────

IPINFO=$(curl -s --max-time "$CURL_TIMEOUT" https://ipinfo.io/json 2>/dev/null || echo "")

PUBLIC_IP=""
PUBLIC_COUNTRY=""
PUBLIC_CITY=""
PUBLIC_ORG=""

if [ -n "$IPINFO" ]; then
    PUBLIC_IP=$(echo "$IPINFO" | jq -r '.ip // ""' 2>/dev/null || true)
    PUBLIC_COUNTRY=$(echo "$IPINFO" | jq -r '.country // ""' 2>/dev/null || true)
    PUBLIC_CITY=$(echo "$IPINFO" | jq -r '.city // ""' 2>/dev/null || true)
    PUBLIC_REGION=$(echo "$IPINFO" | jq -r '.region // ""' 2>/dev/null || true)
    PUBLIC_ORG=$(echo "$IPINFO" | jq -r '.org // ""' 2>/dev/null || true)
fi

# ─── Tailscale Status ───────────────────────────────────────────────────

TAILSCALE_RUNNING=""
if pgrep -x tailscaled >/dev/null 2>&1; then
    TAILSCALE_RUNNING="yes"
fi

# ─── Default Gateway ────────────────────────────────────────────────────

DEFAULT_GATEWAY=""
if [ "$OS" = "macos" ]; then
    DEFAULT_GATEWAY=$(netstat -rn 2>/dev/null | awk '/default/ && /en[0-9]/ {print $2; exit}' || true)
else
    DEFAULT_GATEWAY=$(ip route 2>/dev/null | awk '/default/ {print $3; exit}' || true)
fi

# ─── System Uptime ──────────────────────────────────────────────────────

if [ "$OS" = "macos" ]; then
    SYS_UPTIME_RAW=$(uptime 2>/dev/null || echo "unknown")
    # Parse macOS uptime: "19:34  up 19:49, 11 users, load averages: 1.98 1.97 1.73"
    SYS_UPTIME=$(echo "$SYS_UPTIME_RAW" | sed -E 's/.*up ([^,]+),.*/\1/' | xargs || echo "unknown")
    SYS_LOAD=$(echo "$SYS_UPTIME_RAW" | sed -E 's/.*load averages?: ([0-9.]+ [0-9.]+ [0-9.]+).*/\1/' || echo "")
else
    SYS_UPTIME=$(uptime -p 2>/dev/null || echo "unknown")
    SYS_LOAD=$(uptime 2>/dev/null | sed -E 's/.*load average[s]?: ([0-9.]+,? [0-9.]+,? [0-9.]+).*/\1/' | tr ',' ' ' || echo "")
fi

# ─── IP Leak Check ──────────────────────────────────────────────────────

LEAK_STATUS=""
if [ -n "$PUBLIC_IP" ]; then
    if [ -n "$VPN_IFACES" ]; then
        # VPN is up and we can reach the internet → traffic is routed through VPN
        LEAK_STATUS="no leak"
    else
        # No VPN interface but we have a public IP → direct connection
        LEAK_STATUS="direct"
    fi
fi

# ─── Build Output ───────────────────────────────────────────────────────

COUNTRY_FLAG=$(country_emoji "$PUBLIC_COUNTRY")

if [ "$MODE" = "compact" ]; then
    OUTPUT="🌐 ${PUBLIC_COUNTRY:-??} ${PUBLIC_IP:-unreachable}"
    if [ -n "$LOCAL_IFACES" ]; then
        LOCAL_IP=$(get_interface_pairs | head -1 | awk '{print $2}' || true)
        [ -n "$LOCAL_IP" ] && OUTPUT="$OUTPUT | 🏠 $LOCAL_IP"
    fi
    OUTPUT="$OUTPUT | ⏱️ ${SYS_UPTIME}"
else
    OUTPUT="🌐 Network Status
━━━━━━━━━━━━━━━━━━━━━"

    # VPN Section
    if [ -n "$VPN_IFACES" ]; then
        OUTPUT="$OUTPUT
🛡️ VPN: ${PUBLIC_ORG:-VPN} ${COUNTRY_FLAG} (${PUBLIC_CITY:-Unknown}${PUBLIC_REGION:+, $PUBLIC_REGION})
    Public IP: ${PUBLIC_IP:-unreachable}"
        for iface in $VPN_IFACES; do
            IFACE_IPS=$(get_interface_ips "$iface" | paste -sd ',' - | sed 's/,/, /g')
            [ -z "$IFACE_IPS" ] && continue
            OUTPUT="$OUTPUT
    Interface: ${iface} — ${IFACE_IPS}"
        done
    else
        OUTPUT="$OUTPUT
🛡️ VPN: DISCONNECTED"
    fi

    # Local Network Section
    if [ -n "$LOCAL_IFACES" ]; then
        OUTPUT="$OUTPUT

🏠 Local Network"
        for iface in $LOCAL_IFACES; do
            IFACE_IPS=$(get_interface_ips "$iface" | paste -sd ',' - | sed 's/,/, /g')
            [ -z "$IFACE_IPS" ] && continue
            IFACE_LABEL="$iface"
            [[ "$iface" == en0 ]] || [[ "$iface" == eth0 ]] || [[ "$iface" == wlan0 ]] && IFACE_LABEL="$iface (primary)"
            OUTPUT="$OUTPUT
    ${IFACE_LABEL}: ${IFACE_IPS}"
        done
        [ -n "$DEFAULT_GATEWAY" ] && OUTPUT="$OUTPUT
    Gateway: ${DEFAULT_GATEWAY}"
    else
        OUTPUT="$OUTPUT

🏠 Local Network: no active interface"
    fi

    # Tailscale Section
    if [ -n "$TAILSCALE_IFACES" ] || [ "$TAILSCALE_RUNNING" = "yes" ]; then
        OUTPUT="$OUTPUT

🔗 Tailscale"
        if [ "$TAILSCALE_RUNNING" = "yes" ]; then
            OUTPUT="$OUTPUT
    Status: running"
        fi
        for iface in $TAILSCALE_IFACES; do
            IFACE_IPS=$(get_interface_ips "$iface" | paste -sd ',' - | sed 's/,/, /g')
            [ -z "$IFACE_IPS" ] && continue
            OUTPUT="$OUTPUT
    ${iface}: ${IFACE_IPS}"
        done
    fi

    # Public IP / Leak Check
    OUTPUT="$OUTPUT

🌍 Public IP: ${PUBLIC_IP:-unreachable}"
    if [ -n "$LEAK_STATUS" ]; then
        if [ "$LEAK_STATUS" = "no leak" ]; then
            OUTPUT="$OUTPUT (routed through VPN)"
        elif [ "$LEAK_STATUS" = "direct" ]; then
            OUTPUT="$OUTPUT (direct connection — no VPN)"
        else
            OUTPUT="$OUTPUT ${LEAK_STATUS}"
        fi
    fi

    # System Info
    OUTPUT="$OUTPUT

⏱️ System: ${SYS_UPTIME}"
    [ -n "$SYS_LOAD" ] && OUTPUT="$OUTPUT
    Load: ${SYS_LOAD}"
fi

# ─── Cache and Output ───────────────────────────────────────────────────

echo "$OUTPUT" > "$CACHE_FILE"
cat "$CACHE_FILE"
