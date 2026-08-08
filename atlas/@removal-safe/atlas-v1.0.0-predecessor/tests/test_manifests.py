"""Validation tests for the standard's schemas, examples, and self-hosting claim.

tests/ mirrors the shape of what it verifies: manifests + specs.
"""
import datetime
import json
import pathlib
import sys

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "spec" / "schemas"

from atlas.core import manifest as validate  # noqa: E402

EXAMPLES = sorted((ROOT / "examples").glob("*.yaml"))


def test_schemas_are_valid_json_schema():
    from jsonschema import Draft202012Validator

    for schema_path in (ROOT / "spec" / "schemas").glob("*.schema.json"):
        schema = json.loads(schema_path.read_text())
        Draft202012Validator.check_schema(schema)


@pytest.mark.parametrize("path", EXAMPLES, ids=[p.name for p in EXAMPLES])
def test_examples_validate(path):
    assert validate.validate_file(path, SCHEMAS) == []


def test_self_hosting_manifest_validates():
    """The repository must pass its own standard."""
    assert validate.validate_file(ROOT / "project.yaml", SCHEMAS) == []


def test_template_manifest_validates_after_substitution(tmp_path):
    text = (ROOT / "template" / "project.yaml").read_text()
    text = text.replace("{{PROJECT_NAME}}", "sample-project")
    p = tmp_path / "project.yaml"
    p.write_text(text)
    assert validate.validate_file(p, SCHEMAS) == []


# --- Negative cases: the schema must reject what the Matrix forbids ----------

def _validate_dict(d, tmp_path, name="project.yaml"):
    p = tmp_path / name
    p.write_text(yaml.safe_dump(d))
    return validate.validate_file(p, SCHEMAS)


BASE = {
    "standard": "project/1.0",
    "name": "sample",
    "type": "tool.cli",
    "stage": "active",
    "maturity": "beta",
    "owner": "person:jdoe",
    "visibility": "internal",
}


def test_deprecated_without_successor_rejected(tmp_path):
    bad = dict(BASE, stage="deprecated")
    assert _validate_dict(bad, tmp_path)


def test_sla_without_hardened_rejected(tmp_path):
    bad = dict(BASE, support="sla", maturity="stable")
    assert _validate_dict(bad, tmp_path)


def test_managed_deploy_without_runbook_rejected(tmp_path):
    bad = dict(BASE, deployment="managed.k8s")
    assert _validate_dict(bad, tmp_path)


def test_uppercase_name_rejected(tmp_path):
    bad = dict(BASE, name="AcmeInvoiceAPI2")
    assert _validate_dict(bad, tmp_path)


def test_unknown_type_rejected_but_x_extension_allowed(tmp_path):
    assert _validate_dict(dict(BASE, type="firmware.rtos"), tmp_path)
    assert _validate_dict(dict(BASE, type="x-firmware.rtos"), tmp_path) == []


def test_expired_waiver_fails():
    manifest = {"waivers": [{"id": "ST-01", "reason": "x" * 12,
                             "until": "2020-01-01", "approver": "person:a"}]}
    errs = validate.check_waivers(manifest, today=datetime.date(2026, 8, 6))
    assert errs and "expired" in errs[0]


def test_active_waiver_passes():
    manifest = {"waivers": [{"id": "ST-01", "reason": "x" * 12,
                             "until": "2099-01-01", "approver": "person:a"}]}
    assert validate.check_waivers(manifest, today=datetime.date(2026, 8, 6)) == []


# --- PRESENTATION spec (metadata block) --------------------------------------

def test_public_without_website_rejected(tmp_path):
    bad = dict(BASE, visibility="public",
               metadata={"description": "A useful thing indeed", "topics": ["tool", "a", "b"]})
    assert _validate_dict(bad, tmp_path)


def test_too_few_topics_rejected(tmp_path):
    bad = dict(BASE, metadata={"description": "A useful thing indeed", "topics": ["tool"]})
    assert _validate_dict(bad, tmp_path)


def test_overlong_description_rejected(tmp_path):
    bad = dict(BASE, metadata={"description": "x" * 200, "topics": ["tool", "a", "b"]})
    assert _validate_dict(bad, tmp_path)


def test_metadata_valid_passes(tmp_path):
    good = dict(BASE, metadata={
        "description": "Validates fleet manifests in CI",
        "website": "./docs/",
        "topics": ["tool", "validation", "ci"],
    })
    assert _validate_dict(good, tmp_path) == []
