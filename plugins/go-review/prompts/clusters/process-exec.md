---
cluster_id: process-exec
consolidated: true
---

# Process Execution Review

Inventory `os/exec`, shell invocations, environment construction, PATH lookup,
working directories, and any request/file data that reaches commands.

## Passes

| Prefix | Bug class | Look for |
|--------|-----------|----------|
| CMDI | command-injection | attacker-controlled input reaches shell, command, or argument construction unsafely |
| PATHENV | path-env-hijack | privileged commands rely on attacker-controlled PATH, env, cwd, or executable resolution |
| SHELL | unsafe-shell-invocation | `sh -c`, `bash -c`, PowerShell, or shell wrappers used where direct argv execution is required |

Differentiate direct `exec.Command(name, args...)` from shell interpretation.
