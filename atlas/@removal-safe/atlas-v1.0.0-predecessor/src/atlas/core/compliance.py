"""The compliance engine: PROJECT and PRESENTATION, enforced.

Every gate is a named :class:`Check` in a registry rather than a line in a shell
script. That buys three things the script could not offer:

* **Selection.** ``atlas check --only root-closed-set`` runs one gate, which is
  what you want while fixing one violation.
* **Reporting.** Each gate reports its own id, the rule it enforces, and its
  violations, so ``--json`` output is structured rather than scraped.
* **Extension.** A repository adopting a ninth standard registers a check; it
  does not fork a 120-line bash file.

Checks are pure functions of the repository. They read, they never write, and
they return violations rather than printing or exiting, so the same code backs
the CLI, the tests, and the pre-commit hook.
"""

from __future__ import annotations

import dataclasses
import pathlib
import re
import subprocess
import typing as t

from ..paths import Repository
from . import library as library_mod
from . import prompts as prompts_mod
from . import template as template_mod
from . import workstream as workstream_mod
from .manifest import Violation, load_manifest, validate_manifest

__all__ = ["Check", "CheckResult", "Report", "CHECKS", "register", "run", "check_ids"]

CheckFn = t.Callable[[Repository], list[Violation]]


@dataclasses.dataclass(frozen=True)
class Check:
    """One named compliance gate."""

    id: str
    summary: str
    rule: str
    run: CheckFn
    #: Gates that only apply where the normative sources live.
    standards_only: bool = False
    #: Gates that only apply once the repository adopts the companion standard.
    requires: str | None = None


@dataclasses.dataclass
class CheckResult:
    check: Check
    violations: list[Violation]
    skipped: str | None = None

    @property
    def ok(self) -> bool:
        return self.skipped is not None or not self.violations

    @property
    def state(self) -> str:
        if self.skipped:
            return "skip"
        return "ok" if not self.violations else "fail"

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "id": self.check.id,
            "summary": self.check.summary,
            "rule": self.check.rule,
            "state": self.state,
            "skipped": self.skipped,
            "violations": [v.as_dict() for v in self.violations],
        }


@dataclasses.dataclass
class Report:
    results: list[CheckResult]

    @property
    def violations(self) -> list[Violation]:
        return [v for r in self.results for v in r.violations]

    @property
    def ok(self) -> bool:
        return not self.violations

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.state == "ok")

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if r.state == "fail")

    @property
    def skipped(self) -> int:
        return sum(1 for r in self.results if r.state == "skip")

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "ok": self.ok,
            "summary": {
                "passed": self.passed,
                "failed": self.failed,
                "skipped": self.skipped,
                "violations": len(self.violations),
            },
            "checks": [r.as_dict() for r in self.results],
        }


CHECKS: list[Check] = []


def register(
    check_id: str,
    summary: str,
    rule: str,
    *,
    standards_only: bool = False,
    requires: str | None = None,
) -> t.Callable[[CheckFn], CheckFn]:
    """Register a compliance gate. Import-time side effect, by design."""

    def decorator(fn: CheckFn) -> CheckFn:
        CHECKS.append(
            Check(check_id, summary, rule, fn, standards_only=standards_only, requires=requires)
        )
        return fn

    return decorator


def check_ids() -> list[str]:
    return [c.id for c in CHECKS]


# ============================================================== the closed set

#: PROJECT §8. The base set plus the four extensions ADR-0002 sanctions and the
#: two ADR-0007 adds for the packaged CLI.
ALLOWED_ROOT_FILES = frozenset(
    {
        "README.md",
        "LICENSE",
        "CHANGELOG.md",
        "AGENTS.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "SECURITY.md",
        "ROADMAP.md",
        "project.yaml",
        "pyproject.toml",
        "CLAUDE.md",
        "GEMINI.md",
        ".gitignore",
        ".editorconfig",
        ".cursorrules",
        ".pre-commit-config.yaml",
    }
)
ALLOWED_ROOT_DIRS = frozenset(
    {
        "src",
        "spec",
        "docs",
        "examples",
        "tests",
        "scripts",
        "ops",
        "template",
        "assets",
        "library",
        "work",
        ".github",
        ".git",
    }
)

VENDOR_STUBS = ("CLAUDE.md", "GEMINI.md", ".cursorrules")
README_SECTIONS = ("## What & Why", "## Quickstart", "## Documentation", "## Status")


def _git_ignored(repo: Repository, name: str) -> bool:
    """True when git ignores the path.

    Build output is not sanctioned structure; it is *ignored* structure. Asking
    git means ``site/`` stops being a violation for the same reason it stops
    being committed, and if someone un-ignores it, this check starts failing,
    which is the correct outcome rather than a silent exception list.
    """
    try:
        result = subprocess.run(
            ["git", "check-ignore", "-q", name],
            cwd=repo.root,
            capture_output=True,
            timeout=10,
        )
        if result.returncode in (0, 1):
            return result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        pass
    # Exported archives have no work tree, so fall back to a literal scan of
    # .gitignore. Only root-level names are being tested here, so a pattern is
    # normalized by stripping both slashes: `/site/`, `site/`, and `site` all
    # match the root entry `site`. Stripping only the trailing slash silently
    # stopped matching the moment the patterns were anchored, and the gate began
    # reporting build output as an unsanctioned directory.
    gitignore = repo.root / ".gitignore"
    if not gitignore.exists():
        return False
    patterns = {
        line.strip().strip("/")
        for line in gitignore.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }
    return name.strip("/") in patterns


@register("root-closed-set", "Root contains only sanctioned entries", "PROJECT §8, §9")
def check_root(repo: Repository) -> list[Violation]:
    violations: list[Violation] = []
    for entry in sorted(repo.root.iterdir()):
        name = entry.name
        if name == ".git" or _git_ignored(repo, name):
            continue
        if entry.is_dir():
            if name not in ALLOWED_ROOT_DIRS:
                violations.append(
                    Violation(f"{name}/", "unsanctioned root directory", "PROJECT §9")
                )
        elif name not in ALLOWED_ROOT_FILES:
            violations.append(Violation(name, "unsanctioned root file", "PROJECT §8"))
    return violations


@register("vendor-stubs", "Agent stubs are pointers, not second sources", "PROJECT §12")
def check_vendor_stubs(repo: Repository) -> list[Violation]:
    violations: list[Violation] = []
    for stub in VENDOR_STUBS:
        path = repo.root / stub
        if not path.exists():
            continue
        lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
        if len(lines) > 3:
            violations.append(
                Violation(stub, f"exceeds 3 lines ({len(lines)}): stubs must be pointers", "PROJECT §12")
            )
        if "AGENTS.md" not in path.read_text(encoding="utf-8"):
            violations.append(Violation(stub, "does not point to AGENTS.md", "PROJECT §12"))
    return violations


@register("manifest", "project.yaml validates against its schema", "PROJECT §11")
def check_manifest(repo: Repository) -> list[Violation]:
    if not repo.manifest.exists():
        return [Violation("project.yaml", "missing repository manifest", "PROJECT §11")]
    schemas = repo.schemas if repo.schemas.is_dir() else repo.root / "schemas"
    if not schemas.is_dir():
        return []
    return validate_manifest(load_manifest(repo.manifest), schemas)


@register("readme-skeleton", "README carries the required sections", "PROJECT §8")
def check_readme(repo: Repository) -> list[Violation]:
    readme = repo.root / "README.md"
    if not readme.exists():
        return [Violation("README.md", "missing", "PROJECT §8")]
    text = readme.read_text(encoding="utf-8")
    violations = [
        Violation("README.md", f"missing required section: {section}", "PROJECT §8")
        for section in README_SECTIONS
        if section not in text
    ]
    head = "\n".join(text.splitlines()[:10])
    if not re.search(r"<img |<picture>", head):
        violations.append(
            Violation("README.md", "must open with a hero visual", "PRESENTATION P-02")
        )
    elif 'alt="' not in head:
        violations.append(Violation("README.md", "hero image missing alt text", "PRESENTATION P-02"))
    return violations


@register("agents-guide", "AGENTS.md has all seven required sections", "PROJECT §12")
def check_agents(repo: Repository) -> list[Violation]:
    agents = repo.root / "AGENTS.md"
    if not agents.exists():
        return [Violation("AGENTS.md", "missing canonical agent guide", "PROJECT §12")]
    text = agents.read_text(encoding="utf-8")
    return [
        Violation("AGENTS.md", f"missing section {n}", "PROJECT §12")
        for n in range(1, 8)
        if f"## {n}." not in text
    ]


@register("changelog", "CHANGELOG has an Unreleased section", "PROJECT §8")
def check_changelog(repo: Repository) -> list[Violation]:
    changelog = repo.root / "CHANGELOG.md"
    if not changelog.exists():
        return [Violation("CHANGELOG.md", "missing", "PROJECT §8")]
    if not re.search(r"^## \[Unreleased\]", changelog.read_text(encoding="utf-8"), re.M):
        return [Violation("CHANGELOG.md", "missing [Unreleased] section", "PROJECT §8")]
    return []


@register("forge-metadata", "Declared metadata matches forge settings", "PRESENTATION P-01, P-05")
def check_forge_metadata(repo: Repository) -> list[Violation]:
    if not repo.manifest.exists():
        return []
    manifest = load_manifest(repo.manifest)
    metadata = manifest.get("metadata") or {}
    description = metadata.get("description", "")
    if not description:
        return [
            Violation("project.yaml", "missing metadata.description", "PRESENTATION P-01")
        ]
    settings = repo.forge / "settings.yml"
    if settings.exists() and description not in settings.read_text(encoding="utf-8"):
        return [
            Violation(
                ".github/settings.yml",
                "description drifts from project.yaml metadata",
                "PRESENTATION P-05",
            )
        ]
    return []


@register(
    "workstreams",
    "Every workstream is valid and its index is current",
    "WORKSTREAM W-01..W-20",
    requires="work",
)
def check_workstreams(repo: Repository) -> list[Violation]:
    return workstream_mod.validate(repo)


@register(
    "library",
    "Library indexes and files agree in both directions",
    "LIBRARY L-A2",
    requires="library",
)
def check_library(repo: Repository) -> list[Violation]:
    return library_mod.validate(repo)


@register(
    "prompts",
    "Prompt catalog matches the files on disk",
    "LIBRARY L-08",
    requires="prompts",
)
def check_prompts(repo: Repository) -> list[Violation]:
    return prompts_mod.validate(repo)


@register(
    "template-mirror",
    "template/ mirrors its canonical sources",
    "ADR-0003",
    standards_only=True,
)
def check_template_mirror(repo: Repository) -> list[Violation]:
    return template_mod.check_mirror(repo)


@register(
    "spec-front-matter",
    "Every specification declares complete front matter",
    "PROJECT §13",
    standards_only=True,
)
def check_spec_front_matter(repo: Repository) -> list[Violation]:
    from .specs import load_specs

    required = ("id", "order", "title", "tagline", "question", "version", "status")
    violations: list[Violation] = []
    orders: dict[int, str] = {}
    for spec in load_specs(repo.spec):
        rel = f"spec/{spec.path.name}"
        for key in required:
            if not spec.meta.get(key):
                violations.append(Violation(rel, f"front matter missing `{key}`", "PROJECT §13"))
        if spec.order in orders:
            violations.append(
                Violation(rel, f"duplicate reading order {spec.order} (also {orders[spec.order]})")
            )
        orders[spec.order] = rel
    return violations


# ------------------------------------------------------------------------ run

def _applicable(check: Check, repo: Repository) -> str | None:
    """Return a skip reason, or None when the check applies."""
    if check.standards_only and not repo.is_standards_repository():
        return "not a standards repository"
    if check.requires:
        target = {
            "work": repo.work,
            "library": repo.library,
            "prompts": repo.prompts,
        }[check.requires]
        if not target.is_dir():
            return f"{check.requires}/ not adopted"
    return None


def run(repo: Repository, *, only: t.Sequence[str] | None = None) -> Report:
    """Run the registered gates, in registration order."""
    selected = list(CHECKS)
    if only:
        wanted = set(only)
        unknown = wanted - set(check_ids())
        if unknown:
            from ..errors import UsageError

            raise UsageError(
                f"unknown check(s): {', '.join(sorted(unknown))}",
                hint=f"Available: {', '.join(check_ids())}",
            )
        selected = [c for c in CHECKS if c.id in wanted]

    results: list[CheckResult] = []
    for check in selected:
        reason = _applicable(check, repo)
        if reason:
            results.append(CheckResult(check, [], skipped=reason))
            continue
        try:
            results.append(CheckResult(check, check.run(repo)))
        except Exception as exc:  # noqa: BLE001 - a broken gate must not hide the rest
            results.append(
                CheckResult(check, [Violation(check.id, f"check raised {type(exc).__name__}: {exc}")])
            )
    return Report(results)


def find_root_offenders(repo: Repository) -> list[pathlib.Path]:
    """Unsanctioned root entries, as paths. Used by ``atlas doctor``."""
    return [repo.root / v.path.rstrip("/") for v in check_root(repo)]
