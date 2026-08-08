"""Find out why something is not working.

``check`` tells you the repository is wrong. ``doctor`` tells you the *setup* is
wrong: the wrong Python, a missing dependency, no manifest, a template that is
not where it should be. Each finding names the remedy, because a diagnosis
without a next step is just bad news.
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

from ...core import template as template_mod
from ...errors import ExitCode, NotARepositoryError
from ...paths import Repository, discover
from ...terminal import Console

SUMMARY = "diagnose the environment and this repository"

MIN_PYTHON = (3, 10)


def configure(parser: argparse.ArgumentParser) -> None:  # noqa: ARG001 - no options yet
    return None


def _findings(repo: Repository | None) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []

    def add(state: str, name: str, detail: str, remedy: str = "") -> None:
        found.append({"state": state, "name": name, "detail": detail, "remedy": remedy})

    version = ".".join(str(part) for part in sys.version_info[:3])
    add(
        "ok" if sys.version_info[:2] >= MIN_PYTHON else "fail",
        "python",
        version,
        "" if sys.version_info[:2] >= MIN_PYTHON else "atlas needs Python 3.10 or newer",
    )

    for module, why in (("yaml", "parses the manifests"), ("jsonschema", "validates them")):
        try:
            __import__(module)
            add("ok", module, why)
        except ModuleNotFoundError:
            add("fail", module, f"not installed — {why}", "pip install atlas-editorial")

    add(
        "ok" if shutil.which("git") else "warn",
        "git",
        shutil.which("git") or "not on PATH",
        "" if shutil.which("git") else "`atlas lint --changed` needs git",
    )

    if repo is None:
        add(
            "fail",
            "repository",
            "no project.yaml in this directory or any parent",
            "run `atlas init <name> <path>`, or -C DIR",
        )
        return found

    add("ok", "repository", str(repo.root))
    for label, path, remedy in (
        ("manifest", repo.manifest_path, "copy template/project.yaml"),
        ("authority", repo.authority_path, "copy template/authority.yaml"),
        ("standards", repo.spec_dir, "this repository does not carry the standards; that is fine"),
        ("lexicon", repo.lexicon_path, "add library/lexicon/terms.yaml to enable terminology checks"),
        ("work", repo.work_dir, "run `atlas work new <slug> --owner person:you`"),
    ):
        exists = path.exists()
        add(
            "ok" if exists else "warn",
            label,
            repo.relative(path) if exists else "missing",
            "" if exists else remedy,
        )

    try:
        root = template_mod.template_root(repo.root)
        add("ok", "template", str(root.relative_to(repo.root)) if root.is_relative_to(repo.root) else str(root))
    except Exception as exc:  # noqa: BLE001 - the diagnosis is the point
        add("warn", "template", str(exc), "`atlas init` will not work until this resolves")

    return found


def run(args: argparse.Namespace, console: Console) -> int:
    try:
        repo: Repository | None = discover(args.directory)
    except NotARepositoryError:
        repo = None

    findings = _findings(repo)
    failed = [f for f in findings if f["state"] == "fail"]

    if console.json_mode:
        console.json({"ok": not failed, "findings": findings})
        return int(ExitCode.OK if not failed else ExitCode.VIOLATIONS)

    console.title("atlas doctor")
    console.out()
    for finding in findings:
        console.state(finding["state"], f"{finding['name']:<12}{finding['detail']}")
        if finding["remedy"]:
            console.bullet(finding["remedy"])
    console.out()
    if failed:
        console.state("fail", f"{len(failed)} problems need fixing")
        return int(ExitCode.VIOLATIONS)
    console.state("ok", "everything atlas needs is here")
    return int(ExitCode.OK)
