---
title: Adopt the standard in an existing repository
kind: guide
owner: role:standards-maintainer
status: published
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, leadership]
summary: "Two passes: declare ownership everywhere first, fix the writing second."
---

# Adopt the standard in an existing repository

The blocking question is never agreement. It is what to do with four hundred
existing pages. The answer is that you do not rewrite them.

## The two passes

| Pass | Effort | Buys you |
|---|---|---|
| 1. Declare | An afternoon | Every document has an owner, a kind, and a review date |
| 2. Improve | Ongoing | The writing itself meets VOICE, LANGUAGE, and STRUCTURE |

Pass 1 is mechanical and worth doing on everything. Pass 2 happens document by
document, as each one is edited anyway.

## Pass 1: declare

1. Add `project.yaml` and `authority.yaml`. Copy them from `template/`.
2. Add front matter to every document: `title`, `kind`, `owner`, `status`,
   `updated`. Set `status: published` for what people already rely on.
3. Set `review_by` from the cadence for each kind. Stagger the dates, or you
   will get one enormous review week in six months.
4. Run `atlas check` and fix what it reports.

At the end of pass 1, nothing reads better and everything is accounted for. That
is the point: you now know what you have.

## Pass 2: improve

Do not schedule a rewrite. Instead:

- Fix a document when you are already editing it
- Fix a document when its review date arrives
- Fix the ten documents your audience actually reads, first

```bash
atlas lint docs/ --strict
```

Work down the errors before the warnings. Errors are rule violations; warnings
are judgement calls where a person still decides.

## Adopting the lexicon

Start the lexicon with the arguments you have already had. Every term someone
has corrected twice in review belongs in `library/lexicon/terms.yaml`, so it is
never corrected by hand again.

> **Warning**
> Do not import a 400-term style guide on day one. A lexicon nobody agreed to
> produces a wall of failures and gets switched off.

## Common objections

| Objection | Answer |
|---|---|
| "Our writers will not use a CLI." | They do not have to. CI runs it; writers read the report. |
| "Front matter clutters the file." | Five lines, and it is the only reason ownership survives a reorganisation. |
| "We do not have owners for all of this." | Then you have found the real problem, and it was true before the standard. |

## Next

- [Running the work system](work-management.md)
- [How the pieces fit](../architecture/repository-design.md)
