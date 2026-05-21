---
name: electron-install-persistence
description: Preserve post-install execution and background residency for Electron apps in Squirrel-style delivery chains. Use when the payload checks in once, then dies after install or on app close.
icon: ./assets/icon.png
---

# Electron Install Persistence

Use this skill when a payload runs inside Electron but exits after install, update completion, or user close actions.

## Focus Areas
- `process.argv` handling for `--squirrel-*`
- install/update continuation behavior
- updater-parent termination or continuation logic
- quit and close suppression
- hidden `BrowserWindow` keepalive patterns
- background execution without visible UI

## Workflow
1. Identify install/update entrypoints and `--squirrel-*` handling in the main process.
2. Preserve or reproduce the continuation pattern that keeps the app alive after install completes.
3. If the app requires a live window to remain resident, create a hidden/background `BrowserWindow` and prevent close-driven teardown.
4. Neutralize only the quit/close paths that prematurely terminate residency.
5. Verify that post-install launch, callback continuity, and background residency all survive the installer flow.

## Output
Always report:
- install/update path inspected
- continuation logic preserved or added
- hidden-window behavior used, if any
- specific quit/close paths neutralized
- remaining blockers or unknowns
