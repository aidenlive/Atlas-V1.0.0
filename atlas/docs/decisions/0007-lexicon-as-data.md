---
title: The lexicon is data, not prose
kind: decision
owner: role:editorial-lead
status: published
updated: 2026-08-08
audience: [internal]
summary: "Why house terminology lives in a YAML file that the linter reads directly."
---

# 7. The lexicon is data, not prose

Date: 2026-08-08

## Status

Accepted.

## Context

House terminology usually lives in a table inside a style guide. A person can
read it; nothing can check it. The result is that the same three corrections are
made by hand in review, forever, and inconsistently.

## Decision

Terminology lives in `library/lexicon/terms.yaml` as two lists: terms with one
canonical spelling, and phrases paired with their replacement. `atlas lint` reads
that file directly. A phrase entry with no replacement fails a gate, because a
rule without a remedy is a complaint.

Each entry carries a severity, so a product name can be an error while a style
preference is a warning a writer may override with reason.

## Consequences

Changing the house style is a one-line change to one file, enforced everywhere on
the next run. Reviewers stop spending attention on spelling and spend it on
argument, which is the only part a machine cannot do.

The risk is a lexicon that grows into a wall of failures nobody agreed to. The
mitigation is in the adoption guide: seed it only with corrections that have
already been made twice by hand.
