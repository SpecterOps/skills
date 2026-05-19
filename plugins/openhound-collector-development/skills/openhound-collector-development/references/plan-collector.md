# OpenHound Plan Collector

Use this reference before implementing a new collector or making broad collector changes. The output should be a concise design brief that maps the target service into OpenHound resources, graph nodes, edges, and follow-up implementation references.

Do not implement collection, models, lookup logic, or metadata from this reference. Use it to decide what should be built and in what order.

## Inputs To Gather

- Target service name, slug, and intended short graph prefix.
- Authentication method, required credentials, and non-secret configuration values.
- API base URL, versioning model, pagination style, rate limits, and retry behavior.
- Primary resources to collect, such as users, groups, devices, roles, policies, repositories, or memberships.
- Sample API responses or schema references for each resource.
- Stable identifiers for each resource.
- Relationships between resources and whether they can be emitted directly or need lookup/preproc.
- Any sensitive fields that should not be collected or emitted.
- Expected commands or environments used to validate the collector.

If required information is missing, ask focused questions before designing implementation details.

## Planning Checklist

### 1. Service Identity

Define the collector identity:

- Source name and source_kind  used by `OpenHound("<source>", source_kind=<kind>)`.
- Python package name, normally `openhound_<source>`.
- Short uppercase graph prefix, usually two to four characters.
- Extension metadata values for `extension.yaml`.

### 2. Credentials And Configuration

List required secrets and parameters:

- DLT secret names expected under `[sources.source.<source>]`.
- Environment variable equivalents where useful.
- Non-secret parameters such as tenant, organization, region, or API host.
- Whether a dedicated `auth.py` module is likely needed.

### 3. Resources To Collect

Create a resource inventory:

| Resource | API endpoint | DLT table | Model | Notes |
|---|---|---|---|---|
| users | `/users` | `users` | `User` | Example top-level resource. |

For each resource, decide whether it should be a top-level `@app.resource` or a nested `@app.transformer`.

### 4. Graph Shape

Create a graph inventory:

| Node | Kind constant | Source resource | Stable ID | Notes |
|---|---|---|---|---|
| User | `USER` | `users` | Native user ID | Example node. |

Include one root/environment node for the collected environment. Other emitted nodes should set `environmentid` to that node's OpenGraph ID.

| Edge | Start | End | Source resource | Lookup needed |
|---|---|---|---|---|
| `MEMBER_OF` | User | Group | memberships | No |

Prefer native opaque/global IDs when available. Do not plan raw integer primary keys as OpenGraph node IDs unless they are converted into stable, collision-resistant IDs.

### 5. Lookup And Preproc Needs

Identify where direct conversion is not enough:

- Relationships requiring joins across collected tables.
- Display or context fields that need enrichment from another table.
- Derived tables that should be created in `transforms.py`.
- Lookup methods that should be cached in `lookup.py`.

If no cross-table resolution is needed, explicitly say preproc/lookup is not required.

### 6. Implementation Order

Map the plan to references:

1. `references/graph-schema.md` for graph base types and ID strategy.
2. `references/register-extension.md` for phase registration and metadata.
3. `references/source-collection.md` for API resources and transformers.
4. `references/add-asset.md` for each model, node, edge, and kind constant.
5. `references/preproc-lookup.md` only when cross-table lookup is required.
6. `references/validate-extension.md` before finishing.

## Output Format

Produce a short collector design brief:

```markdown
# Collector Plan: <Service>

## Assumptions
- <assumption or question>

## Credentials And Parameters
- <secret or parameter>

## Resources
| Resource | API endpoint | DLT table | Model | Type |
|---|---|---|---|---|

## Graph
| Node | Kind | Stable ID | Source |
|---|---|---|---|

| Edge | Start | End | Source | Lookup needed |
|---|---|---|---|---|

## Preproc And Lookup
- <needed/not needed and why>

## Implementation Sequence
1. <reference and concrete target>
```

Keep the brief practical. Avoid speculative resources, edges, or abstractions that are not supported by the target service requirements or API data.
