# BloodHound Development

Internal workflows for developing and validating BloodHound Enterprise and BloodHound Community Edition changes.

## Skills

- `bhe-dev-bootstrap` — deprecated compatibility entrypoint that routes existing callers to the focused skills below.
- `bhe-dev-environment` — select or create task-owned worktrees and safely bootstrap, isolate, troubleshoot, and release local stacks.
- `bhe-change-delivery` — implement and validate product changes, track BHE/BHCE parity, prepare PR trust packages, and follow changes through CI and review.
- `bhe-enterprise-review` — perform a mutation-free review of an immutable BHE/BHCE candidate and emit a SHA-bound review receipt.
- `bhe-ui-playwright` — validate BHE frontend behavior, browser errors, failed requests, accessibility, and optional Lighthouse diagnostics.
- `bhe-sample-data-ingest` — load and verify the official AD and Entra sample datasets in a local development instance.

The analyst-oriented `bloodhound` plugin remains a separate dependency for query, AD/Azure, and OpenGraph domain workflows.
