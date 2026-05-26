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

## MCP setup

This plugin includes BloodHound MCP-aware skills and reference material, but it does not install, clone, update, or run the external BloodHound MCP server for you. Follow Codex MCP configuration directly: install or clone the server yourself, then point Codex at that checkout.

Install the external server using its upstream instructions. A typical checkout uses:

```bash
git clone https://github.com/mwnickerson/bloodhound_mcp.git /path/to/bloodhound-mcp
cd /path/to/bloodhound-mcp
uv sync
```

Then add the MCP server to `~/.codex/config.toml` or project `.codex/config.toml`:

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
```

Restart Codex after editing MCP configuration and confirm the `bloodhound_mcp` server is visible under `/mcp` before using live graph workflows. Do not commit environment-specific API values.
