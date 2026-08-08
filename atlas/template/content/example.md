---
title: Example document
kind: guide
owner: {{OWNER}}
status: draft
updated: {{DATE}}
review_by: {{REVIEW_DATE}}
audience: [internal]
summary: "A worked example of the shape every document here takes."
---

# Example document

Delete this file once you have written something real. It exists to show the
shape: front matter that declares the facts, a title that matches it, and a
first screen that says what this is.

## What a document owes its reader

The first screen answers three questions: what this is, who it is for, and what
to do next. Everything else can wait.

## Prerequisites

- Access to this repository
- The Atlas CLI: `pip install atlas-editorial`

## Steps

1. Copy this file and rename it.
2. Change the front matter, starting with `title`, `owner`, and `kind`.
3. Write the first screen.
4. Run `atlas lint content/` and fix what it reports.

## Verify

```bash
atlas lint content/ --strict
```

A clean run means the mechanical half of the standard is satisfied. The other
half is a reviewer.
