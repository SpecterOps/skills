---
name: webapp-review
description: Web application security testing workflow and checklist generation. Use when planning or executing web app assessment steps, including auth, API, injection, and configuration testing.
icon: ./assets/icon.png
---

# Webapp Review

Generate structured web security test plans and, when requested, execute active tests.

## Input Parsing

Accept input as: `TARGET [SCOPE] [MODE]`

Scopes:
- `full` (default)
- `auth`
- `api`
- `injection`
- `config`

Modes:
- `plan`: checklist + suggested commands only
- `execute` (default, preferred): run test commands

If mode is omitted, default to `execute`.

Examples:
- `$webapp-review https://app.example.com`
- `$webapp-review https://api.example.com api`
- `$webapp-review https://app.example.com full execute`
- `$webapp-review auth`

## Execution Policy

- Always produce a checklist and suggested commands first.
- If mode is `execute`, run routine in-scope command batches autonomously.
- Request approval only for OPSEC-dangerous command batches.
- Before OPSEC-dangerous active tests, provide short OPSEC warning (noise + detection surfaces).

## Workflow

1. Create output directory and report path:
   - `mkdir -p recon/`
   - report: `recon/webapp-<target-slugified>.md`
2. If source code exists locally, inspect it for framework/auth/input patterns.
3. Build checklist for selected scope (or full set).
4. Add concrete command suggestions for each relevant test area.
5. If `execute` mode is requested:
   - run routine in-scope commands autonomously,
   - request approval only for OPSEC-dangerous steps,
   - capture and summarize outputs in the report.
6. Save report and provide next-step recommendations.

## Checklist Areas

### Authentication and Session

- default/weak credentials
- brute-force protections and lockout
- session fixation/timeout/invalidation
- JWT validation weaknesses
- OAuth/OIDC misconfiguration
- MFA bypass paths

### Authorization

- IDOR (horizontal access)
- vertical privilege escalation
- function-level authorization gaps
- parameter tampering and role abuse
- API authorization consistency

### Injection

- SQL/NoSQL injection
- command injection
- SSTI
- LDAP/XPath injection
- header injection (CRLF)

### Client-Side

- reflected/stored/DOM XSS
- CSP and client-side hardening gaps
- prototype pollution opportunities

### SSRF and External Interaction

- unvalidated URL fetchers
- metadata service access
- webhook/callback abuse
- internal service pivot risk

### File Handling

- unsafe upload validation
- path traversal in file operations
- XXE and parser abuse
- local/remote file include patterns

### Configuration and Infrastructure

- verbose errors and stack traces
- directory listing and debug endpoints
- security headers and cookie flags
- CORS policy issues
- TLS weaknesses

### Business Logic

- race conditions and double-spend flows
- workflow bypasses
- mass assignment and parameter pollution
- missing rate limits

## Suggested Command Patterns

Prefer target-safe, bounded commands and annotate intent:

```bash
# HTTP probe and fingerprint
curl -isk <target>

# Endpoint/content discovery
ffuf -u <target>/FUZZ -w <wordlist> -mc 200,301,302,403

# API/security template checks
nuclei -u <target> -tags cves,misconfig,exposure

# Parameter fuzzing baseline
ffuf -u '<target>?id=FUZZ' -w <payloads>

# Optional sqlmap quick triage (approval only if OPSEC-dangerous in this context)
sqlmap -u '<target>?id=1' --batch --risk=1 --level=1
```

## Output Format

```markdown
# Webapp Security Review ? <target>
## Scope: <scope>
## Mode: <plan|execute>

## Executive Summary
- High-level risk overview

## Checklist
- [ ] Item

## Suggested Commands
- command + purpose

## Executed Commands and Results
- command
- key output
- interpretation

## Prioritized Next Steps
1. next action
2. next action
```

## Quality Rules

- Keep findings evidence-based and reproducible.
- Separate confirmed findings from hypotheses.
- Include exact commands and relevant output snippets for executed tests.
