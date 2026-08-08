"""Plan, track, and verify editorial work.

Every initiative is a numbered folder under ``work/`` with the same five
sections. The task table is the original; the dashboard and the index are
generated from it, so progress is counted rather than claimed.
"""

from __future__ import annotations

import argparse

from ...core import workstream as ws_mod
from ...errors import ExitCode, UsageError
from ...paths import discover
from ...terminal import Console

SUMMARY = "plan, track, and verify editorial work"


def configure(parser: argparse.ArgumentParser) -> None:
    subparsers = parser.add_subparsers(dest="subcommand", metavar="<subcommand>")

    new = subparsers.add_parser("new", help="open a workstream from the template")
    new.add_argument("slug", help="lower-case-with-hyphens")
    new.add_argument("--owner", required=True, help="who owns it, e.g. person:you or role:editorial-lead")
    new.add_argument("--title", help="human title (default: the slug, prettified)")
    new.add_argument("--kind", default="guide", help="what is being written (default: guide)")
    new.add_argument("--audience", default="internal", help="who it is for (default: internal)")

    listing = subparsers.add_parser("list", help="list workstreams")
    listing.add_argument("--status", help="only this status")
    listing.add_argument("--owner", help="only this owner")

    show = subparsers.add_parser("show", help="show one workstream")
    show.add_argument("id", help="number, slug, or full id")
    show.add_argument("--tasks", action="store_true", help="include the task table")

    subparsers.add_parser("sync", help="regenerate the dashboard and index from the task tables")
    subparsers.add_parser("validate", help="check every workstream's shape and manifest")


def run(args: argparse.Namespace, console: Console) -> int:
    repo = discover(args.directory)
    subcommand = getattr(args, "subcommand", None)
    if not subcommand:
        raise UsageError("`atlas work` needs a subcommand", hint="new, list, show, sync, validate")

    handler = {
        "new": _new,
        "list": _list,
        "show": _show,
        "sync": _sync,
        "validate": _validate,
    }[subcommand]
    return handler(args, console, repo)


def _new(args: argparse.Namespace, console: Console, repo) -> int:
    workstream = ws_mod.create_workstream(
        repo.work_dir,
        args.slug,
        owner=args.owner,
        title=args.title,
        kind=args.kind,
        audience=args.audience,
    )
    ws_mod.sync(repo.work_dir)
    if console.json_mode:
        console.json(workstream.as_dict())
        return int(ExitCode.OK)
    console.title(f"opened {workstream.id}")
    console.out()
    console.field("path", repo.relative(workstream.path))
    console.field("owner", workstream.owner)
    console.out()
    console.note("next: write the brief in 01_brief/brief.md, then add tasks in 02_tasks/tasks.md")
    return int(ExitCode.OK)


def _list(args: argparse.Namespace, console: Console, repo) -> int:
    workstreams = ws_mod.load_workstreams(repo.work_dir)
    if args.status:
        workstreams = [ws for ws in workstreams if ws.status == args.status]
    if args.owner:
        workstreams = [ws for ws in workstreams if ws.owner == args.owner]

    if console.json_mode:
        console.json([ws.as_dict() for ws in workstreams])
        return int(ExitCode.OK)
    if not workstreams:
        console.state("info", "no workstreams match")
        return int(ExitCode.OK)
    console.title(f"{len(workstreams)} workstreams")
    console.out()
    for ws in workstreams:
        console.out(
            f"  {ws.number}  {ws.title:<38}{ws.status:<10}{ws.owner:<22}{ws.done}/{ws.total}"
        )
    return int(ExitCode.OK)


def _show(args: argparse.Namespace, console: Console, repo) -> int:
    workstream = ws_mod.find_workstream(repo.work_dir, args.id)
    if console.json_mode:
        console.json(workstream.as_dict(with_tasks=args.tasks))
        return int(ExitCode.OK)
    console.title(f"{workstream.number} · {workstream.title}")
    console.out()
    console.field("status", workstream.status)
    console.field("owner", workstream.owner)
    console.field("kind", str(workstream.meta.get("kind", "—")))
    console.field("audience", str(workstream.meta.get("audience", "—")))
    console.field("progress", f"{workstream.done}/{workstream.total} tasks ({workstream.percent}%)")
    console.field("path", repo.relative(workstream.path))
    if args.tasks and workstream.tasks:
        console.out()
        for task in workstream.tasks:
            state = "ok" if task.done else ("fail" if task.state == "blocked" else "info")
            console.state(state, f"{task.id:<6}{task.title:<44}{task.owner}", task.state)
    return int(ExitCode.OK)


def _sync(args: argparse.Namespace, console: Console, repo) -> int:
    written = ws_mod.sync(repo.work_dir)
    if console.json_mode:
        console.json({"written": [repo.relative(path) for path in written]})
        return int(ExitCode.OK)
    for path in written:
        console.state("ok", f"regenerated {repo.relative(path)}")
    return int(ExitCode.OK)


def _validate(args: argparse.Namespace, console: Console, repo) -> int:
    violations = ws_mod.validate_workstreams(repo.work_dir, repo.schema_dir)
    if console.json_mode:
        console.json({"ok": not violations, "violations": [v.as_dict() for v in violations]})
        return int(ExitCode.OK if not violations else ExitCode.VIOLATIONS)
    if not violations:
        console.state("ok", "every workstream is shaped correctly")
        return int(ExitCode.OK)
    console.state("fail", f"{len(violations)} violations")
    for violation in violations:
        console.bullet(str(violation))
    return int(ExitCode.VIOLATIONS)
