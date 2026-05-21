# BloodHound Analysis

Focused workflows for BloodHound, AzureHound, GitHound/OpenHound GitHub, JamfHound/OpenHound Jamf, OktaHound/OpenHound Okta, SCIM bridge analysis, saved-query adaptation, optional BloodHound MCP-assisted graph analysis, and OpenGraph extension work.

## Skills

- `bloodhound-analysis` — MCP-aware BloodHound analysis router and live graph workflow.
- `bloodhound-query` — shared query authoring/review workflow for BloodHound and OpenGraph graphs.
- `bloodhound` — AD and ADCS attack-path query workflow.
- `azurehound` — Azure/Entra ID attack-path query workflow.
- `openhound-github` — GitHound/OpenHound GitHub OpenGraph query workflow.
- `openhound-jamf` — JamfHound/OpenHound Jamf OpenGraph query workflow.
- `openhound-okta` — OktaHound/OpenHound Okta OpenGraph query workflow.
- `bloodhound-opengraph` — custom OpenGraph schema, collector, and extension modeling.

## Agents

- `bloodhound-analyst`

## Query snapshots, examples, and references

This plugin vendors upstream saved-query snapshots for offline agent use:

- BloodHound Query Library: `references/query-snapshots/bloodhound-query-library/queries/`
- OpenHound GitHub saved queries: `references/query-snapshots/openhound-github/saved-queries/`
- OpenHound Jamf saved searches: `references/query-snapshots/openhound-jamf/saved-searches/`
- OpenHound Okta saved searches: `references/query-snapshots/openhound-okta/saved-searches/`

It also includes collector-aware reference material:

- SCIM methodology: `references/docs/scim-methodology.md`
- OpenGraph extension management: `references/docs/opengraph-extension-management.md`
- Collector source index: `references/docs/collector-source-index.md`
- Curated example Cypher: `references/examples/example-cypher.md`
- Node and edge reference: `references/examples/node-edge-reference.md`
- Small GitHound SAML/SCIM examples: `references/examples/githound/samples/`
- JamfHound schema/object examples: `references/examples/jamfhound/`

Use `scripts/update-query-snapshots.py` to refresh saved-query snapshots and indexes before publishing a release. Generated indexes live under `references/query-indexes/`. Small example files are curated separately and should be refreshed intentionally from upstream collector repositories when collector schemas change.

## MCP packaging

This plugin includes Codex MCP configuration plus plugin-local install/run scripts for the BloodHound MCP server. These files are packaging artifacts for environments that choose to enable the MCP server; working in this repository does not install or sync anything into the current machine's Codex config.

- `.mcp.json` points Codex at the plugin-owned MCP runner.
- `scripts/install-mcp-deps.sh` installs or updates the BloodHound MCP checkout under `vendor/bloodhound-mcp` by default.
- `scripts/run-bloodhound-mcp.sh` runs the server from `BLOODHOUND_MCP_DIR` or the plugin-local vendor directory.
- `mcp/env.example` documents required BloodHound connection variables without committing secrets.

For a target install environment, install the plugin and MCP server together with the bootstrap sync flow, or point `BLOODHOUND_MCP_DIR` at an existing checkout. Do not commit environment-specific API values.

### Codex GUI app setup

After installing `bloodhound-analysis` from the Codex GUI `/plugins` view, install the MCP server dependency into the installed plugin copy:

```bash
cd ~/.codex/plugins/bloodhound-analysis
scripts/install-mcp-deps.sh
```

Add BloodHound connection values to `~/.codex/config.toml` so the GUI app can see them, then fully restart Codex:

```toml
[mcp_servers.bloodhound_mcp.env]
BLOODHOUND_MCP_DIR = "/home/matthew/.codex/plugins/bloodhound-analysis/vendor/bloodhound-mcp"
BLOODHOUND_DOMAIN = "YOUR_DOMAIN"
BLOODHOUND_TOKEN_ID = "YOUR_TOKEN_ID"
BLOODHOUND_TOKEN_KEY = "YOUR_TOKEN_KEY"
BLOODHOUND_SCHEME = "https"
BLOODHOUND_PORT = "443"
```


#### Windows native PowerShell wrappers

Windows users do not need Git Bash for the helper scripts. Install dependencies from PowerShell after the plugin is installed:

```powershell
cd $env:USERPROFILE\.codex\plugins\bloodhound-analysis
.\scripts\install-mcp-deps.ps1

cd $env:USERPROFILE\.codex\plugins\ghostwriter-mcp
.\scripts\install-mcp-deps.ps1 -Source '<git-url-or-local-path-to-ghostwriter-mcp-server>'
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

Test the runner directly if the GUI does not show BloodHound tools:

```bash
~/.codex/plugins/bloodhound-analysis/scripts/run-bloodhound-mcp.sh
```

Expected Codex tool namespace: `mcp__bloodhound_mcp__*`.
