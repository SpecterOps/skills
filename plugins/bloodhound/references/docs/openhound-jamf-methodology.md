# OpenHound Jamf / JamfHound Methodology

Use for OpenHound Jamf OpenGraph analysis with JamfHound/OpenHound Jamf data.

## Collector context

- JamfHound models Jamf Pro tenants, sites, accounts, groups, API clients, computers, policies, scripts, profiles, and managed-device control relationships.
- Local schema examples live under `../examples/jamfhound/schema/` and object examples under `../examples/jamfhound/objects/`.
- Use an auditor-style collection identity when possible; elevated collection accounts can reveal more data but may overstate what lower-privilege operators can observe.
- Confirm Jamf Cloud/on-prem deployment details, site scoping, API permissions, and extension/schema compatibility before drawing path conclusions.

## Focus areas

- Jamf tenant and site administration paths.
- Account, group, API client, disabled account, and disabled API client effective permissions.
- Computer management control through policy/script/profile creation and scoped permissions.
- Tiered exposure: paths from lower-tier accounts or sites into Tier 0/Tier 1 assets.
- SSO and identity-provider links when the Jamf graph is combined with Okta, Entra, AD, or SCIM data.
- Hybrid Okta/Jamf device-management paths where OktaHound or another collector emitted bridge data.

## Query guidance

- OpenHound Jamf labels and relationships use `jamf_` prefixes in current snapshots.
- Read `../examples/node-edge-reference.md` and local JamfHound schema/object examples before inventing labels or edge kinds.
- Saved searches often model pathfinding with `r.traversable = True`; preserve that filter when adapting attack-path queries.
- Site scoping matters. Always identify whether permissions are global tenant-wide or site-limited.
- Disabled accounts/API clients can still be useful for hygiene and historical context; do not treat them as active control without validating properties.
- Return full paths for attack-path triage and concise node tables for inventory/hygiene.

## Good starting points

- Query index: `../query-indexes/openhound-jamf.md`
- Query snapshots: `../query-snapshots/openhound-jamf/saved-searches/`
- Example Cypher: `../examples/example-cypher.md`
- Node/edge reference: `../examples/node-edge-reference.md`
- Collector source index: `collector-source-index.md`
- Local JamfHound examples: `../examples/jamfhound/`
- JamfHound repository: https://github.com/SpecterOps/JamfHound
- OpenHound Jamf node docs example: https://bloodhound.specterops.io/opengraph/extensions/jamfhound/reference/nodes/jamf_computer
