# Drift register: 2026-08-07

Every fact found stated in more than one place, or stated once and contradicted
elsewhere. Each row was re-derived from the filesystem rather than from any
document that asserted it.

## Contradicted counts

| Claim | Stated in | Reality | Resolution |
|---|---|---|---|
| "ten-section skeleton" | `README.md`, `AGENTS.md`, `CHANGELOG.md`, `docs/reference/quick-reference.md`, `docs/guides/work-management.md`, `docs/decisions/0005`, `template/work/README.md`, and a docstring in `tests/test_workstreams.py` | Nine numbered sections, `01_plan` … `09_issues`, plus `README.md` and `workstream.yaml` | Corrected to "nine numbered sections" everywhere; the accompanying prose lists had nine items all along |
| "seven specs" | `README.md` architecture alt text | Eight | Corrected; the SVG's own `aria-label` already said eight |
| "one of the five standards" | `.github/ISSUE_TEMPLATE/spec-change.md` | Eight | Corrected, and the count removed so it cannot rot again |
| "61 checks" | `CHANGELOG.md` | 63 | Test counts removed from prose entirely — a number that changes on every new test does not belong in a document |

## Duplicated artifacts

| Artifact | Copies | Divergence found |
|---|---|---|
| `work/_template/` | `work/` and `template/work/` | Byte-identical, but nothing prevented divergence |
| `workstream.schema.json` | `spec/schemas/` and `template/work/` | Byte-identical |
| `work.py` | `scripts/` and `template/scripts/` | **Already diverged.** The template copy carried a dual schema-path resolver the root copy lacked, so the scaffold was strictly ahead of the standard it came from |

Resolved by `atlas template sync`: one direction of flow, 18 generated
files, `--check` in CI. The divergence itself was the right code and was
promoted into the canonical `atlas work`.

## Duplicated prose

The eight-standards table appears in `README.md`, `AGENTS.md`, and
`docs/reference/quick-reference.md`. This is a deliberate mirror rather than an
accident: the landing page must answer "what is this" without a click (P-06) —
so it is now enforced by `tests/test_spec_metadata.py` instead of trusted.

## Fabricated records

All four workstreams described migrating an imaginary fleet, staffed by
`person:maintainer`, `agent:planner`, `agent:surveyor`, `agent:migrator`,
`agent:scribe`, and `agent:auditor`. The generated dashboard reported them as
live work, and every repository scaffolded from `template/` would have inherited
that claim. Archived; `work/` now holds one real record.

## Dead and misleading code

| Location | Finding |
|---|---|
| `atlas validate` | `SCHEMA_BY_STANDARD` defined, never read, and contradicted by the function immediately below it |
| `atlas validate` | Admin schemas dispatched on `path.name.startswith("org")` — filename as type system |
| `atlas init` | `mv "$dest/project.yaml" "$dest/project.yaml"` — a file moved onto itself |
| `atlas check` | `site/` and `.pytest_cache/` listed as *sanctioned root directories*, making build output part of the declared repository shape |

## Unstated conventions

Rule identifiers follow a consistent two-namespace pattern: normative rules in
one prefix, checklist items in another (`P-`/`PR-`, `W-`/`WS-`): that appears
nowhere in the documentation. Three specifications (`workspace`, `project`,
`project-matrix`) have no identifiers at all, so their rules cannot be cited in a
waiver, a review, or a checklist row. Registered and tested in v0.0.1;
numbering the unnumbered is deferred (I-02).
