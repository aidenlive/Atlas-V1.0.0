# Prompt library

56 written-once requests, covering 14 stages of a piece of writing. Paste one
into an AI assistant, or hand it to a colleague.

Three conventions hold, and all three are checked:

- **One request per prompt.** A prompt that asks for three things gets one third
  of each.
- **Four sentences at most, one paragraph.** Longer than that is a brief, and
  briefs live in `work/`.
- **Anything that changes files proposes a plan first**, so the reply is a
  change to approve rather than a change to discover.

## The stages

| Stage | For |
|---|---|
| `brief` | Deciding what to write, for whom, and why |
| `research` | Finding the facts a claim needs |
| `drafting` | Getting the first version onto the page |
| `structure` | Fixing the shape rather than the sentences |
| `editing` | Line-level work: tightening, cutting, sharpening |
| `voice` | Making it sound like us |
| `terminology` | Names, spellings, and the lexicon |
| `accessibility` | Making it work for every reader |
| `localisation` | Preparing for and checking translation |
| `review` | Reading someone else's work usefully |
| `publication` | Metadata, channels, and the last mile |
| `maintenance` | Freshness, duplication, and retirement |
| `measurement` | Whether any of it worked |
| `agents` | Briefing, constraining, and reviewing AI assistants |

## Using them

```bash
atlas prompt list --stages
atlas prompt search review
atlas prompt show write-brief
atlas prompt show write-brief | pbcopy
```

## Adding one

Write the file under `library/prompts/<stage>/request-<verb>-<object>.txt`, then
regenerate the catalogue:

```bash
python scripts/build_library.py
atlas check --only prompt-shape
```

`index.yaml` is generated from the files, so it cannot list a prompt that does
not exist, or miss one that does.
