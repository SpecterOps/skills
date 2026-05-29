---
name: electron-app-audit
description: Audit a local downloaded Electron package/path or a named Electron app and produce a deep worksheet for patchability, entrypoints, and install-chain behavior. Use when deciding whether an app is a good candidate and how to modify it.
metadata:
  author: "GhostWorks"
---

# Electron App Audit

Use this skill when auditing either:
- a local installer/package/path, or
- a named Electron app

## Required Output
Produce a deep worksheet covering:
- packaging shape
- unpacking location(s)
- main-process entrypoint
- update/install mechanism
- whether it is Squirrel-like or similarly patchable
- likely patch points
- persistence/install-continuation considerations
- blockers, unknowns, and caveats
- go / no-go conclusion

## Workflow
1. Identify whether the target is a local package or a named app.
2. Determine the packaging layout and locate the main-process entrypoint.
3. Inspect how install/update is handled and whether the chain resembles Squirrel.
4. Identify likely payload injection points and any metadata/repackaging constraints.
5. Assess whether post-install continuity would require continuation logic, quit suppression, or a hidden keepalive window.
6. Conclude with a decision memo backed by the worksheet details.

## Output Style
Prefer a handoff-ready worksheet over a short verdict.
