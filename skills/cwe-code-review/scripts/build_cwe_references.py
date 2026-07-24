#!/usr/bin/env python3
"""Build searchable CWE review references from a CWE catalog XML and schema XSD."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

CWE_NS = "http://cwe.mitre.org/cwe-7"
XSD_NS = "http://www.w3.org/2001/XMLSchema"
NS = {"cwe": CWE_NS, "xs": XSD_NS}

REVIEW_VIEW_NOTES = {
    "699": "Primary software-development browsing view. Use it to scope common review surfaces by development concept.",
    "1000": "Research graph. Use it to move between broad parents and precise child weaknesses while tracing root cause.",
    "1003": "Simplified vulnerability-mapping graph. Use it when a finding needs a practical mapping candidate before refining it.",
    "1435": "2025 CWE Top 25 view from this catalog release. Use it as prioritization context, never as proof of severity.",
    "1344": "OWASP Top Ten 2021 view. Use it when a review or report must align findings with the OWASP 2021 grouping.",
    "1450": "OWASP Top Ten 2025 RC1 view. Use it only when the RC1 taxonomy is specifically relevant.",
    "1448": "AI/ML product view. Use it when model inputs, training, inference, or agentic behavior are in scope.",
    "658": "Implicit C-language view.",
    "659": "Implicit C++-language view.",
    "660": "Implicit Java-language view.",
    "661": "Implicit PHP-language view.",
    "701": "Implicit design-introduction view.",
    "702": "Implicit implementation-introduction view.",
    "919": "Implicit mobile-application view.",
}

CORE_COMPLEX_TYPES = [
    "WeaknessType",
    "MappingNotesType",
    "RelatedWeaknessesType",
    "RelationshipsType",
    "ModesOfIntroductionType",
    "ApplicablePlatformsType",
    "FunctionalAreasType",
    "CommonConsequencesType",
    "DetectionMethodsType",
    "PotentialMitigationsType",
    "ObservedExampleType",
]


def normalize_space(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def text_of(node: ET.Element | None) -> str:
    if node is None:
        return ""
    return normalize_space(" ".join(node.itertext()))


def doc_of(node: ET.Element | None) -> str:
    if node is None:
        return ""
    docs = [text_of(item) for item in node.findall("xs:annotation/xs:documentation", NS)]
    return normalize_space(" ".join(item for item in docs if item))


def short_text(value: str, limit: int = 180) -> str:
    value = normalize_space(value)
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def snake_key(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    return value.replace("-", "_").lower()


def normalized_attrs(node: ET.Element) -> dict[str, str]:
    return {snake_key(key): value for key, value in node.attrib.items()}


def first_text(node: ET.Element, path: str) -> str:
    return text_of(node.find(path, NS))


def all_text(node: ET.Element, path: str) -> list[str]:
    return [text_of(item) for item in node.findall(path, NS) if text_of(item)]


def parse_external_references(root: ET.Element) -> dict[str, dict[str, Any]]:
    references: dict[str, dict[str, Any]] = {}
    for ref in root.findall("cwe:External_References/cwe:External_Reference", NS):
        ref_id = ref.attrib["Reference_ID"]
        references[ref_id] = {
            "reference_id": ref_id,
            "authors": all_text(ref, "cwe:Author"),
            "title": first_text(ref, "cwe:Title"),
            "edition": first_text(ref, "cwe:Edition"),
            "publication": first_text(ref, "cwe:Publication"),
            "publication_year": first_text(ref, "cwe:Publication_Year"),
            "publisher": first_text(ref, "cwe:Publisher"),
            "url": first_text(ref, "cwe:URL"),
            "url_date": first_text(ref, "cwe:URL_Date"),
        }
    return references


def parse_mapping_notes(node: ET.Element) -> dict[str, Any]:
    mapping = node.find("cwe:Mapping_Notes", NS)
    if mapping is None:
        return {}
    return {
        "usage": first_text(mapping, "cwe:Usage"),
        "rationale": first_text(mapping, "cwe:Rationale"),
        "comments": first_text(mapping, "cwe:Comments"),
        "reasons": [
            item.attrib.get("Type", "")
            for item in mapping.findall("cwe:Reasons/cwe:Reason", NS)
            if item.attrib.get("Type")
        ],
        "suggestions": [
            {
                "cwe_id": item.attrib.get("CWE_ID", ""),
                "comment": item.attrib.get("Comment", ""),
            }
            for item in mapping.findall("cwe:Suggestions/cwe:Suggestion", NS)
        ],
    }


def parse_platforms(node: ET.Element) -> list[dict[str, str]]:
    platforms: list[dict[str, str]] = []
    parent = node.find("cwe:Applicable_Platforms", NS)
    if parent is None:
        return platforms
    for child in list(parent):
        item = {"kind": child.tag.rsplit("}", 1)[-1]}
        item.update(normalized_attrs(child))
        platforms.append(item)
    return platforms


def parse_relationships(node: ET.Element) -> list[dict[str, str]]:
    return [
        normalized_attrs(item)
        for item in node.findall("cwe:Related_Weaknesses/cwe:Related_Weakness", NS)
    ]


def parse_consequences(node: ET.Element) -> list[dict[str, Any]]:
    consequences: list[dict[str, Any]] = []
    for item in node.findall("cwe:Common_Consequences/cwe:Consequence", NS):
        consequences.append(
            {
                "consequence_id": item.attrib.get("Consequence_ID", ""),
                "scopes": all_text(item, "cwe:Scope"),
                "impacts": all_text(item, "cwe:Impact"),
                "likelihood": first_text(item, "cwe:Likelihood"),
                "note": first_text(item, "cwe:Note"),
            }
        )
    return consequences


def parse_detection_methods(node: ET.Element) -> list[dict[str, str]]:
    methods: list[dict[str, str]] = []
    for item in node.findall("cwe:Detection_Methods/cwe:Detection_Method", NS):
        methods.append(
            {
                "detection_method_id": item.attrib.get("Detection_Method_ID", ""),
                "method": first_text(item, "cwe:Method"),
                "description": first_text(item, "cwe:Description"),
                "effectiveness": first_text(item, "cwe:Effectiveness"),
                "effectiveness_notes": first_text(item, "cwe:Effectiveness_Notes"),
            }
        )
    return methods


def parse_mitigations(node: ET.Element) -> list[dict[str, Any]]:
    mitigations: list[dict[str, Any]] = []
    for item in node.findall("cwe:Potential_Mitigations/cwe:Mitigation", NS):
        mitigations.append(
            {
                "mitigation_id": item.attrib.get("Mitigation_ID", ""),
                "phases": all_text(item, "cwe:Phase"),
                "strategy": first_text(item, "cwe:Strategy"),
                "description": first_text(item, "cwe:Description"),
                "effectiveness": first_text(item, "cwe:Effectiveness"),
                "effectiveness_notes": first_text(item, "cwe:Effectiveness_Notes"),
            }
        )
    return mitigations


def parse_taxonomy_mappings(node: ET.Element) -> list[dict[str, str]]:
    mappings: list[dict[str, str]] = []
    for item in node.findall("cwe:Taxonomy_Mappings/cwe:Taxonomy_Mapping", NS):
        mappings.append(
            {
                "taxonomy_name": item.attrib.get("Taxonomy_Name", ""),
                "entry_id": first_text(item, "cwe:Entry_ID"),
                "entry_name": first_text(item, "cwe:Entry_Name"),
                "mapping_fit": first_text(item, "cwe:Mapping_Fit"),
            }
        )
    return mappings


def parse_weakness(
    node: ET.Element,
    external_references: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "id": node.attrib["ID"],
        "name": node.attrib["Name"],
        "abstraction": node.attrib.get("Abstraction", ""),
        "structure": node.attrib.get("Structure", ""),
        "status": node.attrib.get("Status", ""),
        "diagram": node.attrib.get("Diagram", ""),
        "description": first_text(node, "cwe:Description"),
        "extended_description": first_text(node, "cwe:Extended_Description"),
        "relationships": parse_relationships(node),
        "weakness_ordinalities": [
            {
                "ordinality": first_text(item, "cwe:Ordinality"),
                "description": first_text(item, "cwe:Description"),
            }
            for item in node.findall("cwe:Weakness_Ordinalities/cwe:Weakness_Ordinality", NS)
        ],
        "platforms": parse_platforms(node),
        "background_details": all_text(node, "cwe:Background_Details/cwe:Background_Detail"),
        "alternate_terms": [
            {
                "term": first_text(item, "cwe:Term"),
                "description": first_text(item, "cwe:Description"),
            }
            for item in node.findall("cwe:Alternate_Terms/cwe:Alternate_Term", NS)
        ],
        "modes_of_introduction": [
            {
                "phase": first_text(item, "cwe:Phase"),
                "note": first_text(item, "cwe:Note"),
            }
            for item in node.findall("cwe:Modes_Of_Introduction/cwe:Introduction", NS)
        ],
        "exploitation_factors": all_text(node, "cwe:Exploitation_Factors/cwe:Exploitation_Factor"),
        "likelihood_of_exploit": first_text(node, "cwe:Likelihood_Of_Exploit"),
        "consequences": parse_consequences(node),
        "detection_methods": parse_detection_methods(node),
        "mitigations": parse_mitigations(node),
        "functional_areas": all_text(node, "cwe:Functional_Areas/cwe:Functional_Area"),
        "affected_resources": all_text(node, "cwe:Affected_Resources/cwe:Affected_Resource"),
        "taxonomy_mappings": parse_taxonomy_mappings(node),
        "related_attack_patterns": [
            item.attrib.get("CAPEC_ID", "")
            for item in node.findall("cwe:Related_Attack_Patterns/cwe:Related_Attack_Pattern", NS)
            if item.attrib.get("CAPEC_ID")
        ],
        "observed_examples": [
            {
                "reference": first_text(item, "cwe:Reference"),
                "description": first_text(item, "cwe:Description"),
                "link": first_text(item, "cwe:Link"),
            }
            for item in node.findall("cwe:Observed_Examples/cwe:Observed_Example", NS)
        ],
        "mapping": parse_mapping_notes(node),
        "notes": [
            {
                "type": item.attrib.get("Type", ""),
                "text": text_of(item),
            }
            for item in node.findall("cwe:Notes/cwe:Note", NS)
        ],
    }
    ref_ids = list(
        dict.fromkeys(
            item.attrib.get("External_Reference_ID", "")
            for item in node.findall("cwe:References/cwe:Reference", NS)
            if item.attrib.get("External_Reference_ID")
        )
    )
    record["references"] = [
        external_references[ref_id] for ref_id in ref_ids if ref_id in external_references
    ]
    return record


def parse_categories(root: ET.Element) -> dict[str, dict[str, Any]]:
    categories: dict[str, dict[str, Any]] = {}
    for node in root.findall("cwe:Categories/cwe:Category", NS):
        categories[node.attrib["ID"]] = {
            "id": node.attrib["ID"],
            "name": node.attrib["Name"],
            "status": node.attrib.get("Status", ""),
            "summary": first_text(node, "cwe:Summary"),
            "relationships": [
                {
                    "kind": item.tag.rsplit("}", 1)[-1],
                    **normalized_attrs(item),
                }
                for item in node.findall("cwe:Relationships/*", NS)
            ],
            "mapping": parse_mapping_notes(node),
        }
    return categories


def parse_views(root: ET.Element) -> dict[str, dict[str, Any]]:
    views: dict[str, dict[str, Any]] = {}
    for node in root.findall("cwe:Views/cwe:View", NS):
        views[node.attrib["ID"]] = {
            "id": node.attrib["ID"],
            "name": node.attrib["Name"],
            "type": node.attrib.get("Type", ""),
            "status": node.attrib.get("Status", ""),
            "objective": first_text(node, "cwe:Objective"),
            "filter": first_text(node, "cwe:Filter"),
            "members": [
                {
                    "kind": item.tag.rsplit("}", 1)[-1],
                    **normalized_attrs(item),
                }
                for item in node.findall("cwe:Members/*", NS)
            ],
            "mapping": parse_mapping_notes(node),
        }
    return views


def implicit_view_members(view_id: str, records: dict[str, dict[str, Any]]) -> set[str]:
    members: set[str] = set()
    for record in records.values():
        if view_id == "1040" and any(
            item["ordinality"] == "Indirect" for item in record["weakness_ordinalities"]
        ):
            members.add(record["id"])
        elif view_id == "1081" and any(item["type"] == "Maintenance" for item in record["notes"]):
            members.add(record["id"])
        elif view_id == "1424" and any(
            item["taxonomy_name"] == "ISA/IEC 62443" for item in record["taxonomy_mappings"]
        ):
            members.add(record["id"])
        elif view_id == "2000":
            members.add(record["id"])
        elif view_id == "604" and record["status"] == "Deprecated":
            members.add(record["id"])
        elif view_id in {"658", "659", "660", "661"}:
            language = {"658": "C", "659": "C++", "660": "Java", "661": "PHP"}[view_id]
            if any(item.get("kind") == "Language" and item.get("name") == language for item in record["platforms"]):
                members.add(record["id"])
        elif view_id == "677" and record["abstraction"] == "Base" and record["status"] != "Deprecated":
            members.add(record["id"])
        elif view_id == "678" and record["structure"] == "Composite" and record["status"] != "Deprecated":
            members.add(record["id"])
        elif view_id in {"679", "999"}:
            continue
        elif view_id == "701" and record["abstraction"] in {"Base", "Class"} and any(
            item["phase"] == "Architecture and Design" for item in record["modes_of_introduction"]
        ):
            members.add(record["id"])
        elif view_id == "702" and any(
            item["phase"] == "Implementation" for item in record["modes_of_introduction"]
        ):
            members.add(record["id"])
        elif view_id == "709" and record["structure"] == "Chain":
            members.add(record["id"])
        elif view_id == "919" and any(
            item.get("kind") == "Technology" and item.get("class") == "Mobile"
            for item in record["platforms"]
        ):
            members.add(record["id"])
    return members


def attach_relationship_names(records: dict[str, dict[str, Any]]) -> None:
    for record in records.values():
        for relationship in record["relationships"]:
            target = records.get(relationship.get("cwe_id", ""))
            if target:
                relationship["target_name"] = target["name"]


def attach_view_memberships(
    records: dict[str, dict[str, Any]],
    categories: dict[str, dict[str, Any]],
    views: dict[str, dict[str, Any]],
) -> None:
    view_members: dict[str, set[str]] = defaultdict(set)
    for view_id, view in views.items():
        if view["type"] == "Implicit":
            view_members[view_id].update(implicit_view_members(view_id, records))
        for member in view["members"]:
            cwe_id = member.get("cwe_id", "")
            if cwe_id in records:
                view_members[view_id].add(cwe_id)
    for category in categories.values():
        for relationship in category["relationships"]:
            view_id = relationship.get("view_id", "")
            cwe_id = relationship.get("cwe_id", "")
            if relationship.get("kind") == "Has_Member" and cwe_id in records:
                view_members[view_id].add(cwe_id)
    for record in records.values():
        for relationship in record["relationships"]:
            view_id = relationship.get("view_id", "")
            view_members[view_id].add(record["id"])
            cwe_id = relationship.get("cwe_id", "")
            if cwe_id in records:
                view_members[view_id].add(cwe_id)
    for view_id, view in views.items():
        view["weakness_member_ids"] = sorted(view_members[view_id], key=int)
    for record in records.values():
        record["view_ids"] = sorted(
            [view_id for view_id, members in view_members.items() if record["id"] in members],
            key=int,
        )


def parse_schema(schema_root: ET.Element) -> dict[str, Any]:
    appinfo = schema_root.find("xs:annotation/xs:appinfo", NS)
    metadata = {
        "version": schema_root.attrib.get("version", ""),
        "schema": first_text(appinfo, "schema") if appinfo is not None else "",
        "date": first_text(appinfo, "date") if appinfo is not None else "",
        "documentation": doc_of(schema_root),
    }
    simple_types: dict[str, dict[str, Any]] = {}
    for node in schema_root.findall("xs:simpleType", NS):
        values = []
        for enum in node.findall(".//xs:enumeration", NS):
            values.append(
                {
                    "value": enum.attrib.get("value", ""),
                    "documentation": doc_of(enum),
                }
            )
        if values:
            simple_types[node.attrib.get("name", "")] = {
                "documentation": doc_of(node),
                "values": values,
            }
    complex_types: dict[str, dict[str, Any]] = {}
    for name in CORE_COMPLEX_TYPES:
        node = schema_root.find(f"xs:complexType[@name='{name}']", NS)
        if node is None:
            continue
        elements = []
        for child in node.findall("xs:sequence/xs:element", NS):
            elements.append(
                {
                    "name": child.attrib.get("name", ""),
                    "type": child.attrib.get("type", ""),
                    "min_occurs": child.attrib.get("minOccurs", "1"),
                    "max_occurs": child.attrib.get("maxOccurs", "1"),
                }
            )
        attributes = []
        for attribute in node.findall("xs:attribute", NS):
            attributes.append(
                {
                    "name": attribute.attrib.get("name", ""),
                    "type": attribute.attrib.get("type", ""),
                    "use": attribute.attrib.get("use", "optional"),
                }
            )
        complex_types[name] = {
            "documentation": doc_of(node),
            "elements": elements,
            "attributes": attributes,
        }
    return {
        "metadata": metadata,
        "simple_types": simple_types,
        "complex_types": complex_types,
    }


def entity_label(
    cwe_id: str,
    records: dict[str, dict[str, Any]],
    categories: dict[str, dict[str, Any]],
    views: dict[str, dict[str, Any]],
) -> str:
    if cwe_id in records:
        return f"CWE-{cwe_id} {records[cwe_id]['name']} [Weakness]"
    if cwe_id in categories:
        return f"CWE-{cwe_id} {categories[cwe_id]['name']} [Category]"
    if cwe_id in views:
        return f"CWE-{cwe_id} {views[cwe_id]['name']} [View]"
    return f"CWE-{cwe_id}"


def write_jsonl(path: Path, records: dict[str, dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in sorted(records.values(), key=lambda item: int(item["id"])):
            handle.write(json.dumps(record, sort_keys=True, ensure_ascii=True) + "\n")


def write_metadata_json(
    path: Path,
    root: ET.Element,
    schema: dict[str, Any],
    categories: dict[str, dict[str, Any]],
    views: dict[str, dict[str, Any]],
) -> None:
    payload = {
        "catalog": {
            "name": root.attrib.get("Name", ""),
            "version": root.attrib.get("Version", ""),
            "date": root.attrib.get("Date", ""),
            "namespace": CWE_NS,
            "schema_location": root.attrib.get(
                "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", ""
            ),
        },
        "schema": schema["metadata"],
        "categories": categories,
        "views": views,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def write_catalog_summary(
    path: Path,
    root: ET.Element,
    schema: dict[str, Any],
    records: dict[str, dict[str, Any]],
    categories: dict[str, dict[str, Any]],
    views: dict[str, dict[str, Any]],
) -> None:
    abstraction_counts = Counter(record["abstraction"] for record in records.values())
    status_counts = Counter(record["status"] for record in records.values())
    usage_counts = Counter(record["mapping"].get("usage", "") for record in records.values())
    structure_counts = Counter(record["structure"] for record in records.values())
    mapping_usage_summary = ", ".join(
        f"{key or 'Unknown'}: {value}" for key, value in sorted(usage_counts.items())
    )
    lines = [
        "# CWE Catalog Summary",
        "",
        "Generated by `scripts/build_cwe_references.py` from the local CWE catalog and XSD supplied to the skill.",
        "",
        "## Source",
        "",
        f"- Catalog: {root.attrib.get('Name', '')} {root.attrib.get('Version', '')} dated {root.attrib.get('Date', '')}",
        f"- Catalog namespace: `{CWE_NS}`",
        f"- Schema: {schema['metadata'].get('schema', '')} {schema['metadata'].get('version', '')} dated {schema['metadata'].get('date', '')}",
        f"- Counts: {len(records)} weaknesses, {len(categories)} categories, {len(views)} views",
        "",
        "## How To Use This Corpus",
        "",
        "- Start with code evidence and a trust-boundary failure, then use the corpus to refine the root-cause weakness.",
        "- Prefer weaknesses with mapping usage `Allowed` or `Allowed-with-Review`; treat `Discouraged` and `Prohibited` entries as navigation aids unless the mapping notes justify an exception.",
        "- Prefer the most precise supported weakness over a broad Pillar, Class, Category, or View. Categories and Views organize the corpus and are not root-cause mappings.",
        "- Use view membership as coverage or prioritization context, not as a severity rating.",
        "- Use `scripts/cwe_lookup.py` for detail retrieval. Use `references/cwe-weakness-index.md` for fast grep-based browsing.",
        "",
        "## Catalog Shape",
        "",
        "| Dimension | Values |",
        "| --- | --- |",
        f"| Abstraction | {', '.join(f'{key}: {value}' for key, value in sorted(abstraction_counts.items()))} |",
        f"| Structure | {', '.join(f'{key}: {value}' for key, value in sorted(structure_counts.items()))} |",
        f"| Status | {', '.join(f'{key}: {value}' for key, value in sorted(status_counts.items()))} |",
        f"| Mapping usage | {mapping_usage_summary} |",
        "",
        "## Review-Oriented Views",
        "",
        "| View | Type | Status | Weakness Members | Use |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for view_id in REVIEW_VIEW_NOTES:
        view = views.get(view_id)
        if not view:
            continue
        lines.append(
            f"| CWE-{view_id} {md_escape(view['name'])} | {view['type']} | {view['status']} | "
            f"{len(view.get('weakness_member_ids', []))} | {md_escape(REVIEW_VIEW_NOTES[view_id])} |"
        )
    lines.extend(
        [
            "",
            "## Generated Files",
            "",
            "- `cwe-weakness-index.md`: compact, line-oriented index of every weakness for grep and quick scanning.",
            "- `cwe-review-views.md`: review-oriented view descriptions, filters, and member lists.",
            "- `cwe-schema-guide.md`: XSD-derived field semantics and enumeration vocabulary.",
            "- `cwe-records.jsonl`: machine-readable record per weakness with mapping notes, relationships, detection methods, mitigations, and examples.",
            "- `cwe-catalog-metadata.json`: machine-readable catalog, schema, category, and view metadata.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_weakness_index(path: Path, records: dict[str, dict[str, Any]]) -> None:
    lines = [
        "# CWE Weakness Index",
        "",
        "Generated from the local CWE catalog. Search this file first, then use `scripts/cwe_lookup.py --id <id>` for complete detail.",
        "",
        "| CWE | Name | Abstraction | Status | Mapping | Phases | Functional Areas | Parent IDs | View IDs |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for record in sorted(records.values(), key=lambda item: int(item["id"])):
        parents = [
            f"CWE-{item['cwe_id']}"
            for item in record["relationships"]
            if item.get("nature") == "ChildOf" and item.get("cwe_id")
        ]
        phases = sorted({item["phase"] for item in record["modes_of_introduction"] if item["phase"]})
        lines.append(
            "| "
            + " | ".join(
                [
                    f"CWE-{record['id']}",
                    md_escape(record["name"]),
                    record["abstraction"],
                    record["status"],
                    record["mapping"].get("usage", ""),
                    md_escape(", ".join(phases)),
                    md_escape(", ".join(record["functional_areas"])),
                    md_escape(", ".join(parents)),
                    md_escape(", ".join(f"CWE-{item}" for item in record["view_ids"])),
                ]
            )
            + " |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_review_views(
    path: Path,
    records: dict[str, dict[str, Any]],
    categories: dict[str, dict[str, Any]],
    views: dict[str, dict[str, Any]],
) -> None:
    lines = [
        "# CWE Review Views",
        "",
        "Use these views to scope coverage and navigate the catalog. A view is not itself a finding or a root-cause mapping.",
        "",
        "## Contents",
        "",
    ]
    for view_id in REVIEW_VIEW_NOTES:
        if view_id in views:
            lines.append(f"- [CWE-{view_id} {views[view_id]['name']}](#cwe-{view_id})")
    for view_id, note in REVIEW_VIEW_NOTES.items():
        view = views.get(view_id)
        if not view:
            continue
        lines.extend(
            [
                "",
                f"## CWE-{view_id}",
                "",
                f"**{view['name']}**",
                "",
                f"- Type: {view['type']}",
                f"- Status: {view['status']}",
                f"- Weakness members: {len(view.get('weakness_member_ids', []))}",
                f"- Review use: {note}",
                "",
                short_text(view["objective"], 600),
            ]
        )
        if view["filter"]:
            lines.extend(["", f"Filter: `{view['filter']}`"])
        if view["members"]:
            label = "Ordered direct members:" if view_id == "1435" else "Direct members:"
            lines.extend(["", label, ""])
            for index, member in enumerate(view["members"], start=1):
                prefix = f"{index}." if view_id == "1435" else "-"
                lines.append(
                    f"{prefix} {entity_label(member.get('cwe_id', ''), records, categories, views)}"
                )
        weakness_member_ids = view.get("weakness_member_ids", [])
        show_all = view_id in {"1003", "1448"}
        if show_all:
            lines.extend(["", "Weakness members:", ""])
            for cwe_id in weakness_member_ids:
                record = records[cwe_id]
                lines.append(
                    f"- CWE-{cwe_id} {record['name']} "
                    f"({record['abstraction']}; mapping {record['mapping'].get('usage', '')})"
                )
        elif weakness_member_ids:
            sample = weakness_member_ids[:20]
            lines.extend(
                [
                    "",
                    f"Sample weakness members ({len(sample)} of {len(weakness_member_ids)}):",
                    "",
                ]
            )
            for cwe_id in sample:
                record = records[cwe_id]
                lines.append(f"- CWE-{cwe_id} {record['name']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_schema_guide(path: Path, schema: dict[str, Any]) -> None:
    lines = [
        "# CWE Schema Guide",
        "",
        "Generated from the local CWE XSD. Use this file when interpreting field meaning, relationship semantics, or allowed vocabulary.",
        "",
        "## Contents",
        "",
        "- [Schema Metadata](#schema-metadata)",
        "- [Core Complex Types](#core-complex-types)",
        "- [Enumerations](#enumerations)",
        "",
        "## Schema Metadata",
        "",
        f"- Name: {schema['metadata'].get('schema', '')}",
        f"- Version: {schema['metadata'].get('version', '')}",
        f"- Date: {schema['metadata'].get('date', '')}",
        "",
        "## Core Complex Types",
        "",
    ]
    for name in CORE_COMPLEX_TYPES:
        item = schema["complex_types"].get(name)
        if not item:
            continue
        lines.extend([f"### {name}", "", short_text(item["documentation"], 900), ""])
        if item["elements"]:
            lines.extend(
                [
                    "| Element | Type | Cardinality |",
                    "| --- | --- | --- |",
                ]
            )
            for element in item["elements"]:
                lines.append(
                    f"| {element['name']} | {element['type'] or 'inline type'} | "
                    f"{element['min_occurs']}..{element['max_occurs']} |"
                )
            lines.append("")
        if item["attributes"]:
            lines.extend(
                [
                    "| Attribute | Type | Use |",
                    "| --- | --- | --- |",
                ]
            )
            for attribute in item["attributes"]:
                lines.append(
                    f"| {attribute['name']} | {attribute['type'] or 'inline type'} | {attribute['use']} |"
                )
            lines.append("")
    lines.extend(["## Enumerations", ""])
    for name, item in sorted(schema["simple_types"].items()):
        lines.extend([f"### {name}", "", short_text(item["documentation"], 500), ""])
        lines.extend(["| Value | Notes |", "| --- | --- |"])
        for value in item["values"]:
            lines.append(
                f"| {md_escape(value['value'])} | {md_escape(short_text(value['documentation'], 240))} |"
            )
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def build(catalog_path: Path, schema_path: Path, output_dir: Path) -> None:
    catalog_root = ET.parse(catalog_path).getroot()
    schema_root = ET.parse(schema_path).getroot()
    external_references = parse_external_references(catalog_root)
    records = {
        node.attrib["ID"]: parse_weakness(node, external_references)
        for node in catalog_root.findall("cwe:Weaknesses/cwe:Weakness", NS)
    }
    categories = parse_categories(catalog_root)
    views = parse_views(catalog_root)
    schema = parse_schema(schema_root)
    attach_relationship_names(records)
    attach_view_memberships(records, categories, views)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_dir / "cwe-records.jsonl", records)
    write_metadata_json(output_dir / "cwe-catalog-metadata.json", catalog_root, schema, categories, views)
    write_catalog_summary(output_dir / "cwe-catalog-summary.md", catalog_root, schema, records, categories, views)
    write_weakness_index(output_dir / "cwe-weakness-index.md", records)
    write_review_views(output_dir / "cwe-review-views.md", records, categories, views)
    write_schema_guide(output_dir / "cwe-schema-guide.md", schema)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", required=True, type=Path, help="Path to CWE catalog XML.")
    parser.add_argument("--schema", required=True, type=Path, help="Path to CWE schema XSD.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "references",
        help="Directory for generated references.",
    )
    args = parser.parse_args()
    build(args.catalog, args.schema, args.output_dir)
    print(f"Generated CWE references in {args.output_dir}")


if __name__ == "__main__":
    main()
