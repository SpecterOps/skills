# BloodHound MCP Tool Surface

This repo expects Codex to connect to a user-managed BloodHound MCP checkout, typically `mwnickerson/bloodhound_mcp`, configured directly under `mcp_servers.bloodhound_mcp`.

## Composite tools

- `domain_info`: domain lists, object search, users, groups, computers, OUs, GPOs, trusts, foreign principals, DCSyncers.
- `user_info`: user properties, sessions, memberships, rights, delegation, controllables, controllers.
- `group_info`: group properties, members, memberships, rights, controllables, controllers.
- `computer_info`: computer properties, sessions, local admins, execution rights, delegation, controllables.
- `ou_info`: OU properties and contained users/groups/computers/GPOs.
- `gpo_info`: GPO properties and controllers.
- `graph_analysis`: shortest path, edge composition, graph search.
- `adcs_info`: templates, ESC paths, CA/template context where supported.
- `cypher_query`: run and manage Cypher queries.
- `data_quality`: stats, platform inventory, collection completeness context.
- `asset_groups`: BloodHound asset group and tag workflows.
- `custom_nodes`: OpenGraph custom node type configuration.
- `file_upload`: SharpHound/AzureHound data ingestion where supported by the MCP branch.

## MCP resources

- `bloodhound://cypher/reference`
- `bloodhound://cypher/offensive-queries`
- `bloodhound://guides/ad`
- `bloodhound://guides/ad-methodology`
- `bloodhound://guides/azure`
- `bloodhound://guides/azure-methodology`
- `bloodhound://guides/adcs`
- `bloodhound://guides/adcs-methodology`
- `bloodhound://opengraph/guide`
- `bloodhound://opengraph/examples`

## Output contract

For findings, include path summary, object IDs/names, edge sequence, evidence source, caveats, confidence, and remediation.
