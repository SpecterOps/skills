---
name: linux-process-injection
description: Use this skill when the user asks about Linux process injection.
metadata:
  author: "Outflank"
---

# Linux Process Injection

## Overview

Start with [the capability matrix](./references/capability-matrix.md).

- Live process: modify an existing image with `ptrace`, `/proc/<pid>/mem`, or `process_vm_writev`. Use the model `overwrite -> execute -> recover`.
- Controlled launch or exec: arrange loading into a new image with `LD_PRELOAD` or seccomp user notification. These do not retrofit an arbitrary running image.

## Workflow

1. Classify the lifecycle. Decide whether the target is already running or launched under injector control.
2. Profile the target. Identify architecture, ABI, mappings, RELRO, thread state, loader/libc, kernel features, and mitigations.
3. Validate prerequisites. Check ptrace and LSM/Yama policy, loader behavior, or parent-child seccomp support as applicable.
4. Separate staging from execution. Identify both where bytes or objects are placed and how control reaches them.

## Method Rules

- Use `ptrace` for register control, thread stops, or the broadest live-process control.
- Treat `/proc/<pid>/mem` writes through non-writable mappings as kernel-policy dependent.
- Use `process_vm_writev` only for writable memory; verify byte counts and assume no atomicity.
- Treat `LD_PRELOAD` as controlled dynamic-loader behavior; static binaries, secure-execution mode, and environment sanitization can block it.
- Treat seccomp notification as syscall mediation, not remote memory or register control. The seccomp-notify PoC installs a listener before `execve` and substitutes a staged shared-object FD for a selected loader `openat` call.

## References

- [Capability matrix](./references/capability-matrix.md)
- [The Definitive Guide to Linux Process Injection](https://www.akamai.com/blog/security-research/the-definitive-guide-to-linux-process-injection)
- [akamai/Linux-Process-Injection](https://github.com/akamai/Linux-Process-Injection)
- [Seccomp Notify Injection](https://www.outflank.nl/blog/2025/12/09/seccomp-notify-injection/)
- [outflanknl/seccomp-notify-injection](https://github.com/outflanknl/seccomp-notify-injection)
