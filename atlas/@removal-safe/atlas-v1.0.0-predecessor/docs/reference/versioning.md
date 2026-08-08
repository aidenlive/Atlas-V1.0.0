# Versioning

Two version numbers appear in this repository and they mean different things.
Conflating them is the mistake this page exists to prevent.

## The suite release version

**`1.0.0`.** The version of *this repository*: its tooling, its documentation,
its template, its packaging. It appears in `CHANGELOG.md`, in the README badge,
in `pyproject.toml`, in `atlas.__version__`, and as the git tag `v1.0.0`.

It follows [SemVer](https://semver.org), and it versions **the tooling's public
surface**: the CLI's commands, flags, exit codes, and `--json` payloads, plus
the importable `atlas.core` and `atlas.site` API. Removing a command, renaming a
flag, or changing an exit code's meaning is a major. Adding a command or a flag
is a minor.

The human-readable terminal output is deliberately *outside* that promise. It
changes whenever we can make it clearer, which is why agents and scripts should
consume `--json`.

## The standard contract version

**`project/1.0`, `workstream/1.0`, `admin/1.0`.** The version of the
*contract* a manifest is written against. It appears as the `standard:` field at
the top of every manifest, and as a `const` in every JSON Schema.

This is an interface identifier, not a release number. `atlas validate`
selects a schema by reading it. A manifest that says `standard: project/1.0` is
making a promise about its own shape, and thousands of manifests across a fleet
may be making that promise. Renumbering it to match the repository's release
version would invalidate every one of them for no gain.

So the two move independently, and they should:

| Change | Suite version | Standard version |
|---|---|---|
| Fix a typo in a guide | patch | unchanged |
| Add a script | minor | unchanged |
| Add an optional field to a manifest | minor | minor (`project/1.1`) |
| Remove or repurpose a manifest field | major | major (`project/2.0`) |
| Add a normative rule that makes a compliant repo non-compliant | major | minor or major |

## What bumps the suite

- **PATCH.** Editorial only. Typos, clarity, examples, non-behavioural tooling.
- **MINOR.** New capability, or a normative change that no compliant repository
  fails.
- **MAJOR.** Any change that makes a previously compliant repository
  non-compliant, or any removal from a manifest shape.

A normative change is **never** a patch. If it changes what compliance means, it
is at minimum a minor.

## Maturity is not a version

`maturity:` in `project.yaml` is a separate axis again: it says how much this
repository can be trusted, and it is earned by passing the matching CHECKLIST
profile. A `1.0.0` release of something untested is still `experimental`, and a
`0.0.1` release with full CI can honestly be `beta`.

The current state is `v1.0.0`, `maturity: stable`. Both moved at the same time
and for the same reason, which is a coincidence worth naming so it is not read
as a rule: `1.0.0` because the CLI's surface is now a promise worth breaking
compatibility over, and `stable` because the Production profile passes —
packaged and installable, a public API, a generated reference that CI proves
current, and the suite enforcing itself.

Earlier drafts badged `1.0.0` and `stable` on a repository whose own ladder did
not support either; `v0.0.1` / `beta` was the correction. The claim is only
worth making when the checks behind it pass.

## Releasing

1. Move `Unreleased` entries under a new version heading and set the date, and
   add the comparison link at the foot of the changelog.
2. Update the version in `pyproject.toml` and `src/atlas/__init__.py`, the badge
   in `README.md`, and `maturity:` in `project.yaml` if the CHECKLIST profile it
   claims has changed.
3. Update `version:` in the front matter of any specification whose normative
   text changed, and the matching `const` in its JSON Schema, in the same
   change-set.
4. Run `atlas check` and `atlas site build --write-reference`; both must leave
   the tree clean.
5. Tag `vX.Y.Z`. The tag is the source of truth for what shipped.
6. Publish: `python -m build && python -m twine upload dist/*`.
