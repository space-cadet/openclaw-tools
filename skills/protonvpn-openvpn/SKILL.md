---
name: "protonvpn-openvpn"
description: "Manage ProtonVPN OpenVPN connections — connect, disconnect, rotate, check status"
---

# ProtonVPN OpenVPN Skill

Manage ProtonVPN OpenVPN connections for privacy, geo-testing, and IP rotation workflows.

## When to Use

Use this skill when:
- Connecting to a specific ProtonVPN country server
- Disconnecting from VPN
- Checking current VPN status and IP location
- Rotating through available VPN configs for IP diversity
- Testing geo-dependent features or bypassing regional blocks

## Prerequisites

- OpenVPN installed (`openvpn` binary in PATH)
- ProtonVPN config files in `/etc/openvpn/client/`
- Auth credentials file at `/etc/openvpn/client/auth.txt` (chmod 600)
- Passwordless sudo for `openvpn` and `kill` commands (recommended)

## Available Configs

| Config File | Country | Code |
|-------------|---------|------|
| `us.protonvpn.udp.ovpn` | United States | us |
| `se.protonvpn.udp.ovpn` | Sweden | se |
| `nl.protonvpn.udp.ovpn` | Netherlands | nl |
| `cz.protonvpn.udp.ovpn` | Czech Republic | cz |
| `in.protonvpn.udp.ovpn` | India (routes via Singapore) | in |

## Commands

### Connect

```bash
sudo openvpn --config /etc/openvpn/client/<country>.protonvpn.udp.ovpn --daemon --log-append /tmp/openvpn.log --writepid /tmp/openvpn.pid
```

Wait 5 seconds for connection, then verify:
```bash
sleep 5 && curl -s --max-time 10 https://ipinfo.io/json | jq -r '"\(.country) | \(.city), \(.region) | \(.ip) | \(.org)"'
```

### Disconnect

```bash
sudo kill $(cat /tmp/openvpn.pid 2>/dev/null) 2>/dev/null || sudo killall openvpn
```

### Status

```bash
# Check if tun0 exists
ip addr show tun0 2>/dev/null && echo "VPN interface: UP" || echo "VPN interface: DOWN"

# Check current IP/location
curl -s --max-time 10 https://ipinfo.io/json | jq -r '"\(.country) | \(.city), \(.region) | \(.ip) | \(.org)"' 2>/dev/null || echo "No VPN connection"
```

### Rotate

Disconnect current, then connect to next config in rotation:
```bash
# 1. Disconnect
sudo kill $(cat /tmp/openvpn.pid 2>/dev/null) 2>/dev/null; sleep 2

# 2. Pick next config (cycle through: us → se → nl → cz → in → us)
# Use a state file to track current position: /tmp/vpn-rotation-state

# 3. Connect to next
sudo openvpn --config /etc/openvpn/client/<next>.protonvpn.udp.ovpn --daemon --log-append /tmp/openvpn.log --writepid /tmp/openvpn.pid
sleep 5

# 4. Verify
curl -s --max-time 10 https://ipinfo.io/json | jq -r '"\(.country) | \(.city), \(.region) | \(.ip) | \(.org)"'
```

## Output Parsing

| Field | Source | Example |
|-------|--------|---------|
| Country | `ipinfo.io` `.country` | `US`, `SE`, `NL` |
| City | `ipinfo.io` `.city` | `Los Angeles`, `Stockholm` |
| IP | `ipinfo.io` `.ip` | `193.37.254.69` |
| Provider | `ipinfo.io` `.org` | `M247 Ltd` |
| Interface | `ip addr show tun0` | `tun0: <POINTOPOINT...>` |

## Error Handling

- If connection fails: check `/tmp/openvpn.log` for auth errors or TLS handshake failures
- If `ipinfo.io` returns wrong country: DNS leak — check resolv.conf
- If `tun0` doesn't appear: OpenVPN daemon crashed — check logs

## Security Notes

- Credentials file must be `chmod 600`
- Config files must reference `auth-user-pass /etc/openvpn/client/auth.txt`
- Never commit credentials to Git
- Use `--daemon` for background operation; use `--writepid` for clean shutdown

## Workflows

### Geo-Testing
```bash
# Connect to target country
vpn-connect us
# Run tests
# ...
# Disconnect
vpn-disconnect
```

### IP Rotation (Scraping)
```bash
# Rotate every N requests
vpn-rotate
# Make requests
# ...
```

### Privacy Mode
```bash
# Connect and stay connected
vpn-connect nl
# All traffic now routed through Netherlands
```
