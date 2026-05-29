---
name: openhound-jamf
description: "Use for OpenHound Jamf/JamfHound OpenGraph BloodHound work when the user clearly means Jamf semantics such as Jamf tenant, site, account, group, computer, API-client exposure, Tier 1 to Tier 0 paths, policy/script/profile management privileges, traversable Jamf edges, Jamf SSO links, Okta/Jamf hybrid links, or Jamf device-management attack-path analysis. Do not use for generic BloodHound path triage, connection checks, explicit Cypher authoring/review, or non-Jamf OpenGraph domains."
license: MIT
metadata:
  author: turbo
  version: "0.1.0"
  category: security
---

# OpenHound Jamf / JamfHound

Use this skill for OpenHound Jamf OpenGraph query design and attack-path triage with JamfHound/OpenHound Jamf data.

## Required context

- Authorized Jamf tenants/sites and managed device scope.
- Whether JamfHound/OpenHound Jamf extension/schema/data is loaded.
- Collector account type/permissions, Jamf Cloud vs on-prem context, and site scoping.
- Target accounts, groups, API clients, sites, computers, tenant objects, policies, scripts, or profiles.

## Workflow

1. Read `../../references/docs/bloodhound-query-methodology.md`, `../../references/docs/openhound-jamf-methodology.md`, and `../../references/docs/collector-source-index.md`.
2. Inspect JamfHound schema/object examples under `../../references/examples/jamfhound/` when node/property shape matters.
3. Search `../../references/query-indexes/openhound-jamf.md` and `../../references/examples/example-cypher.md` for a saved-search starting point.
4. Inspect the referenced JSON snapshot before adapting.
5. Preserve `jamf_` labels/edges and `r.traversable = True` filters where the source query uses them.
6. Distinguish tenant-wide paths from site-scoped permissions and identify hybrid identity/device bridge assumptions.

## Common pivots

- Accounts/groups/API clients to tenant administration.
- Site-scoped admin paths to managed computers.
- Policy/script/profile creation or modification control.
- Disabled principal hygiene and stale access.
- Jamf paths linked to SSO/identity providers when hybrid data exists.
- Okta/Jamf hybrid device-management paths when OktaHound or another collector produced bridge data.

## Output

Use the shared output contract from `$bloodhound-query` and include Jamf-specific caveats such as site scoping, collector account privilege, disabled-account interpretation, extension/schema availability, hybrid bridge availability, and managed-device collection completeness.
