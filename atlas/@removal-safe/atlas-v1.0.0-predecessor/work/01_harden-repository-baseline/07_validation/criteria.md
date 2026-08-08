# Acceptance criteria: 01 Harden the repository into a canonical v0.0.1 baseline

The workstream is `done` when every criterion below has evidence in
[`evidence.md`](evidence.md). Criteria are written before the work, not after.

| ID | Criterion | How it will be checked |
|---|---|---|
| C-01 | The full suite, the compliance script, and the site build all pass | `pytest`, `atlas check`, `atlas site build` |
| C-02 | No factual claim in the documentation contradicts the repository | Counted against the filesystem, one assertion per claim |
| C-03 | No artifact is maintained by hand in two places | `atlas template check` green; no byte-identical pairs remain |
| C-04 | Every specification carries machine-readable metadata and one `h1` | `tests/test_spec_metadata.py` |
| C-05 | Every rule-identifier namespace in use is registered and documented | `tests/test_spec_metadata.py::test_rule_namespaces_are_registered` |
| C-06 | `work/` contains only real records; no fabricated demonstration data | Manual read of `work/index.yaml` |
| C-07 | Everything removed is recoverable and its removal is explained | `@removal-safe/REMOVAL-INDEX.md` lists every file with a SHA-256 |
