"""``atlas spec``. Read the specification suite."""

from __future__ import annotations

import argparse
import typing as t

from ...core import specs as specs_mod
from ...errors import ExitCode

if t.TYPE_CHECKING:  # pragma: no cover
    from .. import Context


def register(subparsers: t.Any, add_global_flags: t.Callable[..., None]) -> None:
    parser = subparsers.add_parser(
        "spec",
        help="read the standards and cite their rules",
        description=(
            "Read the standards from the terminal. Each one opens with machine-readable "
            "metadata giving its id, version, status, rule prefixes, and companions, so a tool "
            "can discover what the suite covers without reading the prose."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_global_flags(parser)
    sub = parser.add_subparsers(dest="subcommand", metavar="<subcommand>")

    listing = sub.add_parser(
        "list",
        help="list the standards in reading order",
        description="List every standard with the question it answers, its version, and status.",
    )
    add_global_flags(listing)
    listing.set_defaults(handler=cmd_list)

    show = sub.add_parser(
        "show",
        help="print one standard",
        description="Print a standard's prose, or just its metadata or rule identifiers.",
        epilog=(
            "atlas spec show workstream\n"
            "atlas spec show WORKSTREAM --rules\n"
            "atlas spec show project --meta"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    show.add_argument("name", help="standard id, filename stem, or title")
    show.add_argument("--meta", action="store_true", help="show only the front matter")
    show.add_argument("--rules", action="store_true",
                      help="show only the rule identifiers this standard defines")
    add_global_flags(show)
    show.set_defaults(handler=cmd_show)

    rules = sub.add_parser(
        "rules",
        help="list every rule identifier in the suite",
        description=(
            "List every rule identifier across the suite, with the standard that owns it. "
            "Use these when citing a rule in a review or a waiver."
        ),
    )
    rules.add_argument("--prefix", help="only rules beginning with this prefix, e.g. W-")
    add_global_flags(rules)
    rules.set_defaults(handler=cmd_rules)

    parser.set_defaults(handler=lambda ctx: _default(ctx, parser))


def _default(ctx: Context, parser: argparse.ArgumentParser) -> ExitCode:
    if not getattr(ctx.args, "subcommand", None):
        return cmd_list(ctx)
    return ExitCode.USAGE  # pragma: no cover


def cmd_list(ctx: Context) -> ExitCode:
    specs = specs_mod.load_specs(ctx.repo.spec)
    ctx.console.emit({"specs": [s.summary() for s in specs]})
    if not specs:
        ctx.console.status("skip", "no specifications in this repository")
        return ExitCode.OK
    ctx.console.title("Standards", f"{len(specs)} specifications, in reading order")
    ctx.console.table(
        ["#", "STANDARD", "ANSWERS", "VER", "STATUS"],
        [(f"{s.order:02d}", s.title, s.question, s.version, s.status) for s in specs],
    )
    ctx.console.write()
    ctx.console.detail("Read one: atlas spec show <name>")
    return ExitCode.OK


def cmd_show(ctx: Context) -> ExitCode:
    spec = specs_mod.find_spec(ctx.repo.spec, ctx.args.name)

    if ctx.args.rules:
        rules = spec.rule_ids()
        ctx.console.emit({"id": spec.id, "rules": rules})
        ctx.console.title(f"{spec.title} rules", f"{len(rules)} identifiers")
        for rule in rules:
            ctx.console.write(f"  {rule}")
        return ExitCode.OK

    if ctx.args.meta:
        ctx.console.emit(spec.summary())
        ctx.console.title(spec.title, spec.tagline)
        ctx.console.definitions(
            [
                ("id", spec.id),
                ("question", spec.question),
                ("version", spec.version),
                ("status", spec.status),
                ("order", str(spec.order)),
                ("prefixes", ", ".join(spec.prefixes) or "—"),
                ("companions", ", ".join(spec.companions) or "—"),
                ("path", ctx.repo.rel(spec.path)),
            ]
        )
        return ExitCode.OK

    ctx.console.emit({**spec.summary(), "body": spec.body})
    if not ctx.console.json_mode:
        print(spec.body, file=ctx.console.stream)
    return ExitCode.OK


def cmd_rules(ctx: Context) -> ExitCode:
    specs = specs_mod.load_specs(ctx.repo.spec)
    rows: list[tuple[str, str]] = []
    for spec in specs:
        for rule in spec.rule_ids():
            if ctx.args.prefix and not rule.startswith(ctx.args.prefix):
                continue
            rows.append((rule, spec.title))
    ctx.console.emit({"rules": [{"id": r, "standard": s} for r, s in rows]})
    if not rows:
        ctx.console.status("skip", "no rules match")
        return ExitCode.OK
    ctx.console.title("Rule identifiers", f"{len(rows)} across {len(specs)} standards")
    ctx.console.table(["RULE", "STANDARD"], rows)
    return ExitCode.OK
