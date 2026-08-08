"""``atlas library``: the shared-asset library."""

from __future__ import annotations

import argparse
import typing as t

from ...core import library as library_mod
from ...errors import ExitCode
from ...terminal import Style

if t.TYPE_CHECKING:  # pragma: no cover
    from .. import Context


def register(subparsers: t.Any, add_global_flags: t.Callable[..., None]) -> None:
    parser = subparsers.add_parser(
        "library",
        help="inspect the shared prompts, icons, typefaces, and media",
        description=(
            "The library holds things written once and used many times, in four kinds: "
            "prompts, icons, typefaces, and media. That list is closed. Adding a fifth kind "
            "means amending the specification, which is the difference between a library and "
            "a second downloads folder."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_global_flags(parser)
    sub = parser.add_subparsers(dest="subcommand", metavar="<subcommand>")

    listing = sub.add_parser(
        "list",
        help="list asset classes and their contents",
        description="List each asset class, what it holds, and how many assets it carries.",
    )
    listing.add_argument("--class", dest="asset_class",
                         choices=sorted(library_mod.CLASSES),
                         help="show the assets in one class")
    add_global_flags(listing)
    listing.set_defaults(handler=cmd_list)

    check = sub.add_parser(
        "check",
        help="verify indexes and files agree",
        description=(
            "Verify that every index entry has a file and every file has an index entry, that "
            "ids are unique, and that derived or foreign assets declare their source and license."
        ),
    )
    add_global_flags(check)
    check.set_defaults(handler=cmd_check)

    parser.set_defaults(handler=lambda ctx: _default(ctx, parser))


def _default(ctx: Context, parser: argparse.ArgumentParser) -> ExitCode:
    if not getattr(ctx.args, "subcommand", None):
        return cmd_list(ctx)
    return ExitCode.USAGE  # pragma: no cover


def cmd_list(ctx: Context) -> ExitCode:
    classes = library_mod.load(ctx.repo)
    wanted = getattr(ctx.args, "asset_class", None)
    if wanted:
        classes = [c for c in classes if c.name == wanted]

    ctx.console.emit(
        {
            "classes": [
                {"name": c.name, "holds": c.holds, "present": c.present,
                 "assets": [a.as_dict() for a in c.assets]}
                for c in classes
            ]
        }
    )

    if wanted:
        target = classes[0]
        ctx.console.title(f"library/{target.name}", target.holds)
        if not target.assets:
            ctx.console.status("skip", "no assets yet")
            return ExitCode.OK
        ctx.console.table(
            ["ID", "FILE", "DESCRIPTION", "LICENCE"],
            [(a.id, a.file, a.description, a.license or "—") for a in target.assets],
        )
        return ExitCode.OK

    ctx.console.title("Library", "four asset classes; the set is closed")
    ctx.console.table(
        ["CLASS", "N", "HOLDS"],
        [
            (c.name, str(c.count) if c.present else "—", c.holds)
            for c in classes
        ],
        align=["l", "r", "l"],
    )
    return ExitCode.OK


def cmd_check(ctx: Context) -> ExitCode:
    from ...core import prompts as prompts_mod

    violations = library_mod.validate(ctx.repo)
    if (ctx.repo.prompts / "index.yaml").exists():
        violations += prompts_mod.validate(ctx.repo)

    ctx.console.emit(
        {"ok": not violations, "violations": [v.as_dict() for v in violations]}
    )
    if not violations:
        ctx.console.status("ok", "library indexes and files agree")
        return ExitCode.OK
    ctx.console.status("fail", f"{len(violations)} violation(s)")
    for violation in violations:
        ctx.console.write(f"  {ctx.console.paint(violation.render(), Style.RED)}")
    return ExitCode.FAILURE
