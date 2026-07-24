# Python Trust-Boundary Surfaces

Use this reference when an attacker-controlled value crosses into a Python security decision or high-impact sink.

## Contents

- Review method
- Trust zones and server-side access
- Secrets and configuration
- Locale, encoding, canonicalization, and allowlists
- Format strings, commands, and SQL
- Binary data, archives, search paths, and deserialization
- Logging, errors, and developer tooling
- Randomness

## Review Method

Trace each candidate as:

```text
attacker input -> parser/decoder -> canonicalization -> validation -> authorization -> transformation -> sink -> impact
```

Record:

- attacker position and required state
- exact input carrier and parser
- Python-specific behavior that matters
- existing control and bypass condition
- target asset or invariant
- test or PoC step that proves the path

Do not stop at a dangerous API or scanner hit. Confirm whether the value is attacker-controlled, whether the control is appropriate for the sink, and whether the sink is reachable in the deployed path.

## Trust Zones And Server-Side Access

Apply `pyscg-0040` and `pyscg-0055` when code trusts a process boundary, client field, or shared runtime too much.

Check for:

- less-trusted parsing, plugin, upload, report-generation, or tenant code running under the same OS user and Python runtime as secrets or privileged operations
- workers, web processes, schedulers, and admin jobs sharing one writable filesystem, environment, cache, database role, or import path
- client-provided `user`, `role`, `tenant`, `org`, `scope`, `is_admin`, `permission`, or `action` fields used as authority
- authorization performed only in templates, frontend code, serialized client state, hidden form values, or unsigned JWT claims
- background tasks that accept an object ID or principal from a queue payload without re-authorizing server-side
- policy failures that default to a broad role, anonymous access, or prior cached state

Expect:

- distinct OS identities or equivalent isolation for materially different trust zones
- server-side identity derivation from validated session, token, service identity, or mTLS context
- object, tenant, and action authorization at every read, write, export, and asynchronous transition
- deny-by-default behavior when identity or policy state is absent, malformed, or stale

Useful leads:

```bash
rg -n "is_admin|role|roles|tenant|org_id|session_user|permission|scope|authorize|authz|current_user|request\\.json|form_data"
rg -n "os\\.setuid|os\\.setgid|subprocess|multiprocessing|celery|rq|dramatiq|ThreadPoolExecutor|ProcessPoolExecutor"
```

## Secrets And Configuration

Apply `pyscg-0041` when source, package artifacts, or runtime defaults contain secret or deployment-specific trust material.

Check for:

- passwords, tokens, API keys, private keys, certificate material, connection strings, backend addresses, or default admin credentials in Python constants, test fixtures, package data, notebooks, `.env` files, or recovered `.pyc` constants
- secret values logged, printed, embedded in exception messages, copied into URLs, or passed on process command lines
- code that cannot rotate or reject secrets without a source change or rebuild
- config readers that accept attacker-writable paths, overly broad permissions, or untrusted environment variables
- shared machine identities where per-deployment or per-service identities are expected

Expect:

- runtime secret injection from a protected mechanism with least-privilege access
- replaceable credentials and explicit failure when required secret material is missing
- no secret-bearing debug output or package artifacts
- deployment-specific trust material separated from code and protected by filesystem or platform controls

Useful leads:

```bash
rg -n "(password|passwd|secret|token|api[_-]?key|private[_-]?key|BEGIN [A-Z ]+ PRIVATE KEY|connection[_-]?string|client[_-]?secret)"
rg -n "os\\.environ|getenv|configparser|dotenv|yaml\\.safe_load|tomllib|Path\\(.+config|open\\(.+config"
```

## Locale, Encoding, Canonicalization, And Allowlists

Apply `pyscg-0043`, `pyscg-0044`, `pyscg-0045`, and `pyscg-0047` together when text crosses a trust boundary.

Check for:

- validation before Unicode normalization, path resolution, case folding, percent decoding, or other canonicalization
- producer and consumer components using different encodings or implicit codec defaults
- lossy transformations that can turn rejected text into executable, queryable, or renderable text later
- locale-dependent dates, numbers, sorting, or comparisons in authentication, policy, signature, or accounting flows
- denylists for characters, extensions, commands, HTML, SQL, paths, or identifiers where an allowlist is feasible
- path checks that compare raw strings instead of resolved paths within a trusted base directory
- multiple validation layers that normalize differently, especially across services or queues

Expect:

- one explicit encoding contract per boundary
- canonicalization before validation and before security comparisons
- allowlists for structured identifiers, actions, extensions, encodings, and protocol values
- sink-specific defense after validation, such as parameterization or path containment
- explicit locale handling where locale can affect behavior

Useful leads:

```bash
rg -n "encode\\(|decode\\(|unicodedata|normalize\\(|casefold\\(|lower\\(|upper\\(|locale\\.|setlocale|resolve\\(|relative_to\\(|urlparse|unquote"
rg -n "deny|blacklist|blocklist|replace\\(|re\\.sub|startswith\\(|endswith\\(|allowed|allowlist|whitelist"
```

Questions to answer:

- Which representation is validated?
- Which representation reaches the sink?
- Can an attacker choose the locale, encoding, normalization form, or path separator?
- Does a later decode, render, filesystem, or database layer reinterpret the value?

## Format Strings, Commands, And SQL

Apply `pyscg-0008`, `pyscg-0009`, and `pyscg-0010` to every path where untrusted text becomes instructions for another interpreter.

### Format Strings

Check for:

- attacker-controlled format templates passed to `.format()`, `.format_map()`, `%`, logging templates, translated strings, or custom formatter logic
- format strings that can traverse attributes or globals from exposed objects
- user-controlled templates used in errors, notifications, exports, or localization workflows

Expect:

- static format templates with attacker data passed only as values
- explicit template allowlists or a constrained rendering engine when users may customize output

Useful leads:

```bash
rg -n "\\.format\\(|format_map\\(|%\\s|%\\(|logging\\.(debug|info|warning|error|exception|critical)\\("
```

### Commands

Check for:

- `subprocess`, `os.system`, `os.popen`, shell wrappers, or platform commands receiving untrusted text
- `shell=True`, string-built commands, `shlex.split()` applied to attacker-influenced strings, user-selected executables or flags, and hostile filenames fed into utilities
- `shell=False` calls where arguments still trigger secondary execution, option injection, path lookup, or dangerous tool behavior
- commands used where `pathlib`, `shutil`, `os`, `stat`, archive, or other library APIs would suffice
- inherited `PATH`, working directory, environment, or import/search paths that change executable resolution

Expect:

- Python library APIs over process execution
- fixed executable paths and structured argv when commands are unavoidable
- allowlisted options and end-of-options handling where supported
- least-privilege execution in a dedicated trust zone

Useful leads:

```bash
rg -n "subprocess\\.|Popen\\(|run\\(|call\\(|check_output\\(|os\\.system\\(|os\\.popen\\(|shell\\s*=\\s*True|shlex\\.split"
```

### SQL

Check for:

- f-strings, `%`, `.format()`, concatenation, or `executescript()` around SQL
- raw ORM fragments, dynamic identifiers, order clauses, table names, or filter operators derived from user input
- database APIs that expose shell or scripting extensions
- sanitization presented as the primary SQL defense instead of parameterization

Expect:

- parameterized values
- strict allowlists for identifiers or sort directions that cannot be bound
- no multi-statement script execution with attacker-influenced text

Useful leads:

```bash
rg -n "execute\\(|executemany\\(|executescript\\(|raw\\(|text\\(|SELECT |INSERT |UPDATE |DELETE |ORDER BY|WHERE "
```

## Binary Data, Archives, Search Paths, And Deserialization

### External Binary And Native Data

Apply `pyscg-0011` when Python consumes data from native code, binary protocols, files, or FFI boundaries.

Check for:

- signed/unsigned mismatch in `struct`, `ctypes`, NumPy, or native-extension values
- width truncation before bounds, allocation, length, or authorization decisions
- attacker-controlled size, offset, index, timestamp, or flag values crossing from C-backed representations

Expect:

- exact format declarations
- range validation before use
- conversions that preserve the full valid range and reject impossible values

### Archives

Apply `pyscg-0012` and `pyscg-0044` together to every archive or package extraction path.

Check for:

- `extractall()` or `extract()` without resolved-path containment under a server-selected base directory
- absolute paths, `..`, mixed separators, drive letters, symlinks, hard links, nested archives, deep trees, huge entry counts, and untrusted metadata sizes
- extraction into executable, importable, served, or shared directories
- use of archive metadata alone to enforce decompressed size limits

Expect:

- server-selected extraction root outside sensitive or executable locations
- resolved member path checks before extraction
- file count, actual-read size, nesting, type, and link controls
- resource isolation for untrusted extraction

Useful leads:

```bash
rg -n "zipfile|tarfile|shutil\\.unpack_archive|extractall\\(|extract\\(|ZipFile|TarFile|infolist\\(|getmembers\\("
```

### Search Paths And Imports

Apply `pyscg-0013` when import or executable resolution can be influenced by less-trusted state.

Check for:

- attacker-writable cwd or directories appearing before trusted package paths
- `sys.path.insert`, `PYTHONPATH`, `PATH`, plugin paths, `sitecustomize`, `usercustomize`, or dynamic import names
- execution from writable temp, upload, or extracted directories
- bytecode or package artifacts loaded without integrity expectations
- process launch that inherits an attacker-controlled environment

Expect:

- trusted, immutable import and executable paths
- explicit environment construction for privileged subprocesses
- plugin/package integrity verification where code is loaded dynamically

Useful leads:

```bash
rg -n "sys\\.path|PYTHONPATH|PATH|importlib|__import__|pkgutil|sitecustomize|usercustomize|zipimport|exec_module|entry_points"
```

### Deserialization

Apply `pyscg-0023` to serialized data from requests, queues, caches, files, databases, or IPC.

Check for:

- `pickle.load(s)`, `shelve`, or equivalent object reconstruction on data that can be tampered with
- integrity checks performed after deserialization
- signed payloads with weak key handling or no replay/context binding
- deserialized objects that choose classes, methods, or dynamic behavior
- JSON/YAML or other text formats accepted without schema, type, range, and authorization validation

Expect:

- text-based data formats with explicit schemas where possible
- integrity verification before any unavoidable object deserialization
- strict type, field, and range validation after parsing
- no assumption that data is safe merely because it originated from a once-trusted source

Useful leads:

```bash
rg -n "pickle\\.|shelve|marshal\\.|yaml\\.|loads\\(|load\\(|dill|cloudpickle|joblib"
```

## Logging, Errors, And Developer Tooling

Apply `pyscg-0019`, `pyscg-0020`, `pyscg-0021`, `pyscg-0022`, and `pyscg-0050` together.

Check for:

- secrets, tokens, cookies, authorization headers, PII, or full request/response bodies in logs
- raw attacker text in line-oriented or HTML-viewed logs without CRLF or context-safe handling
- missing audit events for login failures, authorization denials, privilege changes, sensitive reads, parser rejections, secret use, or admin actions
- stack traces, SQL errors, file paths, internal hosts, secrets, or dependency details returned to users
- debug routes, test helpers, monkey patches, profiler hooks, verbose trace flags, or troubleshooting code shipped in production
- `print()` used for security-relevant operational output

Expect:

- structured, sink-safe logs with secret redaction and security event coverage
- operator-only diagnostics separated from user-visible errors
- production packaging that excludes developer tooling and debug-only behavior

Useful leads:

```bash
rg -n "logging\\.|logger\\.|print\\(|traceback|exc_info|debug|DEBUG|monkey|patch|profiler|werkzeug|pdb|breakpoint\\("
rg -n "Authorization|cookie|session|token|password|secret|api[_-]?key|request\\.body|request\\.json"
```

## Randomness

Apply `pyscg-0038` when random values affect authentication, authorization, secrecy, uniqueness, or anti-replay behavior.

Check for:

- `random`, `randint`, `choice`, `shuffle`, seeded PRNGs, timestamps, UUID variants, or process IDs used for tokens, reset links, session IDs, salts, nonces, API keys, generated passwords, invite codes, or CSRF state
- deterministic seeds or test-mode randomness reachable in production
- custom token generation with too little entropy or predictable formatting

Expect:

- `secrets` or OS-backed cryptographic randomness for security-sensitive values
- enough entropy for the attack model
- no reuse of security-sensitive random values across contexts

Useful leads:

```bash
rg -n "import random|random\\.|seed\\(|uuid|token_|nonce|salt|reset|invite|csrf|session_id|api_key"
```
