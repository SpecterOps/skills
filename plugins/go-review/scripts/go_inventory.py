#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Build a conservative Go source inventory for service-focused security review."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


IGNORED_DIRS = {".git", "vendor", "node_modules", ".go-review-results"}
SERVICE_IMPORTS = {
    "net/http": "net/http",
    "google.golang.org/grpc": "grpc",
    "github.com/gin-gonic/gin": "gin",
    "github.com/labstack/echo": "echo",
    "github.com/go-chi/chi": "chi",
    "github.com/gofiber/fiber": "fiber",
    "github.com/gorilla/mux": "gorilla/mux",
}
SQL_IMPORT_PREFIXES = (
    "database/sql",
    "github.com/jmoiron/sqlx",
    "github.com/jackc/pgx",
    "gorm.io/gorm",
    "entgo.io/ent",
)
CRYPTO_AUTH_IMPORT_PREFIXES = (
    "crypto/",
    "golang.org/x/crypto",
    "github.com/golang-jwt/jwt",
    "github.com/dgrijalva/jwt-go",
    "github.com/gorilla/sessions",
)


def normalize_path(path: Path, repo_root: Path) -> str:
    return str(path.relative_to(repo_root)).replace("\\", "/")


def discover_go_files(repo_root: Path, scope_subpath: str) -> list[Path]:
    scope = (repo_root / scope_subpath).resolve()
    if scope.is_file() and scope.suffix == ".go":
        candidates = [scope]
    elif scope.is_dir():
        candidates = sorted(scope.rglob("*.go"))
    else:
        candidates = []
    files = []
    for path in candidates:
        try:
            path.relative_to(repo_root)
        except ValueError:
            continue
        if path.name.endswith("_test.go"):
            continue
        if any(part in IGNORED_DIRS for part in path.relative_to(repo_root).parts):
            continue
        files.append(path)
    return files


def read_module(repo_root: Path) -> str | None:
    go_mod = repo_root / "go.mod"
    if not go_mod.is_file():
        return None
    match = re.search(r"(?m)^module\s+(\S+)", go_mod.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def parse_imports(text: str) -> list[str]:
    imports: list[str] = []
    for match in re.finditer(r'(?m)^\s*import\s+(?:[A-Za-z_][A-Za-z0-9_]*\s+)?"([^"]+)"', text):
        imports.append(match.group(1))
    for block in re.finditer(r"(?ms)^\s*import\s*\((.*?)^\s*\)", text):
        for match in re.finditer(r'(?:^|\n)\s*(?:[A-Za-z_][A-Za-z0-9_]*\s+)?"([^"]+)"', block.group(1)):
            imports.append(match.group(1))
    return sorted(set(imports))


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def parse_functions(text: str) -> list[dict[str, Any]]:
    functions: list[dict[str, Any]] = []
    pattern = re.compile(
        r"(?m)^\s*func\s+(?:(\([^)]*\))\s*)?([A-Za-z_][A-Za-z0-9_]*)\s*\("
    )
    for match in pattern.finditer(text):
        receiver = match.group(1)
        name = match.group(2)
        functions.append(
            {
                "name": name,
                "receiver": receiver,
                "exported": name[:1].isupper(),
                "line": line_number(text, match.start()),
            }
        )
    return functions


def detect_routes(text: str) -> list[dict[str, Any]]:
    routes: list[dict[str, Any]] = []
    patterns = [
        (re.compile(r'\b(?:http\.)?HandleFunc\s*\(\s*"([^"]+)"'), "HandleFunc"),
        (re.compile(r'\b(?:http\.)?Handle\s*\(\s*"([^"]+)"'), "Handle"),
        (
            re.compile(r'\b[A-Za-z_][A-Za-z0-9_]*\.(GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD)\s*\(\s*"([^"]+)"'),
            "router-method",
        ),
        (
            re.compile(r'\b[A-Za-z_][A-Za-z0-9_]*\.(Handle|HandleFunc|MethodFunc)\s*\(\s*"([^"]+)"'),
            "router-handle",
        ),
    ]
    for pattern, kind in patterns:
        for match in pattern.finditer(text):
            if kind == "router-method":
                method, path = match.group(1), match.group(2)
            else:
                method, path = None, match.group(1)
            routes.append(
                {
                    "kind": kind,
                    "method": method,
                    "path": path,
                    "line": line_number(text, match.start()),
                }
            )
    for match in re.finditer(r"\bRegister([A-Za-z_][A-Za-z0-9_]*)Server\s*\(", text):
        routes.append(
            {
                "kind": "grpc-register",
                "service": match.group(1),
                "line": line_number(text, match.start()),
            }
        )
    return routes


def contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def derive_capability_flags(files: list[dict[str, Any]]) -> dict[str, bool]:
    imports = {item for file in files for item in file["imports"]}
    source = "\n".join(file["source_text"] for file in files)
    has_service = bool(
        imports & set(SERVICE_IMPORTS)
        or contains_any(
            source,
            (
                r"\bhttp\.(?:Handle|HandleFunc|ListenAndServe|Serve)\s*\(",
                r"\bgrpc\.(?:NewServer|Serve)\s*\(",
                r"\bRegister[A-Za-z_][A-Za-z0-9_]*Server\s*\(",
                r"\b[A-Za-z_][A-Za-z0-9_]*\.(?:GET|POST|PUT|PATCH|DELETE|Handle|HandleFunc)\s*\(",
            ),
        )
    )
    has_outbound_http = contains_any(
        source,
        (
            r"\bhttp\.(?:Get|Post|PostForm|Head|NewRequest|NewRequestWithContext)\s*\(",
            r"\b[A-Za-z_][A-Za-z0-9_]*\.(?:Do|RoundTrip)\s*\(",
        ),
    )
    has_sql = any(item.startswith(SQL_IMPORT_PREFIXES) for item in imports) or contains_any(
        source,
        (
            r"\b[A-Za-z_][A-Za-z0-9_]*\.(?:Query|QueryContext|Exec|ExecContext|Raw|Where|First|Find)\s*\(",
        ),
    )
    has_exec = "os/exec" in imports or contains_any(
        source,
        (r"\bexec\.(?:Command|CommandContext)\s*\(", r'\b(?:sh|bash)\s+-c\b'),
    )
    has_fs_archive = contains_any(
        source,
        (
            r"\b(?:os|ioutil)\.(?:Open|OpenFile|Create|ReadFile|WriteFile|Mkdir|MkdirAll|TempFile|CreateTemp|Rename)\s*\(",
            r"\bfilepath\.(?:Join|Clean|Walk|WalkDir|Abs|Rel)\s*\(",
            r"\b(?:zip|tar)\.(?:NewReader|NewWriter)\s*\(",
            r"\barchive/(?:zip|tar)\b",
        ),
    )
    has_template = (
        "html/template" in imports
        or "text/template" in imports
        or contains_any(source, (r"\btemplate\.(?:New|ParseFiles|ParseGlob|Must)\s*\(", r"\.Execute(?:Template)?\s*\("))
    )
    has_crypto_auth = any(item.startswith(CRYPTO_AUTH_IMPORT_PREFIXES) for item in imports) or contains_any(
        source,
        (
            r"\b(?:jwt|tls|subtle)\.",
            r"\bhttp\.Cookie\b",
            r"\bSameSite\b",
            r"\bInsecureSkipVerify\b",
            r"\bmath/rand\b",
        ),
    )
    has_concurrency = (
        "sync" in imports
        or "sync/atomic" in imports
        or contains_any(source, (r"(?m)^\s*go\s+", r"\bmake\s*\(\s*chan\b", r"\bchan\s+[A-Za-z_]"))
    )
    has_unsafe_cgo = "unsafe" in imports or "C" in imports or contains_any(
        source,
        (r"\bunsafe\.", r'(?m)^\s*import\s+"C"', r"(?m)^\s*//\s*#cgo\b"),
    )
    return {
        "has_service": has_service,
        "has_outbound_http": has_outbound_http,
        "has_sql": has_sql,
        "has_exec": has_exec,
        "has_fs_archive": has_fs_archive,
        "has_template": has_template,
        "has_crypto_auth": has_crypto_auth,
        "has_concurrency": has_concurrency,
        "has_unsafe_cgo": has_unsafe_cgo,
    }


def build_inventory(repo_root: Path, *, scope_subpath: str = ".") -> dict[str, Any]:
    repo_root = repo_root.resolve()
    file_records: list[dict[str, Any]] = []
    frameworks: set[str] = set()
    packages: set[str] = set()
    entrypoints: list[dict[str, Any]] = []
    for path in discover_go_files(repo_root, scope_subpath):
        text = path.read_text(encoding="utf-8")
        imports = parse_imports(text)
        package_match = re.search(r"(?m)^\s*package\s+([A-Za-z_][A-Za-z0-9_]*)", text)
        package = package_match.group(1) if package_match else None
        routes = detect_routes(text)
        functions = parse_functions(text)
        record = {
            "path": normalize_path(path, repo_root),
            "package": package,
            "imports": imports,
            "functions": functions,
            "routes": routes,
            "source_text": text,
        }
        file_records.append(record)
        if package:
            packages.add(package)
        for imported, framework in SERVICE_IMPORTS.items():
            if imported in imports:
                frameworks.add(framework)
        for route in routes:
            entrypoints.append({"file": record["path"], **route})
    flags = derive_capability_flags(file_records)
    public_file_records = [
        {key: value for key, value in record.items() if key != "source_text"}
        for record in file_records
    ]
    return {
        "version": 1,
        "repo_root": str(repo_root),
        "scope_subpath": scope_subpath,
        "module": read_module(repo_root),
        "files": public_file_records,
        "frameworks": sorted(frameworks),
        "entrypoints": entrypoints,
        "capability_flags": flags,
        "summary": {
            "go_file_count": len(file_records),
            "package_count": len(packages),
            "entrypoint_count": len(entrypoints),
            "framework_count": len(frameworks),
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--scope-subpath", default=".")
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        inventory = build_inventory(args.repo_root, scope_subpath=args.scope_subpath)
    except (OSError, ValueError) as exc:
        print(f"go_inventory: {exc}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(inventory["summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
