---
title: CLI reference
kind: reference
owner: role:editorial-lead
status: published
updated: 2026-08-08
generated_by: scripts/build_reference.py
---

<!-- Generated from the argument parser. Do not edit by hand. -->

# CLI reference

`atlas` 1.0.0, enforcing standard `editorial/1.0`.

Every command accepts the global flags below, before or after the
command name. Exit codes: `0` ok, `1` violations found, `2` bad usage,
`3` not found, `4` not an Atlas repository.

| Flag | Does |
|---|---|
| `-C, --directory DIR` | operate on the repository at DIR |
| `--json` | emit machine-readable JSON |
| `--no-color` | disable color and styling |
| `-q, --quiet` | suppress progress output |
| `-v, --verbose` | explain each step |

## Start

### `atlas init`

start a new repository that already passes

```text
atlas init [-h] [--owner OWNER] [--description DESCRIPTION] [--template DIR] [--force]
                  [-C DIR] [--json] [--no-color] [-q] [-v]
                  name [path]
```

| Option | Does |
|---|---|
| `name` | repository name, lower-case-with-hyphens |
| `path` | where to create it (default: ./NAME) |
| `--owner` | who owns it (default: person:you) |
| `--description` | one sentence for the manifest |
| `--template` | use this template instead of the built-in one |
| `--force` | write into a non-empty directory |

### `atlas status`

show what this project is and where it stands

```text
atlas status [-h] [--check] [-C DIR] [--json] [--no-color] [-q] [-v]
```

| Option | Does |
|---|---|
| `--check` | also run the compliance gates |

### `atlas doctor`

diagnose the environment and this repository

```text
atlas doctor [-h] [-C DIR] [--json] [--no-color] [-q] [-v]
```

## Verify

### `atlas check`

check this repository against the standard

```text
atlas check [-h] [--only CHECK] [--list] [-C DIR] [--json] [--no-color] [-q] [-v]
```

| Option | Does |
|---|---|
| `--only` | run only this gate (repeatable); see --list |
| `--list` | list the gates and exit |

### `atlas lint`

check a document against the editorial standards

```text
atlas lint [-h] [--only RULE] [--skip RULE] [--changed] [--strict] [--list] [-C DIR]
                  [--json] [--no-color] [-q] [-v]
                  [PATH ...]
```

| Option | Does |
|---|---|
| `paths` | files or directories to lint |
| `--only` | run only this lint rule (repeatable) |
| `--skip` | skip this lint rule (repeatable) |
| `--changed` | lint Markdown changed against the default branch |
| `--strict` | treat warnings as errors |
| `--list` | list the lint rules and exit |

### `atlas validate`

check that a manifest is filled in correctly

```text
atlas validate [-h] [--kind {authority,content,project,workstream}] [-C DIR] [--json]
                      [--no-color] [-q] [-v]
                      PATH [PATH ...]
```

| Option | Does |
|---|---|
| `paths` | manifest files to validate |
| `--kind` | force a schema instead of inferring it |

## Read

### `atlas spec`

read the standards and cite their rules

```text
atlas spec [-h] [-C DIR] [--json] [--no-color] [-q] [-v] <subcommand> ...
```

| Subcommand | Does |
|---|---|
| `spec list` | list the standards |
| `spec show` | show one standard |
| `spec rules` | list every rule in the suite |

### `atlas prompt`

find a written-once request to paste or hand over

```text
atlas prompt [-h] [-C DIR] [--json] [--no-color] [-q] [-v] <subcommand> ...
```

| Subcommand | Does |
|---|---|
| `prompt list` | list prompts, or the stages |
| `prompt search` | search prompts by word |
| `prompt show` | print one prompt, and nothing else |

### `atlas lexicon`

look up a term or a phrasing decision

```text
atlas lexicon [-h] [-C DIR] [--json] [--no-color] [-q] [-v] <subcommand> ...
```

| Subcommand | Does |
|---|---|
| `lexicon list` | list every term |
| `lexicon find` | look one up |
| `lexicon phrases` | list the phrases we replace |

## Work

### `atlas work`

plan, track, and verify editorial work

```text
atlas work [-h] [-C DIR] [--json] [--no-color] [-q] [-v] <subcommand> ...
```

| Subcommand | Does |
|---|---|
| `work new` | open a workstream from the template |
| `work list` | list workstreams |
| `work show` | show one workstream |
| `work sync` | regenerate the dashboard and index from the task tables |
| `work validate` | check every workstream's shape and manifest |

## Shell

### `atlas completion`

print a shell completion script

```text
atlas completion [-h] [-C DIR] [--json] [--no-color] [-q] [-v] {bash,zsh,fish}
```

| Option | Does |
|---|---|
| `shell` | which shell |
