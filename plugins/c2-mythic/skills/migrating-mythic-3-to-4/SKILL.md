---
name: migrating-mythic-3-to-4
description: Audit and migrate Mythic 3.4 servers, payload types, C2 profiles, translation or consuming containers, eventing workflows, scripting clients, and other integrations to Mythic 4. Use for v3-to-v4 upgrade planning, compatibility reviews, breaking-change remediation, or migration failures; do not use for ordinary Mythic feature development with no version migration.
license: UNLICENSED
metadata:
  author: "SpecterOps"
  version: "0.1.0"
  category: security
---

# Migrating Mythic 3 to 4

Migrate Mythic 3.4 components to Mythic 4 with an evidence-backed inventory, bounded code changes, and development-environment validation. Treat Mythic 4 beta APIs and release-candidate dependency versions as moving targets: verify current primary documentation and package releases before changing version pins.

## Scope and safety

- Confirm that the source is Mythic 3.4. For an older version, follow the intervening official upgrade guides instead of assuming a direct migration.
- Distinguish repository migration from a live server upgrade. Do not stop services, run database migrations, reinstall containers, rotate tokens, or restore backups unless the user explicitly placed that environment in scope.
- For a live upgrade, require a tested database backup and Mythic-managed file backup before starting. A v3.4 service must not use a database after v4 migrations have run.
- Prefer a development instance during the public beta. Record the exact Mythic branch/tag and container-library versions used for reproducibility.
- Never expose API-token values in output, tests, diffs, or logs. Mythic 4 tokens are opaque, scoped, and displayed only once.

## Workflow

1. **Establish the migration boundary**
   - Identify the Mythic server version and every in-scope component: payload type, wrapper, C2 profile, translation container, webhook or consuming container, browser script, eventing workflow, Mythic Scripting client, or hand-written RabbitMQ client.
   - Determine whether the request is an audit, plan, code migration, development deployment, or production upgrade.
   - Preserve unrelated local changes and capture the current test/build commands before editing.

2. **Refresh authoritative requirements**
   - Read the [official Mythic 3.4 to 4.0 guide](https://docs.mythic-c2.net/version-4.0/updating/mythic-3.4-greater-than-4.0-updates).
   - Use the [Mythic 4 public-beta announcement](https://specterops.io/blog/2026/08/04/mythic-4-public-beta/) for release context, not as the sole source for API details.
   - Resolve current compatible package versions from official Mythic sources. The prerelease versions in the upgrade guide are examples from the beta and can become stale.

3. **Inventory before changing code**
   - Read [references/migration-checklist.md](references/migration-checklist.md) and run searches appropriate to the repository.
   - Report each hit with its file and migration category. Separate confirmed incompatibilities from possible matches and generated or vendored code.
   - Map credentials and token consumers by purpose and required permissions, but never collect token values.

4. **Plan in dependency order**
   - Update container and scripting libraries before diagnosing missing authentication context in RPC.
   - Then migrate authentication/routes, GraphQL actions and ID semantics, eventing inputs, and component-specific message or payload contracts.
   - Read [references/component-changes.md](references/component-changes.md) only for the component types found in the inventory.
   - For public Mythic services during the beta, use the upstream-requested `Mythic-v4.0.0` compatibility branch unless the maintainer specifies a newer convention.

5. **Implement bounded changes**
   - Make mechanical renames only where the surrounding API contract confirms them.
   - Do not replace every database `id` with a display ID: public task/callback actions use operation-scoped display IDs, while direct table queries and internal messages can still require primary keys.
   - Replace broad token access with the minimum scopes needed by each caller. Treat compatibility shorthands that request `*` as migration debt.
   - Preserve established repository layout, language style, and build conventions. Use `$mythic-implant-development`, `$mythic-profiles`, or `$mythic-translation-containers` when the migration requires detailed component implementation guidance.

6. **Validate behavior**
   - Run existing unit, lint, build, and container tests first, then the relevant checks in [references/upgrade-validation.md](references/upgrade-validation.md).
   - Test against a disposable or development Mythic 4 instance before production.
   - Validate authorization failures as well as successful requests; a working admin token does not prove that least-privilege scopes are correct.
   - Re-run the inventory searches and explain any remaining intentional hits.

## Output requirements

Return a concise migration record containing:

- source and target Mythic versions or branches
- components and external integrations inventoried
- confirmed breaking changes, affected files, and changes made
- dependency versions selected and where they were verified
- validation commands and observed results
- token scopes required by each automation role, without token values
- remaining risks, deferred compatibility shorthands, and rollback readiness

For an audit-only request, do not edit files; provide prioritized findings and an implementation plan instead.

## Primary sources

- [Mythic 3.4 to 4.0 updates](https://docs.mythic-c2.net/version-4.0/updating/mythic-3.4-greater-than-4.0-updates)
- [Mythic 4 public beta](https://specterops.io/blog/2026/08/04/mythic-4-public-beta/)
