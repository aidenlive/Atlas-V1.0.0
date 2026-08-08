# Requirements: 02 Rebrand to Atlas and ship a first-class CLI

| ID | Requirement | Rationale | Met |
|---|---|---|---|
| R-01 | The eight specifications are byte-unchanged in normative content | A rebrand that edits the contract teaches adopters not to upgrade | yes |
| R-02 | Every operation is reachable from one discoverable command | Discovery by directory listing is not discovery | yes |
| R-03 | Every read command emits valid JSON under `--json` | Agents consume this; a stray human line breaks them silently | yes |
| R-04 | Exit codes distinguish "found violations" from "bad usage" | A CI job must not report a red build for the wrong reason | yes |
| R-05 | All logic is importable and unit-testable without a terminal | The compliance checks previously had no tests at all | yes |
| R-06 | The CLI reference is generated, and CI fails on a stale copy | Hand-written reference drifts silently | yes |
| R-07 | The repository still passes its own standard | ADR-0001: self-hosting | yes |
| R-08 | A bare checkout works with no install | CI containers, hooks, fresh clones | yes |
| R-09 | The template carries no executable copy of the tooling | A copy is a fork with a delay | yes |
| R-10 | Status is never conveyed by color alone, in terminal or site | WCAG 1.4.1, and build logs are monochrome | yes |
