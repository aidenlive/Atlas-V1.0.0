# Starting a new compliant project

## Option A: from the forge

Click **Use this template** on the repository page, then delete everything
except the contents of `template/`, moved to the new repository root.

## Option B: locally

```bash
atlas init my-service ../my-service
cd ../my-service && git init && git add -A
```

The scaffolder substitutes the project name into the README, manifest, banner,
changelog, and forge settings, and refuses names that are not
lowercase-hyphenated.

## What you get

```
README.md          hero visual, title, badges, quickstart: the P-06 composition
project.yaml       manifest stub; classify along all eight MATRIX dimensions
AGENTS.md          seven-section agent guide; fill in commands and constraints
CLAUDE.md          three-line vendor stub
CHANGELOG.md       Keep a Changelog, with an Unreleased section
CONTRIBUTING.md    branch → PR → CI → review → squash
LICENSE            placeholder; choose before going public
assets/banner.svg  branded placeholder hero
docs/decisions/    ADR-0001 establishing the practice
work/              the work management system, ready to run
atlas work    new · sync · validate · archive
src/ tests/        source root and its mirror
.github/           CI workflow stub and settings as code
```

## First five minutes

1. Set `type`, `owner`, and `visibility` in `project.yaml`; validate it.
2. Write the one-line value proposition once, and use the same sentence in
   `metadata.description`, the README title, and `.github/settings.yml`.
3. Replace the placeholder banner with a real hero visual.
4. Fill in the build, test, and lint commands in `AGENTS.md`, and run them,
   so they are copy-paste true.
5. Wire CI, then claim a maturity level only once its profile passes.
6. Open your first workstream: `atlas work new <slug> --owner person:you`.

Prompts for each step live in [`library/prompts/repository/`](../../library/prompts/repository/).
