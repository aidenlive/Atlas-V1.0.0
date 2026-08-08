# Baseline inventory: 2026-08-07

Measured before anything was changed, so later claims of improvement have a
number to compare against.

## Shape

| Measure | Value |
|---|---|
| Files | 377 |
| Total size | 532 KB |
| Specifications | 8 |
| Prompts | 78 across 14 categories |
| Workstreams | 4 (all fabricated — see the drift register) |
| Version control | **absent** — no `.git` directory in the archive |

## Health

Every gate was already green, which is the important finding: the defects in
this repository are not the kind a test catches.

| Gate | Result |
|---|---|
| `python -m pytest tests/ -q` | 63 passed |
| `atlas check` | COMPLIANT |
| `atlas work validate` | 4 workstreams valid |
| `atlas site build` | 205 pages |

## Size distribution

`assets/design/neue.design.md` alone was 118 KB: 22% of the repository, and
larger than the four biggest specifications combined. Of it, 27 KB (the YAML
front matter) is read by `build_site.py`; the remaining 91 KB is read by nothing.
