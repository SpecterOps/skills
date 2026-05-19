# OpenHound Okta / OktaHound Methodology

Use for OpenHound Okta OpenGraph analysis with OktaHound/OpenHound Okta data.

## Collector context

- OktaHound models Okta organizations, users, groups, applications, admin roles, custom roles, resource sets, API service integrations, client secrets/JWKs, devices, agents, identity providers, policies, realms, and hybrid links.
- OktaHound supports configuration patterns such as OAuth private-key and SSWS/API-token collection. Prefer least-privilege, time-bound collector credentials and record which method was used.
- OktaHound can emit Okta graph output plus optional AD, Entra, GitHub, Jamf, OnePassword, Snowflake, and hybrid graph context depending on configuration and available source data.
- Current local references vendor saved searches, not generated OktaHound sample graph payloads. Use saved searches plus upstream model/config files listed in `collector-source-index.md`.

## Focus areas

- Okta super-admin and delegated-admin paths.
- Users, groups, applications, app assignments, role assignments, API service applications, client secrets, devices, factors, and identity providers.
- Password and MFA posture: weak/no MFA, password policy concerns, inactive users, and recovery flows where modeled.
- Hybrid paths: Okta to AD agents, SCIM provisioning, inbound federation, outbound application assignments, GitHub SSO, Jamf device-management links, Entra links, and other collected SaaS links.
- Privileged app/client-secret access and API integration blast radius.

## Query guidance

- OpenHound Okta labels and relationships generally use `Okta_` prefixes; SCIM-linked data uses `SCIM_` prefixes.
- Read `scim-methodology.md` before interpreting SCIM provisioning paths.
- Read `../examples/node-edge-reference.md` before inventing Okta labels or edges.
- Confirm the OpenHound Okta extension/schema and optional linked schemas (GitHub, Jamf, SCIM, Entra/AD) before mixed-platform conclusions.
- The collector models secret metadata and access relationships; avoid implying cleartext secret disclosure unless the query explicitly proves read/access control.
- For hybrid paths, state each bridge type (AD agent, SCIM, SSO/federation, app assignment, Jamf/GitHub link) and which collector produced it.
- Use saved-query patterns for app credentials, role assignments, high-risk groups, and hybrid inbound/outbound paths.

## Good starting points

- Query index: `../query-indexes/openhound-okta.md`
- Query snapshots: `../query-snapshots/openhound-okta/saved-searches/`
- Example Cypher: `../examples/example-cypher.md`
- Node/edge reference: `../examples/node-edge-reference.md`
- SCIM methodology: `scim-methodology.md`
- Collector source index: `collector-source-index.md`
- OktaHound repository: https://github.com/SpecterOps/OktaHound
- OpenHound Okta getting started: https://bloodhound.specterops.io/opengraph/extensions/oktahound/getting-started
- Okta client secret reference: https://bloodhound.specterops.io/opengraph/extensions/oktahound/reference/nodes/okta_clientsecret
