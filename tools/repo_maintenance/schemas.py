from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


class DuplicateKeyError(ValueError):
    """A JSON or YAML mapping contains a duplicate key."""


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_json_text(text: str) -> Any:
    return json.loads(text, object_pairs_hook=_unique_json_object)


class StrictSafeLoader(yaml.SafeLoader):
    """Safe YAML loader that also rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: StrictSafeLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in result
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable mapping key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


StrictSafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def load_yaml_text(text: str) -> Any:
    documents = list(yaml.load_all(text, Loader=StrictSafeLoader))
    if len(documents) != 1:
        raise ValueError(f"expected one YAML document, found {len(documents)}")
    return documents[0]


def load_schema(root: Path, name: str) -> dict[str, Any]:
    path = root / "tools" / "maintenance" / "schemas" / f"{name}.schema.json"
    value = load_json_text(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"schema {path} must contain a JSON object")
    return value


def schema_errors(instance: Any, schema: dict[str, Any]) -> list[tuple[str, str]]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    result = []
    for error in errors:
        field = ".".join(str(part) for part in error.absolute_path) or "$"
        result.append((field, error.message))
    return result
