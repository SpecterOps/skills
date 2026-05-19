---
name: ssh-ops
description: Establish and operate scoped SSH sessions for authorized remote command execution with full evidence capture. Use when the operator provides SSH-accessible targets/credentials and Codex must execute commands on a remote host as an interactive user while enforcing OPSEC gating and safe-check behavior.
---

# SSH Ops

Use controlled SSH workflows to execute remote commands, keep session state stable, and return exact command/output evidence.

## Input Contract

Accept input as: `HOST USER [MODE] [NOISE]`

Mode:
- `plan`: produce command sequence and expected outcomes only
- `execute` (default): establish session and run commands

Noise:
- `low` (default): read-only validation and bounded enumeration
- `medium`: broader but still non-destructive enumeration
- `high`: disruptive or high-telemetry operations; explicit approval required

## Session Ownership Rule

When multiple agents are active, route SSH execution through the dedicated `ssh_operator` agent only.
- Do not allow multiple agents to write to the same SSH session concurrently.
- Keep one owner per session and serialize command execution.

## Default Workflow

1. Validate scope and auth assumptions.
2. Run safe connectivity check first:
```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new <user>@<host> 'hostname; id; date -u'
```
3. Run bounded read-only commands before any escalation.
4. If interactive state is required, open one interactive session and execute command batches sequentially.
5. Capture full stdout/stderr and exit status for each command.
6. Return findings, blockers, and next safe step.

## Authentication Handling

- Prefer SSH keys and `ssh-agent`.
- Do not log raw credentials in output.
- Do not run brute-force or repeated auth guessing when login fails.

## OPSEC Gate

Require explicit operator confirmation before:
- destructive commands (`rm`, service stop/restart, system reconfiguration),
- high-noise discovery across many hosts from the remote session,
- actions likely to disrupt availability.

Before requesting confirmation, provide:
- exact action,
- security objective,
- expected impact,
- prerequisites/assumptions,
- likely telemetry and blast radius.

## Refusal and Safe-Check Handling

- Treat failed auth, access denied, host-key errors, and policy blocks as safe-check outcomes.
- Do not auto-escalate after refusal or failure.
- Report refusal/failure cause and propose the lowest-noise alternative next command.
- Only retry blocked operations after operator approval.

## Evidence Requirements

For each command executed, record:
- UTC timestamp,
- host/user/session context,
- exact command string,
- stdout/stderr and exit status,
- interpretation and confidence.
