"""Start a repository that already passes.

Scaffolding that produces a failing repository teaches the wrong lesson on day
one, so ``atlas init`` copies a starter that passes every gate, then tells you
to run ``atlas check`` and see it pass.
"""

from __future__ import annotations

import argparse
import pathlib

from ...core import compliance, template as template_mod
from ...errors import ExitCode, NotARepositoryError
from ...paths import Repository, discover
from ...terminal import Console

SUMMARY = "start a new repository that already passes"


def configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("name", help="repository name, lower-case-with-hyphens")
    parser.add_argument("path", nargs="?", help="where to create it (default: ./NAME)")
    parser.add_argument("--owner", default="person:you", help="who owns it (default: person:you)")
    parser.add_argument("--description", default="", help="one sentence for the manifest")
    parser.add_argument("--template", metavar="DIR", help="use this template instead of the built-in one")
    parser.add_argument("--force", action="store_true", help="write into a non-empty directory")


def run(args: argparse.Namespace, console: Console) -> int:
    try:
        source_repo: Repository | None = discover(args.directory)
    except NotARepositoryError:
        source_repo = None

    template = (
        pathlib.Path(args.template)
        if args.template
        else template_mod.template_root(source_repo.root if source_repo else None)
    )
    destination = pathlib.Path(args.path or args.name).resolve()

    console.step(f"copying {template} → {destination}")
    result = template_mod.scaffold(
        template,
        destination,
        name=args.name,
        owner=args.owner,
        description=args.description,
        force=args.force,
    )

    report = compliance.run(Repository(root=destination))

    if console.json_mode:
        console.json({**result.as_dict(), "ok": report.ok, "check": report.as_dict()["summary"]})
        return int(ExitCode.OK if report.ok else ExitCode.VIOLATIONS)

    console.title(f"created {args.name}")
    console.out()
    console.field("path", str(destination))
    console.field("files", str(len(result.files)))
    console.field("owner", args.owner)
    console.out()
    console.state(
        "ok" if report.ok else "fail",
        f"{report.passed} gates passed, {report.failed} failed",
    )
    console.out()
    console.note("next:")
    console.note(f"  cd {destination}")
    console.note("  atlas check")
    console.note("  atlas work new first-piece --owner person:you")
    return int(ExitCode.OK if report.ok else ExitCode.VIOLATIONS)
