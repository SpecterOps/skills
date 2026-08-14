from __future__ import annotations

import re
import urllib.parse
from pathlib import Path

from markdown_it import MarkdownIt

from tools.repo_maintenance.files import relative_path, repository_files
from tools.repo_maintenance.models import CheckContext, CheckSpec, Diagnostic

MARKDOWN = MarkdownIt("commonmark")
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "data"}
RESOURCE = re.compile(r"^(?:\./|scripts/|references/|assets/).+$")


def _slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\- ]", "", value)
    return re.sub(r"\s+", "-", value)


def _anchors(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    result = set(re.findall(r"<a\s+(?:[^>]*?\s)?(?:id|name)=[\"']([^\"']+)", text, re.I))
    seen: dict[str, int] = {}
    tokens = MARKDOWN.parse(text)
    for index, token in enumerate(tokens[:-1]):
        if token.type != "heading_open" or tokens[index + 1].type != "inline":
            continue
        inline = tokens[index + 1]
        visible = "".join(
            child.content
            for child in (inline.children or [])
            if child.type in {"text", "code_inline", "image"}
        )
        base = _slug(visible)
        count = seen.get(base, 0)
        seen[base] = count + 1
        result.add(base if count == 0 else f"{base}-{count}")
    return result


def _skill_root(path: Path) -> Path:
    for parent in (path.parent, *path.parents):
        if (parent / "SKILL.md").is_file():
            return parent
    parts = path.parts
    if "plugins" in parts:
        index = parts.index("plugins")
        if len(parts) > index + 1:
            return Path(*parts[: index + 2])
    return path.parent


def _candidate(root: Path, document: Path, value: str, resource: bool = False) -> Path:
    decoded = urllib.parse.unquote(value).replace("\\", "/")
    if not decoded:
        return document
    if decoded.startswith("/"):
        return root / decoded.lstrip("/")
    base = _skill_root(document) if resource and not decoded.startswith("./") else document.parent
    return base / decoded.removeprefix("./")


def _validate_target(
    diagnostics: list[Diagnostic], root: Path, document: Path, target: str, *, resource: bool
) -> None:
    if not target or any(marker in target for marker in ("<", ">", "{", "}", "*")):
        return
    parsed = urllib.parse.urlsplit(target)
    if parsed.scheme.lower() in EXTERNAL_SCHEMES or parsed.netloc:
        return
    path_value = parsed.path
    candidate = _candidate(root, document, path_value, resource=resource).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        diagnostics.append(
            Diagnostic(
                "links.internal",
                relative_path(root, document),
                f"target escapes repository: {target}",
            )
        )
        return
    if not candidate.exists():
        diagnostics.append(
            Diagnostic("links.internal", relative_path(root, document), f"missing target: {target}")
        )
        return
    if parsed.fragment:
        anchor_file = candidate if candidate.is_file() else candidate / "README.md"
        if anchor_file.suffix.lower() == ".md" and anchor_file.is_file():
            anchor = urllib.parse.unquote(parsed.fragment).lower()
            if anchor not in _anchors(anchor_file):
                diagnostics.append(
                    Diagnostic(
                        "links.anchor",
                        relative_path(root, document),
                        f"missing anchor #{parsed.fragment} in {relative_path(root, anchor_file)}",
                    )
                )


def run(context: CheckContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for path in repository_files(context.root):
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for token in MARKDOWN.parse(text):
            if token.type != "inline" or not token.children:
                continue
            for child in token.children:
                if child.type == "link_open":
                    href = child.attrGet("href")
                    if href is not None:
                        _validate_target(diagnostics, context.root, path, href, resource=False)
                elif child.type == "image":
                    source = child.attrGet("src")
                    if source is not None:
                        _validate_target(diagnostics, context.root, path, source, resource=False)
                elif child.type == "code_inline" and path.name == "SKILL.md":
                    value = child.content.strip().rstrip(".,;:")
                    if RESOURCE.fullmatch(value):
                        value = re.split(r"\s+(?=-{1,2}[A-Za-z])", value, maxsplit=1)[0]
                        _validate_target(diagnostics, context.root, path, value, resource=True)
    return diagnostics


CHECK = CheckSpec("links.internal", frozenset({"links"}), run)
