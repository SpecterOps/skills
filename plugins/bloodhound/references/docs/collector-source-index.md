# Collector Source Index

Use this index to identify collector outputs, upstream examples, and local references before writing BloodHound/OpenGraph analysis guidance.

## GitHound / OpenHound GitHub

- Repository: https://github.com/SpecterOps/GitHound
- Local saved queries: `references/query-snapshots/openhound-github/saved-queries/`
- Local query index: `references/query-indexes/openhound-github.md`
- Local small samples:
  - `references/examples/githound/samples/githound_saml_O_kgDOCoV2OQ.json`
  - `references/examples/githound/samples/githound_scim_O_kgDOCoV2OQ.json`
- Upstream large sample, intentionally not vendored: https://github.com/SpecterOps/GitHound/blob/main/samples/githound_O_kgDOCoV2OQ.json
- Upstream node docs: https://github.com/SpecterOps/GitHound/tree/main/Documentation/NodeDescriptions
- Upstream edge docs: https://github.com/SpecterOps/GitHound/tree/main/Documentation/EdgeDescriptions
- Useful upstream docs: `Documentation/Schema.md`, `Documentation/Queries.md`, `Documentation/SCIMSamlProviderComparison.md`, `model.json`, `model.mermaid`, `schema.json`, `bh-github-custom-nodes.json`.

## JamfHound / OpenHound Jamf

- Repository: https://github.com/SpecterOps/JamfHound
- Local saved searches: `references/query-snapshots/openhound-jamf/saved-searches/`
- Local query index: `references/query-indexes/openhound-jamf.md`
- Local schema examples: `references/examples/jamfhound/schema/`
- Local object examples: `references/examples/jamfhound/objects/`
- Upstream examples: `schema/`, `objects/`, and `snippets/` in the JamfHound repository.
- Use the local examples for Jamf Pro object shape and schema expectations; use saved-search snapshots for actual path queries.

## OktaHound / OpenHound Okta

- Repository: https://github.com/SpecterOps/OktaHound
- Local saved searches: `references/query-snapshots/openhound-okta/saved-searches/`
- Local query index: `references/query-indexes/openhound-okta.md`
- Useful upstream files: `README.md`, `Roadmap.md`, `Src/SpecterOps.OktaHound/okta.sample.oauth.yaml`, `Src/SpecterOps.OktaHound/okta.sample.token.yaml`, and model classes under `Src/SpecterOps.OktaHound/Model/`.
- Current local references do not vendor generated OktaHound sample data because the upstream repository exposes model/config examples rather than compact generated graph samples.

## SCIM

- Official overview: https://bloodhound.specterops.io/opengraph/extensions/scim/overview
- Official schema: https://bloodhound.specterops.io/opengraph/extensions/scim/schema
- Extension schema repo: https://github.com/SpecterOps/bloodhound-scim-extension
- Local methodology: `references/docs/scim-methodology.md`

## OpenGraph management

- Official management docs: https://bloodhound.specterops.io/opengraph/extensions/manage
- Local methodology: `references/docs/opengraph-extension-management.md`
