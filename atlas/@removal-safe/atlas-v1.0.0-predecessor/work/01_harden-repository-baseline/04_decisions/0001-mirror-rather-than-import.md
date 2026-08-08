# 0001: Mirror the template, do not make it import

- **Status:** accepted
- **Date:** 2026-08-07
- **Scope:** this workstream

## Context

`template/` duplicated three artifacts the repository already owned, and one of
them had drifted. The duplication had to go.

## Options

1. **Import.** Make `template/` reference `../atlas work` and
   `../spec/schemas/`. Zero duplication.
2. **Mirror.** Keep real files in `template/`, generate them from the canonical
   sources, and fail CI when they drift.
3. **Leave it.** Document the duplication and rely on review.

## Decision

Mirror.

Option 1 is the cleanest in this repository and useless in every other one.
`template/` exists to be *copied out*: the moment it leaves, a relative path to
`../spec/` points at nothing. A template whose files only work in the repository
that ships it is not a template.

Option 3 is what produced the drift being fixed.

## Consequences

- `template/` contains real, standalone, copyable files.
- Those files are read-only in practice: edit the canonical source, then run
  `atlas template sync`.
- Drift is a red build (`--check` runs in `check-compliance.sh` and CI), not a
  discovery made months later inside somebody else's repository.
- `atlas work` resolves its schema from either location, which is why one
  file can serve both homes.
