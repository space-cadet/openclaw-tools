---
name: "netstatus"
description: "Combined network + gateway status with VPN info, IP location, and system health"
---

# netstatus — Network + Gateway Status

Show combined network and gateway status including VPN state, public IP location, and system health.

## When to Use

Use `/netstatus` or `/net` when you want a quick overview of:
- Current VPN connection (country, IP, provider)
- Gateway health and uptime
- System status
- Whether traffic is routed through VPN or direct

## Commands

| Command | Description |
|---------|-------------|
| `/netstatus` | Full network + gateway status |
| `/net` | Alias for `/netstatus` |

## Output Format

```
🌐 Network Status
━━━━━━━━━━━━━━━━━━━━━
🛡️ VPN: ProtonVPN NL (Amsterdam)
    IP: 103.69.224.92
    Provider: AS199218 Proton AG
    Interface: tun0 UP

🌍 Public IP: 103.69.224.92 (same as VPN — no leak)

🖥️ Gateway: Running (2h 45m)
    Model: kimi/k2.7
    Context: 50k/131k (38%)

⏱️ System: 38d 21h uptime
```

Or compact mode:
```
🌐 NL 103.69.224.92 | 🖥️ k2.7 38% | ⏱️ 38d 21h
```

## Implementation

The skill runs these checks in sequence:

1. **VPN Interface**: `ifconfig | grep -E "(tun|utun|ppp)"` — checks if tunnel exists (macOS/Linux)
2. **IP Location**: `curl -s https://ipinfo.io/json` — gets country, city, IP, org
3. **Gateway Status**: `openclaw gateway status` or read from runtime
4. **System Uptime**: `uptime` (parsed for macOS/Linux compatibility)

## macOS vs Linux

| Command | Linux | macOS |
|---------|-------|-------|
| VPN interface | `ip addr show tun0` | `ifconfig \| grep utun` |
| Uptime parsing | `uptime -p` | `uptime` (raw output) |

## Error States

| State | Display |
|-------|---------|
| VPN down | `🛡️ VPN: DISCONNECTED` |
| IP mismatch | `⚠️ IP leak detected: VPN=NL but public=US` |
| Can't reach ipinfo | `🌍 Public IP: unreachable` |

## Notes

- Uses `ipinfo.io` for geolocation (free tier, no auth needed)
- Caches result for 30 seconds to avoid rate limits
- Requires `curl`, `jq`, `ifconfig` (macOS) or `ip` (Linux)
- VPN detection uses `utun` on macOS, `tun` on Linux
