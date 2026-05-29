---
name: secret-scan
description: Scan repositories and codebases for exposed secrets, credentials, and sensitive data. Use for GitHub repo/org/user scans, local code scans, and secret-discovery triage with optional command execution.
metadata:
  author: "GhostWorks"
---

# Secret Scan

Identify exposed secrets and sensitive material in approved targets.

## Input Parsing

Accept input as: `ACTION TARGET [MODE]`

Actions:
- `repo <owner/repo>`
- `org <org-name>`
- `user <username>`
- `dork <search phrase>`
- `local <path>`

Modes:
- `plan`: recommendations + command set only
- `execute` (default, preferred): run commands and report evidence

If mode is omitted, default to `execute`.

Examples:
- `$secret-scan repo owner/repo`
- `$secret-scan org acme-corp execute`
- `$secret-scan local ./src execute`
- `$secret-scan dork "Acme Corp"`

## Execution Policy

- Always generate a plan first.
- In `execute` mode, run routine in-scope command batches autonomously.
- Request approval only for OPSEC-dangerous command batches.
- Only scan authorized targets provided by the user.
- Capture exact commands and key output evidence in the report.

## Tool Preference

1. `trufflehog` (preferred)
2. `gitleaks`
3. manual grep-based fallback

Check availability:

```bash
which trufflehog
which gitleaks
which gh
```

## Workflow

1. Create output directory:
   - `mkdir -p recon/secret-scan/`
2. Build a target-specific command plan.
3. In `execute` mode:
   - run routine in-scope commands autonomously,
   - request approval only for OPSEC-dangerous steps,
   - collect outputs and triage.
4. Produce findings with severity and confidence labels.
5. Save report to:
   - `recon/secret-scan/<target-slug>-report.md`

## Command Patterns

### repo

```bash
# Preferred
trufflehog github --repo=https://github.com/<owner/repo> --only-verified --json

# Alternative
git clone --mirror https://github.com/<owner/repo> /tmp/secret-scan-target
gitleaks detect --source /tmp/secret-scan-target --report-format json --report-path recon/secret-scan/gitleaks.json
```

### org

```bash
gh repo list <org> --public --limit 200 --json name,url,pushedAt
trufflehog github --org=<org> --only-verified --json
```

### user

```bash
gh repo list <user> --public --limit 100 --json name,url,pushedAt
```

### dork

```bash
gh search code "<query>" --limit 20 --json repository,path,textMatches
```

### local

```bash
trufflehog filesystem <path> --json
# or
gitleaks detect --source <path> --report-format json --report-path recon/secret-scan/gitleaks-local.json
```

### manual fallback patterns

```bash
grep -RInE 'AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY|api[_-]?key|token|password\\s*[:=]' <path>
grep -RInE 'mongodb(\\+srv)?://|postgres(ql)?://|mysql://|redis://|amqp://' <path>
```

## Triage Rules

- Confirm whether value appears live/real vs placeholder/test string.
- Prioritize:
  1. active credentials and tokens,
  2. private keys/certs,
  3. database connection strings,
  4. internal endpoints and sensitive config.
- Avoid publishing raw secret values in final report unless explicitly required; use redaction where possible.

## Output Format

```markdown
# Secret Scan Report ? <target>
## Action: <repo|org|user|dork|local>
## Mode: <plan|execute>

## Executive Summary
- High-level findings and risk.

## Commands
- exact command
- execution status

## Findings
- secret type
- location (file/path/repo + line)
- confidence
- impact
- recommended response (rotate/revoke/remove/history rewrite)

## Next Steps
1. immediate containment
2. cleanup and hardening
3. verification rerun
```

## Quality Rules

- Keep findings evidence-based and reproducible.
- Separate confirmed secrets from unverified candidates.
- Include exact commands and output snippets for all executed steps.
