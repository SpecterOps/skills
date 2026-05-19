---
name: openhound-okta
description: "Use for OpenHound Okta/OktaHound OpenGraph BloodHound work when the user clearly means Okta semantics such as Okta users, groups, apps, role assignments, super-admin or delegated-admin exposure, API clients and client secrets, MFA or password posture, AD agents, identity providers, inbound or outbound hybrid paths, SCIM provisioning, or GitHub/Azure/Jamf/Entra linked identity paths. Do not use for generic BloodHound path triage, connection checks, explicit Cypher authoring/review, or non-Okta OpenGraph domains."
---

# OpenHound Okta / OktaHound

Use this skill for OpenHound Okta OpenGraph query design and attack-path triage with OktaHound/OpenHound Okta data.

## Required context

- Authorized Okta organizations and linked identity/application platforms.
- Whether OktaHound/OpenHound Okta extension/schema/data is loaded and whether optional schemas (SCIM, GitHub, Jamf, Azure/AD, Entra, SaaS integrations) are present.
- Collector authentication method and scope, such as OAuth private key vs SSWS/API token.
- Target users, groups, applications, role assignments, client secrets, devices, identity providers, or hybrid links.

## Workflow

1. Read `../../references/docs/bloodhound-query-methodology.md`, `../../references/docs/openhound-okta-methodology.md`, and `../../references/docs/collector-source-index.md`.
2. If provisioning, SSO, GitHub, Jamf, Entra, or SCIM bridge paths are relevant, read `../../references/docs/scim-methodology.md`.
3. Search `../../references/query-indexes/openhound-okta.md` and `../../references/examples/example-cypher.md` for a saved-search starting point.
4. Inspect the referenced JSON snapshot before adapting.
5. Preserve `Okta_` and `SCIM_` labels/edges and explicitly document bridge edges in hybrid paths.
6. Separate app/secret metadata risk from proven secret disclosure and identify collector output/coverage limits.

## Common pivots

- Users/groups to super-admin or delegated-admin capability.
- App assignments and app credentials/client secret access.
- API service applications and privileged integrations.
- MFA/password/device posture queries.
- AD agents, SCIM links, inbound/outbound federation, GitHub/Azure/Jamf hybrid paths, and other collected SaaS links.

## Output

Use the shared output contract from `$bloodhound-query` and include Okta-specific caveats such as optional schema availability, collector auth scope, linked-platform coverage, secret metadata limitations, and hybrid bridge confidence.
