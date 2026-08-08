# Examples

Worked manifests for the standards, validated on every pull request
(`tests/test_manifests.py`). An example that does not validate is documentation
that lies with confidence, so none of these are hand-checked.

Filenames follow `<slug>.<kind>.yaml`: the slug is the thing the manifest
describes, the kind is the manifest shape. `validate.py` selects the schema from
the manifest's own `standard:` field, never from the filename, so renaming a file
can never change how it is validated.

| File | Kind | Demonstrates |
|---|---|---|
| `lib-package.project.yaml` | project | A public library; the smallest manifest that passes |
| `service-api.project.yaml` | project | A hardened internal service; the `sla-needs-hardening` and `running-needs-runbook` rules |
| `deprecated-tool.project.yaml` | project | The `deprecated-needs-successor` rule, with a sunset date |
| `solo.admin.yaml` | admin | The solo profile: an owner, a successor, and one expiring agent grant |
| `acme.org.yaml` | admin | The organization profile: teams, grants, policies, and agent limits |
| `harden-payments-api.workstream.yaml` | workstream | An orchestrator plus two scoped sub-agents, with declared dependencies |

## Adding one

Add the file, name it `<slug>.<kind>.yaml`, and add a row above. The test suite
picks it up from the directory automatically. There is no list to register it
in, because a list you can forget to update is a list that will be wrong.
