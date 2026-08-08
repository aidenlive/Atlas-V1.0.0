---
title: Archive the predecessor, then rebuild
kind: decision
owner: role:editorial-lead
status: published
updated: 2026-08-08
audience: [internal, leadership]
summary: "Why this repository was rebuilt rather than refactored, and why the archive is exempt and temporary."
---

# 5. Archive the predecessor, then rebuild

Date: 2026-08-08

## Status

Accepted. Supersedes the predecessor repository in full.

## Context

The predecessor stated what a *repository* must contain and left the writing
itself to taste. Turning it into an editorial system by incremental
reorganisation would have meant every document carrying two purposes at once for
the length of the migration. That is the exact condition the standards exist to
prevent.

The predecessor also, explicitly, banned in-repository graveyards: `legacy/`,
`old/`, `@removal-safe/`. Git is the archive, and dead files beside live ones
poison search, agents, and every grep.

That reasoning still holds. It was overruled here for one narrow reason: this
rebuild does not share a history with what it replaces, so there is no commit to
recover the predecessor from. An archive with no git history behind it is not a
graveyard; it is the only copy.

## Decision

1. The complete predecessor is archived, unmodified, under `@removal-safe/`.
2. The new repository is built from first principles, reusing the architecture
   and the CLI philosophy but none of the files.
3. `@removal-safe/` is excluded from every walk the tooling makes, so nothing in
   it can pass or fail a check, appear in a search, or be picked up by an agent.
4. The exemption is temporary. The archive is deleted once the predecessor is
   published to its own repository with its history intact, and no later than
   **2027-02-08**.

## Consequences

The new repository is coherent on day one rather than at the end of a migration.
The old one remains readable during the changeover, at the cost of one sanctioned
exception that is written down, scoped, and dated.

> **Warning**
> This is the only permitted in-repository archive, and it exists under a
> deadline. A second one is a violation, not a precedent.
