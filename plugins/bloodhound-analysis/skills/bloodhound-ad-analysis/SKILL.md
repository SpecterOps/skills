---
name: bloodhound-ad-analysis
description: "Use for BloodHound Active Directory and ADCS attack-path work when the user clearly means on-prem AD semantics: find a path to Domain Admin, DA, Tier Zero, Domain Controllers, or privileged groups; investigate DCSync, ACL abuse, delegation, sessions, local admin, trusts, GPO abuse, LAPS/gMSA, Kerberoasting, AS-REP roasting, or ADCS ESC paths; or explain AD hygiene and privilege exposure in a BloodHound graph. Do not use for generic BloodHound connection checks, unclear graph-domain triage, explicit Cypher authoring/review, or Azure/OpenHound/OpenGraph-specific work."
---

# BloodHound AD/ADCS

Use this skill for classic BloodHound Active Directory and ADCS query design and attack-path triage.

## Direct triggers

Use this skill when the task mentions any of the following:

- path to Domain Admin
- path to DA
- path to Tier Zero
- path to a domain controller
- DCSync exposure
- ADCS ESC1 / ESC2 / ESC3 / ESC4 / ESC5 / ESC6
- session paths
- local admin paths
- GPO abuse
- ACL abuse
- trust path
- LAPS or gMSA exposure
- Kerberoasting or AS-REP roasting

## Do not use for

- generic BloodHound health or connection checks
- “analyze this BloodHound graph” when the domain is not yet clear
- explicit Cypher/query-writing requests
- AzureHound, OpenHound, or OpenGraph extension work

## Required context

- Authorized scope: domains, forests, tiers, and target objects.
- Data quality: SharpHound collection type/recency, ADCS collection availability, and whether sessions/local admin data are current.
- If MCP/live graph access is unavailable, write queries and triage workflow only; do not assert live findings.

## Workflow

1. Read `../../references/docs/bloodhound-query-methodology.md` and `../../references/docs/bloodhound-methodology.md`.
2. Search `../../references/query-indexes/bloodhound.md` for a Query Library starting point.
3. Inspect the referenced snapshot before adapting the query.
4. Prefer precise labels/edges and bounded hop counts.
5. For each result, classify confirmed graph facts vs inferred risk and include remediation-oriented notes.

## Common pivots

- Low-privileged principals to Tier Zero groups or domain controllers.
- Admin/session/local admin paths to sensitive computers.
- ACL edges to user/group/computer/GPO/domain compromise.
- Delegation and SPN exposure.
- ADCS template/CA/NTAuth/ESC paths.
- Trust paths and cross-domain privileges.

## Output

Use the shared output contract from `$bloodhound-query` and include AD-specific caveats such as collection recency, domain suffix casing, nested group depth, session freshness, and ADCS edge traversability.
