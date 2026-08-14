from __future__ import annotations

import re

from tools.repo_maintenance.files import relative_path, repository_files
from tools.repo_maintenance.models import CheckContext, CheckSpec, Diagnostic

PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{30,})"),
    "aws-access-key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "openai-api-key": re.compile(r"sk-[A-Za-z0-9]{32,}"),
}


def run(context: CheckContext) -> list[Diagnostic]:
    diagnostics = []
    for path in repository_files(context.root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for name, pattern in PATTERNS.items():
                if pattern.search(line):
                    diagnostics.append(
                        Diagnostic(
                            "secrets.high-confidence",
                            relative_path(context.root, path),
                            f"possible {name}; rotate it if real and remove it from history",
                            line=line_number,
                        )
                    )
    return diagnostics


CHECK = CheckSpec("secrets.high-confidence", frozenset({"secrets", "security", "ci"}), run)
