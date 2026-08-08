"""The suite passes the standard it defines."""

from __future__ import annotations

from atlas.core import compliance


def test_every_gate_passes(repo):
    report = compliance.run(repo)
    assert report.ok, "\n".join(str(v) for v in report.violations)


def test_no_gate_is_skipped_in_the_standards_repository(repo):
    report = compliance.run(repo)
    assert report.skipped == 0


def test_gates_are_pure(repo):
    """Running the gates twice changes nothing on disk."""
    before = sorted(p.stat().st_mtime_ns for p in repo.root.rglob("*.md"))
    compliance.run(repo)
    after = sorted(p.stat().st_mtime_ns for p in repo.root.rglob("*.md"))
    assert before == after


def test_a_broken_gate_is_reported_not_raised(repo, monkeypatch):
    def explode(_repo):
        raise RuntimeError("boom")

    monkeypatch.setitem(
        compliance.CHECKS,
        "manifest-valid",
        compliance.Check("manifest-valid", "x", "C-01", explode),
    )
    report = compliance.run(repo, only=["manifest-valid"])
    assert not report.ok
    assert "boom" in report.violations[0].message
