---
name: oc2-bof-script-development
description: Develop Outflank C2 Python BOF scripts. Use when writing Beacon Object Files for OC2.
metadata:
  author: Outflank
---

# Outflank C2 (OC2) BOF Python Script Development

Instead of Cobalt Strike Aggressor Script, Outflank C2 uses Python scripts to define new commands. Use this skill for Python scripts that expose a compiled Beacon Object File (BOF) as an OC2 command. Use the c2-bof-development skill for the C/C++ object itself.

## When NOT to Use

Do not use this skill unless Outflank C2 support is requested, or BOF development is being completed and an OC2 Python script is required to load and execute the BOF.

## References

- [Authoring model](./references/bof-authoring.md) — packaging and lifecycle hooks.
- [Runtime API](./references/bof-runtime-api.md) — constructor, enums, binary resolution, and argument packing.
- [Examples](./references/bof-examples.md) — minimal and typed-argument wrappers.
