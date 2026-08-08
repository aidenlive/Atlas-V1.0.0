# CLI design

Why `atlas` is shaped the way it is. The rules below are the ones that were
easiest to get wrong, and each cost something to learn.

## The CLI is a shell over a library, not the other way round

Every command in `src/atlas/cli/` parses arguments, calls one function, renders
the result, and returns an exit code. The logic lives in `atlas.core` and
`atlas.site`, which know nothing about terminals, argument parsing, or process
exit.

That boundary buys three things. The same code backs the CLI, the test suite,
and anything an adopter builds on top, so a compliance gate can be unit-tested
without spawning a subprocess and scraping stdout. Adopters can register their
own gates in Python instead of forking a shell script. And a bug is reproducible
by calling one function rather than by reconstructing a command line.

The previous arrangement had the logic in `scripts/*.py` invoked as programs.
Nothing could import it, so nothing tested it directly, and `scripts/work.py`
had to be *copied* into the template to be reusable: a copy that promptly
drifted from its source.

## One command, grouped help

Seven scripts with seven invocation styles is seven things to remember, and the
only way to discover the seventh is to list the directory. One command with a
subcommand tree is discoverable by typing it.

Help is grouped by intent rather than listed alphabetically, and every group
carries worked examples, because an alphabetical list of nineteen subcommands
tells a newcomer nothing about where to start.

## The parser is the reference

`docs/reference/cli.md` and the site's command reference are generated from the
argument parser by `atlas site build --write-reference`, and CI fails if the
committed copy differs from a fresh render.

Hand-written CLI reference documentation drifts from the tool the moment someone
adds a flag, and it drifts *silently*: nothing fails, the docs are simply
wrong. Generating it means a flag cannot exist undocumented and the docs cannot
describe a flag that does not exist.

## Exit codes carry meaning

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | The command ran and found violations |
| `2` | The invocation was malformed |
| `3` | A named thing does not exist |
| `4` | Not an Atlas repository |
| `70` | Internal error — always a bug |

The split between `1` and `2` is the load-bearing one. A CI job that treats "the
repository is non-compliant" identically to "you typed the flag wrong" reports a
red build for the wrong reason, and someone spends an afternoon fixing the wrong
thing.

## `--json` lives beside the human output

Each command calls `console.emit(payload)` and the human renderers
unconditionally; exactly one of them produces output, decided once at the
boundary by `--json`.

Keeping both representations in the same function is the only reliable way to
stop them diverging. A separate JSON code path is a second implementation of the
same command, and it will disagree with the first one eventually.

Agents and scripts should prefer `--json`: the human rendering is explicitly not
a stable contract, and it changes when we can make it clearer.

## Color is the third channel, never the only one

Color is disabled when stdout is not a terminal, when `NO_COLOR` is set, and
when `--no-color` is passed. Every status ships a glyph and a word alongside its
hue, and every glyph has an ASCII fallback chosen from the encoding the stream
actually reports.

So a build log, a `LANG=C` runner, a Windows console, and a color-blind reader
all get the same information. This mirrors the rule the design system applies to
status pills on the site: one policy, two surfaces.

## Errors carry a hint

`AtlasError` carries an optional `hint`: the next thing to try. A bare error
message tells someone they are stuck; a hint tells them how to stop being stuck.

```
✕ no workstream '07'
  hint: Known workstreams: 01 harden-repository-baseline
```

## No CLI framework

`argparse` is in the standard library, so `pip install atlas-standard` pulls two
dependencies rather than a dependency tree, and the tool starts fast enough to
sit in a pre-commit hook. The site generator makes the same trade: its Markdown
renderer and syntax highlighter are a few hundred lines each, because a
documentation pipeline that breaks on an upstream release is a documentation
pipeline that stops running.

The cost is real: `argparse` help formatting needed a subclass, and the
highlighter is a tokenizer rather than a parser. Both were cheaper than the
dependency.

## Related

- [ADR-0007](../decisions/0007-packaged-cli-in-src.md): why the tooling moved to `src/`
- [ADR-0008](../decisions/0008-compliance-as-a-registry.md): why gates are a registry
- [`repository-design.md`](repository-design.md): how the whole repository fits together
