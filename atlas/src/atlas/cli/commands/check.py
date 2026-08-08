"""Check this repository against the standard.

Runs every compliance gate and prints what is missing. This is the command CI
runs, and the one that settles the argument about whether something is ready:
the answer is a list of gates and the violations behind them, not an opinion.
"""

from __future__ import annotations

import argparse

from ...core import compliance
from ...errors import ExitCode
from ...paths import discover
from ...terminal import Console

SUMMARY = "check this repository against the standard"


def configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--only", metavar="CHECK", action="append",
        help="run only this gate (repeatable); see --list",
    )
    parser.add_argument("--list", action="store_true", help="list the gates and exit")


def run(args: argparse.Namespace, console: Console) -> int:
    if args.list:
        return _list(console)

    repo = discover(args.directory)
    console.step(f"checking {repo.root}")
    report = compliance.run(repo, only=args.only)

    if console.json_mode:
        console.json(report.as_dict())
        return int(ExitCode.OK if report.ok else ExitCode.VIOLATIONS)

    console.title(f"atlas check · {repo.root.name}")
    console.out()
    for result in report.results:
        detail = result.skipped or result.check.rule
        console.state(result.state, result.check.summary, detail)
        for violation in result.violations:
            location = f"{violation.location}: " if violation.location else ""
            console.bullet(f"{location}{violation.message}")
            if violation.hint and console.verbose:
                console.bullet(f"↳ {violation.hint}", indent=8)
    console.out()
    if report.ok:
        console.state(
            "ok",
            f"{report.passed} gate" + ("" if report.passed == 1 else "s")
            + f" passed, {report.skipped} skipped",
        )
        return int(ExitCode.OK)
    console.state(
        "fail",
        f"{report.failed} of {len(report.results)} gates failed",
        f"{len(report.violations)} violation" + ("" if len(report.violations) == 1 else "s"),
    )
    console.note("run with -v for the remedy on each violation")
    return int(ExitCode.VIOLATIONS)


def _list(console: Console) -> int:
    checks = list(compliance.CHECKS.values())
    if console.json_mode:
        console.json(
            [{"id": c.id, "summary": c.summary, "rule": c.rule} for c in checks]
        )
        return int(ExitCode.OK)
    console.title(f"{len(checks)} gate" + ("" if len(checks) == 1 else "s"))
    console.out()
    for check in checks:
        console.out(f"  {check.id:<22}{check.summary}")
        console.note(f"  {'':<22}{check.rule}")
    return int(ExitCode.OK)
