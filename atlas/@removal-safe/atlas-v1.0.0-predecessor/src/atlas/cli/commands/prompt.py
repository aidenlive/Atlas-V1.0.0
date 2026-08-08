"""``atlas prompt``: the reusable request library."""

from __future__ import annotations

import argparse
import typing as t

from ...core import prompts as prompts_mod
from ...errors import ExitCode
from ...terminal import Style

if t.TYPE_CHECKING:  # pragma: no cover
    from .. import Context


def register(subparsers: t.Any, add_global_flags: t.Callable[..., None]) -> None:
    parser = subparsers.add_parser(
        "prompt",
        help="find a written-once request to paste or hand over",
        description=(
            "Browse the prompt library. Each entry is one to three sentences, asks for exactly "
            "one thing, and names no particular tool, so it works in any AI assistant or as a "
            "request to a colleague. Anything that deletes or overwrites is worded to propose "
            "a plan and wait."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_global_flags(parser)
    sub = parser.add_subparsers(dest="subcommand", metavar="<subcommand>")

    listing = sub.add_parser(
        "list",
        help="list prompts, optionally by category",
        description="List prompts with their objective, grouped by lifecycle category.",
        epilog="atlas prompt list\natlas prompt list --category releases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    listing.add_argument("--category", help="only this category")
    add_global_flags(listing)
    listing.set_defaults(handler=cmd_list)

    categories = sub.add_parser(
        "categories",
        help="list the lifecycle categories",
        description="List the categories and how many prompts each holds.",
    )
    add_global_flags(categories)
    categories.set_defaults(handler=cmd_categories)

    show = sub.add_parser(
        "show",
        help="print one prompt, ready to paste",
        description=(
            "Print a prompt's text and nothing else, so it pipes cleanly into a clipboard "
            "command or another tool."
        ),
        epilog="atlas prompt show cut-release\natlas prompt show releases/cut-release | pbcopy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    show.add_argument("id", help="prompt id, filename stem, or category/id")
    show.add_argument("--with-context", action="store_true",
                      help="include the objective and category alongside the text")
    add_global_flags(show)
    show.set_defaults(handler=cmd_show)

    search = sub.add_parser(
        "search",
        help="search prompts by term",
        description="Substring search across prompt ids, objectives, categories, and bodies.",
        epilog="atlas prompt search release\natlas prompt search 'branch protection'",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    search.add_argument("term", help="what to look for")
    add_global_flags(search)
    search.set_defaults(handler=cmd_search)

    parser.set_defaults(handler=lambda ctx: _default(ctx, parser))


def _default(ctx: Context, parser: argparse.ArgumentParser) -> ExitCode:
    if not getattr(ctx.args, "subcommand", None):
        return cmd_categories(ctx)
    return ExitCode.USAGE  # pragma: no cover


def cmd_list(ctx: Context) -> ExitCode:
    catalog = prompts_mod.load(ctx.repo)
    categories = (
        [catalog.category(ctx.args.category)] if ctx.args.category else catalog.categories
    )
    ctx.console.emit(
        {"prompts": [p.as_dict() for c in categories for p in c.prompts]}
    )
    total = sum(len(c.prompts) for c in categories)
    ctx.console.title("Prompts", f"{total} across {len(categories)} categor{'y' if len(categories)==1 else 'ies'}")
    for category in categories:
        ctx.console.write(ctx.console.paint(f"{category.name}", Style.BOLD))
        ctx.console.table(["ID", "OBJECTIVE"], [(p.id, p.objective) for p in category.prompts])
        ctx.console.write()
    ctx.console.detail("Print one: atlas prompt show <id>")
    return ExitCode.OK


def cmd_categories(ctx: Context) -> ExitCode:
    catalog = prompts_mod.load(ctx.repo)
    ctx.console.emit(
        {
            "categories": [
                {"name": c.name, "description": c.description, "prompts": len(c.prompts)}
                for c in catalog.categories
            ]
        }
    )
    ctx.console.title("Prompt categories",
                      f"{len(catalog.prompts)} prompts across {len(catalog.categories)} categories")
    ctx.console.table(
        ["CATEGORY", "N", "COVERS"],
        [(c.name, str(len(c.prompts)), c.description) for c in catalog.categories],
        align=["l", "r", "l"],
    )
    return ExitCode.OK


def cmd_show(ctx: Context) -> ExitCode:
    catalog = prompts_mod.load(ctx.repo)
    prompt = catalog.get(ctx.args.id)
    ctx.console.emit({**prompt.as_dict(), "text": prompt.text})
    if ctx.console.json_mode:
        return ExitCode.OK
    if ctx.args.with_context:
        ctx.console.title(prompt.id, f"{prompt.category} · {prompt.objective}")
    # Printed bare so it pipes cleanly; --quiet must not suppress the payload.
    print(prompt.text, file=ctx.console.stream)
    return ExitCode.OK


def cmd_search(ctx: Context) -> ExitCode:
    catalog = prompts_mod.load(ctx.repo)
    hits = prompts_mod.search(catalog, ctx.args.term)
    ctx.console.emit({"term": ctx.args.term, "matches": [p.as_dict() for p in hits]})
    if not hits:
        ctx.console.status("skip", f"no prompts match {ctx.args.term!r}")
        ctx.console.detail("List the categories: atlas prompt categories")
        return ExitCode.OK
    ctx.console.title(f"Prompts matching {ctx.args.term!r}", f"{len(hits)} match(es)")
    ctx.console.table(
        ["ID", "CATEGORY", "OBJECTIVE"],
        [(p.id, p.category, p.objective) for p in hits],
    )
    return ExitCode.OK
