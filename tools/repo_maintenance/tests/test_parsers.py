from __future__ import annotations

import json

import pytest
import yaml

from tools.repo_maintenance.schemas import (
    DuplicateKeyError,
    load_json_text,
    load_yaml_text,
)


def test_duplicate_yaml_key_is_rejected() -> None:
    with pytest.raises(yaml.constructor.ConstructorError, match="duplicate key 'name'"):
        load_yaml_text("name: first\nname: second\n")


def test_unsafe_yaml_tag_is_rejected() -> None:
    with pytest.raises(yaml.constructor.ConstructorError):
        load_yaml_text("value: !!python/object/apply:os.system ['never-run']\n")


def test_duplicate_json_key_is_rejected() -> None:
    with pytest.raises(DuplicateKeyError, match="duplicate JSON key 'name'"):
        load_json_text('{"name": "first", "name": "second"}')


def test_invalid_json_is_path_independent() -> None:
    with pytest.raises(json.JSONDecodeError):
        load_json_text('{"broken": }')


def test_yaml_loader_does_not_change_pyyaml_safe_loader() -> None:
    assert yaml.safe_load("name: first\nname: second\n") == {"name": "second"}
