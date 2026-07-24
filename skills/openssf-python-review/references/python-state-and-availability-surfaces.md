# Python State And Availability Surfaces

Use this reference when attacker-influenced inputs can corrupt security-relevant state, bypass limits, hide failures, or exhaust resources.

## Contents

- Reporting threshold
- Numeric integrity
- Exception and control-flow integrity
- Concurrency and resource exhaustion
- Coding-standard failures with security impact
- Review prompts

## Reporting Threshold

OpenSSF includes rules that look like correctness guidance until an attacker can steer them into a security effect. Report them as findings only when the path can affect:

- authorization, authentication, tenant isolation, or business-state transitions
- money, billing, quotas, rate limits, timeouts, or expiry
- file, socket, database, process, or thread availability
- audit completeness or incident-response evidence
- confidentiality or integrity of data derived from numeric or concurrent state

Otherwise, keep the issue as hardening guidance or a coverage note.

## Numeric Integrity

Apply `pyscg-0001` through `pyscg-0007` and `pyscg-0018` when numeric values influence security decisions.

| Rule | Security-relevant failure mode | Review leads |
| --- | --- | --- |
| `pyscg-0001` Control Numeric Precision | Floating-point drift changes balances, quotas, thresholds, or expiry calculations. | `float` in money, resource accounting, percentage, time, or authorization thresholds. |
| `pyscg-0002` Guard Fixed-Width Numbers Against Overflow | C-backed or fixed-width values wrap, truncate, or raise unexpectedly. | `numpy`, `ctypes`, `struct`, `datetime.timedelta`, FFI, binary protocol lengths, time conversions. |
| `pyscg-0003` Use Arithmetic Over Bitwise Operations | Shifts or bitwise math produce unexpected signed, size, or permission values. | Bit shifts in size, flags, permission masks, rate math, or bounds checks. |
| `pyscg-0004` Use Integer Loop Counters | Float counters skip termination or create unexpected iteration counts. | Retry loops, pagination, polling, throttling, and parser loops using float increments. |
| `pyscg-0005` Specify Rounding for Numeric Conversions | Truncation or implicit rounding changes entitlements, charges, or limits. | `int()` on user-derived floats, timestamp conversion, quota math, percentage conversion. |
| `pyscg-0006` Use an Appropriate Comparator for Numbers | String or exact-float comparisons misorder or misclassify values. | Version, amount, threshold, or rate comparison using strings or `==` on floats. |
| `pyscg-0007` Use String Literals for Decimal Construction | Binary float approximation contaminates exact decimal logic. | `Decimal(<float literal>)` in fees, balances, exchange rates, or fixed policy values. |
| `pyscg-0018` Validate Numeric Data Beyond Type Checking | NaN or infinity bypasses range checks and invariants. | `float()` on request data, direct NaN comparisons, min/max checks without `isfinite()`. |

Check for:

- numeric parsing before range validation
- exceptional float values (`nan`, `inf`, `-inf`) that compare unexpectedly
- fixed-width values crossing Python/native boundaries without explicit range checks
- conversions that silently truncate or round values used in authorization, billing, or resource allocation
- equality or ordering assumptions that differ between string, float, decimal, fraction, and integer representations

Expect:

- integers or exact decimal representations where exactness matters
- explicit rounding decisions
- finite/range validation after parsing and before security decisions
- clear separation between bit flags and arithmetic values
- tests at boundary, overflow, underflow, NaN, infinity, rounding, and precision-loss cases

Useful leads:

```bash
rg -n "Decimal\\(|float\\(|int\\(|round\\(|math\\.isclose|math\\.isnan|math\\.isfinite|numpy|ctypes|struct\\.|timedelta|<<|>>"
rg -n "quota|limit|balance|amount|price|rate|timeout|expires|expiry|ttl|offset|size|length|count|retry"
```

## Exception And Control-Flow Integrity

Apply `pyscg-0014`, `pyscg-0015`, `pyscg-0016`, `pyscg-0028`, and `pyscg-0052` when failures can alter security behavior.

| Rule | Security-relevant failure mode | Review leads |
| --- | --- | --- |
| `pyscg-0014` Use Specific Exception Types | Broad exceptions hide the reason a security control failed. | `raise Exception`, `raise BaseException`, broad handlers in auth, validation, file, or policy code. |
| `pyscg-0015` Handle Error Conditions | Ignored failures leave state partially applied or cause fail-open behavior. | Empty handlers, ignored return codes, fallback values, missing rollback or alerting. |
| `pyscg-0016` Propagate Exceptions and Preserve Context | Wrapped or swallowed failures hide the true control failure. | `except: pass`, blanket rethrow, no `raise ... from`, generic retry loops. |
| `pyscg-0028` Preserve Exceptions in Finally Blocks | `return`, `break`, or `continue` in `finally` discards a pending security exception. | `finally` blocks around transactions, auth, validation, cleanup, or policy checks. |
| `pyscg-0052` Ensure Cleanup on Exceptions | Locks, state, files, or transactions stay inconsistent after failure. | Manual lock release, partial mutation, missing rollback, state restored only on success. |

Check for:

- `except Exception` or bare `except` around authentication, authorization, parsing, validation, signature verification, database writes, file operations, or worker execution
- default values or cached state used after a security-relevant exception
- handlers that log and continue without restoring invariants
- `finally` blocks that mask failures or skip cleanup
- exceptions converted to success responses, empty results, or permissive authorization decisions
- retry logic that repeats state-changing work without idempotency or rollback

Expect:

- specific exceptions and explicit recovery rules
- fail-closed behavior for auth, policy, validation, and integrity checks
- preserved exception cause and enough observability for operators
- `with` statements or equivalent structured cleanup
- tests for the failure path, not only the happy path

Useful leads:

```bash
rg -n "except\\s*:|except Exception|except BaseException|raise Exception|raise BaseException|finally:|return .*finally|break|continue"
rg -n "rollback|commit|lock|acquire\\(|release\\(|transaction|retry|fallback|default|pass$"
```

## Concurrency And Resource Exhaustion

Apply `pyscg-0024` through `pyscg-0030`, plus `pyscg-0051` and `pyscg-0052`, to attacker-driven load and shared state.

| Rule | Security-relevant failure mode | Review leads |
| --- | --- | --- |
| `pyscg-0024` Ensure Thread Pool Tasks Can Be Interrupted | Long-running work cannot stop and drains capacity. | Blocking calls, no cancellation flag, stuck shutdown, unbounded external operations. |
| `pyscg-0025` Configure Adequate Resource Pools | Thread-per-input or unbounded queues enable denial of service. | `ThreadPoolExecutor`, manual threads, no queue bounds, no timeout, no backpressure. |
| `pyscg-0026` Prevent Deadlocks | Workers wait on work that cannot run, freezing service capacity. | Nested `future.result()`, lock ordering, tasks submitted from tasks in the same pool. |
| `pyscg-0027` Prevent Race Conditions | Check-then-act or unsynchronized shared state breaks security invariants. | Shared dict/list/set, token reuse, quota decrement, file TOCTOU, state transitions. |
| `pyscg-0029` Reinitialize Reused Thread Objects | Pooled workers leak prior request or tenant state. | `threading.local()`, auth context, tenant context, reused parser or client objects. |
| `pyscg-0030` Ensure Thread Pool Tasks Do Not Fail Silently | Failed security jobs disappear without alerting or retry. | Ignored `Future`, no `result()`/`exception()`, unconsumed `map()`, silent background failures. |
| `pyscg-0051` Release Unused Resources | Open handles accumulate until the service degrades or fails. | Files, sockets, DB cursors, HTTP clients, subprocess handles, temporary resources. |
| `pyscg-0052` Ensure Cleanup on Exceptions | Exceptional paths leak locks or state and amplify denial of service. | Manual acquire/release, partial worker state, cleanup only on success. |

Check for:

- queue, pool, worker, file, socket, DB connection, parser, or archive limits missing or attacker-controlled
- timeouts absent on external calls or task execution
- cancellation requests that do not reach active work
- locks held while waiting on untrusted I/O or other futures
- shared mutable state updated without atomicity or synchronization
- reused thread-local identity, tenant, request, or authorization context
- task exceptions dropped because futures are never observed
- cleanup paths that depend on normal process termination

Expect:

- bounded pools, queues, timeouts, and backpressure
- cancellation or graceful shutdown paths for long-running work
- minimal lock scope and deterministic lock ordering
- synchronization around security-relevant shared state
- explicit reinitialization of reusable worker context
- observed task failures and security-relevant alerting
- deterministic resource release with `with`, `try/finally`, or close hooks

Useful leads:

```bash
rg -n "ThreadPoolExecutor|ProcessPoolExecutor|Future|submit\\(|map\\(|result\\(|exception\\(|threading\\.local|Lock\\(|RLock\\(|Semaphore|Queue\\("
rg -n "open\\(|socket|requests\\.|httpx\\.|aiohttp|cursor\\(|connect\\(|Temporary|mkstemp|NamedTemporaryFile|close\\("
```

## Coding-Standard Failures With Security Impact

Apply `pyscg-0031` through `pyscg-0037` when language behavior changes a security decision.

| Rule | Security-relevant failure mode | Review leads |
| --- | --- | --- |
| `pyscg-0031` Use Copies When Modifying Iterables | In-place mutation skips revocation, filtering, or cleanup entries. | Removing sessions, ACLs, tokens, jobs, or files while iterating. |
| `pyscg-0032` Avoid Redefining Built-ins Or Standard Library Identifiers | Shadowing changes what a security-sensitive call means. | Variables/modules named `open`, `id`, `str`, `list`, `os`, `json`, `secrets`, `logging`. |
| `pyscg-0033` Implement Comparisons By Value Rather Than Reference | Identity checks misclassify roles, tokens, states, or custom objects. | `is` with strings/ints/enums, missing `__eq__`, custom domain objects in membership checks. |
| `pyscg-0034` Check For None Values | Missing lookup results cause crashes or unsafe fallback behavior. | Optional auth/tenant/user returns, cache misses, dereference before validation. |
| `pyscg-0035` Complete Resource Cleanup | Temporary artifacts remain accessible or exhaust storage. | Manual temp files, permissive temp dirs, cleanup only on success, crash leftovers. |
| `pyscg-0036` Check Return Values | Ignored results leave validation, mutation, or cleanup unapplied. | Immutable transforms not assigned, sentinel returns ignored, failed write/delete/auth checks. |
| `pyscg-0037` Presume Assertions May Be Disabled In Production | `python -O` removes security checks entirely. | `assert` used for role, path, token, signature, amount, or invariant validation. |

Check for:

- assertions in any path that guards security behavior
- `is` used where value equality is intended
- custom objects without equality semantics used in policy or membership decisions
- built-in or standard-library shadowing that makes code review or static analysis misleading
- methods on immutable values whose return is ignored
- iterables changed while processing revocations, allowlists, denylists, or resource cleanup
- temporary files or directories with weak permissions or incomplete cleanup

Expect:

- explicit runtime checks for all required security invariants
- value-based comparisons with clear domain semantics
- unambiguous names for security-sensitive modules and helpers
- return values checked and stored when behavior depends on them
- safe temporary file APIs and deterministic cleanup

Useful leads:

```bash
rg -n "\\bassert\\b|\\bis\\b|__eq__|dataclass|for .* in .*:|\\.remove\\(|\\.pop\\(|\\.discard\\(|tempfile|mkstemp|NamedTemporaryFile"
rg -n "^(open|id|str|list|dict|set|json|os|secrets|logging)\\s*=|def (open|id|str|list|dict|set)\\("
```

## Review Prompts

- Can an attacker choose the value, timing, order, or volume that reaches this path?
- Which invariant is supposed to hold before and after the operation?
- Does an exception, timeout, cancellation, or worker reuse break that invariant?
- Does a numeric edge case bypass a limit or create a different state than the reviewer expects?
- Does the code remain secure under `python -O`, process restart, worker reuse, partial failure, and concurrent requests?
- Which regression test proves the failure before the fix and the invariant after it?
