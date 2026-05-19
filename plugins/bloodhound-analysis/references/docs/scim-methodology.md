# SCIM Methodology for BloodHound OpenGraph

Use this reference when GitHub, Okta, Entra, Jamf, or other OpenGraph data includes SCIM-provisioned identities. SCIM is a shared identity bridge, not a standalone collector workflow.

## Model summary

- SCIM is a schema-only OpenGraph extension. It must be installed alongside the platform schemas that produce or consume SCIM data.
- SCIM nodes are produced by other collectors, especially GitHound and OktaHound/OpenHound Okta.
- The top-level environment node is `SCIM_Organization`.
- Node kinds: `SCIM_User`, `SCIM_Group`, `SCIM_Role`, `SCIM_Organization`.
- Edge kinds:
  - `SCIM_Contains` — traversable container edge from organization to SCIM resources.
  - `SCIM_HasRole` — traversable user-to-role assignment.
  - `SCIM_ManagerOf` — non-traversable manager relationship.
  - `SCIM_MemberOf` — traversable user/group membership.
  - `SCIM_Provisioned` — traversable bridge from a SCIM resource to a resource in another extension.

## Analysis workflow

1. Confirm the SCIM extension schema is installed before treating `SCIM_*` labels as structured graph data.
2. Confirm the producing collector ran with SCIM-capable configuration and emitted SCIM payloads.
3. Start from saved-query patterns:
   - GitHub external identities without SCIM: `references/query-snapshots/openhound-github/saved-queries/external-identities-without-scim.json`
   - GitHub hybrid identities: `references/query-snapshots/openhound-github/saved-queries/hybrid-identities.json`
   - Okta SCIM apps receiving password updates: `references/query-snapshots/openhound-okta/saved-searches/scim-read-passwords.json`
   - Okta hybrid synchronization: `references/query-snapshots/openhound-okta/saved-searches/hybrid-sync.json`
4. Identify bridge direction explicitly. Do not collapse `Okta_User -> SCIM_User -> GH_User` into a direct Okta-to-GitHub claim unless the graph contains the bridge edges.
5. Report whether a path is based on SAML/external identity, SCIM provisioning, Okta push/pull synchronization, or another hybrid mechanism.

## Common questions

- Which GitHub users have linked external identities but no SCIM username?
- Which SCIM users/groups are provisioned into GitHub users/teams or another extension node?
- Which Okta apps receive password updates through SCIM-like provisioning paths?
- Which privileged GitHub users or teams map back to Okta/Entra identities through SCIM?
- Which SCIM groups or roles give transitive access to a target system through `SCIM_MemberOf`, `SCIM_HasRole`, and `SCIM_Provisioned`?

## Caveats

- SCIM absence is not proof of unmanaged access; verify collector coverage and enterprise/org configuration.
- `SCIM_ManagerOf` is informational/non-traversable and should not be used as a compromise path edge.
- SCIM user names, external identity IDs, and provider-specific IDs can drift. Validate high-impact identity joins against source platform records.
- GitHub and Okta collectors may produce both platform-native bridge edges and SCIM bridge edges. Preserve both in path explanations.

## Sources

- Official SCIM overview: https://bloodhound.specterops.io/opengraph/extensions/scim/overview
- Official SCIM schema: https://bloodhound.specterops.io/opengraph/extensions/scim/schema
- SCIM extension schema repository: https://github.com/SpecterOps/bloodhound-scim-extension
