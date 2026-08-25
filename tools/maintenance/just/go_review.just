# Offline checks for the public go-review plugin.

go-review-test:
    @cache="$(mktemp -d)"; trap 'rm -rf "$cache"' EXIT; \
    GOCACHE="$cache/go-build" go -C plugins/go-review/scripts test ./...; \
    GOCACHE="$cache/go-build" go -C plugins/go-review/scripts vet ./...; \
    PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX="$cache/pycache" python3 -m unittest discover -s plugins/go-review/scripts -p 'test_*.py'
