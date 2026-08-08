"""Manifests and examples validate against the schemas."""

from __future__ import annotations

import json

import pytest

from atlas.core.manifest import KIND_SCHEMAS, detect_kind, validate_manifest


def test_project_manifest_is_valid(repo):
    assert validate_manifest(repo.manifest_path, repo.schema_dir, "project") == []


def test_authority_manifest_is_valid(repo):
    assert validate_manifest(repo.authority_path, repo.schema_dir, "authority") == []


@pytest.mark.parametrize("kind,filename", sorted(KIND_SCHEMAS.items()))
def test_every_schema_parses(repo, kind, filename):
    schema = json.loads((repo.schema_dir / filename).read_text(encoding="utf-8"))
    assert schema["$schema"].startswith("https://json-schema.org/")
    assert schema.get("title")


def test_examples_validate(repo):
    for path in sorted((repo.root / "examples").glob("*.yaml")):
        assert validate_manifest(path, repo.schema_dir, detect_kind(path)) == [], path.name


def test_detect_kind():
    import pathlib

    assert detect_kind(pathlib.Path("authority.yaml")) == "authority"
    assert detect_kind(pathlib.Path("a.workstream.yaml")) == "workstream"
    assert detect_kind(pathlib.Path("project.yaml")) == "project"


def test_a_bad_manifest_reports_every_error(repo, tmp_path):
    bad = tmp_path / "project.yaml"
    bad.write_text("standard: nope\nname: Not A Slug\n", encoding="utf-8")
    violations = validate_manifest(bad, repo.schema_dir, "project")
    assert len(violations) >= 3  # bad standard, bad name, and the missing fields
