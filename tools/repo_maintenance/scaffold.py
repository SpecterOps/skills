from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from tools.repo_maintenance.generators import catalog
from tools.repo_maintenance.transaction import install_text_outputs

PLUGIN_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def planned_outputs(root: Path, name: str, description: str) -> dict[Path, str]:
    if not PLUGIN_NAME.fullmatch(name):
        raise ValueError("plugin name must be lowercase words separated by single hyphens")
    if not description.strip():
        raise ValueError("description must not be empty")
    plugin_root = Path("plugins") / name
    if (root / plugin_root).exists():
        raise ValueError(f"plugin already exists: {plugin_root.as_posix()}")
    display_name = " ".join(word.capitalize() for word in name.split("-"))
    manifest = {
        "name": name,
        "version": "0.1.0",
        "description": description.strip(),
        "author": {"name": "SpecterOps"},
        "skills": "./",
        "interface": {
            "displayName": display_name,
            "shortDescription": description.strip(),
            "longDescription": description.strip(),
            "developerName": "SpecterOps",
            "category": "Security",
            "capabilities": [],
            "defaultPrompt": [],
            "brandColor": "#00B36B",
            "composerIcon": "./assets/icon.svg",
            "logo": "./assets/icon.svg",
        },
        "license": "UNLICENSED",
        "keywords": ["codex", "specterops"],
    }
    ownership = {
        "plugin": name,
        "purpose": description.strip(),
        "status": "incubating",
        "agents": [],
        "skills": [],
    }
    catalog_text = (root / "tools/maintenance/catalog.toml").read_text(encoding="utf-8")
    catalog_text += f'\n[[plugins]]\nname = "{name}"\nsurfaces = ["codex"]\n'
    return {
        Path("tools/maintenance/catalog.toml"): catalog_text,
        plugin_root / ".codex-plugin/plugin.json": json.dumps(manifest, indent=2) + "\n",
        plugin_root / "ownership.json": json.dumps(ownership, indent=2) + "\n",
        plugin_root / "README.md": (
            f"# {display_name}\n\n{description.strip()}\n\n"
            "## Skills\n\n- None currently packaged in this plugin.\n"
        ),
        plugin_root / "assets/icon.svg": (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" '
            f'aria-label="{display_name}"><rect width="64" height="64" rx="12" '
            'fill="#00B36B"/><path d="M18 32h28M32 18v28" stroke="#fff" '
            'stroke-width="6" stroke-linecap="round"/></svg>\n'
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan or apply metadata-only plugin scaffolding")
    parser.add_argument("command", choices=("plan", "apply"))
    parser.add_argument("name")
    parser.add_argument("description")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    arguments = parser.parse_args(argv)
    root = arguments.root.resolve()
    try:
        outputs = planned_outputs(root, arguments.name, arguments.description)
        if arguments.command == "apply":
            install_text_outputs(root, outputs)
            catalog.generate(root)
    except (OSError, RuntimeError, ValueError) as exc:
        parser.error(str(exc))
    prefix = "created" if arguments.command == "apply" else "would create"
    for path in outputs:
        if path != Path("tools/maintenance/catalog.toml"):
            print(f"{prefix}: {path.as_posix()}")
    catalog_action = "updated" if arguments.command == "apply" else "would update"
    print(f"{catalog_action}: tools/maintenance/catalog.toml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
