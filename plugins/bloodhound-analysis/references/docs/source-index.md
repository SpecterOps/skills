# BloodHound Analysis Source Index

Use this index before writing or adapting BloodHound queries. The repo vendors query snapshots and small examples for offline reference, while official docs remain the canonical behavioral reference.

## Official BloodHound docs

- Search with Cypher: https://bloodhound.specterops.io/analyze-data/explore/cypher-search
- Supported Cypher syntax: https://bloodhound.specterops.io/analyze-data/explore/cypher-supported
- Edges overview: https://bloodhound.specterops.io/resources/edges/overview
- Traversable and non-traversable edges: https://bloodhound.specterops.io/resources/edges/traversable-edges
- Azure/Entra base node reference: https://bloodhound.specterops.io/resources/nodes/az-base
- OpenGraph requirements: https://bloodhound.specterops.io/opengraph/requirements
- OpenGraph graph structure and extension management: https://bloodhound.specterops.io/opengraph/extensions/manage
- OpenGraph FAQ: https://bloodhound.specterops.io/opengraph/faq
- OpenHound GitHub queries: https://bloodhound.specterops.io/opengraph/extensions/github/queries
- OpenHound Jamf node reference example: https://bloodhound.specterops.io/opengraph/extensions/jamfhound/reference/nodes/jamf_computer
- OpenHound Okta getting started: https://bloodhound.specterops.io/opengraph/extensions/oktahound/getting-started
- SCIM overview: https://bloodhound.specterops.io/opengraph/extensions/scim/overview
- SCIM schema: https://bloodhound.specterops.io/opengraph/extensions/scim/schema

## Collector and OpenGraph methodology

- Collector source index: `collector-source-index.md`
- SCIM methodology: `scim-methodology.md`
- OpenGraph extension management methodology: `opengraph-extension-management.md`
- GitHub methodology: `openhound-github-methodology.md`
- Jamf methodology: `openhound-jamf-methodology.md`
- Okta methodology: `openhound-okta-methodology.md`

## Vendored upstream query snapshots

- BloodHound Query Library: `../query-snapshots/bloodhound-query-library/queries/`
- OpenHound GitHub saved queries: `../query-snapshots/openhound-github/saved-queries/`
- OpenHound Jamf saved searches: `../query-snapshots/openhound-jamf/saved-searches/`
- OpenHound Okta saved searches: `../query-snapshots/openhound-okta/saved-searches/`
- Snapshot manifest and license notice: `../query-snapshots/manifest.json`, `../query-snapshots/NOTICE.md`

## Examples and compact references

- Curated example Cypher: `../examples/example-cypher.md`
- Node/edge reference: `../examples/node-edge-reference.md`
- GitHound SAML/SCIM small samples: `../examples/githound/samples/`
- JamfHound schema examples: `../examples/jamfhound/schema/`
- JamfHound object examples: `../examples/jamfhound/objects/`

## Domain indexes

- BloodHound AD/ADCS: `../query-indexes/bloodhound.md`
- AzureHound / Entra ID: `../query-indexes/azurehound.md`
- OpenHound GitHub: `../query-indexes/openhound-github.md`
- OpenHound Jamf: `../query-indexes/openhound-jamf.md`
- OpenHound Okta: `../query-indexes/openhound-okta.md`
- Static safety scan: `../query-indexes/safety-scan.md`
