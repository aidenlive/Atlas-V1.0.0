# @removal-safe

> **Warning**
> Nothing in this directory is current. It is an archive of the repository Atlas
> replaced, kept unmodified during the changeover, and **scheduled for deletion
> on or before 2027-02-08**.

## What this is

`atlas-v1.0.0-predecessor/` is the complete previous repository: 312 files, the
eight repository-structure standards, its tooling, its work system, and its
documentation, exactly as received. Nothing has been edited, reformatted, or
removed.

`MANIFEST.sha256` lists every file with its SHA-256 digest, so the archive can
be verified against the original at any point before it is deleted:

```bash
cd @removal-safe/atlas-v1.0.0-predecessor
shasum -a 256 -c ../MANIFEST.sha256
```

## Why it exists at all

The predecessor's own PROJECT standard banned in-repository archives — `legacy/`,
`old/`, `@removal-safe/` — on the grounds that version control is already a
perfect archive, and that dead files beside live ones poison search, agents, and
every grep. That reasoning is sound and still holds.

It was overruled exactly once, for one narrow reason: this rebuild shares no git
history with what it replaces, so there is no commit to recover the predecessor
from. An archive with no history behind it is not a graveyard; it is the only
copy.

The decision, its scope, and its deadline are recorded in
[ADR-0005](../docs/decisions/0005-archive-then-rebuild.md).

## How it is kept from doing harm

| Concern | How it is handled |
|---|---|
| Polluting checks | `@removal-safe/` is in `EXCLUDED_DIRS`; no walk the tooling makes descends into it |
| Polluting search and agents | `AGENTS.md` marks it off limits: do not read it for guidance, do not copy from it |
| Rotting silently | It cannot rot, because it is frozen and checksummed |
| Becoming permanent | It has a deletion date, and the date is in the changelog |

## What replaces what

| Predecessor | Now |
|---|---|
| WORKSPACE, PROJECT, MATRIX, CHECKLIST | CONTENT, MATRIX, CHECKLIST |
| ADMIN (`admin.yaml`, `org.yaml`) | AUTHORITY (`authority.yaml`) |
| PRESENTATION | PUBLICATION |
| LIBRARY | `library/` — the lexicon, the prompts, content templates |
| WORKSTREAM (nine sections) | AUTHORITY, and `work/` with five sections |
| — | VOICE, LANGUAGE, STRUCTURE — the standards this suite exists for |

The architecture, the manifest model, and the CLI philosophy were carried over.
None of the files were.

## When the deadline arrives

1. Publish `atlas-v1.0.0-predecessor/` to its own repository, with its history.
2. Link that repository from `CHANGELOG.md`.
3. Delete this directory in a commit that says so, and remove the
   `@removal-safe` entry from `EXCLUDED_DIRS` and from the sanctioned root set.
