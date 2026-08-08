---
title: Gates are a registry, not a script
kind: decision
owner: role:standards-maintainer
status: published
updated: 2026-08-08
audience: [developers]
summary: "Why each compliance gate is a named object with an id, a rule, and a pure function."
---

# 6. Gates are a registry, not a script

Date: 2026-08-08

## Status

Accepted. Depends on [ADR-0004](0004-packaged-cli-in-src.md).

## Context

A shell script that runs the checks in sequence works. It stays the right size
until three things are wanted from it: selecting one check, consuming the results
as data, and adding a gate without editing the file.

## Decision

Each gate is a `Check` in a registry: an id, a one-line summary, the rule
identifier it enforces, and a pure function from repository to violations.

```python
@register("root-closed-set", "The root contains only sanctioned entries", "CONTENT C-02")
def _root_closed_set(repo: Repository) -> list[Violation]:
    ...
```

A gate that raises is reported as a failed gate rather than taking the process
down with it.

## Consequences

`atlas check --only root-closed-set` runs one gate, which is what you want while
fixing one violation. `--json` output is structured rather than scraped. A team
with a house rule registers a gate instead of forking a growing script.
