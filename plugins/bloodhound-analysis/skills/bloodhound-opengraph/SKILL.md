---
name: bloodhound-opengraph
description: "Use when creating or changing BloodHound OpenGraph extensions, custom node schemas, custom ingestors, edge models, or Cypher patterns that connect non-AD assets to BloodHound CE graph analysis. Use for graph-model design questions such as new node kinds, new relationship kinds, extension schema changes, or custom ingestor behavior. Do not use for routine BloodHound path triage, connection checks, or known OpenHound query adaptation; use $bloodhound-analysis, $bloodhound-query, $openhound-github, $openhound-jamf, or $openhound-okta instead."
icon: ./assets/icon.png
---

# BloodHound OpenGraph Skill

Use this skill when creating custom BloodHound schema/extensions, ingestors, or attack-path queries that require graph-model customization. For standard OpenHound GitHub/Jamf/Okta analysis, use the matching OpenHound domain skill instead.

## Input Contract
- Context describing the required extension (new node/edge types, ingestor data source, Cypher query need).

## Workflow
1. Read `../../references/docs/opengraph-extension-management.md` before making schema/install/upload recommendations.
2. Read `../../references/docs/collector-source-index.md` for GitHound, JamfHound, OktaHound, and SCIM source context.
3. Inspect `../../references/examples/node-edge-reference.md` and `../../references/examples/example-cypher.md` before proposing custom labels, edges, or queries.
4. For SCIM bridge modeling, read `../../references/docs/scim-methodology.md` and preserve `SCIM_*` labels/edges.
5. Separate extension schema design from collector implementation, saved queries, privilege-zone rules, and data payload upload steps.

## Output
- Documentation or code for custom node/edge definitions, ingestors, or Cypher queries aligned with BloodHound CE or OpenGraph extensions.
- Notes about performance, compatibility, and MITRE technique relevance.

## Notes
- This capability is flagged as in-development and may require extra data/model tuning later.
- Share the TODO tag `bloodhound-opengraph:in-progress` when passing the idea to other agents.
