# 8. Compliance gates are a registry, not a script

Date: 2026-08-07

## Status

Accepted. Depends on [ADR-0007](0007-packaged-cli-in-src.md).

## Context

`check-compliance.sh` ran six checks in sequence, accumulating a `fail` flag and
printing `VIOLATION: …` lines to stderr. It worked, and it was the right size
for what it did when it was written.

It stopped being the right size for three reasons.

Violations were unstructured text. Anything consuming them: CI annotations, an
editor, an agent: had to parse prose that was never designed to be parsed.

Checks could not be selected. Fixing one violation meant re-running all six and
reading past the five that already passed.

Extending it meant editing it. A repository adopting a ninth standard, or an
organisation with a house rule, had no way to add a gate except to fork a
growing shell script, and then to re-fork it on every upstream change.

## Decision

Each gate is a `Check` in a registry: an id, a one-line summary of what it
enforces, the rule identifier it enforces, and a pure function from repository
to a list of `Violation`s.

```python
@register("root-closed-set", "Root contains only sanctioned entries", "PROJECT §8, §9")
def check_root(repo: Repository) -> list[Violation]:
    ...
```

Gates read; they never write. They return violations rather than printing or
exiting. A gate that raises is reported as a failed gate rather than taking the
run down with it, because a broken check should not hide the eleven that work.

Gates declare their own applicability. `standards_only` marks the ones that only
mean something where the normative sources live; `requires` marks the ones that
apply once a repository adopts a companion standard. Inapplicable gates are
reported as **skipped with a reason**, never silently passed: "not adopted" and
"passing" are different facts, and collapsing them lets a repository look
compliant because it has nothing to be compliant about.

## Consequences

**Good.** `--json` emits structured violations with rule identifiers and
document pointers. `--only <id>` runs one gate while you fix it. `--list` shows
what exists. Adding a gate is registering a function: Atlas's own registration
of twelve gates uses exactly the mechanism an adopter would. Every gate is unit
testable in isolation.

**Costs.** More code than the shell script for the same twelve checks, and a
registry is import-order sensitive in a way a sequential script is not. Gate
ordering is registration order, which is implicit; making it explicit would need
a priority field that nothing yet needs.

**`--strict`** exists because "skipped" is honest but exploitable: a repository
can pass by adopting nothing. `--strict` turns skips into failures, for an
organisation that expects every repository to adopt the full suite.

**Rejected: gates as plugin entry points.** Discovering gates through package
entry points would let a third party add one by installing a package. It is the
right answer eventually and premature now: nobody has asked, and the decorator
already works for the in-repository case that does exist.
