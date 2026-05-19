# BloodHound Analysis Examples

This directory contains small vendored examples and curated query references for offline agent use.

## Contents

- `example-cypher.md` — compact read-only Cypher patterns and links to full saved-query snapshots.
- `node-edge-reference.md` — high-signal node and edge labels for GitHub, Jamf, Okta, and SCIM OpenGraph analysis.
- `githound/samples/` — small GitHound SAML and SCIM sample payloads. The large primary GitHound sample is intentionally linked from `docs/collector-source-index.md` instead of vendored.
- `jamfhound/schema/` — JamfHound schema examples from upstream.
- `jamfhound/objects/` — JamfHound object examples from upstream, normalized to valid JSON where needed.

## Use rules

- Treat examples as schema/query design aids, not proof that a client environment contains matching data.
- Prefer saved-query snapshots for production query adaptation.
- Confirm installed extension schemas and collector coverage before drawing assessment conclusions.
