# SpecterOps Skills

Reusable agent skills, plugins, and agent definitions for SpecterOps.

## Use With Claude Code

Each plugin lives under `plugins/<name>/` and includes a Claude Code manifest at `.claude-plugin/plugin.json`.

For local development:

```text
/plugin marketplace add /Users/<user>/Projects/skills
/plugin install <plugin-name>@specterops-skills
```

For a hosted repository:

```text
/plugin marketplace add SpecterOps/skills
/plugin install <plugin-name>@specterops-skills
```

## Use With Codex

Each plugin includes a Codex manifest at `.codex-plugin/plugin.json`.

```bash
codex plugin marketplace add /Users/<user>/Projects/skills
# or
codex plugin marketplace add SpecterOps/skills
```

Then open Codex and install from `/plugins`.

### Codex MCP setup

Codex officially supports MCP servers through declarative `mcp_servers` configuration. This repository no longer ships MCP runner or first-run installer scripts. Install or clone each external MCP server yourself, then point Codex at that server with `command`, `args`, and optional `env` values in `~/.codex/config.toml` or project `.codex/config.toml`.

1. Install or refresh this marketplace in Codex:

   ```bash
   codex plugin marketplace add /Users/<user>/Projects/skills
   # or
   codex plugin marketplace add SpecterOps/skills
   ```

   Then install the relevant plugins from `/plugins`.

2. Configure MCP servers directly in Codex. Example BloodHound and Ghostwriter stdio configurations:

   ```toml
   [mcp_servers.bloodhound_mcp]
   command = "uv"
   args = ["--directory", "/path/to/bloodhound-mcp", "run", "main.py"]

   [mcp_servers.bloodhound_mcp.env]
   BLOODHOUND_DOMAIN = "YOUR_DOMAIN"
   BLOODHOUND_TOKEN_ID = "YOUR_TOKEN_ID"
   BLOODHOUND_TOKEN_KEY = "YOUR_TOKEN_KEY"
   BLOODHOUND_SCHEME = "https"
   BLOODHOUND_PORT = "443"

   [mcp_servers.ghostwriter]
   command = "uv"
   args = ["--directory", "/path/to/GhostWriterMCP", "run", "python", "-m", "ghostwritermcp.server"]

   [mcp_servers.ghostwriter.env]
   GHOSTWRITER_URL = "https://ghostwriter.example.com/"
   GHOSTWRITER_API_KEY = "YOUR_API_KEY"
   GHOSTWRITER_CA_BUNDLE = "/path/to/ca-bundle.crt"
   GHOSTWRITER_OPLOG_ID = "123"
   GHOSTWRITER_OPERATOR = "your-callsign"
   GHOSTWRITER_SOURCE_IP = "10.0.0.5"
   ```

3. Configure Binary Ninja MCP with the command or endpoint documented by your BinjaMCP installation. For stdio servers, the Codex shape is:

   ```toml
   [mcp_servers.binary_ninja]
   command = "/path/to/binja-mcp-server"
   args = []
   ```

Restart Codex after changing MCP configuration, then confirm the tools appear under `/mcp` before relying on MCP-assisted skills.

## Use With npx skills

Use `npx skills` when you only want to install skill instructions. This does not install full plugin behavior such as MCP config, Claude commands, hooks, or agent definitions.

```bash
npx skills add SpecterOps/skill --list
npx skills add SpecterOps/skills --skill <skill-name> --agent claude-code --agent codex --global
```

For local testing:

```bash
npx skills add /Users/<user>/Projects/skills --list
```

## Plugins

| Plugin | Codex | Claude Code | MCP | Description |
|---|---:|---:|---:|---|
| [appsec-assessment](plugins/appsec-assessment/README.md) | Yes | Yes | - | Application and code security assessment workflows for Specter Codex. |
| [bloodhound-analysis](plugins/bloodhound-analysis/README.md) | Yes | Yes | Manual | BloodHound, AzureHound, GitHound/JamfHound/OktaHound OpenGraph attack-path query workflows, SCIM bridge references, and optional BloodHound MCP packaging. |
| [c2-extension-development](plugins/c2-extension-development/README.md) | Yes | Yes | - | Cobalt Strike Aggressor, BOF development, and C2 extension reference workflows. |
| [code-review-and-qa](plugins/code-review-and-qa/README.md) | Yes | Yes | - | Code review and web application QA workflows for Specter Codex. |
| [codex-observability](plugins/codex-observability/README.md) | Yes | Yes | - | Codex activity reporting and telemetry workflows. |
| [course-conversion-internal](plugins/course-conversion-internal/README.md) | Yes | Yes | - | Internal-only staged course wiki migration workflows. |
| [engineering-workflows](plugins/engineering-workflows/README.md) | Yes | Yes | - | Core engineering scaffolding, repository hygiene, and implementation workflows for Specter Codex. |
| [external-recon](plugins/external-recon/README.md) | Yes | Yes | - | Passive external reconnaissance and exposure discovery workflows for Specter Codex. |
| [identity-assessment-core](plugins/identity-assessment-core/README.md) | Yes | Yes | - | Core identity, Active Directory, Windows, and internal assessment workflows. |
| [ludus](plugins/ludus/README.md) | Yes | Yes | - | Ludus cyber range configuration and management skill with full API, CLI, and deployment references |
| [mythic-implant](plugins/mythic-implant/README.md) | Yes | Yes | - | Mythic C2 framework implant development skill with agent message protocols, payload type definitions, and step-by-step build workflow |
| [offensive-tooling](plugins/offensive-tooling/README.md) | Yes | Yes | - | Security tool scaffolding and proof-of-concept development workflows. |
| [openhound-collector-development](plugins/openhound-collector-development/README.md) | Yes | Yes | - | OpenHound collector template support package with the embedded OpenHound development skill. |
| [payloads](plugins/payloads/README.md) | Yes | Yes | - | Reusable Electron payload packaging, persistence, audit, and discovery workflows. |
| [platform-ops-private](plugins/platform-ops-private/README.md) | Yes | Yes | - | Private platform, SSH, tunnel, and firewall operation workflows. |
| [report-writing](plugins/report-writing/README.md) | Yes | Yes | Manual | Finding, report drafting, Ghostwriter MCP, and operation log workflows for security assessment deliverables. |
| [research-workflows](plugins/research-workflows/README.md) | Yes | Yes | - | Source-backed research and synthesis workflows for Specter Codex. |
| [reverse-engineering](plugins/reverse-engineering/README.md) | Yes | Yes | Manual | Reverse engineering workflows and MCP-assisted binary analysis, starting with Binary Ninja. |
| [sccm-assessment](plugins/sccm-assessment/README.md) | Yes | Yes | - | Microsoft Configuration Manager reconnaissance and takeover validation workflows. |
| [social-engineering](plugins/social-engineering/README.md) | Yes | Yes | - | Social engineering research and phishing pretext workflows. |
| [timeline-evidence](plugins/timeline-evidence/README.md) | Yes | Yes | - | Pentest timeline ingestion, consolidation, and evidence packaging workflows. |
| [windows-tradecraft](plugins/windows-tradecraft/README.md) | Yes | - | - | Windows execution, persistence, and COM proxy validation workflows. |

## Skills

| Skill | Plugin | Path |
|---|---|---|
| `secret-scan` | `appsec-assessment` | [SKILL.md](plugins/appsec-assessment/skills/secret-scan/SKILL.md) |
| `security-review` | `appsec-assessment` | [SKILL.md](plugins/appsec-assessment/skills/security-review/SKILL.md) |
| `webapp-review` | `appsec-assessment` | [SKILL.md](plugins/appsec-assessment/skills/webapp-review/SKILL.md) |
| `azurehound-analysis` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/azurehound-analysis/SKILL.md) |
| `bloodhound-ad-analysis` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/bloodhound-ad-analysis/SKILL.md) |
| `bloodhound-analysis` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/bloodhound-analysis/SKILL.md) |
| `bloodhound-opengraph` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/bloodhound-opengraph/SKILL.md) |
| `bloodhound-query` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/bloodhound-query/SKILL.md) |
| `openhound-github` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/openhound-github/SKILL.md) |
| `openhound-jamf` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/openhound-jamf/SKILL.md) |
| `openhound-okta` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/openhound-okta/SKILL.md) |
| `beacon-object-file-development` | `c2-extension-development` | [SKILL.md](plugins/c2-extension-development/skills/beacon-object-file-development/SKILL.md) |
| `c2-bof-development` | `c2-extension-development` | [SKILL.md](plugins/c2-extension-development/skills/c2-bof-development/SKILL.md) |
| `cobalt-strike-aggressor-development` | `c2-extension-development` | [SKILL.md](plugins/c2-extension-development/skills/cobalt-strike-aggressor-development/SKILL.md) |
| `cobalt-strike-aggressor-reference` | `c2-extension-development` | [SKILL.md](plugins/c2-extension-development/skills/cobalt-strike-aggressor-reference/SKILL.md) |
| `code-review` | `code-review-and-qa` | [SKILL.md](plugins/code-review-and-qa/skills/code-review/SKILL.md) |
| `webapp-qa` | `code-review-and-qa` | [SKILL.md](plugins/code-review-and-qa/skills/webapp-qa/SKILL.md) |
| `codex-activity-report` | `codex-observability` | [SKILL.md](plugins/codex-observability/skills/codex-activity-report/SKILL.md) |
| `opentelemetry-codex` | `codex-observability` | [SKILL.md](plugins/codex-observability/skills/opentelemetry-codex/SKILL.md) |
| `course-wiki-migration-orchestrator` | `course-conversion-internal` | [SKILL.md](plugins/course-conversion-internal/skills/course-wiki-migration-orchestrator/SKILL.md) |
| `course-wiki-stage1-scaffold` | `course-conversion-internal` | [SKILL.md](plugins/course-conversion-internal/skills/course-wiki-stage1-scaffold/SKILL.md) |
| `course-wiki-stage2-content-migration` | `course-conversion-internal` | [SKILL.md](plugins/course-conversion-internal/skills/course-wiki-stage2-content-migration/SKILL.md) |
| `course-wiki-stage3-qa` | `course-conversion-internal` | [SKILL.md](plugins/course-conversion-internal/skills/course-wiki-stage3-qa/SKILL.md) |
| `git-cleanup` | `engineering-workflows` | [SKILL.md](plugins/engineering-workflows/skills/git-cleanup/SKILL.md) |
| `git-merge` | `engineering-workflows` | [SKILL.md](plugins/engineering-workflows/skills/git-merge/SKILL.md) |
| `git-preflight` | `engineering-workflows` | [SKILL.md](plugins/engineering-workflows/skills/git-preflight/SKILL.md) |
| `readme-generation` | `engineering-workflows` | [SKILL.md](plugins/engineering-workflows/skills/readme-generation/SKILL.md) |
| `scaffold-python` | `engineering-workflows` | [SKILL.md](plugins/engineering-workflows/skills/scaffold-python/SKILL.md) |
| `osint-recon` | `external-recon` | [SKILL.md](plugins/external-recon/skills/osint-recon/SKILL.md) |
| `shodan` | `external-recon` | [SKILL.md](plugins/external-recon/skills/shodan/SKILL.md) |
| `nmap-parse` | `identity-assessment-core` | [SKILL.md](plugins/identity-assessment-core/skills/nmap-parse/SKILL.md) |
| `ludus-development` | `ludus` | [SKILL.md](plugins/ludus/skills/ludus-development/SKILL.md) |
| `mythic-implant-development` | `mythic-implant` | [SKILL.md](plugins/mythic-implant/skills/mythic-implant-development/SKILL.md) |
| `scaffold-security` | `offensive-tooling` | [SKILL.md](plugins/offensive-tooling/skills/scaffold-security/SKILL.md) |
| `openhound-collector-development` | `openhound-collector-development` | [SKILL.md](plugins/openhound-collector-development/skills/openhound-collector-development/SKILL.md) |
| `electron-app-audit` | `payloads` | [SKILL.md](plugins/payloads/skills/electron-app-audit/SKILL.md) |
| `electron-candidate-discovery` | `payloads` | [SKILL.md](plugins/payloads/skills/electron-candidate-discovery/SKILL.md) |
| `electron-install-persistence` | `payloads` | [SKILL.md](plugins/payloads/skills/electron-install-persistence/SKILL.md) |
| `electron-squirrel-repackage` | `payloads` | [SKILL.md](plugins/payloads/skills/electron-squirrel-repackage/SKILL.md) |
| `nftables-allow-source` | `platform-ops-private` | [SKILL.md](plugins/platform-ops-private/skills/nftables-allow-source/SKILL.md) |
| `proxychains-tunnel` | `platform-ops-private` | [SKILL.md](plugins/platform-ops-private/skills/proxychains-tunnel/SKILL.md) |
| `ssh-ops` | `platform-ops-private` | [SKILL.md](plugins/platform-ops-private/skills/ssh-ops/SKILL.md) |
| `finding-report` | `report-writing` | [SKILL.md](plugins/report-writing/skills/finding-report/SKILL.md) |
| `ghostwriter-mcp` | `report-writing` | [SKILL.md](plugins/report-writing/skills/ghostwriter-mcp/SKILL.md) |
| `ghostwriter-oplog` | `report-writing` | [SKILL.md](plugins/report-writing/skills/ghostwriter-oplog/SKILL.md) |
| `source-research` | `research-workflows` | [SKILL.md](plugins/research-workflows/skills/source-research/SKILL.md) |
| `binary-ninja-mcp-analysis` | `reverse-engineering` | [SKILL.md](plugins/reverse-engineering/skills/binary-ninja-mcp-analysis/SKILL.md) |
| `sccm-recon` | `sccm-assessment` | [SKILL.md](plugins/sccm-assessment/skills/sccm-recon/SKILL.md) |
| `sccm-takeover-relay` | `sccm-assessment` | [SKILL.md](plugins/sccm-assessment/skills/sccm-takeover-relay/SKILL.md) |
| `sccmhunter-install-local` | `sccm-assessment` | [SKILL.md](plugins/sccm-assessment/skills/sccmhunter-install-local/SKILL.md) |
| `credential-harvest-landing-page-copy` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/credential-harvest-landing-page-copy/SKILL.md) |
| `phishing-campaign-builder` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/phishing-campaign-builder/SKILL.md) |
| `phishing-email-html` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/phishing-email-html/SKILL.md) |
| `phishing-pretext` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/phishing-pretext/SKILL.md) |
| `pretext-brainstormer` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/pretext-brainstormer/SKILL.md) |
| `vishing-pretext` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/vishing-pretext/SKILL.md) |
| `timeline-asciinema` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-asciinema/SKILL.md) |
| `timeline-cobaltstrike` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-cobaltstrike/SKILL.md) |
| `timeline-consolidator` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-consolidator/SKILL.md) |
| `timeline-ghostwriter` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-ghostwriter/SKILL.md) |
| `timeline-markdown-notes` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-markdown-notes/SKILL.md) |
| `timeline-mythic` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-mythic/SKILL.md) |
| `timeline-pdf-notes` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-pdf-notes/SKILL.md) |
| `timeline-workflow` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-workflow/SKILL.md) |
| `com-proxy-triage` | `windows-tradecraft` | [SKILL.md](plugins/windows-tradecraft/skills/com-proxy-triage/SKILL.md) |

## Standalone Skills

| Skill | Path |
|---|---|
| - | No standalone skills currently live under `skills/`. |

## Agents

| Agent | Path |
|---|---|
| `architect` | [agents/architect.toml](agents/architect.toml) |
| `bloodhound-analyst` | [agents/bloodhound-analyst.toml](agents/bloodhound-analyst.toml) |
| `code-reviewer` | [agents/code-reviewer.toml](agents/code-reviewer.toml) |
| `domain-ops` | [agents/domain-ops.toml](agents/domain-ops.toml) |
| `exploit-dev` | [agents/exploit-dev.toml](agents/exploit-dev.toml) |
| `internal-network-recon` | [agents/internal-network-recon.toml](agents/internal-network-recon.toml) |
| `osint-recon` | [agents/osint-recon.toml](agents/osint-recon.toml) |
| `planner` | [agents/planner.toml](agents/planner.toml) |
| `poc-dev` | [agents/poc-dev.toml](agents/poc-dev.toml) |
| `report-writer` | [agents/report-writer.toml](agents/report-writer.toml) |
| `researcher` | [agents/researcher.toml](agents/researcher.toml) |
| `sccm-ops` | [agents/sccm-ops.toml](agents/sccm-ops.toml) |
| `security-researcher` | [agents/security-researcher.toml](agents/security-researcher.toml) |
| `ssh-operator` | [agents/ssh-operator.toml](agents/ssh-operator.toml) |
| `winternals` | [agents/winternals.toml](agents/winternals.toml) |

## MCP-Aware Plugins

| MCP Server | Plugin | Configuration |
|---|---|---|
| `bloodhound_mcp` | `bloodhound-analysis` | Configure directly in Codex with `uv --directory /path/to/bloodhound-mcp run main.py`. |
| `ghostwriter` | `report-writing` | Configure directly in Codex with `uv --directory /path/to/GhostWriterMCP run python -m ghostwritermcp.server`. |
| `binary_ninja` | `reverse-engineering` | Configure directly in Codex with the command or endpoint documented by the BinjaMCP server. |
