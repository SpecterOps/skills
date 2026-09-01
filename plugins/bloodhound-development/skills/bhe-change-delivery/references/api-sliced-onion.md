# API Sliced Onion Architecture

Use this checklist only for API handlers, services, persistence, module registration, or their tests. First locate and read the applicable target revision's accepted API Layered Architecture ADR under `docs/adrs/`; the repository ADR is authoritative, and this reference is only an operating checklist. Do not rely on a copied ADR from another worktree or branch.

Useful discovery terms include `API Sliced Onion Architecture`, `API_Layered_Architecture`, `server/modules`, and the reference feature slice named by the ADR.

## Inspect

- Identify the feature slice, endpoint or operation, and current runtime call path.
- Identify handler, service, AppDB, PostgreSQL, and root-registration responsibilities that participate in the behavior.
- Trace imports and consumer-owned interfaces in both directions.
- Read the corresponding tests and the ADR's reference slice before deciding where new behavior belongs.
- Determine whether each touched path is migrated, legacy, or intentionally transitional; do not assume directory names alone prove conformance.

## Plan

- Keep HTTP handling and wire transformations in handlers.
- Keep business rules, domain types, and domain errors in services.
- Keep SQL generation, persistence adaptation, and row-to-domain mapping in AppDB.
- Keep PostgreSQL inaccessible above AppDB.
- Define each dependency interface at its consuming layer and keep dependency direction inward.
- Plan explicit root registration and BHE/BHCE compatibility.
- Identify focused unit evidence for every changed layer and integration or end-to-end evidence for the resulting behavior, as required by the target ADR and repository conventions.
- Make any intentional deviation or transitional duplication explicit, bounded, and connected to a current migration need.

## Verify

- Confirm services import neither handlers nor AppDB.
- Confirm transport and persistence concerns do not leak into the service core.
- Confirm outer-layer dependencies point inward and interfaces remain consumer-owned.
- Confirm PostgreSQL is referenced only beneath AppDB where required by the ADR.
- Confirm root registration and dependency wiring are explicit.
- Run focused tests for every changed layer and the required integration path.
- Inspect for duplicate models, parallel sources of truth, or temporary compatibility logic introduced by the migration.
- Record any unverified architecture boundary or unresolved migration decision; do not infer conformance from passing tests alone.
