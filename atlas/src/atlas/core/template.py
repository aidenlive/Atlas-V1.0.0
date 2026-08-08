"""Scaffolding: starting a repository that already passes.

The starter lives in ``template/`` at the root of this repository — one copy,
mirrored into the wheel at build time so ``atlas init`` works from a pip install
as well as from a checkout. There is no second, hand-maintained copy to drift.

Placeholders are deliberately loud (``{{NAME}}``, ``{{OWNER}}``, ``{{DATE}}``).
A scaffold that leaves a half-filled file behind is worse than one that shouts,
because the shouting is greppable and ``atlas check`` fails on it.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import pathlib
import re
import shutil

from ..errors import NotFoundError, UsageError

__all__ = ["template_root", "scaffold", "ScaffoldResult", "PLACEHOLDER"]

PLACEHOLDER = re.compile(r"\{\{([A-Z_]+)\}\}")
_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

#: Files that are never copied into a new repository.
_SKIP = {".DS_Store", "__pycache__", ".pytest_cache"}


@dataclasses.dataclass
class ScaffoldResult:
    destination: pathlib.Path
    files: list[pathlib.Path]

    def as_dict(self) -> dict[str, object]:
        return {
            "destination": str(self.destination),
            "files": [str(path) for path in self.files],
            "count": len(self.files),
        }


def template_root(repo_root: pathlib.Path | None = None) -> pathlib.Path:
    """Find the starter template: the checkout first, then the installed copy."""
    if repo_root is not None:
        candidate = repo_root / "template"
        if candidate.is_dir():
            return candidate
    packaged = pathlib.Path(__file__).resolve().parent.parent / "_data" / "template"
    if packaged.is_dir():
        return packaged
    raise NotFoundError(
        "no starter template found",
        hint="run from an Atlas checkout, or reinstall the package",
    )


def scaffold(
    template: pathlib.Path,
    destination: pathlib.Path,
    *,
    name: str,
    owner: str,
    description: str = "",
    force: bool = False,
) -> ScaffoldResult:
    """Copy the template to ``destination``, substituting the declared facts."""
    if not _NAME.match(name):
        raise UsageError(
            f"{name!r} is not a valid repository name",
            hint="use lower-case words joined by hyphens, e.g. brand-guidelines",
        )
    if destination.exists() and any(destination.iterdir()) and not force:
        raise UsageError(
            f"{destination} exists and is not empty",
            hint="pass --force to write into it anyway",
        )

    values = {
        "NAME": name,
        "TITLE": name.replace("-", " ").title(),
        "OWNER": owner,
        "DATE": dt.date.today().isoformat(),
        "REVIEW_DATE": (dt.date.today() + dt.timedelta(days=180)).isoformat(),
        "YEAR": str(dt.date.today().year),
        "DESCRIPTION": description or f"Editorial content for {name}",
    }

    written: list[pathlib.Path] = []
    for source in sorted(template.rglob("*")):
        if any(part in _SKIP for part in source.parts):
            continue
        target = destination / source.relative_to(template)
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            text = source.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            shutil.copy2(source, target)
            written.append(target)
            continue
        target.write_text(PLACEHOLDER.sub(lambda m: values.get(m.group(1), m.group(0)), text), encoding="utf-8")
        written.append(target)

    return ScaffoldResult(destination=destination, files=written)
