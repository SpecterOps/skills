# Regenerate tracked marketplace files and the marked README plugin table.
generate-catalog: _require-uv
    @uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never "$uv_cmd" run --project tools/maintenance --frozen --no-sync python -m tools.repo_maintenance.generators.catalog generate

# Validate lifecycle, ownership, manifests, and generated catalog drift.
check-catalog: _require-uv
    @uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never "$uv_cmd" run --project tools/maintenance --frozen --no-sync python -m tools.repo_maintenance.generators.catalog check

# Regenerate root skill, agent, and MCP inventory regions.
generate-inventory: _require-uv
    @uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never "$uv_cmd" run --project tools/maintenance --frozen --no-sync python -m tools.repo_maintenance.generators.inventory generate

# Validate generated root skill, agent, and MCP inventory regions.
check-inventory: _require-uv
    @uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never "$uv_cmd" run --project tools/maintenance --frozen --no-sync python -m tools.repo_maintenance.generators.inventory check

# Plan metadata-only plugin scaffolding; pass mode=apply to create it.
scaffold-plugin-metadata name description mode="plan": _require-uv
    @uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never "$uv_cmd" run --project tools/maintenance --frozen --no-sync python -m tools.repo_maintenance.scaffold {{quote(mode)}} {{quote(name)}} {{quote(description)}}
