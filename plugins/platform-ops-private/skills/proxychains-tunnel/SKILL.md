---
name: proxychains-tunnel
description: Run in-scope network commands through a SOCKS5 tunnel with proxychains4, including tunnel readiness checks and evidence capture. Use when traffic must traverse a local SOCKS proxy (for example pivoting through SSH dynamic forwarding).
icon: ./assets/icon.png
---

# Proxychains Tunnel

Run scoped commands through `proxychains4` when a task requires a SOCKS5 tunnel (for example, internal recon through a pivot host).

## Input Contract

Accept input as: `SOCKS_HOST:SOCKS_PORT COMMAND [MODE] [NOISE]`

Mode:
- `plan`: return command plan only
- `execute` (default): run checks and command sequence

Noise:
- `low` (default): single-host validation and bounded probing
- `medium`: broader enumeration
- `high`: aggressive/noisy actions (approval required)

Examples:
- `$proxychains-tunnel 127.0.0.1:8080 "nmap -Pn -p 445 192.0.2.21" execute low`
- `$proxychains-tunnel 127.0.0.1:8080 "smbclient -L //192.0.2.21 -N" execute low`
- `$proxychains-tunnel 127.0.0.1:1080 "crackmapexec smb 192.0.2.0/24 -u '' -p ''" plan medium`

Natural-language mapping example:
- Request: `Use the Socks5 tunnel on 127.0.0.1:8080 to check port 445`
- Command intent: `nmap -Pn -p 445 <target>`
- Execution pattern: `proxychains4 <command>`

## Preconditions

1. Confirm target is in scope for the active engagement before executing commands.
2. Confirm `proxychains4` is installed.
3. Build an isolated proxychains config for each run instead of mutating global config.
4. Validate local proxy listener before running target command.

## Execution Workflow

1. Parse and validate:
- split `SOCKS_HOST:SOCKS_PORT`,
- parse target command and identify likely noise profile.

2. Create temporary config:

```bash
cat > /tmp/proxychains-codex.conf <<'EOF'
strict_chain
proxy_dns
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 8080
EOF
```

Replace the `socks5` endpoint with provided `SOCKS_HOST:SOCKS_PORT`.

3. Readiness checks:
- `nc -zv <SOCKS_HOST> <SOCKS_PORT>`
- optional egress check:
  - direct: `curl -4 -s https://icanhazip.com`
  - proxied: `proxychains4 -q -f /tmp/proxychains-codex.conf curl -4 -s https://icanhazip.com`
- fail fast if tunnel is down.

4. Execute proxied command:

```bash
proxychains4 -q -f /tmp/proxychains-codex.conf <COMMAND>
```

For the port-445 example:

```bash
proxychains4 -q -f /tmp/proxychains-codex.conf nmap -Pn -p 445 192.0.2.21
```

5. Cleanup:
- remove temp config: `rm -f /tmp/proxychains-codex.conf`

## OPSEC Gate

Require explicit operator confirmation before OPSEC-dangerous actions, including:
- subnet-wide scans through the tunnel,
- aggressive timing or full-port scans,
- brute force or spraying via proxied services,
- exploit execution through the tunnel.

Before requesting confirmation, provide:
- exact command,
- objective,
- expected impact,
- assumptions/prerequisites,
- telemetry and detection surfaces (host/network/identity/EDR-SIEM).

## Reporting Requirements

For each tunneled validation, include:
- SOCKS endpoint and config mode used (`strict_chain`, `proxy_dns`),
- exact command executed (with `proxychains4` wrapper),
- readiness-check output and command output,
- timestamp (UTC ISO 8601),
- confirmed result vs inference,
- remediation or next validation step.
