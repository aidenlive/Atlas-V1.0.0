---
id: content
order: 4
title: "CONTENT: what must be true of a piece of content"
tagline: "What must be true of a piece of content, and of the repository holding it"
question: "What must be true of a piece of content?"
version: "1.0"
status: published
stability: stable
rule_prefix: "C-"
companions: [structure, matrix, authority, publication]
kind: standard
owner: role:editorial-lead
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, developers]
summary: "Every document declares its own facts; the repository around it stays a closed, legible set."
---

# CONTENT: what must be true of a piece of content

> A document that does not say who owns it and when it was last checked is not
> content. It is a rumour with formatting.

## What this is

VOICE, LANGUAGE, and STRUCTURE govern the writing. CONTENT governs everything
around it: the facts a document declares about itself, and the shape of the
repository those documents live in.

The bet is the same one the rest of the suite makes: **a fact stored beside the
thing it describes gets updated in the same edit.** Ownership in a spreadsheet
goes stale in a month. Ownership in the file's front matter changes in the same
pull request that changes the file.

## Front matter

Every published document opens with a YAML block. Five fields are required, the
rest are useful:

```yaml
---
title: Set up two-factor authentication
kind: guide                 # see MATRIX
owner: role:security-lead   # who answers for it
status: published           # draft | review | published | superseded | retired
updated: 2026-08-08
review_by: 2027-02-08       # when someone must read it again
audience: [customers]
reviewers: [person:dana]
summary: "Turn on 2FA, and what changes for your team when you do."
---
```

The block is validated against
[`spec/schemas/content.schema.json`](schemas/content.schema.json), so a typo in
`status` fails a check rather than quietly creating a sixth state.

## The rules

- **C-01 Every document declares itself.** Front matter with `title`, `kind`,
  `owner`, `status`, and `updated` is required on every Markdown file under
  `docs/`, `spec/`, and `content/`.
- **C-02 The root is a closed set.** Only sanctioned files and directories sit
  at the repository root. The root is the first screen a reader and an agent
  both see; anything else belongs in a directory.
- **C-03 Standards declare their metadata.** Every file in `spec/` declares its
  `id`, `order`, `title`, `question`, `version`, `status`, and `rule_prefix`, so
  a tool can discover the suite without reading the prose.
- **C-04 Rule identifiers are unique and sequential.** Each standard numbers its
  rules with its own prefix, from `01`, with no gaps and no repeats. A rule id
  is a permanent address; two documents cannot share one.
- **C-05 Nothing outlives its review date.** A document with a `review_by` in
  the past fails the check. Re-read it, then move the date, supersede it, or
  retire it.
- **C-06 The template passes what it teaches.** The starter under `template/`
  satisfies every rule a scaffolded repository is asked to satisfy. Scaffolding
  that produces a failing repository teaches the wrong lesson on day one.
- **C-07 Shared assets live in the library.** Prompts, lexicon, and content
  templates live under `library/`, one canonical copy each, referenced by path
  rather than pasted.
- **C-08 One prompt, one request.** A library prompt asks for exactly one thing,
  in no more than four sentences and one paragraph. Longer than that is a brief,
  and briefs live in `work/`.
- **C-09 Destructive prompts propose first.** Any prompt that changes files
  rather than producing text — deleting, overwriting, archiving, retiring,
  migrating — must ask for a plan before it acts, so the reply is a change to
  approve rather than a change to discover.

## Lifecycle

Content states are the same five everywhere, and they are declared, not implied:

| Status | Means | Who may move it on |
|---|---|---|
| `draft` | Being written; nobody should rely on it | The author |
| `review` | Complete, awaiting sign-off | A reviewer named in AUTHORITY |
| `published` | Current and relied upon | An approver |
| `superseded` | Replaced; kept for context, with `supersedes` filled in | An approver |
| `retired` | No longer true; removed from navigation | An approver |

> **Warning**
> `retired` means the document leaves the reader's path. It does not mean the
> file is deleted in secret. Version control is the archive; a removal is a
> commit with a reason and a changelog entry.

## Related

- [MATRIX](matrix.md) — what each kind of content requires
- [AUTHORITY](authority.md) — who may move content between states
- [CHECKLIST](checklist.md) — the gates before `published`
