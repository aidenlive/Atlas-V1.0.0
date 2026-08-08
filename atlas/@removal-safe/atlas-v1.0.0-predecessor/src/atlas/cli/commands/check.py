"""``atlas check``. Run every compliance gate."""

from __future__ import annotations

import argparse
import typing as t

from ...core import compliance
from ...errors import ExitCode
from ...terminal import Style

if t.TYPE_CHECKING:  # pragma: no cover
    from .. import Context


def register(subparsers: t.Any, add_global_flags: t.Callable[..., None]) -> None:
    parser = subparsers.add_parser(
        "check",
        help="check this repository against the standard",
        description=(
            "Check everything the standard requires and print what is missing. Twelve checks "
            "run by default, covering the repository root, the agent guide, the manifest, the "
            "README, the forge metadata, the workstreams, the library, and the starter "
            "template. A check that does not apply here is reported as skipped, with the "
            "reason, so a standard nobody has adopted never looks like a passing one."
        ),
        epilog=(
            "atlas check\n"
            "atlas check --only root-closed-set,manifest\n"
            "atlas check --list\n"
            "atlas check --json | jq '.checks[] | select(.state==\"fail\")'"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--only", metavar="IDS",
        help="run only these checks (comma-separated); see --list for the ids",
    )
    parser.add_argument(
        "--list", action="store_true", dest="list_checks",
        help="list the available checks and exit",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="count skipped checks as failures, for a repository expected to adopt everything",
    )
    add_global_flags(parser)
    parser.set_defaults(handler=run)


def run(ctx: Context) -> ExitCode:
    console = ctx.console

    if ctx.args.list_checks:
        console.emit(
            {
                "checks": [
                    {"id": c.id, "summary": c.summary, "rule": c.rule} for c in compliance.CHECKS
                ]
            }
        )
        console.title("Compliance gates", f"{len(compliance.CHECKS)} registered")
        console.table(
            ["ID", "ENFORCES", "RULE"],
            [(c.id, c.summary, c.rule) for c in compliance.CHECKS],
        )
        return ExitCode.OK

    only = [part.strip() for part in ctx.args.only.split(",")] if ctx.args.only else None
    report = compliance.run(ctx.repo, only=only)
    console.emit(report.as_dict())

    console.title(f"Checking {ctx.repo.root.name}", str(ctx.repo.root))
    for result in report.results:
        detail = result.skipped or ""
        console.status(result.state, result.check.summary, detail)
        for violation in result.violations:
            console.write(f"    {console.paint(violation.render(), Style.RED)}")

    console.write()
    console.rule()
    parts = [
        console.paint(f"{report.passed} passed", Style.GREEN),
        console.paint(f"{report.failed} failed", Style.RED) if report.failed else "0 failed",
    ]
    if report.skipped:
        parts.append(console.paint(f"{report.skipped} skipped", Style.GREY))
    console.write(" · ".join(parts))

    if report.ok and ctx.args.strict and report.skipped:
        console.write()
        console.status("fail", "--strict: skipped gates count as failures")
        return ExitCode.FAILURE

    if report.ok:
        console.write()
        console.status("ok", console.paint("COMPLIANT", Style.BOLD, Style.GREEN))
        return ExitCode.OK

    console.write()
    console.status("fail", console.paint("NON-COMPLIANT", Style.BOLD, Style.RED),
                   f"{len(report.violations)} violation(s)")
    console.write()
    console.para("Fix the violations above, then re-run. To work one gate at a time:")
    console.write(f"  {console.paint('atlas check --only <id>', Style.CYAN)}")
    return ExitCode.FAILURE
