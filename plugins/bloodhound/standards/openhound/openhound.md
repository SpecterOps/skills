# OpenHound Standards

OpenHound is a resource collector built on DLT that converts upstream service resources into BloodHound-compatible OpenGraph nodes and edges.

## Core Architecture

Every collector follows the same three-phase pipeline:

```text
collect -> preproc -> convert
```

| Phase | Purpose |
|---|---|
| `collect` | Collect upstream API data and write raw JSONL tables. |
| `preproc` | Optionally load raw tables into DuckDB and build lookup/derived tables. |
| `convert` | Read JSONL plus lookup data and emit OpenGraph nodes/edges. |

All phases are registered in `src/<pkg>/main.py` using one `OpenHound("<source>", <root-kind>)` app instance and the `@app.collect()`, `@app.preproc()`, and `@app.convert()` decorators.

## Naming Conventions

Derive a short uppercase prefix from the service slug, usually two to four characters, and use it consistently across class names and kind strings.

| Service slug | Prefix | Example class | Example kind |
|---|---|---|---|
| `okta` | `OK` | `OKNode` | `OK_User` |
| `github` | `GH` | `GHNodeProperties` | `GH_Repository` |
| `kubernetes` | `K8S` | `K8SLookup` | `K8S_Pod` |

Common patterns: `<PREFIX>NodeProperties`, `<PREFIX>Node`, `<PREFIX>EdgeProperties`, `<PREFIX>Lookup`.

## Required Rules

- Keep exactly one `OpenHound` app instance per extension, defined in `src/<pkg>/main.py`.
- Import `app` from `openhound_<pkg>.main`; do not create duplicate app instances.
- Define node kind strings in `src/<pkg>/kinds/nodes.py`.
- Define edge kind strings in `src/<pkg>/kinds/edges.py`.
- Import kind constants from `kinds/`. Do not hardcode kind strings in model files.
- Every collector must define and emit one root/environment node for the collected environment. For Okta this is an Organization node, for Jamf the Tenant node.
- Every emitted node must set `environmentid` to the OpenGraph ID of the collector's root/environment node.
- Use stable string node IDs from native opaque/global IDs when available.
- Do not use raw integer primary keys as OpenGraph node IDs.
- If no native ID exists, derive a stable ID with `BaseNode.guid(...)` from reproducible properties.
- Every graph property contains docstrings with an "Attributes" section describing each field.
- Keep `EdgeDef(...)` declarations aligned with the asset class that actually emits those edges.
- Prefer `ConditionalEdgePath` for edges to existing nodes when the target can be resolved by stable node properties; use `EdgePath(value=..., match_by="id")` when the exact stable OpenGraph node ID is known.
- Prefer yielding edges with `yield` / `yield from` instead of building edge lists.
- Run `preproc` before `convert` when `self._lookup` is used.

## Key Files

| File | Role |
|---|---|
| `src/<pkg>/main.py` | CLI phase registration and `OpenHound` app ownership. |
| `src/<pkg>/source.py` | DLT resources, transformers, source context, and API collection. |
| `src/<pkg>/graph.py` | Extension-specific node, node property, and edge property dataclasses. |
| `src/<pkg>/models/` | One file per collected entity or relationship asset. |
| `src/<pkg>/kinds/` | Node and edge kind constants. |
| `src/<pkg>/transforms.py` | DuckDB SQL transforms run during `preproc`. |
| `src/<pkg>/lookup.py` | Cached `LookupManager` methods used during `convert`. |
| `extension.yaml` | Extension metadata, credentials, and parameters. |
