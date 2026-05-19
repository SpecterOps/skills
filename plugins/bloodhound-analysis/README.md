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
