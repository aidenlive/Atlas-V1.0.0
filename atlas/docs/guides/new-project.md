---
title: Start a new content repository
kind: guide
owner: role:standards-maintainer
status: published
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, developers]
summary: "Scaffold a repository that already passes, then write the first piece."
---

# Start a new content repository

## Prerequisites

- The CLI installed — see [Install the CLI](install.md)
- A name in lower-case-with-hyphens, and someone to own it

## 1. Scaffold

```bash
atlas init brand-guidelines ../brand-guidelines --owner role:brand-lead
cd ../brand-guidelines
atlas check
```

`init` copies the starter, substitutes your facts, and then runs every gate
against what it produced. Scaffolding that produces a failing repository teaches
the wrong lesson on day one, so this passes before you touch it.

## 2. Replace the placeholders

Three files carry the facts that are still generic:

| File | Change |
|---|---|
| `project.yaml` | `kind`, `audiences`, `channels`, `visibility`, description |
| `authority.yaml` | Real principals and roles, and a second approver |
| `library/lexicon/terms.yaml` | The names this repository writes about |

> **Important**
> Add the second approver before anything is published. AUTHORITY A-04: the
> author is never the sole approver, including the lead's own writing.

## 3. Open the first workstream

```bash
atlas work new launch-messaging --owner person:you
```

Write `01_brief/brief.md` before drafting. A draft without a brief is a guess.

## 4. Write, check, publish

```bash
atlas lint content/ --strict
atlas check
atlas work sync
```

## What you get

- Every document declares its owner, kind, status, and review date
- One command that says whether the repository is in order
- A dashboard that counts progress from the task tables rather than trusting a
  status field

## Next

- [Running the work system](work-management.md)
- [Writing a document end to end](writing-a-document.md)
