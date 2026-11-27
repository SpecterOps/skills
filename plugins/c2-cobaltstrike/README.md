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

SpecterOps maintains the skill instructions and validation guide. The bundled
reference files come from [Cobalt-Strike/beacon-interpreter](https://github.com/Cobalt-Strike/beacon-interpreter).
The [provenance record](skills/cobalt-strike-beacon-interpreter/references/provenance.json)
lists the upstream commit and file hashes.

### Refresh the bundled resources

1. In a Cobalt Strike checkout, export the resources from a reviewed commit.
   Replace `COMMIT_SHA` with the full upstream SHA.

   ```sh
   python tools/export_skill_resources.py COMMIT_SHA beacon-interpreter-resources.zip
   ```

2. From the SpecterOps repository root, import the ZIP and verify the snapshot.
   Set `ARCHIVE` to the path of the exported ZIP.

   ```sh
   python -m tools.repo_maintenance.import_beacon_interpreter_resources ARCHIVE
   python -m tools.repo_maintenance.import_beacon_interpreter_resources ARCHIVE --check
   ```

3. Update the plugin version in both manifests, then run `just generate-catalog`,
   `just generate-inventory`, and `just check`.

## Cobalt Strike MCP setup

The `cobalt-strike-ops` skill uses the official [Cobalt Strike MCP server](https://github.com/Cobalt-Strike/cobaltstrike-mcp-server). Please see its repo for installation steps.
