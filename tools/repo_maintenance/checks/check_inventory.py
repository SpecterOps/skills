from __future__ import annotations

from tools.repo_maintenance.generators.inventory import check
from tools.repo_maintenance.models import CheckContext, CheckSpec, Diagnostic


def run(context: CheckContext) -> list[Diagnostic]:
    return check(context.root)


CHECK = CheckSpec("inventory.generated", frozenset({"inventory", "skills", "agents"}), run)
