# Security policy

## Scope

Atlas is a documentation standard and a command-line tool. It reads files, and
it writes only where you tell it to. It makes no network requests, runs no code
from the repositories it checks, and holds no credentials.

The realistic risks are therefore small but not zero:

- A crafted manifest or Markdown file causing the tool to read outside the
  repository, or to hang.
- A dependency vulnerability in `PyYAML` or `jsonschema`.
- A generated file whose contents come from a manifest and are rendered
  somewhere that trusts them.

## Supported versions

The most recent minor release of `atlas-editorial` receives fixes.

## Reporting

Report privately to `security@example.com`. Include the version, the input that
triggers it, and what you observed.

Do not open a public issue for an unfixed vulnerability.

## What to expect

| When | What |
|---|---|
| Within 3 working days | Acknowledgement that a person has it |
| Within 10 working days | An assessment, and a fix or a plan with a date |
| On release | A changelog entry, and credit if you want it |

## Out of scope

The content of repositories that use Atlas. If a document should not have been
published, that is an editorial failure, not a tooling vulnerability — see
AUTHORITY for who answers for it.
