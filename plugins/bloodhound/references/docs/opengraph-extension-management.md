# OpenGraph Extension Management Methodology

Use this reference before making claims about OpenGraph structured graph availability, collector compatibility, schema updates, data upload, saved-query import, or privilege-zone behavior.

## Structured vs generic graphs

- Generic OpenGraph payloads use the basic node/edge/metadata format and support basic exploration.
- Structured graphs require an installed extension definition schema and data that conforms to that schema.
- Structured graphs unlock extension-aware capabilities such as node search, Cypher search, bulk data removal, pathfinding, and future finding/posture features depending on edition and release status.

## Operating workflow

1. Identify the platform collector and generated payloads: GitHound, JamfHound/OpenHound Jamf, OktaHound/OpenHound Okta, AzureHound, SharpHound, or custom collector.
2. Confirm the matching extension definition schema is installed. For SCIM-aware paths, confirm SCIM plus each platform schema is installed.
3. Confirm saved queries and privilege-zone rules were imported when the assessment depends on them.
4. Validate collection recency, collector version, schema version, and ingest status before interpreting missing nodes or edges as absent risk.
5. Use the domain query index and example references before inventing labels or edge kinds.

## Edition and permission notes

- Extension definition schema upload/delete requires BloodHound Administrator privileges.
- BloodHound Enterprise can ingest supported collector payloads through API-driven workflows.
- BloodHound Community requires manual upload of locally generated collector payloads.
- Deleting an extension removes the schema but leaves underlying data. The data reverts to generic graph behavior until structured schema support is restored.

## Update guidance

- Treat collectors and extension schemas as a compatibility pair.
- Update collector and schema artifacts together whenever possible.
- Before updating a collector alone, confirm the emitted node/edge kinds still match the installed extension schema.
- After upload, validate extension presence, file ingest completion, and representative node/edge counts.

## Analysis checklist

- Which extension schemas are installed?
- Which collector version produced the payload?
- Which payload files were ingested, and when?
- Are saved queries present or only raw Cypher available?
- Are SCIM/platform bridge schemas installed together?
- Is the graph structured or generic for the platform being queried?

## Sources

- OpenGraph extension management: https://bloodhound.specterops.io/opengraph/extensions/manage
- OpenGraph library: https://bloodhound.specterops.io/opengraph/library
