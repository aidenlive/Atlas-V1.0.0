# 0001: The repository governs itself by the standard it defines

Date: 2026-08-07 · Status: Accepted

## Context
The suite claims that declared, machine-checked structure beats promised
structure. A standards repository that is exempt from its own rules cannot
credibly make that claim, and gives adopters no worked example.

## Decision
This repository is a PROJECT.md-compliant `content.spec` project: closed root,
manifest, canonical AGENTS.md with vendor stubs, CI-enforced compliance,
Conventional Commits, SemVer tags. `spec/` is the declared source root
(the standard's "ecosystem idiom" clause).

## Consequences
Every normative change is exercised against a real repo immediately; the repo
doubles as the reference implementation; and any rule too painful to obey here
is a signal to fix the rule, not to grant ourselves an exemption.
