# Core maintenance commands. Checks never sync dependencies or use the network.

maintenance_python := env_var_or_default("MAINTENANCE_PYTHON", "python3.13")

_require-uv:
    @if PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path >/dev/null 2>&1; then exit 0; fi; \
    echo "error: required tool 'uv' is missing; run 'just bootstrap-uv' or install uv, then run 'just doctor'" >&2; exit 1

# Report whether required and optional maintenance tools are available.
doctor:
    @status=0; \
    if command -v just >/dev/null 2>&1; then echo "required  just: $(just --version)"; else echo "required  just: MISSING (install just)"; status=1; fi; \
    if command -v {{quote(maintenance_python)}} >/dev/null 2>&1; then python_version="$({{quote(maintenance_python)}} --version 2>&1)"; if [[ "$python_version" == "Python 3.13"* ]]; then echo "required  python3.13: $python_version"; else echo "required  python3.13: WRONG VERSION ($python_version; install Python 3.13)"; status=1; fi; else echo "required  python3.13: MISSING (install Python 3.13)"; status=1; fi; \
    if uv_path="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path 2>/dev/null)"; then echo "required  uv: $("$uv_path" --version)"; \
    else echo "required  uv: MISSING (run 'just bootstrap-uv' or install uv)"; status=1; fi; \
    if command -v shellcheck >/dev/null 2>&1; then echo "optional  shellcheck: $(shellcheck --version | awk '/version:/ {print $2}')"; else echo "optional  shellcheck: SKIP (not installed)"; fi; \
    if command -v pwsh >/dev/null 2>&1; then \
      echo "optional  powershell: $(pwsh -NoLogo -NoProfile -Command '$PSVersionTable.PSVersion.ToString()')"; \
      if pwsh -NoLogo -NoProfile -Command 'Get-Module -ListAvailable PSScriptAnalyzer | Select-Object -First 1' | grep -q .; then echo "optional  PSScriptAnalyzer: available"; else echo "optional  PSScriptAnalyzer: SKIP (not installed)"; fi; \
    else echo "optional  powershell: SKIP (not installed)"; echo "optional  PSScriptAnalyzer: SKIP (PowerShell unavailable)"; fi; \
    exit $status

# Create a Git-ignored Python 3.13 environment containing the pinned uv tool.
bootstrap-uv:
    PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv ensure

# Create/update the project-local environment from the committed lockfile.
setup: bootstrap-uv
    @uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never "$uv_cmd" sync --project tools/maintenance --locked

# Format maintenance Python and tests.
fmt: _require-uv
    @cache="$(mktemp -d)"; trap 'rm -rf "$cache"' EXIT; \
    uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never RUFF_CACHE_DIR="$cache/ruff" "$uv_cmd" run --project tools/maintenance --frozen --no-sync ruff format --config tools/maintenance/pyproject.toml tools/repo_maintenance; \
    UV_PYTHON_DOWNLOADS=never RUFF_CACHE_DIR="$cache/ruff" "$uv_cmd" run --project tools/maintenance --frozen --no-sync ruff check --config tools/maintenance/pyproject.toml --fix tools/repo_maintenance

# Verify maintenance Python formatting and lint without modifying files.
fmt-check: _require-uv
    @cache="$(mktemp -d)"; trap 'rm -rf "$cache"' EXIT; \
    uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never RUFF_CACHE_DIR="$cache/ruff" "$uv_cmd" run --project tools/maintenance --frozen --no-sync ruff format --config tools/maintenance/pyproject.toml --check tools/repo_maintenance; \
    UV_PYTHON_DOWNLOADS=never RUFF_CACHE_DIR="$cache/ruff" "$uv_cmd" run --project tools/maintenance --frozen --no-sync ruff check --config tools/maintenance/pyproject.toml tools/repo_maintenance

# Run deterministic maintenance tests, optionally narrowed to a topic.
test target="": _require-uv
    @cache="$(mktemp -d)"; trap 'rm -rf "$cache"' EXIT; \
    export PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX="$cache/pycache" XDG_CACHE_HOME="$cache/xdg"; \
    uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never "$uv_cmd" run --project tools/maintenance --frozen --no-sync python -m tools.repo_maintenance test {{quote(target)}}

# Run repository parsers and structural validation, optionally by target.
validate target="": _require-uv
    @cache="$(mktemp -d)"; trap 'rm -rf "$cache"' EXIT; \
    export PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX="$cache/pycache" XDG_CACHE_HOME="$cache/xdg"; \
    uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never "$uv_cmd" run --project tools/maintenance --frozen --no-sync python -m tools.repo_maintenance validate {{quote(target)}}

# Run the complete offline, read-only quality gate.
check: fmt-check validate test go-review-test bhe-development-test
