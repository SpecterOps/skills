---
name: cwe-code-review
description: Perform CWE-grounded security code reviews and precise weakness mapping using a locally derived MITRE CWE corpus, relationship graphs, mapping notes, detection methods, mitigations, and schema semantics. Use when Codex needs to audit source code or pull requests, identify root-cause weakness classes, distinguish broad symptoms from mappable CWEs, justify CWE IDs in findings, or review code against CWE views such as Software Development, Research Concepts, Top 25, OWASP, language-specific, or AI/ML weakness sets.
---

# CWE Code Review

Use this skill for manual security review when the result needs defensible CWE mapping, not just a list of suspicious patterns. Prefer a narrower language, framework, CI, cloud, or infrastructure review skill when one clearly fits; use this skill to add CWE precision and cross-cutting review logic.

## Review Principles

- Start from architecture, trust boundaries, attacker-controlled inputs, sensitive assets, and reachable sinks.
- Confirm a code path before assigning a CWE. A keyword match or a dangerous API alone is not a finding.
- Use CWE as a root-cause taxonomy. Prefer the most precise supported weakness over a broad Pillar, Class, Category, or View.
- Treat mapping notes as part of the evidence. `Allowed` and `Allowed-with-Review` entries are usually better finding mappings than `Discouraged` or `Prohibited` entries.
- Use Top 25, OWASP, language, and lifecycle views for coverage and prioritization context, not as severity proof.
- Keep unsupported hypotheses as open questions or coverage gaps instead of forcing a CWE mapping.
- Always create or update one standalone `poc_<finding_slug>.py` artifact per confirmed finding in the review workspace, with exploit prerequisites and validation steps for that finding.

## References

- Read [references/cwe-catalog-summary.md](references/cwe-catalog-summary.md) first for source metadata, corpus shape, mapping cautions, and the review-oriented view table.
- Read [references/cwe-review-views.md](references/cwe-review-views.md) when scoping a review by software-development, research, Top 25, OWASP, language, lifecycle, mobile, or AI/ML views.
- Search [references/cwe-weakness-index.md](references/cwe-weakness-index.md) when you need a fast grep-friendly catalog scan.
- Read [references/cwe-schema-guide.md](references/cwe-schema-guide.md) when interpreting fields such as `Abstraction`, `Structure`, `Status`, `Mapping_Notes`, relationship nature, detection effectiveness, or mitigation strategy.
- Use [references/cwe-records.jsonl](references/cwe-records.jsonl) through `scripts/cwe_lookup.py` rather than loading the full corpus into context.
- Use [references/cwe-catalog-metadata.json](references/cwe-catalog-metadata.json) when you need machine-readable view or category metadata.

## Lookup Workflow

Resolve this skill directory, then use the lookup helper from that directory:

```bash
python3 scripts/cwe_lookup.py --query "server-side request forgery"
python3 scripts/cwe_lookup.py --id 918
python3 scripts/cwe_lookup.py --id CWE-79 --full
python3 scripts/cwe_lookup.py --view 1435 --limit 30
python3 scripts/cwe_lookup.py --phase Implementation --functional-area Authorization --limit 20
python3 scripts/cwe_lookup.py --impact "Execute Unauthorized Code or Commands" --mapping Allowed --limit 20
```

Use `--query` to discover candidates, then `--id` to read the mapping notes, relationships, consequences, detection methods, and mitigations before naming a CWE in a finding.

## Review Process

1. Build a threat model and code inventory.
   - Identify components, entry points, identities, privilege levels, data stores, external integrations, sensitive assets, and deployment boundaries.
   - Record attacker-controlled inputs, security decisions, and trust assumptions.

2. Trace security-relevant paths.
   - Follow untrusted data to queries, templates, files, archives, URLs, deserializers, process execution, logs, caches, and client responses.
   - Follow identity, authorization, session, secret, cryptographic, and business-state decisions through alternate routes and asynchronous handlers.
   - Record controls, normalization, validation, encoding, authorization checks, failure behavior, and privilege transitions.

3. Discover candidate weaknesses.
   - Query by sink, violated control, impact, lifecycle phase, or functional area.
   - Use view references to widen coverage when the repository exposes a relevant language, platform, lifecycle, OWASP, Top 25, mobile, or AI/ML surface.
   - Use parent and child relationships to move from broad symptoms toward a precise root cause.

4. Validate the mapping.
   - Read the candidate record with `--id`.
   - Check `Abstraction`, `Status`, `Mapping Usage`, mapping rationale, relationship context, and suggestions.
   - Prefer Base or Variant entries when the evidence supports them. Use Compound entries when the exploit requires the combined condition.
   - Avoid mapping a finding to a Category or View. Avoid a Pillar or broad Class when a supported child weakness matches the actual failure.
   - If the best entry is `Allowed-with-Review`, state why the code path fits that entry. If the best visible entry is `Discouraged` or `Prohibited`, keep searching or explain the mapping gap.

5. Report only confirmed findings.
   - Tie each finding to file and line references, attacker influence, the missing or incorrect control, reachable impact, and a focused remediation.
   - Name one primary CWE mapping per finding. Mention secondary CWE relationships only when they explain a distinct contributing weakness or attack chain.
   - Include concise syntax-highlighted code blocks for the affected source or configuration sections that establish the input, missing control, sensitive sink, or authorization decision.
   - Include a regression test or validation step that would fail before the fix and pass after it.

6. Build the PoC artifacts.
   - Create or update one standalone `poc_<finding_slug>.py` file in the review workspace for each confirmed finding.
   - Do not combine unrelated findings into one harness unless the user explicitly asks for a consolidated runner.
   - Make each path incremental: print or implement numbered steps for prerequisites, authentication or material acquisition, trigger, impact verification, and cleanup guidance.
   - State attacker position, required permissions, credentials or certificates, environmental dependencies, and any unproven prerequisite before sending requests.
   - Default to dry-run or harmless markers and require an explicit flag for state-changing validation. Do not overclaim impact when a later exploit step remains unproven.
   - If a confirmed finding has no runnable path, still create its per-finding PoC scaffold and explain the missing prerequisite or why exploitation was not confirmed.

## PoC Artifacts

Per-finding PoC scripts are part of the review output, not an optional appendix. Each script should help another reviewer reproduce one finding without reconstructing the exploit chain from prose.

- Prefer standalone standard-library scripts named `poc_<finding_slug>.py`. Duplicating small amounts of transport or auth plumbing is acceptable when it keeps each PoC independently runnable.
- Keep requirements discoverable through `python3 poc_<finding_slug>.py --requirements` or equivalent help text.
- Model chained findings explicitly. If one finding yields the credential or primitive required by another, state the dependency and expose the steps separately.
- Use safe default destinations, fake secrets, and non-destructive checks where they still prove the root cause. Put stronger impact demonstrations behind explicit arguments and document the side effects.
- Validate each script locally with syntax checks and dry runs, then record which live steps were and were not executed.

## Finding Standard

Lead with findings ordered by severity. For each finding include `Severity`, `Location`, `Issue`, `CWE`, `Evidence`, `Exploit Path`, `Impact`, `Remediation`, and `Test`.

For `CWE`, include the identifier, name, and one sentence explaining why that entry is the precise root-cause mapping. Note `Allowed-with-Review` caveats when applicable.

For `Evidence`, include line-scoped fenced code blocks with an appropriate language tag such as `python`, `go`, `javascript`, `yaml`, `json`, `nginx`, `bash`, or `sql`. Put the source path and line range immediately above each block. Keep excerpts narrow enough to show the relevant control flow without dumping whole modules, and include supporting configuration blocks when they are part of the exploit path.

For each finding, also include `PoC Requirements` and reference the corresponding `poc_<finding_slug>.py` artifact and step sequence.

After findings, include `Open Questions / Assumptions` and `Coverage`. If no confirmed findings exist, say so explicitly and still state the reviewed surfaces, unresolved risks, test gaps, and that no per-finding PoC artifacts were created.

## Regeneration

Rebuild the derived corpus when a newer CWE catalog or schema is provided:

```bash
python3 scripts/build_cwe_references.py \
  --catalog /path/to/cwec.xml \
  --schema /path/to/cwe_schema.xsd
```

Keep the generated references aligned with the source catalog and schema version recorded in `references/cwe-catalog-summary.md`.
