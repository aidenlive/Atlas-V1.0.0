# Deliverables: 01 Harden the repository into a canonical v0.0.1 baseline

Artifacts this workstream produced. Each lives in its permanent home; this
table is the map, not a second copy.

| Deliverable | Home | What it is |
|---|---|---|
| Conventions | [`docs/reference/conventions.md`](../../../docs/reference/conventions.md) | Naming, structure, and terminology rules in one place |
| Glossary | [`docs/reference/glossary.md`](../../../docs/reference/glossary.md) | Every term of art, defined without assuming a reader who codes |
| Rule identifier registry | [`docs/reference/rule-ids.md`](../../../docs/reference/rule-ids.md) | Which prefix belongs to which specification, and why |
| Versioning note | [`docs/reference/versioning.md`](../../../docs/reference/versioning.md) | Why the suite is `0.0.1` while the standards are `1.0` |
| Template mirror generator | `atlas template sync` | Removes 18 hand-maintained duplicate files |
| Design tokens | [`assets/design/tokens.yaml`](../../../assets/design/tokens.yaml) | The consumed 23% of a 118 KB vendored design system |
| Specification metadata tests | [`tests/test_spec_metadata.py`](../../../tests/test_spec_metadata.py) | Front matter, heading trees, ID namespaces, mirror agreement |
| Removal index | `@removal-safe/REMOVAL-INDEX.md` | Every archived file with origin, size, date, SHA-256, and reason |
