#!/usr/bin/env python3
"""Fetch curated BloodHound/OpenGraph saved-query snapshots and regenerate indexes.

This intentionally uses only the Python standard library so the repository can be
maintained without a virtualenv. It vendors upstream query files as snapshots for
agent reference, plus a compact manifest and markdown indexes for skills.
"""
from __future__ import annotations

import base64
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_ROOT = PLUGIN_ROOT / "references" / "query-snapshots"
INDEX_ROOT = PLUGIN_ROOT / "references" / "query-indexes"

SOURCES = [
    {
        "id": "bloodhound-query-library",
        "domain": "bloodhound",
        "repo": "SpecterOps/BloodHoundQueryLibrary",
        "branch": "main",
        "path": "queries",
        "dest": "bloodhound-query-library/queries",
        "extensions": [".yml", ".yaml"],
        "license": "MIT",
        "upstream_url": "https://github.com/SpecterOps/BloodHoundQueryLibrary/tree/main/queries",
    },
    {
        "id": "openhound-github",
        "domain": "openhound-github",
        "repo": "SpecterOps/GitHound",
        "branch": "main",
        "path": "saved-queries",
        "dest": "openhound-github/saved-queries",
        "extensions": [".json"],
        "license": "Apache-2.0",
        "upstream_url": "https://github.com/SpecterOps/GitHound/tree/main/saved-queries",
    },
    {
        "id": "openhound-jamf",
        "domain": "openhound-jamf",
        "repo": "SpecterOps/openhound-jamf",
        "branch": "main",
        "path": "extension/saved_searches",
        "dest": "openhound-jamf/saved-searches",
        "extensions": [".json"],
        "license": "Apache-2.0",
        "upstream_url": "https://github.com/SpecterOps/openhound-jamf/tree/main/extension/saved_searches",
    },
    {
        "id": "openhound-okta",
        "domain": "openhound-okta",
        "repo": "SpecterOps/openhound-okta",
        "branch": "main",
        "path": "extension/saved_searches",
        "dest": "openhound-okta/saved-searches",
        "extensions": [".json"],
        "license": "Apache-2.0",
        "upstream_url": "https://github.com/SpecterOps/openhound-okta/tree/main/extension/saved_searches",
    },
]


def fetch_json(url: str) -> Any:
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "specter-codex-config"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "specter-codex-config"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read().decode("utf-8")


def repo_commit(repo: str, branch: str) -> str:
    data = fetch_json(f"https://api.github.com/repos/{repo}/commits/{urllib.parse.quote(branch)}")
    return data["sha"]


def list_contents(repo: str, path: str, branch: str) -> list[dict[str, Any]]:
    url = f"https://api.github.com/repos/{repo}/contents/{urllib.parse.quote(path)}?ref={urllib.parse.quote(branch)}"
    data = fetch_json(url)
    if not isinstance(data, list):
        raise RuntimeError(f"Expected directory listing for {repo}/{path}")
    return data


def clear_dest(dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for item in dest.iterdir():
        if item.is_file():
            item.unlink()


def rel(path: Path) -> str:
    return path.relative_to(PLUGIN_ROOT).as_posix()


def first_scalar(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.*)$", text)
    if not match:
        return ""
    value = match.group(1).strip()
    return value.strip('"\'')


def yaml_block_list(text: str, key: str) -> list[str]:
    lines = text.splitlines()
    values: list[str] = []
    for i, line in enumerate(lines):
        if line.startswith(f"{key}:"):
            rest = line.split(":", 1)[1].strip()
            if rest and not rest.startswith("|"):
                return [part.strip().strip('"\'') for part in re.split(r",\s*", rest.strip("[]")) if part.strip()]
            for follow in lines[i + 1 :]:
                if not follow.startswith((" ", "-")):
                    break
                stripped = follow.strip()
                if stripped.startswith("-"):
                    values.append(stripped[1:].strip().strip('"\''))
            break
    return values


def yaml_query(text: str) -> str:
    marker = re.search(r"(?m)^query:\s*(\|-?|>-?)\s*$", text)
    if marker:
        body = text[marker.end() :]
        out: list[str] = []
        for line in body.splitlines():
            if line and not line.startswith((" ", "\t")):
                break
            out.append(line[2:] if line.startswith("  ") else line.lstrip())
        return "\n".join(out).strip()
    match = re.search(r"(?m)^query:\s*(.*)$", text)
    return match.group(1).strip() if match else ""


def json_query(data: dict[str, Any]) -> str:
    value = data.get("query") or data.get("cypher") or ""
    return str(value)


def summarize_yaml(file_path: Path, source: dict[str, Any]) -> dict[str, Any]:
    text = file_path.read_text(encoding="utf-8")
    platforms = yaml_block_list(text, "platforms")
    if not platforms:
        scalar = first_scalar(text, "platforms")
        platforms = [scalar] if scalar else []
    platform_text = " ".join(platforms).lower()
    if "azure" in platform_text or "entra" in platform_text or re.search(r"\bAZ[A-Za-z0-9_]+\b", yaml_query(text)):
        domain = "azurehound"
    else:
        domain = "bloodhound"
    return {
        "domain": domain,
        "name": first_scalar(text, "name") or file_path.stem,
        "category": first_scalar(text, "category") or "Uncategorized",
        "description": first_scalar(text, "description"),
        "platforms": platforms,
        "path": rel(file_path),
        "source": source["id"],
        "query": yaml_query(text),
    }


def summarize_json(file_path: Path, source: dict[str, Any]) -> dict[str, Any]:
    data = json.loads(file_path.read_text(encoding="utf-8"))
    return {
        "domain": source["domain"],
        "name": str(data.get("name") or file_path.stem),
        "category": str(data.get("category") or data.get("platform") or source["domain"]),
        "description": str(data.get("description") or ""),
        "platforms": [source["domain"]],
        "path": rel(file_path),
        "source": source["id"],
        "query": json_query(data),
    }


def clean_cell(value: str, max_len: int = 140) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    value = value.replace("|", "\\|")
    if len(value) > max_len:
        return value[: max_len - 1].rstrip() + "…"
    return value


def write_index(domain: str, entries: list[dict[str, Any]], manifest: dict[str, Any]) -> None:
    title = {
        "bloodhound": "BloodHound AD/ADCS Query Index",
        "azurehound": "AzureHound / Entra ID Query Index",
        "openhound-github": "OpenHound GitHub Query Index",
        "openhound-jamf": "OpenHound Jamf Query Index",
        "openhound-okta": "OpenHound Okta Query Index",
    }[domain]
    INDEX_ROOT.mkdir(parents=True, exist_ok=True)
    out = INDEX_ROOT / f"{domain}.md"
    lines = [
        f"# {title}",
        "",
        "Generated from vendored upstream saved-query snapshots. Use this file to find starting points; inspect the referenced snapshot before adapting a query.",
        "",
        f"- Generated: `{manifest['retrieved_at']}`",
        f"- Query count: `{len(entries)}`",
        "",
        "| Query | Category / Platform | Snapshot | Notes |",
        "| --- | --- | --- | --- |",
    ]
    for entry in sorted(entries, key=lambda e: (e.get("category", ""), e.get("name", ""))):
        notes = clean_cell(entry.get("description", ""), 110)
        category = clean_cell(", ".join(entry.get("platforms") or []) or entry.get("category", ""), 60)
        if entry.get("category") and entry.get("category") not in category:
            category = clean_cell(f"{entry['category']} ({category})", 70)
        lines.append(f"| {clean_cell(entry['name'], 80)} | {category} | `{entry['path']}` | {notes} |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_notice(manifest: dict[str, Any]) -> None:
    lines = [
        "# Query Snapshot Notice",
        "",
        "This directory contains vendored snapshots of upstream saved-query files for agent reference and offline query adaptation.",
        "The snapshots are not a replacement for upstream documentation; refresh them with `scripts/update-query-snapshots.py` before publishing a release.",
        "",
        "| Source | Snapshot commit | License | Upstream | Files |",
        "| --- | --- | --- | --- | ---: |",
    ]
    for source in manifest["sources"]:
        lines.append(
            f"| {source['repo']} | `{source['commit']}` | {source['license']} | {source['upstream_url']} | {source['file_count']} |"
        )
    (SNAPSHOT_ROOT / "NOTICE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_safety_report(entries: Iterable[dict[str, Any]]) -> None:
    write_clause = re.compile(r"\b(CREATE|MERGE|DELETE|DETACH\s+DELETE|SET|REMOVE|DROP)\b", re.IGNORECASE)
    broad_without_limit: list[dict[str, Any]] = []
    write_hits: list[tuple[dict[str, Any], str]] = []
    for entry in entries:
        query = entry.get("query", "")
        # Strip line comments before conservative write-clause scanning so docs
        # comments such as "password last set" do not look like mutations.
        scan_query = "\n".join(line.split("//", 1)[0] for line in query.splitlines())
        if hit := write_clause.search(scan_query):
            write_hits.append((entry, hit.group(0)))
        if re.search(r"(?i)\bMATCH\s*\(\s*\w*\s*\)", scan_query) and not re.search(r"(?i)\bLIMIT\b", scan_query):
            broad_without_limit.append(entry)
    lines = [
        "# Query Snapshot Safety Scan",
        "",
        "Static review helper for vendored query snapshots. This is intentionally conservative and does not replace manual review before running a query against a real BloodHound instance.",
        "",
        f"- Potential write-clause hits: `{len(write_hits)}`",
        f"- Broad node matches without LIMIT: `{len(broad_without_limit)}`",
        "",
    ]
    if write_hits:
        lines += ["## Potential write-clause hits", "", "| Query | Clause | Snapshot |", "| --- | --- | --- |"]
        for entry, clause in write_hits[:100]:
            lines.append(f"| {clean_cell(entry['name'], 80)} | `{clause.upper()}` | `{entry['path']}` |")
        lines.append("")
    if broad_without_limit:
        lines += ["## Broad node matches without LIMIT", "", "| Query | Snapshot |", "| --- | --- |"]
        for entry in broad_without_limit[:100]:
            lines.append(f"| {clean_cell(entry['name'], 80)} | `{entry['path']}` |")
        lines.append("")
    (INDEX_ROOT / "safety-scan.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    retrieved_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    SNAPSHOT_ROOT.mkdir(parents=True, exist_ok=True)
    INDEX_ROOT.mkdir(parents=True, exist_ok=True)
    all_entries: list[dict[str, Any]] = []
    manifest: dict[str, Any] = {"retrieved_at": retrieved_at, "sources": [], "indexes": []}

    for source in SOURCES:
        commit = repo_commit(source["repo"], source["branch"])
        contents = list_contents(source["repo"], source["path"], source["branch"])
        dest = SNAPSHOT_ROOT / source["dest"]
        clear_dest(dest)
        copied: list[Path] = []
        for item in contents:
            if item.get("type") != "file":
                continue
            name = item["name"]
            if not any(name.endswith(ext) for ext in source["extensions"]):
                continue
            if item.get("download_url"):
                text = fetch_text(item["download_url"])
            else:
                file_data = fetch_json(item["url"])
                text = base64.b64decode(file_data["content"]).decode("utf-8")
            target = dest / name
            target.write_text(text, encoding="utf-8")
            copied.append(target)
            if name.endswith((".yml", ".yaml")):
                all_entries.append(summarize_yaml(target, source))
            elif name.endswith(".json"):
                all_entries.append(summarize_json(target, source))
        manifest["sources"].append(
            {
                "id": source["id"],
                "repo": source["repo"],
                "branch": source["branch"],
                "commit": commit,
                "source_path": source["path"],
                "snapshot_path": rel(dest),
                "upstream_url": source["upstream_url"],
                "license": source["license"],
                "file_count": len(copied),
            }
        )

    manifest["total_files"] = sum(source["file_count"] for source in manifest["sources"])
    manifest["domain_counts"] = {domain: sum(1 for entry in all_entries if entry["domain"] == domain) for domain in ["bloodhound", "azurehound", "openhound-github", "openhound-jamf", "openhound-okta"]}
    (SNAPSHOT_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_notice(manifest)
    for domain in ["bloodhound", "azurehound", "openhound-github", "openhound-jamf", "openhound-okta"]:
        write_index(domain, [entry for entry in all_entries if entry["domain"] == domain], manifest)
        manifest["indexes"].append(f"references/query-indexes/{domain}.md")
    (SNAPSHOT_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_safety_report(all_entries)
    print(json.dumps({"total_files": manifest["total_files"], "domain_counts": manifest["domain_counts"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
