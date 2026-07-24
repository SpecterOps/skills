---
name: openssf-python-review
description: Perform adversarial Python security code reviews grounded in the OpenSSF Secure Coding Guide for Python. Use when Codex needs to audit large Python repositories, recovered or decompiled Python source, Python services or scripts with unclear trust boundaries, or code paths involving Python-specific injection, deserialization, archive extraction, import-path, encoding, numeric, concurrency, logging, exception, resource-management, secret-handling, or randomness risks.
---

# OpenSSF Python Review

Use this skill for manual Python review when the result needs OpenSSF Python rule coverage plus the evidence standard of the local OWASP and CWE review skills. Prefer a narrower framework or platform skill when one clearly fits; use this skill to drive Python-specific adversarial review and to make recovered-source uncertainty explicit.

## Review Principles

- Start from architecture, trust boundaries, attacker-controlled inputs, sensitive assets, privilege levels, and Python runtime assumptions.
- Treat OpenSSF rules as coverage prompts and root-cause clues, not as proof. Confirm a reachable path before reporting a finding.
- Prioritize paths that cross trust zones or reach code execution, deserialization, query execution, archive extraction, filesystem, import resolution, secrets, authorization, logs, error output, randomness, and shared state.
- Assume attackers will exploit alternate encodings, malformed archives, crafted object state, client-controlled identity fields, poisoned environment variables, thread timing, exceptional control flow, and recovered-source gaps.
- Distinguish confirmed vulnerabilities from suspicious patterns, hardening opportunities, and unanswered questions.
- For recovered source, separate what is visible in code from what may be missing because of decompilation, packaging, generated wrappers, native extensions, or absent deployment configuration.
- Use the guide's linked CWE as an initial mapping candidate. Validate the primary CWE with the local `cwe-code-review` skill when precise mapping matters or when the guide's CWE is broader than the proven root cause.
- Always create or update one standalone `poc_<finding_slug>.py` artifact per confirmed finding in the review workspace.

## References

- Read [references/openssf-python-rule-index.md](references/openssf-python-rule-index.md) first for source scope, rule coverage, CWE candidates, and the rule-to-review map.
- Read [references/large-python-project-triage.md](references/large-python-project-triage.md) when scoping a repository-scale baseline or diff-based review and maintaining a coverage ledger.
- Read [references/python-trust-boundary-surfaces.md](references/python-trust-boundary-surfaces.md) when tracing untrusted input to authorization, encoding, injection, filesystem, archive, deserialization, import-path, logging, error, secret, or randomness sinks.
- Read [references/python-state-and-availability-surfaces.md](references/python-state-and-availability-surfaces.md) when reviewing numeric correctness, exception behavior, thread pools, races, deadlocks, cleanup, assertions, return values, and other integrity or availability paths.
- Read [references/recovered-python-source-review.md](references/recovered-python-source-review.md) when source was recovered from bytecode, wheels, frozen binaries, containers, partial exports, or decompilers, or when project structure and runtime assumptions are incomplete.

## Review Process

1. Build a Python-aware inventory.
   - Identify packages, entry points, frameworks, CLI commands, workers, schedulers, message consumers, plugins, imports, native bindings, templates, configuration loaders, secrets providers, storage, and deployment/runtime boundaries.
   - Identify Python version assumptions, dependency manifests, generated code, vendored packages, bytecode-only areas, and native or C-extension handoffs.
   - Record which components run under distinct OS identities or trust zones and which share one interpreter, filesystem, environment, cache, or database role.

2. Model attacker positions and trust boundaries.
   - Enumerate HTTP/RPC parameters, headers, cookies, uploaded files, archives, queues, task payloads, database records, environment variables, config files, command-line arguments, import paths, plugin names, serialized blobs, and operator-controlled inputs.
   - Mark security decisions that depend on client-supplied identity, role, tenant, path, locale, encoding, type, numeric value, or exception behavior.
   - For recovered source, note missing call sites, unresolved imports, placeholder names, dead code uncertainty, and configuration that must be verified outside the recovered tree.

3. Triage high-risk Python surfaces first.
   - Trace untrusted data to `subprocess`, `os.system`, SQL execution, `pickle`, `marshal`, YAML/object loaders, archive extractors, path resolution, dynamic import, `eval`/`exec`, logging, error rendering, secret loading, and token generation.
   - Check canonicalization before validation, allowlists over denylists, consistent encodings, server-side access decisions, and import/search-path integrity.
   - Review packaging and deployment artifacts for embedded secrets, debug tools, monkey patches, permissive environment inheritance, and shared-process trust-zone collapse.

4. Review integrity and availability paths.
   - Inspect numeric conversions, `Decimal` construction, float comparisons, special float values, fixed-width or C-backed numbers, bitwise arithmetic, and loop counters when they influence money, quotas, sizes, timeouts, authorization, or resource limits.
   - Inspect exception handling, `finally` blocks, return-value handling, assertions, cleanup, locks, thread pools, shared mutable state, thread-local reuse, and silent worker failures.
   - Treat business-state corruption, fail-open behavior, denial of service, and audit blind spots as security issues when an attacker can influence the path.

5. Validate each candidate end to end.
   - Trace `source -> parsing -> normalization -> validation -> authorization -> transformation -> sink -> impact`.
   - Identify the attacker capability, required state, bypassed or missing control, Python behavior that makes the path exploitable, and concrete impact.
   - Read the relevant reference section and rule entry before naming an OpenSSF rule or CWE.
   - Keep scanner hits, dangerous APIs, and decompiler oddities as leads until the full path is proven.

6. Build PoC artifacts.
   - Create or update one standalone `poc_<finding_slug>.py` file for each confirmed finding.
   - Make each PoC incremental: print or implement numbered steps for prerequisites, material acquisition, trigger, impact verification, and cleanup guidance.
   - State attacker position, required permissions, credentials or certificates, environmental dependencies, Python/runtime assumptions, and any unproven prerequisite before sending requests or touching state.
   - Default to dry-run or harmless markers and require an explicit flag for state-changing validation.
   - If a finding has no safe runnable path, still create its per-finding PoC scaffold and explain the missing prerequisite or unsafe step.
   - Validate each script with syntax checks and dry runs, then record which live steps were and were not executed.

## Finding Standard

Lead with findings ordered by severity. For each finding include `Severity`, `Location`, `Issue`, `OpenSSF Rule`, `CWE`, `Evidence`, `Exploit Path`, `Impact`, `Remediation`, `Test`, and `PoC Requirements`.

For `OpenSSF Rule`, include the `pyscg-XXXX` identifier, rule name, and one sentence explaining why the code path violates that rule. If multiple rules contribute, name one primary rule and mention secondary rules only when they explain a distinct contributing failure.

For `CWE`, include the identifier, name, and one sentence explaining why that entry is the precise root-cause mapping. If the guide's CWE is only a candidate or a broad mapping, say so and validate with the local CWE corpus before presenting it as primary.

For `Evidence`, include line-scoped fenced code blocks with an appropriate language tag such as `python`, `toml`, `yaml`, `json`, `bash`, `sql`, or `dockerfile`. Put the source path and line range immediately above each block. Keep excerpts narrow enough to show the input, missing control, Python behavior, and sink without dumping whole modules.

For each finding, reference the corresponding `poc_<finding_slug>.py` artifact and include the minimum attacker position, required permissions or credentials, environmental conditions, safe default behavior, and example invocation.

After findings, include `Open Questions / Assumptions` and `Coverage`. In `Coverage`, list reviewed Python packages, entry points, trust boundaries, OpenSSF rule groups applied, recovered-source gaps, and tests or live validation not performed. If no confirmed findings exist, say so explicitly and still state unresolved risks, review gaps, and that no per-finding PoC artifacts were created.
