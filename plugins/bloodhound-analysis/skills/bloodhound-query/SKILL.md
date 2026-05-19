---
name: bloodhound-query
description: "Use when the user explicitly wants BloodHound Cypher or query work: write a BloodHound query, review or explain Cypher, optimize a query, adapt a saved query, validate query safety or performance, convert a graph question into query syntax, or design follow-up graph questions across BloodHound CE/BHE, AzureHound, OpenHound GitHub, OpenHound Jamf, OpenHound Okta, or other OpenGraph data. Do not use as the default entry skill for generic path triage, connection checks, or AD/Azure/OpenHound exposure analysis when no explicit query-authoring task is requested."
---

# BloodHound Query Workflow

Use this as the shared query authoring/review workflow across BloodHound, AzureHound, OpenHound GitHub, OpenHound Jamf, OpenHound Okta, and custom OpenGraph graphs.

## Direct triggers

Use this skill when the task mentions any of the following:

- write a BloodHound query
- write Cypher
- explain this Cypher
- review this query
- optimize this BloodHound query
- adapt this saved query
- turn this path question into Cypher
- validate this BloodHound query

## Route to instead

- Use `$bloodhound-analysis` for generic BloodHound asks or initial graph triage.
- Use the domain skill when the path question is clear and the user is asking for findings rather than query authoring: `$bloodhound-ad-analysis`, `$azurehound-analysis`, `$openhound-github`, `$openhound-jamf`, or `$openhound-okta`.

## Required context

- Confirm the assessment/lab is authorized and in scope.
- Identify the graph domain and available collectors/extensions.
- If live BloodHound MCP access is unavailable, produce a query/workflow plan and clearly avoid claiming observed graph facts.

## Workflow

1. Read `../../references/docs/bloodhound-query-methodology.md`.
2. Choose the domain skill when the graph is known: `$bloodhound-ad-analysis`, `$azurehound-analysis`, `$openhound-github`, `$openhound-jamf`, or `$openhound-okta`.
3. Use `../../references/docs/source-index.md` to locate the matching query index and snapshots.
4. Adapt a saved-query pattern first; only invent a new query when no pattern fits.
5. For OpenGraph work, inspect `../../references/examples/example-cypher.md` and `../../references/examples/node-edge-reference.md` before inventing labels or edge kinds.
6. For SCIM/hybrid identity work, read `../../references/docs/scim-methodology.md` and document each bridge edge explicitly.
7. Keep the query read-only, bounded, label-specific, and explicit about relationship direction.
8. Return the query with parameters, expected result shape, analysis guidance, caveats, and next queries.

## Output contract

- Query
- Parameters to replace
- Purpose
- Expected result shape
- Analysis guidance
- Caveats / data-quality assumptions
- Next queries
