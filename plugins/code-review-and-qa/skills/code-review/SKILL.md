---
name: code-review
description: Security-focused code review of current git changes. Use when reviewing code diffs, checking for vulnerabilities, or before merging branches.
icon: ./assets/icon.png
---

# Security-Focused Code Review

Review current git changes with a focus on security issues and code quality.

Parse the user's input to determine scope:
- `$code-review` → review all changes (staged + unstaged)
- `$code-review staged` → only staged changes
- `$code-review unstaged` → only unstaged changes

## Steps

1. Determine scope from user input (default: all)
   - staged: `git diff --staged`
   - unstaged: `git diff`
   - all: both `git diff` and `git diff --staged`

2. Run `git status` for the full picture

3. Read the full content of each changed file for context (not just the diff)

4. Analyze for:

### Security Issues (Critical)
- **Injection**: SQL injection, command injection, XSS, SSTI, LDAP injection
- **Hardcoded secrets**: API keys, passwords, tokens, connection strings, private keys
- **Path traversal**: unsanitized file path inputs, `../` patterns
- **Insecure deserialization**: pickle, yaml.load without SafeLoader, json with custom decoders
- **Weak crypto**: MD5/SHA1 for security, ECB mode, hardcoded IVs, insufficient key lengths
- **SSRF**: unvalidated URLs in HTTP requests, DNS rebinding potential
- **Race conditions**: TOCTOU, shared state without locks, async hazards
- **Auth issues**: missing auth checks, privilege escalation, IDOR patterns
- **CORS misconfiguration**: overly permissive Access-Control-Allow-Origin, credentials with wildcard
- **JWT issues**: algorithm confusion (none/HS256 vs RS256), missing expiration, weak secrets

### Logic & Correctness
- Off-by-one errors, boundary conditions
- Unhandled error cases that could crash or leak info
- Resource leaks (unclosed files, connections, sockets)
- Incorrect type handling

### Code Quality
- Overly complex logic that could hide bugs
- Missing input validation at trust boundaries
- Inconsistent error handling patterns

5. Present findings by severity:
   - CRITICAL: Exploitable security vulnerabilities
   - HIGH: Security weaknesses, data exposure risks
   - MEDIUM: Logic bugs, error handling gaps
   - LOW: Style issues, minor improvements

6. Each finding includes: file:line, issue, why it matters, suggested fix

7. Summary: total by severity, verdict (safe to merge / needs fixes / needs rework)
