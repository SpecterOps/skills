# Workflow

## Capture

Run the bundled watcher from an elevated PowerShell session:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\Watch-InProcServer32Misses.ps1" -ProcessName Zoom -ResolveProcessName -DurationSeconds 30
```

The watcher polls a live ETW registry trace and prints one JSON object per matching `OpenKey` miss where:

- `Status == 0xC0000034`
- the path ends with `InProcServer32`
- the process name matches `-ProcessName` if supplied

Each event includes the parsed `Clsid` and the machine-wide `HKLM\SOFTWARE\Classes\CLSID\{...}\InProcServer32` default value as `MachineInprocServer32`.

## Candidate Selection

1. Keep only paths under the current user's `HKCU\Software\Classes\CLSID\{...}\InProcServer32` equivalent.
2. Drop any event where `MachineInprocServer32` is empty.
3. Deduplicate by `Clsid`.
4. Test candidates one at a time from a fresh target launch.

## Proxy Build

Use a local Koppeling checkout when available.

Expected pattern:

1. Patch `Koppeling\Theif\main.cpp` so the payload only runs inside the target process.
2. Build the Koppeling payload DLL.
3. Clone the target HKLM DLL's exports onto the payload DLL with `NetClone`.

The payload used during development was `calc.exe`.

The codified path now is:

1. Use `scripts\Build-KoppelingPayload.ps1` with one or more target process names.
2. Let it generate `Koppeling\Theif\main.cpp` from `assets\theif-main-template.cpp`.
3. Build `Theif.dll`.
4. Restore the original `main.cpp`.

## HKCU Override Loop

The per-user override key is:

```text
HKEY_CURRENT_USER\Software\Classes\CLSID\{CLSID}\InProcServer32
```

For each candidate:

1. Read and save the existing HKCU default value and `ThreadingModel`.
2. Set the default value to the proxy DLL path.
3. Set a compatible `ThreadingModel` such as `Both` if needed.
4. Launch a fresh target process.
5. Check whether the payload fired and whether the proxy DLL loaded.
6. Restore the old HKCU values, or delete the key if it did not exist before the test.

## Config-Driven Runs

Prefer the manifest in `assets\apps.json` over inferring launch paths in chat.

Current wrappers:

- `scripts\Invoke-ComHijackApp.ps1`
- `scripts\Invoke-ComHijackSurvey.ps1`

These wrappers:

- load the app spec from the manifest
- build a target-specific payload DLL
- run the probe script
- append results into the JSONL database
