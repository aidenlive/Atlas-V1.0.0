# Library

Things authored once and used many times. Governed by
[`spec/library.md`](../spec/library.md).

| Class | Holds | Index |
|---|---|---|
| [`prompts/`](prompts/) | Reusable, tool-agnostic statements of intent | [`prompts/index.yaml`](prompts/index.yaml) |
| [`icons/`](icons/) | Interface glyphs, one concept per file | [`icons/index.yaml`](icons/index.yaml) |
| [`typefaces/`](typefaces/) | Font files and the licenses that permit them | [`typefaces/index.yaml`](typefaces/index.yaml) |
| [`media/`](media/) | Diagrams, screenshots, recordings, and their sources | [`media/index.yaml`](media/index.yaml) |

## The rules that hold across all four

An asset lives in exactly one place (L-A1) and appears in its class index
(L-A2). It is named for what it is, not where it came from (L-A3). If it was
derived, the index says from what (L-A4); if the organization did not author it,
the index carries its license and origin (L-A5). Everything arrives by pull
request (L-A6).

The four classes are a **closed set**. A fifth is added by amending the
specification, not by creating a folder, which is what keeps this directory
navigable rather than a second downloads folder.

## Adding something

1. Put the file in the right class directory.
2. Add its index entry, including `source` if derived and `license` if foreign.
3. Open a pull request. `python -m pytest tests/test_library.py -q` checks that
   the files and the indexes agree in both directions.

Prompts are the exception. They are **generated**. Edit
[`scripts/generate_prompts.py`](../scripts/generate_prompts.py) and re-run it.
