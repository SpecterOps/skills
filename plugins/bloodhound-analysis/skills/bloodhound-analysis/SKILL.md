---
name: bloodhound-analysis
description: "Use as the default router for generic BloodHound asks: check the BloodHound connection, verify MCP health, analyze BloodHound data, find or explain a path, inspect shortest paths, find a path to Domain Admin or Tier Zero, show exposure, run a BloodHound query, or triage graph results when the domain is not yet clear. Use BloodHound MCP for authorized BloodHound CE graph analysis, path triage, object lookup, data-quality checks, AD/ADCS/Azure/OpenGraph exposure mapping, and report-ready remediation output. Do not use for unrelated network recon or for domain-specific work that is clearly AzureHound, OpenHound, OpenGraph schema design, or explicit Cypher authoring/review."
icon: ./assets/icon.png
---

# BloodHound Analysis

## When to use

Use this skill as the MCP-aware router for authorized BloodHound analysis. It is optimized for repeatable graph workflows: dataset checks, object lookup, path analysis, query design, ADCS/Azure/OpenGraph code-review, and report-ready output.

## Direct triggers

Use this skill when the task mentions any of the following:

- check the BloodHound connection
- verify BloodHound MCP
- is BloodHound up
- analyze BloodHound data
- find a path
- shortest path
- path to Domain Admin
- path to DA
- path to Tier Zero
- show BloodHound exposure
- inspect this BloodHound result
- run a BloodHound query

## Route to instead

- Use `$bloodhound-ad-analysis` when the user clearly means AD/ADCS pathing such as DCSync, ESC paths, Domain Admins, trusts, sessions, or GPO/ACL abuse.
- Use `$bloodhound-query` when the user explicitly wants Cypher written, reviewed, optimized, explained, or adapted from saved queries.
- Use `$azurehound-analysis`, `$openhound-github`, `$openhound-jamf`, or `$openhound-okta` when the graph domain is explicit.
- Use `$bloodhound-opengraph` when the task is about custom node schemas, ingestors, or graph-model extension work.

## Required context

- Confirm the assessment or lab is authorized and in scope.
- Confirm `bloodhound_mcp` is configured and visible in `/mcp` before relying on live MCP tools.
- If MCP is unavailable, produce a query/workflow plan instead of claiming live graph facts. The repo includes optional MCP packaging for target environments, but repository work should not install or sync it into the current Codex config unless explicitly requested.
- Route domain-specific query work to `$bloodhound-query`, `$bloodhound-ad-analysis`, `$azurehound-analysis`, `$openhound-github`, `$openhound-jamf`, or `$openhound-okta` as appropriate.

## Default workflow

1. **Check data quality first**
   - Start with `data_quality(info_type="stats")` or `data_quality(info_type="platform_list")`.
   - Call out collection gaps before drawing conclusions.
2. **Find the right graph objects**
   - Use `domain_info(info_type="list")` and `domain_info(info_type="search", query=...)`.
   - Capture object IDs/names for every critical claim.
3. **Use the right composite tool before custom Cypher**
   - Prefer `user_info`, `group_info`, `computer_info`, `ou_info`, `gpo_info`, `graph_analysis`, and `adcs_info` for common questions.
   - Use `cypher_query(info_type="run", query=...)` only when the composite tools cannot answer cleanly.
4. **Load references before writing attack queries**
   - For custom query work, read `../../references/docs/bloodhound-query-methodology.md`.
   - For attack scenarios, use the relevant domain index in `../../references/query-indexes/` and adapt a known-good snapshot pattern.
   - For OpenGraph collector, SCIM, or hybrid identity work, also read `../../references/docs/collector-source-index.md`, `../../references/docs/scim-methodology.md`, `../../references/docs/opengraph-extension-management.md`, and `../../references/examples/` as relevant.
   - If MCP exposes live BloodHound resources such as `bloodhound://cypher/reference`, use them as live supplements, not replacements for the repo-packaged guidance.
5. **Produce assessment-ready output**
   - Separate confirmed graph facts from inferred risk.
   - Include affected entities, edge sequence, confidence, data-quality caveats, and remediation.

## Safety and quality rules

- Do not perform write actions such as custom node changes, asset group changes, saved query edits, or file uploads without explicit user confirmation.
- Use pagination (`limit`, `skip`) for broad queries.
- Never label a user, computer, or path as low risk without checking memberships, enabled/admincount status, and relevant edge context.
- Use uppercase names with domain suffixes when filtering BloodHound names, and lowercase property names such as `hasspn`, `enabled`, and `admincount`.
- Prefer remediation-focused wording over exploitation instructions unless the user explicitly asks for operator guidance in an authorized assessment.

## References

- Read `references/bloodhound-mcp-tools.md` for the expected MCP tool and resource surface.
- Read `../../references/docs/source-index.md` for official docs, collector references, examples, and vendored query indexes.
- Use `$bloodhound-query` for cross-domain query authoring/review.
- Use `$bloodhound-ad-analysis`, `$azurehound-analysis`, `$openhound-github`, `$openhound-jamf`, or `$openhound-okta` for domain-specific saved-query adaptation.
- Use `$bloodhound-opengraph` for custom node schema, OpenGraph modeling, and ingestor extension work.
