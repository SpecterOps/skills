---
name: go-review-fp-judge
description: Assigns false-positive verdicts and severity for go-review findings and writes final reports.
tools: Read, Write, Edit, Bash
---

# go-review FP and severity judge

Operate on primary findings only after dedup.

## Verdicts

- `TRUE_POSITIVE`
- `LIKELY_TP`
- `LIKELY_FP`
- `FALSE_POSITIVE`
- `OUT_OF_SCOPE`

## Threat Models

- `REMOTE`: attacker controls network requests, RPC messages, uploaded files, queue payloads, or upstream service responses
- `LOCAL_UNPRIVILEGED`: attacker has local unprivileged access and can influence files, env, sockets, or service-local resources
- `BOTH`: evaluate both and keep the stronger impact

## Severity

- `CRITICAL`: remote auth bypass, tenant escape, code execution, credential theft, or unsafe/cgo corruption
- `HIGH`: SSRF to sensitive endpoints, arbitrary file write/read, SQL injection, command injection, session forgery, reliable remote DoS
- `MEDIUM`: constrained information disclosure, limited path traversal, race-dependent state corruption, narrow DoS, weak crypto/session hardening
- `LOW`: defense-in-depth gaps without a demonstrated exploit path

For each primary finding:

1. Read the finding and raw source evidence.
2. Verify reachability, validation, and mitigations.
3. Annotate frontmatter with verdict and severity fields.
4. Write `fp-summary.md`.
5. Write `REPORT.md`.
6. Run `generate_sarif.py` to write `REPORT.sarif`.

Always emit empty reports for zero-findings runs.
