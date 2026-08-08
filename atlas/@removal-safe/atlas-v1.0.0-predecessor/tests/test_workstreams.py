"""WORKSTREAM contract tests (spec/workstream.md).

The system's promise is that the dashboard, the machine index, and the Markdown
never disagree, and that a workstream cannot claim to be further along than its
task table says. These tests are that promise, made checkable.
"""

from __future__ import annotations

import pathlib
import re

import pytest
import yaml

from atlas.core import workstream as ws
from atlas.paths import Repository

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORK = ROOT / "work"
REPO = Repository(ROOT)

ALL = ws.load_all(REPO)
IDS = [w.id for w in ALL]


# ------------------------------------------------------------------ structure

def test_work_root_exists_with_generated_artifacts():
    assert (WORK / "README.md").exists()
    assert (WORK / "index.yaml").exists()
    assert (WORK / "_template").is_dir()


def test_template_carries_the_full_skeleton():
    """A scaffold that is missing a section teaches every workstream to skip it."""
    for section in ws.SECTIONS:
        assert (WORK / "_template" / section).is_dir(), f"template lacks {section}"
    assert (WORK / "_template" / "README.md").exists()
    assert (WORK / "_template" / "workstream.yaml").exists()
    for sub in ("handoffs", "logs"):
        assert (WORK / "_template" / "08_agents" / sub).is_dir()


@pytest.mark.parametrize("workstream", ALL, ids=[w.name for w in ALL])
def test_manifest_matches_directory(workstream: ws.Workstream):
    """Directory number and slug are the identity; the manifest restates it (W-02, W-03)."""
    match = ws.DIR_RE.match(workstream.name)
    assert match, f"{workstream.name} is not NN_slug"
    assert workstream.id == match["num"]
    assert workstream.slug == match["slug"]


@pytest.mark.parametrize("workstream", ALL, ids=[w.name for w in ALL])
def test_every_workstream_has_the_full_skeleton(workstream: ws.Workstream):
    for section in ws.SECTIONS:
        assert (workstream.directory / section).exists(), f"{workstream.name} lacks {section}"


def test_workstream_numbers_are_unique():
    assert len(IDS) == len(set(IDS)), f"duplicate workstream numbers: {IDS}"


# ----------------------------------------------------------------- validation

def test_validator_passes():
    """The repository is self-hosting: every workstream must be valid."""
    violations = ws.validate(REPO)
    assert violations == [], "\n".join(v.render() for v in violations)


@pytest.mark.parametrize("workstream", ALL, ids=[w.name for w in ALL])
def test_progress_is_derived_not_asserted(workstream: ws.Workstream):
    """Counted from the task table, never written by hand (W-10)."""
    declared = workstream.data.get("progress") or {}
    assert declared.get("tasks_total") == workstream.total
    assert declared.get("tasks_done") == workstream.done


@pytest.mark.parametrize("workstream", ALL, ids=[w.name for w in ALL])
def test_done_workstreams_carry_evidence(workstream: ws.Workstream):
    """`done` is a claim; evidence is what makes it checkable (W-I5)."""
    if workstream.status != "done":
        pytest.skip("not done")
    evidence = workstream.directory / "07_validation" / "evidence.md"
    assert evidence.exists()
    assert "| " in evidence.read_text(encoding="utf-8"), "evidence.md has no evidence table"


@pytest.mark.parametrize("workstream", ALL, ids=[w.name for w in ALL])
def test_at_most_one_orchestrator(workstream: ws.Workstream):
    """Two orchestrators is no orchestrator (W-15)."""
    orchestrators = [a for a in workstream.agents if a.get("role") == "orchestrator"]
    assert len(orchestrators) <= 1


@pytest.mark.parametrize("workstream", ALL, ids=[w.name for w in ALL])
def test_agent_scopes_are_concrete(workstream: ws.Workstream):
    for agent in workstream.agents:
        scope = agent.get("scope")
        assert scope, f"agent {agent.get('id')} has no scope"
        assert scope.strip().lower() not in {"tbd", "n/a", "-", "—"}


@pytest.mark.parametrize("workstream", ALL, ids=[w.name for w in ALL])
def test_task_rows_are_well_formed(workstream: ws.Workstream):
    """Every non-todo task has an owner; every done task has evidence (W-13)."""
    for task in workstream.tasks:
        assert task.status in ws.TASK_STATUSES, f"{task.id}: {task.status!r}"
        if task.status != "todo":
            assert task.owner not in ws.EMPTY_CELLS, f"{task.id} has no owner"
        if task.status == "done":
            assert task.evidence not in ws.EMPTY_CELLS, f"{task.id} has no evidence"


def test_dependencies_resolve_and_are_acyclic():
    known = set(IDS)
    graph = {w.id: w.depends_on for w in ALL}
    for workstream_id, dependencies in graph.items():
        for dependency in dependencies:
            assert dependency in known, f"{workstream_id} depends on unknown {dependency}"
    assert ws._cycles(graph) == []


# ------------------------------------------------------------------ generated

def test_index_is_in_sync_with_manifests():
    """`atlas work sync` is idempotent; a stale index is a lie with a timestamp."""
    on_disk = yaml.safe_load((WORK / "index.yaml").read_text(encoding="utf-8"))
    expected = ws.build_index(ALL)
    assert ws._index_body(on_disk) == ws._index_body(expected), (
        "work/index.yaml is stale — run `atlas work sync`"
    )


def test_dashboard_is_generated_and_says_so():
    dashboard = (WORK / "README.md").read_text(encoding="utf-8")
    assert dashboard.startswith("<!-- GENERATED"), "the dashboard must declare that it is derived"
    assert "atlas work sync" in dashboard


def test_dashboard_lists_every_live_workstream():
    dashboard = (WORK / "README.md").read_text(encoding="utf-8")
    for workstream in ALL:
        if workstream.archived:
            continue
        assert workstream.title in dashboard, f"{workstream.id} missing from the dashboard"


def test_rendering_the_dashboard_is_deterministic():
    """Two renders of the same input must be byte-identical, or CI thrashes."""
    assert ws.render_dashboard(ALL) == ws.render_dashboard(ALL)


# ------------------------------------------------------------------ lifecycle

def test_create_sync_and_validate_round_trip(tmp_path):
    """A scaffolded workstream is valid, counted, and archivable."""
    import shutil

    sandbox = tmp_path / "repo"
    sandbox.mkdir()
    shutil.copy2(ROOT / "project.yaml", sandbox / "project.yaml")
    shutil.copytree(WORK / "_template", sandbox / "work" / "_template")
    (sandbox / "spec" / "schemas").mkdir(parents=True)
    shutil.copy2(
        ROOT / "spec" / "schemas" / "workstream.schema.json",
        sandbox / "spec" / "schemas" / "workstream.schema.json",
    )
    repo = Repository(sandbox)

    created = ws.create(repo, "try-the-system", owner="person:tester")
    assert created.id == "01"
    assert created.slug == "try-the-system"

    count, changed = ws.sync(repo)
    assert count == 1
    assert (sandbox / "work" / "index.yaml").exists()
    assert (sandbox / "work" / "README.md").exists()

    # Sync is idempotent: a second run changes nothing.
    _, again = ws.sync(repo)
    assert again == []

    assert ws.validate(repo) == []

    # A live workstream cannot be archived; a done one can.
    from atlas.errors import UsageError

    with pytest.raises(UsageError):
        ws.archive(repo, "01")


def test_slugs_must_be_lowercase_hyphenated(tmp_path):
    from atlas.errors import UsageError

    shutil_repo = Repository(ROOT)
    with pytest.raises(UsageError):
        ws.create(shutil_repo, "Not A Slug")


def test_template_no_longer_ships_a_copy_of_the_tooling():
    """ADR-0007: the template depends on the package rather than copying it.

    A copy is a fork with a delay; this is the drift that prompted the change.
    """
    assert not (ROOT / "template" / "scripts" / "work.py").exists()
    readme = (ROOT / "template" / "scripts" / "README.md").read_text(encoding="utf-8")
    assert "atlas-standard" in readme


def test_template_ships_the_schema_it_validates_against():
    """A scaffolded repository must be able to validate its own work offline."""
    assert (ROOT / "template" / "work" / "workstream.schema.json").exists()
    assert (ROOT / "template" / "work" / "_template").is_dir()
