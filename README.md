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
   [mcp_servers.binary_ninja_mcp]
   command = "npx"
   args = ["-y", "binary-ninja-mcp", "--host", "localhost", "--port", "9009"]
   ```

Restart Codex after changing MCP configuration, then confirm the tools appear under `/mcp` before relying on MCP-assisted skills.

## Use With npx skills

Use `npx skills` when you only want to install skill instructions. This does not install full plugin behavior such as MCP config, Claude commands, hooks, or agent definitions.

```bash
npx skills add SpecterOps/skills --list
npx skills add SpecterOps/skills --skill <skill-name> --agent claude-code --agent codex --global
```

For local testing:

```bash
npx skills add /Users/<user>/Projects/skills --list
```

## Contributing

Start with [CONTRIBUTING.md](CONTRIBUTING.md). It covers the supported development
environment, setup and validation commands, plugin metadata scaffolding, pull
request expectations, and where to ask for help.

## Plugins

<!-- BEGIN GENERATED PLUGIN CATALOG: run `just generate-catalog` -->

| Plugin | Codex | Claude Code | MCP | Description |
|---|---:|---:|---:|---|
| [workflows-development](plugins/workflows-development/README.md) | Yes | Yes | - | Development scaffolding, repository hygiene, security tooling, and implementation workflows for Specter Codex. |
| [code-review-and-qa](plugins/code-review-and-qa/README.md) | Yes | Yes | - | Code review and web application QA workflows for Specter Codex. |
| [workflows-research](plugins/workflows-research/README.md) | Yes | Yes | - | Source-backed research and synthesis workflows for Specter Codex. |
| [ops-reconnaissance](plugins/ops-reconnaissance/README.md) | Yes | Yes | - | Reconnaissance, OSINT, service enumeration, and exposure discovery workflows for Specter Codex. |
| [ops-appsec](plugins/ops-appsec/README.md) | Yes | Yes | - | Application and code security assessment workflows for Specter Codex. |
| [ops-sccm](plugins/ops-sccm/README.md) | Yes | Yes | - | Microsoft Configuration Manager reconnaissance and takeover validation workflows. |
| [bloodhound](plugins/bloodhound/README.md) | Yes | Yes | Manual | BloodHound, AzureHound, GitHound/JamfHound/OktaHound OpenGraph attack-path query workflows, SCIM bridge references, and optional BloodHound MCP packaging. |
| [payloads](plugins/payloads/README.md) | Yes | Yes | - | Reusable Electron payload packaging, persistence, audit, and discovery workflows. |
| [c2-extensions](plugins/c2-extensions/README.md) | Yes | Yes | - | Beacon Object File development and reusable C2 extension workflows. |
| [report-drafting](plugins/report-drafting/README.md) | Yes | Yes | Manual | Finding, report drafting, Ghostwriter MCP, and operation log workflows for security assessment deliverables. |
| [reverse-engineering](plugins/reverse-engineering/README.md) | Yes | Yes | Manual | Reverse engineering workflows and MCP-assisted binary analysis for Binary Ninja, Ghidra, and related tooling. |
| [report-timeline](plugins/report-timeline/README.md) | Yes | Yes | - | Report timeline ingestion, consolidation, and evidence packaging workflows. |
| [codex-observability](plugins/codex-observability/README.md) | Yes | Yes | - | Codex activity reporting and telemetry workflows. |
| [ops-infrastructure](plugins/ops-infrastructure/README.md) | Yes | Yes | - | Infrastructure operations, SSH, tunnel, firewall, and offensive IaC attack-surface workflows. |
| [internal-training-course](plugins/internal-training-course/README.md) | Yes | Yes | - | Internal training course wiki migration, scaffolding, content migration, and QA workflows. |
| [social-engineering](plugins/social-engineering/README.md) | Yes | Yes | - | Social engineering research and phishing pretext workflows. |
| [ludus](plugins/ludus/README.md) | Yes | Yes | - | Ludus cyber range configuration and management skill with full API, CLI, and deployment references |
| [c2-mythic](plugins/c2-mythic/README.md) | Yes | Yes | - | Mythic C2 framework implant and C2 profile development workflows with agent message protocols, payload type definitions, and listener/profile guidance. |
| [tradecraft-windows](plugins/tradecraft-windows/README.md) | Yes | - | - | Windows execution, persistence, and COM proxy validation workflows. |
| [ops-adcs](plugins/ops-adcs/README.md) | Planned | - | - | Active Directory Certificate Services assessment and attack-path validation workflows. Planned; no capability is currently packaged. |
| [ops-mssql](plugins/ops-mssql/README.md) | Planned | - | - | Microsoft SQL Server reconnaissance, privilege mapping, and assessment workflows. Planned; no capability is currently packaged. |
| [tradecraft-mac](plugins/tradecraft-mac/README.md) | Planned | - | - | macOS execution, persistence, and operator validation workflows. Planned; no capability is currently packaged. |
| [tradecraft-linux](plugins/tradecraft-linux/README.md) | Planned | - | - | Linux execution, persistence, and operator validation workflows. Planned; no capability is currently packaged. |
| [c2-cobaltstrike](plugins/c2-cobaltstrike/README.md) | Yes | Yes | - | Cobalt Strike Aggressor Script, Sleep, BOF loader, and extension workflows. |
| [bloodhound-development](plugins/bloodhound-development/README.md) | Yes | Yes | - | Bootstrap, isolate, validate, review, and test BloodHound Enterprise and Community Edition development work. |

<!-- END GENERATED PLUGIN CATALOG -->

## Skills

<!-- BEGIN GENERATED SKILL INVENTORY: run `just generate-inventory` -->

| Skill | Plugin | Path |
|---|---|---|
| `git-cleanup` | `workflows-development` | [SKILL.md](plugins/workflows-development/skills/git-cleanup/SKILL.md) |
| `git-merge` | `workflows-development` | [SKILL.md](plugins/workflows-development/skills/git-merge/SKILL.md) |
| `git-preflight` | `workflows-development` | [SKILL.md](plugins/workflows-development/skills/git-preflight/SKILL.md) |
| `readme-generation` | `workflows-development` | [SKILL.md](plugins/workflows-development/skills/readme-generation/SKILL.md) |
| `scaffold-python` | `workflows-development` | [SKILL.md](plugins/workflows-development/skills/scaffold-python/SKILL.md) |
| `scaffold-security` | `workflows-development` | [SKILL.md](plugins/workflows-development/skills/scaffold-security/SKILL.md) |
| `code-review` | `code-review-and-qa` | [SKILL.md](plugins/code-review-and-qa/skills/code-review/SKILL.md) |
| `cpp-core-guidelines` | `code-review-and-qa` | [SKILL.md](plugins/code-review-and-qa/skills/cpp-core-guidelines/SKILL.md) |
| `webapp-qa` | `code-review-and-qa` | [SKILL.md](plugins/code-review-and-qa/skills/webapp-qa/SKILL.md) |
| `source-research` | `workflows-research` | [SKILL.md](plugins/workflows-research/skills/source-research/SKILL.md) |
| `nmap-parse` | `ops-reconnaissance` | [SKILL.md](plugins/ops-reconnaissance/skills/nmap-parse/SKILL.md) |
| `osint-recon` | `ops-reconnaissance` | [SKILL.md](plugins/ops-reconnaissance/skills/osint-recon/SKILL.md) |
| `shodan` | `ops-reconnaissance` | [SKILL.md](plugins/ops-reconnaissance/skills/shodan/SKILL.md) |
| `secret-scan` | `ops-appsec` | [SKILL.md](plugins/ops-appsec/skills/secret-scan/SKILL.md) |
| `security-review` | `ops-appsec` | [SKILL.md](plugins/ops-appsec/skills/security-review/SKILL.md) |
| `webapp-review` | `ops-appsec` | [SKILL.md](plugins/ops-appsec/skills/webapp-review/SKILL.md) |
| `sccm-recon` | `ops-sccm` | [SKILL.md](plugins/ops-sccm/skills/sccm-recon/SKILL.md) |
| `sccm-takeover-relay` | `ops-sccm` | [SKILL.md](plugins/ops-sccm/skills/sccm-takeover-relay/SKILL.md) |
| `sccmhunter-install-local` | `ops-sccm` | [SKILL.md](plugins/ops-sccm/skills/sccmhunter-install-local/SKILL.md) |
| `azurehound-analysis` | `bloodhound` | [SKILL.md](plugins/bloodhound/skills/azurehound-analysis/SKILL.md) |
| `bloodhound-ad-analysis` | `bloodhound` | [SKILL.md](plugins/bloodhound/skills/bloodhound-ad-analysis/SKILL.md) |
| `bloodhound-analysis` | `bloodhound` | [SKILL.md](plugins/bloodhound/skills/bloodhound-analysis/SKILL.md) |
| `bloodhound-opengraph` | `bloodhound` | [SKILL.md](plugins/bloodhound/skills/bloodhound-opengraph/SKILL.md) |
| `bloodhound-query` | `bloodhound` | [SKILL.md](plugins/bloodhound/skills/bloodhound-query/SKILL.md) |
| `openhound-development` | `bloodhound` | [SKILL.md](plugins/bloodhound/skills/openhound-development/SKILL.md) |
| `openhound-github` | `bloodhound` | [SKILL.md](plugins/bloodhound/skills/openhound-github/SKILL.md) |
| `openhound-jamf` | `bloodhound` | [SKILL.md](plugins/bloodhound/skills/openhound-jamf/SKILL.md) |
| `openhound-okta` | `bloodhound` | [SKILL.md](plugins/bloodhound/skills/openhound-okta/SKILL.md) |
| `electron-app-audit` | `payloads` | [SKILL.md](plugins/payloads/skills/electron-app-audit/SKILL.md) |
| `electron-candidate-discovery` | `payloads` | [SKILL.md](plugins/payloads/skills/electron-candidate-discovery/SKILL.md) |
| `electron-install-persistence` | `payloads` | [SKILL.md](plugins/payloads/skills/electron-install-persistence/SKILL.md) |
| `electron-squirrel-repackage` | `payloads` | [SKILL.md](plugins/payloads/skills/electron-squirrel-repackage/SKILL.md) |
| `beacon-object-file-development` | `c2-extensions` | [SKILL.md](plugins/c2-extensions/skills/beacon-object-file-development/SKILL.md) |
| `c2-bof-development` | `c2-extensions` | [SKILL.md](plugins/c2-extensions/skills/c2-bof-development/SKILL.md) |
| `finding-report` | `report-drafting` | [SKILL.md](plugins/report-drafting/skills/finding-report/SKILL.md) |
| `ghostwriter-mcp` | `report-drafting` | [SKILL.md](plugins/report-drafting/skills/ghostwriter-mcp/SKILL.md) |
| `ghostwriter-oplog` | `report-drafting` | [SKILL.md](plugins/report-drafting/skills/ghostwriter-oplog/SKILL.md) |
| `binary-ninja-mcp-analysis` | `reverse-engineering` | [SKILL.md](plugins/reverse-engineering/skills/binary-ninja-mcp-analysis/SKILL.md) |
| `ghidra-mcp-analysis` | `reverse-engineering` | [SKILL.md](plugins/reverse-engineering/skills/ghidra-mcp-analysis/SKILL.md) |
| `timeline-asciinema` | `report-timeline` | [SKILL.md](plugins/report-timeline/skills/timeline-asciinema/SKILL.md) |
| `timeline-cobaltstrike` | `report-timeline` | [SKILL.md](plugins/report-timeline/skills/timeline-cobaltstrike/SKILL.md) |
| `timeline-consolidator` | `report-timeline` | [SKILL.md](plugins/report-timeline/skills/timeline-consolidator/SKILL.md) |
| `timeline-ghostwriter` | `report-timeline` | [SKILL.md](plugins/report-timeline/skills/timeline-ghostwriter/SKILL.md) |
| `timeline-markdown-notes` | `report-timeline` | [SKILL.md](plugins/report-timeline/skills/timeline-markdown-notes/SKILL.md) |
| `timeline-mythic` | `report-timeline` | [SKILL.md](plugins/report-timeline/skills/timeline-mythic/SKILL.md) |
| `timeline-pdf-notes` | `report-timeline` | [SKILL.md](plugins/report-timeline/skills/timeline-pdf-notes/SKILL.md) |
| `timeline-workflow` | `report-timeline` | [SKILL.md](plugins/report-timeline/skills/timeline-workflow/SKILL.md) |
| `codex-activity-report` | `codex-observability` | [SKILL.md](plugins/codex-observability/skills/codex-activity-report/SKILL.md) |
| `opentelemetry-codex` | `codex-observability` | [SKILL.md](plugins/codex-observability/skills/opentelemetry-codex/SKILL.md) |
| `iac-attack-surface` | `ops-infrastructure` | [SKILL.md](plugins/ops-infrastructure/skills/iac-attack-surface/SKILL.md) |
| `nftables-allow-source` | `ops-infrastructure` | [SKILL.md](plugins/ops-infrastructure/skills/nftables-allow-source/SKILL.md) |
| `proxychains-tunnel` | `ops-infrastructure` | [SKILL.md](plugins/ops-infrastructure/skills/proxychains-tunnel/SKILL.md) |
| `ssh-ops` | `ops-infrastructure` | [SKILL.md](plugins/ops-infrastructure/skills/ssh-ops/SKILL.md) |
| `course-wiki-migration-orchestrator` | `internal-training-course` | [SKILL.md](plugins/internal-training-course/skills/course-wiki-migration-orchestrator/SKILL.md) |
| `course-wiki-stage1-scaffold` | `internal-training-course` | [SKILL.md](plugins/internal-training-course/skills/course-wiki-stage1-scaffold/SKILL.md) |
| `course-wiki-stage2-content-migration` | `internal-training-course` | [SKILL.md](plugins/internal-training-course/skills/course-wiki-stage2-content-migration/SKILL.md) |
| `course-wiki-stage3-qa` | `internal-training-course` | [SKILL.md](plugins/internal-training-course/skills/course-wiki-stage3-qa/SKILL.md) |
| `credential-harvest-landing-page-copy` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/credential-harvest-landing-page-copy/SKILL.md) |
| `phishing-campaign-builder` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/phishing-campaign-builder/SKILL.md) |
| `phishing-email-html` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/phishing-email-html/SKILL.md) |
| `phishing-pretext` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/phishing-pretext/SKILL.md) |
| `pretext-brainstormer` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/pretext-brainstormer/SKILL.md) |
| `vishing-pretext` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/vishing-pretext/SKILL.md) |
| `ludus-development` | `ludus` | [SKILL.md](plugins/ludus/skills/ludus-development/SKILL.md) |
| `mythic-implant-development` | `c2-mythic` | [SKILL.md](plugins/c2-mythic/skills/mythic-implant-development/SKILL.md) |
| `mythic-profiles` | `c2-mythic` | [SKILL.md](plugins/c2-mythic/skills/mythic-profiles/SKILL.md) |
| `mythic-translation-containers` | `c2-mythic` | [SKILL.md](plugins/c2-mythic/skills/mythic-translation-containers/SKILL.md) |
| `com-proxy-triage` | `tradecraft-windows` | [SKILL.md](plugins/tradecraft-windows/skills/com-proxy-triage/SKILL.md) |
| `cobalt-strike-aggressor-development` | `c2-cobaltstrike` | [SKILL.md](plugins/c2-cobaltstrike/skills/cobalt-strike-aggressor-development/SKILL.md) |
| `cobalt-strike-aggressor-reference` | `c2-cobaltstrike` | [SKILL.md](plugins/c2-cobaltstrike/skills/cobalt-strike-aggressor-reference/SKILL.md) |
| `bhe-dev-bootstrap` | `bloodhound-development` | [SKILL.md](plugins/bloodhound-development/skills/bhe-dev-bootstrap/SKILL.md) |
| `bhe-sample-data-ingest` | `bloodhound-development` | [SKILL.md](plugins/bloodhound-development/skills/bhe-sample-data-ingest/SKILL.md) |
| `bhe-ui-playwright` | `bloodhound-development` | [SKILL.md](plugins/bloodhound-development/skills/bhe-ui-playwright/SKILL.md) |

<!-- END GENERATED SKILL INVENTORY -->

## Standalone Skills

| Skill | Path |
|---|---|
| - | No standalone skills currently live under `skills/`. |

## Agents

<!-- BEGIN GENERATED AGENT INVENTORY: run `just generate-inventory` -->

| Agent | Path |
|---|---|
| `architect` | [agents/architect.toml](agents/architect.toml) |
| `bloodhound-analyst` | [agents/bloodhound-analyst.toml](agents/bloodhound-analyst.toml) |
| `code-reviewer` | [agents/code-reviewer.toml](agents/code-reviewer.toml) |
| `course-migration` | [agents/course-migration.toml](agents/course-migration.toml) |
| `domain-ops` | [agents/domain-ops.toml](agents/domain-ops.toml) |
| `exploit-dev` | [agents/exploit-dev.toml](agents/exploit-dev.toml) |
| `internal-network-recon` | [agents/internal-network-recon.toml](agents/internal-network-recon.toml) |
| `ludus` | [agents/ludus.toml](agents/ludus.toml) |
| `mythic-developer` | [agents/mythic-developer.toml](agents/mythic-developer.toml) |
| `osint-recon` | [agents/osint-recon.toml](agents/osint-recon.toml) |
| `planner` | [agents/planner.toml](agents/planner.toml) |
| `poc-dev` | [agents/poc-dev.toml](agents/poc-dev.toml) |
| `qa-tester` | [agents/qa-tester.toml](agents/qa-tester.toml) |
| `report-writer` | [agents/report-writer.toml](agents/report-writer.toml) |
| `researcher` | [agents/researcher.toml](agents/researcher.toml) |
| `reverse-engineer` | [agents/reverse-engineer.toml](agents/reverse-engineer.toml) |
| `sccm-ops` | [agents/sccm-ops.toml](agents/sccm-ops.toml) |
| `security-researcher` | [agents/security-researcher.toml](agents/security-researcher.toml) |
| `social-engineer` | [agents/social-engineer.toml](agents/social-engineer.toml) |
| `ssh-operator` | [agents/ssh-operator.toml](agents/ssh-operator.toml) |
| `telemetry-analyst` | [agents/telemetry-analyst.toml](agents/telemetry-analyst.toml) |
| `winternals` | [agents/winternals.toml](agents/winternals.toml) |

<!-- END GENERATED AGENT INVENTORY -->

## MCP-Aware Plugins

<!-- BEGIN GENERATED MCP INVENTORY: run `just generate-inventory` -->

| MCP Server | Plugin | Configuration |
|---|---|---|
| `bloodhound_mcp` | `bloodhound` | Configure directly in Codex with `uv --directory /path/to/bloodhound-mcp run main.py`. |
| `ghostwriter` | `report-drafting` | Configure directly in Codex with `uv --directory /path/to/GhostWriterMCP run python -m ghostwritermcp.server`. |
| `binary_ninja_mcp` | `reverse-engineering` | Configure directly in Codex with `npx -y binary-ninja-mcp --host localhost --port 9009` after installing `fosdickio/binary_ninja_mcp` in Binary Ninja. |
| `ghidra` | `reverse-engineering` | Configure directly in Codex with the command or endpoint documented by your Ghidra MCP server. |

<!-- END GENERATED MCP INVENTORY -->
