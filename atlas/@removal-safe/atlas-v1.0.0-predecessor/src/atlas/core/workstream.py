"""The WORKSTREAM system (``spec/workstream.md``).

Markdown is canonical (W-I2). This module derives the machine index and the
dashboard from the workstream manifests and task tables; it never invents facts
and it never edits a workstream's prose. Progress is *counted* from the task
table, which is why a workstream cannot claim to be further along than its
tasks say it is.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import json
import pathlib
import re
import shutil
import typing as t

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from ..errors import NotFoundError, UsageError
from ..paths import Repository
from .manifest import Violation, normalize

__all__ = [
    "SECTIONS",
    "STATUS_ORDER",
    "TASK_STATUSES",
    "Task",
    "Workstream",
    "load_all",
    "create",
    "sync",
    "validate",
    "archive",
    "render_dashboard",
    "build_index",
]

SECTIONS = (
    "01_plan",
    "02_tasks",
    "03_requirements",
    "04_decisions",
    "05_research",
    "06_deliverables",
    "07_validation",
    "08_agents",
    "09_issues",
)
#: Dashboard grouping order: what needs attention first, terminal states last.
STATUS_ORDER = ("active", "blocked", "review", "planned", "done", "cancelled")
TERMINAL_STATUSES = frozenset({"done", "cancelled"})
TASK_STATUSES = frozenset({"todo", "active", "blocked", "done", "dropped"})
DONE_STATUSES = frozenset({"done"})
EMPTY_CELLS = frozenset({"", "—", "-", "–", "n/a"})

DIR_RE = re.compile(r"^(?P<num>\d{2,4})_(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$")
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TASK_ID_RE = re.compile(r"^T-\d+$")


@dataclasses.dataclass(frozen=True)
class Task:
    """One row of ``02_tasks/tasks.md``: the canonical tracker (W-10)."""

    id: str
    title: str
    owner: str
    status: str
    evidence: str

    @property
    def done(self) -> bool:
        return self.status in DONE_STATUSES

    def as_dict(self) -> dict[str, str]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class Workstream:
    """A numbered initiative: its directory, manifest, and counted progress."""

    directory: pathlib.Path
    data: dict[str, t.Any]
    tasks: list[Task]
    archived: bool
    root: pathlib.Path

    # --- identity ---
    @property
    def id(self) -> str:
        return str(self.data.get("id", ""))

    @property
    def slug(self) -> str:
        return str(self.data.get("slug", ""))

    @property
    def title(self) -> str:
        return str(self.data.get("title", self.slug))

    @property
    def status(self) -> str:
        return str(self.data.get("status", "planned"))

    @property
    def owner(self) -> str:
        return str(self.data.get("owner", "person:unassigned"))

    @property
    def summary(self) -> str:
        return str(self.data.get("summary") or "")

    @property
    def target(self) -> str:
        return str(self.data.get("target") or "")

    @property
    def depends_on(self) -> list[str]:
        return [str(d) for d in (self.data.get("depends_on") or [])]

    @property
    def agents(self) -> list[dict[str, t.Any]]:
        return list(self.data.get("agents") or [])

    # --- derived ---
    @property
    def name(self) -> str:
        return self.directory.name

    @property
    def rel(self) -> str:
        return self.directory.relative_to(self.root).as_posix()

    @property
    def total(self) -> int:
        return len(self.tasks)

    @property
    def done(self) -> int:
        return sum(1 for task in self.tasks if task.done)

    @property
    def percent(self) -> int:
        return 100 * self.done // self.total if self.total else 0

    @property
    def progress(self) -> dict[str, int]:
        return {"tasks_total": self.total, "tasks_done": self.done}

    @property
    def blocked_tasks(self) -> list[Task]:
        return [task for task in self.tasks if task.status == "blocked"]

    def as_dict(self) -> dict[str, t.Any]:
        payload = {k: v for k, v in self.data.items() if not k.startswith("_")}
        payload["progress"] = self.progress
        payload["path"] = self.rel
        return payload


# --------------------------------------------------------------------- loading

def _numbered_dirs(root: pathlib.Path, include_archive: bool) -> list[pathlib.Path]:
    work = root / "work"
    roots = [work] + ([work / "archive"] if include_archive else [])
    found: list[pathlib.Path] = []
    for base in roots:
        if base.is_dir():
            found += [d for d in base.iterdir() if d.is_dir() and DIR_RE.match(d.name)]
    return sorted(found, key=lambda d: int(DIR_RE.match(d.name)["num"]))


def parse_tasks(directory: pathlib.Path) -> list[Task]:
    """Parse the task table. Rows that are not tasks are ignored, not errors.

    ``tasks.md`` is a document a human writes, so it contains prose, headings,
    and legend tables alongside the tracker. Anything whose first cell is not a
    ``T-<n>`` identifier is simply not a task row.
    """
    path = directory / "02_tasks" / "tasks.md"
    if not path.exists():
        return []
    tasks: list[Task] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 4 or not TASK_ID_RE.match(cells[0]):
            continue
        cells += [""] * (5 - len(cells))
        tasks.append(
            Task(
                id=cells[0],
                title=cells[1],
                owner=cells[2],
                status=cells[3].lower(),
                evidence=cells[4],
            )
        )
    return tasks


def load_one(directory: pathlib.Path, root: pathlib.Path) -> Workstream:
    manifest = directory / "workstream.yaml"
    data: dict[str, t.Any] = {}
    if manifest.exists():
        parsed = normalize(yaml.safe_load(manifest.read_text(encoding="utf-8")))
        if isinstance(parsed, dict):
            data = parsed
    return Workstream(
        directory=directory,
        data=data,
        tasks=parse_tasks(directory),
        archived=directory.parent.name == "archive",
        root=root,
    )


def load_all(repo: Repository, *, include_archive: bool = True) -> list[Workstream]:
    """Every workstream in the repository, ordered by number."""
    return [load_one(d, repo.root) for d in _numbered_dirs(repo.root, include_archive)]


def find(repo: Repository, identifier: str) -> Workstream:
    """Resolve a workstream by number or slug, live or archived."""
    wanted = identifier.strip().lower()
    candidates = load_all(repo)
    for workstream in candidates:
        if wanted in {workstream.id.lower(), workstream.slug.lower(), workstream.name.lower()}:
            return workstream
    # Numbers are commonly typed without their leading zero.
    if wanted.isdigit():
        for workstream in candidates:
            if workstream.id.lstrip("0") == wanted.lstrip("0"):
                return workstream
    known = ", ".join(f"{w.id} {w.slug}" for w in candidates) or "none"
    raise NotFoundError(f"no workstream {identifier!r}", hint=f"Known workstreams: {known}")


# ---------------------------------------------------------------------- schema

def _schema(repo: Repository) -> dict[str, t.Any]:
    """Locate the workstream schema.

    One codebase serves two homes. In the standards repository the schema is a
    normative artifact under ``spec/schemas/``; in a scaffolded repository it
    ships beside the work it validates. Resolving both is what lets a
    scaffolded repository run the same tooling without a second copy of it.
    """
    for candidate in (
        repo.schemas / "workstream.schema.json",
        repo.work / "workstream.schema.json",
    ):
        if candidate.exists():
            return json.loads(candidate.read_text(encoding="utf-8"))
    raise NotFoundError(
        "workstream.schema.json not found in spec/schemas/ or work/",
        hint="Run `atlas template sync` in the standards repository, or re-scaffold.",
    )


# ------------------------------------------------------------------------- new

def create(
    repo: Repository,
    slug: str,
    *,
    title: str | None = None,
    owner: str = "person:unassigned",
    summary: str = "",
) -> Workstream:
    """Scaffold the next workstream from ``work/_template``."""
    if not SLUG_RE.match(slug):
        raise UsageError(
            f"slug must be lowercase-hyphenated: {slug!r}",
            hint="Use letters, digits, and single hyphens: `migrate-the-fleet`.",
        )
    template = repo.work / "_template"
    if not template.is_dir():
        raise NotFoundError(
            f"no workstream template at {repo.rel(template)}",
            hint="A repository adopting WORKSTREAM ships work/_template/.",
        )

    existing = _numbered_dirs(repo.root, include_archive=True)
    nxt = max((int(DIR_RE.match(d.name)["num"]) for d in existing), default=0) + 1
    number = str(nxt).zfill(max(2, len(str(nxt))))
    destination = repo.work / f"{number}_{slug}"
    if destination.exists():
        raise UsageError(f"{repo.rel(destination)} already exists")

    shutil.copytree(template, destination)
    substitutions = {
        "{{ID}}": number,
        "{{SLUG}}": slug,
        "{{TITLE}}": title or slug.replace("-", " ").capitalize(),
        "{{OWNER}}": owner,
        "{{DATE}}": dt.date.today().isoformat(),
        "{{SUMMARY}}": summary,
    }
    for path in destination.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml"}:
            text = path.read_text(encoding="utf-8")
            for needle, value in substitutions.items():
                text = text.replace(needle, value)
            path.write_text(text, encoding="utf-8")
    return load_one(destination, repo.root)


# ------------------------------------------------------------------------ sync

def build_index(workstreams: list[Workstream]) -> dict[str, t.Any]:
    """The machine index: an agent's entry point to the work (W-11)."""
    return {
        "standard": "workstream/1.0",
        "generated": dt.date.today().isoformat(),
        "counts": {
            status: sum(1 for w in workstreams if w.status == status)
            for status in STATUS_ORDER
        },
        "workstreams": [w.as_dict() for w in workstreams],
    }


def sync(repo: Repository) -> tuple[int, list[str]]:
    """Write derived progress back, then regenerate the index and dashboard.

    Returns the workstream count and the list of files actually changed, so a
    caller can report "nothing to do" honestly rather than claiming work it did
    not perform.
    """
    workstreams = load_all(repo)
    changed: list[str] = []

    for workstream in workstreams:
        manifest = workstream.directory / "workstream.yaml"
        if not manifest.exists():
            continue
        data = normalize(yaml.safe_load(manifest.read_text(encoding="utf-8"))) or {}
        if data.get("progress") != workstream.progress:
            data["progress"] = workstream.progress
            manifest.write_text(
                yaml.safe_dump(data, sort_keys=False, width=100, allow_unicode=True),
                encoding="utf-8",
            )
            changed.append(repo.rel(manifest))

    index_path = repo.work / "index.yaml"
    index_text = (
        "# GENERATED by `atlas work sync`. Do not edit (W-11).\n"
        + yaml.safe_dump(build_index(workstreams), sort_keys=False, width=100, allow_unicode=True)
    )
    if not index_path.exists() or index_path.read_text(encoding="utf-8") != index_text:
        index_path.write_text(index_text, encoding="utf-8")
        changed.append(repo.rel(index_path))

    dashboard_path = repo.work / "README.md"
    dashboard = render_dashboard(workstreams, has_spec=(repo.spec / "workstream.md").exists())
    if not dashboard_path.exists() or dashboard_path.read_text(encoding="utf-8") != dashboard:
        dashboard_path.write_text(dashboard, encoding="utf-8")
        changed.append(repo.rel(dashboard_path))

    return len(workstreams), changed


def _bar(done: int, total: int, width: int = 10) -> str:
    if not total:
        return "—"
    filled = round(width * done / total)
    return f"`{'█' * filled}{'·' * (width - filled)}` {done}/{total}"


def render_dashboard(workstreams: list[Workstream], *, has_spec: bool = True) -> str:
    """Render ``work/README.md``: the human view of the same facts."""
    today = dt.date.today().isoformat()
    live = [w for w in workstreams if not w.archived]
    counts = " · ".join(
        f"{status}: {n}"
        for status in STATUS_ORDER
        if (n := sum(1 for w in live if w.status == status))
    )
    spec_link = (
        "([`spec/workstream.md`](../spec/workstream.md))" if has_spec else "(the WORKSTREAM standard)"
    )

    out: list[str] = [
        "<!-- GENERATED by `atlas work sync`. Do not edit (W-11). -->",
        "# Work Dashboard",
        "",
        f"**{len(live)} live workstream{'s' if len(live) != 1 else ''}**"
        + (f" · {counts}" if counts else "")
        + f" · generated {today}",
        "",
        f"Every initiative in this repository has exactly one home here {spec_link}. "
        "Markdown is canonical; this page and [`index.yaml`](index.yaml) are derived.",
        "",
    ]

    if not live:
        out += [
            "> [!NOTE]",
            "> No live workstreams. Open one with `atlas work new <slug> --owner person:you`.",
            "",
        ]

    for status in STATUS_ORDER:
        group = [w for w in live if w.status == status]
        if not group:
            continue
        out += [
            f"## {status.capitalize()}",
            "",
            "| # | Workstream | Owner | Progress | Target | Agents |",
            "|---|---|---|---|---|---|",
        ]
        for workstream in group:
            agents = ", ".join(f"`{a['id']}`" for a in workstream.agents) or "—"
            out.append(
                f"| `{workstream.id}` | [{workstream.title}]({workstream.name}/) "
                f"| `{workstream.owner}` | {_bar(workstream.done, workstream.total)} "
                f"| {workstream.target or '—'} | {agents} |"
            )
        out.append("")

    dependencies = [(w.id, dep) for w in workstreams for dep in w.depends_on]
    if dependencies:
        out += ["## Dependencies", "", "| Workstream | Depends on |", "|---|---|"]
        out += [f"| `{wid}` | `{dep}` |" for wid, dep in dependencies]
        out.append("")

    archived = [w for w in workstreams if w.archived]
    if archived:
        out += ["## Archive", "", "| # | Workstream | Status | Closed |", "|---|---|---|---|"]
        out += [
            f"| `{w.id}` | {w.title} | {w.status} | {w.data.get('closed') or '—'} |"
            for w in archived
        ]
        out.append("")

    out += [
        "---",
        "",
        "Create a workstream: `atlas work new <slug> --owner person:you`  ",
        "Refresh this page: `atlas work sync`",
    ]
    return "\n".join(out) + "\n"


# -------------------------------------------------------------------- validate

def validate(repo: Repository) -> list[Violation]:
    """Check every workstream against the WORKSTREAM standard.

    Ordered from structural to semantic so the first message a reader sees is
    the one most likely to explain the rest: a missing manifest makes every
    downstream check meaningless, so it short-circuits.
    """
    violations: list[Violation] = []
    validator = Draft202012Validator(_schema(repo), format_checker=FormatChecker())
    directories = _numbered_dirs(repo.root, include_archive=True)
    seen: dict[str, str] = {}
    graph: dict[str, list[str]] = {}

    for directory in directories:
        rel = directory.relative_to(repo.root).as_posix()
        match = DIR_RE.match(directory.name)
        assert match  # _numbered_dirs only yields matching names
        number, slug = match["num"], match["slug"]

        manifest = directory / "workstream.yaml"
        if not manifest.exists():
            violations.append(Violation(rel, "missing workstream.yaml", "W-05"))
            continue

        workstream = load_one(directory, repo.root)
        for error in validator.iter_errors(workstream.data):
            violations.append(
                Violation(
                    rel,
                    error.message,
                    pointer="/".join(str(p) for p in error.path) or None,
                )
            )

        if workstream.id != number:
            violations.append(
                Violation(rel, f"manifest id {workstream.id!r} != directory number {number!r}", "W-03")
            )
        if workstream.slug != slug:
            violations.append(
                Violation(rel, f"manifest slug {workstream.slug!r} != directory slug {slug!r}", "W-02")
            )
        if number in seen:
            violations.append(
                Violation(rel, f"duplicate workstream number {number} (also {seen[number]})", "W-I3")
            )
        seen[number] = rel
        graph[workstream.id] = workstream.depends_on

        for section in (*SECTIONS, "README.md"):
            if not (directory / section).exists():
                violations.append(Violation(rel, f"missing required section {section}", "W-05"))
        for sub in ("handoffs", "logs"):
            if not (directory / "08_agents" / sub).exists():
                violations.append(Violation(rel, f"missing 08_agents/{sub}", "W-16"))

        orchestrators = [a for a in workstream.agents if a.get("role") == "orchestrator"]
        if len(orchestrators) > 1:
            violations.append(
                Violation(rel, f"{len(orchestrators)} orchestrators; at most one is allowed", "W-15")
            )

        if workstream.status == "done":
            evidence = directory / "07_validation" / "evidence.md"
            if not evidence.exists() or "| " not in evidence.read_text(encoding="utf-8"):
                violations.append(
                    Violation(rel, "status 'done' without validation evidence", "W-I5")
                )
            open_tasks = [t for t in workstream.tasks if t.status in {"todo", "active", "blocked"}]
            if open_tasks:
                ids = ", ".join(t.id for t in open_tasks[:5])
                violations.append(
                    Violation(rel, f"status 'done' with {len(open_tasks)} unfinished task(s): {ids}", "W-I5")
                )

        for task in workstream.tasks:
            if task.status not in TASK_STATUSES:
                violations.append(
                    Violation(rel, f"{task.id}: invalid task status {task.status!r}", "W-13")
                )
            if task.status != "todo" and task.owner.lower() in EMPTY_CELLS:
                violations.append(Violation(rel, f"{task.id}: non-todo task without an owner", "W-13"))
            if task.status == "done" and task.evidence.lower() in EMPTY_CELLS:
                violations.append(Violation(rel, f"{task.id}: done task without evidence", "W-13"))

    known = set(seen)
    for workstream_id, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in known:
                violations.append(
                    Violation(
                        f"work/{workstream_id}",
                        f"depends_on unknown workstream {dependency}",
                        "WS-06",
                    )
                )
    violations += _cycles(graph)

    index_path = repo.work / "index.yaml"
    if not index_path.exists():
        violations.append(Violation("work/index.yaml", "missing. Run `atlas work sync`", "W-11"))
    else:
        expected = build_index(load_all(repo))
        actual = normalize(yaml.safe_load(index_path.read_text(encoding="utf-8"))) or {}
        if _index_body(actual) != _index_body(expected):
            violations.append(
                Violation("work/index.yaml", "stale. Run `atlas work sync`", "W-11")
            )

    return violations


def _index_body(index: dict[str, t.Any]) -> t.Any:
    """The comparable part of the index: everything but its generation date.

    Comparing whole documents would report the index as stale every day at
    midnight, which trains people to run sync reflexively and to stop reading
    what it says.
    """
    return {k: v for k, v in (index or {}).items() if k != "generated"}


def _cycles(graph: dict[str, list[str]]) -> list[Violation]:
    """Report dependency cycles (WS-06), each once, with its full path."""
    seen: set[str] = set()
    stack: list[str] = []
    on_stack: set[str] = set()
    found: list[Violation] = []
    reported: set[frozenset[str]] = set()

    def walk(node: str) -> None:
        if node in on_stack:
            cycle = stack[stack.index(node):] + [node]
            key = frozenset(cycle)
            if key not in reported:
                reported.add(key)
                found.append(Violation("work/", "dependency cycle: " + " → ".join(cycle), "WS-06"))
            return
        if node in seen or node not in graph:
            return
        seen.add(node)
        stack.append(node)
        on_stack.add(node)
        for nxt in graph[node]:
            walk(nxt)
        stack.pop()
        on_stack.discard(node)

    for node in list(graph):
        walk(node)
    return found


# --------------------------------------------------------------------- archive

def archive(repo: Repository, identifier: str) -> Workstream:
    """Move a terminal workstream into ``work/archive/`` (W-04)."""
    workstream = find(repo, identifier)
    if workstream.archived:
        raise UsageError(f"{workstream.name} is already archived")
    if workstream.status not in TERMINAL_STATUSES:
        raise UsageError(
            f"{workstream.name} is '{workstream.status}'; only done or cancelled workstreams archive",
            hint="Set `status: done` in its workstream.yaml once the evidence is recorded.",
        )
    destination = repo.work / "archive"
    destination.mkdir(exist_ok=True)
    shutil.move(str(workstream.directory), str(destination / workstream.name))
    return load_one(destination / workstream.name, repo.root)
