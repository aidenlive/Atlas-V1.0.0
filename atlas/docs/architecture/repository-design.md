---
title: How the pieces fit
kind: explainer
owner: role:standards-maintainer
status: published
updated: 2026-08-08
review_by: 2027-08-08
audience: [internal, developers]
summary: "Why the standards, the schemas, the library, and the tooling are shaped the way they are."
---

# How the pieces fit

## The shape

```text
spec/          the product: eight standards + JSON Schemas
src/atlas/     the tooling: core library, then a CLI on top of it
library/       shared assets: the lexicon and the prompt library
work/          every initiative as a numbered workstream + generated dashboard
template/      a starter repository that passes what it teaches
docs/          guides, reference, architecture, decisions
examples/      worked manifests, validated in CI
tests/         schema, consistency, CLI, linter, and template checks
scripts/       thin wrappers and generators
assets/        badges and banners, generated from the manifest
```

## Prose and schema, kept in step

The prose in `spec/` is the standard. The JSON Schemas beside it encode the part
a machine can check. Both describe the same contract, so a value added to one
must be added to the other. A consistency test compares them, because two
sources of truth that nobody compares are only two sources.

## Declared, then checked

Every repository states its own facts in manifests: `project.yaml` for what it
is, `authority.yaml` for who may act, front matter for each document. Nothing is
inferred from directory names or file counts. Declaration makes the facts
reviewable in a diff; checking makes them true.

## Library first, CLI second

Everything the CLI does can be imported from `atlas.core` with no terminal
involved. One body of code therefore serves the command line, the test suite,
CI, and anything built on top. The CLI is a presentation layer over a library,
rather than a program with functions hidden inside it.

## Generated views cannot outrun their source

Four artefacts are generated, and none of them is edited by hand:

| Artefact | Generated from |
|---|---|
| `docs/reference/cli.md` | The argument parser |
| `library/prompts/index.yaml` | The prompt files |
| `work/README.md`, `work/index.yaml` | The task tables |
| `assets/badges/*.svg` | `project.yaml` and the design tokens |

A badge cannot claim something the manifest no longer says. A dashboard cannot
report progress the task table does not show. This is the same idea as
declaration, applied to the outputs.

## The archive

`@removal-safe/` holds the predecessor repository, complete and unmodified. It
is excluded from every walk the tooling makes, and it is temporary — see
[ADR-0005](../decisions/0005-archive-then-rebuild.md) for the scope and the
removal date.

## Related

- [Why the CLI is shaped this way](cli-design.md)
- [Decision records](../decisions/0001-eight-standards.md)
