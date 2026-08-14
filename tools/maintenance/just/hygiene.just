# Validate first-party Markdown links, anchors, and bundled-resource references.
check-links: _require-uv
    @uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never "$uv_cmd" run --project tools/maintenance --frozen --no-sync python -m tools.repo_maintenance validate links
