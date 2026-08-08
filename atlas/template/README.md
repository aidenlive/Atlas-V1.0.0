# {{TITLE}}

{{DESCRIPTION}}

This repository follows the Atlas editorial standard `editorial/1.0`. Every
document declares who owns it and when it was last checked, and one command
checks the whole repository against the standard.

## Where things are

| Path | Holds |
|---|---|
| `content/` | The published writing |
| `docs/` | How this repository works |
| `library/lexicon/` | The names and phrasings this repository has decided |
| `work/` | Editorial work in progress, one numbered workstream each |

## Working here

```bash
atlas status                 # what this is, who owns it, where it stands
atlas check                  # is the repository in order?
atlas lint content/          # does the writing follow the standards?
atlas work new first-piece --owner {{OWNER}}
```

## Next

1. Replace the placeholders in `project.yaml` and `authority.yaml`.
2. Add a second approver, so no author signs off alone.
3. Write the first piece under `content/`, then run `atlas check`.
