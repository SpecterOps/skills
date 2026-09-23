# BHE Enterprise Code Review

Run this gate after implementation and focused validation stabilize, before preparing the PR proposal. The goal is production-quality code that solves the current problem without creating avoidable maintenance cost. Apply the checks proportionally: do not demand speculative abstractions or unrelated cleanup.

## Establish Review Scope

Inspect repository instructions, the complete intended PR diff, changed tests, and enough surrounding code to understand established patterns and downstream consumers:

```bash
git status --short --branch
git diff --stat
git diff
git diff --check
```

Include staged changes and relevant BHCE or submodule diffs when applicable. Separate pre-existing problems from regressions introduced by the change. Review generated files through their source definition and regeneration path.

## Review the Design

- Confirm the implementation directly serves the agreed behavior and acceptance criteria.
- Prefer existing domain concepts, utilities, components, and extension points when they are a clean fit.
- Reject duplicate sources of truth, parallel abstractions, unnecessary layers, premature generalization, and configuration added only for hypothetical use.
- Keep responsibilities cohesive and dependencies directional. Avoid leaking UI, persistence, transport, renderer, or Enterprise-specific concerns across established boundaries.
- Justify each new dependency, public API, feature flag, compatibility shim, migration path, and persistent data field by a current requirement.
- Remove dead code, stale fallbacks, temporary debugging, misleading comments, and TODOs without an owner or concrete follow-up.
- Keep the change narrow. Record worthwhile unrelated cleanup separately rather than expanding the PR.

## Review Production Risk

### Correctness and contracts

- Trace success, empty, malformed, partial, failure, cancellation, and retry paths.
- Check invariants, error propagation, nil or undefined handling, ordering, concurrency, idempotency, and lifecycle cleanup.
- Preserve API, schema, generated-client, routing, authentication, authorization, and BHE/BHCE contracts unless the change intentionally revises them.
- Ensure failures are explicit and actionable rather than silently ignored or converted into misleading success.

### Security and privacy

- Validate untrusted input at the correct boundary and encode output for its destination.
- Enforce authorization server-side and avoid trusting client-visible state for security decisions.
- Avoid exposing secrets, credentials, tokens, sensitive identifiers, or customer data in source, URLs, logs, errors, fixtures, analytics, or screenshots.
- Inspect query construction, file or path handling, deserialization, redirects, outbound requests, and dependency changes for abuse paths.
- Prefer secure defaults and least privilege. Treat a security uncertainty as blocking until resolved or escalated.

### Reliability, performance, and operability

- Avoid unbounded work, accidental N+1 operations, unnecessary network calls, excessive rendering, leaked goroutines or listeners, and avoidable large allocations.
- Check timeout, retry, backoff, cancellation, transaction, and rollback behavior where applicable.
- Preserve useful logs, metrics, and error context without adding noise or sensitive data.
- For migrations, flags, or rollout-sensitive changes, define compatibility, rollback, and cleanup behavior.
- Ensure degraded dependencies and partial data fail predictably.

## Review Maintainability

- Use names and control flow that make intent obvious without requiring explanatory comments.
- Keep functions, components, and modules small enough to reason about, but do not fragment cohesive logic.
- Make invalid states difficult to represent when the repository's language and patterns support it.
- Add comments for non-obvious rationale, constraints, or tradeoffs; do not narrate syntax.
- Ensure tests protect behavior and important failure modes, not implementation trivia. Avoid broad snapshots when focused assertions provide clearer protection.
- Verify documentation, examples, generated artifacts, and cleanup instructions when the change alters developer or operator behavior.

## Determine the Disposition

Classify findings by impact:

- `blocking`: correctness, security, data loss, broken compatibility, serious reliability, or architecture debt likely to impose near-term rework.
- `important`: material complexity, duplication, weak tests, operability gaps, or maintainability cost that should be fixed before PR.
- `minor`: safe improvement that may be fixed now or recorded as a deliberate tradeoff.
- `follow-up`: valuable work outside the agreed scope, with a concrete owner or tracking path when required.

Fix all blocking and important findings before PR preparation. Do not dismiss a finding only because tests pass. Conversely, do not block the PR on taste, speculative reuse, or unrelated cleanup.

After fixes, rerun affected validation and re-review the resulting diff. Repeat until no blocking or important finding remains.

## Record Review Evidence

At the pre-PR handoff, report:

- review scope and relevant surrounding systems inspected;
- findings by disposition;
- changes made in response;
- tests or checks rerun after review;
- accepted tradeoffs and why they are preferable to added complexity;
- remaining risks, unverified areas, and concrete follow-ups.

If the review discovers an unresolved product, architecture, security, or compatibility decision, stop before PR preparation and obtain the appropriate direction.
