from __future__ import annotations

import json
from pathlib import Path

from tools.repo_maintenance import network_maintenance


def test_external_links_are_deduplicated_and_failures_include_sources(
    tmp_path: Path, monkeypatch
) -> None:
    first = tmp_path / "first.md"
    second = tmp_path / "second.md"
    first.write_text("[one](https://good.test) ![bad](https://bad.test/a.png)\n", encoding="utf-8")
    second.write_text("[again](https://bad.test/a.png)\n", encoding="utf-8")
    monkeypatch.setattr(network_maintenance, "repository_files", lambda root: [first, second])
    calls = []

    def fetch(url: str) -> bytes:
        calls.append(url)
        if "bad.test" in url:
            raise RuntimeError("unavailable")
        return b"ok"

    diagnostics = network_maintenance.check_external_links(tmp_path, fetch=fetch, workers=2)
    assert sorted(calls) == ["https://bad.test/a.png", "https://good.test"]
    assert len(diagnostics) == 1
    assert "first.md, second.md" in diagnostics[0]


def test_upstream_check_reports_drift_without_writing_snapshot(tmp_path: Path) -> None:
    manifest = tmp_path / "plugins/bloodhound/references/query-snapshots/manifest.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        json.dumps(
            {
                "sources": [
                    {
                        "id": "example",
                        "repo": "owner/repo",
                        "branch": "main",
                        "commit": "old",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    diagnostics = network_maintenance.check_upstream_bloodhound(
        tmp_path, fetch=lambda url: b'{"sha": "new"}'
    )
    assert diagnostics == ["example: snapshot old trails owner/repo@main new"]
    assert '"commit": "old"' in manifest.read_text(encoding="utf-8")
