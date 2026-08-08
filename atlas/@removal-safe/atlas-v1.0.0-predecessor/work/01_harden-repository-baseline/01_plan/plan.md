# Plan: 01 Harden the repository into a canonical v0.0.1 baseline

## Approach

Measure before changing. The draft passed its own tests, so the failure mode was
never a broken check. It was facts stated in several places with nothing
comparing them. So the pass is: establish a green baseline, enumerate every
duplicated or contradicted fact against the filesystem, then convert each one
into either a single source, a generated mirror, or a test.

The alternative considered was a clean-room rewrite of the repository shape.
Rejected: the shape is sound and the specifications are the product. A rewrite
would have discarded working normative prose to fix a bookkeeping problem.

## Phases

| Phase | Outcome | Tasks |
|---|---|---|
| 1. Understand | A green baseline and a written register of every drift | T-01, T-02 |
| 2. Consolidate | No artifact maintained by hand in two places | T-03, T-04 |
| 3. Correct | Every countable claim agrees with the filesystem | T-05 |
| 4. Codify | Conventions written down and enforced, not inferred | T-06, T-07, T-08 |
| 5. Verify | Everything removed is recoverable and explained | T-09 |

## Assumptions

- The eight specifications are correct in substance. This pass changes their
  packaging (front matter, headings, cross-references) and not their rules.
  *(Checked: no normative sentence was edited; `spec:` commits would be required.)*
- Git history is unavailable. The input arrived as a flat archive with no `.git`
  directory, so provenance is captured as path, size, date, and SHA-256 instead.
  *(Checked: confirmed absent before archiving began.)*
- Downstream repositories have not yet been scaffolded from this template, so
  changing `template/` breaks nobody. *(Unchecked: if adopters exist, the
  template mirror change is a MINOR bump for them, not a patch.)*
