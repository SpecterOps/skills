---
name: iac-attack-surface
description: Hunt for exploitable infrastructure-as-code misconfigurations from an offensive security perspective. Use for Terraform, Docker, Compose, Kubernetes, Ansible, and cloud-init/user-data reviews focused on exposed services, privilege paths, secrets, unsafe defaults, workload escape, lateral movement, persistence, and assessment-ready findings.
metadata:
  author: "SpecterOps"
---

# IaC Attack Surface

Hunt through infrastructure-as-code as an authorized offensive security assessment. The goal is to find misconfigurations that create concrete attacker opportunities: initial access, credential exposure, privilege escalation, lateral movement, workload escape, persistence, data exposure, or detection bypass.

This is a misconfiguration review workflow, not an exploitation workflow. Do not execute attacks or change infrastructure unless the user explicitly asks for follow-up implementation.

## Input Contract

Accept natural language or:

`$iac-attack-surface [scope] [path]`

Supported scopes:
- `terraform`
- `docker`
- `compose`
- `kubernetes`
- `ansible`
- `cloud-init`
- `all` (default)

Examples:
- `$iac-attack-surface`
- `$iac-attack-surface terraform ~/engagement/infra`
- `$iac-attack-surface compose .`
- `Review this Terraform for exploitable misconfigurations and privilege paths`
- `Find offensive issues in these Kubernetes manifests`

## Review Lens

Prioritize exploitable misconfigurations over generic best-practice advice. Start from attacker questions:
- What is reachable from the internet, a compromised user, a compromised workload, or a low-privileged cloud principal?
- Which identities can become more privileged, assume broader roles, read secrets, deploy code, or mutate infrastructure?
- Which services expose credentials, metadata, host access, container escape paths, or admin interfaces?
- Which defaults create unexpected trust between networks, namespaces, projects, accounts, or environments?
- Which bootstrap paths could be abused for persistence or supply-chain insertion?

For each finding, explain the attacker utility, prerequisites, blast radius, safe validation method, and remediation. Always distinguish confirmed evidence from inference. If IaC alone cannot prove runtime exposure or effective permissions, list the exact evidence needed.

## Discovery

Scan the target path for:

| Pattern | Type |
|---|---|
| `*.tf`, `*.tfvars`, `.terraform.lock.hcl` | Terraform |
| `Dockerfile*`, `.dockerignore` | Docker |
| `docker-compose*.yml`, `compose*.yml` | Docker Compose |
| `*.yaml`, `*.yml` with `apiVersion:` | Kubernetes |
| `playbook*.yml`, `roles/`, `inventory*`, `ansible.cfg` | Ansible |
| `cloud-init*.yml`, `user-data*`, launch templates | cloud-init / user data |
| `.env`, `.env.*`, `*.tfstate`, `*.tfvars` | sensitive artifacts |

Exclude generated dependency folders unless they are the subject of the review: `.terraform/`, `node_modules/`, `.venv/`, `vendor/`.

## Offensive Misconfiguration Checks

### 1. Initial Access And Exposed Services

Look for:
- public ingress to management ports: SSH, RDP, WinRM, Kubernetes API, Docker API, databases, CI/CD, admin panels, dashboards, and object storage consoles,
- broad CIDRs such as `0.0.0.0/0`, `::/0`, RFC1918-wide rules, or unbounded security-group references,
- public IPs, public load balancers, public buckets, public registries, or exposed ingress resources on systems that should be internal,
- TLS disabled, weak auth assumptions, anonymous access, default credentials, or unauthenticated health/debug endpoints,
- cloud metadata exposure paths such as SSRF-reachable workloads with instance roles or managed identities.

### 2. Identity And Privilege Paths

Look for:
- IAM policies with wildcard actions or resources,
- broad assume-role trust, external ID gaps, or cross-account trust issues,
- service accounts with cluster-admin, privileged SCC/PSP-equivalent access, or unnecessary token mounting,
- instance profiles or managed identities attached to internet-exposed workloads,
- CI/CD roles that can deploy, assume roles, read secrets, modify pipelines, write container images, or mutate infrastructure broadly,
- low-privileged roles that can pass roles, attach policies, create access keys, update trust policies, modify user data, or create privileged workloads.

### 3. Secrets And Sensitive Artifacts

Look for:
- hardcoded keys, tokens, passwords, private keys, connection strings, and certificates,
- committed `.env`, `terraform.tfvars`, state files, kubeconfigs, inventories, and vault password files,
- secrets passed through Docker `ARG`, `ENV`, user data, startup scripts, or Kubernetes `Secret` manifests,
- outputs, logs, generated templates, or CI variables that expose credentials, bootstrap tokens, kubeconfigs, database URLs, or connection material,
- Terraform state backends, artifact stores, or deployment buckets that may leak secrets if public, weakly scoped, or readable by broad identities.

### 4. Workload Escape And Host Control

Look for:
- Docker socket mounts, `privileged: true`, host networking, host PID/IPC, broad hostPath mounts,
- containers running as root without a reason,
- missing read-only root filesystem or dropped capabilities for exposed workloads,
- Kubernetes pods with dangerous capabilities, hostPath mounts, node selectors that target sensitive nodes, or service account token exposure,
- Compose services with sensitive host mounts such as `/`, `/var/run`, `/etc`, `/home`, cloud credential folders, SSH keys, or kubeconfigs,
- Ansible or bootstrap tasks that grant passwordless sudo, add broad SSH keys, disable security controls, or relax host firewalls.

### 5. Lateral Movement And Segmentation

Look for:
- default or shared networks connecting unrelated workloads,
- database or admin services reachable from broad application tiers,
- permissive egress enabling command-and-control or credential replay paths,
- shared service accounts, SSH keys, or deployment credentials across trust zones,
- security group, firewall, Kubernetes NetworkPolicy, or routing gaps that let one compromised workload reach high-value systems,
- environment mixing where dev/test identities, networks, or images can reach production systems,
- database, Redis, message queue, NFS/SMB, LDAP, or identity endpoints reachable from broad workload tiers.

### 6. Persistence And Bootstrap Abuse

Look for:
- user-data scripts, startup scripts, cron/systemd units, cloud-init, or Ansible tasks that install agents, keys, or remote access,
- long-lived access keys, static SSH authorized keys, or baked credentials,
- image build steps that fetch unsigned scripts or packages,
- mutable tags such as `latest` or unpinned installers that create supply-chain insertion points,
- infrastructure paths that let an attacker update launch templates, images, task definitions, admission controllers, or deployment manifests to regain access.

### 7. Unsafe Defaults And Supply Chain

Look for:
- unpinned base images, package installs, Terraform providers, Helm charts, Ansible Galaxy roles, or remote modules,
- `curl | sh`, unauthenticated downloads, unsigned binaries, or Git checkouts from mutable branches,
- Docker builds that copy the full repo without `.dockerignore`, include `.git`, secrets, local credentials, or test artifacts,
- Terraform modules sourced from mutable refs or untrusted locations.

### 8. Detection And Response Gaps

Look for:
- absent or disabled audit logs, flow logs, CloudTrail-equivalent logging, Kubernetes audit policy, container logs, or identity-provider logs,
- missing alerting around IAM changes, public exposure, secrets access, admin login, deployment changes, and security-control disablement,
- lack of immutable logging or centralized log shipping for high-value environments,
- retention gaps that would prevent reconstructing attacker activity during an assessment or incident.

## Attack Path Mapping

After identifying candidate misconfigurations, group related evidence into practical paths:

1. **Initial access**: public service, exposed secret, weak auth, public storage, or vulnerable management plane.
2. **Credential access**: state file, env var, secret manifest, metadata token, host mount, CI secret, or kubeconfig.
3. **Privilege escalation**: overbroad IAM/RBAC, role passing, deploy rights, host escape, admin service account, or pipeline mutation.
4. **Lateral movement**: flat network, permissive egress, shared keys, exposed internal services, or cross-environment trust.
5. **Persistence**: launch templates, user data, startup scripts, image pipelines, scheduled tasks, deploy hooks, or long-lived keys.
6. **Impact**: data store access, identity takeover, production deployment control, logging blind spot, or infrastructure destruction.

Prefer findings that complete or materially advance one of these paths. Do not bury the report in low-value hardening notes unless they support an attacker path.

## Severity Model

Use assessment impact:

- **Critical**: exploitable public admin access, exposed high-value credentials, direct privilege escalation to environment control, or a complete path to production/high-value impact.
- **High**: strong attacker path with plausible prerequisite access, broad lateral movement, persistence-ready bootstrap, workload escape, or high-impact detection gap.
- **Medium**: misconfiguration that materially improves attacker options but needs additional conditions or runtime confirmation.
- **Low**: hygiene issue with limited direct attacker utility, or a weak signal that should be tracked but not treated as a finding alone.

## Report Format

Lead with findings, ordered by severity.

```markdown
## IaC Attack Surface

### Summary
- Critical: 0
- High: 0
- Medium: 0
- Low: 0
- Files reviewed: N
- Scope: terraform|docker|compose|kubernetes|ansible|cloud-init|all
- Primary paths: initial access|credential access|privilege escalation|lateral movement|persistence|impact

### Findings

#### HIGH-1: Internet-exposed instance profile on SSH-accessible host creates cloud privilege path
**File:** `infra/main.tf:42`
**Evidence:** Security group allows `0.0.0.0/0` to TCP/22 and the instance has `admin_instance_profile`.
**Attack path:** Compromise of SSH credentials could expose cloud permissions attached to the instance.
**Prerequisites:** Network reachability and valid SSH credentials or exploitable SSH-facing service.
**Validation:** Confirm runtime security group attachment and effective role permissions in cloud inventory.
**Remediation:** Restrict management ingress, move access behind a bastion/VPN, and reduce instance profile permissions.
**Path stage:** Initial access -> credential access -> privilege escalation

### Attack Path Notes
- Summarize the most important chained paths, even if individual findings are reported separately.

### Evidence Needed
- List runtime evidence needed for inferred risks, such as effective IAM policy, live security group attachment, or current Kubernetes admission controls.
```

## Safety And Scope

Before recommending validation, confirm the target belongs to the active engagement or operator-controlled environment. Prefer read-only validation commands and inventory checks. If a validation step could change state, increase traffic, trigger alerts, or access sensitive data, present it as a plan and ask for confirmation first.
