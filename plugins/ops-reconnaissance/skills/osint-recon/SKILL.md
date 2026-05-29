---
name: osint-recon
description: Perform OSINT and external reconnaissance for approved targets. Use for subdomain discovery, infrastructure mapping, technology fingerprinting, and recon reporting with optional command execution.
metadata:
  author: "GhostWorks"
---

# OSINT Recon

Run structured reconnaissance against user-provided authorized targets.

## Input Parsing

Accept input as: `TARGET [DEPTH] [MODE]`

Depth:
- `passive` (default)
- `active`
- `full`

Mode:
- `plan`: report plan + command set only
- `execute` (default, preferred): run command batches and capture evidence

If mode is omitted, default to `execute`.

Examples:
- `$osint-recon example.com`
- `$osint-recon example.com active`
- `$osint-recon "Acme Corp" full execute`
- `$osint-recon 203.0.113.0/24 passive execute`

## Execution Policy

- Always generate recon plan first.
- In `execute` mode (default):
  - run command batches autonomously for routine in-scope actions,
  - request approval only for OPSEC-dangerous actions,
  - provide brief OPSEC warning for active/noisy actions.
- Capture exact commands and key outputs in the report.

## Workflow

1. Create output directory:
   - `mkdir -p recon/<target-slug>/`
2. Run passive recon for all depths.
3. Run active recon only for `active` or `full` depth; require approval only for OPSEC-dangerous steps.
4. Correlate findings and prioritize exploitable attack surface.
5. Save report:
   - `recon/<target-slug>/recon-report.md`

## Phase 1: Passive Recon (All Depths)

Suggested commands:

```bash
# Subdomains
subfinder -d <target> -silent -o recon/<target-slug>/subdomains.txt

# DNS records
dig +short <target> A
dig +short <target> MX
dig +short <target> TXT
dig +short <target> NS

# Certificate transparency
curl -s "https://crt.sh/?q=%25.<target>&output=json"

# WHOIS
whois <target>
```

Investigate:
- ASN/IP ownership and provider footprint
- CDN/WAF presence
- exposed technologies and externally reachable services
- credential/leak indicators from public sources

## Phase 2: Active Recon (Active/Full Depth)

Suggested commands:

```bash
# HTTP probing / tech fingerprinting
httpx -l recon/<target-slug>/subdomains.txt -title -status-code -tech-detect -o recon/<target-slug>/httpx.txt

# Quick TCP service scan
nmap -sC -sV --top-ports 1000 -oA recon/<target-slug>/nmap-quick <target>

# Full TCP scan (noisier)
nmap -sC -sV -p- -oA recon/<target-slug>/nmap-full <target>

# Directory discovery
ffuf -u https://<target>/FUZZ -w <wordlist> -mc 200,301,302,403

# Template-based checks
nuclei -l recon/<target-slug>/subdomains.txt -o recon/<target-slug>/nuclei.txt
```

## Reporting Template

```markdown
# OSINT Report ? <target>
## Depth: <passive|active|full>
## Mode: <plan|execute>
## Timestamp: <utc timestamp>

## Executive Summary
- High-level attack-surface summary.

## Findings
- Subdomains / hosts
- Infrastructure ownership and hosting
- Technology fingerprints
- Notable exposures

## Commands and Evidence
- exact command
- key output
- interpretation

## Prioritized Next Steps
1. next action
2. next action
```

## Quality Rules

- Keep results target-specific and evidence-backed.
- Distinguish confirmed findings vs hypotheses.
- Prioritize exploitability over raw finding count.
