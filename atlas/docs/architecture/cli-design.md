---
title: Why the CLI is shaped this way
kind: explainer
owner: role:standards-maintainer
status: published
updated: 2026-08-08
review_by: 2027-08-08
audience: [developers]
summary: "One command, grouped help, JSON everywhere, and a reference generated from the parser."
---

# Why the CLI is shaped this way

## One command, grouped by intent

Eleven subcommands under one name. A flat alphabetical list tells a newcomer
nothing about where to start. So `atlas` with no arguments prints a help tree
grouped by what you are trying to do — Start, Verify, Read, Work, Shell — and
every group carries a worked example.

## argparse, deliberately

The parser comes from the standard library. `pip install atlas-editorial` pulls
no CLI framework, and the tool starts in milliseconds, which is what makes it
usable in a pre-commit hook. The cost is a little more code in `app.py`; the
benefit is two dependencies instead of six.

## The parser is the reference

`docs/reference/cli.md` is rendered from the parser tree. A flag cannot exist
without being documented, and the documentation cannot describe a flag the tool
lacks. Both failures are the ordinary way CLI documentation rots.

## Machine output is a first-class mode

Every command accepts `--json` and prints data on stdout with nothing else mixed
in, so `atlas check --json | jq '.checks[]'` needs no filtering. Exit codes carry
the distinction prose cannot: `1` means violations, `2` means you typed the flag
wrong, `4` means this is not an Atlas repository.

## Flags work in either order

Global flags are attached to the root and to every subcommand, so
`atlas --json check` and `atlas check --json` both work. People type them in
either order, and being right about which one is correct is not worth a usage
error.

## Checks are a registry, not a script

Each gate is a named object with an id, a summary, the rule it enforces, and a
pure function from repository to violations. That is what makes
`atlas check --only content-declared` possible, what makes `--json` structured
rather than scraped, and what lets a team add a house gate without forking a
shell script. See [ADR-0006](../decisions/0006-checks-as-a-registry.md).

## Errors name the remedy

Every error the CLI reports carries an optional hint, and the hint says what to
do next. A tool that reports only what went wrong makes the reader guess the
rest.
