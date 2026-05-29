---
name: finding-report
description: Generate a structured pentest finding report in markdown. Use when documenting a vulnerability, writing up a finding, or creating engagement notes.
metadata:
  author: "GhostWorks"
---

# Pentest Finding Report

Generate a structured markdown finding report suitable for inclusion in a professional penetration test report.

Parse the user's input to determine the finding title and severity:
- `$finding-report "Kerberoastable Service Account with Path to DA"` → create finding with default High severity
- `$finding-report "Open S3 Bucket" --severity critical` → create finding with specified severity
- `$finding-report` → ask for a title

## Steps

1. Create the output directory if it doesn't exist (`mkdir -p findings/`) and create a new file at `findings/<title-slugified>.md` (convert title to kebab-case)

2. Use this template structure:

```markdown
# [Title]

| Field | Value |
|---|---|
| **Severity** | [Critical/High/Medium/Low/Info] |
| **CVSS 3.1** | [Score] ([Vector String]) |
| **CWE** | [CWE-ID: Name] |
| **Affected Asset(s)** | [hosts, URLs, or services] |
| **Status** | Open |

## Description

[2-3 sentences explaining what the vulnerability is and where it exists. Be specific about the affected component.]

## Impact

[What can an attacker achieve by exploiting this? Be concrete — data exposure, lateral movement, privilege escalation, etc.]

## Evidence

[Screenshots, command output, or proof. Use fenced code blocks for command output.]

```
[command or request used]
```

```
[response or output showing the vulnerability]
```

## Reproduction Steps

1. [Step-by-step instructions to reproduce]
2. [Be specific enough that another tester could verify]
3. [Include exact commands, URLs, parameters]

## Remediation

**Short-term**: [Immediate mitigation]

**Long-term**: [Root cause fix]

## References

- [Relevant CVE, blog post, or documentation]
```

3. Fill in the template based on the information provided. If information is missing, insert `[TODO: ...]` placeholders

4. For CVSS scoring, calculate based on the described impact:
   - Network-accessible + no auth + high impact = Critical (9.0+)
   - Requires auth or local access + high impact = High (7.0-8.9)
   - Limited impact or requires chaining = Medium (4.0-6.9)
   - Minor information disclosure = Low (0.1-3.9)

5. Map to appropriate CWE IDs (common ones):
   - SQL Injection: CWE-89
   - XSS: CWE-79
   - Command Injection: CWE-78
   - Path Traversal: CWE-22
   - SSRF: CWE-918
   - Broken Auth: CWE-287
   - IDOR: CWE-639
   - Weak Crypto: CWE-327
   - Kerberoasting: CWE-916
   - ACL Misconfiguration: CWE-732
   - Certificate Template Abuse: CWE-295

6. Report the file path back to the user
