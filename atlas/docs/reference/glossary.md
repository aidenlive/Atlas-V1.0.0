---
title: Glossary
kind: reference
owner: role:editorial-lead
status: published
updated: 2026-08-08
review_by: 2026-11-08
audience: [internal, public]
summary: "Every term Atlas uses, in plain language, assuming no technical background."
---

# Glossary

Nothing here assumes you have read any code.

## The system

**Atlas** — the editorial system: eight standards, a lexicon, a prompt library,
and a command that checks writing against all of it.

**Standard** — one of the eight documents in `spec/`. Each answers one question
and numbers its requirements as rules.

**Rule** — one numbered requirement, such as `V-04`. The identifier is a
permanent address, so a review comment can cite it.

**Gate** — one automated check. `atlas check` runs fourteen of them over a
repository.

**Lint** — checking a single document rather than the whole repository.

## The files

**Manifest** — a small file of declared facts. `project.yaml` says what this
repository is; `authority.yaml` says who may approve what.

**Front matter** — the block at the top of a document, between two `---` lines,
declaring its title, kind, owner, status, and dates.

**Schema** — a machine-readable description of what a manifest may contain. It
turns a typo into a failed check.

**Lexicon** — the file that records how we spell our names and which phrasings
we have decided against.

## The work

**Workstream** — one editorial initiative, as a numbered folder with five fixed
sections.

**Brief** — the short document written before drafting: what, who, why now, and
the one takeaway.

**Profile** — a readiness level. Draft, Review, or Published, each a short list
of things that are true or not.

**Approver** — a role that may accept content for publication. Never the author
alone.

## The tooling

**CLI** — command-line interface. A program you run by typing its name.

**Exit code** — the number a command returns so a script can tell what happened:
`0` fine, `1` violations, `2` bad usage, `3` not found, `4` not a repository.

**Generated file** — a file a tool writes from another file. Editing one by hand
is always the wrong move, because the next run overwrites it.

**CI** — continuous integration. The service that runs the checks automatically
when someone proposes a change.
