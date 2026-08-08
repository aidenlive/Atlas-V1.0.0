# 0006: `library/` generalizes `prompts/`

- **Status:** accepted
- **Date:** 2026-08-07
- **Supersedes:** nothing. **Amends:** [ADR-0002](0002-sanctioned-root-extensions.md) (the sanctioned root set)

## Context

PROMPT-LIBRARY governed one kind of reusable artifact: the request prompt. In
practice a fleet reuses more than sentences. Icons get redrawn slightly
differently in each repository. Font files are emailed around with no license
beside them. Screenshots are committed with no record of what produced them, so
the next person cannot edit them and redraws instead.

Each of those is the same failure the prompt catalog already solved: a thing
authored once, used many times, with no single home, no index, and no review.

## Options

1. **A standard per asset kind.** ICONS, TYPEFACES, MEDIA alongside
   PROMPT-LIBRARY. Four specifications, four root directories.
2. **Generalize PROMPT-LIBRARY into LIBRARY.** One standard, one root directory,
   a closed set of classes inside it.
3. **Leave it.** Let each repository invent `assets/icons/` or `brand/` or
   `static/` as it needs them.

## Decision

Option 2. PROMPT-LIBRARY becomes **LIBRARY**; `prompts/` becomes
`library/prompts/` alongside `icons/`, `typefaces/`, and `media/`.

Option 1 multiplies the root (the thing the closed set exists to prevent) and
would restate the same six rules four times. What actually varies between an
icon and a prompt is narrow: how it is drawn, what license it needs, what counts
as its source. What is common is nearly all of it: one home, an index, a name
that describes the thing, recorded provenance, recorded license, review.

So the standard is one cross-class section (`L-A1`–`L-A6`) plus a short
class-specific section each. The rule that made prompts work is the rule that
makes the rest work; it did not need reinventing three times.

Option 3 is the status quo the suite exists to replace.

## Consequences

- **The root loses a directory rather than gaining three.** `prompts/` is
  retired from the sanctioned set and `library/` takes its place; ADR-0002's
  count is unchanged at four extensions.
- **The class set is closed.** A fifth class is added by amending
  `spec/library.md`, not by creating a folder. `tests/test_library.py` fails on
  an unregistered directory, which is what stops `library/` becoming a second
  downloads folder.
- **Rule identifiers changed.** `PL-01`–`PL-08` are now `L-01`–`L-08`, joined by
  `L-A`, `L-I`, `L-T`, and `L-M`. This invalidates existing citations, which is
  normally disqualifying. It is acceptable here only because the suite is
  pre-1.0 with no adopters. After v1.0 this would have required a major bump and
  an alias table.
- **The manifest contract moved** from `prompt-library/1.0` to `library/1.0`.
- `icons/`, `typefaces/`, and `media/` ship empty, with an index and a README.
  An empty class with a written contract is a place for the next asset to land;
  an absent class is an invitation to invent a folder.
