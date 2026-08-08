---
title: The lexicon
kind: reference
owner: role:editorial-lead
status: published
updated: 2026-08-08
review_by: 2026-11-08
audience: [internal]
summary: "What the lexicon holds, how to read an entry, and how to propose a change to it."
---

# The lexicon

One file — [`library/lexicon/terms.yaml`](../../library/lexicon/terms.yaml) —
decides how we spell our names and which habits of writing we have decided
against. `atlas lint` reads it directly, so the answer it gives is the answer the
check will give.

## Two lists

**Terms** are the words that name our things. Each has one canonical form and a
list of forms that are the same word spelled another way.

```yaml
- id: front-matter
  use: front matter
  avoid: [frontmatter, front-matter]
  kind: concept
  severity: error
  note: "Two words, as in typesetting."
```

**Phrases** are habits of writing, each paired with what to write instead. An
entry without a replacement is a complaint, and fails a gate.

```yaml
- {avoid: in order to, use: to, reason: "the extra words carry nothing"}
```

## Severity

| Severity | Effect |
|---|---|
| `error` | Fails `atlas lint` and the repository check |
| `warn` | Reported; fails only under `--strict` |

Capitalisation of product names is usually `error`. Style preferences are
usually `warn`, because a writer may have a reason.

## Looking something up

```bash
atlas lexicon find email
atlas lexicon phrases
atlas lexicon list --kind product
```

## Proposing a change

Disagreeing with an entry is legitimate and cheap to act on. Change the line,
open a pull request, and say in one sentence which reader is better served. The
next `atlas lint` enforces the new decision everywhere.

> **Tip**
> The best source of new entries is your own review history. Anything you have
> corrected by hand twice belongs here.
