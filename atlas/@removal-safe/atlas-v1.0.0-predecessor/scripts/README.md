# scripts/

Thin wrappers around the `atlas` package. They exist so a checkout with no
install still works: CI, a fresh clone, a container without `pip install -e .`
— and so the paths CI has always used keep working.

Every one of them is one line of dispatch. **The logic lives in `src/atlas/`**;
if you are editing behavior, you are in the wrong directory.

| Script | Equivalent |
|---|---|
| `atlas` | `atlas` (the whole CLI, no install required) |
| `check-compliance.sh` | `atlas check` |
| `build_assets.py` | regenerates `assets/*.svg` from the design tokens |
| `generate_prompts.py` | regenerates the prompt catalog (its own source of truth) |

```bash
scripts/atlas check          # no install
pip install -e .             # then just: atlas check
```
