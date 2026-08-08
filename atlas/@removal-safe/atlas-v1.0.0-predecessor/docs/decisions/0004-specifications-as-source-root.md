# 0004: `spec/` is the source root; schemas live inside it

Date: 2026-08-07 · Status: Accepted

## Context
`spec/project.md` requires one source root: `src/` or the ecosystem's
idiomatic equivalent. For a `content.spec` project the product is prose, and
its consumers cite it; `src/` would be a misnomer that helps no reader.
Separately, the JSON Schemas could plausibly live beside the tooling that
consumes them.

## Decision
`spec/` is this repository's declared source root. `spec/schemas/` lives
inside it because the schemas are normative artifacts of the same product:
they encode the enums the prose defines, are versioned with it, and are
consumed by third parties directly.

## Consequences
"Where is the product?" has one answer. Schema and prose change together in
one directory and one review, and `tests/test_spec_consistency.py` fails if
they diverge. Tooling in `scripts/` references schemas by path, keeping the
dependency one-directional: tools depend on the spec, never the reverse.
