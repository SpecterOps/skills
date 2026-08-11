# BHE/BHCE Parity and Compatibility

Use this reference for every meaningful BHE change. Seek reasonable behavioral parity without requiring identical features, controls, dependencies, or implementations. BHE and BHCE may use different product-specific capabilities; treat a documented, intentional difference as a valid outcome.

## Dispositions

- `matched`: Implement the corresponding behavior in BHCE.
- `equivalent`: Preserve the same user outcome through a different BHCE implementation.
- `bhe-only`: Keep the change Enterprise-only because no BHCE counterpart is appropriate.
- `intentionally-divergent`: Consider a BHCE counterpart and deliberately avoid it because capability, product, complexity, or maintenance costs outweigh the benefit.
- `deferred`: Identify a reasonable BHCE counterpart but postpone it with a concrete follow-up.
- `investigate`: Leave compatibility or parity implications unresolved during local iteration. Resolve this before PR readiness.

## Testing Matrix

### BHE-only source

Run targeted BHE tests. Inspect the BHCE surface and record either its counterpart or why BHCE testing is not required. A change outside `bhce/` normally cannot change BHCE source directly, but it can create undocumented product drift.

### Source inside `bhce/`

Run targeted BHCE unit or browser tests plus applicable type-checking and linting. Run the BHE tests that consume the changed BHCE code. Treat the BHCE commit and the BHE submodule-pointer update as separate reviewable steps.

### Shared boundaries

Test and type-check both products when changing shared packages, component interfaces, API contracts, schemas, generated clients, authentication behavior, routing contracts, or other dependencies consumed by both products.

### Product-specific UI behavior

Validate the changed behavior in the product that owns it. Inspect the other product for a reasonable behavioral counterpart. Do not reproduce a product-specific built-in capability with disproportionate custom code merely for nominal parity. Record capability differences and preserve existing behavior with a regression test when that test provides meaningful protection.

### Equivalent outcomes

Test the user-visible result in both products. Do not require identical DOM structure, controls, graph APIs, or implementation details when the engines differ.

## Recording Workflow

Initialize the task once:

```bash
PARITY_LOG="<bhe-dev-bootstrap skill directory>/scripts/bhe-parity-log.sh"

"$PARITY_LOG" init --task <task-slug> --repo <absolute-worktree-path>
```

Record or revise a change. Reuse the same `--change-id` to append a newer decision for that change:

```bash
"$PARITY_LOG" record \
  --task <task-slug> \
  --change-id <stable-change-slug> \
  --change "<BHE change summary>" \
  --surface <bhe-ui|bhce-ui|shared-ui|api|backend|other> \
  --disposition <matched|equivalent|bhe-only|intentionally-divergent|deferred|investigate> \
  --reason "<decision rationale>" \
  --bhe-validation "<test evidence or pending>" \
  --bhce-validation "<test evidence, pending, or why not required>" \
  --follow-up "<follow-up, none, or pending>" \
  --bhe-ref "<commit or PR, or pending>" \
  --bhce-ref "<commit or PR, or none>"
```

Use `show` at handoffs. During implementation, run:

```bash
"$PARITY_LOG" check --task <task-slug> --stage iteration
```

Before PR preparation, run:

```bash
"$PARITY_LOG" check --task <task-slug> --stage pr
```

Both stages evaluate only the latest revision of each change ID and verify that the recorded worktree and branch still match. The iteration stage checks that records exist and parse correctly. The PR stage additionally rejects unresolved investigations, pending validation, a missing BHE commit/PR reference, a missing BHCE reference for `matched` or `equivalent`, or deferred entries without a concrete follow-up.

After the work is complete and the worktree is no longer needed, archive rather than delete the ledger:

```bash
"$PARITY_LOG" archive --task <task-slug>
```

## Review Questions

Before choosing a disposition, answer:

1. Does BHCE expose the same user workflow or contract?
2. Does this change touch `bhce/` or a boundary consumed by both products?
3. Can the other product provide the same outcome with reasonable implementation and maintenance effort?
4. Would omitting BHCE work break existing behavior, or only leave a documented feature difference?
5. Which focused BHE and BHCE tests provide useful evidence?
