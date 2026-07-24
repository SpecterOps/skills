# Large Python Project Triage

Use this reference to keep a repository-scale review focused, reproducible, and evidence-driven.

## Contents

- Review modes
- Inventory sequence
- Priority order
- Search anchors
- Coverage ledger
- Escalation rules

## Review Modes

- Use a baseline review for a new repository, a recovered source tree, a major release, a post-incident review, or a codebase with unknown trust boundaries.
- Use a diff-based review for a pull request or narrow change, but expand to baseline review when the change introduces a new parser, integration, trust boundary, secret, worker, archive, plugin, or privileged path.
- Use a recovered-source review whenever the tree lacks original source fidelity, even if the repository is large and otherwise complete.

## Inventory Sequence

1. Identify execution surfaces.
   - Find `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements*.txt`, lockfiles, `Pipfile`, `tox.ini`, `noxfile.py`, Dockerfiles, service definitions, and deployment manifests.
   - Find `__main__.py`, console entry points, ASGI/WSGI apps, Celery/RQ/Dramatiq workers, cron jobs, migrations, CLI modules, plugins, import hooks, and notebooks.
   - Find framework routing, task registration, serializers, command handlers, and event consumers.

2. Identify security assets and trust boundaries.
   - Map user identities, service identities, tenants, admin roles, secrets, key material, databases, object stores, caches, queues, uploaded files, generated reports, and external APIs.
   - Mark which inputs are remote, authenticated, tenant-controlled, operator-controlled, environment-controlled, or only locally writable.
   - Mark which components share OS identity, filesystem, import path, database role, cache, or queue.

3. Identify Python-specific sink clusters.
   - Search for command execution, SQL, deserialization, archive extraction, dynamic import, path handling, encoding conversion, logging, error rendering, randomness, thread pools, temporary files, and assertions.
   - Read the surrounding module and its callers instead of reporting from a search hit alone.
   - Cluster repeated helpers so one root cause is not reported as many duplicate symptoms.

4. Trace the most exposed paths first.
   - Start with unauthenticated routes, file uploads, webhooks, queue consumers, parser entry points, import/plugin loaders, admin APIs, secrets/config loaders, and background jobs that act with more privilege than their callers.
   - Then inspect shared helpers and lower-level wrappers that may widen the same flaw across the repository.

5. Keep a coverage ledger while reviewing.
   - Record reviewed package, entry point, trust boundary, rule groups applied, confirmed findings, open questions, and missing runtime evidence.
   - Record skipped packages and why they were lower priority.
   - Record which test, scanner, or live validation steps were not run.

## Priority Order

Use this order unless the threat model gives a stronger reason to change it:

1. Authentication, authorization, tenant isolation, trust-zone separation, and secret handling.
2. Code execution, deserialization, dynamic import, archive extraction, command execution, and SQL.
3. Canonicalization, encoding, path containment, upload handling, and log/error disclosure.
4. Randomness, signing, token creation, and key use.
5. Concurrency, resource exhaustion, cleanup, and background-task failure handling.
6. Numeric integrity and coding-standard rules where they influence security state.

## Search Anchors

Use these as review leads, then trace the path manually:

```bash
rg -n "FastAPI|Flask|Django|Starlette|APIRouter|Blueprint|urlpatterns|add_url_rule|route\\(|@app\\.|@router\\."
rg -n "celery|shared_task|task\\(|rq|dramatiq|cron|schedule|apscheduler|consumer|handler|webhook|callback"
rg -n "subprocess\\.|os\\.system|pickle\\.|shelve|marshal\\.|yaml\\.|zipfile|tarfile|unpack_archive|importlib|__import__|sys\\.path"
rg -n "execute\\(|executescript\\(|raw\\(|text\\(|format\\(|format_map\\(|eval\\(|exec\\("
rg -n "logging\\.|logger\\.|traceback|debug|DEBUG|secret|token|password|api[_-]?key|private[_-]?key"
rg -n "ThreadPoolExecutor|ProcessPoolExecutor|threading\\.local|Lock\\(|Queue\\(|asyncio|Temporary|mkstemp|NamedTemporaryFile|\\bassert\\b"
```

For large repositories, start with file-level counts before reading deeply:

```bash
rg -l "subprocess\\.|os\\.system|pickle\\.|extractall\\(|executescript\\(|sys\\.path|ThreadPoolExecutor|\\bassert\\b" .
rg --files -g '*.py' -g 'pyproject.toml' -g 'setup.py' -g 'requirements*.txt' -g 'Dockerfile*' -g '*.yaml' -g '*.yml'
```

## Coverage Ledger

Maintain a compact working table:

| Surface | Entry point or package | Attacker input | Sensitive sink or decision | Rules applied | Status |
| --- | --- | --- | --- | --- | --- |
| Auth | `api/users.py` | session cookie, JSON body | role and tenant check | `pyscg-0055`, `pyscg-0040` | reviewed / open / finding |
| Upload | `workers/archive.py` | ZIP upload | extraction path and worker FS | `pyscg-0012`, `pyscg-0044` | reviewed / open / finding |
| Queue | `tasks/import.py` | broker payload | `pickle.loads` | `pyscg-0023` | reviewed / open / finding |

Keep notes on:

- caller and sink locations
- trust assumptions not visible in source
- alternate routes or workers that reuse the same helper
- whether the same root cause affects multiple files
- whether a PoC or regression test exists

## Escalation Rules

- Expand from a module to the whole repository when a shared helper performs auth, validation, serialization, logging, config loading, command execution, or path handling.
- Expand from a diff to baseline review when a new dependency, worker, plugin, parser, archive format, or deployment boundary appears.
- Escalate a suspicious pattern to a finding only when attacker influence, missing control, reachability, and impact are all supported.
- Escalate a recovered-source gap to an open question when the missing artifact could materially change exploitability.
