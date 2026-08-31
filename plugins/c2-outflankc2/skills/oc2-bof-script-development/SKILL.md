---
name: oc2-bof-script-development
description: Use when writing Outflank C2 Python BOF wrappers for OC2 V2 (*_bof.s1.py, BaseBOFTask, outflank_stage1, stage1) or V3 (oc2_sdk_python, @command, manifest.json, command provider), when porting/migrating/converting a V2 BOF script to a V3 application, or when passing an existing @artifacts/ catalog file.
metadata:
  author: Outflank
---

# Outflank C2 (OC2) BOF Python Script Development

Python wrappers expose a compiled Beacon Object File as an OC2 command (the OC2 equivalent of Cobalt Strike Aggressor Script). Use the c2-bof-development skill for the C/C++ object itself.

Note that OC2 version 3 is still in beta. Later release candidates may introduce breaking changes.

## Route before writing code

First, determine whether the user is writing a V2 or V3 BOF. Do not always ask. Infer from evidence, then load the matching references:

- V2: `*_bof.s1.py`, `BaseBOFTask`, `outflank_stage1`, or explicit OC2 2.x
- V3: `oc2_sdk_python`, `@command`, or a V3 `manifest.json`
- Port: user says port, migrate, or convert (also load the V3 refs)
- No version clues: for a new wrapper, ask whether it targets V2 or V3. When modifying existing code, ask only if its version cannot be inferred.

## When NOT to Use

Do not use this skill unless Outflank C2 support is requested, or BOF development is being completed and an OC2 Python script is required to load and execute the BOF.

## References

*Version 2*
- [Authoring model (V2)](./references/v2/bof-authoring.md) — packaging and lifecycle hooks
- [Runtime API (V2)](./references/v2/bof-runtime-api.md) — constructor, enums, binary resolution, packing
- [Examples (V2)](./references/v2/bof-examples.md) — minimal and typed-argument wrappers

*Version 3*
- [Authoring model (V3)](./references/v3/bof-authoring.md) — application layout, manifest artifacts, lifecycle
- [Runtime API (V3)](./references/v3/bof-runtime-api.md) — `@command`, packing, implant opcodes, BUFFER ids
- [Examples (V3)](./references/v3/bof-examples.md) — no-arg, typed pack, catalog-artifact BUFFER

*Porting Version 2 scripts to Version 3*
- [Porting cookbook](./references/bof-port-v2-to-v3.md) — audit, hook map, side-by-side. Also load the V3 authoring and runtime refs.
