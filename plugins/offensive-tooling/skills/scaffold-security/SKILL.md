---
name: scaffold-security
description: Scaffold a security tool project with CLI, logging, and target handling. Prefer uv-based setup and packaging; if uv is unavailable, warn the user, request approval, and use a fallback bootstrap path.
---

# Scaffold Security

Create a security/pentest tool scaffold with a consistent Python project layout.

## Input Parsing

Accept input as: `TOOL_NAME [DESCRIPTION]`

Examples:
- `$scaffold-security recon-spider`
- `$scaffold-security recon-spider "Async web crawler for subdomain content discovery"`

If no tool name is provided, ask the user for one before proceeding.

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
   uv init --name <tool_name> --package
   ```
3. Ensure structure exists:
   ```text
   <tool_name>/
     src/
       <package_name>/
         __init__.py
         main.py
         cli.py
         core.py
         output.py
     tests/
       __init__.py
       conftest.py
     .gitignore
     README.md
     pyproject.toml
   ```
4. Ensure `pyproject.toml` includes:
   - Python `>=3.11`
   - runtime dependencies: `typer`, `rich`, `pydantic`, `httpx`
   - dev dependencies: `pytest`, `ruff`, `mypy`
   - script entry point mapping tool name to `<package>.cli:app`
   - Ruff config (line length 88, 4-space indent)
5. Implement `cli.py` with:
   - Typer app
   - options for target, ports, output, format, verbose, timeout
   - logging setup using `rich.logging`
   - delegation to `core.py`
6. Implement `core.py` with:
   - typed models for results
   - tool logic class/functions
   - async support where network I/O is expected
7. Implement `output.py` with:
   - formatters for text/json/csv output
   - helper for stdout vs file output
8. Implement `main.py` with `__main__` entry.
9. Write test stubs and basic README usage.
10. Run:
    ```bash
    uv sync
    ```
11. Report created files and example usage.

## Fallback Steps (Only If Approved)

Use only when `uv` is unavailable and user explicitly approves fallback.

1. Create the same project structure.
2. Write/adjust `pyproject.toml` with equivalent project and tool settings.
3. Initialize virtual environment:
   ```bash
   python3 -m venv .venv
   .venv/bin/python -m pip install --upgrade pip
   ```
4. Install dependencies:
   ```bash
   .venv/bin/pip install typer rich pydantic httpx pytest ruff mypy
   ```
5. Report fallback usage and remind user to install `uv` for future scaffolds.

## Output Requirements

- Report final directory tree.
- Report whether preferred (`uv`) or fallback path was used.
- Include a runnable example command for the scaffolded tool.
- If fallback was used, include the `uv` install reminder at the end.
