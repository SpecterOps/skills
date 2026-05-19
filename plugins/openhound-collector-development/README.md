# OpenHound Template

OpenHound collector template support package. The full cookiecutter template is preserved at `templates/openhound-collector-development/`, and this plugin exposes the embedded `openhound` development skill through the shared marketplaces.

## Contents

- `skills/openhound/` - OpenHound collector development workflow and references.
- `standards/` - OpenHound standards copied from the generated template.
- `.claude-plugin/plugin.json` - Claude Code plugin manifest.
- `.codex-plugin/plugin.json` - Codex plugin manifest.

## Template

Use the full template from the repository root:

```text
templates/openhound-collector-development/
```

The skill still references generated collector paths such as `.agents/standards/`. When using it outside a generated OpenHound project, consult the copied `standards/` directory in this plugin.
