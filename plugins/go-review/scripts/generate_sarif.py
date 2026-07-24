#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Generate go-review SARIF from finding frontmatter."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SEVERITY_ORDER = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
SEVERITY_LEVEL = {"LOW": "note", "MEDIUM": "warning", "HIGH": "error", "CRITICAL": "error"}
FILTER_MIN = {"all": 1, "medium": 2, "high": 3}
SURVIVOR_VERDICTS = {"TRUE_POSITIVE", "LIKELY_TP"}
CONFIDENCE_TO_SEVERITY = {"HIGH": "MEDIUM", "MEDIUM": "MEDIUM", "LOW": "LOW"}

RULE_DESCRIPTIONS = {
    "missing-route-authorization": "Service entry point reaches privileged logic without authorization",
    "tenant-isolation-bypass": "Tenant-scoped data access omits ownership or tenant isolation",
    "confused-deputy": "Privileged backend action is performed on behalf of an untrusted caller",
    "unbounded-request-body": "Request parsing allows unbounded body or multipart resource use",
    "decoder-fail-open": "Decoder or parser errors fail open on attacker input",
    "trusted-header-spoofing": "Service trusts attacker-controlled headers or metadata as identity",
    "ssrf": "Attacker-controlled destination reaches outbound network requests",
    "redirect-credential-leak": "Redirect handling leaks credentials or internal headers",
    "missing-http-timeout": "Outbound HTTP request lacks bounded timeout or cancellation",
    "sql-injection": "Attacker input reaches SQL construction unsafely",
    "tenant-filter-omission": "Storage query omits tenant or owner scoping",
    "transaction-boundary": "Security-relevant state change crosses an unsafe transaction boundary",
    "ignored-query-error": "Storage error handling fails open or discards important failures",
    "command-injection": "Attacker input reaches command construction or execution",
    "path-env-hijack": "Command execution trusts attacker-influenced PATH, env, or cwd",
    "unsafe-shell-invocation": "Shell invocation is used where direct argv execution is required",
    "text-template-html": "text/template is used for browser-facing HTML output",
    "unsafe-template-bypass": "Template escaping is bypassed for attacker-controlled content",
    "response-header-injection": "Attacker data reaches response headers or redirects unsafely",
    "path-traversal": "Attacker-controlled path escapes an intended filesystem root",
    "archive-slip": "Archive extraction allows path or symlink escape",
    "symlink-toctou": "Filesystem trust check races with symlink or rename behavior",
    "unsafe-temp-file": "Temporary file handling is predictable or overly permissive",
    "jwt-validation": "JWT verification omits critical validation or trusts unsafe algorithms",
    "weak-token-randomness": "Security token generation uses predictable randomness",
    "tls-misconfiguration": "TLS configuration weakens peer or transport validation",
    "cookie-session-flags": "Cookie or session configuration omits important security flags",
    "timing-unsafe-compare": "Secret comparison is not constant-time",
    "shared-map-race": "Concurrent handlers access shared map or state unsafely",
    "goroutine-leak": "Attacker-influenced work leaks goroutines, timers, or channels",
    "missing-context-cancellation": "Request cancellation is not propagated to dependent work",
    "auth-cache-race": "Authorization or session cache race weakens access control",
    "unsafe-pointer-lifetime": "Unsafe pointer lifetime crosses Go or GC invariants",
    "cgo-ownership-confusion": "cgo memory ownership or lifetime is mismatched",
    "length-truncation": "Length conversion across Go and C boundaries truncates attacker input",
}


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    frontmatter = text[4:end]
    body = text[end + len("\n---") :].lstrip("\n")
    return parse_frontmatter(frontmatter), body


def parse_frontmatter(frontmatter: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in frontmatter.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("  - ") and current_key:
            result.setdefault(current_key, []).append(parse_scalar(line[4:]))
            continue
        if ":" not in line or line.startswith((" ", "\t")):
            current_key = None
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        current_key = key
        if value == "":
            result[key] = []
        else:
            result[key] = parse_scalar(value)
    return result


def _split_inline_list(inner: str) -> list[str]:
    parts: list[str] = []
    buffer: list[str] = []
    quote: str | None = None
    for char in inner:
        if quote:
            buffer.append(char)
            if char == quote:
                quote = None
        elif char in ('"', "'"):
            quote = char
            buffer.append(char)
        elif char == ",":
            parts.append("".join(buffer).strip())
            buffer = []
        else:
            buffer.append(char)
    if buffer:
        parts.append("".join(buffer).strip())
    return parts


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part) for part in _split_inline_list(inner)]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    return value


def parse_context(output_dir: Path) -> dict[str, Any]:
    path = output_dir / "context.md"
    if not path.is_file():
        return {}
    frontmatter, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    return frontmatter


def iter_findings(output_dir: Path) -> list[dict[str, Any]]:
    index = output_dir / "findings-index.txt"
    if index.is_file():
        paths = [Path(line.strip()) for line in index.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        paths = sorted((output_dir / "findings").glob("*.md"))
    findings: list[dict[str, Any]] = []
    for path in paths:
        if not path.is_absolute():
            path = output_dir / path
        try:
            frontmatter, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, AttributeError) as exc:
            print(f"warning: skipping {path}: {exc}", file=sys.stderr)
            continue
        frontmatter["_path"] = str(path)
        findings.append(frontmatter)
    return findings


def normalize_path(path: str) -> str:
    value = path.replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    while "//" in value:
        value = value.replace("//", "/")
    return value


def location_parts(location: Any) -> tuple[str, int]:
    value = str(location or "")
    match = re.match(r"^\[([^\]]+)\]\([^)]+\):(\d+)$", value)
    if match:
        return normalize_path(match.group(1)), max(1, int(match.group(2)))
    path, sep, line = value.rpartition(":")
    if sep and line.isdecimal():
        return normalize_path(path), max(1, int(line))
    return normalize_path(value), 1


def severity_allowed(severity: str, severity_filter: str) -> bool:
    return SEVERITY_ORDER.get(severity, 0) >= FILTER_MIN.get(severity_filter, 1)


def build_sarif(output_dir: Path) -> dict[str, Any]:
    context = parse_context(output_dir)
    severity_filter = str(context.get("severity_filter", "all")).lower()
    threat_model = str(context.get("threat_model", "UNKNOWN"))
    all_findings = iter_findings(output_dir)
    surviving_primary_ids = {
        str(finding["id"])
        for finding in all_findings
        if finding.get("id")
        and not finding.get("merged_into")
        and str(finding.get("fp_verdict", "LIKELY_TP")).upper() in SURVIVOR_VERDICTS
    }
    findings: list[dict[str, Any]] = []
    for finding in all_findings:
        merged_into = finding.get("merged_into")
        if merged_into and str(merged_into) in surviving_primary_ids:
            continue
        verdict = str(finding.get("fp_verdict", "LIKELY_TP")).upper()
        if verdict not in SURVIVOR_VERDICTS:
            continue
        severity = str(
            finding.get(
                "severity",
                CONFIDENCE_TO_SEVERITY.get(str(finding.get("confidence", "MEDIUM")).upper(), "MEDIUM"),
            )
        ).upper()
        if not severity_allowed(severity, severity_filter):
            continue
        normalized = dict(finding)
        normalized["fp_verdict"] = verdict
        normalized["severity"] = severity
        findings.append(normalized)

    bug_classes = sorted({str(finding.get("bug_class", "unknown")) for finding in findings})
    rules = []
    for bug_class in bug_classes:
        max_severity = max(
            (str(finding["severity"]) for finding in findings if finding.get("bug_class") == bug_class),
            key=lambda value: SEVERITY_ORDER.get(value, 0),
        )
        rules.append(
            {
                "id": bug_class,
                "shortDescription": {"text": RULE_DESCRIPTIONS.get(bug_class, bug_class.replace("-", " ").title())},
                "defaultConfiguration": {"level": SEVERITY_LEVEL.get(max_severity, "warning")},
            }
        )

    results = []
    for finding in findings:
        path, line = location_parts(finding.get("location"))
        results.append(
            {
                "ruleId": str(finding.get("bug_class", "unknown")),
                "level": SEVERITY_LEVEL.get(str(finding["severity"]), "warning"),
                "message": {"text": str(finding.get("title", finding.get("id", "finding")))},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": path},
                            "region": {"startLine": line},
                        }
                    }
                ],
                "properties": {
                    "finding_id": finding.get("id"),
                    "bug_class": finding.get("bug_class"),
                    "severity": finding.get("severity"),
                    "fp_verdict": finding.get("fp_verdict"),
                    "attack_vector": finding.get("attack_vector"),
                    "exploitability": finding.get("exploitability"),
                    "threat_model": threat_model,
                    "function": finding.get("function"),
                },
            }
        )

    return {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "go-review",
                        "rules": rules,
                    }
                },
                "results": results,
            }
        ],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    sarif = build_sarif(args.output_dir)
    output = args.output or args.output_dir / "REPORT.sarif"
    output.write_text(json.dumps(sarif, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
