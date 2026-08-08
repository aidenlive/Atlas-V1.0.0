"""The compliance engine: the standards, enforced on a repository.

Every gate is a named :class:`Check` in a registry rather than a line in a shell
script. That buys three things a script could not offer:

* **Selection.** ``atlas check --only root-closed-set`` runs one gate, which is
  what you want while fixing one violation.
* **Reporting.** Each gate reports its id, the rule it enforces, and its
  violations, so ``--json`` output is structured rather than scraped.
* **Extension.** A team with a house rule registers a check; it does not fork a
  growing shell script.

Gates are pure functions of the repository. They read, they never write, and
they return violations rather than printing or exiting, so the same code backs
the CLI, the tests, and the pre-commit hook. A gate that raises is reported as a
failed gate rather than taking the process down with it.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import pathlib
import re
import tempfile
import typing as t

from ..paths import EXCLUDED_DIRS, Repository
from . import frontmatter, lexicon as lexicon_mod, lint as lint_mod, prompts as prompts_mod
from . import specs as specs_mod
from . import workstream as workstream_mod
from .manifest import Violation, load_yaml, validate_manifest

__all__ = ["Check", "CheckResult", "Report", "CHECKS", "register", "run", "check_ids"]

CheckFn = t.Callable[[Repository], list[Violation]]


@dataclasses.dataclass(frozen=True)
class Check:
    """One named compliance gate."""

    id: str
    summary: str
    rule: str
    run: CheckFn
    #: Gates that only make sense where the standards themselves are published.
    standards_only: bool = False


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
            "violations": [violation.as_dict() for violation in self.violations],
        }


@dataclasses.dataclass
class Report:
    repository: pathlib.Path
    results: list[CheckResult]

    @property
    def violations(self) -> list[Violation]:
        return [v for result in self.results for v in result.violations]

    @property
    def ok(self) -> bool:
        return not self.violations

    @property
    def passed(self) -> int:
        return sum(1 for result in self.results if result.state == "ok")

    @property
    def failed(self) -> int:
        return sum(1 for result in self.results if result.state == "fail")

    @property
    def skipped(self) -> int:
        return sum(1 for result in self.results if result.state == "skip")

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "repository": str(self.repository),
            "ok": self.ok,
            "checks": [result.as_dict() for result in self.results],
            "summary": {
                "passed": self.passed,
                "failed": self.failed,
                "skipped": self.skipped,
                "violations": len(self.violations),
            },
        }


CHECKS: dict[str, Check] = {}


def register(id: str, summary: str, rule: str, *, standards_only: bool = False):
    def decorate(fn: CheckFn) -> CheckFn:
        CHECKS[id] = Check(id=id, summary=summary, rule=rule, run=fn, standards_only=standards_only)
        return fn

    return decorate


def check_ids() -> list[str]:
    return list(CHECKS)


# ---------------------------------------------------------------------------
# The sanctioned root
# ---------------------------------------------------------------------------

ROOT_FILES = frozenset(
    {
        "README.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "SECURITY.md",
        "LICENSE",
        "AGENTS.md",
        "CLAUDE.md",
        "GEMINI.md",
        "project.yaml",
        "authority.yaml",
        "pyproject.toml",
        ".gitignore",
        ".editorconfig",
    }
)

ROOT_DIRS = frozenset(
    {
        ".git",
        ".github",
        "assets",
        "content",
        "docs",
        "examples",
        "library",
        "scripts",
        "spec",
        "src",
        "template",
        "tests",
        "work",
        "@removal-safe",
    }
)

#: Directories whose Markdown is content and must therefore declare itself.
DECLARED_CONTENT_DIRS = ("docs", "spec", "content")


# ---------------------------------------------------------------------------
# Gates
# ---------------------------------------------------------------------------


@register("manifest-valid", "project.yaml is present and valid", "CONTENT C-01")
def _manifest_valid(repo: Repository) -> list[Violation]:
    if not repo.manifest_path.is_file():
        return [Violation(rule="CONTENT C-01", message="project.yaml is missing", path="project.yaml")]
    return validate_manifest(repo.manifest_path, repo.schema_dir, "project")


@register("authority-declared", "authority.yaml names who may approve", "AUTHORITY A-01")
def _authority(repo: Repository) -> list[Violation]:
    if not repo.authority_path.is_file():
        return [
            Violation(
                rule="AUTHORITY A-01",
                message="authority.yaml is missing: nobody is declared as able to approve",
                path="authority.yaml",
                hint="copy template/authority.yaml and name at least one approver",
            )
        ]
    violations = validate_manifest(repo.authority_path, repo.schema_dir, "authority")
    data = load_yaml(repo.authority_path)
    principals = {str(entry.get("id")) for entry in data.get("principals", []) if isinstance(entry, dict)}
    for role in data.get("roles", []) or []:
        if not isinstance(role, dict):
            continue
        for holder in role.get("held_by", []) or []:
            if str(holder) not in principals:
                violations.append(
                    Violation(
                        rule="AUTHORITY A-02",
                        message=f"role {role.get('name')!r} is held by undeclared principal {holder!r}",
                        path="authority.yaml",
                    )
                )
    manifest_owner = str(load_yaml(repo.manifest_path).get("owner", "")) if repo.manifest_path.is_file() else ""
    if manifest_owner and principals and manifest_owner not in principals:
        violations.append(
            Violation(
                rule="AUTHORITY A-02",
                message=f"project.yaml owner {manifest_owner!r} is not a principal in authority.yaml",
                path="project.yaml",
            )
        )
    return violations


@register("root-closed-set", "The root contains only sanctioned entries", "CONTENT C-02")
def _root_closed_set(repo: Repository) -> list[Violation]:
    violations: list[Violation] = []
    for entry in sorted(repo.root.iterdir()):
        name = entry.name
        if name.startswith(".") and name not in ROOT_FILES and name not in ROOT_DIRS:
            continue  # tool dotfiles are the tools' business, not the standard's
        if entry.is_dir():
            if name not in ROOT_DIRS and name not in EXCLUDED_DIRS:
                violations.append(
                    Violation(
                        rule="CONTENT C-02",
                        message=f"unsanctioned root directory: {name}/",
                        path=name,
                        hint="the root is a closed set; file it under docs/, library/, or work/",
                    )
                )
        elif name not in ROOT_FILES:
            violations.append(
                Violation(
                    rule="CONTENT C-02",
                    message=f"unsanctioned root file: {name}",
                    path=name,
                    hint="the root is the repository's first screen; move it into a directory",
                )
            )
    return violations


@register("standards-metadata", "Every standard declares its metadata", "CONTENT C-03", standards_only=True)
def _standards_metadata(repo: Repository) -> list[Violation]:
    violations: list[Violation] = []
    for spec in specs_mod.load_specs(repo.spec_dir):
        for field in specs_mod.REQUIRED_META:
            if not spec.meta.get(field):
                violations.append(
                    Violation(
                        rule="CONTENT C-03",
                        message=f"standard `{spec.id}` does not declare `{field}`",
                        path=f"spec/{spec.path.name}",
                    )
                )
        for companion in spec.companions:
            if not (repo.spec_dir / f"{companion}.md").is_file():
                violations.append(
                    Violation(
                        rule="CONTENT C-03",
                        message=f"standard `{spec.id}` names a companion that does not exist: {companion}",
                        path=f"spec/{spec.path.name}",
                    )
                )
    return violations


@register("rule-ids", "Rule identifiers are unique and match their standard", "CONTENT C-04", standards_only=True)
def _rule_ids(repo: Repository) -> list[Violation]:
    violations: list[Violation] = []
    seen: dict[str, str] = {}
    for spec in specs_mod.load_specs(repo.spec_dir):
        prefix = spec.rule_prefix
        numbers: list[int] = []
        for rule in spec.rules:
            if prefix and not rule.id.startswith(prefix):
                violations.append(
                    Violation(
                        rule="CONTENT C-04",
                        message=f"rule {rule.id} does not use the `{prefix}` prefix of `{spec.id}`",
                        path=f"spec/{spec.path.name}",
                        line=rule.line,
                    )
                )
            if rule.id in seen and seen[rule.id] != spec.id:
                violations.append(
                    Violation(
                        rule="CONTENT C-04",
                        message=f"rule {rule.id} is defined in both `{seen[rule.id]}` and `{spec.id}`",
                        path=f"spec/{spec.path.name}",
                        line=rule.line,
                    )
                )
            seen[rule.id] = spec.id
            tail = rule.id.rsplit("-", 1)[-1]
            if tail.isdigit():
                numbers.append(int(tail))
        for expected, actual in enumerate(numbers, start=1):
            if expected != actual:
                violations.append(
                    Violation(
                        rule="CONTENT C-04",
                        message=f"`{spec.id}` numbers its rules with a gap or repeat at {prefix}{actual:02d}",
                        path=f"spec/{spec.path.name}",
                    )
                )
                break
    return violations


@register("content-declared", "Every document declares its facts", "CONTENT C-01")
def _content_declared(repo: Repository) -> list[Violation]:
    settings = _settings(repo)
    violations: list[Violation] = []
    for path in repo.walk_markdown(*DECLARED_CONTENT_DIRS):
        document = frontmatter.read(path)
        relative = repo.relative(path)
        if not document.has_frontmatter:
            violations.append(
                Violation(
                    rule="CONTENT C-01",
                    message="no front matter",
                    path=relative,
                    hint="declare " + ", ".join(settings.required_fields),
                )
            )
            continue
        for field in settings.required_fields:
            if not document.meta.get(field):
                violations.append(
                    Violation(
                        rule="CONTENT C-01",
                        message=f"front matter is missing `{field}`",
                        path=relative,
                    )
                )
    return violations


@register("content-fresh", "Nothing published is past its review date", "CONTENT C-05")
def _content_fresh(repo: Repository) -> list[Violation]:
    today = dt.date.today()
    violations: list[Violation] = []
    for path in repo.walk_markdown(*DECLARED_CONTENT_DIRS):
        document = frontmatter.read(path)
        review_by = document.meta.get("review_by")
        if not review_by:
            continue
        try:
            due = dt.date.fromisoformat(str(review_by))
        except ValueError:
            violations.append(
                Violation(
                    rule="CONTENT C-05",
                    message=f"`review_by` is not an ISO date: {review_by!r}",
                    path=repo.relative(path),
                )
            )
            continue
        if due < today:
            violations.append(
                Violation(
                    rule="CONTENT C-05",
                    message=f"review was due {due.isoformat()} ({(today - due).days} days ago)",
                    path=repo.relative(path),
                    hint="re-read it, then move the date or retire the document",
                )
            )
    return violations


@register("lexicon-consistent", "The lexicon does not contradict itself", "LANGUAGE L-01")
def _lexicon(repo: Repository) -> list[Violation]:
    lex = lexicon_mod.load_lexicon(repo.lexicon_path)
    if not lex.terms and not lex.phrases:
        return []
    violations: list[Violation] = []
    relative = repo.relative(repo.lexicon_path)
    canonical = {term.use.lower(): term for term in lex.terms}
    seen_ids: set[str] = set()
    for term in lex.terms:
        if term.id in seen_ids:
            violations.append(
                Violation(rule="LANGUAGE L-01", message=f"duplicate term id {term.id!r}", path=relative)
            )
        seen_ids.add(term.id)
        for wrong in term.avoid:
            if wrong == term.use:
                violations.append(
                    Violation(
                        rule="LANGUAGE L-01",
                        message=f"term {term.use!r} lists its own canonical form under `avoid`",
                        path=relative,
                    )
                )
            other = canonical.get(wrong.lower())
            if other is not None and other.id != term.id:
                violations.append(
                    Violation(
                        rule="LANGUAGE L-01",
                        message=f"{wrong!r} is canonical for {other.id!r} and forbidden by {term.id!r}",
                        path=relative,
                    )
                )
    for phrase in lex.phrases:
        if not phrase.use:
            violations.append(
                Violation(
                    rule="LANGUAGE L-02",
                    message=f"phrase {phrase.avoid!r} has no replacement",
                    path=relative,
                    hint="a rule without a remedy is a complaint",
                )
            )
        if phrase.severity not in lexicon_mod.SEVERITIES:
            violations.append(
                Violation(
                    rule="LANGUAGE L-02",
                    message=f"phrase {phrase.avoid!r} has unknown severity {phrase.severity!r}",
                    path=relative,
                )
            )
    return violations


@register("prompt-shape", "Every prompt asks for exactly one thing", "CONTENT C-08")
def _prompt_shape(repo: Repository) -> list[Violation]:
    violations: list[Violation] = []
    for prompt in prompts_mod.load_prompts(repo.prompts_dir):
        relative = repo.relative(prompt.path)
        if prompt.sentences > prompts_mod.MAX_SENTENCES:
            violations.append(
                Violation(
                    rule="CONTENT C-08",
                    message=f"{prompt.sentences} sentences (limit {prompts_mod.MAX_SENTENCES})",
                    path=relative,
                    hint="longer than this is a brief, and briefs live in work/",
                )
            )
        if prompt.is_destructive and "propose" not in prompt.text.lower() and "plan" not in prompt.text.lower():
            violations.append(
                Violation(
                    rule="CONTENT C-09",
                    message="prompt removes or rewrites without asking for a plan first",
                    path=relative,
                    hint="word it to propose the change, then wait",
                )
            )
        if "\n\n" in prompt.text:
            violations.append(
                Violation(
                    rule="CONTENT C-08",
                    message="prompt has more than one paragraph",
                    path=relative,
                )
            )
    return violations


@register("links-resolve", "Every relative link points at something", "STRUCTURE S-07")
def _links(repo: Repository) -> list[Violation]:
    pattern = re.compile(r"\[[^\]]*\]\((?P<target>[^)\s]+)\)")
    violations: list[Violation] = []
    for path in repo.walk_markdown():
        document = frontmatter.read(path)
        for index, line in enumerate(document.lines):
            for match in pattern.finditer(line):
                target = match.group("target")
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                resolved = (path.parent / target.split("#", 1)[0]).resolve()
                if not resolved.exists():
                    violations.append(
                        Violation(
                            rule="STRUCTURE S-07",
                            message=f"link target does not exist: {target}",
                            path=repo.relative(path),
                            line=document.line_number(index),
                        )
                    )
    return violations


@register("generated-current", "Generated views match their sources", "AUTHORITY A-09")
def _generated_current(repo: Repository) -> list[Violation]:
    if not repo.work_dir.is_dir():
        return []
    violations: list[Violation] = []
    dashboard = repo.work_dir / "README.md"
    expected = workstream_mod.render_dashboard(repo.work_dir)
    if not dashboard.is_file():
        violations.append(
            Violation(rule="AUTHORITY A-09", message="work/README.md has not been generated", path="work/README.md")
        )
    elif dashboard.read_text(encoding="utf-8").strip() != expected.strip():
        violations.append(
            Violation(
                rule="AUTHORITY A-09",
                message="work/README.md is out of date with the task tables",
                path="work/README.md",
                hint="run `atlas work sync`",
            )
        )
    if not (repo.work_dir / "index.yaml").is_file():
        violations.append(
            Violation(
                rule="AUTHORITY A-09",
                message="work/index.yaml has not been generated",
                path="work/index.yaml",
                hint="run `atlas work sync`",
            )
        )
    return violations


@register("workstreams-shaped", "Every workstream has the same five sections", "AUTHORITY A-07")
def _workstreams(repo: Repository) -> list[Violation]:
    return workstream_mod.validate_workstreams(repo.work_dir, repo.schema_dir)


@register("prose-lints-clean", "Published prose passes the editorial rules", "VOICE V-01")
def _prose(repo: Repository) -> list[Violation]:
    lex = lexicon_mod.load_lexicon(repo.lexicon_path)
    settings = _settings(repo)
    violations: list[Violation] = []
    paths = [repo.root / "README.md", *repo.walk_markdown(*DECLARED_CONTENT_DIRS)]
    for path in paths:
        if not path.is_file():
            continue
        result = lint_mod.lint_document(
            frontmatter.read(path), lex, settings, skip=("declaration",)
        )
        for finding in result.errors:
            violations.append(
                dataclasses.replace(finding.as_violation(), path=repo.relative(path))
            )
    return violations


@register("template-compliant", "The starter template passes what it teaches", "CONTENT C-06")
def _template(repo: Repository) -> list[Violation]:
    """Scaffold the template into a temporary directory and check *that*.

    Validating the template files in place would only ever prove that the
    placeholders parse. The claim worth making is that a repository somebody
    creates from this template passes on its first run, so the gate creates one
    and runs every other gate against it.
    """
    if not repo.template_dir.is_dir():
        return []
    from . import template as template_mod

    with tempfile.TemporaryDirectory() as tmp:
        destination = pathlib.Path(tmp) / "scaffold-check"
        try:
            template_mod.scaffold(
                repo.template_dir,
                destination,
                name="scaffold-check",
                owner="role:editorial-lead",
                description="Scaffold verification run",
            )
        except Exception as exc:  # noqa: BLE001 - a broken template is the finding
            return [
                Violation(
                    rule="CONTENT C-06",
                    message=f"the template could not be scaffolded: {exc}",
                    path="template/",
                )
            ]

        report = run(Repository(root=destination), only=[c for c in CHECKS if c != "template-compliant"])
        return [
            dataclasses.replace(
                violation,
                path=f"template/{violation.path}" if violation.path else "template/",
            )
            for violation in report.violations
        ]


def _settings(repo: Repository) -> lint_mod.Settings:
    data = load_yaml(repo.manifest_path) if repo.manifest_path.is_file() else {}
    return lint_mod.Settings.from_manifest(data)


# ---------------------------------------------------------------------------
# Running
# ---------------------------------------------------------------------------


def run(repo: Repository, *, only: t.Sequence[str] | None = None) -> Report:
    from ..errors import NotFoundError

    selected = list(only) if only else list(CHECKS)
    for name in selected:
        if name not in CHECKS:
            raise NotFoundError(
                f"no check named {name!r}", hint=f"known checks: {', '.join(CHECKS)}"
            )

    results: list[CheckResult] = []
    for name in selected:
        check = CHECKS[name]
        if check.standards_only and not repo.is_standards_source:
            results.append(CheckResult(check=check, violations=[], skipped="not the standards repository"))
            continue
        try:
            violations = check.run(repo)
        except Exception as exc:  # a broken gate is a failed gate, not a crash
            violations = [
                Violation(rule=check.rule, message=f"check raised {type(exc).__name__}: {exc}")
            ]
        results.append(CheckResult(check=check, violations=violations))
    return Report(repository=repo.root, results=results)
