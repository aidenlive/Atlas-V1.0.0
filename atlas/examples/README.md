# Examples

Worked manifests, validated in CI. Each one is a real, valid file — copy it and
change the facts rather than starting from an empty document.

| File | Shows |
|---|---|
| `handbook.project.yaml` | An internal handbook, maintained, several audiences |
| `marketing-site.project.yaml` | Public marketing content with tight approvals |
| `small-team.authority.yaml` | The smallest authority file that still has two approvers |
| `launch-guide.workstream.yaml` | A workstream mid-flight, with a target date |
| `published-guide.md` | Front matter for a published document |
| `needs-work.md` | A deliberately flawed draft — run the linter on it to see every rule fire |

Validate them the way CI does:

```bash
atlas validate examples/handbook.project.yaml
atlas validate examples/small-team.authority.yaml --kind authority
```

`needs-work.md` is the before to `published-guide.md`'s after. It is the file in
the README's screenshot, and it is where new rules get their first test:

```bash
atlas lint examples/needs-work.md -v
```
