# CLI reference

<!-- GENERATED from the argument parser by `atlas site build --write-reference`.
     Do not edit; change src/atlas/cli/ and regenerate. -->

Every command in `atlas` 1.0.0. Generated from the parser itself, so it cannot drift from the tool.

## Global options

These are accepted by every command, before or after the subcommand.

| Option | Description |
|---|---|
| `-C, --directory DIR` | Operate on the repository at `DIR` instead of the current one. |
| `--json` | Emit machine-readable JSON instead of formatted output. |
| `--no-color` | Disable color and styling. Also honoured: `NO_COLOR`. |
| `-q, --quiet` | Suppress progress output. Errors still print to stderr. |
| `-v, --verbose` | Explain each step. |
| `--version` | Print the version and exit. |

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Success. |
| `1` | The command ran and found violations. |
| `2` | The invocation was malformed. |
| `3` | A named thing does not exist. |
| `4` | Not run inside an Atlas repository. |
| `70` | Internal error: always a bug in Atlas. |

## Commands

### `atlas init`

Copy the starter template into a new directory, filling in the project name, the date, and the owner. What you get passes `atlas check` on the first run and has the work system ready to use. Any placeholder the scaffold could not fill is listed at the end, so a template never ships with `{{PROJECT_NAME}}` still in it.

```bash
atlas init [-h] [--owner OWNER] [--description DESCRIPTION] [-C DIR] [--json] [--no-color] [-q] [-v] name [destination]
```

| Argument | Required | Description |
|---|---|---|
| `name` | yes | lowercase-hyphenated project name, e.g. payments-api |
| `destination` | no | where to create it (default: ./<name>) |

| Option | Default | Description |
|---|---|---|
| `--owner` | `person:you` | accountable principal for the new repository |
| `--description` | `` | one-line description for project.yaml |

```bash
atlas init payments-api ../payments-api
atlas init payments-api ../payments-api --owner team:platform
```

### `atlas status`

One screen covering how this project is classified, who owns it, what work is live, and what is blocked. Every value is read from the declared manifest rather than guessed from the files, so this is what the repository says about itself. Where the claim and reality disagree, `atlas check` is what finds out.

```bash
atlas status [-h] [-C DIR] [--json] [--no-color] [-q] [-v]
```

### `atlas doctor`

Check that everything Atlas needs is installed and that this repository is shaped the way the standard expects. Each problem comes with the command that fixes it. Safe to run anywhere: outside a repository it checks the environment only, which makes it the right first command when an install seems wrong.

```bash
atlas doctor [-h] [-C DIR] [--json] [--no-color] [-q] [-v]
```

### `atlas check`

Check everything the standard requires and print what is missing. Twelve checks run by default, covering the repository root, the agent guide, the manifest, the README, the forge metadata, the workstreams, the library, and the starter template. A check that does not apply here is reported as skipped, with the reason, so a standard nobody has adopted never looks like a passing one.

```bash
atlas check [-h] [--only IDS] [--list] [--strict] [-C DIR] [--json] [--no-color] [-q] [-v]
```

| Option | Default | Description |
|---|---|---|
| `--only` | — | run only these checks (comma-separated); see --list for the ids |
| `--list` | — | list the available checks and exit |
| `--strict` | — | count skipped checks as failures, for a repository expected to adopt everything |

```bash
atlas check
atlas check --only root-closed-set,manifest
atlas check --list
atlas check --json | jq '.checks[] | select(.state=="fail")'
```

### `atlas validate`

Validate one or more manifests. The schema is chosen from the manifest's own `standard:` field and content, never from its filename, so a manifest is equally valid at examples/acme.org.yaml and at org.yaml. Expired waivers are failures.

```bash
atlas validate [-h] [--all] [-C DIR] [--json] [--no-color] [-q] [-v] [FILE ...]
```

| Argument | Required | Description |
|---|---|---|
| `FILE` | no | manifests to validate |

| Option | Default | Description |
|---|---|---|
| `--all` | — | validate project.yaml plus every manifest in examples/ |

```bash
atlas validate project.yaml
atlas validate examples/*.yaml
atlas validate --all
```

### `atlas work`

Every initiative lives in its own numbered folder with the same nine sections, one accountable owner, and a step where someone records how the result was checked. The Markdown is the original. The dashboard a person reads and the index an agent reads are both generated from the task tables, so progress is counted rather than claimed: a workstream cannot report itself further along than its own tasks say it is.

```bash
atlas work [-h] [-C DIR] [--json] [--no-color] [-q] [-v] <subcommand> ...
```

#### `atlas work new`

Scaffold the next numbered workstream from work/_template and re-sync.

```bash
atlas work new [-h] [--title TITLE] [--owner OWNER] [--summary SUMMARY] [-C DIR] [--json] [--no-color] [-q] [-v] slug
```

| Argument | Required | Description |
|---|---|---|
| `slug` | yes | lowercase-hyphenated name, e.g. migrate-the-fleet |

| Option | Default | Description |
|---|---|---|
| `--title` | — | human title (default: the slug, de-hyphenated) |
| `--owner` | `person:unassigned` | accountable principal, e.g. person:dana or team:platform |
| `--summary` | `` | one sentence on what this workstream is for |

```bash
atlas work new migrate-the-fleet --owner person:dana --title 'Migrate the fleet'
```

#### `atlas work list`

List workstreams with owner, status, and counted progress.

```bash
atlas work list [-h] [--status STATUS] [--owner OWNER] [--archived] [-C DIR] [--json] [--no-color] [-q] [-v]
```

| Option | Default | Description |
|---|---|---|
| `--status` | — | filter by status: active, blocked, review, planned, done, cancelled |
| `--owner` | — | filter by owning principal |
| `--archived` | — | include archived workstreams |

```bash
atlas work list --status blocked
atlas work list --owner person:dana --json
```

#### `atlas work show`

Show a workstream's manifest, task table, agents, and dependencies.

```bash
atlas work show [-h] [--tasks] [-C DIR] [--json] [--no-color] [-q] [-v] id
```

| Argument | Required | Description |
|---|---|---|
| `id` | yes | workstream number or slug |

| Option | Default | Description |
|---|---|---|
| `--tasks` | — | show the full task table |

```bash
atlas work show 01
atlas work show harden-repository-baseline
```

#### `atlas work sync`

Recount progress from the task tables, write it back into each manifest, then regenerate work/index.yaml and work/README.md. Idempotent: reports what changed.

```bash
atlas work sync [-h] [--check] [-C DIR] [--json] [--no-color] [-q] [-v]
```

| Option | Default | Description |
|---|---|---|
| `--check` | — | fail if anything would change, instead of writing (for CI) |

#### `atlas work validate`

Check every workstream: schema, skeleton completeness, id and slug agreement, task-table hygiene, evidence before done, the dependency graph, and whether the generated index is current.

```bash
atlas work validate [-h] [-C DIR] [--json] [--no-color] [-q] [-v]
```

#### `atlas work archive`

Move a done or cancelled workstream into work/archive/ and re-sync.

```bash
atlas work archive [-h] [-C DIR] [--json] [--no-color] [-q] [-v] id
```

| Argument | Required | Description |
|---|---|---|
| `id` | yes | workstream number or slug |

```bash
atlas work archive 01
```

### `atlas spec`

Read the standards from the terminal. Each one opens with machine-readable metadata giving its id, version, status, rule prefixes, and companions, so a tool can discover what the suite covers without reading the prose.

```bash
atlas spec [-h] [-C DIR] [--json] [--no-color] [-q] [-v] <subcommand> ...
```

#### `atlas spec list`

List every standard with the question it answers, its version, and status.

```bash
atlas spec list [-h] [-C DIR] [--json] [--no-color] [-q] [-v]
```

#### `atlas spec show`

Print a standard's prose, or just its metadata or rule identifiers.

```bash
atlas spec show [-h] [--meta] [--rules] [-C DIR] [--json] [--no-color] [-q] [-v] name
```

| Argument | Required | Description |
|---|---|---|
| `name` | yes | standard id, filename stem, or title |

| Option | Default | Description |
|---|---|---|
| `--meta` | — | show only the front matter |
| `--rules` | — | show only the rule identifiers this standard defines |

```bash
atlas spec show workstream
atlas spec show WORKSTREAM --rules
atlas spec show project --meta
```

#### `atlas spec rules`

List every rule identifier across the suite, with the standard that owns it. Use these when citing a rule in a review or a waiver.

```bash
atlas spec rules [-h] [--prefix PREFIX] [-C DIR] [--json] [--no-color] [-q] [-v]
```

| Option | Default | Description |
|---|---|---|
| `--prefix` | — | only rules beginning with this prefix, e.g. W- |

### `atlas prompt`

Browse the prompt library. Each entry is one to three sentences, asks for exactly one thing, and names no particular tool, so it works in any AI assistant or as a request to a colleague. Anything that deletes or overwrites is worded to propose a plan and wait.

```bash
atlas prompt [-h] [-C DIR] [--json] [--no-color] [-q] [-v] <subcommand> ...
```

#### `atlas prompt list`

List prompts with their objective, grouped by lifecycle category.

```bash
atlas prompt list [-h] [--category CATEGORY] [-C DIR] [--json] [--no-color] [-q] [-v]
```

| Option | Default | Description |
|---|---|---|
| `--category` | — | only this category |

```bash
atlas prompt list
atlas prompt list --category releases
```

#### `atlas prompt categories`

List the categories and how many prompts each holds.

```bash
atlas prompt categories [-h] [-C DIR] [--json] [--no-color] [-q] [-v]
```

#### `atlas prompt show`

Print a prompt's text and nothing else, so it pipes cleanly into a clipboard command or another tool.

```bash
atlas prompt show [-h] [--with-context] [-C DIR] [--json] [--no-color] [-q] [-v] id
```

| Argument | Required | Description |
|---|---|---|
| `id` | yes | prompt id, filename stem, or category/id |

| Option | Default | Description |
|---|---|---|
| `--with-context` | — | include the objective and category alongside the text |

```bash
atlas prompt show cut-release
atlas prompt show releases/cut-release | pbcopy
```

#### `atlas prompt search`

Substring search across prompt ids, objectives, categories, and bodies.

```bash
atlas prompt search [-h] [-C DIR] [--json] [--no-color] [-q] [-v] term
```

| Argument | Required | Description |
|---|---|---|
| `term` | yes | what to look for |

```bash
atlas prompt search release
atlas prompt search 'branch protection'
```

### `atlas library`

The library holds things written once and used many times, in four kinds: prompts, icons, typefaces, and media. That list is closed. Adding a fifth kind means amending the specification, which is the difference between a library and a second downloads folder.

```bash
atlas library [-h] [-C DIR] [--json] [--no-color] [-q] [-v] <subcommand> ...
```

#### `atlas library list`

List each asset class, what it holds, and how many assets it carries.

```bash
atlas library list [-h] [--class {icons,media,prompts,typefaces}] [-C DIR] [--json] [--no-color] [-q] [-v]
```

| Option | Default | Description |
|---|---|---|
| `--class` | — | show the assets in one class |

#### `atlas library check`

Verify that every index entry has a file and every file has an index entry, that ids are unique, and that derived or foreign assets declare their source and license.

```bash
atlas library check [-h] [-C DIR] [--json] [--no-color] [-q] [-v]
```

### `atlas site`

The site is generated from the Markdown every time. It is build output: ignored by git, rebuilt in CI, and never edited by hand. Where the site and the Markdown disagree, the Markdown is right and the site is stale.

```bash
atlas site [-h] [-C DIR] [--json] [--no-color] [-q] [-v] <subcommand> ...
```

#### `atlas site build`

Render every specification, document, workstream, prompt, and CLI page into a static site with client-side search, a sitemap, and a 404.

```bash
atlas site build [-h] [--out DIR] [--write-reference] [-C DIR] [--json] [--no-color] [-q] [-v]
```

| Option | Default | Description |
|---|---|---|
| `--out` | — | output directory (default: site/) |
| `--write-reference` | — | also regenerate docs/reference/cli.md from the parser |

```bash
atlas site build
atlas site build --out public --write-reference
```

#### `atlas site serve`

Build the site and serve it on a local port, so links, search, and the 404 behave as they will in production. Ctrl-C to stop.

```bash
atlas site serve [-h] [--port PORT] [--host HOST] [--no-open] [--no-build] [--out DIR] [-C DIR] [--json] [--no-color] [-q] [-v]
```

| Option | Default | Description |
|---|---|---|
| `--port` | `8000` | port to listen on |
| `--host` | `127.0.0.1` | address to bind |
| `--no-open` | — | do not open a browser |
| `--no-build` | — | serve the existing build instead of rebuilding |
| `--out` | — | output directory |

```bash
atlas site serve
atlas site serve --port 8080 --no-open
```

#### `atlas site clean`

Delete the build directory. Nothing here is a source, so nothing is lost.

```bash
atlas site clean [-h] [--out DIR] [-C DIR] [--json] [--no-color] [-q] [-v]
```

| Option | Default | Description |
|---|---|---|
| `--out` | — | output directory |

### `atlas template`

The template is what `atlas init` copies. A few of its files are copies of things this repository already owns, and copies drift, so the direction of flow is fixed and checked in CI: edit the original, then run the sync. A hand-edited copy fails the build instead of surfacing months later in someone else's project.

```bash
atlas template [-h] [-C DIR] [--json] [--no-color] [-q] [-v] <subcommand> ...
```

#### `atlas template check`

Assert that every mirrored file matches its canonical source. Used in CI.

```bash
atlas template check [-h] [-C DIR] [--json] [--no-color] [-q] [-v]
```

#### `atlas template sync`

Copy canonical sources into template/. The only direction of flow.

```bash
atlas template sync [-h] [-C DIR] [--json] [--no-color] [-q] [-v]
```

#### `atlas template list`

List each mirrored file and whether it is currently in sync.

```bash
atlas template list [-h] [-C DIR] [--json] [--no-color] [-q] [-v]
```

### `atlas completion`

Print a completion script for bash, zsh, or fish. Generated from the command tree, so it never suggests a command the tool does not have.

```bash
atlas completion [-h] [-C DIR] [--json] [--no-color] [-q] [-v] {bash,zsh,fish}
```

| Argument | Required | Description |
|---|---|---|
| `shell` | yes | which shell to generate for |

```bash
atlas completion bash > /etc/bash_completion.d/atlas
atlas completion zsh  > ~/.zsh/completions/_atlas
atlas completion fish > ~/.config/fish/completions/atlas.fish
```
