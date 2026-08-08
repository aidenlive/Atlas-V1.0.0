# Contributing

You do not need to write code to contribute here. Most of this repository is
prose, and most of what makes it good is people noticing that a sentence is
wrong.

## Start here

| If you want to… | Do this |
|---|---|
| Fix a typo or an unclear sentence | Open a pull request. That is the whole process. |
| Report something that seems wrong | Open an issue. You do not need to propose a fix. |
| Understand a term | [`docs/reference/glossary.md`](docs/reference/glossary.md) |
| Know how to name or place something | [`docs/reference/conventions.md`](docs/reference/conventions.md) |
| Change what compliance *means* | Read "Normative changes" below first. |

If a document confused you, that is a defect in the document. Saying so is a
contribution, and "I didn't understand this paragraph" is a complete and useful
issue.

## The two kinds of change

**1. Editorial.** Typos, clarity, examples, tooling, tests, formatting.

Branch, open a pull request, get CI green, one review, squash-merge. These
merge freely.

**2. Normative.** Anything that changes what compliance *means*: a rule, an
enum value, an invariant, a checklist item, a schema constraint.

Open an issue first, so the discussion happens before the diff. Then open a pull
request that updates, in one change-set:

- the specification prose,
- the matching JSON Schema in `spec/schemas/`,
- the `version:` field in that specification's front matter,
- an entry in `CHANGELOG.md`.

CI enforces the schema half. Normative changes bump the suite MINOR at minimum,
and MAJOR if any previously compliant repository becomes non-compliant. New enum
values follow the Matrix extension policy (`x-` prefix until standardized). See
[`docs/reference/versioning.md`](docs/reference/versioning.md).

## Workflow

```
branch (type/short-desc) → PR → CI green → review → squash-merge
```

- Commits follow [Conventional Commits](https://www.conventionalcommits.org):
  `feat | fix | docs | chore | spec | test | ci | refactor`. `spec:` marks a
  normative change.
- Every pull request that changes behaviour or normative text adds a
  `CHANGELOG.md` entry under `Unreleased`.
- Decisions about the *shape* of this repository, or the standard's direction,
  get an ADR at `docs/decisions/NNNN-short-title.md`. Accepted ADRs are
  immutable: supersede, never edit.

## Two things that will fail CI

**Editing a generated file.** Several files here are written by scripts, and
editing one is always a mistake: your change survives until the next sync. The
full list is in
[`conventions.md`](docs/reference/conventions.md#generated-files). It includes
`work/README.md`, `work/index.yaml`, everything under `library/prompts/`, and three
files under `template/`. Edit the source and run the generator.

**Putting an unchecked count in prose.** "78 prompts" is fine because a test
counts them. "61 tests" is not, because nothing did, and it was wrong for
months. If you want to state a number, add the assertion that keeps it true.

## Local verification

```bash
pip install -r scripts/requirements.txt
python -m pytest tests/ -q && atlas check
```

Both should be green before you open a pull request. If `check-compliance.sh`
tells you the template mirror is stale, run `atlas template sync`.

## Releasing

1. Move `Unreleased` entries under a new version heading and set the date.
2. Update the release badge in `README.md`.
3. Update `version:` in the front matter of any specification whose normative
   text changed.
4. Tag `vX.Y.Z`. The tag is the source of truth for what shipped.
