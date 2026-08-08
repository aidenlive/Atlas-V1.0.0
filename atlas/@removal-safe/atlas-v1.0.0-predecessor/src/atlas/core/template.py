"""The starter template: mirroring it, and scaffolding from it.

``template/`` is the scaffold consumers copy, so it must ship a working system
rather than a description of one. Some of its files are not authored there:
they are copies of artifacts this repository already owns. Copies maintained by
hand drift: this pair drifted once already, the template's tooling having
gained a fix the canonical copy never received.

So the flow is one-directional and enforced: canonical source → template, with
``check_mirror`` run in CI so drift is a red build rather than a surprise in a
scaffolded repository months later.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import filecmp
import pathlib
import re
import shutil
import typing as t

from ..errors import NotFoundError, UsageError
from ..paths import Repository
from .manifest import Violation

__all__ = ["MIRRORS", "mirror_pairs", "check_mirror", "sync_mirror", "scaffold", "NAME_RE"]

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

#: (canonical source, destination inside template/). Directories are expanded
#: to file pairs, and a file present only in the destination is drift too.
MIRRORS: tuple[tuple[str, str], ...] = (
    ("spec/schemas/workstream.schema.json", "template/work/workstream.schema.json"),
    ("work/_template", "template/work/_template"),
)

#: Files whose content is substituted at scaffold time.
SUBSTITUTED_SUFFIXES = frozenset({".md", ".yaml", ".yml", ".svg", ".toml", ".txt"})


@dataclasses.dataclass(frozen=True)
class MirrorPair:
    source: pathlib.Path
    destination: pathlib.Path

    def current(self) -> bool:
        return self.destination.exists() and filecmp.cmp(
            self.source, self.destination, shallow=False
        )


def mirror_pairs(repo: Repository) -> list[MirrorPair]:
    """Flatten the directory mirrors into concrete file pairs."""
    pairs: list[MirrorPair] = []
    for source_rel, destination_rel in MIRRORS:
        source, destination = repo.root / source_rel, repo.root / destination_rel
        if not source.exists():
            raise NotFoundError(f"canonical mirror source missing: {source_rel}")
        if source.is_dir():
            pairs += [
                MirrorPair(f, destination / f.relative_to(source))
                for f in sorted(p for p in source.rglob("*") if p.is_file())
            ]
        else:
            pairs.append(MirrorPair(source, destination))
    return pairs


def check_mirror(repo: Repository) -> list[Violation]:
    """Report every file where the template has drifted from its source."""
    if not repo.template.is_dir():
        return []
    pairs = mirror_pairs(repo)
    violations = [
        Violation(repo.rel(pair.destination), "stale mirror. Run `atlas template sync`", "ADR-0003")
        for pair in pairs
        if not pair.current()
    ]
    expected = {pair.destination for pair in pairs}
    for _, destination_rel in MIRRORS:
        destination = repo.root / destination_rel
        if destination.is_dir():
            violations += [
                Violation(repo.rel(f), "present in template/ but not in the canonical source", "ADR-0003")
                for f in sorted(destination.rglob("*"))
                if f.is_file() and f not in expected
            ]
    return violations


def sync_mirror(repo: Repository) -> list[str]:
    """Rewrite the mirror from its canonical sources. Returns changed paths."""
    for _, destination_rel in MIRRORS:
        destination = repo.root / destination_rel
        if destination.is_dir():
            shutil.rmtree(destination)
    changed: list[str] = []
    for pair in mirror_pairs(repo):
        if pair.current():
            continue
        pair.destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pair.source, pair.destination)
        changed.append(repo.rel(pair.destination))
    return changed


# ------------------------------------------------------------------ scaffolding

def scaffold(
    repo: Repository,
    name: str,
    destination: pathlib.Path,
    *,
    owner: str = "person:you",
    description: str = "",
) -> list[pathlib.Path]:
    """Copy ``template/`` to ``destination`` with placeholders substituted."""
    if not NAME_RE.match(name):
        raise UsageError(
            f"project name must be lowercase-hyphenated: {name!r}",
            hint="Use letters, digits, and single hyphens: `payments-api`.",
        )
    if destination.exists() and any(destination.iterdir()):
        raise UsageError(f"{destination} exists and is not empty")
    if not repo.template.is_dir():
        raise NotFoundError(
            f"no template at {repo.rel(repo.template)}",
            hint="Run `atlas init` from a checkout of the Atlas standards repository.",
        )

    shutil.copytree(repo.template, destination, dirs_exist_ok=True)
    substitutions = {
        "{{PROJECT_NAME}}": name,
        "{{DATE}}": dt.date.today().isoformat(),
        "{{OWNER}}": owner,
        "{{DESCRIPTION}}": description or f"One line saying what {name} is.",
    }
    written: list[pathlib.Path] = []
    for path in sorted(destination.rglob("*")):
        if not path.is_file():
            continue
        written.append(path)
        if path.suffix.lower() not in SUBSTITUTED_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:  # pragma: no cover - binary in template
            continue
        replaced = text
        for needle, value in substitutions.items():
            replaced = replaced.replace(needle, value)
        if replaced != text:
            path.write_text(replaced, encoding="utf-8")
    return written


def remaining_placeholders(destination: pathlib.Path) -> dict[str, list[str]]:
    """Placeholders a scaffold still carries, so ``atlas init`` can list them.

    A scaffold that silently leaves ``{{PROJECT_NAME}}`` in three files is how
    a template ends up published with its placeholders intact.
    """
    pattern = re.compile(r"\{\{[A-Z_]+\}\}")
    found: dict[str, list[str]] = {}
    for path in sorted(destination.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUBSTITUTED_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:  # pragma: no cover
            continue
        for token in set(pattern.findall(text)):
            found.setdefault(token, []).append(path.relative_to(destination).as_posix())
    return {k: sorted(v) for k, v in sorted(found.items())}


def template_files(repo: Repository) -> t.Iterator[pathlib.Path]:
    if repo.template.is_dir():
        yield from (p for p in sorted(repo.template.rglob("*")) if p.is_file())
