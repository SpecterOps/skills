# Example Cypher Patterns

These examples are read-only starting points. Prefer the referenced saved-query snapshot when it exists, then adapt parameters, labels, and edge filters to the target graph.

## GitHub external identities without SCIM

Snapshot: `references/query-snapshots/openhound-github/saved-queries/external-identities-without-scim.json`

```cypher
MATCH (ei:GH_ExternalIdentity)
WHERE ei.scim_identity_username = ''
RETURN ei
LIMIT 1000
```

Use this to find GitHub external identities that may not be managed by SCIM deprovisioning. Validate enterprise/org SCIM configuration and collector coverage before treating results as unmanaged access.

## GitHub hybrid identities

Snapshot: `references/query-snapshots/openhound-github/saved-queries/hybrid-identities.json`

```cypher
MATCH p=(s)-[]->(d:GH_User)
WHERE s:AZUser
OR s:Okta_User
RETURN p
LIMIT 1000
```

Use this as a broad external-identity pivot. For SCIM-specific analysis, add `SCIM_*` labels and `SCIM_Provisioned` paths once SCIM data is confirmed.

## SCIM provisioned resources to GitHub users

Curated pattern based on the SCIM schema. Confirm `SCIM_Provisioned` exists in the graph before relying on it.

```cypher
MATCH p = (:SCIM_Organization)-[:SCIM_Contains]->(s:SCIM_User)-[:SCIM_Provisioned]->(g:GH_User)
RETURN p
LIMIT 1000
```

Use this to explain identity bridge paths without inventing direct Okta/Entra-to-GitHub edges.

## SCIM group and role transitive membership

Curated pattern based on the SCIM schema.

```cypher
MATCH p = (:SCIM_User)-[:SCIM_MemberOf|SCIM_HasRole*1..3]->(target)
WHERE target:SCIM_Group OR target:SCIM_Role
RETURN p
LIMIT 1000
```

Use bounded hops and avoid `SCIM_ManagerOf` for pathfinding because it is non-traversable.

## Okta SCIM apps receiving password updates

Snapshot: `references/query-snapshots/openhound-okta/saved-searches/scim-read-passwords.json`

```cypher
MATCH p = (:Okta_Organization)-[:Okta_Contains]->(:Okta_Application)-[:Okta_ReadPasswordUpdates]->(:Okta_User)
RETURN p
LIMIT 1000
```

Use this as a posture query for applications receiving password updates. Treat it as app-assignment/provisioning exposure, not cleartext password disclosure.

## Okta hybrid synchronization

Snapshot: `references/query-snapshots/openhound-okta/saved-searches/hybrid-sync.json`

```cypher
MATCH p = (:Okta_Organization)-[:Okta_Contains]->(:Okta)-[:Okta_UserPull|Okta_UserPush|Okta_GroupPull|Okta_GroupPush]->(:Okta)
RETURN p
LIMIT 1000
```

Use this to discover synchronization paths and then pivot into privileged role or application assignment queries.

## Jamf Tier 1 to Tier 0 paths

Snapshot: `references/query-snapshots/openhound-jamf/saved-searches/Jamf_Tier_1_to_Tier_0_Attack_Paths.json`

```cypher
MATCH p=(s)-[r*1..5]->(t)
WHERE s.Tier = 1 AND t.Tier = 0
AND s.primarykind <> 'jamf_Tenant'
AND s.primarykind <> 'jamf_Site'
AND r.traversable = True
RETURN p
LIMIT 1000
```

Preserve `r.traversable = True` when adapting Jamf attack-path queries.

## Cross-platform SCIM to GitHub repository control

Curated pattern for follow-up analysis once SCIM and GitHub data are confirmed.

```cypher
MATCH p = (:SCIM_User)-[:SCIM_Provisioned]->(:GH_User)-[*1..4]->(repo:GH_Repository)
WHERE all(rel IN relationships(p) WHERE coalesce(rel.traversable, true) = true)
RETURN p, repo.name AS repository
LIMIT 1000
```

Replace the variable-length segment with specific `GH_*` relationship kinds when possible to reduce false positives and improve performance.
