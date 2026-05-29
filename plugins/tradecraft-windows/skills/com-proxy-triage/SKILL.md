---
name: com-proxy-triage
description: Use this skill when the user wants to triage Windows COM proxy/hijack candidates by capturing `HKCU\Software\Classes\CLSID\{...}\InProcServer32` `NAME NOT FOUND` lookups for a process, mapping each CLSID to the machine-wide `HKLM\SOFTWARE\Classes\CLSID\{...}\InProcServer32` DLL, and optionally testing HKCU overrides with a Koppeling-style proxy DLL. Good for Zoom, Edge, and similar COM activation hunts.
metadata:
  author: "GhostWorks"
---

# COM Proxy Triage

## Overview

This skill captures live `OpenKey` misses for `*InProcServer32`, enriches them with the corresponding machine-wide `InProcServer32` DLL, and tests only CLSIDs that have a usable HKLM backing DLL.

Fresh hosts should start with `scripts/Initialize-ComHijackHost.ps1 -ValidateOnly`. If the `FAIL` rows show missing build prerequisites such as `MSBuild`, `VC x64 toolchain`, `Windows SDK`, or `vswhere`/Visual Studio Build Tools details, run `scripts/Initialize-ComHijackHost.ps1 -InstallBuildTools` and then rerun `-ValidateOnly` before full validation. Use `scripts/Watch-InProcServer32Misses.ps1` for the capture step, `scripts/Invoke-ComHijackProbe.ps1` for a low-level probe, `scripts/Invoke-ComHijackApp.ps1` for an app-name-first single-app run, `scripts/Invoke-ComHijackSurvey.ps1` for batch runs, and `scripts/Get-ComHijackOverlap.ps1` to analyze the running JSONL database. Read `references/workflow.md` when you need the concrete test loop, registry handling, or Koppeling build notes.

## Workflow

1. Run the watcher from an elevated PowerShell session and filter to the target process with `-ProcessName`.
2. Keep only `HKCU` `InProcServer32` misses where `MachineInprocServer32` is present.
3. Deduplicate by `Clsid`.
4. Build or reuse a proxy DLL that clones the HKLM target DLL's exports and runs the chosen payload.
5. Override `HKCU\Software\Classes\CLSID\{CLSID}\InProcServer32`, launch a fresh target process, and check whether the payload fired.
6. Restore the prior HKCU state after every test. If the key did not exist before, remove it.
7. Resolve installed apps by name first. Use `assets\apps.json` as an override cache when present, not as a required source of truth.

## Rules

- Ignore candidates that do not have a corresponding `MachineInprocServer32` value.
- Treat `0xC0000034` as `NAME NOT FOUND`.
- Prefer cold-start launches of the target app for each test.
- Record whether the payload fired and whether the proxy DLL was actually loaded.
- Never leave a test override behind unless the user explicitly asks to keep it.
- Treat the repo-local `Koppeling\` submodule as the primary proxy dependency. Only fall back to adjacent or `Documents\Codex` checkouts if the submodule is unavailable.
- Seed `Koppeling\Bin\NetClone.exe` from `assets\koppeling-netclone\` before trying to rebuild it on a fresh or offline host.
- Always write discovery artifacts even when the host is missing the VC toolchain for full payload validation.
- By default, validate every discovered candidate. Use `-MaxCandidates` only as an explicit throttle for faster spot checks.
- When `Initialize-ComHijackHost.ps1 -ValidateOnly` fails on build-toolchain checks (`MSBuild`, `VC x64 toolchain`, `Windows SDK`, or `vswhere`/Build Tools-related details), run `Initialize-ComHijackHost.ps1 -InstallBuildTools` before retrying full validation.
- Do not treat `-InstallBuildTools` as a fix for missing elevation, missing target apps, or other non-toolchain blockers; discovery-only runs remain valid when full validation is not possible.

## Database Snapshot

- Before pushing updates to `com-proxy-triage`, verify whether the published `COM-Proxy-Database` snapshot also needs to be refreshed.
- If the push changes probe behavior, result semantics, or dashboard-visible fields, update the local `COM-Proxy-Database` clone, run `scripts\Refresh-ComProxyDatabaseSnapshot.ps1`, and push that repo as part of the same publishing pass.
- Keep the published database snapshot aligned with the live dashboard metrics:
  `Active Apps`, `Unique CLSIDs`, `Unique DLLs`, `Shared DLLs`, and `Shared CLSIDs`.

Use this refresh step:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\Refresh-ComProxyDatabaseSnapshot.ps1"
```

## Quick Start

Validate a fresh host first:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\Initialize-ComHijackHost.ps1" -ValidateOnly
```

If the `FAIL` rows show missing `MSBuild`, `VC x64 toolchain`, `Windows SDK`, or `vswhere`/Build Tools-related details, install the toolchain:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\Initialize-ComHijackHost.ps1" -InstallBuildTools
```

Then validate the host again before running the probe:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\Initialize-ComHijackHost.ps1" -ValidateOnly
```

Use this watcher pattern:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\Watch-InProcServer32Misses.ps1" -ProcessName Zoom -ResolveProcessName -DurationSeconds 30
```

The emitted JSON already includes:

- `Clsid`
- `Path`
- `MachineInprocServer32`

That is enough to pick candidates and drive the HKCU override loop in `references/workflow.md`.

Run any installed app by name:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\Invoke-ComHijackApp.ps1" -AppName "Slack" -KillExisting
```

That default run tests every discovered candidate. Add `-MaxCandidates 5` or another positive limit only when you want a smaller sample.

Run a manifest-backed app:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\Invoke-ComHijackApp.ps1" -AppName Zoom -KillExisting
```

To inspect CLSID overlap across everything already tested:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\Get-ComHijackOverlap.ps1"
```

To run every app currently declared in the manifest:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\Invoke-ComHijackSurvey.ps1" -KillExisting
```
