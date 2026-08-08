"""Repository discovery.

Every command needs one answer to "which repository am I operating on?", and it
must not depend on the current working directory being the repository root.
:class:`Repository` resolves that once, from an explicit ``-C`` directory or by
walking upward, and exposes the canonical paths as attributes so no other
module builds a path out of string fragments.
"""

from __future__ import annotations

import dataclasses
import os
import pathlib

from .errors import AtlasError, ExitCode

__all__ = ["Repository", "find_repository", "NoRepositoryError"]

#: A directory is an Atlas repository if it carries the manifest. `project.yaml`
#: is the one file PROJECT requires of every repository past `idea` stage, so it
#: is the only reliable marker: `.git` is absent in exported archives and
#: present in things that are not repositories of ours.
MARKER = "project.yaml"


class NoRepositoryError(AtlasError):
    """Raised when no Atlas repository encloses the working directory."""

    exit_code = ExitCode.NO_REPOSITORY


@dataclasses.dataclass(frozen=True)
class Repository:
    """The resolved repository root and the paths that hang off it.

    Paths are exposed even when the directory does not exist: a scaffolded
    repository has no ``library/`` until it adopts LIBRARY, and callers should
    branch on ``.exists()`` rather than guessing at path shapes themselves.
    """

    root: pathlib.Path

    # --- declared structure (PROJECT §9) ---
    @property
    def manifest(self) -> pathlib.Path:
        return self.root / "project.yaml"

    @property
    def spec(self) -> pathlib.Path:
        return self.root / "spec"

    @property
    def schemas(self) -> pathlib.Path:
        return self.root / "spec" / "schemas"

    @property
    def docs(self) -> pathlib.Path:
        return self.root / "docs"

    @property
    def work(self) -> pathlib.Path:
        return self.root / "work"

    @property
    def library(self) -> pathlib.Path:
        return self.root / "library"

    @property
    def prompts(self) -> pathlib.Path:
        return self.root / "library" / "prompts"

    @property
    def examples(self) -> pathlib.Path:
        return self.root / "examples"

    @property
    def template(self) -> pathlib.Path:
        return self.root / "template"

    @property
    def assets(self) -> pathlib.Path:
        return self.root / "assets"

    @property
    def tests(self) -> pathlib.Path:
        return self.root / "tests"

    @property
    def scripts(self) -> pathlib.Path:
        return self.root / "scripts"

    @property
    def tokens(self) -> pathlib.Path:
        return self.root / "assets" / "design" / "tokens.yaml"

    @property
    def forge(self) -> pathlib.Path:
        return self.root / ".github"

    # --- derived ---
    @property
    def site_out(self) -> pathlib.Path:
        return self.root / "site"

    def rel(self, path: pathlib.Path | str) -> str:
        """Path relative to the root, for messages a reader can act on."""
        p = pathlib.Path(path)
        try:
            return p.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return p.as_posix()

    def has_workstreams(self) -> bool:
        return self.work.is_dir()

    def is_standards_repository(self) -> bool:
        """True for the Atlas repository itself, which hosts the specs.

        Some commands (``atlas spec``, ``atlas template sync``) only mean
        something where the normative sources live. Detecting that from the
        filesystem beats a flag nobody remembers to set.
        """
        return (self.spec / "project.md").exists()


def find_repository(start: pathlib.Path | str | None = None) -> Repository:
    """Locate the enclosing repository, walking upward from ``start``.

    ``ATLAS_REPOSITORY`` overrides the search entirely, which is what makes the
    tool usable from a hook, an editor task, or a CI step whose working
    directory is not ours to choose.
    """
    override = os.environ.get("ATLAS_REPOSITORY")
    if override:
        root = pathlib.Path(override).expanduser().resolve()
        if not (root / MARKER).exists():
            raise NoRepositoryError(
                f"ATLAS_REPOSITORY points at {root}, which has no {MARKER}",
                hint="Unset ATLAS_REPOSITORY, or point it at a repository root.",
            )
        return Repository(root)

    here = pathlib.Path(start or pathlib.Path.cwd()).expanduser().resolve()
    if here.is_file():
        here = here.parent
    for candidate in (here, *here.parents):
        if (candidate / MARKER).exists():
            return Repository(candidate)
    raise NoRepositoryError(
        f"not an Atlas repository (no {MARKER} in {here} or any parent)",
        hint="Run `atlas init <name> <dir>` to create one, or `cd` into an existing repository.",
    )
