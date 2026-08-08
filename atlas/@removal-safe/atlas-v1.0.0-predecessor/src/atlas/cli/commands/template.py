"""``atlas template``: the starter scaffold and its mirror."""

from __future__ import annotations

import argparse
import typing as t

from ...core import template as template_mod
from ...errors import ExitCode
from ...terminal import Style

if t.TYPE_CHECKING:  # pragma: no cover
    from .. import Context


def register(subparsers: t.Any, add_global_flags: t.Callable[..., None]) -> None:
    parser = subparsers.add_parser(
        "template",
        help="inspect and refresh the starter template",
        description=(
            "The template is what `atlas init` copies. A few of its files are copies of things "
            "this repository already owns, and copies drift, so the direction of flow is fixed "
            "and checked in CI: edit the original, then run the sync. A hand-edited copy fails "
            "the build instead of surfacing months later in someone else's project."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_global_flags(parser)
    sub = parser.add_subparsers(dest="subcommand", metavar="<subcommand>")

    check = sub.add_parser(
        "check",
        help="fail if the template has drifted from its sources",
        description="Assert that every mirrored file matches its canonical source. Used in CI.",
    )
    add_global_flags(check)
    check.set_defaults(handler=cmd_check)

    sync = sub.add_parser(
        "sync",
        help="rewrite the mirror from its canonical sources",
        description="Copy canonical sources into template/. The only direction of flow.",
    )
    add_global_flags(sync)
    sync.set_defaults(handler=cmd_sync)

    listing = sub.add_parser(
        "list",
        help="list the mirrored files",
        description="List each mirrored file and whether it is currently in sync.",
    )
    add_global_flags(listing)
    listing.set_defaults(handler=cmd_list)

    parser.set_defaults(handler=lambda ctx: _default(ctx, parser))


def _default(ctx: Context, parser: argparse.ArgumentParser) -> ExitCode:
    if not getattr(ctx.args, "subcommand", None):
        return cmd_list(ctx)
    return ExitCode.USAGE  # pragma: no cover


def cmd_check(ctx: Context) -> ExitCode:
    violations = template_mod.check_mirror(ctx.repo)
    ctx.console.emit({"ok": not violations, "violations": [v.as_dict() for v in violations]})
    if not violations:
        pairs = template_mod.mirror_pairs(ctx.repo)
        ctx.console.status("ok", f"template mirror current ({len(pairs)} files)")
        return ExitCode.OK
    ctx.console.status("fail", f"{len(violations)} file(s) have drifted")
    for violation in violations:
        ctx.console.write(f"  {ctx.console.paint(violation.render(), Style.RED)}")
    ctx.console.hint("Run `atlas template sync`.")
    return ExitCode.FAILURE


def cmd_sync(ctx: Context) -> ExitCode:
    changed = template_mod.sync_mirror(ctx.repo)
    ctx.console.emit({"changed": changed})
    if changed:
        ctx.console.status("ok", f"{len(changed)} file(s) re-mirrored")
        for path in changed:
            ctx.console.detail(f"  {path}")
    else:
        ctx.console.status("ok", "template mirror already current")
    return ExitCode.OK


def cmd_list(ctx: Context) -> ExitCode:
    pairs = template_mod.mirror_pairs(ctx.repo)
    ctx.console.emit(
        {
            "mirrors": [
                {"source": ctx.repo.rel(p.source), "destination": ctx.repo.rel(p.destination),
                 "current": p.current()}
                for p in pairs
            ]
        }
    )
    ctx.console.title("Template mirrors", f"{len(pairs)} files, canonical source → template/")
    ctx.console.table(
        ["SOURCE", "DESTINATION", "STATE"],
        [
            (ctx.repo.rel(p.source), ctx.repo.rel(p.destination), "current" if p.current() else "stale")
            for p in pairs
        ],
    )
    return ExitCode.OK
