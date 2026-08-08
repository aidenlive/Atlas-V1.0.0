# 0003: Catalogs are generated from one source, never hand-edited

Date: 2026-08-07 · Status: Accepted

## Context
The prompt library exists in three views: the individual `.txt` payloads,
the machine catalog (`library/prompts/index.yaml`), and the human index
(`library/prompts/README.md`). Three hand-maintained views of one fact is the
truth-fragmentation failure the suite exists to prevent: the wiki/README
split wearing new clothes.

## Decision
`scripts/generate_prompts.py` holds the prompts as data and emits all three
views. Edits go to the generator; the files are output. `tests/test_prompts.py`
enforces mutual completeness between files and index, so hand-edited drift
fails CI rather than shipping.

## Consequences
Prompt changes are slightly indirect (edit generator, regenerate) in exchange
for catalogs that cannot disagree with themselves. If the library outgrows a
single generator module, the natural next step is per-category data files
consumed by the same emitter: the contract tests are unaffected.
