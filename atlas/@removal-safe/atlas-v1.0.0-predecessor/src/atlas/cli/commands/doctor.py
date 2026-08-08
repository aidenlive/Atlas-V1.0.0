"""``atlas doctor``: diagnose the environment and the repository."""

from __future__ import annotations

import dataclasses
import importlib.util
import shutil
import subprocess
import sys
import typing as t

from ... import __version__
from ...core import compliance
from ...errors import ExitCode
from ...paths import NoRepositoryError, find_repository
from ...terminal import Style

if t.TYPE_CHECKING:  # pragma: no cover
    from .. import Context

MIN_PYTHON = (3, 10)


@dataclasses.dataclass
class Finding:
    state: str          # ok | warn | fail | skip
    label: str
    detail: str = ""
    fix: str = ""

    def as_dict(self) -> dict[str, str]:
        return dataclasses.asdict(self)


def register(subparsers: t.Any, add_global_flags: t.Callable[..., None]) -> None:
    parser = subparsers.add_parser(
        "doctor",
        help="find out why something is not working",
        description=(
            "Check that everything Atlas needs is installed and that this repository is shaped "
            "the way the standard expects. Each problem comes with the command that fixes it. "
            "Safe to run anywhere: outside a repository it checks the environment only, which "
            "makes it the right first command when an install seems wrong."
        ),
    )
    add_global_flags(parser)
    parser.set_defaults(handler=run)


def _environment() -> list[Finding]:
    findings: list[Finding] = []
    version = ".".join(str(p) for p in sys.version_info[:3])
    if sys.version_info[:2] >= MIN_PYTHON:
        findings.append(Finding("ok", "Python", version))
    else:
        findings.append(
            Finding("fail", "Python", version,
                    f"Atlas needs Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or newer.")
        )

    for module, why in (("yaml", "reading manifests"), ("jsonschema", "validating them")):
        if importlib.util.find_spec(module):
            findings.append(Finding("ok", f"{module}", why))
        else:
            findings.append(
                Finding("fail", f"{module}", "missing", "pip install atlas-standard")
            )

    if shutil.which("git"):
        findings.append(Finding("ok", "git", shutil.which("git") or ""))
    else:
        findings.append(
            Finding("warn", "git", "not on PATH",
                    "Without git, the root closed-set check falls back to reading .gitignore.")
        )
    findings.append(Finding("ok", "atlas", f"v{__version__}", ""))
    return findings


def _repository(ctx: Context) -> tuple[list[Finding], bool]:
    try:
        repo = find_repository(getattr(ctx.args, "directory", None))
    except NoRepositoryError as error:
        return [Finding("skip", "repository", "not inside one", error.hint or "")], False

    findings = [Finding("ok", "repository", str(repo.root))]

    for label, path, required in (
        ("manifest", repo.manifest, True),
        ("agent guide", repo.root / "AGENTS.md", True),
        ("docs/", repo.docs, True),
        ("tests/", repo.tests, False),
        ("work/", repo.work, False),
        ("library/", repo.library, False),
        ("design tokens", repo.tokens, False),
    ):
        if path.exists():
            findings.append(Finding("ok", label, repo.rel(path)))
        elif required:
            findings.append(Finding("fail", label, "missing", f"Create {repo.rel(path)}."))
        else:
            findings.append(Finding("skip", label, "not adopted"))

    try:
        dirty = subprocess.run(
            ["git", "status", "--porcelain"], cwd=repo.root,
            capture_output=True, text=True, timeout=10,
        )
        if dirty.returncode == 0:
            count = len([ln for ln in dirty.stdout.splitlines() if ln.strip()])
            findings.append(
                Finding("ok" if not count else "warn", "working tree",
                        "clean" if not count else f"{count} uncommitted change(s)")
            )
    except (OSError, subprocess.SubprocessError):
        pass

    report = compliance.run(repo)
    if report.ok:
        findings.append(Finding("ok", "compliance", f"{report.passed} gate(s) pass"))
    else:
        findings.append(
            Finding("fail", "compliance",
                    f"{len(report.violations)} violation(s) across {report.failed} gate(s)",
                    "atlas check")
        )
    return findings, True


def run(ctx: Context) -> ExitCode:
    console = ctx.console
    environment = _environment()
    repository, in_repo = _repository(ctx)

    console.emit(
        {
            "environment": [f.as_dict() for f in environment],
            "repository": [f.as_dict() for f in repository],
            "ok": not any(f.state == "fail" for f in environment + repository),
        }
    )

    console.title("atlas doctor", "environment and repository diagnostics")
    console.rule("environment")
    for finding in environment:
        console.status(finding.state, finding.label.ljust(14), finding.detail)
        if finding.fix:
            console.write(f"    {console.paint(finding.fix, Style.CYAN)}")

    console.write()
    console.rule("repository")
    for finding in repository:
        console.status(finding.state, finding.label.ljust(14), finding.detail)
        if finding.fix:
            console.write(f"    {console.paint(finding.fix, Style.CYAN)}")

    failures = [f for f in environment + repository if f.state == "fail"]
    warnings = [f for f in environment + repository if f.state == "warn"]
    console.write()
    console.rule()
    if failures:
        console.status("fail", f"{len(failures)} problem(s) need attention")
        return ExitCode.FAILURE
    if warnings:
        console.status("warn", f"{len(warnings)} warning(s); nothing blocking")
        return ExitCode.OK
    console.status("ok", "everything checks out" if in_repo else "environment is ready")
    return ExitCode.OK
