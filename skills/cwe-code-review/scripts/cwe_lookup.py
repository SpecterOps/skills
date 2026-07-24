#!/usr/bin/env python3
"""Search and render the generated CWE review corpus."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable

DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "references" / "cwe-records.jsonl"
DEFAULT_METADATA_PATH = Path(__file__).resolve().parent.parent / "references" / "cwe-catalog-metadata.json"


def normalize_space(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def short_text(value: str, limit: int = 220) -> str:
    value = normalize_space(value)
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def load_records(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_metadata(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_id(value: str) -> str:
    match = re.fullmatch(r"(?:CWE-)?(\d+)", value.strip(), re.IGNORECASE)
    return match.group(1) if match else value.strip()


def flatten_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(flatten_text(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(flatten_text(item) for item in value)
    return str(value)


def score_query(record: dict[str, Any], query: str) -> int:
    if normalize_id(query) == record["id"]:
        return 100
    terms = [term for term in re.findall(r"[a-z0-9+/#.-]+", query.lower()) if term]
    if not terms:
        return 0
    name = record["name"].lower()
    description = record["description"].lower()
    alternate_terms = " ".join(item.get("term", "") for item in record["alternate_terms"]).lower()
    functional_areas = " ".join(record["functional_areas"]).lower()
    blob = flatten_text(record).lower()
    if not all(term in blob for term in terms):
        return 0
    score = 0
    for term in terms:
        if term in name:
            score += 8
        if term in alternate_terms:
            score += 6
        if term in description:
            score += 4
        if term in functional_areas:
            score += 2
        if term in blob:
            score += 1
    return score


def matches_filters(record: dict[str, Any], args: argparse.Namespace) -> bool:
    if args.id and record["id"] not in {normalize_id(item) for item in args.id}:
        return False
    if args.view and normalize_id(args.view) not in record.get("view_ids", []):
        return False
    if args.phase and not any(
        item.get("phase", "").lower() == args.phase.lower() for item in record["modes_of_introduction"]
    ):
        return False
    if args.functional_area and not any(
        item.lower() == args.functional_area.lower() for item in record["functional_areas"]
    ):
        return False
    if args.impact and not any(
        args.impact.lower() in impact.lower()
        for consequence in record["consequences"]
        for impact in consequence["impacts"]
    ):
        return False
    if args.mapping and record["mapping"].get("usage", "").lower() != args.mapping.lower():
        return False
    if args.abstraction and record["abstraction"].lower() != args.abstraction.lower():
        return False
    if args.status and record["status"].lower() != args.status.lower():
        return False
    return True


def sort_matches(records: Iterable[dict[str, Any]], query: str | None) -> list[dict[str, Any]]:
    if not query:
        return sorted(records, key=lambda item: int(item["id"]))
    if re.fullmatch(r"(?:CWE-)?\d+", query.strip(), re.IGNORECASE):
        exact_id = normalize_id(query)
        return [record for record in records if record["id"] == exact_id]
    scored = [(score_query(record, query), record) for record in records]
    return [
        record
        for score, record in sorted(scored, key=lambda item: (-item[0], int(item[1]["id"])))
        if score > 0
    ]


def render_relationships(record: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for item in record["relationships"]:
        target = f"CWE-{item.get('cwe_id', '')}"
        if item.get("target_name"):
            target += f" {item['target_name']}"
        details = [item.get("nature", "")]
        if item.get("view_id"):
            details.append(f"view CWE-{item['view_id']}")
        if item.get("ordinal"):
            details.append(item["ordinal"])
        lines.append(f"- {target}: {', '.join(part for part in details if part)}")
    return lines


def render_record(record: dict[str, Any], metadata: dict[str, Any], full: bool) -> str:
    mapping = record["mapping"]
    view_names = metadata.get("views", {})
    lines = [
        f"# CWE-{record['id']}: {record['name']}",
        "",
        f"- Abstraction: {record['abstraction']}",
        f"- Structure: {record['structure']}",
        f"- Status: {record['status']}",
        f"- Mapping usage: {mapping.get('usage', '')}",
        f"- Likelihood of exploit: {record['likelihood_of_exploit'] or 'Not specified'}",
        "",
        "## Description",
        "",
        record["description"],
    ]
    if record["extended_description"]:
        lines.extend(["", "## Extended Description", "", record["extended_description"]])
    lines.extend(
        [
            "",
            "## Mapping Guidance",
            "",
            f"- Usage: {mapping.get('usage', '')}",
            f"- Reasons: {', '.join(mapping.get('reasons', [])) or 'None listed'}",
            f"- Rationale: {mapping.get('rationale', '')}",
            f"- Comments: {mapping.get('comments', '')}",
        ]
    )
    if mapping.get("suggestions"):
        lines.extend(["", "Suggestions:"])
        for suggestion in mapping["suggestions"]:
            lines.append(f"- CWE-{suggestion['cwe_id']}: {suggestion['comment']}")
    if record["relationships"]:
        lines.extend(["", "## Relationships", "", *render_relationships(record)])
    phases = [item["phase"] for item in record["modes_of_introduction"] if item["phase"]]
    if phases:
        lines.extend(["", "## Introduction Phases", "", "- " + "\n- ".join(phases)])
    if record["functional_areas"]:
        lines.extend(["", "## Functional Areas", "", "- " + "\n- ".join(record["functional_areas"])])
    if record["platforms"]:
        lines.extend(["", "## Applicable Platforms", ""])
        for platform in record["platforms"]:
            details = ", ".join(
                f"{key}={value}" for key, value in platform.items() if key != "kind" and value
            )
            lines.append(f"- {platform['kind']}: {details}")
    if record["consequences"]:
        lines.extend(["", "## Common Consequences", ""])
        for item in record["consequences"]:
            scope = ", ".join(item["scopes"])
            impact = ", ".join(item["impacts"])
            note = f" {item['note']}" if item["note"] else ""
            lines.append(f"- Scope: {scope}; Impact: {impact}.{note}")
    if record["detection_methods"]:
        lines.extend(["", "## Detection Methods", ""])
        for item in record["detection_methods"]:
            effectiveness = f" ({item['effectiveness']})" if item["effectiveness"] else ""
            lines.append(f"- {item['method']}{effectiveness}: {item['description']}")
    if record["mitigations"]:
        lines.extend(["", "## Potential Mitigations", ""])
        for item in record["mitigations"]:
            prefix = "; ".join(
                part
                for part in [
                    ", ".join(item["phases"]),
                    item["strategy"],
                    item["effectiveness"],
                ]
                if part
            )
            lines.append(f"- {prefix}: {item['description']}" if prefix else f"- {item['description']}")
    if record["view_ids"]:
        lines.extend(["", "## View Membership", ""])
        for view_id in record["view_ids"]:
            view = view_names.get(view_id, {})
            lines.append(f"- CWE-{view_id}: {view.get('name', '')}")
    if full:
        if record["background_details"]:
            lines.extend(["", "## Background Details", ""])
            lines.extend(f"- {item}" for item in record["background_details"])
        if record["exploitation_factors"]:
            lines.extend(["", "## Exploitation Factors", ""])
            lines.extend(f"- {item}" for item in record["exploitation_factors"])
        if record["observed_examples"]:
            lines.extend(["", "## Observed Examples", ""])
            for item in record["observed_examples"]:
                lines.append(f"- {item['reference']}: {item['description']}")
        if record["notes"]:
            lines.extend(["", "## Notes", ""])
            lines.extend(f"- {item['type']}: {item['text']}" for item in record["notes"])
        if record["references"]:
            lines.extend(["", "## External References", ""])
            for item in record["references"]:
                suffix = f" ({item['url']})" if item.get("url") else ""
                lines.append(f"- {item['reference_id']}: {item['title']}{suffix}")
    return "\n".join(lines) + "\n"


def render_list(records: list[dict[str, Any]], metadata: dict[str, Any], args: argparse.Namespace) -> str:
    catalog = metadata.get("catalog", {})
    lines = [
        f"# CWE Matches ({len(records)})",
        "",
        f"Catalog: {catalog.get('name', '')} {catalog.get('version', '')} dated {catalog.get('date', '')}",
        "",
        "| CWE | Name | Abstraction | Status | Mapping | Description |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for record in records[: args.limit]:
        lines.append(
            f"| CWE-{record['id']} | {md_escape(record['name'])} | {record['abstraction']} | "
            f"{record['status']} | {record['mapping'].get('usage', '')} | "
            f"{md_escape(short_text(record['description']))} |"
        )
    if len(records) > args.limit:
        lines.extend(["", f"Showing {args.limit} of {len(records)} matches."])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA_PATH, help="Path to cwe-records.jsonl.")
    parser.add_argument(
        "--metadata",
        type=Path,
        default=DEFAULT_METADATA_PATH,
        help="Path to cwe-catalog-metadata.json.",
    )
    parser.add_argument("--id", action="append", help="CWE ID, with or without the CWE- prefix.")
    parser.add_argument("--query", help="Keyword search across weakness content.")
    parser.add_argument("--view", help="Filter by view ID.")
    parser.add_argument("--phase", help="Filter by introduction phase.")
    parser.add_argument("--functional-area", help="Filter by functional area.")
    parser.add_argument("--impact", help="Filter by technical impact substring.")
    parser.add_argument("--mapping", help="Filter by mapping usage.")
    parser.add_argument("--abstraction", help="Filter by abstraction.")
    parser.add_argument("--status", help="Filter by status.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum list results to render.")
    parser.add_argument("--full", action="store_true", help="Include background details, notes, and references.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    args = parser.parse_args()

    records = load_records(args.data)
    metadata = load_metadata(args.metadata)
    matches = [record for record in records if matches_filters(record, args)]
    matches = sort_matches(matches, args.query)

    if args.json:
        print(json.dumps(matches[: args.limit] if len(matches) != 1 else matches[0], indent=2, sort_keys=True))
        return
    if not matches:
        print("No matching CWE records found.")
        return
    if len(matches) == 1:
        print(render_record(matches[0], metadata, args.full), end="")
        return
    print(render_list(matches, metadata, args), end="")


if __name__ == "__main__":
    main()
