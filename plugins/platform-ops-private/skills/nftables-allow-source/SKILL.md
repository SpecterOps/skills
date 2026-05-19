---
name: nftables-allow-source
description: Add a source IP or CIDR to nftables using the working method from this repo session: live top-of-`input` insertion with `nft -a` verification first, then persistent config update and reload.
---

# Nftables Allow Source

Use this skill to add a source IP or CIDR to nftables using the method that worked in this repo session:
- inspect the live `input` chain with `nft -a`
- insert a source allow rule at the top of the live `input` chain
- verify the live rule immediately
- add the same source allow rule to `/etc/nftables.conf` in the `input` chain
- reload the ruleset and verify config and live state match

Do not use a config-first workflow here. The working method is live `input` insertion first, persistence second.

## Direct Triggers

Use this skill when the task mentions any of the following:
- add an nftables allow rule
- allow inbound from an IP
- whitelist an IP in nftables
- add a source address to the firewall
- insert an nft rule at the top
- use `nft -a` handles

## Input Contract

Accept input as:
`HOST SOURCE [MODE]`

Mode:
- `plan`: produce the command sequence only
- `execute` (default): inspect, insert, and verify the live rule

Examples:
- `$nftables-allow-source bastion 203.0.113.42 execute`
- `$nftables-allow-source 198.51.100.25 203.0.113.42/32 plan`
- `$nftables-allow-source edge-firewall 198.51.100.0/24 execute`

## Preconditions

1. Confirm the host is in scope and operator-controlled.
2. Confirm SSH or console access exists before changing the firewall.
3. Confirm `nft` is installed and the host is actually using nftables.
4. Prefer live insertion into the `input` chain before any persistent edit.

## Execution Workflow

1. Inspect the live `input` chain with handles.

```bash
sudo nft -a list chain inet filter input
```

Use this to:
- confirm the chain exists
- see current rule order
- identify whether a matching source rule already exists

2. Verify whether the source is already allowed.
- If already present in the live chain, do not insert a duplicate.
- Record existing handle and position if present.

3. Insert the allow rule at the top of the live `input` chain.

Preferred live insertion pattern:

```bash
sudo nft insert rule inet filter input position 0 ip saddr <SOURCE> accept
```

This is the working method and should be preferred over editing `/etc/nftables.conf` first.

4. Verify the live `input` chain immediately.

```bash
sudo nft -a list chain inet filter input
```

Success means the new `ip saddr <SOURCE> accept` rule appears at the top of the `input` chain before the rest of the policy logic.

5. Persist the same rule in `/etc/nftables.conf`.
- insert `ip saddr <SOURCE> accept comment "Authorized External IP"` immediately after:
  - `type filter hook input priority filter; policy drop;`
- do not rely on a broad grep for the source IP elsewhere in the file; check the `input` chain specifically
- if `/etc/nftables.conf` is empty or corrupted, restore from the latest backup before editing
- back up the file before changing it

6. Reload and verify.
- reload with:
  - `sudo nft -f /etc/nftables.conf`
- verify both:
  - `sudo sed -n '/chain input {/,/}/p' /etc/nftables.conf`
  - `sudo nft -a list chain inet filter input`
- confirm the persistent and live rules both contain the source allow at the top of the `input` chain

## Command Patterns

### Live chain inspection

```bash
sudo nft -a list chain inet filter input
```

### Live top-of-chain insertion

```bash
sudo nft insert rule inet filter input position 0 ip saddr 203.0.113.42 accept
```

### Persistent config backup

```bash
sudo cp /etc/nftables.conf /etc/nftables.conf.bak-$(date +%Y%m%d%H%M%S)
```

### Persistent input-chain insertion

```bash
sudo sed -i '/type filter hook input priority filter; policy drop;/a\        ip saddr 203.0.113.42 accept comment "Authorized External IP"' /etc/nftables.conf
```

### Persistent config reload

```bash
sudo nft -f /etc/nftables.conf
```

### Post-reload verification

```bash
sudo sed -n '/chain input {/,/}/p' /etc/nftables.conf
sudo nft -a list chain inet filter input
```

## Prohibited Method

Do not use these approaches as the default workflow for this skill:
- editing `/etc/nftables.conf` first and assuming reload will be safe
- checking only whether the source IP exists somewhere in the file instead of in the `input` chain
- adding the exception only to the `management` chain when the operator wants a host-wide source exception
- broad text-rewrite methods that can blank or corrupt `/etc/nftables.conf`

## OPSEC Gate

Require explicit operator confirmation before:
- broad rules such as `0.0.0.0/0`
- wide CIDR additions that materially expand exposure
- deleting or reordering existing firewall controls
- reloading or restarting nftables on production-like hosts when access risk is non-trivial

Before requesting approval, include:
- exact rule change
- objective
- expected impact
- rollback plan
- possible connectivity risk

## Reporting Requirements

For each run, include:
- target host
- live chain modified: `inet filter input`
- source IP/CIDR added
- exact commands used
- pre-change live chain output
- post-change live chain output
- persistent `input`-chain config snippet after edit
- whether the rule is live only or also persistent
- any remaining follow-up needed to reconcile config and runtime state

## Troubleshooting Note

If a service is still unreachable after the source allow rule is added:
1. verify the service is actually listening on the destination host
2. compare reachability of the blocked port against a temporary listener on an alternate port on the same host
3. if the alternate port succeeds while the original port fails, do not attribute the failure to nftables alone
4. report that the environment or path may specifically disallow the original port
