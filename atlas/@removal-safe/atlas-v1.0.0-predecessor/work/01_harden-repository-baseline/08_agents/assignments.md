# Agent assignments: 01 Harden the repository into a canonical v0.0.1 baseline

At most one orchestrator (W-15). Every assignment states concrete scope —
paths or task IDs, because an agent with no written scope has unbounded scope
(W-14). Authority comes from `admin.yaml`; an assignment narrows it and never
widens it (W-18).

| Agent | Role | Scope | Definition of done | Expires |
|---|---|---|---|---|
| agent:auditor | orchestrator | Whole repository. May edit `spec/` packaging (front matter, headings, cross-references) but not normative sentences; may edit `docs/`, `scripts/`, `tests/`, `template/`, `examples/`, `.github/` freely. | Every criterion in `07_validation/criteria.md` carries evidence, and `pytest` plus `check-compliance.sh` are green. | 2026-12-31 |
