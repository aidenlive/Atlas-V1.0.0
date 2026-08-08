# Evidence: 01 Harden the repository into a canonical v0.0.1 baseline

One row per criterion: how it was checked, by whom, when, and the result.
An unattributed checkmark is not evidence (W-08).

| Criterion | Check performed | By | Date | Result |
|---|---|---|---|---|
| C-01 | `pytest tests/ -q`, `atlas check`, `atlas site build` run from a clean checkout | agent:auditor | 2026-08-07 | pass |
| C-02 | Every numeric and cross-reference claim re-derived from the filesystem; 4 distinct propagated errors corrected across 11 files | agent:auditor | 2026-08-07 | pass |
| C-03 | `sync-template.py --check`; 18 previously hand-maintained files now generated | agent:auditor | 2026-08-07 | pass |
| C-04 | `pytest tests/test_spec_metadata.py -q` over all 8 specifications | agent:auditor | 2026-08-07 | pass |
| C-05 | 12 namespaces registered in `docs/reference/rule-ids.md`; test asserts prose and registry agree | agent:auditor | 2026-08-07 | pass |
| C-06 | `work/index.yaml` read; 1 workstream, this one, describing work actually performed | agent:auditor | 2026-08-07 | pass |
| C-07 | `@removal-safe/REMOVAL-INDEX.md` reviewed; 89 archived files each carry origin path, size, date, and SHA-256 | agent:auditor | 2026-08-07 | pass |
