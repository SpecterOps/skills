from __future__ import annotations

import datetime as dt

from tools.repo_maintenance.checks.check_exceptions import validate


def test_empty_exception_registry_is_valid() -> None:
    assert validate({"exceptions": []}, today=dt.date(2026, 8, 14)) == []


def test_exception_requires_exact_owned_and_unexpired_scope() -> None:
    diagnostics = validate(
        {
            "exceptions": [
                {
                    "rule": "links.internal",
                    "path": "plugins/**/SKILL.md",
                    "rationale": "",
                    "owner": "maintenance",
                    "expires": dt.date(2026, 8, 13),
                    "ticket": "example-1",
                }
            ]
        },
        today=dt.date(2026, 8, 14),
    )
    reasons = [item.reason for item in diagnostics]
    assert any("invalid fields" in reason for reason in reasons)
    assert any("without globs" in reason for reason in reasons)
    assert any("rationale" in reason for reason in reasons)
    assert any("expired" in reason for reason in reasons)


def test_exception_expiration_must_be_a_date() -> None:
    value = {
        "exceptions": [
            {
                "rule": "links.internal",
                "path": "README.md",
                "rationale": "Temporary migration",
                "owner": "maintenance",
                "expires": "later",
            }
        ]
    }
    assert any("ISO date" in item.reason for item in validate(value))
