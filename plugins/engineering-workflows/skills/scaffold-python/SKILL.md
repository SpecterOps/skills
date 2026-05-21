---
name: scaffold-python
description: Scaffold a new Python project with a src layout, linting, and tests. Prefer uv-based setup and packaging; if uv is unavailable, warn the user, request approval, and use a fallback bootstrap path.
icon: ./assets/icon.png
---

# Scaffold Python

Create a new Python project scaffold with consistent structure and tooling.

## Input Parsing

Accept input as: `PROJECT_NAME`

Examples:
- `$scaffold-python my-tool`

If no project name is provided, ask the user for one before proceeding.

## Preference Policy

- Prefer `uv` for initialization and environment management.
- If `uv` is missing:
  - warn the user that `uv` is preferred,
  - remind them to install `uv`,
  - ask for approval before using a fallback bootstrap path.
- Fallback only after explicit user approval.

Recommended install reminder:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Steps (Preferred: uv)

1. Create the project directory in the current working directory.
2. Run:
   ```bash
   uv init --name <project_name> --package
   ```
3. Ensure structure exists:
   ```text
   <project_name>/
     src/
       <package_name>/
         __init__.py
         main.py
     tests/
       __init__.py
       conftest.py
     .gitignore
     README.md
     pyproject.toml
   ```
4. Ensure `pyproject.toml` includes:
   - Python `>=3.11`
   - dev dependencies: `pytest`, `ruff`, `mypy`
   - Ruff config (line length 88, 4-space indent)
   - mypy strict mode
5. Write `src/<package_name>/__init__.py` with:
   ```python
   __version__ = "0.1.0"
   ```
6. Write `src/<package_name>/main.py` with a minimal `main()` entry point.
7. Write test stubs (`tests/__init__.py`, `tests/conftest.py`).
8. Write `.gitignore` for Python artifacts.
9. Write `README.md` with basic usage:
   ```bash
   uv run python -m <package_name>
   ```
10. Run:
    ```bash
    uv sync
    ```
11. Report created files and next commands.

## Fallback Steps (Only If Approved)

Use only when `uv` is unavailable and user explicitly approves fallback.

1. Create the same project structure.
2. Write/adjust `pyproject.toml` with the same project and tool configuration.
3. Initialize a virtual environment:
   ```bash
   python3 -m venv .venv
   .venv/bin/python -m pip install --upgrade pip
   ```
4. Install developer tools:
   ```bash
   .venv/bin/pip install pytest ruff mypy
   ```
5. Report fallback usage and remind user to install `uv` for future scaffolds.

## Output Requirements

- Report final directory tree.
- Report whether preferred (`uv`) or fallback path was used.
- If fallback was used, include the `uv` install reminder at the end.
