# scripts

Thin wrappers, so a bare checkout works without an install.

| Script | Does |
|---|---|
| `atlas` | Run the CLI from a checkout: `scripts/atlas check` |
| `build_library.py` | Regenerate `library/prompts/index.yaml` from the prompt files |
| `build_reference.py` | Regenerate `docs/reference/cli.md` from the argument parser |
| `build_assets.py` | Regenerate the badges from `project.yaml` and the design tokens |
| `build_screenshots.py` | Re-record the README's terminal demos by running the real commands |
| `write_prompts.py` | Rewrite the prompt library source files as a set |

Everything here is derived from something else in the repository. If a generated
file and its source disagree, the source wins and the script is re-run.
