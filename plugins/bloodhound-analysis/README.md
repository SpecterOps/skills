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
- `scripts/run-bloodhound-mcp.sh` runs the server from `BLOODHOUND_MCP_DIR` or the plugin-local vendor directory, and auto-runs the installer on first start when the checkout is missing.
- `mcp/env.example` documents required BloodHound connection variables without committing secrets.

For a target install environment, install the plugin from Codex and configure only the BloodHound connection values. The first MCP start bootstraps the plugin-local server checkout automatically unless `BLOODHOUND_MCP_AUTO_INSTALL=0` is set. Do not commit environment-specific API values.

### Codex GUI app setup

After installing `bloodhound-analysis` from the Codex GUI `/plugins` view, add BloodHound connection values to `~/.codex/config.toml` so the GUI app can see them, then fully restart Codex. The plugin-owned MCP runner clones/syncs the BloodHound MCP server into `vendor/bloodhound-mcp` on first start.

```toml
[mcp_servers.bloodhound_mcp.env]
BLOODHOUND_DOMAIN = "YOUR_DOMAIN"
BLOODHOUND_TOKEN_ID = "YOUR_TOKEN_ID"
BLOODHOUND_TOKEN_KEY = "YOUR_TOKEN_KEY"
BLOODHOUND_SCHEME = "https"
BLOODHOUND_PORT = "443"
```


#### Windows native PowerShell wrappers

Windows users do not need Git Bash for the helper scripts. The PowerShell runner also auto-installs the MCP checkout on first start. If the GUI does not run the Bash wrapper, override the MCP command to PowerShell and point `-File` at the installed plugin copy. Codex installs plugins into its plugin cache rather than a stable `~/.codex/plugins/bloodhound-analysis` path, so use the plugin details/cache path from your local install. For repo-local development, use this repository's `plugins/bloodhound-analysis/scripts/run-bloodhound-mcp.ps1` path.

```toml
[mcp_servers.bloodhound_mcp]
command = "powershell.exe"
args = ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "C:\\path\\to\\installed\\bloodhound-analysis\\scripts\\run-bloodhound-mcp.ps1"]

[mcp_servers.bloodhound_mcp.env]
BLOODHOUND_DOMAIN = "YOUR_DOMAIN"
BLOODHOUND_TOKEN_ID = "YOUR_TOKEN_ID"
BLOODHOUND_TOKEN_KEY = "YOUR_TOKEN_KEY"
BLOODHOUND_SCHEME = "https"
BLOODHOUND_PORT = "443"
```

Optionally pre-warm or test the runner from a repo checkout if the GUI does not show BloodHound tools:

```bash
plugins/bloodhound-analysis/scripts/run-bloodhound-mcp.sh
```

For an installed plugin, run the same script from the plugin cache path Codex installed. Set `BLOODHOUND_MCP_AUTO_INSTALL=0` to disable first-run bootstrap. Expected Codex tool namespace: `mcp__bloodhound_mcp__*`.
