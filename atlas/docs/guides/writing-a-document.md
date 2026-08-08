---
title: Writing a document end to end
kind: guide
owner: role:editorial-lead
status: published
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal]
summary: "From brief to published, with the standard applied at each step and nothing applied twice."
---

# Writing a document end to end

This is the whole path, once. It assumes no technical background beyond running
a command someone gave you.

## 1. Decide what it is

Two declarations settle most later arguments: the **kind** and the **audience**.
A guide for developers and a guide for customers are not the same document with
different words.

Look the kind up in [MATRIX](../../spec/matrix.md). It tells you the shape, the
tone, and how often the document must be re-read.

## 2. Write the brief

Open a workstream and fill in `01_brief/brief.md`. Five short answers: what,
who, why now, the one takeaway, and what done looks like.

## 3. Draft

Follow the composition order from [STRUCTURE](../../spec/structure.md):

1. Context
2. Key takeaway
3. Supporting detail
4. Examples
5. Next steps

Lead with the answer. Background is what the reader wanted second.

## 4. Check yourself

```bash
atlas lint content/your-file.md -v
```

Errors are rule violations and must be fixed. Warnings are judgement calls: a
34-word sentence may be the right sentence, and you are allowed to keep it.

## 5. Review

Set `status: review`, name your reviewers, and hand them the
[CHECKLIST](../../spec/checklist.md) Review profile. Ask for the three places
they would stop reading, not for a general opinion.

## 6. Publish

An approver named in `authority.yaml` signs off. Then set `status: published`,
set `review_by`, link the document from the index readers actually start at, and
run:

```bash
atlas check
```

## 7. Retire it, eventually

Every document stops being true. Mark it `superseded` and point at the
replacement, or mark it `retired` and take it out of navigation. Content left
published and untrue is worse than no content at all.

## The short version

> **Tip**
> Declare what it is, write the brief, lead with the answer, run `atlas lint`,
> get one other pair of eyes, then set the date it must be read again.
