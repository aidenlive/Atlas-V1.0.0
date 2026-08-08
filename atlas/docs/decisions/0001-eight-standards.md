---
title: Eight standards, one question each
kind: decision
owner: role:editorial-lead
status: published
updated: 2026-08-08
audience: [internal]
summary: "Why the suite is eight documents rather than one style guide or twenty rules pages."
---

# 1. Eight standards, one question each

Date: 2026-08-08

## Status

Accepted.

## Context

A single style guide is read once and cited never. It mixes voice advice with
approval workflow with file naming, so nobody can find the sentence they need
during a review, and no part of it can be checked independently.

The predecessor repository had already shown the alternative working, with eight
standards covering repository structure. The question was whether the same shape
carried over to writing.

## Decision

Eight standards, each answering exactly one question, each numbering its own
rules with its own prefix:

VOICE, LANGUAGE, STRUCTURE, CONTENT, MATRIX, CHECKLIST, AUTHORITY, PUBLICATION.

A rule belongs to the standard that answers its question, and to no other.

## Consequences

A review comment can cite `V-05` and the author knows which document to open. A
gate can enforce one rule without a linter that understands all of them. And a
standard can be revised on its own cadence, because nothing else depends on its
internal numbering.

Some subjects sit on a boundary: heading capitalisation is both LANGUAGE and
STRUCTURE. We resolve those by asking which question the reader would have
asked, not which document is thinner.
