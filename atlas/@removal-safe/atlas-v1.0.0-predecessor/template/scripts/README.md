# scripts/

Development and maintenance automation for this repository. Not shipped code —
that lives in `src/`.

The work system, the compliance gates, and the documentation site are provided
by Atlas rather than copied in here, so this repository gets fixes without a
merge:

```bash
pip install atlas-standard

atlas check                  # every compliance gate
atlas work sync              # regenerate the dashboard and index
atlas work new <slug> --owner person:you
atlas site serve             # browse the docs locally
```

Add your own scripts beside this file as the project needs them.
