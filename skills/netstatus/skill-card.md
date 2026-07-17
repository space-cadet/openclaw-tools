# netstatus — Skill Card

| Field | Value |
|-------|-------|
| **Name** | netstatus |
| **Version** | — |
| **One-liner** | Combined network + gateway status with VPN info, IP location, and system health. |

## Trigger
- `/netstatus` or `/net`
- Need quick overview of VPN, gateway, system health
- "Am I connected to VPN?"

## Key Commands

```bash
# VPN interface check
ip addr show tun0

# IP location
curl -s https://ipinfo.io/json

# Gateway status
openclaw gateway status

# System uptime
uptime -p
```

## Dependencies
- `curl`, `jq`, `ip`
- `ipinfo.io` (free tier, no auth)

## Quick Example

```
🌐 Network Status
━━━━━━━━━━━━━━━━━━━━━
🛡️ VPN: ProtonVPN NL (Amsterdam)
    IP: 103.69.224.92
🌍 Public IP: 103.69.224.92 (same as VPN — no leak)
🖥️ Gateway: Running (2h 45m) | Model: kimi/k2.7 | Context: 38%
⏱️ System: 38d 21h uptime
```

> Caches result for 30 seconds to avoid rate limits.
