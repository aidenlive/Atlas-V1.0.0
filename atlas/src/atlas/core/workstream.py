"""Workstreams: editorial work, planned and counted in the repository.

A workstream is one numbered folder under ``work/`` with the same five sections
in the same order, every time:

===================  =====================================================
``01_brief``         what we are writing, for whom, and why
``02_tasks``         the task table — the only place status is recorded
``03_drafts``        drafts in progress, or pointers to where they live
``04_review``        reviewers, comments, and sign-off
``05_publication``   where it went, when, and what happens to it next
===================  =====================================================

A fixed shape means a person joining on Tuesday and an agent picking the work up
on Wednesday both find the brief in ``01_brief/`` without asking anyone.

Progress is **counted, not claimed**. The task table is the original; the
dashboard a person reads (``work/README.md``) and the index an agent reads
(``work/index.yaml``) are both generated from it. A workstream therefore cannot
report itself further along than its own tasks say it is.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import pathlib
import re
import shutil
import typing as t

import yaml

from ..errors import NotFoundError, UsageError
from .manifest import Violation, load_yaml

__all__ = [
    "Task",
    "Workstream",
    "SECTIONS",
    "STATUSES",
    "TASK_STATES",
    "load_workstreams",
    "find_workstream",
    "create_workstream",
    "build_index",
    "render_dashboard",
    "sync",
    "validate_workstreams",
]

SECTIONS: tuple[str, ...] = (
    "01_brief",
    "02_tasks",
    "03_drafts",
    "04_review",
    "05_publication",
)

#: Workstream lifecycle, in order.
STATUSES: tuple[str, ...] = ("planned", "active", "blocked", "review", "published", "closed")

#: Task states. `done` is the only one that counts towards progress.
TASK_STATES: tuple[str, ...] = ("todo", "doing", "blocked", "done")

_ROW = re.compile(r"^\|(?P<cells>.+)\|\s*$")
_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclasses.dataclass(frozen=True)
class Task:
    id: str
    title: str
    owner: str
    state: str

    @property
    def done(self) -> bool:
        return self.state == "done"

    def as_dict(self) -> dict[str, str]:
        return {"id": self.id, "title": self.title, "owner": self.owner, "state": self.state}


@dataclasses.dataclass
class Workstream:
    number: str
    slug: str
    path: pathlib.Path
    meta: dict[str, t.Any]
    tasks: list[Task]

    @property
    def id(self) -> str:
        return f"{self.number}_{self.slug}"

    @property
    def title(self) -> str:
        return str(self.meta.get("title", self.slug.replace("-", " ")))

    @property
    def status(self) -> str:
        return str(self.meta.get("status", "planned"))

    @property
    def owner(self) -> str:
        return str(self.meta.get("owner", "unassigned"))

    @property
    def done(self) -> int:
        return sum(1 for task in self.tasks if task.done)

    @property
    def total(self) -> int:
        return len(self.tasks)

    @property
    def percent(self) -> int:
        return round(100 * self.done / self.total) if self.total else 0

    @property
    def blocked(self) -> list[Task]:
        return [task for task in self.tasks if task.state == "blocked"]

    def as_dict(self, *, with_tasks: bool = False) -> dict[str, t.Any]:
        payload = {
            "id": self.id,
            "number": self.number,
            "slug": self.slug,
            "title": self.title,
            "status": self.status,
            "owner": self.owner,
            "kind": self.meta.get("kind"),
            "audience": self.meta.get("audience"),
            "done": self.done,
            "total": self.total,
            "percent": self.percent,
            "blocked": len(self.blocked),
        }
        if with_tasks:
            payload["tasks"] = [task.as_dict() for task in self.tasks]
        return payload


# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------


def parse_tasks(text: str) -> list[Task]:
    """Read the task table.

    Anything that is not a four-column row is ignored, so a table can carry a
    heading, a separator, and prose around it without special handling.
    """
    tasks: list[Task] = []
    for line in text.splitlines():
        match = _ROW.match(line.strip())
        if not match:
            continue
        cells = [cell.strip() for cell in match.group("cells").split("|")]
        if len(cells) < 4:
            continue
        ident, title, owner, state = cells[0], cells[1], cells[2], cells[3].lower()
        if set(ident) <= {"-", ":", " "} or ident.lower() == "id":
            continue
        tasks.append(Task(id=ident, title=title, owner=owner, state=state))
    return tasks


def load_workstream(path: pathlib.Path) -> Workstream:
    number, _, slug = path.name.partition("_")
    manifest = path / "workstream.yaml"
    meta = load_yaml(manifest) if manifest.is_file() else {}
    table = path / "02_tasks" / "tasks.md"
    tasks = parse_tasks(table.read_text(encoding="utf-8")) if table.is_file() else []
    return Workstream(number=number, slug=slug, path=path, meta=meta, tasks=tasks)


def load_workstreams(work_dir: pathlib.Path) -> list[Workstream]:
    if not work_dir.is_dir():
        return []
    found = [
        load_workstream(path)
        for path in sorted(work_dir.iterdir())
        if path.is_dir() and not path.name.startswith((".", "_"))
    ]
    return sorted(found, key=lambda ws: ws.number)


def find_workstream(work_dir: pathlib.Path, needle: str) -> Workstream:
    wanted = needle.strip().lower()
    for workstream in load_workstreams(work_dir):
        if wanted in {workstream.number, workstream.slug.lower(), workstream.id.lower()}:
            return workstream
    known = ", ".join(ws.id for ws in load_workstreams(work_dir)) or "none"
    raise NotFoundError(f"no workstream matching {needle!r}", hint=f"known: {known}")


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------


def next_number(work_dir: pathlib.Path) -> str:
    existing = [ws.number for ws in load_workstreams(work_dir) if ws.number.isdigit()]
    return f"{max((int(n) for n in existing), default=0) + 1:02d}"


def create_workstream(
    work_dir: pathlib.Path,
    slug: str,
    *,
    owner: str,
    title: str | None = None,
    kind: str = "guide",
    audience: str = "internal",
) -> Workstream:
    """Scaffold a workstream from ``work/_template``."""
    if not _SLUG.match(slug):
        raise UsageError(
            f"{slug!r} is not a valid slug",
            hint="use lower-case words joined by hyphens, e.g. rewrite-onboarding-guide",
        )
    template = work_dir / "_template"
    if not template.is_dir():
        raise NotFoundError(f"no workstream template at {template}")

    number = next_number(work_dir)
    destination = work_dir / f"{number}_{slug}"
    if destination.exists():
        raise UsageError(f"{destination} already exists")

    shutil.copytree(template, destination)
    today = dt.date.today().isoformat()
    meta = {
        "id": f"{number}_{slug}",
        "title": title or slug.replace("-", " ").capitalize(),
        "status": "planned",
        "owner": owner,
        "kind": kind,
        "audience": audience,
        "opened": today,
        "target": None,
        "standards": ["voice", "structure", "checklist"],
    }
    (destination / "workstream.yaml").write_text(
        "# Generated by `atlas work new`. Edit freely; `atlas work validate` checks it.\n"
        + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    readme = destination / "README.md"
    if readme.is_file():
        readme.write_text(
            readme.read_text(encoding="utf-8")
            .replace("{{WORKSTREAM_TITLE}}", str(meta["title"]))
            .replace("{{WORKSTREAM_ID}}", str(meta["id"]))
            .replace("{{WORKSTREAM_OWNER}}", owner)
            .replace("{{WORKSTREAM_DATE}}", today),
            encoding="utf-8",
        )
    return load_workstream(destination)


# ---------------------------------------------------------------------------
# Generated views
# ---------------------------------------------------------------------------


def build_index(work_dir: pathlib.Path) -> dict[str, t.Any]:
    workstreams = load_workstreams(work_dir)
    return {
        "generated_by": "atlas work sync",
        "generated_on": dt.date.today().isoformat(),
        "count": len(workstreams),
        "done": sum(ws.done for ws in workstreams),
        "total": sum(ws.total for ws in workstreams),
        "workstreams": [ws.as_dict(with_tasks=True) for ws in workstreams],
    }


def _bar(percent: int, width: int = 10) -> str:
    filled = round(width * percent / 100)
    return "█" * filled + "·" * (width - filled)


def render_dashboard(work_dir: pathlib.Path) -> str:
    workstreams = load_workstreams(work_dir)
    total = sum(ws.total for ws in workstreams)
    done = sum(ws.done for ws in workstreams)
    percent = round(100 * done / total) if total else 0
    lines = [
        "<!-- Generated by `atlas work sync`. Edit the task tables, not this file. -->",
        "",
        "# Work",
        "",
        "Every editorial initiative in this repository, one numbered folder each.",
        "Progress is counted from the task tables, so nothing here can claim more",
        "than its own tasks say.",
        "",
        f"**{done} of {total} tasks complete ({percent}%)** across {len(workstreams)} workstreams.",
        "",
        "| # | Workstream | Owner | Status | Progress |",
        "|---|---|---|---|---|",
    ]
    for ws in workstreams:
        lines.append(
            f"| {ws.number} | [{ws.title}]({ws.path.name}/) | {ws.owner} | "
            f"`{ws.status}` | {_bar(ws.percent)} {ws.done}/{ws.total} |"
        )
    blocked = [(ws, task) for ws in workstreams for task in ws.blocked]
    if blocked:
        lines += ["", "## Blocked", "", "| Workstream | Task | Owner |", "|---|---|---|"]
        lines += [f"| {ws.number} | {task.title} | {task.owner} |" for ws, task in blocked]
    lines += [
        "",
        "## Working here",
        "",
        "```bash",
        "atlas work new rewrite-onboarding --owner person:you   # open one",
        "atlas work list --status blocked                       # what is stuck",
        "atlas work show 01 --tasks                             # read the tasks",
        "atlas work sync                                        # regenerate this file",
        "```",
        "",
    ]
    return "\n".join(lines)


def sync(work_dir: pathlib.Path) -> list[pathlib.Path]:
    """Regenerate the dashboard and the index from the task tables."""
    written: list[pathlib.Path] = []
    dashboard = work_dir / "README.md"
    dashboard.write_text(render_dashboard(work_dir), encoding="utf-8")
    written.append(dashboard)

    index = work_dir / "index.yaml"
    index.write_text(
        "# Generated by `atlas work sync`. Do not edit by hand.\n"
        + yaml.safe_dump(build_index(work_dir), sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    written.append(index)
    return written


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_workstreams(work_dir: pathlib.Path, schema_dir: pathlib.Path) -> list[Violation]:
    from .manifest import load_schema, validate_against_schema

    violations: list[Violation] = []
    if not work_dir.is_dir():
        return violations

    try:
        schema = load_schema(schema_dir, "workstream")
    except NotFoundError:
        schema = None

    for workstream in load_workstreams(work_dir):
        relative = f"work/{workstream.path.name}"
        manifest = workstream.path / "workstream.yaml"
        if not manifest.is_file():
            violations.append(
                Violation(
                    rule="AUTHORITY A-06",
                    message="workstream has no workstream.yaml",
                    path=relative,
                )
            )
        elif schema is not None:
            violations.extend(
                validate_against_schema(
                    workstream.meta, schema, source=f"{relative}/workstream.yaml",
                    rule="AUTHORITY A-06",
                )
            )
        for section in SECTIONS:
            if not (workstream.path / section).is_dir():
                violations.append(
                    Violation(
                        rule="AUTHORITY A-07",
                        message=f"missing section `{section}/`",
                        path=relative,
                        hint="every workstream has the same five sections, in the same order",
                    )
                )
        for task in workstream.tasks:
            if task.state not in TASK_STATES:
                violations.append(
                    Violation(
                        rule="AUTHORITY A-08",
                        message=f"task {task.id} has unknown state {task.state!r}",
                        path=f"{relative}/02_tasks/tasks.md",
                        hint=f"one of: {', '.join(TASK_STATES)}",
                    )
                )
    return violations
