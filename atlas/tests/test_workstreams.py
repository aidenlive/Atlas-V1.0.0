"""Workstreams: parsing, counting, generating, and validating."""

from __future__ import annotations

import shutil

from atlas.core import workstream as ws_mod

TABLE = """
| ID | Task | Owner | Status |
|---|---|---|---|
| T1 | Write it | person:a | done |
| T2 | Review it | person:b | blocked |
"""


def test_task_table_parsing():
    tasks = ws_mod.parse_tasks(TABLE)
    assert [t.id for t in tasks] == ["T1", "T2"]
    assert tasks[0].done and not tasks[1].done


def test_separator_and_header_rows_are_ignored():
    assert len(ws_mod.parse_tasks(TABLE)) == 2


def test_progress_is_counted_not_claimed(repo):
    for workstream in ws_mod.load_workstreams(repo.work_dir):
        assert workstream.done == sum(1 for task in workstream.tasks if task.state == "done")
        assert workstream.percent == (
            round(100 * workstream.done / workstream.total) if workstream.total else 0
        )


def test_dashboard_is_current(repo):
    rendered = ws_mod.render_dashboard(repo.work_dir)
    on_disk = (repo.work_dir / "README.md").read_text(encoding="utf-8")
    assert rendered.strip() == on_disk.strip()


def test_workstreams_validate(repo):
    assert ws_mod.validate_workstreams(repo.work_dir, repo.schema_dir) == []


def test_new_workstream_gets_the_five_sections(repo, tmp_path):
    work = tmp_path / "work"
    work.mkdir()
    shutil.copytree(repo.work_dir / "_template", work / "_template")
    created = ws_mod.create_workstream(work, "write-the-thing", owner="person:you")
    assert created.number == "01"
    for section in ws_mod.SECTIONS:
        assert (created.path / section).is_dir()
    assert created.meta["owner"] == "person:you"


def test_numbers_do_not_collide(repo, tmp_path):
    work = tmp_path / "work"
    work.mkdir()
    shutil.copytree(repo.work_dir / "_template", work / "_template")
    ws_mod.create_workstream(work, "one", owner="person:you")
    second = ws_mod.create_workstream(work, "two", owner="person:you")
    assert second.number == "02"


def test_a_bad_slug_is_rejected(repo, tmp_path):
    from atlas.errors import UsageError
    import pytest

    work = tmp_path / "work"
    work.mkdir()
    shutil.copytree(repo.work_dir / "_template", work / "_template")
    with pytest.raises(UsageError):
        ws_mod.create_workstream(work, "Not A Slug", owner="person:you")
