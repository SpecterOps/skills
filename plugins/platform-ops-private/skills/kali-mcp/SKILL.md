---
name: kali-mcp
description: Execute in-scope offensive security workflows through the Kali MCP server in ../MCP-Kali-Server. Use when command execution or Kali tooling is required through MCP (nmap, gobuster, dirb, nikto, sqlmap, hydra, john, enum4linux, wpscan, metasploit, or raw command execution) and the task needs structured output, OPSEC-aware gating, and evidence capture.
icon: ./assets/icon.png
---

# Kali MCP

Run Kali toolchains through the `kali_mcp` MCP server while keeping execution scoped, evidence-backed, and OPSEC-aware.

## Input Contract

Accept input as: `OBJECTIVE TARGET [MODE] [NOISE]`

Mode:
- `plan`: build command/tool plan only
- `execute` (default): run tool calls and capture evidence

Noise:
- `low` (default): discovery and validation with bounded requests
- `medium`: broader enumeration with controlled expansion
- `high`: aggressive or potentially disruptive actions, only with explicit approval

Examples:
- `$kali-mcp service-discovery 198.51.100.15 execute low`
- `$kali-mcp web-enum http://198.51.100.20 execute medium`
- `$kali-mcp smb-enum 198.51.100.25 plan low`

## Preconditions

1. Confirm MCP server registration in config as `kali_mcp`, sourced from `../MCP-Kali-Server/client.py`.
2. Run `server_health` before first action batch.
3. Enforce scope boundary from the active engagement scope unless the operator explicitly expands it.
4. Refuse or pause before out-of-scope targets.

## Tool Map

Use the typed MCP tools before falling back to raw command execution:

- Host/service discovery: `nmap_scan`
- Web content enumeration: `gobuster_scan`, `dirb_scan`
- Web vuln checks: `nikto_scan`, `sqlmap_scan`, `wpscan_analyze`
- SMB/Windows enumeration: `enum4linux_scan`
- Credential cracking/testing: `hydra_attack`, `john_crack`
- Exploit module execution: `metasploit_run`
- Connectivity and readiness: `server_health`
- Fallback command execution: `execute_command`

Use `execute_command` only when no typed tool covers the objective, and include command rationale.

## Execution Workflow

1. Build objective-specific plan:
- define target,
- pick minimal tool set,
- set stopping conditions.

2. Health and safety gate:
- call `server_health`,
- verify target scope and OPSEC posture,
- request approval if action is OPSEC-dangerous.

3. Execute in bounded batches:
- start with low-noise probes,
- inspect outputs before escalating,
- preserve exact input arguments per tool call.

4. Escalate only when justified:
- move from `low` to `medium` to `high`,
- include expected impact and detection surfaces before high-noise runs.

5. Capture evidence:
- include tool name, input arguments, timestamp (UTC ISO 8601),
- capture raw MCP response fields (`stdout`, `stderr`, `return_code`, `success`, `timed_out`, `partial_results`),
- summarize confirmed result vs inference.

6. Produce actionable next steps:
- remediation candidates,
- follow-on validation commands,
- detection opportunities.

## OPSEC Gate

Treat these as OPSEC-dangerous and require explicit operator confirmation first:
- broad port scans across many hosts,
- brute-force/password spraying (`hydra_attack`) beyond tightly bounded test cases,
- exploit execution with `metasploit_run`,
- aggressive or lengthy `sqlmap_scan`,
- raw commands with destructive or high-blast-radius behavior.

Before confirmation request, provide:
- exact action,
- objective,
- expected impact,
- assumptions/prerequisites,
- telemetry and detection surfaces (host/network/identity/EDR-SIEM).

## Reporting Requirements

For each finding, include:
- title and severity,
- affected target and service/port/tool context,
- exact MCP tool calls with arguments and outputs,
- observed impact and exploitability,
- detection opportunities,
- remediation options with tradeoffs.

If no issue is found, report negative validation evidence and confidence level.
