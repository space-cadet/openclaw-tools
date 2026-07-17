# protonvpn-openvpn — Skill Card

| Field | Value |
|-------|-------|
| **Name** | protonvpn-openvpn |
| **Version** | — |
| **One-liner** | Manage ProtonVPN OpenVPN connections — connect, disconnect, rotate, check status. |

## Trigger
- "Connect to VPN"
- "Disconnect VPN"
- "Check VPN status"
- "Rotate IP" / geo-testing / privacy mode

## Key Commands

```bash
# Connect
sudo openvpn --config /etc/openvpn/client/nl.protonvpn.udp.ovpn \
  --daemon --log-append /tmp/openvpn.log --writepid /tmp/openvpn.pid

# Disconnect
sudo kill $(cat /tmp/openvpn.pid 2>/dev/null) 2>/dev/null || sudo killall openvpn

# Check status
ip addr show tun0 2>/dev/null && echo "UP" || echo "DOWN"
curl -s --max-time 10 https://ipinfo.io/json | jq -r '"\(.country) | \(.city) | \(.ip)"'

# Rotate (disconnect → next config → connect)
# Cycle: us → se → nl → cz → in → us
```

## Dependencies
- `openvpn` binary in PATH
- ProtonVPN configs in `/etc/openvpn/client/`
- Auth file at `/etc/openvpn/client/auth.txt` (chmod 600)

## Quick Example

```bash
# Connect to Netherlands
sudo openvpn --config /etc/openvpn/client/nl.protonvpn.udp.ovpn \
  --daemon --log-append /tmp/openvpn.log --writepid /tmp/openvpn.pid
sleep 5
curl -s https://ipinfo.io/json | jq -r '.country, .ip'
```

> Never commit credentials to Git. Use `--daemon` + `--writepid` for clean background operation.
