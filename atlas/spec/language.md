---
id: language
order: 2
title: "LANGUAGE: words, names, and mechanics"
tagline: "Words, names, spellings, and mechanics, decided once"
question: "Which words, names, and mechanics do we use?"
version: "1.0"
status: published
stability: stable
rule_prefix: "L-"
companions: [voice, structure, publication]
kind: standard
owner: role:editorial-lead
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, developers]
summary: "One spelling per name, one convention per mechanic, and one file that decides both."
---

# LANGUAGE: words, names, and mechanics

> Two spellings of the same product name is not a style disagreement. It is two
> products, as far as search, a new hire, and an agent are concerned.

## What this is

VOICE governs how we sound. LANGUAGE governs the smaller decisions underneath
it: what we call things, how we spell them, how we punctuate, and which of the
several defensible conventions we picked so nobody has to pick again.

Most of this standard is enforced from data rather than prose. The canonical
spellings live in [`library/lexicon/terms.yaml`](../library/lexicon/terms.yaml),
and `atlas lint` reads that file directly, so adding a house term is a one-line
change that every check picks up.

## The rules

- **L-01 One spelling per name.** Every product, feature, role, and system has
  exactly one written form, recorded in the lexicon. Alternatives are listed
  under `avoid` so they fail a check rather than an argument.
- **L-02 Every avoidance has a replacement.** A lexicon entry that forbids a
  phrase must say what to write instead. A rule without a remedy is a complaint.
- **L-03 One term per concept.** Within a document, one idea keeps one name.
  Calling it a *check*, then a *gate*, then a *validation* in three paragraphs
  makes a reader wonder what the difference is, and there is none.
- **L-04 Sentence case in headings.** Headings, buttons, labels, and table
  headers capitalise the first word and any names, and nothing else.
  `Set up two-factor authentication`, not `Set Up Two-Factor Authentication`.
- **L-05 Serial comma.** `red, white, and blue`. It removes an ambiguity we
  cannot otherwise remove, and costs one character.
- **L-06 One space after a period.** Two is a typewriter artefact and shows up
  as a ragged gap in every proportional font we publish in.
- **L-07 ISO dates in data, long dates in prose.** `2026-08-08` in front matter,
  manifests, and tables; `8 August 2026` in a sentence. Never `08/08/26`, which
  means two different days on two continents.
- **L-08 Clean mechanics.** No trailing whitespace, no hard tabs, no
  double spaces, no smart quotes inside code. These are invisible until they are
  a diff full of noise.
- **L-09 Expand on first use.** Spell out an acronym the first time it appears
  in a document, with the acronym in parentheses, then use the acronym.
  Exceptions are terms in the lexicon marked as needing no expansion.
- **L-10 Plain, precise, inclusive.** Write about people the way they describe
  themselves; prefer `they` to a coin-flip `he`; avoid metaphors of violence,
  war, and hazing for ordinary work. Prefer `allowlist`, `main`, `primary` over
  the legacy terms they replace.

## Numbers, units, and code

| Thing | Convention | Example |
|---|---|---|
| Numbers under ten | Words in prose, digits in data | `three retries`, `retries: 3` |
| Large numbers | Digits with separators | `1,240 accounts` |
| Ranges | En dash, no spaces | `10–20 minutes` |
| Percentages | Digit and symbol | `12%` |
| Money | Symbol, then digits, currency where ambiguous | `$1,200 USD` |
| Units | Space between number and unit | `250 ms`, `4 GB` |
| Commands, paths, keys | Inline code | `atlas check`, `spec/voice.md` |
| Placeholders | Angle brackets in code | `atlas init <name>` |

## Words we have already decided

The full list is data, not prose — run `atlas lexicon list` or read
[`library/lexicon/terms.yaml`](../library/lexicon/terms.yaml). A sample of the
kinds of decision it records:

| Write | Not | Why |
|---|---|---|
| `Atlas` | `ATLAS`, `atlas` (as the product) | The product is a name; the command `atlas` is lower case |
| `front matter` | `frontmatter` | Two words, as in typesetting |
| `workstream` | `work stream` | One thing, one word |
| `changelog` | `change log` | The file is `CHANGELOG.md` |
| `GitHub` | `Github` | Their capitalisation, not ours |

> **Tip**
> Disagreeing with an entry is legitimate and cheap to act on: change the line,
> open a pull request, and the next `atlas lint` enforces the new decision.

## Related

- [VOICE](voice.md) — how the company sounds
- [STRUCTURE](structure.md) — the shape a document takes
- [PUBLICATION](publication.md) — metadata, titles, and channel conventions
