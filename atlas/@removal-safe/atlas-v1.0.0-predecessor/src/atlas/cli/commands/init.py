"""``atlas init``: scaffold a compliant repository."""

from __future__ import annotations

import argparse
import pathlib
import typing as t

from ...core import template
from ...errors import ExitCode
from ...terminal import Style

if t.TYPE_CHECKING:  # pragma: no cover
    from .. import Context


def register(subparsers: t.Any, add_global_flags: t.Callable[..., None]) -> None:
    parser = subparsers.add_parser(
        "init",
        help="start a new repository that already passes",
        description=(
            "Copy the starter template into a new directory, filling in the project name, the "
            "date, and the owner. What you get passes `atlas check` on the first run and has "
            "the work system ready to use. Any placeholder the scaffold could not fill is "
            "listed at the end, so a template never ships with `{{PROJECT_NAME}}` still in it."
        ),
        epilog=(
            "atlas init payments-api ../payments-api\n"
            "atlas init payments-api ../payments-api --owner team:platform"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("name", help="lowercase-hyphenated project name, e.g. payments-api")
    parser.add_argument("destination", nargs="?", help="where to create it (default: ./<name>)")
    parser.add_argument("--owner", default="person:you",
                        help="accountable principal for the new repository")
    parser.add_argument("--description", default="", help="one-line description for project.yaml")
    add_global_flags(parser)
    parser.set_defaults(handler=run)


def run(ctx: Context) -> ExitCode:
    destination = pathlib.Path(ctx.args.destination or ctx.args.name).expanduser().resolve()
    written = template.scaffold(
        ctx.repo,
        ctx.args.name,
        destination,
        owner=ctx.args.owner,
        description=ctx.args.description,
    )
    remaining = template.remaining_placeholders(destination)

    ctx.console.emit(
        {
            "name": ctx.args.name,
            "destination": str(destination),
            "files": len(written),
            "placeholders": remaining,
        }
    )
    ctx.console.title(f"Scaffolded {ctx.args.name}", str(destination))
    ctx.console.status("ok", f"{len(written)} files written")
    ctx.console.write()
    ctx.console.para("Next:")
    ctx.console.bullet(f"cd {destination}")
    ctx.console.bullet("Edit project.yaml: type, owner, visibility, description")
    ctx.console.bullet("Replace assets/banner*.svg before going public")
    ctx.console.bullet("atlas check")
    ctx.console.bullet("git init && git add -A && git commit -m 'chore: initial commit'")

    if remaining:
        ctx.console.write()
        ctx.console.status("warn", f"{len(remaining)} placeholder(s) still to fill")
        for token, files in remaining.items():
            shown = ", ".join(files[:3]) + (f" (+{len(files) - 3} more)" if len(files) > 3 else "")
            ctx.console.write(f"    {ctx.console.paint(token, Style.YELLOW)}  {shown}")
    return ExitCode.OK
