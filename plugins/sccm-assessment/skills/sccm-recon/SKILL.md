---
name: sccm-recon
description: Perform SCCM reconnaissance and takeover prerequisite validation, including site-role mapping, provider and AdminService checks, site database separation checks, and relay-path prechecks.
icon: ./assets/icon.png
---

# SCCM Recon

Use this skill to identify SCCM infrastructure and validate the prerequisites needed for follow-on SCCM operations such as site takeover, provider abuse, or controlled client-execution validation.

This skill is the preferred precursor to `$sccm-takeover-relay`.

## Direct Triggers

Use this skill when the task mentions any of the following:
- SCCM recon
- ConfigMgr recon
- find the site server
- find the SMS Provider
- find the site database
- validate SCCM takeover prerequisites
- AdminService check
- SCCM site role mapping

## Input Contract

Accept input as:
`TARGET [MODE] [NOISE]`

Mode:
- `plan`: produce the recon plan and command set only
- `execute` (default): run bounded checks and capture evidence

Noise:
- `low` (default): focused validation against known or likely SCCM assets
- `medium`: broader SCCM role discovery and enrichment
- `high`: aggressive probing, approval required

Examples:
- `$sccm-recon 192.0.2.20 execute low`
- `$sccm-recon corp.local plan`
- `$sccm-recon smsprov01.corp.local execute medium`

## Objectives

1. Identify likely SCCM assets and roles:
- site server
- SMS Provider
- site database host
- management point
- distribution point

2. Identify SCCM-specific services and interfaces where feasible:
- `mssms`-related SQL context
- `SMS_SITE_COMPONENT_MANAGER` and related role hints
- AdminService
- provider/WMI access points

3. Validate takeover prerequisites for follow-on operations:
- site database is separate from the coercion target
- likely relay path to MSSQL exists
- candidate site-system hosts are high-value coercion targets
- EPA/NTLM conditions need further verification

## Preconditions

1. Confirm the target or target range is in scope.
2. Prefer known SCCM hosts first before expanding outward.
3. If using pivots or C2 egress paths, note the transport and path assumptions in evidence.

## Tooling Setup

Before execution, confirm where the skill will run and whether the following tools are available on that host.

Preferred Linux tooling:
- `nmap`
- `curl`
- `rpcclient`
- `smbclient`
- `nc`

Typical Kali/Debian install commands:

```bash
sudo apt-get update
sudo apt-get install -y nmap curl netcat-openbsd smbclient rpcbind
```

Notes:
- `rpcclient` and `smbclient` are typically provided by the Samba client packages on Debian/Kali systems.
- If `rpcclient` is not present after install, verify with:

```bash
which rpcclient
which smbclient
```

If this recon must run through a pivot or team server, record:
- host running the commands
- pivot method, if any
- whether `$proxychains-tunnel` should wrap the commands

Do not begin execution until the operator path for running the recon is clear.

## Execution Workflow

1. Build the host set.
- start with operator-provided hostnames/IPs
- enrich with DNS and naming clues when available, for example:
  - `sccm`
  - `cm`
  - `mecm`
  - `sms`
  - `mp`
  - `dp`
  - `cas`

2. Run low-noise service checks.
- confirm core Windows service exposure and likely SCCM surfaces:
  - SMB `445`
  - RPC `135`
  - WinRM `5985/5986`
  - MSSQL `1433`
  - HTTP/HTTPS `80/443`
- check for AdminService paths when web services are present

3. Identify likely roles.
- infer role from service exposure, hostname conventions, and accessible web/API surfaces
- distinguish confirmed role evidence from naming-based hypotheses

4. Validate site database separation and relay path assumptions.
- check whether the candidate site DB host differs from the candidate coercion target
- check whether MSSQL is reachable on the site DB host
- record any evidence that the SMS Provider is on a separate host

5. Gather takeover-specific prereqs for handoff.
- likely coercion targets
- likely MSSQL relay targets
- likely SMS Provider verification target
- reachable ports relevant to takeover
- blockers such as closed `1433`, no reachable provider, or collapsed single-host architecture

6. Produce a normalized handoff for `$sccm-takeover-relay`.

7. Troubleshoot relay-path assumptions when needed.
- if a required relay port appears blocked, compare it against a temporary listener on another known-allowed port
- if the alternate port is reachable but the required port is refused, treat that as evidence of a port-specific environment restriction
- record the test commands and outcomes for both ports

## Command Patterns

### Focused port validation

```bash
nmap -Pn -p 80,135,139,443,445,1433,5985,5986 <TARGET>
```

### HTTP header and AdminService probing

```bash
curl -isk https://<TARGET>/AdminService/wmi/
curl -isk https://<TARGET>/ccm_system/request
```

### SMB and host-role context

```bash
rpcclient -N -U "" <TARGET>
smbclient -L //<TARGET> -N
```

### SQL reachability

```bash
nc -zv <TARGET> 1433
```

Use `$ssh-ops` or `$proxychains-tunnel` when these checks should run through operator-controlled remote or tunneled command execution.

If the operator provides external MCP tooling, verify the relevant MCP tools are available before relying on them.

## OPSEC Gate

Require explicit operator confirmation before:
- subnet-wide SCCM hunting across many hosts
- aggressive web/content discovery
- intrusive RPC/SMB enumeration beyond bounded checks
- any brute force, spraying, or exploit execution

Before requesting approval, include:
- exact action
- objective
- expected impact
- assumptions/prerequisites
- telemetry and detection surfaces
- expected noise level

## Output Requirements

For each run, include:
- target(s) tested
- exact commands and outputs
- candidate SCCM roles per host with confidence labels:
  - `confirmed`
  - `likely`
  - `unknown`
- takeover-prereq assessment:
  - candidate coercion target
  - candidate site DB target
  - candidate SMS Provider target
  - relevant port reachability
  - blockers and unknowns
- timestamps in UTC ISO 8601
- recommended next step

## Handoff To `sccm-takeover-relay`

When used as a precursor, provide:
- `coercion_target`
- `site_db_target`
- `sms_provider_target`
- `relay_path_notes`
- `candidate_site_code`
- `confidence`
- `blocked_by` if prerequisites are incomplete

## Port Troubleshooting Guidance

When validating relay-host reachability through SOCKS, pivots, or C2 transport:
1. test the intended port first
2. if it fails, stand up a temporary listener on a different port on the same relay host
3. test the same path to that alternate port
4. interpret results:
- alternate port succeeds, intended port fails:
  - likely port-specific outbound or environment restriction
- both fail:
  - broader path, routing, firewall, or listener issue
- both succeed:
  - relay-path connectivity is not the blocker

## Reporting Notes

Prefer high-signal evidence over broad host counts. If role certainty is weak, say so and recommend the narrowest next validation step.
