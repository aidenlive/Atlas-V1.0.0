# Tasks: 01 Harden the repository into a canonical v0.0.1 baseline

Canonical tracker. `atlas work sync` counts these rows into the dashboard,
so the table shape matters: `T-NN` ids, one owner per non-todo task, evidence
on every `done` (W-12, W-13).

Status values: `todo · active · blocked · done · dropped`

| ID | Task | Owner | Status | Evidence |
|---|---|---|---|---|
| T-01 | Inventory every file; run the test suite, compliance script, and site build to establish a working baseline | agent:auditor | done | [`05_research/2026-08-07-baseline-inventory.md`](../05_research/2026-08-07-baseline-inventory.md) |
| T-02 | Identify every fact stated in more than one place and every claim contradicted elsewhere | agent:auditor | done | [`05_research/2026-08-07-drift-register.md`](../05_research/2026-08-07-drift-register.md) |
| T-03 | Single-source `template/` on the canonical artifacts; add a drift check | agent:auditor | done | `atlas template check` green in CI |
| T-04 | Split the vendored design system into consumed tokens and archived narrative | agent:auditor | done | `assets/design/tokens.yaml`; site builds |
| T-05 | Correct every propagated count and cross-reference error | agent:auditor | done | [`07_validation/evidence.md`](../07_validation/evidence.md) C-02 |
| T-06 | Give every specification machine-readable front matter and a single heading tree | agent:auditor | done | `tests/test_spec_metadata.py` |
| T-07 | Publish the conventions and glossary a non-specialist can start from | agent:auditor | done | `docs/reference/conventions.md`, `docs/reference/glossary.md` |
| T-08 | Remove dead code and stop sanctioning build output as repository structure | agent:auditor | done | `atlas check` reads `.gitignore` |
| T-09 | Move stale, duplicate, and experimental material to `@removal-safe` with a removal index | agent:auditor | done | `@removal-safe/REMOVAL-INDEX.md` |
