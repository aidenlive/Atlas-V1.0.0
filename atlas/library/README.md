# library

Shared editorial assets. One canonical copy of each, referenced by path rather
than pasted (CONTENT C-07).

| Directory | Holds |
|---|---|
| [`lexicon/`](lexicon/terms.yaml) | How we spell our names, and which phrasings we have decided against |
| [`prompts/`](prompts/README.md) | 56 written-once requests, covering 14 stages of a piece of writing |
| `templates/` | Skeletons for the kinds of document we write most |

Both the lexicon and the prompt catalogue are read by the tooling, so a change
here changes what `atlas lint` enforces and what `atlas prompt` finds.
