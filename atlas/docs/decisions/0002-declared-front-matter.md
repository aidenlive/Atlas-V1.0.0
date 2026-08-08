---
title: Facts live in front matter, not in a tracker
kind: decision
owner: role:editorial-lead
status: published
updated: 2026-08-08
audience: [internal]
summary: "Why ownership, status, and review dates are stored in the document itself."
---

# 2. Facts live in front matter, not in a tracker

Date: 2026-08-08

## Status

Accepted.

## Context

Ownership recorded in a spreadsheet is accurate on the day it is written. Six
months later it names people who changed teams, documents that were merged, and
review dates nobody honoured, and the only way to find out is to read everything.

## Decision

Every document declares its own facts in a YAML block at the top: `title`,
`kind`, `owner`, `status`, `updated`, and usually `review_by`. The block is
validated against a schema, and a gate fails when a required field is missing.

## Consequences

A fact stored beside the thing it describes gets updated in the same edit, by
the person who already has the file open. Ownership survives reorganisations
because it moves with the file.

The cost is five lines at the top of every document, and the objection that they
clutter the file is real. We accept it: those five lines are the only reason the
question "who owns this?" has an answer a year later.
