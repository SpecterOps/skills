# Plugins

Place installable plugin packages in this directory.

Each cross-platform plugin should use:

```text
plugins/<plugin-name>/
├── .codex-plugin/plugin.json
├── .claude-plugin/plugin.json
├── skills/
└── README.md
```

Optional plugin-owned content can include `commands/`, `hooks/`, `.mcp.json`, `assets/`, `scripts/`, and reference documentation.

After adding a plugin, update:

- `.agents/plugins/marketplace.json`
- `.claude-plugin/marketplace.json`
- `README.md`
