---
name: openhound-development
description: Use for OpenHound collector and OpenGraph extension development work, including planning, graph schema, source collection, assets, lookup/preproc, registration, validation, and collector template adaptation under the BloodHound plugin.
metadata:
  author: "GhostWorks"
---

# OpenHound Development

Use this skill for any OpenHound collector task.

## Critical Rules (Always apply)

1. Read `../../standards/openhound/openhound.md` before editing collector code when working from this plugin, or `.agents/standards/openhound.md` inside a generated collector repo. This includes important standards and best practices for OpenHound collector development that are not repeated in the reference docs.
2. Based on the requested task, select the matching reference from the routing table. These contain specific rules and examples for different types of collector work.
3. For broad collector work, or when creating a new collector, read `../../standards/openhound/workflow.md` when working from this plugin, or `.agents/standards/workflow.md` inside a generated collector repo.
4. Important: Before finishing collector and graph behavior changes read `references/validate-extension.md`.

### Route By Task

| Task | Reference |
|---|---|
| Plan a new collector from API docs, sample responses, or requirements | `references/plan-collector.md` |
| Define graph base classes, common properties, node IDs, or edge properties | `references/graph-schema.md` |
| Register `collect`, `preproc`, `convert`, metadata, or entry points | `references/register-extension.md` |
| Implement API clients, auth, DLT resources, transformers, or secrets | `references/source-collection.md` |
| Add or modify models, node assets, edge assets, kind constants, or exports | `references/add-asset.md` |
| Add DuckDB transforms, lookup methods, lookup registration, or `self._lookup` usage | `references/preproc-lookup.md` |
| Validate collector changes before finishing | `references/validate-extension.md` |

### Routing Rules

- If the task touches multiple areas, read every matching reference.
- If adding or changing collector behavior, always read `references/validate-extension.md` before finishing.
- If the task involves a new collector or broad redesign, start with `references/plan-collector.md`.
- If models use `self._lookup`, also read `references/preproc-lookup.md` and `references/register-extension.md`.
- If adding a new collected resource, usually read `references/source-collection.md`, `references/add-asset.md`, and `references/validate-extension.md`.
