# Brief

## What we are writing

The eight standards, the lexicon, the prompt library, and the tooling that
checks them — rebuilt from first principles as one editorial system rather than
grown by accretion.

## Who it is for

Everyone at the company who writes anything a colleague, a customer, or a
partner will read. The standards assume no technical background; the CLI is for
people who want the checks in CI.

## Why now

The predecessor repository stated what a *repository* must contain and left the
writing itself to taste. Editorial disagreements had no shared reference, so
every review re-argued the same questions: what do we call this, how long should
a paragraph be, who signs off, when does a document expire.

## The one thing they should take away

Writing standards only hold when they are checkable. Everything mechanical is a
gate; everything else is a reviewer's judgement, and the two are kept apart.

## Constraints

- Channel: repository, then the docs site
- Length: eight standards, none longer than one sitting
- Deadline: v1.0.0
- Must not say: anything the tooling cannot check or a reviewer cannot judge

## Done looks like

`atlas check` passes on this repository, the standards are self-hosting, and a
new repository scaffolded from `template/` passes on its first run.
