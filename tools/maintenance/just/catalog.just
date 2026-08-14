# Regenerate tracked marketplace files and the marked README plugin table.
generate-catalog: _require-uv
    @uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never "$uv_cmd" run --project tools/maintenance --frozen --no-sync python -m tools.repo_maintenance.generators.catalog generate

# Validate lifecycle, ownership, manifests, and generated catalog drift.
check-catalog: _require-uv
    @uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never "$uv_cmd" run --project tools/maintenance --frozen --no-sync python -m tools.repo_maintenance.generators.catalog check
