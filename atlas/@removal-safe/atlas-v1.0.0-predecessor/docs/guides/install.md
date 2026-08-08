# Install and first run

Get the `atlas` CLI working, then use it on a real repository. Five minutes.

## Install

Atlas needs Python 3.10 or newer and nothing else: two runtime dependencies,
both of which `pip` brings along.

```bash
pipx install atlas-standard     # recommended: isolated, still on your PATH
pip install atlas-standard      # or into the current environment
```

Verify:

```bash
atlas --version
atlas doctor
```

`atlas doctor` checks the environment before it checks anything else, so if
something is missing it says which thing and what to run.

> [!TIP]
> Working from a clone of this repository, or in a container where you would
> rather not install? `scripts/atlas` runs the identical CLI straight from the
> source tree with no install step.

## Shell completion

Worth the thirty seconds. The script is generated from the command tree, so it
never suggests a command the tool does not have.

```bash
# zsh
atlas completion zsh > ~/.zsh/completions/_atlas

# bash
atlas completion bash > ~/.local/share/bash-completion/completions/atlas

# fish
atlas completion fish > ~/.config/fish/completions/atlas.fish
```

Restart the shell, then type `atlas ` and press Tab.

## Start a repository

```bash
atlas init payments-api ../payments-api --owner person:you
cd ../payments-api
```

The scaffold is compliant on the first run, and `atlas init` finishes by listing
any placeholders it could not fill, so a template never reaches production with
`{{PROJECT_NAME}}` still in it.

```bash
atlas check
```

## Adopt in an existing repository

There is no adoption ceremony. Point the tool at what you have and read the
report:

```bash
cd ~/code/some-existing-service
atlas check
```

Most repositories fail several gates on the first run. That is the point: the
output is a work list, not a verdict. Take them one at a time:

```bash
atlas check --list                      # what gates exist
atlas check --only root-closed-set      # work one gate to green
```

[`docs/guides/adoption.md`](adoption.md) walks the full path in order.

## Daily use

```bash
atlas status                            # what this is, and where it stands
atlas check                             # is it still compliant
atlas work list --status blocked        # what is stuck, and who owns it
atlas spec show workstream --rules      # cite a rule in a review
atlas prompt search release             # find a prompt to hand to an assistant
atlas site serve                        # read the docs as a site
```

## In CI

`atlas check` exits non-zero on violations, so it needs no wrapper:

```yaml
- run: pip install atlas-standard
- run: atlas check
- run: atlas work sync --check      # generated artifacts are current
```

Exit codes distinguish outcomes, so a CI job can tell "this repository is
non-compliant" (`1`) from "the invocation was wrong" (`2`) or "this is not an
Atlas repository at all" (`4`).

## For agents and scripts

Every command accepts `--json`. The human rendering is not a stable contract;
the JSON is.

```bash
atlas check --json | jq '.checks[] | select(.state == "fail")'
atlas work list --json | jq '.workstreams[] | select(.status == "blocked")'
atlas spec show project --meta --json
```

Use `-C <dir>` to operate on a repository other than the current directory, or
set `ATLAS_REPOSITORY` when the working directory is not yours to choose.

## As a library

The CLI is a thin shell over an importable package. Anything it does, you can do
in Python without a terminal:

```python
from atlas.core import compliance
from atlas.paths import find_repository

report = compliance.run(find_repository("."))
for result in report.results:
    if not result.ok:
        print(result.check.id, [v.render() for v in result.violations])
```

Register your own gate and it runs alongside the built-in ones:

```python
from atlas.core.compliance import register
from atlas.core.manifest import Violation

@register("house-style", "READMEs name a support channel", "internal")
def check_support_channel(repo):
    text = (repo.root / "README.md").read_text()
    if "#support" not in text:
        return [Violation("README.md", "no support channel named", "internal")]
    return []
```

## Next

- [`docs/reference/cli.md`](../reference/cli.md): every command and flag
- [`docs/guides/new-project.md`](new-project.md): the scaffold in detail
- [`docs/guides/work-management.md`](work-management.md): running the work system
- [`docs/reference/glossary.md`](../reference/glossary.md): every term of art
