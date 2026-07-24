---
name: owasp-security-code-review
description: Perform evidence-driven security code reviews across application repositories, services, libraries, and pull requests. Use when Codex needs to audit source code for security flaws, map trust boundaries, verify authentication or authorization, trace untrusted data to sensitive sinks, assess business logic or cryptography, or produce prioritized findings when no narrower language or platform review skill fits.
---

# OWASP Security Code Review

Use this skill to perform a manual security review that starts from architecture and follows concrete execution paths. Prefer a narrower language, framework, CI, cloud, or infrastructure review skill when one clearly fits; use this skill for baseline coverage and cross-cutting review logic.

## Review Principles

- Build a threat model before reporting issues: identify actors, assets, trust boundaries, privilege levels, and attacker-controlled inputs.
- Treat entry points, identity decisions, privilege changes, and sensitive data movement as primary anchors.
- Confirm issues end to end from source through transformations and guards to sink or security decision.
- Separate confirmed vulnerabilities from suspicious patterns and unanswered questions.
- Prefer a small number of well-supported findings over speculative issue lists.
- Keep coverage visible: record reviewed surfaces, skipped areas, and assumptions that affect confidence.
- Always create or update one standalone `poc_<finding_slug>.py` artifact per confirmed finding in the review workspace.

## References

- Use the local reference files below during ordinary reviews. Retrieve upstream OWASP pages only when the user asks for source verification or updated guidance.
- Read [references/common-vulnerability-patterns.md](references/common-vulnerability-patterns.md) when reviewing input handling, injection, authentication, authorization, deserialization, XML, or cryptographic implementation patterns.
- Read [references/attack-trees.md](references/attack-trees.md) when mapping multi-step attack paths, reviewing critical business workflows, or turning a threat model into concrete code paths.
- Read [references/owasp-secure-code-review.md](references/owasp-secure-code-review.md) for the OWASP review workflow, source-to-sink tracing, and baseline versus diff-based review prompts.
- Read [references/owasp-input-validation.md](references/owasp-input-validation.md), [references/owasp-sql-injection.md](references/owasp-sql-injection.md), [references/owasp-xss.md](references/owasp-xss.md), [references/owasp-file-upload.md](references/owasp-file-upload.md), [references/owasp-os-command-injection.md](references/owasp-os-command-injection.md), and [references/owasp-nosql-security.md](references/owasp-nosql-security.md) for input and injection-specific patterns.
- Read [references/owasp-authentication.md](references/owasp-authentication.md), [references/owasp-session-management.md](references/owasp-session-management.md), and [references/owasp-authorization.md](references/owasp-authorization.md) for identity and access-control patterns.
- Read [references/owasp-deserialization.md](references/owasp-deserialization.md), [references/owasp-xxe.md](references/owasp-xxe.md), and [references/owasp-cryptographic-storage.md](references/owasp-cryptographic-storage.md) for serialization, XML parser, and cryptographic storage patterns.

## Review Process

1. Review architecture for security anti-patterns.
   - Inventory components, languages, frameworks, storage, external integrations, privileged jobs, and deployment boundaries.
   - Identify trust assumptions such as internal-network trust, shared admin paths, tenant co-mingling, unsafe plugin or deserialization surfaces, dynamic code execution, and secret-bearing services.
   - Note where security controls are centralized and where alternate paths may bypass them.

2. Analyze entry points and input validation.
   - Enumerate HTTP/RPC routes, GraphQL resolvers, message consumers, webhooks, CLI commands, scheduled jobs, file imports, deserializers, and configuration inputs.
   - Trace parsing, normalization, canonicalization, schema checks, type checks, size limits, allowlists, and rejection behavior.
   - Look for alternate encodings, duplicate parameters, path confusion, object binding issues, and validation performed after a dangerous sink.

3. Verify authentication and authorization.
   - Map how identities are established, refreshed, propagated, and revoked across user, service, and background-job flows.
   - Check session, token, API key, mTLS, and service-account validation assumptions.
   - Verify every read, write, export, and state transition enforces the required role, tenant, ownership, and object-level checks, including alternate routes and asynchronous handlers.
   - Test fail-open behavior when middleware, policy engines, or upstream identity data is absent or malformed.

4. Trace data flows.
   - Follow untrusted data to SQL/NoSQL queries, templates, filesystem paths, archives, redirects, outbound requests, command execution, logs, serialization, caches, and client responses.
   - Follow sensitive data such as credentials, tokens, personal data, and keys through storage, telemetry, errors, exports, and third-party boundaries.
   - Record sanitizers, encoders, escaping, parameterization, and privilege boundaries on each path; verify that each control is appropriate for the sink.

5. Analyze business logic.
   - Model critical workflows as states and invariants: approvals, payments, invitations, password resets, account recovery, quotas, entitlements, tenant isolation, and admin actions.
   - Check replay, race, ordering, stale-state, double-spend, partial-failure, and TOCTOU behavior.
   - Look for ways to skip steps, reuse artifacts, change identifiers, or invoke a privileged transition through an unexpected channel.

6. Review cryptographic implementation.
   - Identify password hashing, encryption, signatures, MACs, randomness, key derivation, key storage, certificate validation, and token construction.
   - Verify modern primitives, secure parameters, nonce/IV uniqueness, constant-time comparisons where relevant, key separation, rotation, and failure behavior.
   - Treat custom crypto, hardcoded keys, weak randomness, disabled TLS verification, and unsigned or partially verified tokens as priority review areas.

7. Verify error handling.
   - Check whether errors fail closed at authentication, authorization, validation, and transaction boundaries.
   - Review exception swallowing, fallback behavior, retries, partial commits, default values, verbose responses, stack traces, and secret-bearing logs.
   - Confirm that security-relevant failures are observable without leaking sensitive details.

8. Review configuration and deployment.
   - Inspect defaults and environment parsing for debug modes, CORS, trusted proxies, host validation, cookie flags, security headers, logging, feature flags, and secret loading.
   - Review container/runtime privileges, filesystem permissions, network exposure, cloud/IAM bindings, CI/CD secrets, build-time substitutions, and production-vs-development drift when those artifacts are in scope.
   - Identify insecure defaults that make a secure deployment depend on undocumented operator behavior.

9. Build the PoC artifacts.
   - Create or update one standalone `poc_<finding_slug>.py` file for each confirmed finding.
   - Keep each PoC incremental: print or implement numbered steps for prerequisites, authentication or material acquisition, trigger, impact verification, and cleanup guidance.
   - State attacker position, required permissions, credentials or certificates, environmental dependencies, and any unproven prerequisite before sending requests.
   - Default to dry-run or harmless markers and require an explicit flag for state-changing validation.
   - If a finding has no safe runnable path, still create its per-finding PoC scaffold and explain the missing prerequisite or unsafe step.
   - Validate each script with syntax checks and dry runs, then record which live steps were and were not executed.

## Finding Standard

Report a finding only when the review can state:

- the affected code path with file and line references
- the attacker-controlled input or violated trust assumption
- the missing, bypassed, or incorrect control
- the reachable impact and required prerequisites
- a concrete remediation direction
- a focused regression test or validation step

If a concern lacks a complete path or depends on missing runtime context, label it as an open question or coverage gap instead of a confirmed vulnerability.

## Output

Lead with findings ordered by severity. For each finding, include `Severity`, `Location`, `Issue`, `Exploit Path`, `Impact`, `Remediation`, `Test`, and `PoC Requirements`.

For each confirmed finding, reference the corresponding `poc_<finding_slug>.py` artifact in the report and include the minimum attacker position, required permissions or credentials, environmental conditions, safe default behavior, and example invocation.

After findings, include `Open Questions / Assumptions` and `Coverage`. If no confirmed findings exist, say so explicitly and still state the reviewed surfaces, unresolved risks, and test gaps.
