from __future__ import annotations

import importlib
import pkgutil
from types import ModuleType

from tools.repo_maintenance.models import CheckSpec


class DiscoveryError(RuntimeError):
    """A maintenance check package could not be discovered safely."""


def discover_checks(package_name: str = "tools.repo_maintenance.checks") -> list[CheckSpec]:
    try:
        package = importlib.import_module(package_name)
    except Exception as exc:
        raise DiscoveryError(f"cannot import check package {package_name!r}: {exc}") from exc

    package_path = getattr(package, "__path__", None)
    if package_path is None:
        raise DiscoveryError(f"check package {package_name!r} has no package path")

    modules = sorted(
        info.name for info in pkgutil.iter_modules(package_path) if info.name.startswith("check_")
    )
    checks: list[CheckSpec] = []
    seen: dict[str, str] = {}
    for module_name in modules:
        qualified_name = f"{package_name}.{module_name}"
        try:
            module = importlib.import_module(qualified_name)
        except Exception as exc:
            raise DiscoveryError(f"cannot import check module {qualified_name!r}: {exc}") from exc
        check = _module_check(module, qualified_name)
        if check.check_id in seen:
            raise DiscoveryError(
                f"duplicate check id {check.check_id!r} in {seen[check.check_id]!r} "
                f"and {qualified_name!r}"
            )
        seen[check.check_id] = qualified_name
        checks.append(check)
    return checks


def _module_check(module: ModuleType, qualified_name: str) -> CheckSpec:
    check = getattr(module, "CHECK", None)
    if not isinstance(check, CheckSpec):
        raise DiscoveryError(f"check module {qualified_name!r} must export CHECK: CheckSpec")
    if not check.check_id or not check.targets:
        raise DiscoveryError(f"check module {qualified_name!r} has an empty id or target set")
    return check
