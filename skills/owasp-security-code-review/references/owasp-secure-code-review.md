# OWASP Secure Code Review

Use this reference to choose review scope, organize evidence, and keep manual review centered on code paths that automated tools often miss.

## Review Modes

- Use a baseline review for new applications, major releases, legacy onboarding, compliance work, or post-incident review.
- Use a diff-based review for pull requests, commits, feature delivery, and routine security regression checks.
- Escalate from diff-based to baseline review when a change introduces a new trust boundary, new integration, new privilege path, or evidence of systemic control gaps.

## Baseline Sequence

1. Map architecture, components, assets, trust boundaries, and deployment assumptions.
2. Enumerate entry points and verify server-side validation.
3. Verify authentication and authorization at each path.
4. Trace untrusted and sensitive data through processing to sinks.
5. Model critical business workflows and invariants.
6. Review cryptographic implementations and key handling.
7. Check fail-closed error handling and security logging.
8. Inspect configuration, secrets, runtime privileges, and deployment drift.

## Diff-Based Sequence

1. Identify the security controls touched by the change.
2. Identify new or widened attack paths.
3. Verify changed trust-boundary crossings.
4. Review new integrations, parsers, stores, and privileged actions.
5. Check for regressions in existing auth, validation, and logging behavior.
6. Apply the relevant sink-specific references in this directory.

## Evidence Pattern

Trace each suspected issue as:

```text
source -> parsing -> validation -> authorization -> transformation -> sink -> impact
```

Record:

- attacker capability and required state
- exact route, job, function, or parser
- existing controls and bypass conditions
- affected asset or invariant
- test case that proves the issue or proves the control

## Pattern Examples

### Missing alternate-path review

```python
# Primary route enforces ownership.
@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id, user):
    return invoices.get_for_user(invoice_id, user.id)

# Export path skips the same check.
@app.get("/exports/invoices/{invoice_id}")
def export_invoice(invoice_id, user):
    return invoices.get(invoice_id)
```

Review both routes because a single missed authorization check defeats the protected resource.

### Incomplete data-flow tracing

```ts
const filename = req.query.name;
const normalized = sanitize(filename);
audit.log(normalized);
return fs.readFileSync(path.join(REPORT_DIR, normalized));
```

Do not stop at `sanitize()`. Verify whether the sanitizer is correct for a filesystem path sink, whether canonicalization happens before comparison, and whether the resolved path stays under `REPORT_DIR`.

### Business-logic bypass

```ts
if (order.status === "paid") {
  ship(order);
}

// Separate admin helper can call ship() without checking payment state.
```

Trace every path that can reach the state transition, not only the normal workflow.

## Review Prompts

- Which assets would matter most if confidentiality, integrity, or availability failed?
- Which trust boundaries were added or changed?
- Which security controls are centralized, and which alternate paths bypass them?
- Which suspicious patterns are only scanner hints, and which are complete exploit paths?
- Which unresolved assumptions should be recorded as coverage gaps rather than findings?

## Source

Local summary based on the OWASP Secure Code Review Cheat Sheet:
`https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html`
