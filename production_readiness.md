# Production Readiness Maintenance Roadmap

Last reviewed: 2026-08-13

This document is the execution plan for making repository maintenance local-first, deterministic, and CI-ready. It is intentionally written as a set of bounded work packets. A fresh agent should be able to implement one packet by reading the global execution contract and that packet only; prior chat history must not be required.

## Objective and scope

The target end state is a repository in which maintainers use a small, stable `just` interface locally and CI invokes the same commands. Routine validation must be offline, read-only, deterministic, and safe to run in a dirty worktree. Network access and tracked-file mutation must be explicit.

This roadmap addresses these review findings:

- Finding 1: the Codex activity-report skill can persist secrets without redaction.
- Finding 3: the BloodHound snapshot/index generator corrupts YAML metadata and can misclassify query domains.
- Finding 4: two supplied internal-training course configurations are invalid YAML.
- Finding 6: four marketplace plugins are installable empty shells.
- Finding 7: the repository lacks unified maintenance automation and CI, and has catalog, metadata, link, portability, and provenance drift.

The following are not authorized by this roadmap unless a packet explicitly says otherwise:

- Remediating findings 2 or 5 from the original review.
- Changing offensive-security workflow behavior merely because a validator encounters it.
- Selecting or applying a repository-wide license.
- Automatically committing generated or refreshed data.
- Publishing reports, releases, pull requests, issues, or other external state.
- Broadly rewriting skill content that is unrelated to a packet's acceptance criteria.

Repository counts recorded in review notes are observations, not permanent assertions. Validators must discover the current repository dynamically.

## How to assign a packet to a fresh agent

Give the agent the packet ID and this instruction:

> Implement packet `PR-XX` from `production_readiness.md`. Read the global execution contract, source-of-truth table, and the complete `PR-XX` packet. Verify its prerequisites and record the starting Git state before editing. Stay within its owned paths unless a shared integration change is explicitly required. Preserve unrelated worktree changes. Run every acceptance command that is available, report unavailable prerequisites, and update the packet's status and handoff fields before finishing.

An execution agent must not infer missing decisions from another packet or from prior conversation. If a required choice is not encoded here and materially changes behavior, it must stop and record a decision blocker rather than expand scope.

## Global execution contract

These requirements apply to every packet.

### Command classes

- `just check` is the primary quality gate. It must be offline, read-only, deterministic, and safe in a dirty worktree.
- `just ci` invokes the same offline quality gate as `just check`. CI may install pinned dependencies beforehand, but the quality gate itself must not fetch data.
- `check-*`, `validate-*`, and `test-*` recipes do not modify tracked files or use the network.
- `generate-*` recipes may update only their declared generated files and must not use the network.
- `refresh-*` recipes may use the network and modify only their declared snapshot/generated files.
- `check-external-*` and `check-upstream-*` recipes may use the network but remain non-mutating.
- No ordinary check may depend on a clean worktree. Generated checks build expected output in temporary storage and compare only declared outputs.

### Toolchain

- `just` is the stable human-facing command interface.
- Python 3.13 is the selected maintenance runtime. Add `tools/maintenance/.python-version` and constrain the maintenance project accordingly.
- `uv` manages and locks Python dependencies through `tools/maintenance/pyproject.toml` and `tools/maintenance/uv.lock`.
- `uv` and other missing tools are detected by `just doctor`; automation must not silently download or install them.
- The initial locked dependency set should be intentionally small: PyYAML, jsonschema, markdown-it-py, pytest, and ruff. Use the standard library, including `tomllib`, where practical.
- Platform tools such as ShellCheck, PowerShell, or PSScriptAnalyzer must be detected explicitly. A missing optional local tool produces a visible skip; the corresponding platform CI job becomes authoritative once `PR-60` lands.

### Worktree and filesystem safety

- Record `git rev-parse HEAD` and `git status --short` before editing.
- Preserve all unrelated tracked and untracked changes.
- Never use a whole-worktree reset, cleanup, or generated-drift comparison.
- Use temporary directories for comparisons and fixture output.
- Refresh workflows stage and validate complete output before replacing live data. A failure must leave existing output unchanged.
- Avoid fixed shared temporary paths. Use system temporary-directory APIs and unique names.

### Diagnostics and tests

- A failed check identifies the rule, offending path, and actionable reason.
- Tests use committed synthetic fixtures or construct them at runtime; they do not depend on host credentials, caches, or unrelated directories.
- Tests do not access the network unless they are explicitly testing a network adapter with a mocked transport.
- Avoid hard-coded repository counts, timestamps, absolute developer paths, and current Git SHAs in expected output.
- Every bug fixed under this roadmap gets a regression fixture that fails for the original behavior.

### Generated-file policy

- Commit generated marketplace files, README table regions, and BloodHound indexes because consumers use them without running maintenance tooling.
- Use explicit generated-region markers in mixed prose/Markdown documents. Never replace unrelated hand-written prose.
- JSON generated files cannot contain comments; their generated status and source command must be documented alongside the generator and in this file.
- Ordinary generation must not introduce wall-clock timestamps. A network refresh may update retrieval metadata.
- Running the same generator twice from the same inputs must produce byte-identical output.

### Exceptions

Exceptions live in `tools/maintenance/exceptions.toml`. Each exception must contain:

- An exact rule identifier and exact path or narrowly bounded path pattern.
- A rationale explaining why remediation is not appropriate.
- An owner.
- An expiration or review date.

Do not create a broad legacy baseline. New exceptions require explicit maintainer judgment and must not conceal a defect assigned to this roadmap.

### Security and provenance

- Treat all `.codex` activity sources as unsafe to publish.
- CI must never request sensitive/verbatim activity-report output and must not upload generated activity reports.
- Secret fixtures use unmistakable synthetic canaries assembled from fragments when needed to avoid triggering repository secret scanners.
- Do not fabricate artifact provenance. If a packaged binary cannot be tied to a real source, version/commit, license, and digest, record a decision blocker.
- Licensing checks are report-only until maintainers choose a licensing policy.

### Completion and handoff

Before finishing a packet, its agent must:

1. Run the packet-specific acceptance commands and the aggregate `just check` when available.
2. Confirm that check commands introduced no additional worktree changes.
3. Update the packet status, start reference, and completion reference or PR link.
4. Record changed files, test results, generated outputs, remaining risks, and blockers.
5. Mark a packet `complete` only when all required acceptance criteria pass. Missing optional platform tooling is acceptable only where the packet explicitly delegates that check to `PR-60`.

Allowed status values are `not-started`, `ready`, `in-progress`, `blocked`, and `complete`.

## Planned repository layout

`PR-00` establishes this layout. Later packets should extend it rather than creating parallel maintenance frameworks.

```text
justfile
.gitignore
tools/
  __init__.py
  maintenance/
    pyproject.toml
    uv.lock
    .python-version
    catalog.toml
    exceptions.toml
    provenance.toml
    just/
      core.just
      activity_report.just
      bloodhound.just
      catalog.just
      hygiene.just
      portability.just
      ci.just
    schemas/
  repo_maintenance/
    __init__.py
    __main__.py
    cli.py
    checks/
    generators/
    schemas.py
    tests/
      fixtures/
.github/
  workflows/
    quality.yml
    scheduled-maintenance.yml
```

The root `justfile` should import the predefined files under `tools/maintenance/just/`. The aggregate Python runner should discover checks by module convention so later packets normally add a check module and their owned recipe fragment without editing a central list. `PR-00` must document and test this extension seam.

## Sources of truth

| Concern | Canonical input | Derived or validated output |
|---|---|---|
| Plugin implementation | Plugin directory and packaged components | Capability/lifecycle validation |
| Plugin identity and UI | Codex and Claude manifests | Cross-manifest parity checks |
| Ownership | `plugins/*/ownership.json` | Exact skill and agent-reference validation |
| Plugin lifecycle | `ownership.json` status field | Publication eligibility |
| Publication order/surfaces | `tools/maintenance/catalog.toml` | Codex marketplace, Claude marketplace, root README regions |
| Skill membership | Directories containing `SKILL.md` | `ownership.skills` must exactly mirror discovery |
| Agent membership | Root `agents/*.toml`, curated ownership references | Reference validation; never inferred into ownership |
| BloodHound raw queries | Checked-in query snapshots and refresh manifest | Deterministic Markdown indexes and safety summary |
| Activity evidence | Original `.codex` sources | Redacted-by-default derived reports |
| Packaged executable origin | `tools/maintenance/provenance.toml` plus real upstream evidence | Digest, license, and immutable-source checks |

The Codex and Claude catalogs are intentionally allowed to have different membership. `tools/maintenance/catalog.toml` declares the intended surfaces; validators must not assume catalog equality.

## Planned command surface

These recipes become available as their owning packets land. `PR-00` owns the common commands and reserves/imports the phase-specific recipe files.

| Command | Owning packet | Required behavior |
|---|---|---|
| `just doctor` | PR-00 | Report required/optional tools and versions. |
| `just setup` | PR-00 | Run the locked `uv` environment setup without global installation. |
| `just fmt` / `just fmt-check` | PR-00 | Format maintenance Python or verify formatting. |
| `just test [target]` | PR-00 | Run deterministic tests, optionally narrowed by target. |
| `just validate [target]` | PR-00 | Run format/schema/semantic validation. |
| `just check` | PR-00 | Run every registered offline check. |
| `just ci` | PR-60 | Invoke the same offline gate as `just check`. |
| `just check-activity-report` | PR-10 | Run report redaction and CLI regression tests. |
| `just check-bloodhound` | PR-20 | Validate snapshots and compare deterministic output offline. |
| `just generate-bloodhound` | PR-20 | Regenerate tracked indexes from tracked snapshots. |
| `just refresh-bloodhound` | PR-20 | Refresh snapshots over the network using immutable upstream commits. |
| `just check-upstream-bloodhound` | PR-70 | Report upstream commit drift without modifying files. |
| `just check-catalog` | PR-30 | Compare generated catalogs/README regions without mutation. |
| `just generate-catalog` | PR-30 | Update declared catalog and README outputs. |
| `just check-links` | PR-40 | Validate first-party internal links and resource references offline. |
| `just check-portability` | PR-50 | Run path, temporary-file, executable-mode, and source-pin checks. |
| `just check-provenance` | PR-50 | Verify tracked executable metadata and digests. |
| `just check-powershell` | PR-50 | Run PowerShell AST/static checks when the required tool exists. |
| `just check-external-links` | PR-70 | Perform networked external-link validation with bounded retries. |

## Dependency graph and status

```text
PR-00 Foundation and invalid configurations
  |-- PR-10 Activity-report redaction (deferred)
  |-- PR-20 BloodHound deterministic generation (deferred)
  `-- PR-30 Plugin lifecycle and catalog generation
        `-- PR-50 Portability and artifact provenance
              `-- PR-40 Metadata and links
                    `-- PR-60 Core CI
                                                                                |
                                                                                v
                                                              PR-70 Scheduled maintenance
```

The current maintainer priority is `PR-30`, `PR-50`, `PR-40`, then `PR-60`.
`PR-10` and `PR-20` are explicitly deferred; they remain program-level work and their
checks must be added to the CI gate when implemented. `PR-40` waits for the catalog
contract from `PR-30`. The current-scope `PR-60` waits for `PR-30`, `PR-50`, and
`PR-40`. `PR-70` waits for core CI.

The graph and dependency fields, not the physical order of packet text, define execution order. Use the linked IDs below to open a packet directly.

| ID | Status | Findings | Depends on | May run in parallel with | Start ref | Completion ref / PR |
|---|---|---|---|---|---|---|
| [PR-00](#pr-00) | complete | 4, 7 | None | None until merged | `03ebface66a4e540da56dd3171692ce4b318a3f7` | `4c0a993` plus current hardening changeset |
| [PR-10](#pr-10) | not-started (deferred) | 1 | PR-00 | PR-20, PR-30, PR-50 | TBD | TBD |
| [PR-20](#pr-20) | not-started (deferred) | 3 | PR-00 | PR-10, PR-30, PR-50 | TBD | TBD |
| [PR-30](#pr-30) | complete | 6, 7 | PR-00 | PR-10, PR-20, PR-50 | `4c0a993` plus PR-00 hardening | Current working changeset |
| [PR-40](#pr-40) | complete | 7 | PR-00, PR-30 | PR-10, PR-20, PR-50 | Current working changeset | Current working changeset |
| [PR-50](#pr-50) | complete | 7 | PR-00 | PR-10, PR-20 | Current working changeset | Current working changeset |
| [PR-60](#pr-60) | in-progress | 7 | PR-30, PR-40, PR-50 | None | Current working changeset | Hosted CI evidence pending |
| [PR-70](#pr-70) | blocked | 7 | PR-60 | None | TBD | TBD |

---

<a id="pr-00"></a>

## PR-00 — Foundation and invalid configurations

Status: `complete`

Findings addressed: finding 4 and the maintenance foundation of finding 7.

Depends on: none.

Expected starting ref: `03ebface66a4e540da56dd3171692ce4b318a3f7`.

### Fresh-context brief

Create the repository's local maintenance harness and make its initial offline check green. Add the pinned Python 3.13/`uv` environment, thin `just` interface, extensible validation package, core schemas/tests, and `.gitignore`. Repair and schema-test the two invalid course YAML files. Do not absorb catalog, redaction, BloodHound, link, portability, provenance, or CI remediation assigned to later packets.

### Read first

- `README.md`
- `plugins/README.md`
- `.agents/plugins/marketplace.json`
- `.claude-plugin/marketplace.json`
- Representative `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, `ownership.json`, `SKILL.md`, `agents/openai.yaml`, and root `agents/*.toml` files.
- `plugins/internal-training-course/skills/course-wiki-migration-orchestrator/references/course-config-template.yaml`
- `plugins/internal-training-course/skills/course-wiki-migration-orchestrator/references/atrto-config.yaml`
- `plugins/internal-training-course/skills/course-wiki-migration-orchestrator/scripts/common.sh`

### Baseline evidence

- No root `justfile`, maintenance Python project/lock/runtime pin under `tools/maintenance/`, `.gitignore`, or CI workflow currently provides a common maintenance entry point.
- Both course configuration files use the unquoted scalar `course_title: Adversary Tactics: Red Team Operations`, which is invalid YAML because of the second colon.
- `common.sh` loads these configurations with PyYAML, so the supplied examples fail through the real runtime path.
- Python caches can appear under plugin script directories and are not ignored.
- Existing plugin and skill validation logic is fragmented rather than exposed through a repository-wide command.

### Decisions already made

- Use Python 3.13 and `uv`; do not add a parallel requirements/venv workflow as the primary path.
- Use a root lowercase `justfile` and phase-specific imported files under `tools/maintenance/just/`.
- The root recipes orchestrate; Python modules implement validation and generation behavior.
- Strict YAML parsing rejects duplicate mapping keys.
- Initial `just check` must be green after the two YAML repairs. Checks for known catalog, UI, link, redaction, BloodHound, and provenance defects become blocking only in their owning packets.
- Missing `uv` is reported with installation guidance; it is not silently installed.

### In scope

- Add the planned root toolchain and maintenance package skeleton.
- Define and test the check-module discovery/registration convention.
- Add `doctor`, `setup`, `fmt`, `fmt-check`, `test`, `validate`, and `check` recipes.
- Add strict JSON, YAML, TOML, Markdown-frontmatter, and Python syntax parsing.
- Add baseline structural validation for plugins, skills, UI metadata files, ownership files, root agents, and catalog JSON without yet enforcing later remediation rules.
- Quote both invalid `course_title` values.
- Add a course-config JSON Schema or equivalent path-specific schema.
- Require string values for `course_id`, `course_title`, repository/path fields, branch/title/image fields, and both preview URLs; require nonempty `commit_messages.stage1` and `commit_messages.stage2`.
- Add an integration test that sources `common.sh`, invokes `cfg_get` against both files, and reads `course_title`, both preview URLs, and both nested commit-message keys through the real helper.
- Add ignores for `.venv`, Python/test/tool caches, editor noise, and default generated `reports/codex-*.md` files.
- Document how later packets add checks and recipes without editing central dispatch where possible.

### Out of scope

- Catalog generation or lifecycle changes.
- UI length/prompt remediation, ownership drift, and link repair.
- Activity-report implementation changes.
- BloodHound generation changes.
- COM-path or binary provenance changes.
- GitHub Actions workflows.
- Adding temporary exceptions for defects assigned to later packets.

### Owned and shared paths

Normally owned:

- `justfile`
- `tools/maintenance/pyproject.toml`
- `tools/maintenance/uv.lock`
- `tools/maintenance/.python-version`
- `.gitignore`
- `tools/maintenance/just/`
- `tools/maintenance/schemas/`
- `tools/repo_maintenance/`
- `tools/repo_maintenance/tests/`
- The two course YAML files and focused course-config tests.

Shared integration paths established here:

- `tools/maintenance/exceptions.toml`
- Empty or documented placeholders for `tools/maintenance/catalog.toml` and `tools/maintenance/provenance.toml` if needed by the import/layout contract.

Later packets should extend their own recipe fragment and add discoverable Python modules rather than restructure these shared files.

### Required implementation

- [x] Pin the maintenance runtime to Python 3.13 and produce a complete `tools/maintenance/uv.lock`.
- [x] Make `just doctor` succeed while clearly distinguishing missing required and optional tools.
- [x] Make `just setup` use the locked environment and avoid global installation.
- [x] Ensure all core parsers produce path-specific failures and never execute parsed repository content.
- [x] Reject duplicate YAML keys with a regression fixture.
- [x] Repair both course configurations and validate their required top-level strings, URI-shaped preview URLs, and nested stage commit messages.
- [x] Prove that `just check` uses no network and creates no repository-local caches; disable bytecode/pytest caches or direct all tool caches to unique temporary locations.
- [x] Add tests for discovering a newly added check module without central registration edits.
- [x] Document recipe semantics in `plugins/README.md` or a focused maintenance section without duplicating this entire roadmap.

### Acceptance commands and outcomes

```text
git rev-parse HEAD
git status --short
just doctor
just setup
just fmt-check
just validate
just test
just check
just check
git status --short
```

Required outcomes:

- Both course YAML files parse and satisfy the course schema through an integration test.
- All JSON, YAML, TOML, Python, and selected frontmatter inputs parse under the core validator.
- The second `just check` is identical in result and does not change any tracked or untracked path other than declared ephemeral caches that are ignored.
- `just --list` exposes the documented core interface and imported phase recipe structure.
- Existing unrelated worktree changes remain untouched.

### Failure and rollback behavior

- If `uv` is unavailable, do not install it implicitly. Record the blocker and exact approved setup command needed.
- A parser failure must not partially rewrite a configuration.
- If stricter core validation discovers unrelated legacy drift, assign the rule to the appropriate later packet or seek a narrow, reviewed exception; do not mass-rewrite content to force green.

### Completion evidence and handoff

Record:

- Starting and completion refs.
- Tool versions used.
- The exact tests proving duplicate-key rejection and both course-config loads.
- The complete list of new commands.
- `just check` results and confirmation that it was non-mutating.
- Any extension-interface constraints later packets must follow.

Implementation handoff (2026-08-13):

- Starting ref: `03ebface66a4e540da56dd3171692ce4b318a3f7`.
- Completion reference: uncommitted working-tree changeset, intentionally left for
  maintainer review. This roadmap remains an untracked operational sidecar.
- Tool versions: Just 1.51.0, Python 3.13.14, bootstrapped uv 0.12.3, PyYAML
  6.0.3, jsonschema 4.25.1, markdown-it-py 4.0.0, pytest 8.4.2, and Ruff 0.12.12.
- Added commands: `bootstrap-uv`, `doctor`, `setup`, `fmt`, `fmt-check`, `test
  [target]`, `validate [target]`, and `check`.
- `just bootstrap-uv` creates the ignored `tools/maintenance/.bootstrap-venv`;
  `just setup` creates the ignored `tools/maintenance/.venv` from the complete lock.
- The duplicate-key regressions are
  `tools/repo_maintenance/tests/test_parsers.py::test_duplicate_yaml_key_is_rejected` and
  `tools/repo_maintenance/tests/test_parsers.py::test_duplicate_json_key_is_rejected`.
- Both real course files are schema-tested and exercised through sourced
  `common.sh`/`cfg_get` calls by `tools/repo_maintenance/tests/test_course_config.py`.
- `just fmt-check`, `just validate`, `just test`, and consecutive `just check`
  runs passed; 31 tests passed. Normalized check output was identical,
  Git status was unchanged, and no cache directory was created outside the two
  declared ignored virtual environments.
- ShellCheck, PowerShell, and PSScriptAnalyzer were unavailable and reported as
  optional skips; no PR-00 acceptance criterion depends on them.
- Later packets add sorted `check_*.py` modules exporting one unique `CheckSpec`
  and extend their pre-imported `tools/maintenance/just/*.just` fragment. Networked
  and mutating operations must remain outside automatic check discovery.

Update the status table and this packet's status before finishing.

---

<a id="pr-20"></a>

## PR-20 — Deterministic BloodHound snapshot generation

Status: `not-started`; deferred by maintainer priority.

Findings addressed: finding 3.

Depends on: `PR-00`.

May run in parallel with: `PR-10`, `PR-30`, and `PR-50`.

Expected starting ref: the completion ref of `PR-00`.

### Fresh-context brief

Replace the fragile BloodHound query snapshot/index workflow with a tested pipeline that cleanly separates offline deterministic generation from network refresh. Parse upstream YAML as YAML, classify domains only from metadata, repair the committed indexes, pin every refresh request to resolved immutable commits, and guarantee that a failed refresh leaves existing data intact.

### Read first

- `plugins/bloodhound/scripts/update-query-snapshots.py`
- `plugins/bloodhound/references/query-snapshots/manifest.json`
- `plugins/bloodhound/references/query-snapshots/NOTICE.md`
- `plugins/bloodhound/references/query-indexes/bloodhound.md`
- `plugins/bloodhound/references/query-indexes/azurehound.md`
- `plugins/bloodhound/references/query-indexes/openhound.md`
- `plugins/bloodhound/references/query-indexes/safety-scan.md`
- Representative YAML and JSON files under `plugins/bloodhound/references/query-snapshots/`.
- The BloodHound recipe fragment and maintenance extension contract from `PR-00`.

### Baseline evidence

- The generator uses line-oriented regular expressions for YAML scalar extraction. Its whitespace expression can consume a following line, turning an empty `description:` into the text `query: |-`.
- Generated indexes currently contain many rows with that bogus description.
- Domain inference scans query text for Azure-like terms. An Active Directory query containing `AZUREADKERBEROS` is consequently classified as Azure.
- The refresh path clears live destinations before all downloads and parsing succeed.
- Some content requests continue using a mutable branch after a commit SHA has been resolved.
- Manifest generation is inconsistent and does not provide complete per-file integrity evidence.

### Decisions already made

- Parse YAML with the repository's strict safe YAML loader. Do not recover scalar metadata with regular expressions.
- Normalize `platforms` from a supported string or list representation. Metadata is the only domain classifier; query text is never used for domain inference.
- A query may declare multiple domains. It appears once in each declared domain index, never twice within one index. Its snapshot file and manifest entry remain unique.
- An empty description remains an empty string.
- Offline generation consumes only checked-in snapshots and existing refresh metadata.
- Refresh resolves each upstream branch/ref once and uses only the resulting immutable commit for listings and file contents.
- Refresh stages all output, validates it completely, and installs it with rollback. It never deletes the live destination first.
- Refresh metadata timestamps may change only during refresh, not ordinary offline generation.
- Query safety-policy expansion belongs to finding 2 and is outside this packet. Existing safety output must remain deterministic, but this packet does not invent new blocking Cypher policy.

### In scope

- Refactor the current script into a thin CLI and importable parser/generator/refresh modules.
- Add explicit offline `check`, offline `generate`, and networked `refresh` modes.
- Add a non-mutating upstream-status adapter that `PR-70` can expose later, without scheduling it here.
- Parse supported YAML and JSON query formats with strict field types.
- Require nonempty name, query text, category where required by the source, and recognized platform metadata.
- Preserve upstream subdirectories recursively.
- Reject absolute paths, traversal, duplicate normalized paths, and case-fold path collisions.
- Resolve branch names to immutable commits before any content fetch and verify that every request uses those commits.
- Add bounded network timeouts and actionable source/path diagnostics.
- Stage snapshots, manifest, notice, indexes, and safety output in temporary storage; write the manifest once after validation.
- Record canonical source keys, immutable commits, file counts, and per-file SHA-256 values or an equivalently reviewable digest inventory.
- Make sorting, path encoding, Markdown escaping, newline policy, and output headers deterministic.
- Regenerate and commit the corrected indexes from the already checked-in snapshots without requiring a network refresh.
- Register `check-bloodhound`, `generate-bloodhound`, and `refresh-bloodhound` recipes.

### Out of scope

- Automatically refreshing to the latest upstream commit as part of a PR check.
- Changing query content merely because it lacks `LIMIT` or performs a write.
- Resolving broader operational safety findings from the original review.
- Scheduled upstream monitoring; that belongs to `PR-70`.
- Auto-committing refresh output.

### Owned and shared paths

Normally owned:

- `plugins/bloodhound/scripts/update-query-snapshots.py`
- New importable helpers beside that script.
- `plugins/bloodhound/references/query-snapshots/`
- `plugins/bloodhound/references/query-indexes/`
- Focused BloodHound tests and fixtures.
- `tools/maintenance/just/bloodhound.just`
- New BloodHound maintenance check/generator modules.

Shared only when required:

- Locked dependencies if the strict loader added by `PR-00` is insufficient.
- Maintenance documentation for new command names.

Do not edit `bloodhound-development` or unrelated BloodHound skill behavior.

### Required implementation

- [ ] Add a regression fixture where an empty YAML description is followed by `query: |-` and assert the description stays empty.
- [ ] Add an AD fixture containing `AZUREADKERBEROS` and assert it stays in the AD/BloodHound domain.
- [ ] Test scalar, list, and multi-domain platform metadata plus unknown/invalid platform types.
- [ ] Test supported JSON `query`/`cypher` fallbacks and reject invalid field types.
- [ ] Validate manifest keys, counts, safe unique paths, hashes, notices, and index links.
- [ ] Assert each query appears once per declared index and no generated description contains the parser artifact `query: |-`.
- [ ] Assert byte-identical output from repeated generation over identical fixtures.
- [ ] Simulate network, parse, and final-install failures and prove existing output is unchanged.
- [ ] Assert that offline check/generation opens no network connection.
- [ ] Assert every refresh content request uses the resolved immutable commit rather than a mutable branch.
- [ ] Handle paths with spaces without shell splitting.
- [ ] Preserve retrieval metadata during offline generation.

### Acceptance commands and outcomes

```text
git rev-parse HEAD
git status --short
just doctor
just test bloodhound
just check-bloodhound
just generate-bloodhound
just generate-bloodhound
just check-bloodhound
just check
git status --short
```

Required outcomes:

- Corrected indexes contain no metadata corruption from empty descriptions.
- The `AZUREADKERBEROS` AD regression fixture is classified from metadata, not its query text.
- Repeated generation creates no second diff.
- Offline checks use no network and do not modify tracked files.
- Tests prove failed refreshes preserve the existing destination.
- The committed manifest, notice, indexes, links, counts, source identifiers, and digests agree dynamically.

A live network refresh is not required for packet completion unless explicitly authorized. The mocked refresh suite must nevertheless cover the complete transactional behavior.

### Failure and rollback behavior

- Never clear the live snapshot or index directories before a fully validated replacement exists.
- On install failure, restore the prior directory and report both the primary and rollback errors.
- On unknown metadata, fail with the source path; do not guess a platform.
- A network failure must leave tracked files byte-for-byte unchanged.

### Completion evidence and handoff

Record:

- Starting and completion refs.
- Corrected generated files and whether the second generation was empty.
- Parser/classifier fixtures and their results.
- Simulated failure cases proving rollback.
- Manifest integrity fields and source-key normalization.
- Any upstream format not supported and the exact diagnostic it receives.

Update the status table and this packet's status before finishing.

---

<a id="pr-30"></a>

## PR-30 — Plugin lifecycle and catalog generation

Status: `complete`.

Findings addressed: finding 6 and catalog portions of finding 7.

Depends on: `PR-00`.

May run in parallel with: `PR-10`, `PR-20`, and `PR-50`.

Expected starting ref: the completion ref of `PR-00`.

### Fresh-context brief

Define an enforceable lifecycle for plugin directories, stop presenting empty shells as usable plugins, and replace the repository's manual multi-catalog update process with deterministic generation. Keep intentional publication metadata small and canonical, derive descriptive data from manifests and implementation, preserve intended Codex/Claude surface differences, and make catalog drift an offline blocking check.

### Read first

- `plugins/README.md`
- `README.md`, especially plugin installation/catalog tables.
- `.agents/plugins/marketplace.json`
- `.claude-plugin/marketplace.json`
- Every `plugins/*/ownership.json`.
- Codex and Claude manifests under representative active plugins.
- All files under `plugins/ops-adcs/`, `plugins/ops-mssql/`, `plugins/tradecraft-linux/`, and `plugins/tradecraft-mac/`.
- The catalog recipe fragment and generator extension contract from `PR-00`.

### Baseline evidence

- Repository documentation currently tells maintainers to update both marketplace files and README data manually.
- `ops-adcs`, `ops-mssql`, `tradecraft-linux`, and `tradecraft-mac` have manifests and marketplace entries but no packaged skills or other usable local capability.
- Their Codex entries are marked `AVAILABLE`, and some manifests advertise actionable starter prompts despite the corresponding README saying no skills are packaged.
- Catalog membership intentionally differs by platform, so naive equality checks would remove supported Codex-only entries.
- Descriptions, versions, ordering, policy, and membership are duplicated across multiple hand-edited files.

### Decisions already made

- Add `status` to each `ownership.json` with exactly these values: `active`, `incubating`, or `deprecated`.
- `active` requires at least one usable capability packaged by that plugin: a valid skill, local agent/command/hook, MCP/app declaration, or equivalent functional component. References to shared root agents in `ownership.json` do not count.
- `incubating` may remain in source without a capability. It is represented as `NOT_AVAILABLE` in the generated Codex catalog, omitted from the installable Claude catalog, and shown as planned/unavailable rather than usable in generated documentation.
- `deprecated` requires explicit replacement or retirement metadata. This packet adds schema support but does not deprecate plugins without a maintainer decision.
- Plugin directories and manifests supply implementation, identity, version, description, and category data.
- `tools/maintenance/catalog.toml` supplies only intentional ordering, publication surfaces, and narrowly necessary policy overrides. Do not duplicate full manifest metadata there.
- `ownership.skills` remains an asserted mirror of discovered skill directories and must match them exactly. Ownership agent references remain curated and are validated, not inferred.
- Marketplace JSON and marked root README regions are generated outputs. Manifests and ownership metadata remain hand-authored inputs.
- Codex and Claude surface membership is validated against declarations, not against each other.

### In scope

- Define and schema-validate plugin lifecycle metadata.
- Add lifecycle status to all plugin ownership files, preserving active plugins as active unless evidence requires a decision.
- Mark the four named empty shells `incubating`.
- Remove actionable default prompts from those four incubating Codex manifests or otherwise make their unavailable state unambiguous without inventing functionality.
- Add `tools/maintenance/catalog.toml` with explicit order and intended `codex`/`claude` surfaces.
- Build deterministic generators for `.agents/plugins/marketplace.json`, `.claude-plugin/marketplace.json`, and marked plugin-table regions in `README.md`.
- Preserve hand-written README prose outside generated markers.
- Validate common manifest identity/version/description fields for parity where both surfaces exist.
- Validate manifest name against directory and `ownership.plugin`.
- Validate `ownership.skills` as an exact set and every ownership agent reference against `agents/*.toml`.
- Fail if an active plugin loses its last packaged capability.
- Fail if an incubating plugin becomes installable or is described as currently usable.
- Fail if a required manifest for a declared surface is missing; do not silently change surface membership.
- Document the one-command catalog update/check workflow.
- Register `generate-catalog` and `check-catalog` with the aggregate offline check.

### Out of scope

- Inventing ADCS, MSSQL, Linux, or macOS skills to fill the empty shells.
- Deleting the four incubating plugin directories.
- Generating plugin manifests from catalog data.
- Inferring curated agent ownership from file references.
- Fixing all UI description lengths, link failures, or README skill-name drift; those belong to `PR-40`.
- Selecting licenses for currently unlicensed plugins.

### Owned and shared paths

Normally owned:

- `tools/maintenance/catalog.toml`
- Catalog schema, generator, tests, and fixtures.
- `tools/maintenance/just/catalog.just`
- `.agents/plugins/marketplace.json`
- `.claude-plugin/marketplace.json`
- Generated regions of `README.md`
- `plugins/*/ownership.json` lifecycle fields.
- Manifests/READMEs of the four incubating plugins only.

Shared integration paths:

- `tools/maintenance/exceptions.toml` for explicit publication exceptions.
- Root README generated-region conventions.

`PR-40` depends on this packet and must use the generator for generated README regions rather than hand-edit them.

### Required implementation

- [x] Define lifecycle and catalog schemas with actionable path-specific diagnostics.
- [x] Derive capability presence from actual packaged content rather than README claims.
- [x] Add regression tests for active-empty, incubating-published, missing-surface-manifest, duplicate-order, and stale generated-output failures.
- [x] Encode intentional Codex-only/Claude-only membership explicitly.
- [x] Generate stable ordering without timestamps or environment-dependent paths.
- [x] Use generated markers around mixed README content and test that prose outside markers is preserved exactly.
- [x] Make full-file JSON generation stable and document its source command.
- [x] Mark the four empty shells incubating and prevent their installation.
- [x] Validate semantic versions and common manifest parity without forcing fields that are genuinely platform-specific to match.
- [x] Ensure losing the last capability of an active plugin fails instead of silently changing publication.

### Acceptance commands and outcomes

```text
git rev-parse HEAD
git status --short
just doctor
just test catalog
just generate-catalog
just generate-catalog
just check-catalog
just check
git status --short
```

Required outcomes:

- A second catalog generation produces no diff.
- Both marketplace files and generated README regions match canonical inputs.
- All active plugins have at least one real packaged capability.
- The four named shells remain in source but are not installable: Codex marks them unavailable and Claude omits them from its installable list.
- Intentional cross-platform catalog differences are retained.
- Removing a manifest, capability, catalog declaration, or ownership reference causes a focused fixture test to fail.
- Hand-written README prose is unchanged by generation.

### Failure and rollback behavior

- Generate all catalog outputs in temporary storage, validate the complete set, then replace declared outputs.
- A failure in one output must not leave a partially updated catalog set.
- Never infer a surface change from a missing file; fail and request an explicit catalog update.
- Do not silently promote an incubating plugin when content appears. Promotion requires an explicit lifecycle change reviewed with its capability.

### Completion evidence and handoff

Record:

- Starting and completion refs.
- Final lifecycle disposition of every plugin and specifically the four shells.
- Canonical catalog fields and intentionally different platform membership.
- Generated files, idempotence result, and preserved prose test.
- Any plugin whose capability or lifecycle required maintainer judgment.

Implementation handoff (2026-08-13):

- Starting reference: `4c0a993` plus the PR-00 hardening changeset; completion
  reference is the current working changeset pending maintainer commit.
- All 25 plugins now declare lifecycle status. `ops-adcs`, `ops-mssql`,
  `tradecraft-linux`, and `tradecraft-mac` are incubating; every other plugin is
  active and has a discovered packaged capability.
- `tools/maintenance/catalog.toml` owns ordering and explicit Codex/Claude
  surfaces. Codex retains the four incubating entries as `NOT_AVAILABLE`; Claude
  omits them. The three tradecraft plugins remain intentionally Codex-only.
- Both marketplace files and the marked root README table are generated.
  Consecutive generation was byte-identical, and the rollback fixture preserved
  all outputs after a simulated partial installation failure.
- Seven catalog tests and the aggregate gate passed. No lifecycle decision
  remained ambiguous.

Update the status table and this packet's status before finishing.

---

<a id="pr-10"></a>

## PR-10 — Secure-by-default activity reports

Status: `not-started`; deferred by maintainer priority.

Findings addressed: finding 1.

Depends on: `PR-00`.

May run in parallel with: `PR-20`, `PR-30`, and `PR-50`.

Expected starting ref: the completion ref of `PR-00`.

### Fresh-context brief

Change the `codex-activity-report` generator from verbatim-by-default to redacted-by-default without changing its selection, focus, deduplication, or ordinary CLI semantics. Add a centralized recursive redactor, explicit unsafe opt-in, secure output handling, multi-source synthetic fixtures, documentation, and an offline check registered with the repository harness.

### Read first

- `plugins/codex-observability/skills/codex-activity-report/SKILL.md`
- `plugins/codex-observability/skills/codex-activity-report/references/log-sources.md`
- `plugins/codex-observability/skills/codex-activity-report/scripts/generate_codex_activity_report.py`
- The maintenance extension contract and activity-report recipe fragment produced by `PR-00`.

### Baseline evidence

- The skill instructs the generator to preserve exact prompts and commands.
- Event fields include command, quote, output, path lists, and arbitrary nested metadata.
- Tool arguments, history prompts, warnings/errors, planner objectives, command batches, and output excerpts can reach Markdown renderers.
- No centralized report redaction policy or default redaction pass exists.

### Decisions already made

- Every `.codex` source is trusted to parse but unsafe to publish.
- Raw logs remain authoritative evidence; generated reports are derived summaries.
- Parsing, filtering, focus matching, deduplication, and collapsing operate on raw in-memory events. Redaction occurs on a deep copy after selection and immediately before rendering.
- Default mode is `safe`; optional mode `strict` broadens high-entropy detection.
- `--include-sensitive` is the sole unsafe opt-out. It must be explicit, visibly warned, and forbidden in CI. No environment variable may disable redaction.
- Invalid redaction configuration fails closed before either report is written.
- Placeholders are typed and non-reversible, for example `[REDACTED:AUTH_TOKEN]`. Do not output hashes, lengths, or samples.
- Redaction is best effort and does not make a report automatically suitable for public release.

### In scope

- Add a focused redaction module beside the generator and a redaction-policy reference document.
- Recursively redact all string-bearing event fields and nested dict/list metadata.
- Independently sanitize report-level paths such as repository and Codex-home locations.
- Detect sensitive structured keys, assignments, environment variables, CLI flags, authorization/cookie headers, URL userinfo/query parameters, private-key blocks, JWTs, and common provider-token formats.
- Preserve operational false positives such as `max_tokens`, token counts/budgets, UUIDs, Git SHAs, session IDs, and public-key material.
- Support additive organization-specific JSON rules that cannot disable built-ins.
- Add `--redaction-mode safe|strict`, `--redaction-config PATH`, and `--include-sensitive` while retaining every current argument/default output path.
- Add report headers containing mode, sensitive-output status, and counts by redaction category only.
- Write both outputs atomically and with mode `0600` on POSIX.
- Refactor the entry point only as needed to inject `argv`, clock, paths, or transports for deterministic tests.
- Update skill and log-source documentation to describe redacted defaults and sensitive opt-in.
- Register focused tests and `just check-activity-report` with the aggregate offline check.
- Add a policy test that tracked CI/workflow content never invokes `--include-sensitive`.

### Out of scope

- Rewriting, deleting, or auditing existing user reports or original logs.
- Automatically rotating credentials that may have appeared in historical reports.
- Uploading reports as CI artifacts.
- Altering event selection or focus semantics.
- Claiming comprehensive secret detection.

### Owned and shared paths

Normally owned:

- `plugins/codex-observability/skills/codex-activity-report/`
- Focused activity-report tests/fixtures.
- `tools/maintenance/just/activity_report.just`
- New activity-report maintenance check modules.

Shared only when required:

- `tools/maintenance/exceptions.toml` for narrowly approved false positives.
- Aggregate maintenance documentation established by `PR-00`.

Do not edit unrelated observability skills or CI workflows.

### Required implementation

- [ ] Prove the existing leak with synthetic failing tests before or alongside the fix.
- [ ] Apply redaction to every renderer input, including collapsed command metadata and output excerpts.
- [ ] Make replacement idempotent.
- [ ] Ensure raw focus matching can select an event whose emitted match is redacted.
- [ ] Make unsafe output require `--include-sensitive`, emit a conspicuous stderr warning, and add a banner to both reports.
- [ ] Ensure invalid custom rules create no output files.
- [ ] Construct fixtures for rollout JSONL, archived rollout ZIP, `history.jsonl`, TUI logs, SQLite, and planner artifacts.
- [ ] Assert that every canary is absent from both default reports and that expected false positives remain.
- [ ] Test nested values, multiline keys, URL encoding, mixed case, repeated secrets, permissions, and existing CLI flags.
- [ ] Ensure no report output or canary fixture value is uploaded or persisted by maintenance CI.

### Acceptance commands and outcomes

```text
git rev-parse HEAD
git status --short
just doctor
just check-activity-report
just test activity-report
just check
git status --short
```

Required outcomes:

- No synthetic secret appears in either default Markdown output across any supported source type.
- Unsafe fixture values appear only with `--include-sensitive`, and both stderr and reports identify the unsafe mode.
- Existing non-security flags and selection behavior remain covered and unchanged.
- Invalid configuration fails before creating output.
- POSIX outputs have owner-only permissions.
- `just check` invokes the activity-report regression gate, remains offline, and does not generate a tracked report.

### Failure and rollback behavior

- A redaction exception or invalid rule fails closed; never fall back to verbatim output.
- Write to temporary sibling files and replace final reports only after both render successfully.
- Do not alter original activity sources.
- If a compatibility conflict requires weakening the safe default, stop and record a security decision blocker.

### Completion evidence and handoff

Record:

- Starting and completion refs.
- The redaction categories and explicit false-positive allowlist.
- Fixture source types and canary-absence results.
- CLI compatibility and file-permission results.
- Documentation changed and any limitations users must review manually.

Update the status table and this packet's status before finishing.

---

<a id="pr-40"></a>

## PR-40 — Metadata consistency and internal references

Status: `complete`.

Findings addressed: metadata, ownership, and internal-link portions of finding 7.

Depends on: `PR-00` and `PR-30`.

May run in parallel with: `PR-10`, `PR-20`, and `PR-50` after its dependencies are complete.

Expected starting ref: a ref containing completed `PR-00` and `PR-30`.

### Fresh-context brief

Turn repository metadata and first-party internal references into enforced contracts, then repair the current drift. Validate skill UI metadata, plugin manifests, ownership, root agents, skill indexes, Markdown links/anchors, and explicit bundled-resource references. Keep external URL checks and operating-system portability/provenance outside this packet.

### Read first

- The schema/check framework from `PR-00` and catalog/source-of-truth rules from `PR-30`.
- Representative `SKILL.md` and `agents/openai.yaml` pairs across several plugins.
- Every `plugins/*/ownership.json` and root `agents/*.toml`.
- `plugins/bloodhound/README.md` and `plugins/bloodhound/skills/README.md`.
- `plugins/ops-infrastructure/ownership.json`.
- `plugins/social-engineering/ownership.json` and `agents/report-writer.toml`.
- `plugins/c2-cobaltstrike/skills/c2-cobaltstrike-development/references/sleep-functions/INDEX.md` and linked local material.
- `plugins/report-timeline/skills/timeline-workflow/SKILL.md` and its resource tree.
- Root and per-plugin README/index files.

### Baseline evidence

- Many `agents/openai.yaml` short descriptions exceed the 25–64 character contract, and several are visibly truncated with an ellipsis.
- Several Codex plugin manifests provide more than three starter/default prompts.
- The BloodHound README uses stale skill identifiers and its skill index omits a packaged skill.
- `ops-infrastructure/ownership.json` omits the existing `iac-attack-surface` skill.
- `social-engineering/ownership.json` refers to `report_writer`, while the actual root agent identifier is `report-writer`.
- The root README contains a singular/plural repository installation typo.
- Multiple first-party Markdown references point to missing Cobalt Strike/Sleep tutorial files, and some skills name bundled resources that do not exist at the resolved path.
- No offline, fenced-code-aware internal-link/resource checker blocks recurrence.

### Decisions already made

- Every skill directory contains exactly one valid `SKILL.md`; its frontmatter name is globally unique and equals the directory name.
- Every skill has `agents/openai.yaml` with a 25–64 character `short_description`, no literal truncation suffix, and a `default_prompt` containing the exact `$skill-name` token.
- UI colors are six-digit hex values, icon paths remain inside the skill directory and exist, policy fields are real booleans, and MCP dependencies use supported shapes.
- Codex plugin manifests may contain at most three starter/default prompts.
- `ownership.skills` exactly matches discovered skill directories. Ownership agent names resolve to root `agents/<name>.toml`; underscore/hyphen aliases are not guessed.
- Root agent TOML filenames equal declared names and referenced skills exist.
- Internal first-party links and bundled-resource references are blocking. External HTTP(S) links are handled separately in `PR-70`.
- Actual Markdown links/anchors are parsed through a Markdown AST and ignore fenced code. Inline-code resource checks apply only to path-like references rooted at `scripts/`, `references/`, `assets/`, or an explicit relative path.
- If a document promises content that never existed and no correct target can be established, convert it to clearly marked planned/unavailable text rather than inventing a tutorial.
- Generated README regions from `PR-30` are changed only through the catalog generator.

### In scope

- Add strict skill/UI/plugin/ownership/root-agent semantic validators and regression fixtures.
- Repair all current first-party violations of those contracts.
- Limit plugin starter/default prompt arrays to three without changing core plugin capability.
- Correct ownership skill and agent-name drift.
- Correct stale skill names and incomplete per-plugin skill indexes.
- Build an offline internal Markdown link and anchor checker.
- Build a narrowly scoped checker for explicit bundled `scripts/`, `references/`, and `assets/` paths in skill instructions.
- Repair current broken first-party internal links/resources or explicitly remove unsupported promises.
- Validate local manifest/icon/logo paths and prevent traversal outside the intended plugin/skill root.
- Register metadata/link checks with `just check`, expose `just check-links`, and add exact regression fixtures.

### Out of scope

- External URL availability.
- Hard-coded developer home paths, temporary paths, executable bits, PowerShell portability, or packaged binary provenance; these belong to `PR-50`.
- Generating catalogs or hand-editing generated README regions.
- Changing broad plugin `Read`/`Write` capability declarations without a separate policy decision.
- Applying a license.
- Writing missing substantive training/tutorial content without a source or maintainer direction.

### Owned and shared paths

Normally owned:

- Skill `agents/openai.yaml` files requiring repair.
- Plugin manifests requiring starter-prompt repair.
- `plugins/*/ownership.json` fields other than lifecycle status.
- Root `agents/*.toml` only when needed to correct a proven identifier/reference defect.
- First-party Markdown/index files with broken internal references.
- Metadata/link validators, fixtures, and tests.
- `tools/maintenance/just/hygiene.just`

Shared integration paths:

- `tools/maintenance/exceptions.toml` for narrowly justified link/resource exceptions.
- Generated README regions, which must be updated via `just generate-catalog` rather than edited directly.

Do not modify vendored upstream content merely to satisfy a first-party style rule. Classify it precisely or add a reviewed exception.

### Required implementation

- [x] Validate every skill/frontmatter/UI pairing and add fixtures for length, truncation, prompt token, color, icon, boolean, and dependency errors.
- [x] Validate plugin manifest prompt limits and cross-file identity/path invariants.
- [x] Validate exact ownership skill sets and root agent references.
- [x] Repair the known BloodHound, infrastructure, social-engineering, and root README drift.
- [x] Parse Markdown links and anchors without treating fenced examples as live links.
- [x] Resolve paths relative to the containing document and reject unintended root escape.
- [x] Distinguish internal paths from external URLs, URI schemes, templates, globs, and illustrative placeholders.
- [x] Repair all unapproved first-party broken references found at implementation time.
- [x] Add fixtures for paths containing spaces, URL-encoded Markdown targets, anchors, nested relative paths, and code fences.
- [x] Produce a concise summary grouped by rule rather than flooding output with duplicate downstream errors.

### Acceptance commands and outcomes

```text
git rev-parse HEAD
git status --short
just doctor
just test metadata
just test links
just validate skills
just validate plugins
just validate ownership
just check-links
just check-catalog
just check
git status --short
```

Required outcomes:

- All skill/UI, plugin-prompt, ownership, and root-agent contracts pass without a broad legacy allowlist.
- Every first-party internal Markdown link/anchor and explicit bundled-resource path resolves or has a narrow, owned, unexpired exception.
- Generated catalog/README regions remain in sync after metadata repairs.
- External URLs are not fetched.
- The checker is stable on paths with spaces and ignores fenced examples as designed.
- `just check` remains non-mutating.

### Failure and rollback behavior

- Do not automatically truncate descriptions; write concise replacements that preserve the actual capability.
- Do not silently translate underscores to hyphens in ownership. Correct the source identifier deliberately.
- Do not create empty placeholder files solely to satisfy a broken link.
- Do not rewrite hand-written prose outside the minimum affected reference or generated region.
- If resolving a promised resource requires authoring substantive new material, record a maintainer decision blocker or remove the unsupported promise when intent is unambiguous.

### Completion evidence and handoff

Record:

- Starting and completion refs.
- Violations by rule before and after remediation; counts are evidence, not future assertions.
- All exceptions with owner and expiration.
- Files whose wording changed to satisfy UI limits.
- Broken references repaired, removed, or blocked on content decisions.
- Confirmation that generated catalog output remains current.

Implementation handoff (2026-08-13):

- Starting and completion references are the current working changeset pending
  maintainer commit.
- Repaired 37 overlong/truncated skill descriptions, five plugin prompt arrays,
  BloodHound skill names/index membership, ownership skill/agent drift, and the
  root `SpecterOps/skill` typo. The catalog remained current.
- The link checker validates Markdown AST links, anchors, encoded spaces, nested
  paths, root escape, and explicit bundled resources in `SKILL.md`, while fenced
  examples and external URLs are ignored.
- Removed 41 unsupported local-link promises from the imported Sleep reference
  material without creating placeholder tutorials. No exceptions were added.
- Nine metadata tests, three link tests, and the aggregate gate passed.

Update the status table and this packet's status before finishing.

---

<a id="pr-50"></a>

## PR-50 — Portability and executable provenance

Status: `complete`.

Findings addressed: portability and provenance portions of finding 7.

Depends on: `PR-00`.

May run in parallel with: `PR-10`, `PR-20`, and `PR-30`; it may also run alongside `PR-40` if shared Markdown files are avoided.

Expected starting ref: the completion ref of `PR-00`.

### Fresh-context brief

Make first-party scripts and packaged executable assets portable and reviewable. Add targeted checks for developer-specific operational paths, unsafe temporary-file defaults, script syntax/modes, immutable runtime sources, and artifact provenance. Repair the known COM proxy-triage paths and Koppeling/NetClone source pinning without fabricating provenance or applying a license.

### Read first

- `plugins/tradecraft-windows/skills/com-proxy-triage/SKILL.md`
- `plugins/tradecraft-windows/skills/com-proxy-triage/scripts/Watch-InProcServer32Misses.ps1`
- `plugins/tradecraft-windows/skills/com-proxy-triage/scripts/ComHijackHost.Common.ps1`
- All executable assets and accompanying documentation under `plugins/tradecraft-windows/skills/com-proxy-triage/assets/`.
- First-party shell, Python, Node, and PowerShell scripts across `plugins/`.
- `.gitignore` and the maintenance extension contract from `PR-00`.

### Baseline evidence

- `Watch-InProcServer32Misses.ps1` defaults to a specific developer path under `C:\Users\zach\Documents\...`, and the skill quickstart can rely on that default.
- COM helper logic performs an unpinned shallow clone of the Koppeling repository at runtime.
- A packaged `NetClone.exe` and multiple DLLs lack a complete machine-verifiable origin/commit/license/hash inventory.
- The repository has no central check for developer-specific operational paths, fixed temporary names, executable modes, or immutable runtime downloads.
- PowerShell, ShellCheck, and related platform tools may not be installed in every local sandbox.

### Decisions already made

- Scan first-party executable/configuration defaults, not every appearance of a Windows/Linux path in vendored docs, fixtures, or legitimate target-system examples.
- Developer-specific home paths are forbidden in operational defaults.
- Temporary output defaults use platform APIs and unique paths; scripts accept an explicit override where users need stable evidence locations.
- A shebang script documented as directly executable must have the corresponding Git executable bit.
- Runtime clones/downloads use HTTPS plus an immutable commit/version and verify the resulting source or artifact where practical.
- `tools/maintenance/provenance.toml` is canonical for tracked executable assets and contains real evidence: artifact path, upstream URL, immutable version/commit, build method, license evidence, and SHA-256.
- If provenance cannot be established, do not guess. Report a decision blocker; removal/replacement of the binary requires explicit maintainer direction.
- License checks report current state but do not select or apply a license.
- Local `just check-powershell` may visibly skip when PowerShell is unavailable. `PR-60` must run it in an environment where PowerShell is present before production readiness is complete.

### In scope

- Add first-party portability scanners with precise vendor/fixture/example boundaries.
- Detect developer-specific POSIX and Windows home paths in executable/config defaults.
- Detect unsafe fixed temporary-file patterns and require safe APIs or explicit reviewed exceptions.
- Check case-fold path collisions, UTF-8, line endings, shebang consistency, and Git executable bits.
- Run Python compile/AST parsing, `bash -n`, Node syntax checking, and available platform-native static analysis.
- Provide targeted `check-powershell`; add PSScriptAnalyzer integration when available.
- Replace the COM watcher developer-specific default with a unique portable temporary path and update quickstart behavior.
- Pin the Koppeling runtime source to a recorded immutable commit and verify the checked-out commit.
- Inventory tracked PE/DLL/executable artifacts dynamically in `tools/maintenance/provenance.toml` and verify SHA-256 values.
- Record source, commit/version, build instructions, and license evidence for the packaged Koppeling/NetClone assets when verifiable.
- Register `check-portability`, `check-provenance`, and `check-powershell` recipes and include portable checks in `just check`.

### Out of scope

- Selecting a root or plugin license.
- Reverse engineering a binary to manufacture origin evidence.
- Removing or replacing an unverified artifact without maintainer approval.
- Validating external Markdown URLs.
- General prose/path examples that are clearly non-operational and not used as defaults.
- Broad functional changes to COM proxy-triage behavior.

### Owned and shared paths

Normally owned:

- `tools/maintenance/provenance.toml`
- Provenance/portability schemas, checks, tests, and fixtures.
- `tools/maintenance/just/portability.just`
- First-party scripts whose portability defect is proven.
- `plugins/tradecraft-windows/skills/com-proxy-triage/` implementation and focused documentation.

Shared integration paths:

- `.gitignore` only if `PR-00` omitted a required generated/runtime path.
- `tools/maintenance/exceptions.toml` for exact vendor/example/static-analysis exceptions.

Avoid changing metadata/link files owned by `PR-40` unless the same COM instruction must describe the corrected invocation; report that overlap explicitly.

### Required implementation

- [x] Build authored-file classification so vendored/reference material does not receive unsafe automatic rewrites.
- [x] Add regression fixtures for POSIX, Windows, quoted, escaped, fixture, and legitimate target-path cases.
- [x] Replace the COM trace default and test its path creation/override behavior without assuming a specific user profile.
- [x] Pin and verify the Koppeling source checkout.
- [x] Discover executable assets from the Git index and fail when provenance entries are missing, stale, duplicated, or have the wrong digest.
- [x] Verify provenance paths remain inside the repository and immutable source fields are not branch names.
- [x] Check direct-invocation executable modes using Git metadata rather than host filesystem assumptions alone.
- [x] Add syntax checks that report missing optional tools distinctly from syntax failures.
- [x] Run PowerShell parser/static checks when available and encode the required `PR-60` CI follow-up when unavailable locally.
- [x] Keep license results informational until policy is explicitly decided.

### Acceptance commands and outcomes

```text
git rev-parse HEAD
git status --short
just doctor
just test portability
just check-portability
just check-provenance
just check-powershell
just check
git status --short
```

Required outcomes:

- No first-party executable/config default contains a developer-specific home path.
- COM watcher defaults are unique and portable, and explicit trace paths still work.
- The runtime Koppeling checkout is immutable and verified.
- Every tracked executable artifact in scope has matching, non-fabricated provenance and SHA-256 metadata, or the packet is explicitly blocked for a maintainer artifact decision.
- Script syntax/mode checks pass where tools are available; unavailable PowerShell coverage is clearly handed to `PR-60`.
- Licensing output remains informational.
- `just check` remains offline and non-mutating.

### Failure and rollback behavior

- Do not change or delete a binary merely to make provenance validation green.
- Do not replace a specific developer path with another fixed global path.
- A failed source clone/build/download must not overwrite a known-good packaged asset.
- Hash mismatch is a hard failure with no automatic update.
- Missing provenance evidence is a decision blocker, not an invitation to infer metadata from filenames.

### Completion evidence and handoff

Record:

- Starting and completion refs.
- Authored/vendor classification rules and exceptions.
- Corrected operational defaults and syntax checks run.
- Full provenance inventory and how each immutable source was verified.
- Any unavailable local platform tooling that `PR-60` must exercise.
- Any artifact decision blockers.

Implementation handoff (2026-08-13):

- Starting and completion references are the current working changeset pending
  maintainer commit.
- Authored executable/config files exclude `references/` and `assets/` vendor or
  fixture content. Checks cover developer homes, fixed temporary outputs,
  case-fold collisions, UTF-8/line endings, Git executable modes, Bash syntax,
  and Node syntax.
- The COM trace default uses `GetTempPath()` plus a GUID. Koppeling hydration is
  pinned to and verifies commit `c2eafe11e6c31e1f64438a88d283ce3b0e4536a8`.
- `tools/maintenance/provenance.toml` inventories all ten tracked PE artifacts
  with SHA-256, immutable source/package references, build descriptions, and
  license-evidence URLs. The NetClone entry explicitly records that exact
  reproducible equivalence of the local build has not been independently proven.
- Thirteen focused tests and the aggregate gate passed. PowerShell and
  PSScriptAnalyzer were unavailable locally and are delegated to PR-60 Windows CI.

Update the status table and this packet's status before finishing.

---

<a id="pr-60"></a>

## PR-60 — Core CI enforcement

Status: `in-progress`; local implementation and policy tests are complete. Hosted
Linux and Windows workflow evidence remains pending. Deferred PR-10 and PR-20
checks will join the gate when those packets resume.

Findings addressed: CI enforcement portion of finding 7.

Depends on: the current blocking offline-quality packets (`PR-30`, `PR-40`, and
`PR-50`). `PR-10` and `PR-20` remain required for the program-level definition of
done but are not prerequisites for establishing the initial CI gate.

May run in parallel with: none. Integrate only after the local baseline is green.

Expected starting ref: a ref containing every completed prerequisite.

### Fresh-context brief

Add required, least-privilege GitHub Actions checks that execute the same `just` recipes maintainers already run locally. Core pull-request validation must remain offline after pinned dependency installation, upload no sensitive reports, perform no repository writes, and include authoritative PowerShell coverage in addition to the primary Linux quality job.

### Read first

- `justfile` and every file under `tools/maintenance/just/`.
- `tools/maintenance/pyproject.toml`, `tools/maintenance/uv.lock`, and `tools/maintenance/.python-version`.
- All maintenance checks/tests and their tool requirements.
- The final handoff notes from `PR-10`, `PR-20`, `PR-30`, `PR-40`, and `PR-50`.
- Any existing files under `.github/workflows/` at execution time.

### Baseline evidence

- The original repository had no CI workflow enforcing plugin, skill, generated-file, link, redaction, snapshot, portability, or provenance checks.
- Local environments may lack `uv`, ShellCheck, PowerShell, and PSScriptAnalyzer.
- Activity-report source data is sensitive and must not become a CI artifact.
- Network refresh and external-link checks are intentionally excluded from the ordinary offline gate.

### Decisions already made

- GitHub Actions is the initial CI platform because the repository is hosted on GitHub.
- CI installs pinned tools/dependencies, then runs repository-owned `just` recipes. It does not duplicate validator command internals in YAML.
- `just ci` invokes the same offline aggregate as `just check`.
- Core workflow permissions are read-only, checkout credentials are not persisted, and ordinary jobs receive no write token.
- Every third-party action is pinned to a full immutable commit SHA, with the human-readable release tag/version in a comment.
- Activity reports are never uploaded and CI never invokes `--include-sensitive`.
- Network refresh, upstream drift, and external links belong to `PR-70`, not PR validation.
- Branch-protection activation is an external maintainer action after the workflow proves green; this packet documents it but does not assume authority to change repository settings.

### In scope

- Add `.github/workflows/quality.yml` for pull requests and pushes to the default branch.
- Add a Linux quality job that selects Python 3.13, installs pinned `uv`/`just` and locked dependencies, then runs `just ci`.
- Add an authoritative Windows/PowerShell job that runs the repository's PowerShell parser/static-analysis recipe.
- Add any narrowly justified portability smoke job required by `PR-50` handoff evidence.
- Set explicit `contents: read` or narrower permissions, `persist-credentials: false`, job timeouts, and concurrency cancellation.
- Prevent accidental execution of networked or mutating recipes from the core workflow through a repository-owned workflow-policy check.
- Validate workflow YAML, action pinning, permissions, sensitive flags, and allowed recipe invocations through maintenance tests.
- Ensure failures produce useful logs without uploading generated reports or secret-containing fixtures.
- Document the required-check names and manual branch-protection activation step.

### Out of scope

- Scheduled workflows.
- External-link checks or upstream BloodHound access.
- Automatic fixes, commits, pull requests, releases, or issues.
- Repository write permissions.
- Changing branch-protection settings through an external API.
- Uploading activity reports or unsafe fixture output.

### Owned and shared paths

Normally owned:

- `.github/workflows/quality.yml`
- Workflow-policy validators and fixtures.
- `tools/maintenance/just/ci.just`
- Focused CI/maintainer documentation.

Shared integration paths:

- `justfile` only if the stable import contract cannot expose `just ci`; prefer the existing recipe fragment.
- Locked external-tool metadata if the repository records non-Python CI tools centrally.

Do not change implementation checks merely to accommodate CI. If a local command is not CI-safe, fix its owning command contract or return the packet to its owner.

### Required implementation

- [x] Make `just ci` delegate to the complete offline `just check` gate.
- [x] Pin every action and tool version immutably.
- [x] Use Python 3.13 and `uv sync --frozen`/locked equivalent.
- [x] Disable persisted checkout credentials.
- [x] Set least-privilege permissions, timeouts, and concurrency cancellation.
- [x] Run PowerShell validation where the tool is present and fail on parser/static-analysis errors.
- [x] Add policy tests rejecting `--include-sensitive`, `refresh-*`, `generate-*`, external-link, and upstream-network recipes in core workflow steps.
- [x] Ensure no job uploads activity reports or broad workspace artifacts.
- [x] Test the workflow policy against deliberately unsafe fixtures.
- [x] Document exact required job/check names for maintainers.

### Acceptance commands and outcomes

Local validation:

```text
git rev-parse HEAD
git status --short
just doctor
just test workflows
just validate workflows
just ci
just check
git status --short
```

CI validation:

- Open or update a test pull request through the maintainer's normal workflow.
- Confirm the Linux quality and Windows PowerShell jobs both execute the intended `just` recipes and pass.
- Confirm jobs have no write permission and create no report artifacts.
- Confirm cancellation works for a superseded run.

Required outcomes:

- `just ci` and `just check` cover the same offline checks.
- All action references are immutable and workflow permissions are read-only.
- Core CI invokes no refresh, generate, upstream, or external-link command.
- PowerShell coverage deferred by `PR-50` is executed successfully.
- The workflow is green before maintainers make it required.

### Failure and rollback behavior

- Do not weaken a repository check to make CI green. Return the failure to its owning packet.
- Do not grant write permission to solve checkout, cache, or reporting problems.
- Do not upload broad debug archives on failure; logs must exclude synthetic secret values and activity reports.
- A missing platform tool must fail setup clearly rather than silently skip an authoritative CI job.

### Completion evidence and handoff

Record:

- Starting and completion refs.
- Action/tool versions and immutable pins.
- Workflow permissions and job names.
- Local `just ci` result and links/references to successful Linux and Windows runs.
- Confirmation that sensitive/mutating/network command policy tests pass.
- Manual branch-protection step still required from maintainers.

Local implementation handoff (2026-08-13):

- Starting and implementation references are the current working changeset
  pending maintainer commit.
- `just ci` delegates to `just check`. The workflow uses checkout v4.2.2 and
  setup-python v5.4.0 pinned to full commits, Python 3.13, uv 0.12.3, Just
  1.51.0, PSScriptAnalyzer 1.24.0, read-only permissions, credential-free
  checkout, job timeouts, and superseded-run cancellation.
- Intended required check names are `Linux quality` and `Windows PowerShell`.
  Ten workflow-policy tests reject mutable actions, write permissions,
  persisted credentials, uploads, sensitive flags, and mutating/networked recipes.
- The local `just ci` gate passes with 76 tests and is equivalent to `just check`.
  Hosted Linux/Windows run links and branch-protection activation remain external
  maintainer steps; keep this packet in progress until both jobs are observed green.

Update the status table and this packet's status before finishing.

---

<a id="pr-70"></a>

## PR-70 — Scheduled network maintenance

Status: `blocked` pending `PR-60`.

Findings addressed: scheduled maintenance portion of finding 7.

Depends on: `PR-60`.

May run in parallel with: none in this roadmap.

Expected starting ref: the completion ref of `PR-60`.

### Fresh-context brief

Add explicitly networked, non-mutating scheduled maintenance for external-link health and upstream BloodHound drift. Keep these checks separate from required PR validation, bounded against flaky services, least-privilege, and report-only until maintainers deliberately authorize automated update workflows.

### Read first

- `.github/workflows/quality.yml` and its workflow-policy tests from `PR-60`.
- Internal-link implementation and handoff from `PR-40`.
- BloodHound refresh/upstream adapters and handoff from `PR-20`.
- `tools/maintenance/exceptions.toml`.
- Root `justfile` and `tools/maintenance/just/ci.just`/`bloodhound.just`/`hygiene.just`.

### Baseline evidence

- External links can fail transiently and require network access, so they are inappropriate for deterministic PR checks.
- BloodHound snapshots are pinned, but maintainers need visibility when upstream commits advance.
- No scheduled workflow currently reports either condition.
- Automatic refresh commits would introduce supply-chain and review risk beyond the requested maintenance scope.

### Decisions already made

- Scheduled checks are separate from `just check` and are not required PR checks.
- `check-external-links` and `check-upstream-bloodhound` may use the network but never modify tracked files.
- Upstream drift reports commit differences; it does not fetch and install refreshed snapshots.
- External-link checks use bounded timeouts/retries, identify redirects separately, and support exact owned exceptions with review dates.
- Scheduled workflows use read-only permissions and no repository write token.
- Initial reporting is through job summaries/logs and ordinary failed scheduled runs. Do not open issues or pull requests automatically.

### In scope

- Add a networked external-link checker reusing the Markdown discovery rules from `PR-40`.
- Add bounded concurrency, user agent, timeout, retry/backoff, redirect policy, and deterministic result grouping.
- Respect exact external-link exceptions with owner and expiration.
- Expose the BloodHound non-mutating upstream-status command as `just check-upstream-bloodhound`.
- Add `.github/workflows/scheduled-maintenance.yml` with a weekly schedule and manual `workflow_dispatch`.
- Run external-link and BloodHound drift jobs independently so one result does not obscure the other.
- Pin actions/tools, use timeouts/concurrency cancellation, and retain read-only permissions.
- Add mocked tests for success, redirect, timeout, retry, rate limit, expired exception, and upstream drift responses.
- Document the manual commands maintainers use to investigate and, separately, perform an authorized refresh.

### Out of scope

- Adding these network checks to `just check` or required PR validation.
- Automatically running `refresh-bloodhound`.
- Committing changes, opening pull requests/issues, or granting write permissions.
- Treating every redirect as broken without policy.
- Adding credentials for private external sites.

### Owned and shared paths

Normally owned:

- `.github/workflows/scheduled-maintenance.yml`
- External-link network adapter, tests, and fixtures.
- Scheduled/upstream recipe additions in their predefined recipe fragments.
- Focused scheduled-maintenance documentation.

Shared integration paths:

- `tools/maintenance/exceptions.toml` for exact external-link exceptions.
- Existing BloodHound code only if the `PR-20` handoff lacks the promised non-mutating upstream adapter.

Do not modify core `quality.yml` except to repair a proven policy-test interaction.

### Required implementation

- [ ] Keep all network calls out of the aggregate offline check registry.
- [ ] Test network behavior with mocked transports; ordinary unit tests must remain offline.
- [ ] Bound request concurrency, retries, redirects, response size, and total job duration.
- [ ] Group failures by domain/status and print the originating repository path.
- [ ] Report expired exceptions as failures.
- [ ] Compare current pinned BloodHound commits to resolved upstream commits without writing snapshots or manifests.
- [ ] Use read-only workflow permissions and immutable action/tool pins.
- [ ] Provide manual `workflow_dispatch` without accepting an unsafe auto-refresh input.
- [ ] Document that a maintainer reviews drift and runs `just refresh-bloodhound` separately when authorized.

### Acceptance commands and outcomes

Offline tests and workflow policy:

```text
git rev-parse HEAD
git status --short
just test external-links
just test bloodhound-upstream
just validate workflows
just check
git status --short
```

Explicit network smoke tests, run only when authorized and connectivity is available:

```text
just check-external-links
just check-upstream-bloodhound
```

Required outcomes:

- Offline aggregate checks remain offline and non-mutating.
- Network commands never alter the worktree.
- Mocked tests cover transient and permanent failure behavior.
- The scheduled workflow has read-only permissions and runs the two checks independently.
- A manual scheduled run reports results without commits, pull requests, issues, or unsafe artifacts.

### Failure and rollback behavior

- Network failures report an indeterminate/transient state distinctly from a confirmed missing resource.
- Bounded retries must not turn the workflow into an unbounded wait.
- Upstream drift never triggers refresh automatically.
- If a site requires credentials or bot-specific access, report it and use a narrow reviewed exception; do not add secrets under this packet.

### Completion evidence and handoff

Record:

- Starting and completion refs.
- Schedule, permissions, action pins, request bounds, and exception policy.
- Mocked test results and one authorized manual workflow result when available.
- External-link and upstream-drift findings at completion time as observations only.
- Any future automation proposals left explicitly out of scope.

Update the status table and this packet's status before finishing.

---

## Program-level definition of done

The maintenance program is complete only when all packets are `complete` and the following statements are true:

- A fresh clone with approved prerequisites passes `just setup && just check`.
- After setup, `just check` uses no network, is deterministic, and changes no repository file.
- `just ci` invokes the same offline gate, and required Linux and PowerShell jobs are green with read-only permissions.
- Running any offline generator twice from unchanged inputs produces no second diff.
- Removing or renaming a skill, agent, manifest, ownership entry, catalog declaration, or declared resource fails with a path-specific diagnostic.
- Both supplied course configurations parse through the runtime-equivalent loader and satisfy their schema.
- Default activity reports contain none of the synthetic canaries from any supported source; unsafe output requires explicit visible opt-in and is absent from CI.
- BloodHound indexes are byte-reproducible, preserve empty descriptions, classify the AD `AZUREADKERBEROS` regression correctly, and survive refresh failure unchanged.
- No installable plugin is an empty shell; the four named incubating plugins cannot be installed as active capabilities.
- Generated catalogs and marked README regions match canonical metadata and preserve intended platform differences.
- All unexcepted first-party internal links and bundled-resource references resolve.
- No first-party operational default contains a developer-specific home path.
- Every tracked executable asset in scope has verified, non-fabricated provenance and digest metadata.
- External-link and upstream-drift checks run separately on a read-only schedule and never update the repository automatically.

## Maintainer decisions that remain external

The automation can surface these issues but cannot decide them:

- Repository and plugin licensing policy.
- Whether an artifact with unverifiable provenance should be removed, replaced, or retained under a documented risk acceptance.
- Promotion of an incubating plugin after a real capability is added.
- Enabling required branch protection after CI is proven green.
- Authorizing a future bot to open refresh pull requests or issues.
