---
name: security-review
description: Perform a security-focused review of current git changes. Use when reviewing staged/unstaged diffs, checking for vulnerabilities, and deciding merge readiness.
metadata:
  author: "GhostWorks"
---

# Security Review

Review local git changes with emphasis on exploitability, trust boundaries, and safe-by-default behavior.

## Input Parsing

Accept input as: `SCOPE`

Supported scopes:
- `all` (default): staged and unstaged changes
- `staged`: only staged changes
- `unstaged`: only unstaged changes

Examples:
- `$security-review`
- `$security-review staged`
- `$security-review unstaged`

## Review Workflow

1. Determine scope:
   - staged: `git diff --staged`
   - unstaged: `git diff`
   - all: both
2. Run `git status` for context.
3. Read full changed files (not only hunks) to catch cross-function issues.
4. Analyze findings by categories below.
5. Report findings ordered by severity with actionable fixes.
6. Provide merge verdict (`safe to merge`, `needs fixes`, `needs rework`).

## Security Categories

- Injection risks: SQL/command/LDAP/template/XSS paths.
- Secrets exposure: API keys, credentials, tokens, private keys, connection strings.
- Path/file handling: traversal, unsafe joins, arbitrary read/write.
- Insecure deserialization: unsafe loaders, implicit object decoding.
- Crypto misuse: weak algorithms, static keys/IVs, incorrect modes.
- SSRF/open redirect: unvalidated URLs or callback targets.
- AuthN/AuthZ flaws: missing checks, IDOR, privilege escalation.
- Session/JWT issues: weak secrets, missing expiry/validation, algorithm confusion.
- CORS and headers: overly permissive policies, missing protective headers.

## Correctness and Reliability

- Boundary and off-by-one issues.
- Error handling gaps that leak sensitive details.
- Resource lifecycle leaks.
- Concurrency/race condition hazards.

## Reporting Format

For each finding include:
- `severity`
- `file:line`
- `issue`
- `impact`
- `recommended fix`

Then include:
- total findings by severity
- overall merge verdict

## Quality Rules

- Focus findings first; keep summary brief.
- Avoid speculative claims without code evidence.
- Prefer concrete fix guidance over generic advice.
