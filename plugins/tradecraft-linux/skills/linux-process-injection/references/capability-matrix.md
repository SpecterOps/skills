# Linux Process Injection Capability Matrix

Use this file for feasibility checks. Live-process methods modify an existing image; launch-time methods affect a new image during controlled `execve`.

## Overview

| Technique                 | Scope                         | Provides                                       | Key constraints                                                                                              |
| ------------------------- | ----------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `ptrace`                  | Existing image                | Memory and register access; per-thread control | `PTRACE_MODE_ATTACH_REALCREDS`; dumpability, capabilities, LSM/Yama; usually requires ptrace-stops           |
| `/proc/<pid>/mem`         | Existing image                | Remote memory access                           | Open uses `PTRACE_MODE_ATTACH_FSCREDS`; no implicit stop; non-writable VMA access depends on proc-mem policy |
| `process_vm_writev`       | Existing image                | Writes to writable remote memory               | `PTRACE_MODE_ATTACH_REALCREDS`; no register or stop control; partial and non-atomic writes                   |
| `LD_PRELOAD`              | Controlled launch or `execve` | Loader maps a shared object                    | Requires a compatible dynamic loader; static targets, secure execution, or sanitization can block it         |
| Seccomp user notification | Supervised launch             | Mediates selected syscalls and can inject FDs  | Child must install a listener before `execve`; requires supported seccomp operations and controlled launch   |

## Live-Process Primitive Coverage

| Primitive                      | `ptrace`  | `/proc/<pid>/mem`                           | `process_vm_writev`                |
| ------------------------------ | --------- | ------------------------------------------- | ---------------------------------- |
| Write writable memory          | Yes       | Yes                                         | Yes                                |
| Write RX memory                | Generally | Policy-dependent                            | No                                 |
| Modify saved PC/IP             | Yes       | No                                          | No                                 |
| Overwrite current instruction  | Yes       | Policy-dependent                            | Only in writable executable memory |
| Stack or ROP hijack            | Yes       | Yes                                         | Yes                                |
| GOT or function-pointer hijack | Yes       | Yes if writable; otherwise policy-dependent | Only if writable                   |
| Stop thread or write registers | Yes       | No                                          | No                                 |

A `Yes` means the primitive is available, not that staging, synchronization, execution transfer, or recovery is solved.

## Launch-Time Comparison

| Property          | Traditional `LD_PRELOAD`                                                 | seccomp-notify                                                                                           |
| ----------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| Setup             | Supply a shared object through a controlled preload request              | Launch a child, install a listener, pass it to the supervisor, then `execve`                             |
| Trigger           | Loader maps and initializes the object                                   | Loader calls filtered `openat`/`openat2`; supervisor supplies an FD with `SECCOMP_IOCTL_NOTIF_ADDFD`     |
| Main requirements | Dynamic target, compatible ABI and loader, honored preload configuration | Controlled launch, dynamic target for this PoC, filter-install permission, supported notification ioctls |
| Kernel dependency | No dedicated injection API                                               | User notification: 5.0; `ADDFD`: 5.9; `SECCOMP_ADDFD_FLAG_SEND`: 5.14                                    |
| Privilege effect  | Runs in the launched program's resulting security context                | Does not cross the target's UID, namespace, or LSM boundaries                                            |
| Cleanup           | Remove preload configuration and manage library side effects             | Manage staged FDs and the seccomp filter that survives `execve`                                          |

The PoC's `memfd`, loader-open substitution, and IFUNC resolver are implementation choices, not universal seccomp-notify requirements.

## Key Caveats

- All live methods use the ptrace access algorithm. `ptrace` and `process_vm_writev` use real credentials; `/proc/<pid>/mem` uses filesystem credentials.
- Yama may add restrictions: scope `0` adds none, `1` usually requires ancestry or `PR_SET_PTRACER`, `2` requires `CAP_SYS_PTRACE`, and `3` denies attach-gated access.
- Full RELRO blocks writable-only GOT modification. `ptrace` can generally write ordinary private mappings despite page protections; `/proc/<pid>/mem` depends on proc-mem override policy.
- Linux has no direct equivalents of `VirtualAllocEx`, `VirtualProtectEx`, or `CreateRemoteThread`; induce allocation, permission changes, or thread creation inside the target.
- ASLR, PIE, CET/shadow stacks, CFI, PAC, calling conventions, syscall restart behavior, and instruction-cache rules are platform-specific.
- Installing a seccomp listener without `CAP_SYS_ADMIN` in the relevant user namespace normally requires `PR_SET_NO_NEW_PRIVS`. Validate notification IDs before acting on target state.
