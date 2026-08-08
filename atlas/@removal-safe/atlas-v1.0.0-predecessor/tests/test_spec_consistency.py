"""Cross-document consistency: JSON Schemas must agree with the spec prose.

Documentation drifts from code because they change on different triggers
(PROJECT.md paragraph 1). These tests are the trigger-coupling: a normative
enum change in prose without a schema change (or vice versa) turns CI red.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
MATRIX = (ROOT / "spec" / "project-matrix.md").read_text()
SCHEMA = json.loads((ROOT / "spec" / "schemas" / "project.schema.json").read_text())


def _schema_types():
    for option in SCHEMA["properties"]["type"]["anyOf"]:
        if "enum" in option:
            return set(option["enum"])
    raise AssertionError("type enum not found in schema")


def test_d1_type_enum_matches_prose():
    m = re.search(r"# D1 enum\ntype:\n(.*?)\n#", MATRIX, re.S)
    assert m, "D1 enum block not found in project-matrix.md"
    prose_types = set()
    for line in m.group(1).splitlines():
        fam_match = re.match(r"\s*(\w+):\s*\[([^\]]+)\]", line)
        if fam_match:
            fam, kinds = fam_match.groups()
            prose_types |= {f"{fam}.{k.strip()}" for k in kinds.split(",")}
    assert prose_types == _schema_types()


def test_d2_stage_enum_matches_prose():
    m = re.search(r"stage: \[([^\]]+)\]", MATRIX)
    assert set(s.strip() for s in m.group(1).split(",")) == set(
        SCHEMA["properties"]["stage"]["enum"]
    )


def test_d3_maturity_enum_matches_prose():
    m = re.search(r"maturity: \[([^\]]+)\]", MATRIX)
    assert set(s.strip() for s in m.group(1).split(",")) == set(
        SCHEMA["properties"]["maturity"]["enum"]
    )


def test_d4_packaging_enum_matches_prose():
    m = re.search(r"packaging: \[([^\]]+)\]", MATRIX)
    prose = {s.strip() for s in m.group(1).split(",")}
    assert prose == set(SCHEMA["properties"]["packaging"]["items"]["enum"])


def test_d5_deployment_enum_matches_prose():
    m = re.search(r"deployment: \[([^\]]+)\]", MATRIX)
    assert set(s.strip() for s in m.group(1).split(",")) == set(
        SCHEMA["properties"]["deployment"]["enum"]
    )


def test_d7_visibility_enum_matches_prose():
    m = re.search(r"visibility: \[([^\]]+)\]", MATRIX)
    assert set(s.strip() for s in m.group(1).split(",")) == set(
        SCHEMA["properties"]["visibility"]["enum"]
    )


def test_d8_support_enum_matches_prose():
    m = re.search(r"support: \[([^\]]+)\]", MATRIX)
    assert set(s.strip() for s in m.group(1).split(",")) == set(
        SCHEMA["properties"]["support"]["enum"]
    )


def test_presentation_spec_exists_and_readme_obeys_p02():
    """P-02: this repository's README opens with a hero visual."""
    spec = ROOT / "spec" / "presentation.md"
    assert spec.exists()
    head = "\n".join((ROOT / "README.md").read_text().splitlines()[:5])
    assert "<img " in head and 'alt="' in head


def test_settings_yml_mirrors_manifest_description():
    """P-05: settings-as-code must not drift from project.yaml metadata."""
    import yaml
    manifest = yaml.safe_load((ROOT / "project.yaml").read_text())
    desc = manifest["metadata"]["description"]
    assert desc in (ROOT / ".github" / "settings.yml").read_text()


def test_banner_and_architecture_assets_exist():
    assert (ROOT / "assets" / "banner.svg").exists()
    assert (ROOT / "assets" / "architecture.svg").exists()


def test_prompt_library_spec_exists_and_is_cited():
    assert (ROOT / "spec" / "library.md").exists()
    readme = (ROOT / "README.md").read_text()
    assert "library/prompts/" in readme and "library.md" in readme


def test_workstream_spec_exists_and_is_wired():
    assert (ROOT / "spec" / "workstream.md").exists()
    assert (ROOT / "spec" / "schemas" / "workstream.schema.json").exists()
    readme = (ROOT / "README.md").read_text()
    assert "workstream.md" in readme and "work/" in readme
