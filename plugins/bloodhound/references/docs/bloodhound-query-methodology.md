# BloodHound Query Methodology

Use this as the shared workflow for BloodHound, AzureHound, OpenHound GitHub, OpenHound Jamf, OpenHound Okta, and custom OpenGraph query work.

## Core rules

- Work only in authorized assessment or lab scope.
- If no live MCP/graph access is available, produce a query plan and clearly label all conclusions as expected behavior, not observed facts.
- Use officially supported BloodHound Cypher syntax. Avoid Neo4j-only syntax unless the target environment explicitly supports it.
- Query read-only by default. Do not use `CREATE`, `MERGE`, `DELETE`, `SET`, `REMOVE`, custom-node mutations, asset-group edits, saved-query edits, upload, or clear-database behavior without explicit confirmation.
- Prefer labels, relationship types, bounded hops, `WHERE` filters, and `LIMIT` for performance.
- BloodHound relationship direction is the attack/privilege direction. Preserve arrows unless intentionally investigating reverse relationships.
- Pathfinding depends on traversable edges. Non-traversable edges can still explain why a traversable composite exists, but should not be treated as directly pathfinding-equivalent.
- Always report data-quality caveats: collection recency, missing collector coverage, missing OpenGraph extension/schema, empty node populations, and edition/backend limitations.

## Query-writing loop

1. Identify the platform: AD/ADCS BloodHound, AzureHound/Entra, OpenHound GitHub, OpenHound Jamf, OpenHound Okta, or mixed OpenGraph.
2. Read the domain skill and domain index. Prefer adapting a known saved-query pattern over inventing a broad graph crawl.
3. Confirm labels and edge names from docs, saved-query snapshots, or live schema/resource output.
4. Parameterize target names, IDs, domains, tenant names, repository names, or object IDs instead of hardcoding assessment-specific values.
5. Build the smallest query that answers the question. Use `shortestPath`/`allShortestPaths` only when a path result is required.
6. Add row limits and return the right result shape: `p` for visual path triage, node/edge properties for tables, `count()` for prevalence.
7. Explain expected result columns/path structure and how to validate false positives.
8. Provide follow-up queries that move from discovery -> triage -> confirmation -> reporting.

## Output contract

When asked for a query or analysis, return:

- **Query**: formatted Cypher ready to run or adapt.
- **Parameters**: values the operator must replace.
- **Purpose**: why this query is useful for attack-path analysis.
- **Expected result shape**: paths, nodes, rows, counts, or properties.
- **Analysis guidance**: how to interpret high-risk paths and edge sequences.
- **Caveats/confidence**: data completeness, extension/schema availability, and false-positive checks.
- **Next queries**: 2-5 follow-ups for deeper triage.

## Efficiency checklist

- Use `objectid` or exact `name` filters where available.
- Restrict labels (`:User`, `:Computer`, `:Group`, `:AZUser`, `:GH_Repository`, `:Okta_User`, etc.).
- Restrict edge types rather than using `[*]` for broad paths.
- Use bounded recursion (`*1..3`, `*1..5`) before unbounded recursion.
- Start with `LIMIT 100`/`LIMIT 1000` for exploration, then remove or page only when exporting validated results.
- Split very broad mixed-platform paths into staged `MATCH`/`WITH` blocks.
