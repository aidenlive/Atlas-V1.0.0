"""Finding the repository, and naming the places inside it.

One object answers "where am I, and where does everything live". Commands take
a :class:`Repository` rather than assembling paths themselves, so a directory
that moves is renamed in one file.
"""

from __future__ import annotations

import dataclasses
import pathlib

from .errors import NotARepositoryError

__all__ = ["Repository", "discover", "default_spec_dir", "default_schema_dir", "EXCLUDED_DIRS"]


def default_spec_dir() -> pathlib.Path:
    """The standards that shipped with the installed package."""
    here = pathlib.Path(__file__).resolve()
    packaged = here.parent / "_data" / "spec"
    return packaged if packaged.is_dir() else here.parents[2] / "spec"


def default_schema_dir() -> pathlib.Path:
    """The schemas that shipped with the installed package.

    Mirrored into the wheel from ``spec/`` at build time (see pyproject.toml), so
    there is one copy in the source tree and one in the artefact, never two under
    maintenance.
    """
    here = pathlib.Path(__file__).resolve()
    return default_spec_dir() / "schemas"

#: Directory names that no walk of the repository descends into. `@removal-safe`
#: is the migration archive of the predecessor repository: it is deliberately
#: exempt, and deliberately temporary (see docs/decisions/0005-archive-then-rebuild.md).
EXCLUDED_DIRS = frozenset(
    {
        ".git",
        ".github",
        "@removal-safe",
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "venv",
        "node_modules",
        "site",
        "dist",
        "build",
    }
)


@dataclasses.dataclass(frozen=True)
class Repository:
    """An Atlas repository: a root directory containing ``project.yaml``."""

    root: pathlib.Path

    # -- named locations -------------------------------------------------
    @property
    def manifest_path(self) -> pathlib.Path:
        return self.root / "project.yaml"

    @property
    def authority_path(self) -> pathlib.Path:
        return self.root / "authority.yaml"

    @property
    def spec_dir(self) -> pathlib.Path:
        """This repository's standards, or the installed copy.

        Only the standards repository carries ``spec/``. Everywhere else,
        ``atlas spec show voice`` still has to work — a writer should be able to
        read the rule they were cited from whatever repository they are in.
        """
        local = self.root / "spec"
        return local if (local / "voice.md").is_file() else default_spec_dir()

    @property
    def schema_dir(self) -> pathlib.Path:
        """This repository's schemas, or the installed copy.

        Only the standards repository carries ``spec/``. Every other repository
        is validated against the schemas that shipped with the tool, which is
        what keeps a scaffolded repository checkable on its first run.
        """
        local = self.root / "spec" / "schemas"
        return local if local.is_dir() else default_schema_dir()

    @property
    def docs_dir(self) -> pathlib.Path:
        return self.root / "docs"

    @property
    def library_dir(self) -> pathlib.Path:
        return self.root / "library"

    @property
    def prompts_dir(self) -> pathlib.Path:
        return self.library_dir / "prompts"

    @property
    def lexicon_path(self) -> pathlib.Path:
        return self.library_dir / "lexicon" / "terms.yaml"

    @property
    def content_dir(self) -> pathlib.Path:
        return self.root / "content"

    @property
    def work_dir(self) -> pathlib.Path:
        return self.root / "work"

    @property
    def template_dir(self) -> pathlib.Path:
        return self.root / "template"

    # -- questions commands ask ------------------------------------------
    @property
    def is_standards_source(self) -> bool:
        """True in the repository that *publishes* the standards.

        A few checks (every standard carries metadata, every rule is unique)
        only make sense where ``spec/`` is the product rather than a copy.
        """
        return (self.root / "spec" / "voice.md").is_file()

    def has(self, *relative: str) -> bool:
        return all((self.root / part).exists() for part in relative)

    def relative(self, path: pathlib.Path) -> str:
        try:
            return str(path.relative_to(self.root))
        except ValueError:
            return str(path)

    def walk_markdown(self, *subdirs: str) -> list[pathlib.Path]:
        """Every Markdown file under ``subdirs`` (or the whole repository).

        Excluded directories are never descended into, so the archive under
        ``@removal-safe/`` cannot fail a check about live content.
        """
        roots = [self.root / s for s in subdirs] if subdirs else [self.root]
        found: list[pathlib.Path] = []
        for base in roots:
            if not base.exists():
                continue
            for path in sorted(base.rglob("*.md")):
                if any(part in EXCLUDED_DIRS for part in path.relative_to(self.root).parts):
                    continue
                found.append(path)
        return found


def discover(start: pathlib.Path | str | None = None) -> Repository:
    """Walk up from ``start`` until a directory holds ``project.yaml``.

    Raises :class:`NotARepositoryError` rather than guessing, because a tool
    that silently checks the wrong directory is worse than one that stops.
    """
    current = pathlib.Path(start or pathlib.Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "project.yaml").is_file():
            return Repository(root=candidate)
    raise NotARepositoryError(
        f"no project.yaml found in {current} or any parent directory",
        hint="run `atlas init <name> <path>` to start one, or -C DIR to point at an existing repository",
    )
