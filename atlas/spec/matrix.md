---
id: matrix
order: 5
title: "MATRIX: what kind of content is this?"
tagline: "What kind of content this is, and what that kind requires"
question: "What kind of content is this, and what does that require?"
version: "1.0"
status: published
stability: stable
rule_prefix: "M-"
companions: [content, checklist, voice, publication]
kind: standard
owner: role:editorial-lead
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, leadership]
summary: "Ten kinds of content, each with a declared purpose, shape, tone, owner, and review cadence."
---

# MATRIX: what kind of content is this?

> "Make it good" is not a standard. "This is a guide, so it opens with
> prerequisites, uses numbered steps, and is re-read every six months" is.

## What this is

Most disagreements about a draft are disagreements about what it is. One
person is editing a reference; the other is writing an explainer. MATRIX removes
that argument by naming the kinds, and by attaching requirements to each.

Every document declares its kind in front matter. The kind then decides its
shape, its tone, who owns it, and how often it is re-read.

## The kinds

| Kind | Answers | Shape | Tone | Review |
|---|---|---|---|---|
| `standard` | What must be true? | Numbered rules with prefixes | Neutral, normative | 6 months |
| `guide` | How do I do this? | Prerequisites, numbered steps, verification | Instructive | 6 months |
| `reference` | What are the exact details? | Tables and lists, generated where possible | Terse, complete | 3 months |
| `explainer` | Why does this work this way? | Prose with diagrams | Conversational | 12 months |
| `decision` | What did we decide, and why? | Context, decision, consequences | Factual, dated | Never — decisions are immutable |
| `announcement` | What changed? | What, who is affected, what to do | Confident, plain | Never — announcements are dated |
| `policy` | What are the rules for people? | Scope, rules, exceptions, escalation | Precise, unhedged | 12 months |
| `template` | How do I start one of these? | Skeleton with placeholders | Instructive | 12 months |
| `brief` | What are we about to write? | Audience, goal, message, constraints | Direct | Closed with its workstream |
| `note` | Everything else worth keeping | Free | Free | 12 months |

## Audience

Kind decides the shape; audience decides the assumptions. Both are declared,
because a guide for developers and a guide for customers are not the same
document with different words:

| Audience | Assume | Never assume |
|---|---|---|
| `internal` | Shared context, shared vocabulary | That new hires have either |
| `leadership` | Time pressure, decision framing | Familiarity with implementation |
| `customers` | Motivation, not expertise | That they have read anything else |
| `partners` | Commercial context | Access to internal systems |
| `developers` | Technical fluency | Knowledge of our specific choices |
| `press` | No context at all | Good faith or careful reading |
| `public` | Nothing | Anything |

## The rules

- **M-01 Kind is declared, not inferred.** Every document names its kind in
  front matter. A document that cannot be assigned one is usually two documents.
- **M-02 Kind sets the shape.** The table above is normative. A `guide` without
  prerequisites and verification steps is incomplete, however well written.
- **M-03 Audience is declared.** Every document names who it is for, and is
  edited against that reader rather than against a general one.
- **M-04 One kind per document.** A reference that turns into a tutorial halfway
  down serves neither reader. Split it and link the two.
- **M-05 Review cadence follows kind.** `review_by` is set from the table above
  when the document is published, not left blank until someone notices.
- **M-06 Immutable kinds are never edited in place.** A `decision` or an
  `announcement` is a dated record. Correct one by publishing a new one that
  supersedes it, so the history stays readable.

## Related

- [CONTENT](content.md) — the facts every document declares
- [CHECKLIST](checklist.md) — the readiness profiles each kind must pass
- [VOICE](voice.md) — the tone each situation takes
