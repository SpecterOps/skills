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

### Codex GUI MCP setup

Installing a Codex plugin from `/plugins` installs the plugin package, skills, MCP config, and helper scripts. It does **not** clone external MCP server repositories, run dependency installers, or write secrets into the GUI app. Complete the MCP dependency and environment setup after installing the plugin.

1. Install or refresh this marketplace in the Codex GUI app:

   ```bash
   codex plugin marketplace add /home/matthew/Projects/skills
   # or
   codex plugin marketplace add SpecterOps/skills
   ```

   Then open the Codex GUI app, go to `/plugins`, and install `bloodhound-analysis`, `ghostwriter-mcp`, and optionally `ghostwriter-oplog`.

2. Install the MCP server dependencies into the installed plugin copies:

   ```bash
   cd ~/.codex/plugins/bloodhound-analysis
   scripts/install-mcp-deps.sh
   ```

   ```bash
   cd ~/.codex/plugins/ghostwriter-mcp
   scripts/install-mcp-deps.sh
   ```

3. Add GUI-visible MCP environment values to `~/.codex/config.toml` and restart the Codex GUI app:

   ```toml
   [mcp_servers.bloodhound_mcp.env]
   BLOODHOUND_MCP_DIR = "/home/matthew/.codex/plugins/bloodhound-analysis/vendor/bloodhound-mcp"
   BLOODHOUND_DOMAIN = "YOUR_DOMAIN"
   BLOODHOUND_TOKEN_ID = "YOUR_TOKEN_ID"
   BLOODHOUND_TOKEN_KEY = "YOUR_TOKEN_KEY"
   BLOODHOUND_SCHEME = "https"
   BLOODHOUND_PORT = "443"

   [mcp_servers.ghostwriter.env]
   GHOSTWRITER_MCP_DIR = "/home/matthew/.codex/plugins/ghostwriter-mcp/vendor/ghostwriter-mcp"
   GHOSTWRITER_URL = "https://ghostwriter.example.com/"
   GHOSTWRITER_API_KEY = "YOUR_API_KEY"
   GHOSTWRITER_CA_BUNDLE = "/path/to/ca-bundle.crt"
   GHOSTWRITER_OPLOG_ID = "123"
   GHOSTWRITER_OPERATOR = "your-callsign"
   GHOSTWRITER_SOURCE_IP = "10.0.0.5"
   ```


#### Windows native PowerShell wrappers

Windows users do not need Git Bash for the helper scripts. Install dependencies from PowerShell after the plugin is installed:

```powershell
cd $env:USERPROFILE\.codex\plugins\bloodhound-analysis
.\scripts\install-mcp-deps.ps1

cd $env:USERPROFILE\.codex\plugins\ghostwriter-mcp
.\scripts\install-mcp-deps.ps1
```

Use Windows paths in `~/.codex/config.toml` and override the MCP command to PowerShell if the GUI does not run the Bash wrappers:

```toml
[mcp_servers.bloodhound_mcp]
command = "powershell.exe"
args = ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "C:\\Users\\<you>\\.codex\\plugins\\bloodhound-analysis\\scripts\\run-bloodhound-mcp.ps1"]

[mcp_servers.bloodhound_mcp.env]
BLOODHOUND_MCP_DIR = "C:\\Users\\<you>\\.codex\\plugins\\bloodhound-analysis\\vendor\\bloodhound-mcp"

[mcp_servers.ghostwriter]
command = "powershell.exe"
args = ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "C:\\Users\\<you>\\.codex\\plugins\\ghostwriter-mcp\\scripts\\run-ghostwriter-mcp.ps1"]

[mcp_servers.ghostwriter.env]
GHOSTWRITER_MCP_DIR = "C:\\Users\\<you>\\.codex\\plugins\\ghostwriter-mcp\\vendor\\ghostwriter-mcp"
```

4. Verify the runners outside the GUI before troubleshooting Codex:

   ```bash
   ~/.codex/plugins/bloodhound-analysis/scripts/run-bloodhound-mcp.sh
   ~/.codex/plugins/ghostwriter-mcp/scripts/run-ghostwriter-mcp.sh
   ```

   In the GUI, start a new session after restart and confirm tools appear under `mcp__bloodhound_mcp__*` and `mcp__ghostwriter__*`.

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
| [engineering-workflows](plugins/engineering-workflows/README.md) | Yes | Yes | - | Core engineering scaffolding, repository hygiene, and implementation workflows for Specter Codex. |
| [code-review-and-qa](plugins/code-review-and-qa/README.md) | Yes | Yes | - | Code review and web application QA workflows for Specter Codex. |
| [research-workflows](plugins/research-workflows/README.md) | Yes | Yes | - | Source-backed research and synthesis workflows for Specter Codex. |
| [external-recon](plugins/external-recon/README.md) | Yes | Yes | - | Passive external reconnaissance and exposure discovery workflows for Specter Codex. |
| [appsec-assessment](plugins/appsec-assessment/README.md) | Yes | Yes | - | Application and code security assessment workflows for Specter Codex. |
| [identity-assessment-core](plugins/identity-assessment-core/README.md) | Yes | Yes | - | Core identity, Active Directory, Windows, and internal assessment workflows. |
| [sccm-assessment](plugins/sccm-assessment/README.md) | Yes | Yes | - | Microsoft Configuration Manager reconnaissance and takeover validation workflows. |
| [bloodhound-analysis](plugins/bloodhound-analysis/README.md) | Yes | Yes | Yes | BloodHound, AzureHound, GitHound/JamfHound/OktaHound OpenGraph attack-path query workflows, SCIM bridge references, and optional BloodHound MCP packaging. |
| [offensive-tooling](plugins/offensive-tooling/README.md) | Yes | Yes | - | Security tool scaffolding and proof-of-concept development workflows. |
| [payloads](plugins/payloads/README.md) | Yes | Yes | - | Reusable Electron payload packaging, persistence, audit, and discovery workflows. |
| [c2-extension-development](plugins/c2-extension-development/README.md) | Yes | Yes | - | Cobalt Strike Aggressor and BOF development workflows. |
| [report-writing](plugins/report-writing/README.md) | Yes | Yes | - | Finding and report drafting workflows for security assessment deliverables. |
| [timeline-evidence](plugins/timeline-evidence/README.md) | Yes | Yes | - | Pentest timeline ingestion, consolidation, and evidence packaging workflows. |
| [codex-observability](plugins/codex-observability/README.md) | Yes | Yes | - | Codex activity reporting and telemetry workflows. |
| [platform-ops-private](plugins/platform-ops-private/README.md) | Yes | Yes | - | Private platform, MCP, SSH, tunnel, and firewall operation workflows. |
| [course-conversion-internal](plugins/course-conversion-internal/README.md) | Yes | Yes | - | Internal-only staged course wiki migration workflows. |
| [social-engineering](plugins/social-engineering/README.md) | Yes | Yes | - | Social engineering research and phishing pretext workflows. |
| [ghostwriter-mcp](plugins/ghostwriter-mcp/README.md) | Yes | Yes | Yes | MCP integration for Ghostwriter security documentation platform |
| [ghostwriter-oplog](plugins/ghostwriter-oplog/README.md) | Yes | Yes | - | Quick logging commands for GhostWriter operation logs |
| [cobalt-strike-aggressor-reference](plugins/cobalt-strike-aggressor-reference/README.md) | Yes | Yes | - | Cobalt Strike Aggressor script development skill with complete function references for Aggressor and Sleep languages |
| [beacon-object-file-development](plugins/beacon-object-file-development/README.md) | Yes | Yes | - | Beacon Object File (BOF) development skill with API documentation, build guides, and a BOF linter |
| [ludus](plugins/ludus/README.md) | Yes | Yes | - | Ludus cyber range configuration and management skill with full API, CLI, and deployment references |
| [binary-ninja-mcp](plugins/binary-ninja-mcp/README.md) | Yes | Yes | - | Binary Ninja analysis skill with BNIL IL documentation and MCP server usage guide |
| [mythic-implant](plugins/mythic-implant/README.md) | Yes | Yes | - | Mythic C2 framework implant development skill with agent message protocols, payload type definitions, and step-by-step build workflow |
| [openhound-collector-development](plugins/openhound-collector-development/README.md) | Yes | Yes | - | OpenHound collector template support package with the embedded OpenHound development skill. |
| [windows-tradecraft](plugins/windows-tradecraft/README.md) | Yes | - | - | Windows execution, persistence, and COM proxy validation workflows. |

## Skills

| Skill | Plugin | Path |
|---|---|---|
| `git-cleanup` | `engineering-workflows` | [SKILL.md](plugins/engineering-workflows/skills/git-cleanup/SKILL.md) |
| `git-merge` | `engineering-workflows` | [SKILL.md](plugins/engineering-workflows/skills/git-merge/SKILL.md) |
| `git-preflight` | `engineering-workflows` | [SKILL.md](plugins/engineering-workflows/skills/git-preflight/SKILL.md) |
| `readme-generation` | `engineering-workflows` | [SKILL.md](plugins/engineering-workflows/skills/readme-generation/SKILL.md) |
| `scaffold-python` | `engineering-workflows` | [SKILL.md](plugins/engineering-workflows/skills/scaffold-python/SKILL.md) |
| `code-review` | `code-review-and-qa` | [SKILL.md](plugins/code-review-and-qa/skills/code-review/SKILL.md) |
| `webapp-qa` | `code-review-and-qa` | [SKILL.md](plugins/code-review-and-qa/skills/webapp-qa/SKILL.md) |
| `source-research` | `research-workflows` | [SKILL.md](plugins/research-workflows/skills/source-research/SKILL.md) |
| `osint-recon` | `external-recon` | [SKILL.md](plugins/external-recon/skills/osint-recon/SKILL.md) |
| `shodan` | `external-recon` | [SKILL.md](plugins/external-recon/skills/shodan/SKILL.md) |
| `secret-scan` | `appsec-assessment` | [SKILL.md](plugins/appsec-assessment/skills/secret-scan/SKILL.md) |
| `security-review` | `appsec-assessment` | [SKILL.md](plugins/appsec-assessment/skills/security-review/SKILL.md) |
| `webapp-review` | `appsec-assessment` | [SKILL.md](plugins/appsec-assessment/skills/webapp-review/SKILL.md) |
| `nmap-parse` | `identity-assessment-core` | [SKILL.md](plugins/identity-assessment-core/skills/nmap-parse/SKILL.md) |
| `sccm-recon` | `sccm-assessment` | [SKILL.md](plugins/sccm-assessment/skills/sccm-recon/SKILL.md) |
| `sccm-takeover-relay` | `sccm-assessment` | [SKILL.md](plugins/sccm-assessment/skills/sccm-takeover-relay/SKILL.md) |
| `sccmhunter-install-local` | `sccm-assessment` | [SKILL.md](plugins/sccm-assessment/skills/sccmhunter-install-local/SKILL.md) |
| `azurehound-analysis` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/azurehound-analysis/SKILL.md) |
| `bloodhound-ad-analysis` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/bloodhound-ad-analysis/SKILL.md) |
| `bloodhound-analysis` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/bloodhound-analysis/SKILL.md) |
| `bloodhound-opengraph` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/bloodhound-opengraph/SKILL.md) |
| `bloodhound-query` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/bloodhound-query/SKILL.md) |
| `openhound-github` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/openhound-github/SKILL.md) |
| `openhound-jamf` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/openhound-jamf/SKILL.md) |
| `openhound-okta` | `bloodhound-analysis` | [SKILL.md](plugins/bloodhound-analysis/skills/openhound-okta/SKILL.md) |
| `scaffold-security` | `offensive-tooling` | [SKILL.md](plugins/offensive-tooling/skills/scaffold-security/SKILL.md) |
| `electron-app-audit` | `payloads` | [SKILL.md](plugins/payloads/skills/electron-app-audit/SKILL.md) |
| `electron-candidate-discovery` | `payloads` | [SKILL.md](plugins/payloads/skills/electron-candidate-discovery/SKILL.md) |
| `electron-install-persistence` | `payloads` | [SKILL.md](plugins/payloads/skills/electron-install-persistence/SKILL.md) |
| `electron-squirrel-repackage` | `payloads` | [SKILL.md](plugins/payloads/skills/electron-squirrel-repackage/SKILL.md) |
| `c2-bof-development` | `c2-extension-development` | [SKILL.md](plugins/c2-extension-development/skills/c2-bof-development/SKILL.md) |
| `cobalt-strike-aggressor-development` | `c2-extension-development` | [SKILL.md](plugins/c2-extension-development/skills/cobalt-strike-aggressor-development/SKILL.md) |
| `finding-report` | `report-writing` | [SKILL.md](plugins/report-writing/skills/finding-report/SKILL.md) |
| `timeline-asciinema` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-asciinema/SKILL.md) |
| `timeline-cobaltstrike` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-cobaltstrike/SKILL.md) |
| `timeline-consolidator` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-consolidator/SKILL.md) |
| `timeline-ghostwriter` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-ghostwriter/SKILL.md) |
| `timeline-markdown-notes` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-markdown-notes/SKILL.md) |
| `timeline-mythic` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-mythic/SKILL.md) |
| `timeline-pdf-notes` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-pdf-notes/SKILL.md) |
| `timeline-workflow` | `timeline-evidence` | [SKILL.md](plugins/timeline-evidence/skills/timeline-workflow/SKILL.md) |
| `codex-activity-report` | `codex-observability` | [SKILL.md](plugins/codex-observability/skills/codex-activity-report/SKILL.md) |
| `opentelemetry-codex` | `codex-observability` | [SKILL.md](plugins/codex-observability/skills/opentelemetry-codex/SKILL.md) |
| `kali-mcp` | `platform-ops-private` | [SKILL.md](plugins/platform-ops-private/skills/kali-mcp/SKILL.md) |
| `nftables-allow-source` | `platform-ops-private` | [SKILL.md](plugins/platform-ops-private/skills/nftables-allow-source/SKILL.md) |
| `proxychains-tunnel` | `platform-ops-private` | [SKILL.md](plugins/platform-ops-private/skills/proxychains-tunnel/SKILL.md) |
| `ssh-ops` | `platform-ops-private` | [SKILL.md](plugins/platform-ops-private/skills/ssh-ops/SKILL.md) |
| `course-wiki-migration-orchestrator` | `course-conversion-internal` | [SKILL.md](plugins/course-conversion-internal/skills/course-wiki-migration-orchestrator/SKILL.md) |
| `course-wiki-stage1-scaffold` | `course-conversion-internal` | [SKILL.md](plugins/course-conversion-internal/skills/course-wiki-stage1-scaffold/SKILL.md) |
| `course-wiki-stage2-content-migration` | `course-conversion-internal` | [SKILL.md](plugins/course-conversion-internal/skills/course-wiki-stage2-content-migration/SKILL.md) |
| `course-wiki-stage3-qa` | `course-conversion-internal` | [SKILL.md](plugins/course-conversion-internal/skills/course-wiki-stage3-qa/SKILL.md) |
| `credential-harvest-landing-page-copy` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/credential-harvest-landing-page-copy/SKILL.md) |
| `phishing-campaign-builder` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/phishing-campaign-builder/SKILL.md) |
| `phishing-email-html` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/phishing-email-html/SKILL.md) |
| `phishing-pretext` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/phishing-pretext/SKILL.md) |
| `pretext-brainstormer` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/pretext-brainstormer/SKILL.md) |
| `vishing-pretext` | `social-engineering` | [SKILL.md](plugins/social-engineering/skills/vishing-pretext/SKILL.md) |
| `cobalt-strike-aggressor-reference` | `cobalt-strike-aggressor-reference` | [SKILL.md](plugins/cobalt-strike-aggressor-reference/skills/cobalt-strike-aggressor-reference/SKILL.md) |
| `beacon-object-file-development` | `beacon-object-file-development` | [SKILL.md](plugins/beacon-object-file-development/skills/beacon-object-file-development/SKILL.md) |
| `ludus-development` | `ludus` | [SKILL.md](plugins/ludus/skills/ludus-development/SKILL.md) |
| `binary-ninja-mcp-analysis` | `binary-ninja-mcp` | [SKILL.md](plugins/binary-ninja-mcp/skills/binary-ninja-mcp-analysis/SKILL.md) |
| `mythic-implant-development` | `mythic-implant` | [SKILL.md](plugins/mythic-implant/skills/mythic-implant-development/SKILL.md) |
| `openhound-collector-development` | `openhound-collector-development` | [SKILL.md](plugins/openhound-collector-development/skills/openhound-collector-development/SKILL.md) |
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

## MCP Plugins

| MCP Package | Plugin | Config |
|---|---|---|
| `bloodhound-analysis` | `bloodhound-analysis` | [config](plugins/bloodhound-analysis/.mcp.json) |
| `ghostwriter-mcp` | `ghostwriter-mcp` | [config](plugins/ghostwriter-mcp/.mcp.json) |
