#!/bin/bash
# ProtonVPN OpenVPN Manager
# Usage: protonvpn.sh [connect|disconnect|status|rotate] [country-code]
#
# Environment:
#   PROTONVPN_CONFIG_DIR — override config directory (default: /etc/openvpn/client)
#   PROTONVPN_LOG_FILE   — override log file (default: /tmp/openvpn.log)
#   PROTONVPN_PID_FILE   — override PID file (default: /tmp/openvpn.pid)
#   PROTONVPN_STATE_FILE — override rotation state file (default: /tmp/vpn-rotation-state)

CONFIG_DIR="${PROTONVPN_CONFIG_DIR:-/etc/openvpn/client}"
LOG_FILE="${PROTONVPN_LOG_FILE:-/tmp/openvpn.log}"
PID_FILE="${PROTONVPN_PID_FILE:-/tmp/openvpn.pid}"
ROTATION_STATE="${PROTONVPN_STATE_FILE:-/tmp/vpn-rotation-state}"
CURL_TIMEOUT=10

# Available configs in rotation order
CONFIGS=("us" "se" "nl" "cz" "in")

usage() {
    echo "Usage: $0 {connect|disconnect|status|rotate} [country-code]"
    echo ""
    echo "Countries: us, se, nl, cz, in"
    echo ""
    echo "Examples:"
    echo "  $0 connect us     # Connect to US server"
    echo "  $0 disconnect     # Disconnect VPN"
    echo "  $0 status         # Check VPN status"
    echo "  $0 rotate         # Rotate to next country"
    exit 1
}

verify_connection() {
    sleep 5
    local result
    result=$(curl -s --max-time "$CURL_TIMEOUT" https://ipinfo.io/json 2>/dev/null)
    if [ -n "$result" ]; then
        echo "$result" | jq -r '"\(.country) | \(.city), \(.region) | \(.ip) | \(.org)"' 2>/dev/null || echo "Connected (parse error)"
    else
        echo "FAILED — no response from ipinfo.io"
    fi
}

cmd_connect() {
    local country="${1:-us}"
    local config_file="$CONFIG_DIR/${country}.protonvpn.udp.ovpn"
    
    if [ ! -f "$config_file" ]; then
        echo "Error: Config file not found: $config_file"
        echo "Available: ${CONFIGS[*]}"
        exit 1
    fi
    
    # Disconnect any existing connection first
    cmd_disconnect >/dev/null 2>&1
    sleep 2
    
    echo "Connecting to ProtonVPN ($country)..."
    sudo openvpn --config "$config_file" --daemon --log-append "$LOG_FILE" --writepid "$PID_FILE"
    
    local status
    status=$(verify_connection)
    echo "Result: $status"
    
    # Save current country for rotation
    echo "$country" > "$ROTATION_STATE"
}

cmd_disconnect() {
    if [ -f "$PID_FILE" ]; then
        local pid
        pid=$(cat "$PID_FILE" 2>/dev/null)
        if [ -n "$pid" ]; then
            sudo kill "$pid" 2>/dev/null
        fi
        rm -f "$PID_FILE"
    fi
    # Fallback: kill all openvpn processes
    sudo killall openvpn 2>/dev/null
    echo "Disconnected"
}

cmd_status() {
    local interface_status="DOWN"
    if ip addr show tun0 >/dev/null 2>&1; then
        interface_status="UP"
    fi
    
    echo "VPN Interface: $interface_status"
    
    local location
    location=$(curl -s --max-time "$CURL_TIMEOUT" https://ipinfo.io/json 2>/dev/null)
    if [ -n "$location" ]; then
        echo "Location: $(echo "$location" | jq -r '"\(.country) | \(.city), \(.region) | \(.ip) | \(.org)"' 2>/dev/null)"
    else
        echo "Location: No VPN connection detected"
    fi
    
    if [ -f "$ROTATION_STATE" ]; then
        echo "Current config: $(cat "$ROTATION_STATE")"
    fi
}

cmd_rotate() {
    local current_idx=0
    local current_country=""
    
    if [ -f "$ROTATION_STATE" ]; then
        current_country=$(cat "$ROTATION_STATE")
        for i in "${!CONFIGS[@]}"; do
            if [ "${CONFIGS[$i]}" = "$current_country" ]; then
                current_idx=$i
                break
            fi
        done
    fi
    
    local next_idx=$(( (current_idx + 1) % ${#CONFIGS[@]} ))
    local next_country="${CONFIGS[$next_idx]}"
    
    echo "Rotating from ${current_country:-none} to $next_country..."
    cmd_connect "$next_country"
}

# Main
case "${1:-}" in
    connect|c)
        cmd_connect "${2:-us}"
        ;;
    disconnect|d|stop)
        cmd_disconnect
        ;;
    status|s)
        cmd_status
        ;;
    rotate|r)
        cmd_rotate
        ;;
    *)
        usage
        ;;
esac
