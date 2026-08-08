---
title: Quick reference
kind: reference
owner: role:editorial-lead
status: published
updated: 2026-08-08
review_by: 2026-11-08
audience: [internal, developers]
summary: "The whole suite on one page: standards, rules that get cited most, commands, and states."
---

# Quick reference

## The eight standards

| Standard | Question | Rules |
|---|---|---|
| [VOICE](../../spec/voice.md) | How does the company sound? | `V-01`–`V-10` |
| [LANGUAGE](../../spec/language.md) | Which words and mechanics? | `L-01`–`L-10` |
| [STRUCTURE](../../spec/structure.md) | How is it shaped? | `S-01`–`S-10` |
| [CONTENT](../../spec/content.md) | What must be true of it? | `C-01`–`C-09` |
| [MATRIX](../../spec/matrix.md) | What kind is it? | `M-01`–`M-06` |
| [CHECKLIST](../../spec/checklist.md) | Is it ready? | `Q-01`–`Q-06` |
| [AUTHORITY](../../spec/authority.md) | Who may act? | `A-01`–`A-10` |
| [PUBLICATION](../../spec/publication.md) | Where does it go? | `P-01`–`P-08` |

## The rules cited most in review

| Rule | Short form |
|---|---|
| `V-03` | Use the shorter word |
| `V-04` | One sentence, one idea — 34 words is the ceiling |
| `V-05` | A claim carries a number, a source, or an example |
| `V-06` | Say the hard thing first |
| `S-04` | Lead with the answer |
| `S-07` | Link text names its destination |
| `S-08` | One fact, one home |
| `L-01` | One spelling per name |
| `A-04` | The author is never the sole approver |

## Commands

```bash
atlas status                  # what this is, who owns it, where it stands
atlas check                   # the repository against the standard
atlas lint content/ --strict  # the writing against the standards
atlas spec show voice --rules # the rules a standard defines
atlas lexicon find email      # how do we spell it, and why
atlas prompt search review    # a written-once request to paste
atlas work list --status blocked
```

## States

| Where | Values |
|---|---|
| Document `status` | `draft`, `review`, `published`, `superseded`, `retired` |
| Workstream `status` | `planned`, `active`, `blocked`, `review`, `published`, `closed` |
| Task state | `todo`, `doing`, `blocked`, `done` |
| Repository `stage` | `idea`, `draft`, `active`, `maintained`, `frozen`, `retired` |

## Exit codes

`0` ok · `1` violations found · `2` bad usage · `3` not found · `4` not an
Atlas repository.
