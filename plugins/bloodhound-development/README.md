# BloodHound Development

Internal workflows for developing and validating BloodHound Enterprise and BloodHound Community Edition changes.

## Skills

- `bhe-dev-bootstrap` — deprecated compatibility entrypoint that routes existing callers to the focused skills below.
- `bhe-dev-environment` — select or create task-owned worktrees and safely bootstrap, isolate, troubleshoot, and release local stacks.
- `bhe-change-delivery` — implement and validate product changes, track BHE/BHCE parity, prepare PR trust packages, and follow changes through CI and review.
- `bhe-enterprise-review` — perform a mutation-free review of an immutable BHE/BHCE candidate and emit a SHA-bound review receipt.
- `bhe-ui-playwright` — validate BHE/BHCE frontend behavior, choose durable Playwright coverage, capture reviewer evidence, and report browser, accessibility, and CI-enforcement results.
- `bhe-sample-data-ingest` — load and verify the official AD and Entra sample datasets in a local development instance.

The analyst-oriented `bloodhound` plugin remains a separate dependency for query, AD/Azure, and OpenGraph domain workflows.

`bhe-change-delivery` is the primary orchestrator. It proactively delegates independent investigation, implementation, environment, browser-validation, and review lanes when useful. Leaf skills retain single-owner boundaries: one environment operator owns stack state and sample ingest, one browser agent owns Playwright evidence, and one fresh reviewer owns the immutable enterprise verdict.
