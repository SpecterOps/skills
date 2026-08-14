from __future__ import annotations

import argparse
import json
import re
from collections.abc import Iterable
from pathlib import Path
from urllib.parse import urlsplit

from tools.repo_maintenance.generators import catalog
from tools.repo_maintenance.transaction import install_text_outputs

PLUGIN_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SUPPORTED_MANIFESTS = ("codex", "claude")
DEFAULT_SUPPORT_URL = "https://github.com/SpecterOps/skills/issues"


def _manifest_selection(values: Iterable[str]) -> tuple[str, ...]:
    selected = tuple(dict.fromkeys(value.strip() for value in values if value.strip()))
    unknown = sorted(set(selected) - set(SUPPORTED_MANIFESTS))
    if unknown:
        raise ValueError(f"unsupported manifest surface(s): {', '.join(unknown)}")
    if "codex" not in selected:
        raise ValueError("plugin scaffolding requires the canonical Codex manifest")
    return selected


def planned_outputs(
    root: Path,
    name: str,
    description: str,
    *,
    manifests: Iterable[str] = SUPPORTED_MANIFESTS,
    maintainer: str = "SpecterOps",
    support_url: str = DEFAULT_SUPPORT_URL,
) -> dict[Path, str]:
    if not PLUGIN_NAME.fullmatch(name):
        raise ValueError("plugin name must be lowercase words separated by single hyphens")
    if not description.strip():
        raise ValueError("description must not be empty")
    selected_manifests = _manifest_selection(manifests)
    if not maintainer.strip():
        raise ValueError("maintainer must not be empty")
    support = urlsplit(support_url)
    if support.scheme != "https" or not support.netloc:
        raise ValueError("support URL must use https")
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
        "contacts": {
            "maintainers": [maintainer.strip()],
            "support": support_url,
        },
        "release": {
            "version": manifest["version"],
            "channel": "unreleased",
        },
        "agents": [],
        "skills": [],
    }
    catalog_text = (root / "tools/maintenance/catalog.toml").read_text(encoding="utf-8")
    catalog_text += f'\n[[plugins]]\nname = "{name}"\nsurfaces = ["codex"]\n'
    manifest_names = ", ".join(surface.title() for surface in selected_manifests)
    outputs = {
        Path("tools/maintenance/catalog.toml"): catalog_text,
        plugin_root / ".codex-plugin/plugin.json": json.dumps(manifest, indent=2) + "\n",
        plugin_root / "ownership.json": json.dumps(ownership, indent=2) + "\n",
        plugin_root / "README.md": (
            f"# {display_name}\n\n{description.strip()}\n\n"
            "## Status\n\n"
            "Incubating. This metadata-only scaffold is not installable until a capability is "
            "packaged and the plugin is explicitly promoted.\n\n"
            "## Supported clients\n\n"
            f"Manifest templates included for: {manifest_names}. Publication surfaces remain "
            "restricted while the plugin is incubating.\n\n"
            "## Prerequisites\n\n- None declared yet.\n\n"
            "## Skills\n\n- None currently packaged in this plugin.\n\n"
            "## Example prompts\n\n"
            "Add tested example prompts when the first capability is packaged.\n\n"
            "## Development\n\n"
            "Run `just check` after updating manifests, ownership, capabilities, or this README. "
            "Run `just generate-catalog` when publication metadata changes.\n\n"
            "## Support\n\n"
            f"Maintainer: {maintainer.strip()}  \nSupport: {support_url}\n\n"
            "## Release\n\n- Version: `0.1.0`\n- Channel: unreleased\n"
        ),
        plugin_root / "assets/icon.svg": (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" '
            f'aria-label="{display_name}"><rect width="64" height="64" rx="12" '
            'fill="#00B36B"/><path d="M18 32h28M32 18v28" stroke="#fff" '
            'stroke-width="6" stroke-linecap="round"/></svg>\n'
        ),
    }
    if "claude" in selected_manifests:
        claude_manifest = {
            key: manifest[key] for key in ("name", "description", "version", "author")
        }
        claude_manifest["license"] = manifest["license"]
        claude_manifest["keywords"] = manifest["keywords"]
        outputs[plugin_root / ".claude-plugin/plugin.json"] = (
            json.dumps(claude_manifest, indent=2) + "\n"
        )
    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan or apply metadata-only plugin scaffolding")
    parser.add_argument("command", choices=("plan", "apply"))
    parser.add_argument("name")
    parser.add_argument("description")
    parser.add_argument(
        "--manifests",
        default=",".join(SUPPORTED_MANIFESTS),
        help="comma-separated manifest templates to create (Codex is required)",
    )
    parser.add_argument("--maintainer", default="SpecterOps")
    parser.add_argument("--support-url", default=DEFAULT_SUPPORT_URL)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    arguments = parser.parse_args(argv)
    root = arguments.root.resolve()
    try:
        outputs = planned_outputs(
            root,
            arguments.name,
            arguments.description,
            manifests=arguments.manifests.split(","),
            maintainer=arguments.maintainer,
            support_url=arguments.support_url,
        )
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
