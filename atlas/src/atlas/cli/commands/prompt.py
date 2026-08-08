"""Find a written-once request to paste or hand over.

Prompts are for the work nobody should re-derive: the same request, worded the
same way, every time. Pipe one straight to the clipboard, or read it and rewrite
it for the job in front of you.
"""

from __future__ import annotations

import argparse

from ...core import prompts as prompts_mod
from ...errors import ExitCode, UsageError
from ...paths import discover
from ...terminal import Console

SUMMARY = "find a written-once request to paste or hand over"


def configure(parser: argparse.ArgumentParser) -> None:
    subparsers = parser.add_subparsers(dest="subcommand", metavar="<subcommand>")

    listing = subparsers.add_parser("list", help="list prompts, or the stages")
    listing.add_argument("--stage", help="only this stage")
    listing.add_argument("--stages", action="store_true", help="list the stages instead")

    search = subparsers.add_parser("search", help="search prompts by word")
    search.add_argument("query", help="a word to look for")
    search.add_argument("--stage", help="only this stage")

    show = subparsers.add_parser("show", help="print one prompt, and nothing else")
    show.add_argument("slug", help="prompt slug, e.g. write-guide")


def run(args: argparse.Namespace, console: Console) -> int:
    repo = discover(args.directory)
    subcommand = getattr(args, "subcommand", None) or "list"
    if subcommand == "list":
        return _list(args, console, repo)
    if subcommand == "search":
        return _search(args, console, repo)
    if subcommand == "show":
        return _show(args, console, repo)
    raise UsageError(f"unknown subcommand: {subcommand}")


def _print_table(console: Console, prompts) -> None:
    stage = None
    for prompt in prompts:
        if prompt.stage != stage:
            stage = prompt.stage
            console.out()
            console.title(f"  {stage}")
        console.out(f"    {prompt.slug:<28}{prompt.summary}")


def _list(args: argparse.Namespace, console: Console, repo) -> int:
    if getattr(args, "stages", False):
        stages = prompts_mod.stages(repo.prompts_dir)
        if console.json_mode:
            console.json(stages)
            return int(ExitCode.OK)
        console.title(f"{len(stages)} stages")
        for stage in stages:
            console.out(f"  {stage}")
        return int(ExitCode.OK)

    prompts = prompts_mod.search_prompts(repo.prompts_dir, "", stage=args.stage)
    if console.json_mode:
        console.json([prompt.as_dict() for prompt in prompts])
        return int(ExitCode.OK)
    console.title(f"{len(prompts)} prompts")
    _print_table(console, prompts)
    return int(ExitCode.OK)


def _search(args: argparse.Namespace, console: Console, repo) -> int:
    prompts = prompts_mod.search_prompts(repo.prompts_dir, args.query, stage=args.stage)
    if console.json_mode:
        console.json([prompt.as_dict() for prompt in prompts])
        return int(ExitCode.OK if prompts else ExitCode.NOT_FOUND)
    if not prompts:
        console.state("info", f"nothing matches {args.query!r}")
        return int(ExitCode.NOT_FOUND)
    console.title(f"{len(prompts)} prompts match {args.query!r}")
    _print_table(console, prompts)
    return int(ExitCode.OK)


def _show(args: argparse.Namespace, console: Console, repo) -> int:
    prompt = prompts_mod.find_prompt(repo.prompts_dir, args.slug)
    if console.json_mode:
        console.json(prompt.as_dict(with_text=True))
        return int(ExitCode.OK)
    # Deliberately unadorned: `atlas prompt show x | pbcopy` should copy the
    # prompt, not a heading and a box.
    print(prompt.text)
    return int(ExitCode.OK)
