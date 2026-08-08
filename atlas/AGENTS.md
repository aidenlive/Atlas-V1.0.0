# Agent guide

This is the canonical instruction file for AI agents working in this repository.
`CLAUDE.md` and `GEMINI.md` are stubs that point here: vendors multiply, truth
must not.

## What this repository is

Atlas: eight standards for company writing, a lexicon, a prompt library, and the
tooling that checks all of it. The repository is self-hosting — it passes the
standard it defines — so any change you make must leave `atlas check` passing.

## Before you change anything

```bash
scripts/atlas check
scripts/atlas lint --changed --strict
python -m pytest tests/ -q
```

## Rules that apply to you specifically

- **You may draft, edit, and review. You may not approve.** AUTHORITY A-10:
  machines draft and check; people accept the risk.
- **Propose before you remove.** Deleting, overwriting, retiring, or migrating
  anything means proposing a plan and waiting for a person.
- **Never edit a generated file.** `docs/reference/cli.md`,
  `library/prompts/index.yaml`, `work/README.md`, `work/index.yaml`, and
  everything under `assets/` are derived. Change the source and re-run the
  script.
- **Terminology comes from `library/lexicon/terms.yaml`.** Do not invent a
  second spelling for anything.
- **Status lives in the task table** of the relevant workstream, and nowhere
  else.
- **`@removal-safe/` is off limits.** It is an archive of the predecessor
  repository, excluded from every check. Do not read from it for guidance, and
  do not copy anything out of it.

## Where things are

| Looking for | Path |
|---|---|
| The rules themselves | `spec/` |
| What a rule means in practice | `docs/guides/` |
| Definitions, in plain language | `docs/reference/glossary.md` |
| Naming and placement | `docs/reference/conventions.md` |
| Why something is the way it is | `docs/decisions/` |
| Work in progress | `work/` |

## Changing a rule

A rule change travels as one change-set: the prose in `spec/`, the schema beside
it, the standard version, and a changelog entry. Do not ship any part alone.

## Writing well here

Read [`spec/voice.md`](spec/voice.md) before drafting prose. The short version:
one voice, second person, active verbs, the shorter word, one idea per sentence,
claims carry evidence, and the hard thing goes first.
