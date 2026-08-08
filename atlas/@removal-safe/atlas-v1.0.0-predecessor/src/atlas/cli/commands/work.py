"""``atlas work``: the WORKSTREAM system."""

from __future__ import annotations

import argparse
import typing as t

from ...core import workstream as ws
from ...errors import ExitCode
from ...terminal import Style

if t.TYPE_CHECKING:  # pragma: no cover
    from .. import Context


def register(subparsers: t.Any, add_global_flags: t.Callable[..., None]) -> None:
    parser = subparsers.add_parser(
        "work",
        help="plan, track, and verify initiatives",
        description=(
            "Every initiative lives in its own numbered folder with the same nine sections, "
            "one accountable owner, and a step where someone records how the result was "
            "checked. The Markdown is the original. The dashboard a person reads and the index "
            "an agent reads are both generated from the task tables, so progress is counted "
            "rather than claimed: a workstream cannot report itself further along than its "
            "own tasks say it is."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_global_flags(parser)
    sub = parser.add_subparsers(dest="subcommand", metavar="<subcommand>")

    new = sub.add_parser(
        "new",
        help="scaffold the next workstream",
        description="Scaffold the next numbered workstream from work/_template and re-sync.",
        epilog="atlas work new migrate-the-fleet --owner person:dana --title 'Migrate the fleet'",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    new.add_argument("slug", help="lowercase-hyphenated name, e.g. migrate-the-fleet")
    new.add_argument("--title", help="human title (default: the slug, de-hyphenated)")
    new.add_argument("--owner", default="person:unassigned",
                     help="accountable principal, e.g. person:dana or team:platform")
    new.add_argument("--summary", default="", help="one sentence on what this workstream is for")
    add_global_flags(new)
    new.set_defaults(handler=cmd_new)

    listing = sub.add_parser(
        "list",
        help="list workstreams",
        description="List workstreams with owner, status, and counted progress.",
        epilog="atlas work list --status blocked\natlas work list --owner person:dana --json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    listing.add_argument("--status", help="filter by status: " + ", ".join(ws.STATUS_ORDER))
    listing.add_argument("--owner", help="filter by owning principal")
    listing.add_argument("--archived", action="store_true", help="include archived workstreams")
    add_global_flags(listing)
    listing.set_defaults(handler=cmd_list)

    show = sub.add_parser(
        "show",
        help="show one workstream in detail",
        description="Show a workstream's manifest, task table, agents, and dependencies.",
        epilog="atlas work show 01\natlas work show harden-repository-baseline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    show.add_argument("id", help="workstream number or slug")
    show.add_argument("--tasks", action="store_true", help="show the full task table")
    add_global_flags(show)
    show.set_defaults(handler=cmd_show)

    sync = sub.add_parser(
        "sync",
        help="regenerate the dashboard and machine index",
        description=(
            "Recount progress from the task tables, write it back into each manifest, then "
            "regenerate work/index.yaml and work/README.md. Idempotent: reports what changed."
        ),
    )
    sync.add_argument("--check", action="store_true",
                      help="fail if anything would change, instead of writing (for CI)")
    add_global_flags(sync)
    sync.set_defaults(handler=cmd_sync)

    validate = sub.add_parser(
        "validate",
        help="check every workstream against the standard",
        description=(
            "Check every workstream: schema, skeleton completeness, id and slug agreement, "
            "task-table hygiene, evidence before done, the dependency graph, and whether the "
            "generated index is current."
        ),
    )
    add_global_flags(validate)
    validate.set_defaults(handler=cmd_validate)

    archive = sub.add_parser(
        "archive",
        help="move a finished workstream to work/archive/",
        description="Move a done or cancelled workstream into work/archive/ and re-sync.",
        epilog="atlas work archive 01",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    archive.add_argument("id", help="workstream number or slug")
    add_global_flags(archive)
    archive.set_defaults(handler=cmd_archive)

    parser.set_defaults(handler=lambda ctx: _default(ctx, parser))


def _default(ctx: Context, parser: argparse.ArgumentParser) -> ExitCode:
    if not getattr(ctx.args, "subcommand", None):
        parser.print_help()
        return ExitCode.OK
    return ExitCode.USAGE  # pragma: no cover - argparse routes to a handler


# ---------------------------------------------------------------------- new

def cmd_new(ctx: Context) -> ExitCode:
    created = ws.create(
        ctx.repo,
        ctx.args.slug,
        title=ctx.args.title,
        owner=ctx.args.owner,
        summary=ctx.args.summary,
    )
    count, changed = ws.sync(ctx.repo)
    ctx.console.emit({"created": created.rel, "id": created.id, "synced": count})
    ctx.console.status("ok", f"created {created.rel}")
    ctx.console.write()
    ctx.console.para("Next:")
    ctx.console.bullet(f"Write the plan: {created.rel}/01_plan/plan.md")
    ctx.console.bullet(f"List the tasks: {created.rel}/02_tasks/tasks.md")
    ctx.console.bullet("Re-sync when tasks change: atlas work sync")
    return ExitCode.OK


# --------------------------------------------------------------------- list

def cmd_list(ctx: Context) -> ExitCode:
    workstreams = ws.load_all(ctx.repo)
    if not ctx.args.archived:
        workstreams = [w for w in workstreams if not w.archived]
    if ctx.args.status:
        workstreams = [w for w in workstreams if w.status == ctx.args.status]
    if ctx.args.owner:
        workstreams = [w for w in workstreams if w.owner == ctx.args.owner]

    ctx.console.emit({"workstreams": [w.as_dict() for w in workstreams]})

    if not workstreams:
        ctx.console.title("Workstreams", "none matching")
        ctx.console.para("No workstreams match. Open one with `atlas work new <slug>`.")
        return ExitCode.OK

    live = [w for w in workstreams if not w.archived]
    counts = " · ".join(
        f"{status}: {n}"
        for status in ws.STATUS_ORDER
        if (n := sum(1 for w in live if w.status == status))
    )
    ctx.console.title("Workstreams", counts or f"{len(workstreams)} total")
    order = {status: i for i, status in enumerate(ws.STATUS_ORDER)}
    rows = [
        (
            w.id,
            w.title + (" (archived)" if w.archived else ""),
            w.status,
            w.owner,
            ctx.console.progress(w.done, w.total, width=12),
        )
        for w in sorted(workstreams, key=lambda w: (order.get(w.status, 99), w.id))
    ]
    ctx.console.table(["#", "WORKSTREAM", "STATUS", "OWNER", "PROGRESS"], rows)
    return ExitCode.OK


# --------------------------------------------------------------------- show

def cmd_show(ctx: Context) -> ExitCode:
    workstream = ws.find(ctx.repo, ctx.args.id)
    payload = workstream.as_dict()
    payload["tasks"] = [task.as_dict() for task in workstream.tasks]
    ctx.console.emit(payload)

    ctx.console.title(f"{workstream.id}: {workstream.title}", workstream.summary)
    ctx.console.definitions(
        [
            ("status", workstream.status),
            ("owner", workstream.owner),
            ("target", workstream.target or "—"),
            ("progress", ctx.console.progress(workstream.done, workstream.total)),
            ("path", workstream.rel),
            ("depends on", ", ".join(workstream.depends_on) or "—"),
            ("agents", ", ".join(a.get("id", "?") for a in workstream.agents) or "—"),
        ]
    )

    blocked = workstream.blocked_tasks
    if blocked:
        ctx.console.write()
        ctx.console.status("warn", f"{len(blocked)} blocked task(s)")
        for task in blocked:
            ctx.console.bullet(f"{task.id} {task.title}: {task.owner}")

    if ctx.args.tasks and workstream.tasks:
        ctx.console.write()
        ctx.console.rule("tasks")
        ctx.console.table(
            ["ID", "TASK", "OWNER", "STATUS", "EVIDENCE"],
            [(t.id, t.title, t.owner, t.status, t.evidence) for t in workstream.tasks],
        )
    elif workstream.tasks:
        ctx.console.write()
        ctx.console.detail("Run with --tasks for the full task table.")
    return ExitCode.OK


# --------------------------------------------------------------------- sync

def cmd_sync(ctx: Context) -> ExitCode:
    if ctx.args.check:
        violations = [v for v in ws.validate(ctx.repo) if v.rule == "W-11"]
        ctx.console.emit({"current": not violations})
        if violations:
            ctx.console.status("fail", "generated artifacts are stale")
            ctx.console.hint("Run `atlas work sync`.")
            return ExitCode.FAILURE
        ctx.console.status("ok", "dashboard and index are current")
        return ExitCode.OK

    count, changed = ws.sync(ctx.repo)
    ctx.console.emit({"workstreams": count, "changed": changed})
    if changed:
        ctx.console.status("ok", f"synced {count} workstream(s)", f"{len(changed)} file(s) updated")
        for path in changed:
            ctx.console.detail(f"  {path}")
    else:
        ctx.console.status("ok", f"{count} workstream(s) already current")
    return ExitCode.OK


# ----------------------------------------------------------------- validate

def cmd_validate(ctx: Context) -> ExitCode:
    violations = ws.validate(ctx.repo)
    count = len(ws.load_all(ctx.repo))
    ctx.console.emit(
        {"ok": not violations, "workstreams": count,
         "violations": [v.as_dict() for v in violations]}
    )
    if not violations:
        ctx.console.status("ok", f"{count} workstream(s) valid")
        return ExitCode.OK
    ctx.console.status("fail", f"{len(violations)} violation(s) across {count} workstream(s)")
    for violation in violations:
        ctx.console.write(f"  {ctx.console.paint(violation.render(), Style.RED)}")
    return ExitCode.FAILURE


# ------------------------------------------------------------------ archive

def cmd_archive(ctx: Context) -> ExitCode:
    archived = ws.archive(ctx.repo, ctx.args.id)
    ws.sync(ctx.repo)
    ctx.console.emit({"archived": archived.rel})
    ctx.console.status("ok", f"archived {archived.name}", archived.rel)
    return ExitCode.OK
