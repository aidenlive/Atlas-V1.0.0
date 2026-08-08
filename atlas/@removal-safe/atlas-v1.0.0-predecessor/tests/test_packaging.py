"""Packaging invariants: what ships, and what must never be excluded.

These exist because of a real incident. `.gitignore` carried `site/` to exclude
the generated documentation site. With no leading slash that pattern matches a
directory of that name at *any* depth, so it also excluded `src/atlas/site/` —
the site generator package. The working tree was complete, every test passed
locally, and CI checked out a repository with no `atlas.site` module in it. The
first sign of trouble was `ModuleNotFoundError` from an installed entry point.

The lesson generalises past that one pattern: anything that decides what ships
needs a test, because the failure mode is invisible from inside a working tree.
"""

from __future__ import annotations

import importlib
import pathlib
import pkgutil
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=30
    )


def _has_git_repository() -> bool:
    try:
        return _git("rev-parse", "--is-inside-work-tree").returncode == 0
    except (OSError, subprocess.SubprocessError):  # pragma: no cover
        return False


requires_git = pytest.mark.skipif(
    not _has_git_repository(), reason="not a git work tree (exported archive)"
)


# ------------------------------------------------------------------ gitignore

@requires_git
def test_no_source_file_is_git_ignored():
    """The incident, made checkable.

    Not one file under `src/` or `tests/` may be excluded from version control.
    A build-output pattern that swallows a source package produces a repository
    that is complete on the author's disk and broken everywhere else.
    """
    sources = [
        p for p in [*SRC.rglob("*.py"), *(ROOT / "tests").rglob("*.py")]
        if "__pycache__" not in p.parts
    ]
    assert sources, "no sources found — the test is looking in the wrong place"

    result = _git("check-ignore", *[str(p.relative_to(ROOT)) for p in sources])
    ignored = [line for line in result.stdout.splitlines() if line.strip()]
    assert not ignored, (
        "these source files are excluded by .gitignore and would never be "
        "committed:\n  " + "\n  ".join(ignored)
    )


@requires_git
def test_build_output_patterns_are_anchored():
    """A build-output pattern must be anchored to the repository root.

    `site/` matches at any depth; `/site/` matches only the real build output.
    Anchoring is the fix, so the fix itself is what gets asserted — a test that
    only checked `src/atlas/site/` would pass again the moment someone adds a
    `dist/` or `build/` package.
    """
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    build_outputs = {"site", "dist", "build"}
    offenders = []
    for line in gitignore.splitlines():
        entry = line.strip()
        if not entry or entry.startswith("#"):
            continue
        if entry.rstrip("/").lstrip("/") in build_outputs and not entry.startswith("/"):
            offenders.append(entry)
    assert not offenders, (
        f"unanchored build-output patterns: {offenders}. "
        "Use a leading slash so they cannot match a package of the same name."
    )


@requires_git
def test_the_generated_site_is_still_ignored():
    """The anchoring fix must not stop ignoring what it was written to ignore."""
    (ROOT / "site").mkdir(exist_ok=True)
    marker = ROOT / "site" / ".ignore-probe"
    marker.write_text("", encoding="utf-8")
    try:
        assert _git("check-ignore", "-q", "site/.ignore-probe").returncode == 0, (
            "the generated site is no longer ignored — it would be committed"
        )
    finally:
        marker.unlink(missing_ok=True)


# ------------------------------------------------------------------- packages

def test_every_subpackage_imports():
    """Catch a missing `__init__.py` or an unimportable module before CI does."""
    import atlas

    failures: list[str] = []
    for module in pkgutil.walk_packages(atlas.__path__, prefix="atlas."):
        try:
            importlib.import_module(module.name)
        except Exception as error:  # noqa: BLE001 - reporting, not handling
            failures.append(f"{module.name}: {type(error).__name__}: {error}")
    assert not failures, "\n".join(failures)


def test_the_declared_subpackages_are_present():
    """The three-layer split is the architecture; assert it exists on disk."""
    for package in ("atlas.core", "atlas.site", "atlas.cli", "atlas.cli.commands"):
        module = importlib.import_module(package)
        assert module.__file__, f"{package} has no module file"


def test_every_package_directory_has_an_init():
    """A directory without `__init__.py` is data, not a package, to most builders."""
    missing = [
        str(d.relative_to(ROOT))
        for d in SRC.rglob("*")
        if d.is_dir() and d.name != "__pycache__" and not (d / "__init__.py").exists()
    ]
    assert not missing, f"package directories without __init__.py: {missing}"


# ---------------------------------------------------------------- entry point

def test_console_script_resolves():
    """`atlas = atlas.cli:main` must actually resolve to a callable."""
    import tomllib

    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    target = pyproject["project"]["scripts"]["atlas"]
    module_name, _, attribute = target.partition(":")
    module = importlib.import_module(module_name)
    assert callable(getattr(module, attribute)), f"{target} is not callable"


def test_declared_version_matches_the_package():
    import tomllib

    import atlas

    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["version"] == atlas.__version__, (
        "pyproject.toml and atlas.__version__ disagree"
    )


def test_runtime_dependencies_are_importable():
    """Anything imported at module scope must be a declared dependency."""
    import tomllib

    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    declared = {
        dep.split(">")[0].split("=")[0].split("[")[0].strip().lower()
        for dep in pyproject["project"]["dependencies"]
    }
    assert "pyyaml" in declared and "jsonschema" in declared

    # The CLI must start with only the standard library plus these two.
    for module in ("yaml", "jsonschema"):
        importlib.import_module(module)


@pytest.mark.skipif(sys.version_info < (3, 11), reason="tomllib needs 3.11")
def test_wheel_would_contain_every_source_file():
    """The hatchling `packages` entry must cover the whole tree under src/.

    Checked by construction rather than by building a wheel: a build in the test
    suite is slow and needs network access on a cold cache.
    """
    import tomllib

    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    packages = pyproject["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"]
    assert packages == ["src/atlas"], packages
    covered = ROOT / packages[0]
    for source in SRC.rglob("*.py"):
        if "__pycache__" in source.parts:
            continue
        assert covered in source.parents or source.parent == covered, (
            f"{source.relative_to(ROOT)} is outside the packaged tree"
        )


# --------------------------------------------------------------------- badges

def test_badges_match_the_manifest():
    """PRESENTATION P-07: a badge value must be derivable from project.yaml.

    The badges are drawn locally rather than fetched from a badge service
    precisely so this can be asserted. A hand-typed shields.io URL can claim
    `maturity-stable` for years after the manifest says otherwise, and nothing
    notices; here, the claim and its source are compared on every run.
    """
    import re

    manifest = (ROOT / "project.yaml").read_text(encoding="utf-8")

    def field(name: str) -> str:
        m = re.search(rf"^{name}:\s*(.+?)\s*(?:#.*)?$", manifest, re.M)
        assert m, f"project.yaml declares no {name}"
        return m.group(1).strip().strip("\"'")

    badges = ROOT / "assets" / "badges"
    assert badges.is_dir(), "badges have never been generated"

    for name in ("stage", "maturity", "standard"):
        svg = (badges / f"{name}.svg").read_text(encoding="utf-8")
        assert field(name) in svg, (
            f"the {name} badge disagrees with project.yaml — "
            "run `python scripts/build_assets.py`"
        )

    release = re.search(r"^## \[(\d+\.\d+\.\d+)\]", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), re.M)
    assert release, "CHANGELOG has no released version"
    assert f"v{release.group(1)}" in (badges / "release.svg").read_text(encoding="utf-8")


def test_badges_never_rely_on_color_alone():
    """The dot carries status; the text must repeat it (WCAG 1.4.1).

    Same rule the terminal and the site follow: a reader who cannot see the
    green dot still reads the word STABLE.
    """
    for svg_path in sorted((ROOT / "assets" / "badges").glob("*.svg")):
        svg = svg_path.read_text(encoding="utf-8")
        assert "<title>" in svg, f"{svg_path.name} has no accessible name"
        assert 'role="img"' in svg and "aria-label=" in svg, svg_path.name
        assert "<text" in svg, f"{svg_path.name} states its value only as color"


def test_banners_carry_no_countable_boast():
    """A banner is regenerated rarely, so it must not state a number.

    `EIGHT STANDARDS · ONE CLI` was baked into the artwork. Add a ninth
    standard and the banner is quietly wrong in every README that embeds it.
    """
    for svg_path in sorted((ROOT / "assets").glob("banner*.svg")):
        text = svg_path.read_text(encoding="utf-8")
        for boast in ("EIGHT STANDARDS", "ONE CLI"):
            assert boast not in text, f"{svg_path.name} still claims {boast!r}"
