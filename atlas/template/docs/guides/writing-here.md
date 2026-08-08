---
title: Writing here
kind: guide
owner: {{OWNER}}
status: draft
updated: {{DATE}}
review_by: {{REVIEW_DATE}}
audience: [internal]
summary: "How to open a workstream, write a draft, and get it published."
---

# Writing here

Every piece of writing in this repository follows the same path: brief, draft,
review, publish. The path is short on purpose.

## 1. Open a workstream

```bash
atlas work new rewrite-onboarding --owner {{OWNER}}
```

That creates a numbered folder under `work/` with five sections. Write the brief
in `01_brief/brief.md` before anything else.

## 2. Draft

Write under `content/`, with front matter declaring `title`, `kind`, `owner`,
`status: draft`, and `updated`. Check yourself as you go:

```bash
atlas lint content/your-file.md
```

## 3. Review

Set `status: review`, name your reviewers in front matter, and record their
comments in `04_review/`. A reviewer who has not read it has not reviewed it.

## 4. Publish

An approver named in `authority.yaml` signs off, `status` becomes `published`,
and `review_by` is set from the cadence for that kind of content. Then:

```bash
atlas check
atlas work sync
```
