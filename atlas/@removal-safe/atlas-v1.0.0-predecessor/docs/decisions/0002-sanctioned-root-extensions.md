# 0002: `template/` as a sanctioned root extension

Date: 2026-08-07 · Status: Accepted

## Context
`spec/project.md` §9 defines a closed root set. Most of what this repository
keeps at the root is already in that set: `spec/` (the source root, ADR-0004),
`docs/`, `tests/`, `scripts/`, `assets/`, and the conditional roots `work/` and
`library/prompts/` defined by the workstream and library standards. One surface
is not: `template/`, the starter repository consumers copy. Burying it under
`examples/` or `scripts/` would misclassify a product as a sample and break the
"Use this template" flow that depends on a stable path.

## Decision
`template/` is added to this repository's closed set, via exactly the mechanism
the standard prescribes: new needs "trigger a deliberate standard revision —
never an ad-hoc root entry." This ADR is that revision, scoped to this
repository. `atlas check` carries the allow-list, so anything
else at the root still fails.

## Consequences
The closed set stays closed and mechanically enforced, with exactly one named,
reviewable, revertible exception. If a future suite version standardizes a
scaffold location, this ADR is superseded rather than edited.
