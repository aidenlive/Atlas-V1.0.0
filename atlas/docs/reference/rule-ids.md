---
title: How to cite a rule
kind: reference
owner: role:standards-maintainer
status: published
updated: 2026-08-08
review_by: 2026-11-08
audience: [internal]
summary: "Rule identifiers, what makes them stable, and how to use one in a review comment."
---

# How to cite a rule

## The shape

A rule identifier is a prefix and two digits: `V-04`, `S-07`, `A-10`. The prefix
belongs to exactly one standard, and the number never changes once published.

| Prefix | Standard |
|---|---|
| `V-` | VOICE |
| `L-` | LANGUAGE |
| `S-` | STRUCTURE |
| `C-` | CONTENT |
| `M-` | MATRIX |
| `Q-` | CHECKLIST |
| `A-` | AUTHORITY |
| `P-` | PUBLICATION |

## Why they are gapless

Each standard numbers its rules from `01`, with no gaps and no repeats, and a
gate enforces it. A gap means a rule was deleted, which would silently
invalidate every review comment and commit message that cited it. Retiring a
rule therefore means renumbering deliberately and saying so in the changelog.

## Citing one

In a review comment, name the rule and quote the sentence:

> The second paragraph makes a claim with no number behind it (`V-05`).

In a commit message, put it at the end of the line:

```text
Shorten the install steps and cut the hedging (V-04, V-07)
```

## Looking one up

```bash
atlas spec rules --grep evidence
atlas spec show voice --rules
```

## Rules the tooling enforces

Not every rule is machine-checkable, and pretending otherwise would be worse
than useless. The gates enforce the mechanical subset; run `atlas check --list`
and `atlas lint --list` to see exactly which. Everything else is a reviewer's
judgement, and is meant to be.
