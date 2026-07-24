# OpenSSF Python Rule Index

Use this reference first to scope coverage and choose the rule pages relevant to a suspected Python weakness.

## Contents

- Source scope
- How to use the index
- High-priority rule groups
- Rule map
- Coverage notes

## Source Scope

- Source: OpenSSF Secure Coding One Stop Shop for Python.
- Snapshot basis: upstream `main` tree inspected on 2026-07-23 at Git tree `79c851adf711e4b8878b35b37397f828c25a9c0b`.
- Guide scope: CPython 3.9 and later, with standard-library-focused examples and rule pages named `pyscg-XXXX`.
- Rule count in this snapshot: 48 rules across Introduction, Encoding and Strings, Numbers, Neutralization, Exception Handling, Logging, Concurrency, Coding Standards, and Cryptography.
- The guide maps each rule to one or more CWE entries. Treat those as mapping candidates until the reviewed code path proves the root cause.
- The guide examples are intentionally narrow teaching examples. Do not copy a compliant sample into production or assume it addresses adjacent risks outside the named rule.

## How To Use The Index

- Start with architecture and attacker-controlled inputs, then use the table to widen coverage.
- Prioritize rules that reach a trust boundary, code execution, data disclosure, authorization decision, secret, log, error output, or availability limit.
- Read the topic reference for the relevant rule group before reporting.
- Use the `cwe-code-review` skill when a finding needs a more precise CWE than the guide's candidate.
- Keep rules that are not reachable from attacker influence as hardening notes or coverage items, not confirmed findings.

## High-Priority Rule Groups

| Group | Rules | Why prioritize |
| --- | --- | --- |
| Trust and identity | `pyscg-0040`, `pyscg-0041`, `pyscg-0055` | Shared runtimes, embedded secrets, or client-controlled roles can collapse the security model. |
| Input normalization and neutralization | `pyscg-0043`, `pyscg-0044`, `pyscg-0045`, `pyscg-0047`, `pyscg-0008`, `pyscg-0009`, `pyscg-0010` | Alternate encodings and unsafe sinks commonly turn user input into code, queries, or policy bypasses. |
| Files, imports, and object loading | `pyscg-0012`, `pyscg-0013`, `pyscg-0023`, `pyscg-0011` | Archives, search paths, deserialization, and external binary data can cross into execution or arbitrary file effects. |
| Observability and leakage | `pyscg-0019`, `pyscg-0020`, `pyscg-0021`, `pyscg-0022`, `pyscg-0050` | Logs and debug tooling can leak secrets, hide attacks, or expose new privileged functionality. |
| Integrity and availability | `pyscg-0001` to `pyscg-0007`, `pyscg-0014` to `pyscg-0018`, `pyscg-0024` to `pyscg-0037`, `pyscg-0051`, `pyscg-0052` | Numeric, exception, resource, and concurrency failures become security issues when attackers can drive state or load. |
| Randomness | `pyscg-0038` | Predictable tokens, IDs, or secrets undermine authentication and confidentiality. |

## Rule Map

### 01 Introduction

| Rule | CWE candidate | Review focus | Common leads |
| --- | --- | --- | --- |
| `pyscg-0040` Use Process Isolation for Trust Zones | CWE-501 | Separate less-trusted code or data processing from sensitive runtime privileges. | Shared interpreter/UID for web, worker, parser, admin, or tenant workloads; no OS isolation around risky parsing. |
| `pyscg-0041` Externalize Configuration and Secrets | CWE-798 | Keep credentials, keys, and deployment-specific trust material out of code and replaceable at runtime. | Hardcoded passwords, API keys, certs, tokens, backend IPs, service accounts, `.pyc`-recoverable constants. |
| `pyscg-0042` Ensure Correct Operator Precedence | CWE-783 | Verify expressions that combine assignment, comparison, or mutation do not produce unintended security state. | Dense boolean expressions, chained reads/writes, policy checks mixed with side effects, arithmetic used in bounds checks. |
| `pyscg-0055` Determine Access on Server Side | CWE-472 | Derive identity and permissions from trusted server-side state, not client-supplied fields. | `role`, `user`, `tenant`, `is_admin`, or action scope accepted from form/JSON/query data without verified session binding. |

### 02 Encoding and Strings

| Rule | CWE candidate | Review focus | Common leads |
| --- | --- | --- | --- |
| `pyscg-0043` Specify Locale Explicitly | CWE-175 | Prevent locale-dependent parsing, formatting, or comparisons from changing security behavior. | Locale-sensitive dates, numbers, case handling, implicit process locale, user-controlled locale selection. |
| `pyscg-0044` Canonicalize Input Before Validating | CWE-180 | Normalize equivalent representations before validation or policy checks. | Path validation before `.resolve()`, Unicode confusables, mixed normalization forms, encoded traversal, case-folding mismatch. |
| `pyscg-0045` Enforce Consistent Encoding | CWE-176 | Keep text encoding stable across trust boundaries and sanitization steps. | Implicit `.encode()`/`.decode()`, fallback codecs, lossy ASCII conversion, different producer/consumer encodings, forensic parsers. |

### 03 Numbers

| Rule | CWE candidate | Review focus | Common leads |
| --- | --- | --- | --- |
| `pyscg-0001` Control Numeric Precision | CWE-1339 | Avoid floating-point drift in security-relevant amounts, quotas, or comparisons. | Money, billing, limits, percentages, resource accounting, token expiry math using `float`. |
| `pyscg-0002` Guard Fixed-Width Numbers Against Overflow | CWE-191, CWE-190 | Check C-backed or fixed-width numeric boundaries explicitly. | `numpy`, `ctypes`, `struct`, `datetime.timedelta`, native bindings, size or timestamp conversions. |
| `pyscg-0003` Use Arithmetic Over Bitwise Operations | CWE-1335 | Keep arithmetic semantics clear where bounds or permissions depend on numeric state. | Shifts used as multiply/divide, mixed bitwise and arithmetic operations, signed values, packed flags. |
| `pyscg-0004` Use Integer Loop Counters | CWE-197 | Avoid float counters that skip, repeat, or never terminate. | Float increments in retry, pagination, timeout, rate, or resource loops. |
| `pyscg-0005` Specify Rounding for Numeric Conversions | CWE-197 | Make truncation and rounding decisions explicit. | `int(float_value)`, quota or price conversion, timestamps, percentage thresholds, size calculations. |
| `pyscg-0006` Use an Appropriate Comparator for Numbers | CWE-681 | Compare numeric values as numbers with appropriate tolerance or decimal semantics. | String comparison of amounts or versions, direct float equality, `Decimal` mixed with floats. |
| `pyscg-0007` Use String Literals for Decimal Construction | CWE-681 | Construct decimals from exact text, not binary float approximations. | `Decimal(0.1)`, monetary constants, tax or fee tables, threshold constants. |

### 04 Neutralization

| Rule | CWE candidate | Review focus | Common leads |
| --- | --- | --- | --- |
| `pyscg-0047` Use Allow Lists Over Deny Lists | CWE-184 | Prefer accepted forms over trying to enumerate malicious forms. | Character stripping, regex denylists, extension denylists, filter lists for HTML, paths, commands, or identifiers. |
| `pyscg-0008` Prevent Format String Injection | CWE-134 | Keep the format template static when attacker data is formatted. | User-controlled `.format()` or `format_map()` templates, translation strings, templated errors, access to `__globals__`. |
| `pyscg-0009` Prevent OS Command Injection | CWE-78 | Avoid mixing lesser-trusted data into command lines; prefer Python APIs. | `subprocess`, `os.system`, `shell=True`, string-built argv, `shlex.split`, user-selected executable/flags, hostile filenames. |
| `pyscg-0010` Prevent SQL Injection | CWE-89 | Keep SQL code separate from data and avoid script execution paths. | f-strings, `%`, `.format()`, concatenation, `executescript()`, raw ORM fragments, dynamic identifiers. |
| `pyscg-0011` Prevent Type Confusion | CWE-843 | Preserve signedness, width, and expected type when consuming external binary or native data. | `struct.unpack`, `ctypes`, foreign-function data, protocol fields, signed/unsigned conversions. |
| `pyscg-0012` Extract Archives Safely | CWE-409 | Stop traversal, bombs, hostile links, and unbounded extraction effects. | `extractall()`, `extract()`, `tarfile`, `zipfile`, `shutil.unpack_archive`, member paths, count/size limits, symlinks. |
| `pyscg-0013` Secure Search Paths | CWE-426 | Keep module and executable resolution out of attacker-controlled directories and environment. | `sys.path`, `PYTHONPATH`, cwd imports, `sitecustomize`, plugin loading, environment inheritance, writable import dirs. |
| `pyscg-0023` Secure Deserialization | CWE-502 | Avoid object deserialization across trust boundaries or verify integrity before use. | `pickle.loads`, `pickle.load`, `shelve`, serialized cache/queue data, unsigned blobs, gadget-capable object loaders. |

### 05 Exception Handling

| Rule | CWE candidate | Review focus | Common leads |
| --- | --- | --- | --- |
| `pyscg-0014` Use Specific Exception Types | CWE-397 | Make exceptional security states distinguishable and recover only where intended. | Raising `Exception`/`BaseException`, broad handlers around auth, file, or policy code. |
| `pyscg-0015` Handle Error Conditions | CWE-755 | Fail deliberately and visibly instead of continuing after failed security-relevant operations. | Ignored filesystem or network errors, empty `except`, fallback defaults, partial state changes. |
| `pyscg-0016` Propagate Exceptions and Preserve Context | CWE-396 | Preserve failure cause and let the correct layer decide recovery. | `except: pass`, blanket wrapping, discarded `__cause__`, generic retries, fail-open error translation. |
| `pyscg-0018` Validate Numeric Data Beyond Type Checking | CWE-754 | Reject exceptional numeric values such as NaN and infinities when they break invariants. | `float()` on user input, `nan`, `inf`, direct NaN comparison, limits checked only by type. |
| `pyscg-0028` Preserve Exceptions in Finally Blocks | CWE-584 | Avoid `return`, `break`, or `continue` suppressing pending exceptions. | Control flow inside `finally`, hidden validation failures, transaction cleanup that masks errors. |
| `pyscg-0052` Ensure Cleanup on Exceptions | CWE-460 | Restore locks, state, and resources on all exceptional paths. | Manual acquire/release, partially updated state, cleanup skipped after parser or worker failure. |

### 06 Logging

| Rule | CWE candidate | Review focus | Common leads |
| --- | --- | --- | --- |
| `pyscg-0019` Exclude Sensitive Data From Logs | CWE-532 | Keep secrets and personal data out of logs and debug output. | Passwords, tokens, cookies, keys, full request bodies, PII, `print()` debugging, verbose exception data. |
| `pyscg-0020` Implement Informative Event Logging | CWE-778 | Record security-relevant events with enough context for detection and response. | Missing auth failure, authorization denial, admin action, data access, parser rejection, or secret-use audit events. |
| `pyscg-0021` Exclude Developer Tools From the Final Product | CWE-489 | Keep test, debug, monkey-patch, and troubleshooting surfaces out of production packages. | Debug routes, admin helpers, monkey patches, test credentials, profiling hooks, development-only flags. |
| `pyscg-0022` Neutralize Untrusted Data in Logs | CWE-117 | Prevent CRLF and structured-log manipulation. | Raw request values in logs, newline injection, unescaped JSON/log fields, log viewer XSS. |
| `pyscg-0050` Sanitize Error Output to Prevent Information Disclosure | CWE-209 | Separate operator diagnostics from user-visible error output. | Stack traces, paths, SQL errors, secrets in exception text, raw downstream errors, verbose debug responses. |

### 07 Concurrency

| Rule | CWE candidate | Review focus | Common leads |
| --- | --- | --- | --- |
| `pyscg-0024` Ensure Thread Pool Tasks Can Be Interrupted | CWE-400 | Ensure long-running tasks can stop during shutdown or overload. | Blocking tasks, no cancellation signal, stuck worker shutdown, unbounded external calls. |
| `pyscg-0025` Configure Adequate Resource Pools | CWE-410 | Bound worker count and queue growth under attacker-driven load. | Thread-per-request/message, oversized pools, no queue limit, no timeout or grace period. |
| `pyscg-0026` Prevent Deadlocks | CWE-833 | Avoid worker tasks waiting on work scheduled into the same exhausted pool. | Nested `future.result()`, lock ordering, thread-starvation patterns, interdependent subtasks. |
| `pyscg-0027` Prevent Race Conditions | CWE-362 | Synchronize shared state and security decisions. | Shared dict/list/set mutation, check-then-act, chained operations, TOCTOU, missing locks. |
| `pyscg-0029` Reinitialize Reused Thread Objects | CWE-665 | Clear thread-local or reusable worker state between tasks. | `threading.local()`, per-request auth context, tenant data, pooled workers, stale principal leakage. |
| `pyscg-0030` Ensure Thread Pool Tasks Do Not Fail Silently | CWE-392 | Observe worker failures instead of losing security-relevant processing errors. | Ignored `Future`, no `result()`/`exception()`, `map()` exceptions never consumed, silent audit job failure. |

### 08 Coding Standards

| Rule | CWE candidate | Review focus | Common leads |
| --- | --- | --- | --- |
| `pyscg-0031` Use Copies When Modifying Iterables | CWE-1095 | Avoid skipped or inconsistent processing when collections mutate during iteration. | Removing ACLs, sessions, jobs, or filters while iterating the same collection. |
| `pyscg-0032` Avoid Redefining Built-in Functions or Standard Library Identifiers | CWE-1109 | Prevent shadowing that changes security behavior or misleads reviewers. | Variables or modules named `str`, `list`, `id`, `open`, `json`, `os`, `secrets`, `logging`. |
| `pyscg-0033` Implement Comparisons by Value Rather Than Reference | CWE-595 | Use value equality for security state and custom objects. | `is` used for strings/ints/roles, missing `__eq__`, identity-based membership assumptions. |
| `pyscg-0034` Check for None Values | CWE-476 | Handle absent objects and optional returns before dereference or policy use. | `None` from lookup/auth/cache, `len(None)`, attribute access after failed fetch, raising `None`. |
| `pyscg-0035` Complete Resource Cleanup | CWE-459 | Remove temporary artifacts and limit access to them. | Manual temp paths, leaked files, permissive temporary permissions, abnormal termination cleanup gaps. |
| `pyscg-0036` Check Return Values | CWE-252 | Use returned values and sentinel states correctly. | Ignored immutable transforms, unchecked `None`/false returns, failed validation or write results. |
| `pyscg-0037` Presume Assertions May Be Disabled In Production | CWE-617 | Never rely on `assert` for security checks or required validation. | `assert user.is_admin`, `assert token`, `assert path.is_relative_to`, `python -O` exposure. |
| `pyscg-0051` Release Unused Resources | CWE-404 | Close files, sockets, DB handles, and other OS resources deterministically. | Missing `with`, leaked clients, long-lived handles, worker/process resource accumulation. |

### 09 Cryptography

| Rule | CWE candidate | Review focus | Common leads |
| --- | --- | --- | --- |
| `pyscg-0038` Use Sufficiently Random Values | CWE-330 | Use cryptographically strong randomness for security-sensitive values. | `random`, seeded PRNGs, predictable tokens, reset links, session IDs, salts, nonces, generated passwords. |

## Coverage Notes

- Apply every high-priority group that matches an exposed trust boundary, then record which lower-priority groups were sampled or excluded.
- Treat numeric, concurrency, and coding-standard rules as security findings only when the code path can affect confidentiality, integrity, availability, authorization, auditability, or resource isolation.
- The guide is standard-library focused. If the repository uses framework, third-party, native, or cloud-specific APIs, extend the review beyond this index while keeping the same evidence standard.
- For recovered source, record whether a rule could not be evaluated because configuration, native code, generated code, or original symbol information is missing.
