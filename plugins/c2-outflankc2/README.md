# Outflank C2 Development

Outflank C2 (OC2) BOF script and event-driven bot development workflows.

## Status

Active preview. The plugin packages two development skills and self-contained OC2 reference material.

## Supported clients

- Codex
- Claude Code

## Prerequisites

- Access to an authorized Outflank C2 project or server source tree
- The `outflank_stage1` Python library supplied with that OC2 version
- Python and any compiler/toolchain required by the surrounding OC2 project

This plugin does not install, configure, or connect to an OC2 server. Prefer the library and examples shipped with the target OC2 deployment if their interfaces differ from the bundled references.

## Skills

- `oc2-bof-script-development` — author Python `_bof.s1.py` task wrappers that register, validate, and encode BOF execution in OC2.
- `oc2-bot-development` — build event-driven Python bots around `BaseBot`, OC2 services, implants, and tasks.

## Example prompts

- "Create an OC2 BOF script for these x86 and x64 object files and encode its two arguments."
- "Add privilege and architecture validation to this `_bof.s1.py` wrapper."
- "Build an OC2 bot that schedules initial inventory tasks for new implants."
- "Debug why this OC2 bot is not receiving task-response events."

## Development

Run `just check` after changing plugin content. Run `just generate-catalog` and `just generate-inventory` when publication metadata or packaged skills change.

## Support

Maintainer: Outflank  
Support: https://github.com/SpecterOps/skills/issues

Do not include credentials, customer data, operational evidence, or proprietary OC2 packages in public issues.

## Release

- Version: `0.1.0`
- Channel: preview
