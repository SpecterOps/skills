---
name: openhound-github
description: "Use for OpenHound GitHub/GitHound OpenGraph BloodHound work when the user clearly means GitHub semantics such as enterprises, organizations, repositories, teams, branch protection, Actions policy, secrets or variables metadata, app installations, personal access tokens, GitHub-to-Azure OIDC or federated identity paths, SAML external identities, or SSO/SCIM links from Azure, Okta, or SCIM identities. Do not use for generic BloodHound path triage, connection checks, explicit Cypher authoring/review, or non-GitHub OpenGraph domains."
icon: ./assets/icon.png
---

# OpenHound GitHub / GitHound

Use this skill for OpenHound GitHub OpenGraph query design and attack-path triage with GitHound-collected GitHub data.

## Required context

- Authorized GitHub enterprises, organizations, and repositories.
- Whether GitHound/OpenHound GitHub schema/data is loaded.
- Whether SAML external identity, SCIM, Azure, Okta, or other linked identity data is available.
- Target repositories, teams, users, actions policies, environments, secrets, PATs, apps, or cloud identities.

## Workflow

1. Read `../../references/docs/bloodhound-query-methodology.md`, `../../references/docs/openhound-github-methodology.md`, and `../../references/docs/collector-source-index.md`.
2. If SCIM, SAML, SSO, Okta, Azure, or external identity links are relevant, read `../../references/docs/scim-methodology.md` and inspect the small GitHound examples under `../../references/examples/githound/samples/`.
3. Search `../../references/query-indexes/openhound-github.md` and `../../references/examples/example-cypher.md` for a saved-query starting point.
4. Inspect the referenced JSON snapshot and adapt parameters safely.
5. Preserve `GH_` labels/edges, `SCIM_*` bridge labels/edges, and permission-inheritance path shape.
6. Separate posture checks from attack paths and list false-positive validation steps.

## Common pivots

- GitHub users/teams to repo admin/write access.
- Branch protection bypass and dangerous branch permissions.
- Actions policy, SHA pinning, workflow dispatch, runner, and secret exfiltration risk.
- Secrets/variables scope exposure and secret scanning alert metadata.
- App installations and PATs with broad repository access.
- GitHub OIDC to Azure federated identity credentials.
- External identities without SCIM and SCIM-provisioned identities mapped to GitHub users/teams.

## Output

Use the shared output contract from `$bloodhound-query` and include GitHub-specific caveats such as enterprise/org coverage, Actions settings collection, SAML/SCIM data availability, secret metadata limitations, and linked-identity confidence.
