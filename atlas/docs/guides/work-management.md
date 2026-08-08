---
title: Running the work system
kind: guide
owner: role:editorial-lead
status: published
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal]
summary: "One numbered folder per initiative, five sections, and progress counted from the task table."
---

# Running the work system

Editorial work goes wrong in a predictable way: the plan is in one person's
head, the status is in a chat thread, and the draft is in an attachment. The
work system puts all three in the repository, next to the writing.

## The shape

Every initiative is one numbered folder under `work/`, with the same five
sections in the same order:

| Section | Holds |
|---|---|
| `01_brief` | What we are writing, for whom, and why |
| `02_tasks` | The task table — the only place status is recorded |
| `03_drafts` | Drafts in progress, or pointers to where they live |
| `04_review` | Reviewers, comments, and sign-off |
| `05_publication` | Where it went, and what happens next |

## Opening one

```bash
atlas work new rewrite-onboarding --owner person:you --kind guide --audience customers
```

Then write the brief. Everything downstream is cheaper when the brief is honest
about who the reader is.

## Tracking

Status lives in one table, in `02_tasks/tasks.md`. Four states, and no others:

| State | Means |
|---|---|
| `todo` | Not started |
| `doing` | Someone is on it now |
| `blocked` | Waiting on something named |
| `done` | Finished, and someone else could verify it |

```bash
atlas work list --status blocked
atlas work show 01 --tasks
```

## Regenerating the views

```bash
atlas work sync
```

This rewrites `work/README.md`, the dashboard a person reads, and
`work/index.yaml`, the file an agent reads. Both are generated from the task
tables, so progress is counted rather than claimed: a workstream cannot report
itself further along than its own tasks say it is.

> **Warning**
> Never hand-edit `work/README.md` or `work/index.yaml`. The `generated-current`
> gate will notice, and your edit will be overwritten by the next sync.

## Closing one

Fill in `05_publication`, set `status: closed` in `workstream.yaml`, and leave
the folder where it is. A closed workstream is the record of why the writing
says what it says.

## Next

- [Writing a document end to end](writing-a-document.md)
- [AUTHORITY](../../spec/authority.md), the standard behind all of this
