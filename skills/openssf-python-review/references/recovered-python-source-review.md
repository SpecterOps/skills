# Recovered Python Source Review

Use this reference when source came from bytecode, wheels, frozen applications, containers, partial exports, code-generation output, or decompilers.

## Contents

- Goal
- Provenance and fidelity
- Reconstruct the execution model
- Handle decompiler and packaging artifacts
- Review workflow
- Evidence and reporting

## Goal

Treat recovered source as an evidence set, not as a perfect source tree. The review still needs a concrete attacker-controlled path and reachable impact, but the report must show which parts are proven from recovered code and which depend on missing runtime or packaging context.

## Provenance And Fidelity

Record before reviewing:

- original artifact type: `.pyc`, wheel, zipapp, PyInstaller bundle, container layer, vendored package, decompiled binary, or partial source export
- Python version and implementation if known
- recovery tool and version if known
- whether line numbers, symbol names, docstrings, annotations, decorators, exception tables, package metadata, and resources were preserved
- whether native extensions, compiled templates, static assets, config files, environment files, migrations, and deployment manifests are present
- whether the tree contains original source mixed with recovered output

Use confidence labels in working notes:

- `confirmed`: visible control flow and data path are sufficient to prove the issue
- `probable`: evidence strongly suggests the path, but a missing artifact or runtime fact still matters
- `open`: a suspicious construct exists, but exploitability cannot be decided from recovered material

Do not report `probable` or `open` items as confirmed vulnerabilities.

## Reconstruct The Execution Model

1. Recover package layout.
   - Find `__main__.py`, `__init__.py`, package metadata, entry points, console scripts, service wrappers, task modules, framework apps, and plugin registration.
   - Map import roots and package names before assuming a module is reachable.

2. Recover runtime boundaries.
   - Identify web, worker, scheduler, CLI, parser, migration, and admin components.
   - Identify where code likely runs under separate processes, OS identities, containers, or serverless handlers.
   - Note when the recovered tree cannot prove whether `pyscg-0040` process isolation exists.

3. Recover trust inputs.
   - Find request, CLI, file, archive, queue, database, environment, config, plugin, and IPC parsing code.
   - Track serialized data, dynamic imports, generated paths, and values copied into logs or errors.
   - When a caller is missing, state what input source would need to be confirmed.

4. Recover sensitive sinks.
   - Find subprocess, SQL, deserialization, archive extraction, path, import, secret, random, thread-pool, temp-file, and error/logging surfaces.
   - Trace back from sinks when entry points are missing or names are poor.

Useful leads:

```bash
rg -n "__main__|entry_points|console_scripts|FastAPI|Flask|Django|ASGI|WSGI|celery|shared_task|ThreadPoolExecutor|ProcessPoolExecutor"
rg -n "subprocess\\.|os\\.system|pickle\\.|marshal\\.|shelve|zipfile|tarfile|extractall\\(|importlib|__import__|sys\\.path|execute\\(|executescript\\("
rg -n "co_filename|<lambda>|<listcomp>|<dictcomp>|<module>|LOAD_GLOBAL|site-packages|dist-info|egg-info"
```

## Handle Decompiler And Packaging Artifacts

Expect ambiguity around:

- lost or shifted line numbers
- synthetic variable names and flattened comprehensions
- reconstructed `try`/`except`/`finally` blocks that obscure exception behavior
- lost decorators or descriptors that change authorization, routing, serialization, or validation
- constant folding that hides the original secret or comparison expression
- optimized bytecode that removed `assert` statements
- generated wrappers that hide framework checks or middleware
- missing package resources, templates, migrations, or configuration defaults
- missing native extensions or CFFI/ctypes targets
- duplicated vendored code that is not actually reachable

Verify before concluding:

- whether an odd expression is a decompiler artifact or real logic
- whether a missing validation step might exist in middleware, a decorator, a native extension, or generated code
- whether a dangerous helper is imported and reachable from an entry point
- whether an apparent secret is a real credential, a fixture, or a dead constant
- whether `assert`-based checks disappeared because the artifact was optimized

## Review Workflow

1. Start with sinks, not style.
   - Search for high-impact OpenSSF surfaces first: `pyscg-0055`, `pyscg-0041`, `pyscg-0009`, `pyscg-0010`, `pyscg-0012`, `pyscg-0013`, `pyscg-0023`, `pyscg-0019`, `pyscg-0050`, and `pyscg-0038`.
   - Read callers, registration points, and surrounding helpers until the input source and control path are visible.

2. Rebuild cross-module paths.
   - Track imports, exports, decorators, factory functions, dependency injection, task registration, and route registration.
   - Use module names, strings, SQL, log messages, and config keys as anchors when symbols are degraded.
   - Compare duplicate helpers or vendored copies to identify the live implementation.

3. Separate source facts from deployment assumptions.
   - Source can prove a hardcoded secret, unsafe deserializer, string-built command, or raw archive extraction.
   - Source may not prove whether a route is internet-exposed, a queue is attacker-writable, a process runs as root, or a config file is protected.
   - Keep missing deployment facts in `Open Questions / Assumptions`.

4. Validate Python behavior.
   - Confirm version-dependent behavior for bytecode, import resolution, archive APIs, exception semantics, thread pools, and optimized assertions.
   - Confirm whether recovery preserved the behavior relevant to the finding.

5. Build conservative PoCs.
   - Prefer a local harness that imports or reproduces the recovered function with harmless input.
   - State when the PoC uses reconstructed assumptions because the original entry point or environment is missing.
   - Do not claim remote exploitability unless the external input path is proven.

## Evidence And Reporting

For each confirmed finding:

- cite recovered file and line references when available
- state artifact provenance and recovery confidence
- show the input, missing control, sink, and impact in narrow code excerpts
- identify the exact missing runtime facts, if any, that affect severity but not root-cause confirmation
- include the primary OpenSSF rule and precise CWE mapping
- reference the per-finding PoC and state which steps were reconstructed versus executed

Use `Open Questions / Assumptions` for:

- missing entry-point registration
- unknown exposure or authentication boundary
- unknown OS user, container, filesystem, queue, or database permissions
- missing native extension or middleware behavior
- missing secret-management, deployment, or runtime configuration
- uncertainty introduced by decompilation or optimization

Use `Coverage` to state:

- artifact types reviewed
- packages and entry points reconstructed
- OpenSSF rule groups applied
- native/generated/configuration areas not available
- tests, dynamic validation, and PoC steps not executed
