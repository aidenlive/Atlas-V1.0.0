"""The starter template passes what it teaches."""

from __future__ import annotations

import pytest

from atlas.core import compliance, template as template_mod
from atlas.errors import UsageError
from atlas.paths import Repository


@pytest.fixture(scope="module")
def scaffolded(root, tmp_path_factory):
    destination = tmp_path_factory.mktemp("scaffold") / "brand-guidelines"
    template_mod.scaffold(
        root / "template",
        destination,
        name="brand-guidelines",
        owner="role:brand-lead",
        description="How the brand sounds and looks",
    )
    return Repository(root=destination)


def test_a_new_repository_passes_on_its_first_run(scaffolded):
    report = compliance.run(scaffolded)
    assert report.ok, "\n".join(str(v) for v in report.violations)


def test_no_placeholders_survive(scaffolded):
    for path in scaffolded.root.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        leftover = [m.group(0) for m in template_mod.PLACEHOLDER.finditer(text)]
        assert not [p for p in leftover if not p.startswith("{{WORKSTREAM")], (path, leftover)


def test_the_workstream_template_survives_scaffolding(scaffolded):
    tasks = (scaffolded.work_dir / "_template" / "02_tasks" / "tasks.md").read_text(encoding="utf-8")
    assert "{{WORKSTREAM_OWNER}}" in tasks


def test_declared_facts_are_substituted(scaffolded):
    manifest = scaffolded.manifest_path.read_text(encoding="utf-8")
    assert "brand-guidelines" in manifest
    assert "role:brand-lead" in manifest


def test_a_bad_name_is_rejected(root, tmp_path):
    with pytest.raises(UsageError):
        template_mod.scaffold(root / "template", tmp_path / "x", name="Not A Name", owner="person:a")


def test_a_non_empty_destination_needs_force(root, tmp_path):
    (tmp_path / "occupied").mkdir()
    (tmp_path / "occupied" / "file.txt").write_text("hi", encoding="utf-8")
    with pytest.raises(UsageError):
        template_mod.scaffold(root / "template", tmp_path / "occupied", name="x", owner="person:a")


def test_a_scaffolded_repository_can_still_read_the_standards(scaffolded):
    """A writer cited `V-05` must be able to read V-05 from their own repository."""
    from atlas.core import specs as specs_mod

    assert not scaffolded.is_standards_source
    specs = specs_mod.load_specs(scaffolded.spec_dir)
    assert [spec.id for spec in specs][:3] == ["voice", "language", "structure"]


def test_a_scaffolded_repository_validates_against_packaged_schemas(scaffolded):
    from atlas.core.manifest import validate_manifest

    assert validate_manifest(scaffolded.manifest_path, scaffolded.schema_dir, "project") == []
