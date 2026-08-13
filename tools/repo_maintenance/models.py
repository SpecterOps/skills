from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, order=True)
class Diagnostic:
    rule: str
    path: str
    reason: str
    line: int | None = None
    column: int | None = None

    def render(self) -> str:
        location = self.path
        if self.line is not None:
            location += f":{self.line}"
            if self.column is not None:
                location += f":{self.column}"
        return f"{self.rule}: {location}: {self.reason}"


@dataclass(frozen=True)
class CheckContext:
    root: Path


CheckRunner = Callable[[CheckContext], list[Diagnostic]]


@dataclass(frozen=True)
class CheckSpec:
    check_id: str
    targets: frozenset[str]
    run: CheckRunner
