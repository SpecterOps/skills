# Report whether bundled BloodHound snapshots trail their upstream branches (uses the network).
check-upstream-bloodhound: _require-uv
    @uv_cmd="$(PYTHONDONTWRITEBYTECODE=1 {{quote(maintenance_python)}} -m tools.repo_maintenance.bootstrap_uv path)"; \
    UV_PYTHON_DOWNLOADS=never "$uv_cmd" run --project tools/maintenance --frozen --no-sync python -m tools.repo_maintenance.network_maintenance upstream-bloodhound

# Run offline regression tests for the private BloodHound development plugin.
bhe-development-test:
    plugins/bloodhound-development/tests/run.sh
