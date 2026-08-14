from __future__ import annotations

from pathlib import Path

from tools.repo_maintenance.checks import check_links
from tools.repo_maintenance.models import CheckContext


def test_links_handle_spaces_anchors_nesting_and_fenced_examples(
    tmp_path: Path, monkeypatch
) -> None:
    root = tmp_path
    docs = root / "docs"
    (docs / "nested").mkdir(parents=True)
    main = docs / "main.md"
    target = docs / "target file.md"
    child = docs / "nested/child.md"
    target.write_text("# Target Heading\n", encoding="utf-8")
    child.write_text("# Child\n", encoding="utf-8")
    main.write_text(
        "\n".join(
            (
                "[encoded](target%20file.md#target-heading)",
                "[nested](nested/child.md)",
                "[external](https://example.test/missing)",
                "```markdown",
                "[fenced](missing.md)",
                "```",
                "",
            )
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(check_links, "repository_files", lambda root: [main, target, child])
    assert check_links.run(CheckContext(root)) == []


def test_links_report_missing_anchor_and_root_escape(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path
    docs = root / "docs"
    docs.mkdir()
    main = docs / "main.md"
    target = docs / "target.md"
    target.write_text("# Existing\n", encoding="utf-8")
    main.write_text("[anchor](target.md#missing)\n[escape](../../outside.md)\n", encoding="utf-8")
    monkeypatch.setattr(check_links, "repository_files", lambda root: [main, target])
    diagnostics = check_links.run(CheckContext(root))
    assert {item.rule for item in diagnostics} == {"links.anchor", "links.internal"}
    assert any("escapes repository" in item.reason for item in diagnostics)


def test_skill_inline_resource_paths_are_checked(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path
    skill = root / "plugins/demo/skills/example"
    (skill / "scripts").mkdir(parents=True)
    (skill / "scripts/run.sh").write_text("#!/bin/sh\n", encoding="utf-8")
    document = skill / "SKILL.md"
    document.write_text("Use `scripts/run.sh`. Missing: `assets/missing.svg`.\n", encoding="utf-8")
    monkeypatch.setattr(check_links, "repository_files", lambda root: [document])
    diagnostics = check_links.run(CheckContext(root))
    assert len(diagnostics) == 1
    assert diagnostics[0].reason == "missing target: assets/missing.svg"
