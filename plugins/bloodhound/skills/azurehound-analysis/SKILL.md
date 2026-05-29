---
name: azurehound-analysis
description: "Use for AzureHound and BloodHound Azure or Entra ID attack-path work when the user clearly means Azure semantics such as Global Administrator, privileged Entra roles, service principals, applications, app roles, managed identities, subscriptions, resource groups, VMs, Key Vaults, or hybrid AD/Azure paths. Do not use for generic BloodHound connection checks, unclear graph-domain triage, explicit Cypher authoring/review, or OpenGraph schema-extension work."
metadata:
  author: "GhostWorks"
---

# AzureHound

Use this skill for AzureHound / Entra ID BloodHound query design and attack-path triage.

## Required context

- Authorized Azure tenants/subscriptions and whether AzureHound/Entra collection is present.
- Known object IDs, tenant names, privileged roles, subscriptions, or resource scopes.
- Hybrid collection availability when paths cross AD, GitHub, Okta, or SCIM.

## Workflow

1. Read `../../references/docs/bloodhound-query-methodology.md` and `../../references/docs/azurehound-methodology.md`.
2. Search `../../references/query-indexes/azurehound.md` for a matching Query Library pattern.
3. Inspect the snapshot and confirm `AZ*` labels/edges before adapting.
4. Use exact `objectid` filters when possible and bound broad tenant paths.
5. Explain each path segment by platform and collector source.

## Common pivots

- Users/groups/service principals to privileged Entra roles.
- App owners, app role assignments, credentials, and Graph API permission edges.
- Managed identities to Azure resources.
- Subscription/resource group/VM/Key Vault control paths.
- AAD/Entra Connect and synced identity bridges.
- GitHub/OIDC or Okta/SCIM hybrid paths when data is present.

## Output

Use the shared output contract from `$bloodhound-query` and include Azure-specific caveats such as display-name ambiguity, tenant-scale query cost, non-traversable Graph API edges, and collector freshness.
