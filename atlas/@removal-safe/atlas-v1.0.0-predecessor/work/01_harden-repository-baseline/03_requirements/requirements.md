# Requirements: 01 Harden the repository into a canonical v0.0.1 baseline

Each requirement is testable and traceable to an acceptance criterion.

| ID | Requirement | Source | Criterion |
|---|---|---|---|
| R-01 | The repository must remain self-hosting: it passes its own standard at every commit | [ADR-0001](../../../docs/decisions/0001-self-hosting.md) | [C-01](../07_validation/criteria.md) |
| R-02 | Every fact has exactly one home; all other appearances are links or generated mirrors | `spec/project.md` §1 | [C-02](../07_validation/criteria.md), [C-03](../07_validation/criteria.md) |
| R-03 | Structural claims that can be counted must be checked, not asserted in prose | `spec/workstream.md` W-10 | [C-02](../07_validation/criteria.md) |
| R-04 | Every specification is machine-discoverable without parsing its prose | `spec/library.md` L-08 (same principle) | [C-04](../07_validation/criteria.md) |
| R-05 | A contributor who does not write code can find the rules that apply to them | `spec/presentation.md` P-06 | [C-04](../07_validation/criteria.md) |
| R-06 | Nothing is deleted without a recoverable copy and a written reason | `spec/project.md` §3 (git is the archive) | [C-07](../07_validation/criteria.md) |
| R-07 | `work/` records real work only | `spec/workstream.md` W-I5 | [C-06](../07_validation/criteria.md) |
