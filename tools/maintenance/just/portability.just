# Check authored paths, temporary outputs, syntax, encoding, and executable modes.
check-portability: _require-uv
    @uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never "$uv_cmd" run --project tools/maintenance --frozen --no-sync python -m tools.repo_maintenance.portability check

# Verify every tracked PE artifact against its immutable provenance inventory.
check-provenance: _require-uv
    @uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never "$uv_cmd" run --project tools/maintenance --frozen --no-sync python -m tools.repo_maintenance.portability provenance

# Run PowerShell parser and PSScriptAnalyzer checks when their platform tools exist.
check-powershell: _require-uv
    @uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never "$uv_cmd" run --project tools/maintenance --frozen --no-sync python -m tools.repo_maintenance.portability powershell
