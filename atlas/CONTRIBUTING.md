# Contributing

Two kinds of change, and they are not held to the same bar.

| Change | Needs |
|---|---|
| Editorial — wording, examples, formatting, a new prompt | One reviewer |
| Standard — a rule added, changed, or removed | The editorial lead and a standards maintainer |

## Before you open a pull request

```bash
scripts/atlas check
scripts/atlas lint --changed --strict
python -m pytest tests/ -q
```

## Changing a rule

A change to what the standard requires travels as one change-set (AUTHORITY
A-05):

1. The prose in `spec/`.
2. The schema beside it, if the change is machine-checkable.
3. The standard version in `project.yaml`, if the contract moved.
4. A `CHANGELOG.md` entry naming the rule and what to do about it.

Rules are numbered without gaps. Removing one means renumbering deliberately and
saying so, because a rule identifier is a permanent address that review comments
and commit messages already cite.

## Adding a lexicon entry

The best source is your own review history: anything you have corrected by hand
twice belongs in `library/lexicon/terms.yaml`. Say in one sentence which reader
is better served, and set `severity: warn` unless the entry is a product name.

## Adding a prompt

One request, four sentences at most, one paragraph. Anything that changes files
proposes a plan first. Then:

```bash
python scripts/build_library.py
```

## Generated files

Never edit these by hand; the next run overwrites them, and a gate will notice:

- `docs/reference/cli.md`
- `library/prompts/index.yaml`
- `work/README.md` and `work/index.yaml`
- `assets/badges/*.svg` and `assets/banner-*.svg`

## Commit messages

One line, present tense, with any rule identifiers at the end:

```text
Shorten the install steps and cut the hedging (V-04, V-07)
```
