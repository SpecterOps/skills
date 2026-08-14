from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from markdown_it import MarkdownIt

from tools.repo_maintenance.files import relative_path, repository_files

MARKDOWN = MarkdownIt("commonmark")
USER_AGENT = "specterops-skills-maintenance/1"
MAX_JSON_BYTES = 1_048_576


def request_bytes(url: str, *, timeout: float = 15, attempts: int = 3) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/plain;q=0.9, */*;q=0.1",
        },
    )
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read(MAX_JSON_BYTES + 1)
                if len(body) > MAX_JSON_BYTES:
                    raise RuntimeError(f"response exceeds {MAX_JSON_BYTES} bytes")
                return body
        except (OSError, urllib.error.HTTPError) as exc:
            if attempt + 1 == attempts or (
                isinstance(exc, urllib.error.HTTPError) and exc.code < 500
            ):
                raise RuntimeError(str(exc)) from exc
            time.sleep(0.25 * (2**attempt))
    raise AssertionError("retry loop exhausted")


def external_urls(root: Path) -> dict[str, set[str]]:
    urls: dict[str, set[str]] = {}
    for path in repository_files(root):
        if path.suffix.lower() != ".md":
            continue
        for token in MARKDOWN.parse(path.read_text(encoding="utf-8")):
            if token.type != "inline" or not token.children:
                continue
            for child in token.children:
                attribute = (
                    "href"
                    if child.type == "link_open"
                    else "src"
                    if child.type == "image"
                    else None
                )
                value = child.attrGet(attribute) if attribute else None
                if value and value.startswith(("https://", "http://")):
                    urls.setdefault(value, set()).add(relative_path(root, path))
    return urls


def check_external_links(
    root: Path, *, fetch: Callable[[str], bytes] = request_bytes, workers: int = 8
) -> list[str]:
    urls = external_urls(root)

    def inspect(url: str) -> str | None:
        try:
            fetch(url)
        except RuntimeError as exc:
            locations = ", ".join(sorted(urls[url]))
            return f"{url} ({locations}): {exc}"
        return None

    with ThreadPoolExecutor(max_workers=workers) as executor:
        return sorted(result for result in executor.map(inspect, urls) if result is not None)


def check_upstream_bloodhound(
    root: Path, *, fetch: Callable[[str], bytes] = request_bytes
) -> list[str]:
    manifest_path = root / "plugins/bloodhound/references/query-snapshots/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    diagnostics = []
    for source in manifest.get("sources", []):
        repo = source["repo"]
        branch = source["branch"]
        url = f"https://api.github.com/repos/{repo}/commits/{branch}"
        try:
            payload: Any = json.loads(fetch(url))
            upstream = payload["sha"]
        except (RuntimeError, json.JSONDecodeError, KeyError, TypeError) as exc:
            diagnostics.append(f"{source['id']}: unable to resolve {repo}@{branch}: {exc}")
            continue
        if upstream != source["commit"]:
            diagnostics.append(
                f"{source['id']}: snapshot {source['commit']} trails {repo}@{branch} {upstream}"
            )
    return diagnostics


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run bounded, read-only network maintenance")
    parser.add_argument("command", choices=("external-links", "upstream-bloodhound"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    arguments = parser.parse_args(argv)
    try:
        diagnostics = (
            check_external_links(arguments.root)
            if arguments.command == "external-links"
            else check_upstream_bloodhound(arguments.root)
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        diagnostics = [str(exc)]
    for diagnostic in diagnostics:
        print(diagnostic)
    return 1 if diagnostics else 0


if __name__ == "__main__":
    raise SystemExit(main())
