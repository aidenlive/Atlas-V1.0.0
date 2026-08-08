---
title: The tooling is a library first
kind: decision
owner: role:standards-maintainer
status: published
updated: 2026-08-08
audience: [developers]
summary: "Why the checks live in an importable package rather than in the command that runs them."
---

# 4. The tooling is a library first

Date: 2026-08-08

## Status

Accepted.

## Context

Checks written inside command functions can be run one way: by running the
command. Tests then have to invoke a process and parse its output, CI cannot
reuse a single gate, and nothing can be embedded in another tool.

## Decision

Everything lives in `src/atlas/core/` as pure functions over a `Repository`
object. They read, they never write, and they return violations rather than
printing or exiting. `src/atlas/cli/` is a presentation layer on top.

Packaging is declared in one `pyproject.toml` at the root, sanctioned as a root
entry. It is the Python ecosystem's single declaration point for build,
dependencies, entry points, and tool config, and the alternative is four
dotfiles.

## Consequences

The same code backs the CLI, the test suite, CI, and anything built on top. A
gate can be called directly in a test with no subprocess. The command layer stays
thin enough to read in one sitting.
