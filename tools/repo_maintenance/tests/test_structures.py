from __future__ import annotations

from pathlib import Path

from tools.repo_maintenance.checks import check_structures
from tools.repo_maintenance.models import CheckContext


def test_malformed_structural_yaml_is_a_path_specific_diagnostic(
    tmp_path: Path, monkeypatch
) -> None:
    metadata = tmp_path / "plugins/example/skills/broken/agents/openai.yaml"
    metadata.parent.mkdir(parents=True)
    metadata.write_text("interface: [\n", encoding="utf-8")
    monkeypatch.setattr(
        check_structures,
        "_inputs",
        lambda root: [(metadata, "skill-ui", "yaml")],
    )

    diagnostics = check_structures.run(CheckContext(tmp_path))

    assert len(diagnostics) == 1
    assert diagnostics[0].rule == "core.structure"
    assert diagnostics[0].path == "plugins/example/skills/broken/agents/openai.yaml"
    assert "expected the node content" in diagnostics[0].reason
