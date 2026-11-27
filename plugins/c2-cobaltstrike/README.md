# C2 Cobalt Strike

Focused workflows for Cobalt Strike operations, Beacon Interpreter C scripts, Aggressor scripts, Sleep language references, BOF loader work, aliases, hooks, and Malleable C2 profile development.

## Skills

- `cobalt-strike-aggressor-development`
- `cobalt-strike-aggressor-reference`
- [`cobalt-strike-beacon-interpreter`](skills/cobalt-strike-beacon-interpreter/SKILL.md)
- `cobalt-strike-malleable-c2-development`
- `cobalt-strike-ops`

## Agents

- `exploit-dev`

## Beacon Interpreter

Use `$cobalt-strike-beacon-interpreter` in Codex or
`/c2-cobaltstrike:cobalt-strike-beacon-interpreter` in Claude Code. The skill
includes offline compatibility guidance, headers, and an example for writing
and reviewing Interpreter C scripts.

This bundle is imported from [Cobalt-Strike/beacon-interpreter](https://github.com/Cobalt-Strike/beacon-interpreter)
at [commit `7fbd3014608cf0941455a586d78ec244ae0fcf7e`](https://github.com/Cobalt-Strike/beacon-interpreter/tree/7fbd3014608cf0941455a586d78ec244ae0fcf7e/skills/cobalt-strike-beacon-interpreter).
Make skill changes upstream, then refresh this directory from a reviewed commit
and update the pin. The bundle includes its Apache-2.0 license and provenance.

## Cobalt Strike MCP setup

The `cobalt-strike-ops` skill uses the official [Cobalt Strike MCP server](https://github.com/Cobalt-Strike/cobaltstrike-mcp-server). Please see its repo for installation steps.
