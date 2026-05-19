# Standalone Skills

This directory is for standalone skills that should be discoverable by `npx skills`.

Use this path only for skills that can work without full plugin installation.

```text
skills/<skill-name>/SKILL.md
```

If a workflow depends on plugin-only behavior such as MCP configuration, Claude slash commands, hooks, or Codex app mappings, package it under `plugins/<plugin-name>/skills/` instead and document that full plugin installation is required.
