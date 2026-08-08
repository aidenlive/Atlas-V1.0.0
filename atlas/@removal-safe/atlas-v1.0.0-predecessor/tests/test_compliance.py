"""The compliance engine: the registry, the gates, and their reporting contract.

These tests care about the *engine* — that gates are pure, that skips are
distinguishable from passes, that a broken gate does not take the run down. The
individual rules each gate enforces are covered by the tests beside them.
"""

from __future__ import annotations

import pathlib
import shutil

import pytest

from atlas.core import compliance
from atlas.errors import UsageError
from atlas.paths import Repository

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = Repository(ROOT)


@pytest.fixture
def minimal(tmp_path):
    """A repository with a manifest and nothing else adopted."""
    shutil.copy2(ROOT / "project.yaml", tmp_path / "project.yaml")
    return Repository(tmp_path)


# ------------------------------------------------------------------- registry

def test_gate_ids_are_unique():
    ids = compliance.check_ids()
    assert len(ids) == len(set(ids))


def test_every_gate_declares_what_it_enforces():
    for check in compliance.CHECKS:
        assert check.summary, f"{check.id} has no summary"
        assert check.rule, f"{check.id} names no rule"


def test_this_repository_passes_its_own_standard():
    """ADR-0001: the suite is self-hosting."""
    report = compliance.run(REPO)
    assert report.ok, "\n".join(v.render() for v in report.violations)
    assert report.failed == 0


def test_gates_are_selectable():
    report = compliance.run(REPO, only=["root-closed-set"])
    assert len(report.results) == 1
    assert report.results[0].check.id == "root-closed-set"


def test_selecting_an_unknown_gate_is_a_usage_error():
    with pytest.raises(UsageError):
        compliance.run(REPO, only=["no-such-gate"])


def test_gates_are_pure(tmp_path):
    """A gate reads; it never writes. Running twice must change nothing on disk."""
    sandbox = tmp_path / "repo"
    shutil.copytree(ROOT, sandbox, ignore=shutil.ignore_patterns(
        ".git", "site", "__pycache__", ".pytest_cache"))
    repo = Repository(sandbox)

    before = {p: p.stat().st_mtime_ns for p in sandbox.rglob("*") if p.is_file()}
    compliance.run(repo)
    compliance.run(repo)
    after = {p: p.stat().st_mtime_ns for p in sandbox.rglob("*") if p.is_file()}
    assert before == after, "a compliance gate wrote to disk"


def test_reports_are_deterministic():
    first = compliance.run(REPO).as_dict()
    second = compliance.run(REPO).as_dict()
    assert first == second


# ---------------------------------------------------------------------- skips

def test_inapplicable_gates_are_skipped_with_a_reason(minimal):
    """"Not adopted" and "passing" are different facts; collapsing them lets a
    repository look compliant because it has nothing to be compliant about."""
    report = compliance.run(minimal)
    skipped = [r for r in report.results if r.state == "skip"]
    assert skipped, "a bare repository should skip the companion-standard gates"
    for result in skipped:
        assert result.skipped, f"{result.check.id} skipped without saying why"


def test_standards_only_gates_skip_elsewhere(minimal):
    report = compliance.run(minimal, only=["template-mirror"])
    assert report.results[0].state == "skip"


def test_skips_do_not_count_as_passes(minimal):
    report = compliance.run(minimal)
    assert report.passed + report.failed + report.skipped == len(report.results)


# ------------------------------------------------------------------ isolation

def test_a_raising_gate_is_reported_not_fatal(monkeypatch):
    """One broken gate must not hide the eleven that work."""
    def explode(repo):
        raise RuntimeError("boom")

    target = compliance.CHECKS[0]
    broken = compliance.Check(target.id, target.summary, target.rule, explode)
    monkeypatch.setattr(compliance, "CHECKS", [broken, *compliance.CHECKS[1:]])

    report = compliance.run(REPO)
    first = report.results[0]
    assert first.state == "fail"
    assert "RuntimeError" in first.violations[0].message
    assert len(report.results) == len(compliance.CHECKS)


# ------------------------------------------------------------- detection work

def test_an_unsanctioned_root_file_is_caught(tmp_path, minimal):
    (minimal.root / "notes.txt").write_text("stray", encoding="utf-8")
    violations = compliance.check_root(minimal)
    assert any("notes.txt" in v.path for v in violations)


def test_a_gitignored_path_is_not_a_violation(minimal):
    """Build output is ignored structure, not sanctioned structure."""
    (minimal.root / ".gitignore").write_text("site/\n", encoding="utf-8")
    (minimal.root / "site").mkdir()
    violations = compliance.check_root(minimal)
    assert not any("site" in v.path for v in violations)


def test_anchored_gitignore_patterns_are_honoured_without_git(minimal, monkeypatch):
    """The no-git fallback must read anchored patterns the way git does.

    `/site/`, `site/`, and `site` all exclude a root-level `site` directory.
    Normalising only the trailing slash made the fallback stop matching as soon
    as the patterns were anchored, and the gate reported build output as an
    unsanctioned root directory.
    """
    monkeypatch.setattr(
        compliance.subprocess, "run",
        lambda *a, **k: (_ for _ in ()).throw(OSError("no git here")),
    )
    for pattern in ("/site/", "site/", "site"):
        (minimal.root / ".gitignore").write_text(f"{pattern}\n", encoding="utf-8")
        (minimal.root / "site").mkdir(exist_ok=True)
        violations = compliance.check_root(minimal)
        assert not any("site" in v.path for v in violations), (
            f"pattern {pattern!r} was not honoured without git"
        )


def test_an_overlong_vendor_stub_is_caught(minimal):
    (minimal.root / "CLAUDE.md").write_text(
        "See AGENTS.md\n\nline\nline\nline\nline\n", encoding="utf-8")
    violations = compliance.check_vendor_stubs(minimal)
    assert any("exceeds 3 lines" in v.message for v in violations)


def test_a_stub_that_does_not_point_home_is_caught(minimal):
    (minimal.root / "GEMINI.md").write_text("Do whatever.\n", encoding="utf-8")
    violations = compliance.check_vendor_stubs(minimal)
    assert any("AGENTS.md" in v.message for v in violations)


def test_a_readme_without_a_hero_is_caught(minimal):
    (minimal.root / "README.md").write_text(
        "# x\n\n## What & Why\n## Quickstart\n## Documentation\n## Status\n", encoding="utf-8")
    violations = compliance.check_readme(minimal)
    assert any("hero visual" in v.message for v in violations)


def test_drifted_forge_metadata_is_caught(minimal):
    (minimal.forge).mkdir(parents=True, exist_ok=True)
    (minimal.forge / "settings.yml").write_text(
        'repository:\n  description: "something else entirely"\n', encoding="utf-8")
    violations = compliance.check_forge_metadata(minimal)
    assert any("drifts" in v.message for v in violations)


def test_violations_carry_a_rule_and_render_readably(minimal):
    (minimal.root / "stray.md").write_text("x", encoding="utf-8")
    violation = compliance.check_root(minimal)[0]
    assert violation.rule
    assert violation.path in violation.render()
    assert violation.as_dict()["rule"] == violation.rule
